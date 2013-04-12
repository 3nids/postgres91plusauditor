from qgis.core import *
from mysettings import MySettings
import re

class LogLayer():
    def __init__(self):
        self.settings = MySettings()


    def isValid(self):
        self.logLayer = QgsMapLayerRegistry.instance().mapLayer( self.settings.value("logLayer") )
        return self.checkLayer(self.logLayer)

    def checkLayer(self, layer):
        if layer is None:
            return False
            # TODO check validity

        return True


    def performSearch(self, layer, featureId, pkeyName, onlyGeometry=False):
        if not self.isValid():
            return None

        dataUri = QgsDataSourceURI(layer.dataProvider().dataSourceUri())
        geomColumn = dataUri.geometryColumn()

        currentFeature = QgsFeature()
        featReq = QgsFeatureRequest().setFilterFid( featureId )
        if not layer.hasGeometryType():
            featReq.setFlags( QgsFeatureRequest.NoGeometry )
        if layer.getFeatures( featReq ).nextFeature( currentFeature ) is False:
            return None

        logFeature = QgsFeature()
        featReq = QgsFeatureRequest().setFlags( QgsFeatureRequest.NoGeometry )
        iterator = self.logLayer.getFeatures( featReq )
        while iterator.nextFeature( logFeature ):
            if logFeature.attribute("schema_name").toString() == dataUri.schema() and logFeature.attribute("table_name").toString() == dataUri.table():
                data = logFeature.attribute("row_data").toString()
                id = self.getAttribute(data, pkeyName)
                if id is not None:
                    print data



    def getAttribute(self, data, fieldName):
        regex = re.compile( '("%s"|%s)\s*=\>\s*' % (fieldName,fieldName) )
        p = regex.search(data)
        if p:
            data = data[p.end():]
            dataReWithQuote = re.compile('\s*".*?[^\\\\]"')
            p =  dataReWithQuote.match(data)
            if p:
                return data[p.start()+1:p.end()-1]
            dataReWithoutQuote = re.compile('.*?"')
            p = dataReWithoutQuote.match(data)
            if p:
                return data[p.start()+1:p.end()-1]
        return None


