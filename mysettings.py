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

pluginName = "postgresauditor91plus"

mySettings = [
    # global settings
    Bool(pluginName,"displayColumnChangedFields", "global", True ),
    Bool(pluginName,"displayColumnAction       ", "global", True ),
    Bool(pluginName,"displayColumnDate         ", "global", True ),
    Bool(pluginName,"displayColumnUser         ", "global", True ),
    Bool(pluginName,"displayColumnApplication  ", "global", True ),
    Bool(pluginName,"displayColumnClientIP     ", "global", True ),
    Bool(pluginName,"searchOnlyGeometry        ", "global", True ),

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
        if LogLayer(self.layerComboManager.getLayer().id()).isValid():
            QDialog.accept()
        else:
            self.logLayer.currentIndex(0)




