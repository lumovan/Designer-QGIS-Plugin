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
        QObject.connect(self.btnInputDir, SIGNAL("clicked()"), self.setInputDir)
        QObject.connect(self.btnOutputDir, SIGNAL("clicked()"), self.setOutputDir)
        QObject.connect(self.btnCommand, SIGNAL("clicked()"), self.testCommand)

    def on_buttonBox_accepted(self):
        # TODO? check to see if all vars are set?
        #if True:
        #    return False
        self.emit( SIGNAL("inputDirSet(QString)"), self.leInputDir.text() )
        self.emit( SIGNAL("outputDirSet(QString)"), self.leOutputDir.text() )
        self.emit( SIGNAL("commandSet(QString)"), self.leCommand.text() )

    def testCommand(self):
        self.leCommand.setText(QFileDialog.getOpenFileName(self, u"Please give command to run (with path)"))

    def setInputDir(self):
        self.leInputDir.setText(QFileDialog.getExistingDirectory(self, u"Please provide directory for INPUT files"))

    def setOutputDir(self):
        self.leOutputDir.setText(QFileDialog.getExistingDirectory(self, u"Please provide directory for OUTPUT files"))




