from PyQt4.QtGui import QTableWidget,QTableWidgetItem



class LogResultsTable(QTableWidget):
    def __init__(self, parent):
        QTableWidget.__init__(self, parent)

        self.resultsTable.setSortingEnabled(True)
        self.resultsTable.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.resultsTable.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.resultsTable.setObjectName(_fromUtf8("resultsTable"))
        self.resultsTable.setColumnCount(0)
        self.resultsTable.setRowCount(0)
        self.resultsTable.horizontalHeader().setMinimumSectionSize(15)
        self.resultsTable.verticalHeader().setVisible(False)
        self.resultsTable.verticalHeader().setDefaultSectionSize(25)




    def displayLoggedActionsColumns(self,dummy=None):
        self.clear()
        for c in range( self.tableViewTable.columnCount()-1, -1, -1 ):
            self.tableViewTable.removeColumn(c)
        for r in range( self.tableViewTable.rowCount()-1, -1, -1 ):
            self.tableViewTable.removeRow(r)
        c = 0
        for i,col in enumerate(columnVarSetting):
            if self.value(col):
                self.tableViewTable.insertColumn(c)
                self.tableViewTable.setHorizontalHeaderItem(c, QTableWidgetItem(columnFancyName[i]))
                c += 1
        self.tableViewTable.horizontalHeader().setMinimumSectionSize(15)
        self.displayLoggedActionsLines()



    def displayLoggedActionsLines(self):
        self.clearContents()
        for r in range( self.tableViewTable.rowCount()-1, -1, -1 ):
            self.tableViewTable.removeRow(r)
        for row in self.logLayer.results.values():
            r = self.tableViewTable.rowCount()
            self.tableViewTable.insertRow(r)

            c = 0
            for i,col in enumerate(columnVarSetting):
                if not self.value(col):
                    continue
                dataStr = eval("row."+columnRowName[i]+"()")
                if i == 0:
                    item = LogTableWidgetItem( dataStr )
                else:
                    item = QTableWidgetItem( dataStr )
                item.setData(Qt.UserRole, row.dateMs)
                item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                self.tableViewTable.setItem(r,c,item)
                c+=1
        self.tableViewTable.resizeColumnsToContents()
        self.tableViewTable.sortByColumn(0, Qt.DescendingOrder)






class LogTableWidgetItem(QTableWidgetItem):
    def __init__(self, text):
        QTableWidgetItem.__init__(self, text)

    def __gt__(self, other):
        return self.data(Qt.UserRole).toInt()[0] > other.data(Qt.UserRole).toInt()[0]

    def __lt__(self, other):
        return self.data(Qt.UserRole).toInt()[0] < other.data(Qt.UserRole).toInt()[0]

    def __eq__(self, other):
        return self.data(Qt.UserRole).toInt()[0] == other.data(Qt.UserRole).toInt()[0]


