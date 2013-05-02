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

            currentValue = layerFeature.attribute(field.name()).toString()
            logValue = logRow.getFieldValue(logRow.logData, field.name())

            items[0] = QTableWidgetItem(field.name())
            items[1] = QTableWidgetItem(currentValue)
            items[2] = QTableWidgetItem(logValue)

            if currentValue != logValue:
                for c, item in enumerate(items):
                    self.reduceFontSize(item)
                    item.setFlags(Qt.ItemIsEnabled)
                    item.setBackground(QBrush(QColor(250, 250, 210)))
                    self.setItem(r, c, item)

        self.adjustSize()
        self.resizeColumnsToContents()

    def clearRows(self):
        while self.rowCount() > 0:
            self.removeRow(0)

    def reduceFontSize(self, item):
        font = item.font()
        font.setPointSize(font.pointSize() - 2)
        item.setFont(font)
        return item