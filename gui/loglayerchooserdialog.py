from PyQt4.QtGui import QDialog

from ..qgissettingmanager import SettingDialog
from ..qgiscombomanager import VectorLayerCombo

from ..core.mysettings import MySettings
from ..core.loglayer import LogLayer

from ..ui.ui_loglayerchooser import Ui_LogLayerChooser


class LogLayerChooserDialog(QDialog, Ui_LogLayerChooser, SettingDialog):

    def __init__(self, legendInterface):
        QDialog.__init__(self)
        self.setupUi(self)
        self.settings = MySettings()
        SettingDialog.__init__(self, self.settings)

        self.layerComboManager = VectorLayerCombo(legendInterface, self.logLayer,
                                                  lambda: self.settings.value("logLayer"),
                                                  {"dataProvider": "postgres"})

    def accept(self):
        layer = self.layerComboManager.getLayer()
        if LogLayer().checkLayer(layer):
            QDialog.accept(self)
        else:
            self.logLayer.setCurrentIndex(0)