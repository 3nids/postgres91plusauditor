from PyQt4.QtCore import Qt
from PyQt4.QtGui import QTableWidget, QTableWidgetItem, QAbstractItemView, QBrush, QColor


class DifferenceViewer(QTableWidget):
    def __init__(self, parent):
        QTableWidget.__init__(self, parent)
        self.setSelectionMode(QAbstractItemView.NoSelection)
        self.setColumnCount(0)
        self.setRowCount(0)
        self.horizontalHeader().setMinimumSectionSize(15)
        self.verticalHeader().setVisible(False)
        self.verticalHeader().setDefaultSectionSize(25)
        #self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        for c, header in enumerate(("Field", "Current", "")):
            self.insertColumn(c)
            self.setHorizontalHeaderItem(c, QTableWidgetItem(header))
        self.adjustSize()

    def display(self, layerFeature, logRow):
        self.clearContents()
        self.setHorizontalHeaderItem(2, QTableWidgetItem(logRow.dateStr()))
        self.clearRows()

        items = [0, 0, 0]
        for r, field in enumerate(layerFeature.fields()):
            self.insertRow(r)

            items[0] = QTableWidgetItem(field.name())
            items[0].setFlags(Qt.ItemIsEnabled)
            self.setItem(r, 0, items[0])

            currentValue = layerFeature.attribute(field.name()).toString()
            items[1] = QTableWidgetItem(currentValue)
            items[1].setFlags(Qt.ItemIsEnabled)
            self.setItem(r, 1, items[1])

            logValue = logRow.getFieldValue(logRow.logData, field.name())
            if logValue is None:
                logValue = ""
            items[2] = QTableWidgetItem(logValue)
            items[2].setFlags(Qt.ItemIsEnabled)
            self.setItem(r, 2, items[2])

            if currentValue != logValue:
                for item in items:
                    item.setBackground(QBrush(QColor(240, 128, 128)))

        self.adjustSize()
        self.resizeColumnsToContents()

    def clearRows(self):
        while self.rowCount() > 0:
            self.removeRow(0)