from qgis.core import QgsMapLayerRegistry


class LogLayer():
    def __init__(self, layerId):
        self.layer = QgsMapLayerRegistry.instance().mapLayer(layerId)


    def isValid(self):
        if self.layer is None:
            return False
        # TODO check validity

        return True


    def performSearch(self, onlyGeometry=False):
        if not self.isValid():
            return None
        