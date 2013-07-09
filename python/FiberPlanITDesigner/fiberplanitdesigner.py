# -*- coding: utf-8 -*-
"""
/***************************************************************************
 FiberPlanITDesigner
                                 A QGIS plugin

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
# Import the PyQt and QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
# Initialize Qt resources from file resources.py
import resources_rc
# Import the code for the dialog
from fiberplanitdesignerdialog import FiberPlanITDesignerDialog

import subprocess # for calling external processes
import os
import shutil # for copying files
import operator

class FiberPlanITDesigner:

    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/python/plugins/fiberplanitdesigner"
        # initialize locale
        localePath = ""
        locale = QSettings().value("locale/userLocale").toString()[0:2]

        if QFileInfo(self.plugin_dir).exists():
            localePath = self.plugin_dir + "/i18n/fiberplanitdesigner_" + locale + ".qm"

        if QFileInfo(localePath).exists():
            self.translator = QTranslator()
            self.translator.load(localePath)
            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)
        # Create the dialog (after translation) and keep reference
        self.dlg = FiberPlanITDesignerDialog()
        self.settings = QSettings()
        self.inputdir = ''
        # from settings you retrieve a QVariant!
        if self.settings.contains('/fiberplanitdesigner/inputpath'):
            self.inputdir = unicode(self.settings.value('/fiberplanitdesigner/inputpath').toString())
        self.outputdir = ''
        if self.settings.contains('/fiberplanitdesigner/outputpath'):
            self.outputdir = unicode(self.settings.value('/fiberplanitdesigner/outputpath').toString())
        self.command = ''
        if self.settings.contains('/fiberplanitdesigner/command'):
            self.command = unicode(self.settings.value('/fiberplanitdesigner/command').toString())
        QObject.connect(self.dlg, SIGNAL("inputDirSet(QString)"), self.setInputDir)
        QObject.connect(self.dlg, SIGNAL("outputDirSet(QString)"), self.setOutputDir)
        QObject.connect(self.dlg, SIGNAL("commandSet(QString)"), self.setCommand)

    def initGui(self):
        # Add toolbar 
        self.toolBar = self.iface.addToolBar(QCoreApplication.translate("fiberplanitdesigner","FiberplanIT Designer"))
        self.toolBar.setObjectName("FiberplanIT Designer")

        self.actiontxt = QCoreApplication.translate("fiberplanitdesigner","FiberplanIT Designer")
        self.action = QAction(
            QIcon(":/plugins/fiberplanitdesigner/icon.png"),
            self.actiontxt, self.iface.mainWindow())
        # 3 groups 

        # GROUP 1_1: configure /configure

        # GROUP 2_1: switch to area view (input folder project)
        # GROUP 2_2: create trenches /streetDoubler
        # GROUP 2_3: create drop trenches /createBuildingTrenches
        # GROUP 2_4: create crossings /createCrossings
        # GROUP 2_5: process ares /procesInput

        # GROUP 3_1: switch to design view (output folder project)
        # GROUP 3_2: calculate distribution /calculateDistribution
        # GROUP 3_3: lock/unlock elements
        # GROUP 3_4: calculate network /calculate
        # GROUP 3_5: show bill of material (show FPI-BoM.xlsx)

        self.action_1_2_txt = QCoreApplication.translate("fiberplanitdesigner", u"Configure FiberPlanIT Designer Plugin")
        self.action_1_2 = QAction(
            QIcon(":/plugins/fiberplanitdesigner/icons/toolbox.png"),
            self.action_1_2_txt, self.iface.mainWindow())
        QObject.connect(self.action_1_2, SIGNAL("triggered()"), self.configure2)
        # this one NOT in the toolbar (only in menu)
        #self.toolBar.addAction(self.action_1_2)
        self.iface.addPluginToMenu(self.actiontxt, self.action_1_2)

        self.action_1_1_txt = QCoreApplication.translate("fiberplanitdesigner", u"Edit Rules")
        self.action_1_1 = QAction(
            QIcon(":/plugins/fiberplanitdesigner/icons/cog.png"),
            self.action_1_1_txt, self.iface.mainWindow())
        QObject.connect(self.action_1_1, SIGNAL("triggered()"), self.configure)
        self.toolBar.addAction(self.action_1_1)
        self.iface.addPluginToMenu(self.actiontxt, self.action_1_1)

        self.toolBar.addSeparator()

        self.action_2_1_txt = QCoreApplication.translate("fiberplanitdesigner", u"Switch to Area View")
        self.action_2_1 = QAction(
            QIcon(":/plugins/fiberplanitdesigner/icons/map.png"),
            self.action_2_1_txt, self.iface.mainWindow())
        QObject.connect(self.action_2_1, SIGNAL("triggered()"), self.areaview)
        self.toolBar.addAction(self.action_2_1)
        self.iface.addPluginToMenu(self.actiontxt, self.action_2_1)

        self.action_2_2_txt = QCoreApplication.translate("fiberplanitdesigner", u"Create Trenches")
        self.action_2_2 = QAction(
            QIcon(":/plugins/fiberplanitdesigner/icons/doubler.png"),
            self.action_2_2_txt, self.iface.mainWindow())
        QObject.connect(self.action_2_2, SIGNAL("triggered()"), self.createtrenches)
        self.toolBar.addAction(self.action_2_2)
        self.iface.addPluginToMenu(self.actiontxt, self.action_2_2)

        self.action_2_3_txt = QCoreApplication.translate("fiberplanitdesigner", u"Create Drop Trenches")
        self.action_2_3 = QAction(
            QIcon(":/plugins/fiberplanitdesigner/icons/drop.png"),
            self.action_2_3_txt, self.iface.mainWindow())
        QObject.connect(self.action_2_3, SIGNAL("triggered()"), self.createbuildingtrenches)
        self.toolBar.addAction(self.action_2_3)
        self.iface.addPluginToMenu(self.actiontxt, self.action_2_3)

        self.action_2_4_txt = QCoreApplication.translate("fiberplanitdesigner", u"Create Crossings")
        self.action_2_4 = QAction(
            QIcon(":/plugins/fiberplanitdesigner/icons/crossing.png"),
            self.action_2_4_txt, self.iface.mainWindow())
        QObject.connect(self.action_2_4, SIGNAL("triggered()"), self.createcrossings)
        self.toolBar.addAction(self.action_2_4)
        self.iface.addPluginToMenu(self.actiontxt, self.action_2_4)
        
        self.action_2_5_txt = QCoreApplication.translate("fiberplanitdesigner", u"Process Area")
        self.action_2_5 = QAction(
            QIcon(":/plugins/fiberplanitdesigner/icons/process area.png"),
            self.action_2_5_txt, self.iface.mainWindow())
        QObject.connect(self.action_2_5, SIGNAL("triggered()"), self.processarea)
        self.toolBar.addAction(self.action_2_5)
        self.iface.addPluginToMenu(self.actiontxt, self.action_2_5)

        self.toolBar.addSeparator()

        self.action_3_1_txt = QCoreApplication.translate("fiberplanitdesigner", u"Switch to Design View")
        self.action_3_1 = QAction(
            QIcon(":/plugins/fiberplanitdesigner/icons/blueprint.png"),
            self.action_3_1_txt, self.iface.mainWindow())
        QObject.connect(self.action_3_1, SIGNAL("triggered()"), self.designview)
        self.toolBar.addAction(self.action_3_1)
        self.iface.addPluginToMenu(self.actiontxt, self.action_3_1)

        self.action_3_2_txt = QCoreApplication.translate("fiberplanitdesigner", u"Calculate Distribution")
        self.action_3_2 = QAction(
            QIcon(":/plugins/fiberplanitdesigner/icons/fiberplanit_distribution.png"),
            self.action_3_2_txt, self.iface.mainWindow())
        QObject.connect(self.action_3_2, SIGNAL("triggered()"), self.calculatedistribution)
        self.toolBar.addAction(self.action_3_2)
        self.iface.addPluginToMenu(self.actiontxt, self.action_3_2)

        self.action_3_4_txt = QCoreApplication.translate("fiberplanitdesigner", u"Calculate Network")
        self.action_3_4 = QAction(
            QIcon(":/plugins/fiberplanitdesigner/icons/fiberplanit.png"),
            self.action_3_4_txt, self.iface.mainWindow())
        QObject.connect(self.action_3_4, SIGNAL("triggered()"), self.calculatenetwork)
        self.toolBar.addAction(self.action_3_4)
        self.iface.addPluginToMenu(self.actiontxt, self.action_3_4)

        self.action_3_3_txt = QCoreApplication.translate("fiberplanitdesigner", u"Lock/Unlock Selected Elements")
        self.action_3_3 = QAction(
            QIcon(":/plugins/fiberplanitdesigner/icons/lock.png"),
            self.action_3_3_txt, self.iface.mainWindow())
        QObject.connect(self.action_3_3, SIGNAL("triggered()"), self.lockUnlockElements)
        self.toolBar.addAction(self.action_3_3)
        self.iface.addPluginToMenu(self.actiontxt, self.action_3_3)
         # lockUnlockElements is triggered by the F11
        self.iface.registerMainWindowAction(self.action_3_3, "F11")
        
        self.toolBar.addSeparator()

        self.action_3_5_txt = QCoreApplication.translate("fiberplanitdesigner", u"Show Bill of Material")
        self.action_3_5 = QAction(
            QIcon(":/plugins/fiberplanitdesigner/icons/file_extension_xls.png"),
            self.action_3_5_txt, self.iface.mainWindow())
        QObject.connect(self.action_3_5, SIGNAL("triggered()"), self.showbillofmaterial)
        self.toolBar.addAction(self.action_3_5)
        self.iface.addPluginToMenu(self.actiontxt, self.action_3_5)

    def unload(self):
        # Remove the plugin menu item and icon
        self.iface.removePluginMenu(self.actiontxt, self.action_1_1)
        self.iface.removePluginMenu(self.actiontxt, self.action_1_2)
        self.iface.removePluginMenu(self.actiontxt, self.action_2_1)
        self.iface.removePluginMenu(self.actiontxt, self.action_2_2)
        self.iface.removePluginMenu(self.actiontxt, self.action_2_3)
        self.iface.removePluginMenu(self.actiontxt, self.action_2_4)
        self.iface.removePluginMenu(self.actiontxt, self.action_2_5)
        self.iface.removePluginMenu(self.actiontxt, self.action_3_1)
        self.iface.removePluginMenu(self.actiontxt, self.action_3_2)
        self.iface.removePluginMenu(self.actiontxt, self.action_3_3)
        self.iface.removePluginMenu(self.actiontxt, self.action_3_4)
        self.iface.removePluginMenu(self.actiontxt, self.action_3_5)

        self.iface.removePluginMenu(self.actiontxt, self.action)

    def setInputDir(self, inputdir):
        # from dialog signal you receive a QString
        self.inputdir = unicode(inputdir)
        self.settings.setValue('/fiberplanitdesigner/inputpath', inputdir)

    def setOutputDir(self, outputdir):
        self.outputdir = unicode(outputdir)
        self.settings.setValue('/fiberplanitdesigner/outputpath', outputdir)

    def setCommand(self, command):
        self.command = unicode(command)
        self.settings.setValue('/fiberplanitdesigner/command', command)

    def configure(self):
        self.ensureConfigured()
        output = subprocess.call([self.command, '/configure', self.inputdir, self.outputdir])

    def configure2(self):
        self.dlg.leInputDir.setText(self.inputdir)
        self.dlg.leOutputDir.setText(self.outputdir)
        self.dlg.leCommand.setText(self.command)
        self.dlg.show()

    def nounsavededits(self):
        # check if there are any layers being edited
        layers = QgsMapLayerRegistry.instance().mapLayers()
        unsavedChangesFound = False
        for id in layers:
            if layers[id].type()==0 and layers[id].isEditable() and layers[id].isModified():
                unsavedChangesFound = True
                break
        if (unsavedChangesFound):
            # changeing this to "QMessageBox.warning" causes a crash (?)
            ret = QMessageBox.critical(self.iface.mainWindow(), "Warning", "There is at least one layer with unsaved edits.\nPress 'OK' to save all changes and continue.\nPress 'Cancel' to stop.", QMessageBox.Ok, QMessageBox.Cancel)
            #ret = QMessageBox.warning(self.iface.mainWindow(), QCoreApplication.translate("fiberplanitdesigner", "Edited layer"), QCoreApplication.translate("fiberplanitdesigner", "There is at least one layer with unsaved edits.\nPress ok to save all changes and continue.\nPress Cancel to stop."), QMessageBox.Ok, QMessageBox.Cancel):
            if (ret == QMessageBox.Ok):
                for id in layers:
                    if layers[id].type()==0 and layers[id].isEditable() and layers[id].isModified():
                        layers[id].commitChanges()
            else:
                return False

        # we also save current project here!!
        QgsProject.instance().write()
        return True

    def areaview(self):
        if self.nounsavededits():
            # first removing all layers (just to be sure ??)
            QgsMapLayerRegistry.instance().removeAllMapLayers()
            f = QFileInfo(self.inputdir+'/_Scheme.qgs')
            QgsProject.instance().read(f)

    def designview(self):
        if self.nounsavededits():
            # first removing all layers (just to be sure ??)
            QgsMapLayerRegistry.instance().removeAllMapLayers()
            f = QFileInfo(self.outputdir+'/_Scheme.qgs')
            QgsProject.instance().read(f)

    def zoomToLayer(self, layername):
        for layer in self.iface.mapCanvas().layers():
            if layer.name() == layername:
                self.iface.mapCanvas().setExtent(layer.extent())
                self.iface.mapCanvas().refresh()

    def ensureConfigured(self):
        # test for empty plugin variables
        if  (self.inputdir is None or self.inputdir == '') or (self.outputdir is None or self.outputdir == '') or (self.command is None or self.command == ''):
            self.configure2()

    def callFPI(self, argument):
        self.ensureConfigured()
        # first removing all layers (just to be sure ??)
        QgsMapLayerRegistry.instance().removeAllMapLayers()
        # 'close' project first to be sure we do not mess up the projects
        self.iface.newProject() # newProject(False) == default == NO save dialog
        self.iface.mapCanvas().refresh()
        # run FPI with given argument
        exitcode = subprocess.call([self.command, argument, self.inputdir, self.outputdir], cwd=os.path.dirname(self.command))
        if exitcode > 0:
            QMessageBox.warning(self.iface.mainWindow(), "-", ( QCoreApplication.translate("fiberplanitdesigner","FPI returned an error code: ") + str(exitcode)), QMessageBox.Ok, QMessageBox.Ok)
        else:
            #QMessageBox.warning(self.iface.mainWindow(), "-", ( QCoreApplication.translate("fiberplanitdesigner","FPI ready (0 == OK): " + str(exitcode)), QMessageBox.Ok, QMessageBox.Ok)
            pass

    def createtrenches(self):
        if self.nounsavededits():
            self.callFPI('/streetDoubler')
            self.areaview()

    def createbuildingtrenches(self):
        if self.nounsavededits():
            self.callFPI('/createBuildingTrenches')
            self.areaview()
    
    def createcrossings(self):
        if self.nounsavededits():
            self.callFPI('/createCrossings')
            self.areaview()

    def processarea(self):
        if self.nounsavededits():
            self.callFPI('/processInput')
            self.areaview()

    def calculatedistribution(self):
        if self.nounsavededits():
            self.callFPI('/calculateDistributionAndLock')
            self.designview()
            # example to zoom to a layer
            self.zoomToLayer('IN_PossibleTrenches')


    def calculatenetwork(self):
        if self.nounsavededits():
            self.callFPI('/calculateAndLock')
            self.designview()

    def showbillofmaterial(self):
        output = subprocess.call([unicode(self.outputdir)+u'/FPI - BoM.xlsx'], shell=True)

    def lockUnlockElements(self):
        layer = self.iface.mapCanvas().currentLayer()
        if (layer == None):
        	infoString = QString("No layer selected... Select a layer from the layer list...")
        	QMessageBox.warning(self.iface.mainWindow(), "-", infoString, QMessageBox.Ok, QMessageBox.Ok)
        	return

        provider = layer.dataProvider()
        fields = provider.fields()

        # Get the "LOCKED" attribute
        locked_index = provider.fieldNameIndex("LOCKED")
        if (locked_index == -1):
        	infoString = QString("Locking not possible on selected layer. LOCK attribute missing.")
        	QMessageBox.warning(self.iface.mainWindow(), "-", infoString, QMessageBox.Ok, QMessageBox.Ok)
        	return

        if not layer.isEditable():
        	layer.startEditing()

        # number of features
        nF = layer.selectedFeatureCount()
        if (nF == 0):
        	infoString = QString("Select some elements in current <b>" + layer.name() + "</b> layer for locking")
        	QMessageBox.warning(self.iface.mainWindow(), "-", infoString, QMessageBox.Ok, QMessageBox.Ok)
        	return

        selectedFeatIDs = layer.selectedFeaturesIds()
        selectedFeats = layer.selectedFeatures()

        trueValue = QVariant("T")
        falseValue = QVariant("F")

        mixedLockUnlock = False
        lockedSeen = False
        unlockedSeen = False
        for feat in selectedFeats:
            for (k, attr) in feat.attributeMap().iteritems():
                if (fields[k].name() == "LOCKED"):
                    if (attr.toString() == "F"):
                        unlockedSeen = True
                        newValue = trueValue
                    else:
                        lockedSeen = True
                        newValue = falseValue

        if (lockedSeen and unlockedSeen):
            infoString = QString("Both locked and unlocked elements selected. Everything will be locked.")
            QMessageBox.information(self.iface.mainWindow(), "Warning", infoString)
            newValue = trueValue

        # Change the attributes of the selected features
        for i in selectedFeatIDs:
        	layer.changeAttributeValue(int(i), locked_index, newValue)
        for i in selectedFeatIDs:
            layer.deselect(i)
        return