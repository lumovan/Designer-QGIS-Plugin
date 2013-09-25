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

    def __init__(self):
        QDialog.__init__(self)
        self.setupUi(self)
        QObject.connect(self.btnWorkspaceDir, SIGNAL("clicked()"), self.setWorkspaceDir)
        QObject.connect(self.btnCommand, SIGNAL("clicked()"), self.setExecutable)
        QObject.connect(self.btnInitializeWorkspace, SIGNAL("clicked()"), self.initializeWorkspace)

    def on_buttonBox_accepted(self):
        # TODO? check to see if all vars are set?
        #if True:
        #    return False
        self.emit( SIGNAL("workspaceDirSet(QString)"), self.leWorkspaceDir.text() )
        self.emit( SIGNAL("commandSet(QString)"), self.leCommand.text() )

    def setExecutable(self):
        self.leCommand.setText(QFileDialog.getOpenFileName(self, u"Please select the executable location"))


    def setWorkspaceDir(self):
        self.leWorkspaceDir.setText(QFileDialog.getExistingDirectory(self, u"Please select a workspace folder"))

    def initializeWorkspace(self):
        self.emit( SIGNAL("workspaceDirSet(QString)"), self.leWorkspaceDir.text() )
        self.emit( SIGNAL("commandSet(QString)"), self.leCommand.text() )
        self.emit( SIGNAL("workpaceInit(QString)"), self.leCommand.text() )



