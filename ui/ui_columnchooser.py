# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_columnchooser.ui'
#
# Created: Tue Apr 30 16:06:35 2013
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_columnChooser(object):
    def setupUi(self, columnChooser):
        columnChooser.setObjectName(_fromUtf8("columnChooser"))
        columnChooser.resize(304, 268)
        self.gridLayout = QtGui.QGridLayout(columnChooser)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.columns = QtGui.QListWidget(columnChooser)
        self.columns.setObjectName(_fromUtf8("columns"))
        item = QtGui.QListWidgetItem()
        item.setCheckState(QtCore.Qt.Checked)
        self.columns.addItem(item)
        item = QtGui.QListWidgetItem()
        item.setCheckState(QtCore.Qt.Checked)
        self.columns.addItem(item)
        item = QtGui.QListWidgetItem()
        item.setCheckState(QtCore.Qt.Checked)
        self.columns.addItem(item)
        item = QtGui.QListWidgetItem()
        item.setCheckState(QtCore.Qt.Checked)
        self.columns.addItem(item)
        item = QtGui.QListWidgetItem()
        item.setCheckState(QtCore.Qt.Checked)
        self.columns.addItem(item)
        item = QtGui.QListWidgetItem()
        item.setCheckState(QtCore.Qt.Unchecked)
        self.columns.addItem(item)
        item = QtGui.QListWidgetItem()
        item.setCheckState(QtCore.Qt.Unchecked)
        self.columns.addItem(item)
        item = QtGui.QListWidgetItem()
        item.setCheckState(QtCore.Qt.Unchecked)
        self.columns.addItem(item)
        self.gridLayout.addWidget(self.columns, 0, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(columnChooser)
        self.buttonBox.setOrientation(QtCore.Qt.Vertical)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 0, 1, 1, 1)

        self.retranslateUi(columnChooser)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), columnChooser.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), columnChooser.reject)
        QtCore.QMetaObject.connectSlotsByName(columnChooser)

    def retranslateUi(self, columnChooser):
        columnChooser.setWindowTitle(QtGui.QApplication.translate("columnChooser", "Logged actions table :: column chooser", None, QtGui.QApplication.UnicodeUTF8))
        __sortingEnabled = self.columns.isSortingEnabled()
        self.columns.setSortingEnabled(False)
        item = self.columns.item(0)
        item.setText(QtGui.QApplication.translate("columnChooser", "Date", None, QtGui.QApplication.UnicodeUTF8))
        item = self.columns.item(1)
        item.setText(QtGui.QApplication.translate("columnChooser", "User", None, QtGui.QApplication.UnicodeUTF8))
        item = self.columns.item(2)
        item.setText(QtGui.QApplication.translate("columnChooser", "Action", None, QtGui.QApplication.UnicodeUTF8))
        item = self.columns.item(3)
        item.setText(QtGui.QApplication.translate("columnChooser", "Changed geometry", None, QtGui.QApplication.UnicodeUTF8))
        item = self.columns.item(4)
        item.setText(QtGui.QApplication.translate("columnChooser", "Changed fields", None, QtGui.QApplication.UnicodeUTF8))
        item = self.columns.item(5)
        item.setText(QtGui.QApplication.translate("columnChooser", "Application", None, QtGui.QApplication.UnicodeUTF8))
        item = self.columns.item(6)
        item.setText(QtGui.QApplication.translate("columnChooser", "Client IP", None, QtGui.QApplication.UnicodeUTF8))
        item = self.columns.item(7)
        item.setText(QtGui.QApplication.translate("columnChooser", "Client port", None, QtGui.QApplication.UnicodeUTF8))
        self.columns.setSortingEnabled(__sortingEnabled)

