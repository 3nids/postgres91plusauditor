# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/ui_loglayerchooser.ui'
#
# Created: Wed Apr 17 18:01:48 2013
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_LogLayerChooser(object):
    def setupUi(self, LogLayerChooser):
        LogLayerChooser.setObjectName(_fromUtf8("LogLayerChooser"))
        LogLayerChooser.resize(331, 106)
        LogLayerChooser.setAcceptDrops(False)
        self.gridLayout = QtGui.QGridLayout(LogLayerChooser)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(LogLayerChooser)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(LogLayerChooser)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 2, 1, 1, 1)
        self.logLayer = QtGui.QComboBox(LogLayerChooser)
        self.logLayer.setObjectName(_fromUtf8("logLayer"))
        self.gridLayout.addWidget(self.logLayer, 0, 1, 1, 1)
        self.redefineSubset = QtGui.QCheckBox(LogLayerChooser)
        self.redefineSubset.setObjectName(_fromUtf8("redefineSubset"))
        self.gridLayout.addWidget(self.redefineSubset, 1, 0, 1, 2)

        self.retranslateUi(LogLayerChooser)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), LogLayerChooser.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), LogLayerChooser.reject)
        QtCore.QMetaObject.connectSlotsByName(LogLayerChooser)

    def retranslateUi(self, LogLayerChooser):
        LogLayerChooser.setWindowTitle(QtGui.QApplication.translate("LogLayerChooser", "Postgres 91 plus Auditor :: logged action layer chooser", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("LogLayerChooser", "Logged action layer", None, QtGui.QApplication.UnicodeUTF8))
        self.redefineSubset.setText(QtGui.QApplication.translate("LogLayerChooser", "Redefine layer subset to search faster", None, QtGui.QApplication.UnicodeUTF8))

