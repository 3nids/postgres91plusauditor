from PyQt4.QtGui import QDialog
from qgis.core import QgsMapLayerRegistry, QgsFeature, QgsFeatureRequest

from mysettings import mySettings, pluginName, LogLayerChooserDialog
from loglayer import LogLayer
from ui.ui_showhistory import Ui_showHistory

from qgistools.gui import VectorLayerCombo, FieldCombo
from qgistools.pluginsettings import PluginSettings


class ShowHistoryDialog(QDialog, Ui_showHistory, PluginSettings):
    def __init__(self, legendInterface, layerId=None, featureId=None):
        QDialog.__init__(self)
        self.setupUi(self)
        PluginSettings.__init__(self, pluginName, mySettings, False, True) # column chooser, advanced search options
        self.legendInterface = legendInterface

        self.layerId = layerId
        self.featureId = featureId

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
        self.logLayer = LogLayer( self.value("logLayer") )
        if not self.logLayer.isValid():
            if not LogLayerChooserDialog(self.legendInterface):
                e.ignore()


        if self.layerId is not None:
            self.layerCombo.setEnabled( False )
            layer = self.layerComboManager.getLayer()
            if layer is None:
                e.ignore()

        if self.featureId is not None:
            self.featureEdit.setEnabled( False )
            self.searchButton.hide()
            f = QgsFeature()
            featReq = QgsFeatureRequest().setFilterFid( self.featureId ).setFlags( QgsFeatureRequest.NoGeometry )
            if layer.getFeatures( featReq ).nextFeature( f ) is False:
                e.ignore()


   # def searchHistory(self):

