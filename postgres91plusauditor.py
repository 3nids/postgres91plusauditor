from qgis.core import *
from PyQt4.QtGui import QAction,QIcon

from showhistory import ShowHistoryDialog
from mysettings import LogLayerChooserDialog

actionName = "History audit"
pluginName = "postgres91plusauditor"


class Postgres91plusAuditor():
    def __init__(self, iface):
        self.iface = iface
        QgsMapLayerRegistry.instance().layersAdded.connect(self.addLayersActions)
        self.addLayersActions()

    def initGui(self):
        # log layer chooser
        self.connectLayerAction = QAction(QIcon(":/plugins/postgres91plusauditor/icons/connect.png"), "Define logged actions layer", self.iface.mainWindow())
        self.connectLayerAction.triggered.connect( LogLayerChooserDialog(self.iface.legendInterface()).exec_ )
        self.iface.addPluginToMenu("&Postgres 91 plus Auditor", self.connectLayerAction)
        # show history action
        self.showHistoryAction = QAction(QIcon(":/plugins/postgres91plusauditor/icons/qaudit-64.png"), "Audit logged actions", self.iface.mainWindow())
        self.showHistoryAction.triggered.connect( ShowHistoryDialog(self.iface.legendInterface()).exec_ )
        self.iface.addToolBarIcon(self.showHistoryAction)
        self.iface.addPluginToMenu("&Postgres 91 plus Auditor", self.showHistoryAction)

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

                actionStr = "qgis.utils.plugins['%s'].showHistory('%s',[%% $id %%])" % (pluginName, layerid)

                actions.addAction(QgsAction.GenericPython, actionName, actionStr)



    def showHistory(self, layerId, featureId):
        ShowHistoryDialog(self.iface.legendInterface(),layerId, featureId).exec_()
        print layerId, featureId



     # QgsDataSourceURI(layer.dataProvider().dataSourceUri()).geometryColumn()



