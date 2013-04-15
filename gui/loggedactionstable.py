from PyQt4.QtCore import Qt
from PyQt4.QtGui import QTableWidget,QTableWidgetItem,QAbstractItemView

from ..mysettings import MySettings
from ..src.loglayer import columnVarSetting, columnFancyName, columnRowName


class LoggedActionsTable(QTableWidget):
    def __init__(self, parent):
        QTableWidget.__init__(self, parent)
        self.settings = MySettings()

        self.setSortingEnabled(True)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setColumnCount(0)
        self.setRowCount(0)
        self.horizontalHeader().setMinimumSectionSize(15)
        self.verticalHeader().setVisible(False)
        self.verticalHeader().setDefaultSectionSize(25)

    def displayColumns(self,dummy=None):
        self.clear()
        for c in range( self.columnCount()-1, -1, -1 ):
            self.removeColumn(c)
        for r in range( self.rowCount()-1, -1, -1 ):
            self.removeRow(r)
        c = 0
        for i,col in enumerate(columnVarSetting):
            if self.settings.value(col):
                self.insertColumn(c)
                item = QTableWidgetItem(columnFancyName[i])
                item.setData(Qt.UserRole, columnRowName[i])
                self.setHorizontalHeaderItem(c, item)
                c += 1
        self.horizontalHeader().setMinimumSectionSize(15)
        self.displayRows([])


    def displayRows(self, rows):
        self.clearContents()
        for r in range( self.rowCount()-1, -1, -1 ):
            self.removeRow(r)
        for row in rows.values():
            r = self.rowCount()
            self.insertRow(r)

            for c in range(self.columnCount()):
                crn = self.column(c).data(Qt.UserRole)
                dataStr = eval("row."+crn+"()")
                if i == 0:
                    item = LoggedActiontItem( dataStr )
                else:
                    item = QTableWidgetItem( dataStr )
                item.setData(Qt.UserRole, row.dateMs)
                item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                self.tableViewTable.setItem(r,c,item)
                c+=1
        self.tableViewTable.resizeColumnsToContents()
        self.tableViewTable.sortByColumn(0, Qt.DescendingOrder)






class LoggedActiontItem(QTableWidgetItem):
    def __init__(self, text):
        QTableWidgetItem.__init__(self, text)

    def __gt__(self, other):
        return self.data(Qt.UserRole).toInt()[0] > other.data(Qt.UserRole).toInt()[0]

    def __lt__(self, other):
        return self.data(Qt.UserRole).toInt()[0] < other.data(Qt.UserRole).toInt()[0]

    def __eq__(self, other):
        return self.data(Qt.UserRole).toInt()[0] == other.data(Qt.UserRole).toInt()[0]

