# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/ui_showhistory.ui'
#
# Created: Mon Apr 15 07:46:38 2013
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_showHistory(object):
    def setupUi(self, showHistory):
        showHistory.setObjectName(_fromUtf8("showHistory"))
        showHistory.resize(546, 441)
        self.gridLayout_6 = QtGui.QGridLayout(showHistory)
        self.gridLayout_6.setObjectName(_fromUtf8("gridLayout_6"))
        self.widget = QtGui.QWidget(showHistory)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setObjectName(_fromUtf8("widget"))
        self.gridLayout = QtGui.QGridLayout(self.widget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.layerCombo = QtGui.QComboBox(self.widget)
        self.layerCombo.setObjectName(_fromUtf8("layerCombo"))
        self.gridLayout.addWidget(self.layerCombo, 0, 1, 1, 1)
        self.featureEdit = QtGui.QLineEdit(self.widget)
        self.featureEdit.setObjectName(_fromUtf8("featureEdit"))
        self.gridLayout.addWidget(self.featureEdit, 0, 3, 1, 2)
        self.label = QtGui.QLabel(self.widget)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_2 = QtGui.QLabel(self.widget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 0, 2, 1, 1)
        self.label_3 = QtGui.QLabel(self.widget)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 0, 5, 1, 1)
        self.pkeyCombo = QtGui.QComboBox(self.widget)
        self.pkeyCombo.setObjectName(_fromUtf8("pkeyCombo"))
        self.gridLayout.addWidget(self.pkeyCombo, 0, 6, 1, 1)
        self.searchButton = QtGui.QPushButton(self.widget)
        self.searchButton.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.searchButton.setObjectName(_fromUtf8("searchButton"))
        self.gridLayout.addWidget(self.searchButton, 2, 6, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 0, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 6, 1, 1)
        self.groupBox_2 = QgsCollapsibleGroupBoxBasic(self.widget)
        self.groupBox_2.setProperty("collapsed", True)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.gridLayout_8 = QtGui.QGridLayout(self.groupBox_2)
        self.gridLayout_8.setMargin(6)
        self.gridLayout_8.setObjectName(_fromUtf8("gridLayout_8"))
        self.checkBox = QtGui.QCheckBox(self.groupBox_2)
        self.checkBox.setChecked(True)
        self.checkBox.setObjectName(_fromUtf8("checkBox"))
        self.gridLayout_8.addWidget(self.checkBox, 0, 1, 1, 1)
        self.checkBox_3 = QtGui.QCheckBox(self.groupBox_2)
        self.checkBox_3.setChecked(True)
        self.checkBox_3.setObjectName(_fromUtf8("checkBox_3"))
        self.gridLayout_8.addWidget(self.checkBox_3, 0, 0, 1, 1)
        self.checkBox_2 = QtGui.QCheckBox(self.groupBox_2)
        self.checkBox_2.setChecked(True)
        self.checkBox_2.setObjectName(_fromUtf8("checkBox_2"))
        self.gridLayout_8.addWidget(self.checkBox_2, 0, 2, 1, 1)
        self.searchOnlyGeometry = QtGui.QCheckBox(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.searchOnlyGeometry.sizePolicy().hasHeightForWidth())
        self.searchOnlyGeometry.setSizePolicy(sizePolicy)
        self.searchOnlyGeometry.setObjectName(_fromUtf8("searchOnlyGeometry"))
        self.gridLayout_8.addWidget(self.searchOnlyGeometry, 1, 0, 1, 3)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_8.addItem(spacerItem1, 0, 3, 1, 1)
        self.gridLayout.addWidget(self.groupBox_2, 1, 0, 2, 6)
        self.gridLayout_6.addWidget(self.widget, 0, 0, 1, 1)
        self.splitter = QtGui.QSplitter(showHistory)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.historyPanel = QtGui.QWidget(self.splitter)
        self.historyPanel.setObjectName(_fromUtf8("historyPanel"))
        self.gridLayout_4 = QtGui.QGridLayout(self.historyPanel)
        self.gridLayout_4.setMargin(0)
        self.gridLayout_4.setMargin(0)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.groupBox = QgsCollapsibleGroupBoxBasic(self.historyPanel)
        self.groupBox.setProperty("collapsed", True)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayout_7 = QtGui.QGridLayout(self.groupBox)
        self.gridLayout_7.setMargin(3)
        self.gridLayout_7.setObjectName(_fromUtf8("gridLayout_7"))
        self.scrollArea = QtGui.QScrollArea(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName(_fromUtf8("scrollArea"))
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 312, 115))
        self.scrollAreaWidgetContents.setObjectName(_fromUtf8("scrollAreaWidgetContents"))
        self.gridLayout_9 = QtGui.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_9.setMargin(3)
        self.gridLayout_9.setObjectName(_fromUtf8("gridLayout_9"))
        self.displayColumnChangedFields = QtGui.QCheckBox(self.scrollAreaWidgetContents)
        self.displayColumnChangedFields.setChecked(True)
        self.displayColumnChangedFields.setObjectName(_fromUtf8("displayColumnChangedFields"))
        self.gridLayout_9.addWidget(self.displayColumnChangedFields, 2, 1, 1, 1)
        self.displayColumnChangedGeometry = QtGui.QCheckBox(self.scrollAreaWidgetContents)
        self.displayColumnChangedGeometry.setChecked(True)
        self.displayColumnChangedGeometry.setObjectName(_fromUtf8("displayColumnChangedGeometry"))
        self.gridLayout_9.addWidget(self.displayColumnChangedGeometry, 1, 1, 1, 1)
        self.displayColumnClientIP = QtGui.QCheckBox(self.scrollAreaWidgetContents)
        self.displayColumnClientIP.setObjectName(_fromUtf8("displayColumnClientIP"))
        self.gridLayout_9.addWidget(self.displayColumnClientIP, 3, 1, 1, 1)
        self.displayColumnApplication = QtGui.QCheckBox(self.scrollAreaWidgetContents)
        self.displayColumnApplication.setChecked(True)
        self.displayColumnApplication.setObjectName(_fromUtf8("displayColumnApplication"))
        self.gridLayout_9.addWidget(self.displayColumnApplication, 4, 0, 1, 1)
        self.displayColumnAction = QtGui.QCheckBox(self.scrollAreaWidgetContents)
        self.displayColumnAction.setChecked(True)
        self.displayColumnAction.setObjectName(_fromUtf8("displayColumnAction"))
        self.gridLayout_9.addWidget(self.displayColumnAction, 3, 0, 1, 1)
        self.displayColumnClientPort = QtGui.QCheckBox(self.scrollAreaWidgetContents)
        self.displayColumnClientPort.setObjectName(_fromUtf8("displayColumnClientPort"))
        self.gridLayout_9.addWidget(self.displayColumnClientPort, 4, 1, 1, 1)
        self.displayColumnUser = QtGui.QCheckBox(self.scrollAreaWidgetContents)
        self.displayColumnUser.setChecked(True)
        self.displayColumnUser.setObjectName(_fromUtf8("displayColumnUser"))
        self.gridLayout_9.addWidget(self.displayColumnUser, 2, 0, 1, 1)
        self.displayColumnDate = QtGui.QCheckBox(self.scrollAreaWidgetContents)
        self.displayColumnDate.setChecked(True)
        self.displayColumnDate.setObjectName(_fromUtf8("displayColumnDate"))
        self.gridLayout_9.addWidget(self.displayColumnDate, 1, 0, 1, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout_7.addWidget(self.scrollArea, 0, 0, 1, 1)
        self.gridLayout_4.addWidget(self.groupBox, 2, 0, 1, 1)
        self.logResultsWidget = QtGui.QWidget(self.historyPanel)
        self.logResultsWidget.setObjectName(_fromUtf8("logResultsWidget"))
        self.gridLayout_2 = QtGui.QGridLayout(self.logResultsWidget)
        self.gridLayout_2.setMargin(3)
        self.gridLayout_2.setMargin(0)
        self.gridLayout_2.setHorizontalSpacing(3)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.gridLayout_4.addWidget(self.logResultsWidget, 3, 0, 1, 1)
        self.featurePanel = QtGui.QWidget(self.splitter)
        self.featurePanel.setObjectName(_fromUtf8("featurePanel"))
        self.gridLayout_5 = QtGui.QGridLayout(self.featurePanel)
        self.gridLayout_5.setMargin(0)
        self.gridLayout_5.setMargin(0)
        self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
        spacerItem2 = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        self.gridLayout_5.addItem(spacerItem2, 0, 1, 1, 1)
        self.pushButton_2 = QtGui.QPushButton(self.featurePanel)
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.gridLayout_5.addWidget(self.pushButton_2, 0, 2, 1, 1)
        self.differenceWidget = QtGui.QWidget(self.featurePanel)
        self.differenceWidget.setObjectName(_fromUtf8("differenceWidget"))
        self.gridLayout_3 = QtGui.QGridLayout(self.differenceWidget)
        self.gridLayout_3.setMargin(0)
        self.gridLayout_3.setMargin(0)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.gridLayout_5.addWidget(self.differenceWidget, 1, 0, 1, 3)
        self.gridLayout_6.addWidget(self.splitter, 3, 0, 1, 1)

        self.retranslateUi(showHistory)
        QtCore.QMetaObject.connectSlotsByName(showHistory)

    def retranslateUi(self, showHistory):
        showHistory.setWindowTitle(QtGui.QApplication.translate("showHistory", "Postgres 91 plus Auditor :: search history", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("showHistory", "Layer", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("showHistory", "Feature", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("showHistory", "Primary key", None, QtGui.QApplication.UnicodeUTF8))
        self.searchButton.setText(QtGui.QApplication.translate("showHistory", "search", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("showHistory", "Advanced search", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox.setText(QtGui.QApplication.translate("showHistory", "Updates", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox_3.setText(QtGui.QApplication.translate("showHistory", "Insert", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox_2.setText(QtGui.QApplication.translate("showHistory", "Delete", None, QtGui.QApplication.UnicodeUTF8))
        self.searchOnlyGeometry.setText(QtGui.QApplication.translate("showHistory", "Search only for geometry changes", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("showHistory", "Columns", None, QtGui.QApplication.UnicodeUTF8))
        self.displayColumnChangedFields.setText(QtGui.QApplication.translate("showHistory", "changed fields", None, QtGui.QApplication.UnicodeUTF8))
        self.displayColumnChangedGeometry.setText(QtGui.QApplication.translate("showHistory", "changed geometry", None, QtGui.QApplication.UnicodeUTF8))
        self.displayColumnClientIP.setText(QtGui.QApplication.translate("showHistory", "client IP", None, QtGui.QApplication.UnicodeUTF8))
        self.displayColumnApplication.setText(QtGui.QApplication.translate("showHistory", "application", None, QtGui.QApplication.UnicodeUTF8))
        self.displayColumnAction.setText(QtGui.QApplication.translate("showHistory", "action", None, QtGui.QApplication.UnicodeUTF8))
        self.displayColumnClientPort.setText(QtGui.QApplication.translate("showHistory", "client port", None, QtGui.QApplication.UnicodeUTF8))
        self.displayColumnUser.setText(QtGui.QApplication.translate("showHistory", "user", None, QtGui.QApplication.UnicodeUTF8))
        self.displayColumnDate.setText(QtGui.QApplication.translate("showHistory", "date", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_2.setText(QtGui.QApplication.translate("showHistory", "Set feature", None, QtGui.QApplication.UnicodeUTF8))

from qgis.gui import QgsCollapsibleGroupBoxBasic
