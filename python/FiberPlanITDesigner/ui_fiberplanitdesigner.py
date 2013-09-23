# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Abram\IdeaProjects\FiberPlanIT_Wrap\QGisDesignerPlugin\python\FiberPlanITDesigner\ui_fiberplanitdesigner.ui'
#
# Created: Fri Sep 20 17:16:57 2013
#      by: PyQt4 UI code generator 4.10.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_FiberPlanITDesigner(object):
    def setupUi(self, FiberPlanITDesigner):
        FiberPlanITDesigner.setObjectName(_fromUtf8("FiberPlanITDesigner"))
        FiberPlanITDesigner.resize(756, 131)
        self.gridLayout = QtGui.QGridLayout(FiberPlanITDesigner)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.buttonBox = QtGui.QDialogButtonBox(FiberPlanITDesigner)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout_2.addWidget(self.buttonBox, 3, 1, 1, 3)
        self.btnCommand = QtGui.QPushButton(FiberPlanITDesigner)
        self.btnCommand.setObjectName(_fromUtf8("btnCommand"))
        self.gridLayout_2.addWidget(self.btnCommand, 0, 2, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem, 2, 1, 1, 1)
        self.lblCommand = QtGui.QLabel(FiberPlanITDesigner)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblCommand.sizePolicy().hasHeightForWidth())
        self.lblCommand.setSizePolicy(sizePolicy)
        self.lblCommand.setObjectName(_fromUtf8("lblCommand"))
        self.gridLayout_2.addWidget(self.lblCommand, 0, 0, 1, 1, QtCore.Qt.AlignRight)
        self.leWorkspaceDir = QtGui.QLineEdit(FiberPlanITDesigner)
        self.leWorkspaceDir.setObjectName(_fromUtf8("leWorkspaceDir"))
        self.gridLayout_2.addWidget(self.leWorkspaceDir, 1, 1, 1, 1)
        self.lblOutputDir = QtGui.QLabel(FiberPlanITDesigner)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblOutputDir.sizePolicy().hasHeightForWidth())
        self.lblOutputDir.setSizePolicy(sizePolicy)
        self.lblOutputDir.setObjectName(_fromUtf8("lblOutputDir"))
        self.gridLayout_2.addWidget(self.lblOutputDir, 1, 0, 1, 1, QtCore.Qt.AlignRight)
        self.leCommand = QtGui.QLineEdit(FiberPlanITDesigner)
        self.leCommand.setObjectName(_fromUtf8("leCommand"))
        self.gridLayout_2.addWidget(self.leCommand, 0, 1, 1, 1)
        self.btnWorkspaceDir = QtGui.QPushButton(FiberPlanITDesigner)
        self.btnWorkspaceDir.setObjectName(_fromUtf8("btnWorkspaceDir"))
        self.gridLayout_2.addWidget(self.btnWorkspaceDir, 1, 2, 1, 1)
        self.btnInitilaizeWorkspace = QtGui.QPushButton(FiberPlanITDesigner)
        self.btnInitilaizeWorkspace.setObjectName(_fromUtf8("btnInitilaizeWorkspace"))
        self.gridLayout_2.addWidget(self.btnInitilaizeWorkspace, 1, 3, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_2, 4, 0, 1, 1)

        self.retranslateUi(FiberPlanITDesigner)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), FiberPlanITDesigner.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), FiberPlanITDesigner.reject)
        QtCore.QMetaObject.connectSlotsByName(FiberPlanITDesigner)
        FiberPlanITDesigner.setTabOrder(self.btnCommand, self.btnWorkspaceDir)
        FiberPlanITDesigner.setTabOrder(self.btnWorkspaceDir, self.btnInitilaizeWorkspace)
        FiberPlanITDesigner.setTabOrder(self.btnInitilaizeWorkspace, self.buttonBox)
        FiberPlanITDesigner.setTabOrder(self.buttonBox, self.leCommand)
        FiberPlanITDesigner.setTabOrder(self.leCommand, self.leWorkspaceDir)

    def retranslateUi(self, FiberPlanITDesigner):
        FiberPlanITDesigner.setWindowTitle(_translate("FiberPlanITDesigner", "FiberPlanIT Designer Plugin config", None))
        self.btnCommand.setText(_translate("FiberPlanITDesigner", "Browse", None))
        self.lblCommand.setText(_translate("FiberPlanITDesigner", "Command", None))
        self.leWorkspaceDir.setText(_translate("FiberPlanITDesigner", "Path to workspace folder", None))
        self.leWorkspaceDir.setPlaceholderText(_translate("FiberPlanITDesigner", "Path to output folder", None))
        self.lblOutputDir.setText(_translate("FiberPlanITDesigner", "Workspace dir", None))
        self.leCommand.setText(_translate("FiberPlanITDesigner", "Executable (with path)", None))
        self.leCommand.setPlaceholderText(_translate("FiberPlanITDesigner", "Executable (with path)", None))
        self.btnWorkspaceDir.setText(_translate("FiberPlanITDesigner", "Browse", None))
        self.btnInitilaizeWorkspace.setText(_translate("FiberPlanITDesigner", "Initialize", None))

