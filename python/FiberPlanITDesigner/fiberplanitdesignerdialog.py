# -*- coding: utf-8 -*-
"""
/***************************************************************************
 FiberPlanITDesignerDialog
                                 A QGIS plugin
 todo
                             -------------------
        begin                : 2013-02-06
        copyright            : (C) 2013 by Comsof
        email                : luc.deheyn@comsof.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from ui_fiberplanitdesigner import Ui_FiberPlanITDesigner

class FiberPlanITDesignerDialog(QDialog, Ui_FiberPlanITDesigner):

    def __init__(self, fpiMain):
        QDialog.__init__(self)
        self.setupUi(self)
        QObject.connect(self.btnWorkspaceDir, SIGNAL("clicked()"), self.setWorkspaceDir)
        QObject.connect(self.btnCommand, SIGNAL("clicked()"), self.setExecutable)
        QObject.connect(self.btnInitializeWorkspace, SIGNAL("clicked()"), self.initializeWorkspace)
        self.fpiMain = fpiMain

    def on_buttonBox_accepted(self):
        # TODO? check to see if all vars are set?
        #if True:
        #    return False
        self.emit( SIGNAL("workspaceDirSet(QString)"), self.leWorkspaceDir.text() )
        self.emit( SIGNAL("commandSet(QString)"), self.leCommand.text() )

    def setExecutable(self):
        selectedFile = QFileDialog.getOpenFileName(self, u"Please select the executable location", self.fpiMain.command)
        if selectedFile:
            self.leCommand.setText(selectedFile)


    def setWorkspaceDir(self):
        selectedFolder = QFileDialog.getExistingDirectory(self, u"Please select a workspace folder", self.fpiMain.workspacedir)
        if selectedFolder:
            self.leWorkspaceDir.setText(selectedFolder)

    def initializeWorkspace(self):
        self.emit( SIGNAL("workspaceDirSet(QString)"), self.leWorkspaceDir.text() )
        self.emit( SIGNAL("commandSet(QString)"), self.leCommand.text() )

        if self.fpiMain.command is None or self.fpiMain.command == '':
            QMessageBox.warning(self, "No executable specified", u"Please select an executable first.", QMessageBox.Ok, QMessageBox.Ok)
        elif self.fpiMain.workspacedir is None or self.fpiMain.workspacedir == '':
            QMessageBox.warning(self, "No workspace selected", u"Please select a workspace first.", QMessageBox.Ok, QMessageBox.Ok)
        else:
            self.emit( SIGNAL("workpaceInit(QString)"), self.leCommand.text() )



