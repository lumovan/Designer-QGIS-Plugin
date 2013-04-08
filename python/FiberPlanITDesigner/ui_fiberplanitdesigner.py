# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_fiberplanitdesigner.ui'
#
# Created: Tue Feb 12 15:15:10 2013
#      by: PyQt4 UI code generator 4.9.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_FiberPlanITDesigner(object):
    def setupUi(self, FiberPlanITDesigner):
        FiberPlanITDesigner.setObjectName(_fromUtf8("FiberPlanITDesigner"))
        FiberPlanITDesigner.resize(756, 277)
        self.gridLayout = QtGui.QGridLayout(FiberPlanITDesigner)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.btnCommand = QtGui.QPushButton(FiberPlanITDesigner)
        self.btnCommand.setObjectName(_fromUtf8("btnCommand"))
        self.gridLayout.addWidget(self.btnCommand, 2, 2, 1, 1)
        self.leCommand = QtGui.QLineEdit(FiberPlanITDesigner)
        self.leCommand.setObjectName(_fromUtf8("leCommand"))
        self.gridLayout.addWidget(self.leCommand, 2, 1, 1, 1)
        self.leOutputDir = QtGui.QLineEdit(FiberPlanITDesigner)
        self.leOutputDir.setObjectName(_fromUtf8("leOutputDir"))
        self.gridLayout.addWidget(self.leOutputDir, 1, 1, 1, 1)
        self.btnOutputDir = QtGui.QPushButton(FiberPlanITDesigner)
        self.btnOutputDir.setObjectName(_fromUtf8("btnOutputDir"))
        self.gridLayout.addWidget(self.btnOutputDir, 1, 2, 1, 1)
        self.leInputDir = QtGui.QLineEdit(FiberPlanITDesigner)
        self.leInputDir.setObjectName(_fromUtf8("leInputDir"))
        self.gridLayout.addWidget(self.leInputDir, 0, 1, 1, 1)
        self.lblCommand = QtGui.QLabel(FiberPlanITDesigner)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblCommand.sizePolicy().hasHeightForWidth())
        self.lblCommand.setSizePolicy(sizePolicy)
        self.lblCommand.setObjectName(_fromUtf8("lblCommand"))
        self.gridLayout.addWidget(self.lblCommand, 2, 0, 1, 1)
        self.lblOutputDir = QtGui.QLabel(FiberPlanITDesigner)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblOutputDir.sizePolicy().hasHeightForWidth())
        self.lblOutputDir.setSizePolicy(sizePolicy)
        self.lblOutputDir.setObjectName(_fromUtf8("lblOutputDir"))
        self.gridLayout.addWidget(self.lblOutputDir, 1, 0, 1, 1)
        self.lblInputDir = QtGui.QLabel(FiberPlanITDesigner)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblInputDir.sizePolicy().hasHeightForWidth())
        self.lblInputDir.setSizePolicy(sizePolicy)
        self.lblInputDir.setObjectName(_fromUtf8("lblInputDir"))
        self.gridLayout.addWidget(self.lblInputDir, 0, 0, 1, 1)
        self.btnInputDir = QtGui.QPushButton(FiberPlanITDesigner)
        self.btnInputDir.setObjectName(_fromUtf8("btnInputDir"))
        self.gridLayout.addWidget(self.btnInputDir, 0, 2, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(FiberPlanITDesigner)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 3, 0, 1, 3)

        self.retranslateUi(FiberPlanITDesigner)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), FiberPlanITDesigner.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), FiberPlanITDesigner.reject)
        QtCore.QMetaObject.connectSlotsByName(FiberPlanITDesigner)

    def retranslateUi(self, FiberPlanITDesigner):
        FiberPlanITDesigner.setWindowTitle(QtGui.QApplication.translate("FiberPlanITDesigner", "FiberPlanIT Designer Plugin config", None, QtGui.QApplication.UnicodeUTF8))
        self.btnCommand.setText(QtGui.QApplication.translate("FiberPlanITDesigner", "Browse", None, QtGui.QApplication.UnicodeUTF8))
        self.leCommand.setText(QtGui.QApplication.translate("FiberPlanITDesigner", "Executable (with path)", None, QtGui.QApplication.UnicodeUTF8))
        self.leCommand.setPlaceholderText(QtGui.QApplication.translate("FiberPlanITDesigner", "Executable (with path)", None, QtGui.QApplication.UnicodeUTF8))
        self.leOutputDir.setText(QtGui.QApplication.translate("FiberPlanITDesigner", "Path to output folder", None, QtGui.QApplication.UnicodeUTF8))
        self.leOutputDir.setPlaceholderText(QtGui.QApplication.translate("FiberPlanITDesigner", "Path to output folder", None, QtGui.QApplication.UnicodeUTF8))
        self.btnOutputDir.setText(QtGui.QApplication.translate("FiberPlanITDesigner", "Browse", None, QtGui.QApplication.UnicodeUTF8))
        self.leInputDir.setText(QtGui.QApplication.translate("FiberPlanITDesigner", "Path to input folder", None, QtGui.QApplication.UnicodeUTF8))
        self.leInputDir.setPlaceholderText(QtGui.QApplication.translate("FiberPlanITDesigner", "Path to input folder", None, QtGui.QApplication.UnicodeUTF8))
        self.lblCommand.setText(QtGui.QApplication.translate("FiberPlanITDesigner", "Command", None, QtGui.QApplication.UnicodeUTF8))
        self.lblOutputDir.setText(QtGui.QApplication.translate("FiberPlanITDesigner", "Output dir", None, QtGui.QApplication.UnicodeUTF8))
        self.lblInputDir.setText(QtGui.QApplication.translate("FiberPlanITDesigner", "Input dir", None, QtGui.QApplication.UnicodeUTF8))
        self.btnInputDir.setText(QtGui.QApplication.translate("FiberPlanITDesigner", "Browse", None, QtGui.QApplication.UnicodeUTF8))

