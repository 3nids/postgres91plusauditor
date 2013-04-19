from PyQt4.QtCore import Qt
from PyQt4.QtGui import QTableWidget, QTableWidgetItem, QAbstractItemView


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
        while self.rowCount() > 0:
            self.removeRow(0)

        for r, field in enumerate(layerFeature.fields()):
            self.insertRow(r)

            item = QTableWidgetItem(field.name())
            item.setFlags(Qt.ItemIsEnabled)
            self.setItem(r, 0, item)

            currentValue = layerFeature.attribute(field.name()).toString()
            item = QTableWidgetItem(currentValue)
            item.setFlags(Qt.ItemIsEnabled)
            self.setItem(r, 1, item)

            logValue = logRow.getFieldValue(logRow.logData, field.name())
            if logValue is None:
                logValue = ""
            item = QTableWidgetItem(logValue)
            item.setFlags(Qt.ItemIsEnabled)
            self.setItem(r, 2, item)
