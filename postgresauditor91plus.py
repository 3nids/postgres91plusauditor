from qgis.core import *

from showhistory import ShowHistoryDialog
from mysettings import LogLayerChooserDialog

actionName = "History audit"


class PostgresAuditor91plus():
    def __init__(self, iface):
        self.iface = iface
        QgsMapLayerRegistry.instance().layersAdded.connect(self.addLayersActions)
        self.addLayersActions()

    def initGui(self):
        self.connectLayerAction = QAction(QIcon(":/plugins/itembrowser/icons/connect.png"), "Define logged actions layer", self.iface.mainWindow())
        self.connectLayerAction.triggered.connect( LogLayerChooserDialog().exec_)
        self.iface.addToolBarIcon(self.connectLayerAction)
        self.iface.addPluginToMenu("&Postgres Auditor 91 plus", self.connectLayerAction)

    def unload(self):
        for layerid, layer in QgsMapLayerRegistry.instance().mapLayers().iteritems():
            if layer.dataProvider().name() == "postgres":
                actionExists = False
                actions = layer.actions()
                for i in range(actions.size()):
                    action = actions.at(i)
                    if action.name() == actionName:
                        actions.removeAction(i)


    def addLayersActions(self):
        for layerid, layer in QgsMapLayerRegistry.instance().mapLayers().iteritems():
            if layer.dataProvider().name() == "postgres":
                actionExists = False
                actions = layer.actions()
                for i in range(actions.size()):
                    action = actions.at(i)
                    if action.name() == actionName:
                        actionExists = True
                        break
                if actionExists:
                    break

                actionStr = "qgis.utils.plugins['postgresauditor91plus'].showHistory('%s',[%% $id %%])" % layerid

                actions.addAction(QgsAction.GenericPython, actionName, actionStr)



    def showHistory(self, layerId, featureId):
        ShowHistoryDialog(self.iface.legendInterface(),layerId, featureId).exec_()
        print layerId, featureId



     # QgsDataSourceURI(layer.dataProvider().dataSourceUri()).geometryColumn()



