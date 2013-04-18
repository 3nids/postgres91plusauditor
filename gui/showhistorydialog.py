from PyQt4.QtCore import *
from PyQt4.QtGui import QDialog
from qgis.core import QgsFeature, QgsFeatureRequest

from ..mysettings import MySettings
from ..qgistools.gui import VectorLayerCombo, FieldCombo
from ..qgistools.settingmanager import SettingDialog
from ..src.loglayer import LogLayer, columnVarSetting#, columnFancyName, columnRowName   
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
        self.layerComboManager = VectorLayerCombo(legendInterface, self.layerCombo, layerId,
                                                  {"dataProvider": "postgres"})

        self.logLayer = LogLayer()
        self.logLayer.setProgressMax.connect(self.progressBar.setMaximum)
        self.logLayer.setProgressMin.connect(self.progressBar.setMinimum)
        self.logLayer.setProgressValue.connect(self.progressBar.setValue)

        self.differenceViewer = DifferenceViewer(self.differenceViewerWidget)
        self.loggedActionsTable = LoggedActionsTable(self.loggedActionsWidget)
        for col in columnVarSetting:
            self.settings.setting(col).valueChanged.connect(self.displayLoggedActions)

        pkeyName = ""
        layer = self.layerComboManager.getLayer()
        if layer is not None:
            pkeyIdx = layer.dataProvider().pkAttributeIndexes()
            if len(pkeyIdx) == 1:
                pkeyName = layer.pendingFields()[pkeyIdx[0]].name()
        self.fieldComboManager = FieldCombo(self.pkeyCombo, self.layerComboManager, pkeyName)
        self.featureEdit.setText("%s" % featureId)

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
        onlyGeometry = self.value("searchOnlyGeometry")
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

    def updateDifferenceDisplay(self):
        selected = self.resultsTable.selectedItems()
        if len(selected) != 1:
            self.differenceViewer.clearContents()
        rowId = selected.data(Qt.UserRole).toInt()[0]
        logRow = self.logLayer.results[rowId]
        feat = self.logLayer.logFeature

    def displayDifferenceInTable(self):
        self.tableView.clear()
