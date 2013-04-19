from PyQt4.QtGui import QTableWidget, QTableWidgetItem, QSizePolicy


class DifferenceViewer(QTableWidget):
    def __init__(self, parent):
        QTableWidget.__init__(self, parent)
        for c,header in enumerate(("Field", "Current", "_date_")):
            self.insertColumn(c)
            self.setHorizontalHeaderItem(c, QTableWidgetItem(header))

            self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
            self.adjustSize()



    def displayDifference(self, layerFeature, logRow):
        pass
