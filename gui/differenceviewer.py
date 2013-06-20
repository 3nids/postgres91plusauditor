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
        self.columns()

    def columns(self, nc=2, dateTitle=""):
        while self.columnCount() > 0:
            self.removeColumn(0)
        if nc == 2:
            headers = ("Field", dateTitle)
        else:
            headers = ("Field", "Current", dateTitle)
        for c, header in enumerate(headers):
            self.insertColumn(c)
            self.setHorizontalHeaderItem(c, QTableWidgetItem(header))
        self.adjustSize()

    def display(self, logRow):
        self.clearRows()

        layerFeature = logRow.getLayerFeature()
        # if a feature exists (it has been modified but not deleted), display difference
        if layerFeature is None:
            nc = 2
        else:
            nc = 3
        self.columns(nc, logRow.dateStr())
        items = [0, 0, 0]
        items = items[:nc]
        currentValue = None
        for r, field in enumerate(logRow.fields):
            self.insertRow(r)

            logValue = logRow.getFieldValue(logRow.logData, field.name())

            items[0] = QTableWidgetItem(field.name())
            if layerFeature is not None:
                currentValue = layerFeature[field.name()]
                if currentValue is None:
                    currentValue = "NULL"
                items[1] = QTableWidgetItem(currentValue)
            items[nc-1] = QTableWidgetItem(logValue)

            for c, item in enumerate(items):
                self.reduceFontSize(item)
                item.setFlags(Qt.ItemIsEnabled)
                if layerFeature is not None and currentValue != logValue:
                    item.setBackground(QBrush(QColor(250, 250, 210)))
                self.setItem(r, c, item)

        self.resizeColumnsToContents()
        self.adjustSize()

    def clearRows(self):
        self.clearContents()
        while self.rowCount() > 0:
            self.removeRow(0)

    def reduceFontSize(self, item):
        font = item.font()
        font.setPointSize(font.pointSize() - 2)
        item.setFont(font)
        return item
