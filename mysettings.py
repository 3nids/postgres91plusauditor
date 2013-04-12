"""
Postgres Auditor 91 plus
QGIS plugin

Denis Rouzaud
denis.rouzaud@gmail.com
"""
from PyQt4.QtGui import QDialog

from qgistools.pluginsettings import *
from qgistools.gui import VectorLayerCombo

from ui.ui_loglayerchooser import Ui_LogLayerChooser
from loglayer import LogLayer
pluginName = "postgres91plusauditor"


mySettings = [
    # global settings
    Bool(pluginName,"displayColumnChangedFields", "global", True ),
    Bool(pluginName,"displayColumnAction       ", "global", True ),
    Bool(pluginName,"displayColumnDate         ", "global", True ),
    Bool(pluginName,"displayColumnUser         ", "global", True ),
    Bool(pluginName,"displayColumnApplication  ", "global", False ),
    Bool(pluginName,"displayColumnClientIP     ", "global", False ),
    Bool(pluginName,"searchOnlyGeometry        ", "global", False ),

    # project
    String(pluginName, "logLayer", "project", "")
]

class IntersectItSettings(PluginSettings):
    def __init__(self):
        PluginSettings.__init__(self, pluginName, mySettings)


class LogLayerChooserDialog(QDialog, Ui_LogLayerChooser, PluginSettings):
    def __init__(self, legendInterface):
        QDialog.__init__(self)
        self.setupUi(self)
        PluginSettings.__init__(self, pluginName, mySettings)

        self.layerComboManager = VectorLayerCombo(legendInterface, self.logLayer, lambda: self.value("logLayer"), {"dataProvider":"postgres"})


    def accept(self):
        layer = self.layerComboManager.getLayer()
        if layer is not None and LogLayer(layer.id()).isValid():
            QDialog.accept()
        else:
            self.logLayer.currentIndex(0)




