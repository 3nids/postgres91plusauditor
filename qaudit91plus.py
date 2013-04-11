from qgis.core import *

actionName = "History audit"


class Qaudit91plus():
    def __init__(self, iface):
        self.iface = iface
        QgsMapLayerRegistry.instance().layersAdded.connect(self.addLayersActions)
        self.addLayersActions()

    def addLayersActions(self):
        for layerid, layer in QgsMapLayerRegistry.instance.mapLayers().iteritems():
            if layer.dataProvider().name() == "postgres":
                actionExists = False
                for i in range(actions.size()):
                    action = actions.at(i)
                    if action.name() == actionName:
                        actionExists = True
                        break
                if actionExists:
                    break

                actionStr = "qgis.utils.plugins['qaudit91plus'].showHistory('%s',[%% $id %%])" % layerid

                actions.addAction(QgsAction.GenericPython, actionName, actionStr)



    def showHistory(self, layerId, featureId):
        print layerId, featureId



     # QgsDataSourceURI(layer.dataProvider().dataSourceUri()).geometryColumn()



