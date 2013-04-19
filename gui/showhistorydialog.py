from PyQt4.QtCore import *
from PyQt4.QtGui import QDialog, QGridLayout
from qgis.core import QgsFeature, QgsFeatureRequest

from ..qgistools.gui import VectorLayerCombo, FieldCombo
from ..qgistools.settingmanager import SettingDialog

from ..src.mysettings import MySettings
from ..src.loglayer import LogLayer, columnVarSetting

from ..ui.ui_showhistory import Ui_showHistory

from loglayerchooserdialog import LogLayerChooserDialog
from differenceviewer import DifferenceViewer
from loggedactionstable import LoggedActionsTable


class ShowHistoryDialog(QDialog, Ui_showHistory, SettingDialog):
    rejectLater = pyqtSignal()

    def __init__(self, legendInterface, layerId=None, featureId=None):
        QDialog.__init__(self)
        self.setupUi(self)
        self.settings = MySettings()
        SettingDialog.__init__(self, self.settings, False, True)  # column chooser, advanced search options
        self.legendInterface = legendInterface
        self.layerId = layerId
        self.featureId = featureId

        self.rejectLater.connect(self.reject, Qt.QueuedConnection)
        self.buttonDisplayMode(False)

        self.featureEdit.setText("%s" % featureId)

        # setup layer - field combo, with primary key selector as field
        pkeyName = ""
        self.layerComboManager = VectorLayerCombo(legendInterface, self.layerCombo, layerId,
                                                  {"dataProvider": "postgres"})
        layer = self.layerComboManager.getLayer()
        if layer is not None:
            pkeyIdx = layer.dataProvider().pkAttributeIndexes()
            if len(pkeyIdx) == 1:
                pkeyName = layer.pendingFields()[pkeyIdx[0]].name()
        self.fieldComboManager = FieldCombo(self.pkeyCombo, self.layerComboManager, pkeyName)

        # log layer
        self.logLayer = LogLayer()
        self.logLayer.setProgressMax.connect(self.progressBar.setMaximum)
        self.logLayer.setProgressMin.connect(self.progressBar.setMinimum)
        self.logLayer.setProgressValue.connect(self.progressBar.setValue)

        # logged actions table
        self.loggedActionsLayout = QGridLayout(self.loggedActionsWidget)
        self.loggedActionsTable = LoggedActionsTable(self.loggedActionsWidget)
        self.loggedActionsLayout.addWidget(self.loggedActionsTable, 0, 0, 1, 1)
        for col in columnVarSetting:
            self.settings.setting(col).valueChanged.connect(self.displayLoggedActions)
        self.loggedActionsTable.itemClicked.connect(self.displayDifference)

        # difference viewer
        self.differenceLayout = QGridLayout(self.differenceViewerWidget)
        self.differenceViewer = DifferenceViewer(self.differenceViewerWidget)
        self.differenceLayout.addWidget(self.differenceViewer, 0, 0, 1, 1)

        #TODO: disable geometry checkbox if layer has no geom

    def showEvent(self, e):
        SettingDialog.showEvent(self, e)
        while not self.logLayer.isValid():
            if not LogLayerChooserDialog(self.legendInterface).exec_():
                self.rejectLater.emit()
                return
        if self.layerId is not None:
            self.layerCombo.setEnabled(False)
            layer = self.layerComboManager.getLayer()
            if layer is None:
                self.rejectLater.emit()
                return
        if self.featureId is not None:
            self.featureEdit.setEnabled(False)
            f = QgsFeature()
            featReq = QgsFeatureRequest().setFilterFid(self.featureId).setFlags(QgsFeatureRequest.NoGeometry)
            if layer.getFeatures(featReq).nextFeature(f) is False:
                self.rejectLater.emit()
                return

    @pyqtSignature("on_stopButton_clicked()")
    def on_stopButton_clicked(self):
        self.logLayer.interrupt()

    @pyqtSignature("on_searchButton_clicked()")
    def on_searchButton_clicked(self):
        layer = self.layerComboManager.getLayer()
        pkeyName = self.fieldComboManager.getFieldName()
        featureId = self.featureEdit.text().toInt()[0]
        onlyGeometry = self.settings.value("searchOnlyGeometry")
        if layer is None or pkeyName == "":
            return
        self.buttonDisplayMode(True)
        self.logLayer.performSearch(layer, featureId, pkeyName, onlyGeometry)
        self.buttonDisplayMode(False)
        self.displayLoggedActions()

    def buttonDisplayMode(self, searchOn):
        self.searchButton.setVisible(not searchOn)
        self.stopButton.setVisible(searchOn)
        self.progressBar.setVisible(searchOn)

    def displayLoggedActions(self, dummy=None):
        self.loggedActionsTable.displayColumns()
        self.loggedActionsTable.displayRows(self.logLayer.results)

    def displayDifference(self, item):
        rowId = item.data(Qt.UserRole).toLongLong()[0]
        logRow = self.logLayer.results[rowId]
        feat = self.logLayer.layerFeature
        print logRow, feat
