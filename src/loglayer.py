from PyQt4.QtCore import QCoreApplication, QString, pyqtSignal, QObject
from qgis.core import QgsMapLayerRegistry, QgsFeature, QgsFeatureRequest, QgsDataSourceURI
import re

from ..mysettings import MySettings

# tuplets for settings, display name, and row-data property
columnVarSetting    = ("displayColumnDate","displayColumnUser","displayColumnAction","displayColumnChangedGeometry","displayColumnChangedFields","displayColumnApplication","displayColumnClientIP","displayColumnClientPort")
columnFancyName     = ("Date"             ,"User"             ,"Action"             ,"G"                           ,"Fields"                    ,"Application"             ,"Client IP"            ,"Client port")
columnRowName       = ("dateStr"          ,"user"             ,"action"             ,"changedGeometry"             ,"changedFields"             ,"application"             ,"clientIP"             ,"clientPort")

# regexp to parse data from hstore
fieldRe = lambda(fieldName): re.compile('("%s"|%s)\s*=\>\s*' % (fieldName, fieldName))
dataReWithQuote = re.compile('\s*".*?[^\\\\]"')
dataReWithoutQuote = re.compile('.*?, ')


def getFieldValue(data, fieldName):
    p = fieldRe(fieldName).search(data)
    if p:
        data = data[p.end():]
        p = dataReWithQuote.match(data)
        if p:
            return data[p.start()+1:p.end()-1]
        p = dataReWithoutQuote.match(data)
        if p:
            return data[p.start():p.end()-1]
    return None


class LogLayer(QObject):
    setProgressMax = pyqtSignal(int)
    setProgressMin = pyqtSignal(int)
    setProgressValue = pyqtSignal(int)

    def __init__(self):
        QObject.__init__(self)
        self.settings = MySettings()
        self.results = LogResults()
        self.continueSearch = True
        self.layer = None

    def isValid(self):
        self.layer = QgsMapLayerRegistry.instance().mapLayer(self.settings.value("logLayer"))
        return self.checkLayer(self.layer)

    def checkLayer(self, layer):
        if layer is None:
            return False
            # TODO check validity

        return True

    def interrupt(self):
        self.continueSearch = False

    def performSearch(self, layer, featureId, pkeyName, onlyGeometry=False):
        self.results.clear()
        if not self.isValid():
            return None

        dataUri = QgsDataSourceURI(layer.dataProvider().dataSourceUri())
        geomColumn = dataUri.geometryColumn()

        layerFeature = QgsFeature()
        if featureId != 0:
            featReq = QgsFeatureRequest().setFilterFid(featureId)
            if not layer.hasGeometryType():
                featReq.setFlags(QgsFeatureRequest.NoGeometry)
            if layer.getFeatures(featReq).nextFeature(layerFeature) is False:
                return None
        else:
            layerFeature.setFields(layer.dataProvider().fields())
        self.results.setFeature(layerFeature)
        
        if self.settings.value("redefineSubset"):
            subset = "schema_name = %s and table_name = %s" % (dataUri.schema(), dataUri.table())
            self.layer.setSubsetString(subset)

        self.continueSearch = True
        logFeature = QgsFeature()
        featReq = QgsFeatureRequest().setFlags(QgsFeatureRequest.NoGeometry)
        iterator = self.layer.getFeatures(featReq)
        self.setProgressMin.emit(0)
        self.setProgressMax.emit(self.layer.featureCount())
        k = 0
        while iterator.nextFeature(logFeature):
            self.setProgressValue.emit(k)
            QCoreApplication.processEvents()
            if not self.continueSearch:
                break
            if logFeature.attribute("schema_name").toString() == dataUri.schema() and logFeature.attribute("table_name").toString() == dataUri.table():
                row = LogResultRow(logFeature, layerFeature, pkeyName, geomColumn)
                if featureId == 0 or row.logFeatureId == featureId:
                    self.results.addRow(row)
            k += 1
        if self.settings.value("redefineSubset"):
            self.layer.setSubsetString("")



class LogResults(dict):
    def __init__(self):
        self.layerFeature = QgsFeature()

    def geometry(self):
        self.layerFeature.geometry()

    def clear(self):
        dict.clear(self)

    def setFeature(self, layerFeature):
        self.layerFeature = layerFeature

    def addRow(self, row):
        self[row.dateMs] = row


class LogResultRow():
    def __init__(self, logFeature, layerFeature, pkeyName, geomColumn):
        self.fields = layerFeature.fields()
        self.logFeature = QgsFeature(logFeature)
        self.geomColumn = geomColumn
        self.date = logFeature.attribute("action_tstamp_tx").toDateTime()
        self.dateMs = self.date.toMSecsSinceEpoch()
        self.logData = self.logFeature.attribute("row_data").toString()
        self.logFeatureId = getFieldValue(self.logData, pkeyName).toInt()[0]

    def dateStr(self):
        return self.date.toString("ddd dd MMM yyyy hh:mm")

    def user(self):
        return self.logFeature.attribute("session_user_name").toString()

    def action(self):
        action = self.logFeature.attribute("action").toString()
        if action == "I":
            return "insert"
        if action == "U":
            return "update"
        if action == "D":
            return "delete"
        raise NameError("Invalid action %s" % action)

    def application(self):
        return self.logFeature.attribute("application_name").toString()

    def clientIP(self):
        return self.logFeature.attribute("client_addr").toString()

    def clientPort(self):
        return self.logFeature.attribute("client_port").toString()

    def changedFields(self):
        data = self.logFeature.attribute("changed_fields").toString()
        columns = ""
        for field in self.fields:
            if getFieldValue(data, field.name()) is not None:
                columns += field.name() + ", "
        return columns[:-2]

    def changedGeometry(self):
        data = self.logFeature.attribute("changed_fields").toString()
        geometry = getFieldValue(data, self.geomColumn)
        if geometry is None:
            return ""
        else:
            return QString(u"\u2713")  # check sign

    def data(self):
        out = dict()
        for field in self.fields:
            out[field.name()] = getFieldValue(self.logData, field.name())
        return out


