from PyQt4.QtCore import *
from PyQt4.QtGui import QDialog
from qgis.core import QgsMapLayerRegistry, QgsFeature, QgsFeatureRequest

from mysettings import mySettings, pluginName, LogLayerChooserDialog
from loglayer import LogLayer
from ui.ui_showhistory import Ui_showHistory

from qgistools.gui import VectorLayerCombo, FieldCombo
from qgistools.pluginsettings import PluginSettings


class ShowHistoryDialog(QDialog, Ui_showHistory, PluginSettings):
    rejectLater = pyqtSignal()

    def __init__(self, legendInterface, layerId=None, featureId=None):
        print layerId
        QDialog.__init__(self)
        self.setupUi(self)
        PluginSettings.__init__(self, pluginName, mySettings, False, True) # column chooser, advanced search options
        self.legendInterface = legendInterface
        self.layerId = layerId
        self.featureId = featureId
        self.rejectLater.connect( self.reject, Qt.QueuedConnection )

        self.logLayer = LogLayer( self.value("logLayer") )

        self.layerComboManager = VectorLayerCombo(legendInterface, self.layerCombo, layerId, {"dataProvider":"postgres"})
        pkeyName = ""
        layer = self.layerComboManager.getLayer()
        if layer is not None:
            pkeyIdx = layer.dataProvider().pkAttributeIndexes()
            if len(pkeyIdx)==1:
                pkeyName = layer.pendingFields()[pkeyIdx[0]].name()
        self.fieldComboManager = FieldCombo(self.pkeyCombo, self.layerComboManager, pkeyName)
        self.featureEdit.setText( "%s" % featureId )



    def showEvent(self, e):
        if not self.logLayer.isValid():
            if not LogLayerChooserDialog(self.legendInterface).exec_():
                self.rejectLater.emit()
                return

        if self.layerId is not None:
            self.layerCombo.setEnabled( False )
            layer = self.layerComboManager.getLayer()
            if layer is None:
                self.rejectLater.emit()
                return

        if self.featureId is not None:
            self.featureEdit.setEnabled( False )
            self.searchButton.hide()
            f = QgsFeature()
            featReq = QgsFeatureRequest().setFilterFid( self.featureId ).setFlags( QgsFeatureRequest.NoGeometry )
            if layer.getFeatures( featReq ).nextFeature( f ) is False:
                self.rejectLater.emit()
                return

            self.searcHistory()


    def searchHistory(self):
        onlyGeometry = self.value("searchOnlyGeometry")
        self.logLayer.performSearch(onlyGeometry)

