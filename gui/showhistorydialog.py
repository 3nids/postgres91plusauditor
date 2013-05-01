from PyQt4.QtCore import Qt, pyqtSignal, pyqtSignature, QDateTime
from PyQt4.QtGui import QDialog, QGridLayout
from qgis.core import QgsFeature, QgsFeatureRequest
from qgis.gui import QgsRubberBand

from ..qgiscombomanager import VectorLayerCombo, FieldCombo
from ..qgissettingmanager import SettingDialog
from ..qgistools.vectorlayer import primaryKey

from ..src.mysettings import MySettings
from ..src.loglayer import LogLayer, columnVarSetting

from ..ui.ui_showhistory import Ui_showHistory

from loglayerchooserdialog import LogLayerChooserDialog
from differenceviewer import DifferenceViewer
from loggedactionstable import LoggedActionsTable


class ShowHistoryDialog(QDialog, Ui_showHistory, SettingDialog):
    rejectShowEvent = pyqtSignal()
    performSearchAtShowEvent = pyqtSignal()

    def __init__(self, iface, layerId=None, featureId=None):
        QDialog.__init__(self)
        self.setupUi(self)
        self.settings = MySettings()
        SettingDialog.__init__(self, self.settings, False, True)  # column chooser, advanced search options
        self.legendInterface = iface.legendInterface()
        self.layerId = layerId
        self.featureId = featureId

        self.layer = None
        self.rubber = QgsRubberBand(iface.mapCanvas())
        self.mapCanvas = iface.mapCanvas()

        self.panShowGeometry.clicked.connect(self.displayGeomDifference)

        self.rejectShowEvent.connect(self.reject, Qt.QueuedConnection)
        self.performSearchAtShowEvent.connect(self.on_searchButton_clicked, Qt.QueuedConnection)
        
        self.buttonDisplayMode(False)

        self.featureEdit.setText("%s" % featureId)

        # setup layer - field combo, with primary key selector as field
        self.layerComboManager = VectorLayerCombo(self.legendInterface, self.layerCombo, layerId,
                                                  {"dataProvider": "postgres", "finishInit": False})
        self.layerComboManager.finishInit()
        pkeyLambda = lambda: primaryKey(self.layerComboManager.getLayer())
        self.fieldComboManager = FieldCombo(self.pkeyCombo, self.layerComboManager, pkeyLambda)

        # log layer
        self.logLayer = LogLayer()
        self.logLayer.setProgressMax.connect(self.progressBar.setMaximum)
        self.logLayer.setProgressMin.connect(self.progressBar.setMinimum)
        self.logLayer.setProgressValue.connect(self.progressBar.setValue)

        # logged actions table
        self.loggedActionsLayout = QGridLayout(self.loggedActionsWidget)
        self.loggedActionsTable = LoggedActionsTable(self.loggedActionsWidget)
        self.loggedActionsLayout.addWidget(self.loggedActionsTable, 0, 0, 1, 1)
        self.loggedActionsTable.itemSelectionChanged.connect(self.displayDifference)
        self.columnChooserButton.clicked.connect(self.loggedActionsTable.columnChooser)

        # difference viewer
        self.differenceLayout = QGridLayout(self.differenceViewerWidget)
        self.differenceViewer = DifferenceViewer(self.differenceViewerWidget)
        self.differenceLayout.addWidget(self.differenceViewer, 0, 0, 1, 1)

        self.adjustSize()

        #TODO: disable geometry checkbox if layer has no geom

    def closeEvent(self, e):
        self.rubber.reset()

    def showEvent(self, e):
        SettingDialog.showEvent(self, e)
        while not self.logLayer.isValid():
            if not LogLayerChooserDialog(self.legendInterface).exec_():
                self.rejectShowEvent.emit()
                return
        if self.layerId is not None:
            self.layerCombo.setEnabled(False)
            layer = self.layerComboManager.getLayer()
            if layer is None:
                self.rejectShowEvent.emit()
                return
        if self.featureId is not None:
            self.featureEdit.setEnabled(False)
            f = QgsFeature()
            featReq = QgsFeatureRequest().setFilterFid(self.featureId).setFlags(QgsFeatureRequest.NoGeometry)
            if layer.getFeatures(featReq).nextFeature(f) is False:
                self.rejectShowEvent.emit()
                return
            self.performSearchAtShowEvent.emit()

    @pyqtSignature("on_layerCombo_currentIndexChanged(int)")
    def on_layerCombo_currentIndexChanged(self, i):
        self.layer = self.layerComboManager.getLayer()
        self.panShowGeometry.setEnabled(self.layer is not None and self.layer.hasGeometryType())

    @pyqtSignature("on_stopButton_clicked()")
    def on_stopButton_clicked(self):
        self.logLayer.interrupt()

    @pyqtSignature("on_searchButton_clicked()")
    def on_searchButton_clicked(self):
        self.layer = self.layerComboManager.getLayer()
        self.loggedActionsTable.geomColumn = self.layer.hasGeometryType()
        pkeyName = self.fieldComboManager.getFieldName()
        if self.layer is None or pkeyName == "":
            return
        featureId = self.featureEdit.text().toInt()[0]
        searchOnlyGeometry = self.searchOnlyGeometry.isChecked()
        searchInserts = self.searchInserts.isChecked()
        searchUpdates = self.searchUpdates.isChecked()
        searchDeletes = self.searchDeletes.isChecked()
        searchBeforeDate = QDateTime()
        if self.searchBefore.isChecked():
            searchBeforeDate = self.searchAfterDate.dateTime()
        searchAfterDate = QDateTime()
        if self.searchAfter.isChecked():
            searchAfterDate = self.searchAfterDate.dateTime()
        self.buttonDisplayMode(True)
        self.logLayer.performSearch(self.layer, featureId, pkeyName, searchInserts, searchUpdates, searchDeletes,
                                    searchOnlyGeometry, searchAfterDate, searchBeforeDate)
        self.buttonDisplayMode(False)
        self.panShowGeometry.setEnabled(self.layer.hasGeometryType())
        self.displayLoggedActions()

    def buttonDisplayMode(self, searchOn):
        self.searchButton.setVisible(not searchOn)
        self.stopButton.setVisible(searchOn)
        self.progressBar.setVisible(searchOn)

    def displayLoggedActions(self):
        self.differenceViewer.clear()
        self.loggedActionsTable.data = self.logLayer.results
        self.loggedActionsTable.displayColumns()
        self.loggedActionsTable.displayRows()

    def displayDifference(self):
        self.differenceViewer.clear()
        item = self.loggedActionsTable.selectedItems()
        if len(item) == 0:
            return
        rowId = item[0].data(Qt.UserRole).toLongLong()[0]
        logRow = self.logLayer.results[rowId]
        self.differenceViewer.display(self.logLayer.layerFeature, logRow)
        self.displayGeomDifference()

    def displayGeomDifference(self):
        self.rubber.reset()
        item = self.loggedActionsTable.selectedItems()
        if len(item) == 0:
            return
        rowId = item[0].data(Qt.UserRole).toLongLong()[0]
        logRow = self.logLayer.results[rowId]

        if self.layer.hasGeometryType() and self.panShowGeometry.isChecked():
            geom = logRow.geometry()
            self.rubber.setToGeometry(geom, self.layer)
            panTo = self.mapCanvas.mapRenderer().layerExtentToOutputExtent(self.layer, geom.boundingBox())
            panTo.scale(1.5)
            self.mapCanvas.setExtent(panTo)
            self.mapCanvas.refresh()



