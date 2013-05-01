from qgis.core import *
from PyQt4.QtGui import QAction, QIcon

from gui.auditdialog import AuditDialog
from gui.loglayerchooserdialog import LogLayerChooserDialog

actionName = "History audit"
pluginName = "postgres91plusauditor"

import resources

# run manually qgis.utils.plugins["postgres91plusauditor"].audit("district20130425093453834",1)


class Postgres91plusAuditor():
    def __init__(self, iface):
        self.iface = iface
        QgsMapLayerRegistry.instance().layersAdded.connect(self.addLayersActions)
        self.addLayersActions()

    def initGui(self):
        # log layer chooser
        self.connectLayerAction = QAction(QIcon(":/plugins/postgres91plusauditor/icons/connect.png"),
                                          "Define logged actions layer", self.iface.mainWindow())
        self.connectLayerAction.triggered.connect(self.showLogLayerChooser)
        self.iface.addPluginToMenu("&Postgres 91 plus Auditor", self.connectLayerAction)
        # show history action
        self.auditAction = QAction(QIcon(":/plugins/postgres91plusauditor/icons/qaudit-64.png"),
                                         "Audit logged actions", self.iface.mainWindow())
        self.auditAction.triggered.connect(self.audit)
        self.iface.addToolBarIcon(self.auditAction)
        self.iface.addPluginToMenu("&Postgres 91 plus Auditor", self.auditAction)

    def unload(self):
        self.iface.removePluginMenu("&Postgres 91 plus Auditor", self.connectLayerAction)
        self.iface.removePluginMenu("&Postgres 91 plus Auditor", self.auditAction)
        self.iface.removeToolBarIcon(self.auditAction)
        for layerid, layer in QgsMapLayerRegistry.instance().mapLayers().iteritems():
            if layer.dataProvider().name() == "postgres":
                actions = layer.actions()
                for i in range(actions.size()):
                    action = actions.at(i)
                    if action.name() == actionName:
                        actions.removeAction(i)

    def showLogLayerChooser(self):
        LogLayerChooserDialog(self.iface.legendInterface()).exec_()

    def audit(self, layerId=None, featureId=None):
        if layerId is False:
            layerId = None
        AuditDialog(self.iface, layerId, featureId).exec_()

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

                actionStr = "qgis.utils.plugins['%s'].audit('%s',[%% $id %%])" % (pluginName, layerid)

                actions.addAction(QgsAction.GenericPython, actionName, actionStr)
