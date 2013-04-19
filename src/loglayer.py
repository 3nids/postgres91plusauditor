from PyQt4.QtCore import QCoreApplication, pyqtSignal, QObject
from qgis.core import QgsMapLayerRegistry, QgsFeature, QgsFeatureRequest, QgsDataSourceURI


from mysettings import MySettings
from logresults import LogResults, LogResultRow

# tuplets for settings, display name, and row-data property
columnVarSetting    = ("displayColumnDate", "displayColumnUser", "displayColumnAction", "displayColumnChangedGeometry", "displayColumnChangedFields", "displayColumnApplication", "displayColumnClientIP", "displayColumnClientPort")
columnFancyName     = ("Date"             , "User"             , "Action"             , "G"                           , "Fields"                    , "Application"             , "Client IP"            , "Client port")
columnRowName       = ("dateStr"          , "user"             , "action"             , "changedGeometry"             , "changedFields"             , "application"             , "clientIP"             , "clientPort")


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

        # set query subset for layer to drastically improve search speed
        if self.settings.value("redefineSubset"):
            subset = "schema_name = '%s' and table_name = '%s'" % (dataUri.schema(), dataUri.table())
            if not self.layer.setSubsetString(subset):
                raise NameError("Subset could not be set.")

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
            if logFeature.attribute("schema_name").toString() == dataUri.schema() and \
               logFeature.attribute("table_name").toString() == dataUri.table():
                row = LogResultRow(logFeature, layerFeature, pkeyName, geomColumn)
                if featureId == 0 or row.logFeatureId == featureId:
                    self.results.addRow(row)
            k += 1
        if self.settings.value("redefineSubset"):
            self.layer.setSubsetString("")




