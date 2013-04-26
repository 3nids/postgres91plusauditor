from PyQt4.QtCore import QCoreApplication, pyqtSignal, QObject, QDateTime
from qgis.core import QgsMapLayerRegistry, QgsFeature, QgsFeatureRequest, QgsDataSourceURI


from mysettings import MySettings
from logresultrow import LogResultRow

# tuplets for settings, display name, and row-data property
columnVarSetting    = ("displayColumnDate", "displayColumnUser", "displayColumnAction", "displayColumnChangedGeometry", "displayColumnChangedFields", "displayColumnApplication", "displayColumnClientIP", "displayColumnClientPort")
columnFancyName     = ("Date"             , "User"             , "Action"             , "G"                           , "Fields"                    , "Application"             , "Client IP"            , "Client port")
columnRowName       = ("dateStr"          , "user"             , "action"             , "changedGeometryStr"          , "changedFields"             , "application"             , "clientIP"             , "clientPort")


class LogLayer(QObject):
    setProgressMax = pyqtSignal(int)
    setProgressMin = pyqtSignal(int)
    setProgressValue = pyqtSignal(int)

    def __init__(self):
        QObject.__init__(self)
        self.settings = MySettings()
        self.results = dict()
        self.continueSearch = True
        self.layer = None
        self.layerFeature = QgsFeature()

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

    def performSearch(self, featureLayer, featureId, pkeyName, searchInserts, searchUpdates, searchDeletes,
                      searchOnlyGeometry, searchAfterDate, searchBeforeDate):
        self.results.clear()
        if not self.isValid():
            return

        dataUri = QgsDataSourceURI(featureLayer.dataProvider().dataSourceUri())
        if featureLayer.hasGeometryType():
            geomColumn = dataUri.geometryColumn()
        else:
            geomColumn = None

        # initiate the layer feature (feature at given ID, or an empty feature otherwise)
        self.layerFeature = QgsFeature()
        noGeometry = False
        if featureId != 0:
            featReq = QgsFeatureRequest().setFilterFid(featureId)
            if not featureLayer.hasGeometryType():
                noGeometry = True
                featReq.setFlags(QgsFeatureRequest.NoGeometry)
            if featureLayer.getFeatures(featReq).nextFeature(self.layerFeature) is False:
                self.layerFeature.setFields(featureLayer.dataProvider().fields())
        else:
            fields = featureLayer.dataProvider().fields()
            self.layerFeature.setFields(fields)

        # set query subset for layer to drastically improve search speed
        # todo: if a subset already exists, should give a warning
        if self.settings.value("redefineSubset"):
            subset = "schema_name = '%s' and table_name = '%s'" % (dataUri.schema(), dataUri.table())
            if not searchInserts or not searchUpdates or not searchDeletes:
                subset += "and ("
                if searchInserts:
                    subset += " action = 'I' or"
                if searchUpdates:
                    subset += " action = 'U' or"
                if searchDeletes:
                    subset += " action = 'D' or"
                subset = subset[:-3] + ")"
            if not searchAfterDate.isNull():
                subset += " and action_tstamp_tx >= '%s'" % searchAfterDate.toString("yyyy-MM-dd hh:mm:ss")
            if not searchBeforeDate.isNull():
                subset += " and action_tstamp_tx <= '%s'" % searchBeforeDate.toString("yyyy-MM-dd hh:mm:ss")

            print subset, searchAfterDate

            if not self.layer.setSubsetString(subset):
                raise NameError("Subset could not be set.")

            print self.layer.subsetString()

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
               logFeature.attribute("table_name").toString() == dataUri.table() and \
               (searchInserts and logFeature.attribute("action") == 'I' or
                searchUpdates and logFeature.attribute("action") == 'U' or
                searchDeletes and logFeature.attribute("action") == 'D') and \
               (searchAfterDate.isNull() or logFeature.attribute("action_tstamp_tx").toDateTime() >= searchAfterDate.toString("yyyy-MM-dd hh:mm:ss")) and \
               (searchBeforeDate.isNull() or logFeature.attribute("action_tstamp_tx").toDateTime() <= searchBeforeDate.toString("yyyy-MM-dd hh:mm:ss")):
                row = LogResultRow(logFeature, self.layerFeature, pkeyName, geomColumn)
                if featureId != 0 and row.logFeatureId != featureId:
                    continue
                if searchOnlyGeometry and not row.changedGeometry():
                    continue

                self.results[row.dateMs] = row
            k += 1
        if self.settings.value("redefineSubset"):
            self.layer.setSubsetString("")




