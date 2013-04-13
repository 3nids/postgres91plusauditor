from qgis.core import *
from mysettings import MySettings
import re


columnVarSetting    = ("displayColumnDate","displayColumnUser","displayColumnAction","displayColumnChangedFields","displayColumnApplication","displayColumnClientIP")
columnFancyName     = ("Date"             ,"User"             ,"Action"             ,"Fields"                    ,"Application"             ,"Client IP:port"       )
columnRowName       = ("dateStr"          ,"user"             ,"action"             ,"changedFields"             ,"application"             ,"clientIPport"         )



def getFieldValue(data, fieldName):
    regex = re.compile( '("%s"|%s)\s*=\>\s*' % (fieldName,fieldName) )
    p = regex.search(data)
    if p:
        data = data[p.end():]
        dataReWithQuote = re.compile('\s*".*?[^\\\\]"')
        p =  dataReWithQuote.match(data)
        if p:
            return data[p.start()+1:p.end()-1]
        dataReWithoutQuote = re.compile('.*?,')
        p = dataReWithoutQuote.match(data)
        if p:
            return data[p.start():p.end()-1]
    return None


class LogLayer():
    def __init__(self):
        self.settings = MySettings()
        self.results = LogResults()


    def isValid(self):
        self.logLayer = QgsMapLayerRegistry.instance().mapLayer( self.settings.value("logLayer") )
        return self.checkLayer(self.logLayer)

    def checkLayer(self, layer):
        if layer is None:
            return False
            # TODO check validity

        return True

    def performSearch(self, layer, featureId, pkeyName, onlyGeometry=False):
        self.results.clear()
        if not self.isValid():
            return None

        dataUri = QgsDataSourceURI(layer.dataProvider().dataSourceUri())
        geomColumn = dataUri.geometryColumn()

        layerFeature = QgsFeature()
        if featureId != 0:
            featReq = QgsFeatureRequest().setFilterFid( featureId )
            if not layer.hasGeometryType():
                featReq.setFlags( QgsFeatureRequest.NoGeometry )
            if layer.getFeatures( featReq ).nextFeature( layerFeature ) is False:
                return None
        else:
            layerFeature.setFields( layer.dataProvider().fields() )
        self.results.setFeature(layerFeature)

        logFeature = QgsFeature()
        featReq = QgsFeatureRequest().setFlags( QgsFeatureRequest.NoGeometry )
        iterator = self.logLayer.getFeatures( featReq )
        while iterator.nextFeature( logFeature ):
            if logFeature.attribute("schema_name").toString() == dataUri.schema() and logFeature.attribute("table_name").toString() == dataUri.table():
                row = LogResultRow(logFeature, layerFeature, pkeyName)
                if featureId == 0 or row.logFeatureId == featureId:
                    self.results.addRow(row)


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
        self[row.date] = row



class LogResultRow():
    def __init__(self, logFeature, layerFeature, pkeyName):
        date    = logFeature.attribute("action_tstamp_tx").toDateTime()
        logData = logFeature.attribute("row_data").toString()
        self.date    = date.toMSecsSinceEpoch()
        self.dateStr = date.toString("ddd dd MMM yyyy hh:mm")
        self.user          = logFeature.attribute("session_user_name").toString()
        self.application   = logFeature.attribute("application_name").toString()
        self.clientIPport  = logFeature.attribute("client_addr").toString()+":"+logFeature.attribute("client_port").toString()
        self.action        = logFeature.attribute("action").toString()
        self.changedFields = logFeature.attribute("changed_fields").toString()

        self.logFeatureId = getFieldValue(logData, pkeyName).toInt()[0]

        self.data = dict()
        for field in layerFeature.fields():
            self.data[field.name()] = getFieldValue(logData, field.name())


