from PyQt4.QtGui import QTableWidget,QTableWidgetItem

class DifferenceViewer(QTableWidget):
    def __init__(self, parent):
        QTableWidget.__init__(self, parent)
        for c,header in enumerate(("Field","Current","_date_")):
            self.insertColumn(c)
            self.setHorizontalHeaderItem(c, QTableWidgetItem(header))

    def displayDifference(self, layerFeature, logRow):
        pass
