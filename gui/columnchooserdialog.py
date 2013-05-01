from PyQt4.QtCore import Qt, pyqtSignal, pyqtSignature, QDateTime
from PyQt4.QtGui import QDialog, QGridLayout
from qgis.core import QgsFeature, QgsFeatureRequest
from qgis.gui import QgsRubberBand

from ..qgissettingmanager import SettingDialog

from ..src.mysettings import MySettings

from ..ui.ui_columnchooser import Ui_columnChooser


class ColumnChooserDialog(QDialog, Ui_columnChooser, SettingDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.setupUi(self)
        self.settings = MySettings()
        SettingDialog.__init__(self, self.settings)  # column chooser, advanced search options
