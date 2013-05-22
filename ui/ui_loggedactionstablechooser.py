# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_loggedactionstablechooser.ui'
#
# Created: Wed May 22 14:09:21 2013
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_LoggedActionsTableChooser(object):
    def setupUi(self, LoggedActionsTableChooser):
        LoggedActionsTableChooser.setObjectName(_fromUtf8("LoggedActionsTableChooser"))
        LoggedActionsTableChooser.resize(359, 106)
        LoggedActionsTableChooser.setAcceptDrops(False)
        self.gridLayout = QtGui.QGridLayout(LoggedActionsTableChooser)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(LoggedActionsTableChooser)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(LoggedActionsTableChooser)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 2, 1, 1, 1)
        self.logLayer = QtGui.QComboBox(LoggedActionsTableChooser)
        self.logLayer.setObjectName(_fromUtf8("logLayer"))
        self.gridLayout.addWidget(self.logLayer, 0, 1, 1, 1)
        self.redefineSubset = QtGui.QCheckBox(LoggedActionsTableChooser)
        self.redefineSubset.setObjectName(_fromUtf8("redefineSubset"))
        self.gridLayout.addWidget(self.redefineSubset, 1, 0, 1, 2)

        self.retranslateUi(LoggedActionsTableChooser)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), LoggedActionsTableChooser.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), LoggedActionsTableChooser.reject)
        QtCore.QMetaObject.connectSlotsByName(LoggedActionsTableChooser)

    def retranslateUi(self, LoggedActionsTableChooser):
        LoggedActionsTableChooser.setWindowTitle(QtGui.QApplication.translate("LoggedActionsTableChooser", "Postgres 91 plus Auditor :: logged action table chooser", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("LoggedActionsTableChooser", "Logged action table", None, QtGui.QApplication.UnicodeUTF8))
        self.redefineSubset.setText(QtGui.QApplication.translate("LoggedActionsTableChooser", "Redefine layer subset to increase performance", None, QtGui.QApplication.UnicodeUTF8))

