from qgis.core import QgsMapLayerRegistry, QgsAction
from PyQt4.QtCore import QUrl
from PyQt4.QtGui import QAction, QIcon, QDesktopServices

from gui.auditdialog import AuditDialog
from gui.loggedactionstablechooserdialog import LoggedActionsTableChooserDialog

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
                                          "Define logged actions table", self.iface.mainWindow())
        self.connectLayerAction.triggered.connect(self.showLogLayerChooser)
        self.iface.addPluginToMenu("&Postgres 91 plus Auditor", self.connectLayerAction)
        # show history action
        self.auditAction = QAction(QIcon(":/plugins/postgres91plusauditor/icons/qaudit-64.png"),
                                   "Audit logged actions", self.iface.mainWindow())
        self.auditAction.triggered.connect(self.audit)
        self.iface.addToolBarIcon(self.auditAction)
        self.iface.addPluginToMenu("&Postgres 91 plus Auditor", self.auditAction)
        # help action
        self.helpAction = QAction(QIcon(":/plugins/postgres91plusauditor/icons/help.png"),
                                  "Help", self.iface.mainWindow())
        self.helpAction.triggered.connect(lambda: QDesktopServices.openUrl(QUrl("http://3nids.github.io/postgres91plusauditor/")))
        self.iface.addPluginToMenu("&Postgres 91 plus Auditor", self.helpAction)

    def unload(self):
        self.iface.removePluginMenu("&Postgres 91 plus Auditor", self.connectLayerAction)
        self.iface.removePluginMenu("&Postgres 91 plus Auditor", self.auditAction)
        self.iface.removePluginMenu("&Postgres 91 plus Auditor", self.helpAction)
        self.iface.removeToolBarIcon(self.auditAction)
        for layer in QgsMapLayerRegistry.instance().mapLayers().values():
            if layer.dataProvider().name() == "postgres":
                actions = layer.actions()
                for i in range(actions.size()):
                    if actions[i].name() == actionName:
                        actions.removeAction(i)

    def showLogLayerChooser(self):
        LoggedActionsTableChooserDialog().exec_()

    def audit(self, layerId=None, featureId=None):
        if layerId is False:
            layerId = None
        self.auditDlg = AuditDialog(self.iface, layerId, featureId)
        self.auditDlg.show()

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
