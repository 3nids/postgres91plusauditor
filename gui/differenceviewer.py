from PyQt4.QtGui import QTableWidget,QTableWidgetItem

class DifferenceViewer(QTableWidget):
    def __init__(self, parent):
        QTaableWidget.__init__(self, parent)
        for i,header in enumerate(("Field","Current","_date_")):
            self.tableViewTable.insertColumn(i)
            self.tableViewTable.setHorizontalHeaderItem(c, QTableWidgetItem(header))

    def displayDifference(self, layerFeature, logRow):
        pass