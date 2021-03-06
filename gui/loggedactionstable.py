from PyQt4.QtCore import Qt
from PyQt4.QtGui import QTableWidget, QTableWidgetItem, QAbstractItemView

from ..core.mysettings import MySettings
from ..core.loglayer import columnVarSetting, columnFancyName, columnRowName


class LoggedActionsTable(QTableWidget):
    def __init__(self, parent):
        QTableWidget.__init__(self, parent)
        self.settings = MySettings()

        self.geomColumn = True

        self.setSortingEnabled(True)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setColumnCount(0)
        self.setRowCount(0)
        self.horizontalHeader().setMinimumSectionSize(15)
        self.verticalHeader().setVisible(False)
        self.verticalHeader().setDefaultSectionSize(25)
        #self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.displayColumns()

        self.adjustSize()

    def displayColumns(self):
        self.clear()
        for c in range(self.columnCount() - 1, -1, -1):
            self.removeColumn(c)
        for r in range(self.rowCount() - 1, -1, -1):
            self.removeRow(r)
        columns = self.settings.value("columns")
        c = 0
        for i, col in enumerate(columnVarSetting):
            if col in columns:
                if columnRowName[i] == "changedGeometryStr" and not self.geomColumn:
                    continue
                self.insertColumn(c)
                item = QTableWidgetItem(columnFancyName[i])
                item.setData(Qt.UserRole, columnRowName[i])
                font = item.font()
                font.setPointSize(font.pointSize() - 2)
                item.setFont(font)
                self.setHorizontalHeaderItem(c, item)
                c += 1
        self.horizontalHeader().setMinimumSectionSize(15)

    def displayRows(self, data):
        self.clearContents()
        for r in range(self.rowCount() - 1, -1, -1):
            self.removeRow(r)
        for row in data.values():
            r = self.rowCount()
            self.insertRow(r)

            for c in range(self.columnCount()):
                crn = self.horizontalHeaderItem(c).data(Qt.UserRole)
                dataStr = eval("row.%s()" % crn)
                if crn == "dateStr":
                    item = LoggedActiontItem(dataStr)
                else:
                    item = QTableWidgetItem(dataStr)
                item.setData(Qt.UserRole, row.dateMs)
                item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                if crn in ("user", "action", "changedGeometryStr"):
                    item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                else:
                    item.setTextAlignment(Qt.AlignVCenter)
                font = item.font()
                font.setPointSize(font.pointSize() - 2)
                item.setFont(font)
                self.setItem(r, c, item)

        self.resizeColumnsToContents()
        self.sortByColumn(0, Qt.DescendingOrder)


class LoggedActiontItem(QTableWidgetItem):
    def __init__(self, text):
        QTableWidgetItem.__init__(self, text)

    def __gt__(self, other):
        return long(self.data(Qt.UserRole)) > long(other.data(Qt.UserRole))

    def __lt__(self, other):
        return long(self.data(Qt.UserRole)) < long(other.data(Qt.UserRole))

    def __eq__(self, other):
        return long(self.data(Qt.UserRole)) == long(other.data(Qt.UserRole))


