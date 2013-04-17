from PyQt4.QtGui import QDialog

from ..mysettings import mySettings, pluginName
from ..qgistools.pluginsettings import PluginSettings
from ..qgistools.gui import VectorLayerCombo
from ..src.loglayer import LogLayer
from ..ui.ui_loglayerchooser import Ui_LogLayerChooser

class LogLayerChooserDialog(QDialog, Ui_LogLayerChooser, PluginSettings):
    def __init__(self, legendInterface):
        QDialog.__init__(self)
        self.setupUi(self)
        PluginSettings.__init__(self, pluginName, mySettings)

        self.layerComboManager = VectorLayerCombo(legendInterface, self.logLayer, lambda: self.value("logLayer"), {"dataProvider": "postgres"})

    def accept(self):
        layer = self.layerComboManager.getLayer()
        if LogLayer().checkLayer(layer):
            QDialog.accept(self)
        else:
            self.logLayer.setCurrentIndex(0)


    # TODO: if uncheck subset, clear layer subset