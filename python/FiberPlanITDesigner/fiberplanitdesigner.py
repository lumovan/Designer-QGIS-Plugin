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
        locale = QSettings().value("locale/userLocale")[0:2]

        if QFileInfo(self.plugin_dir).exists():
            localePath = self.plugin_dir + "/i18n/fiberplanitdesigner_" + locale + ".qm"

        if QFileInfo(localePath).exists():
            self.translator = QTranslator()
            self.translator.load(localePath)
            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)
        # Create the dialog (after translation) and keep reference
        self.dlg = FiberPlanITDesignerDialog(self)
        self.settings = QSettings()
        self.workspacedir = ''
        if self.settings.contains('/fiberplanitdesigner/workspacepath'):
            self.workspacedir = unicode(self.settings.value('/fiberplanitdesigner/workspacepath'))
        self.command = ''
        if self.settings.contains('/fiberplanitdesigner/command'):
            self.command = unicode(self.settings.value('/fiberplanitdesigner/command'))
        QObject.connect(self.dlg, SIGNAL("workspaceDirSet(QString)"), self.setWorkspacedirDir)
        QObject.connect(self.dlg, SIGNAL("commandSet(QString)"), self.setCommand)
        QObject.connect(self.dlg, SIGNAL("workpaceInit(QString)"), self.initWorkspace)

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

        ####### DROP
        # TODO: switch to QToolButton: http://gis.stackexchange.com/questions/59313/how-to-create-a-dropdown-menu-in-qgis-toolbar-with-python
        self.dropAction1_txt = QCoreApplication.translate("fiberplanitdesigner", u"Create Drop Trenches")
        self.dropAction2_txt = QCoreApplication.translate("fiberplanitdesigner", u"Create Drop Trenches Per 2 Buildings")

        self.dropAction = QAction(QIcon(":/plugins/fiberplanitdesigner/icons/drop.png"), self.dropAction1_txt, self.iface.mainWindow())
        self.dropAction1 = QAction(QIcon(":/plugins/fiberplanitdesigner/icons/drop.png"), self.dropAction1_txt, self.iface.mainWindow())
        self.dropAction2 = QAction(QIcon(":/plugins/fiberplanitdesigner/icons/drop2.png"), self.dropAction2_txt, self.iface.mainWindow())

        self.popupMenu = QMenu(self.iface.mainWindow())
        self.popupMenu.addAction(self.dropAction1)
        self.popupMenu.addAction(self.dropAction2)

        self.dropAction.triggered.connect(self.createbuildingtrenches)
        self.dropAction1.triggered.connect(self.createbuildingtrenches)
        self.dropAction2.triggered.connect(self.createpairedbuildingtrenches)

        self.dropAction.setMenu(self.popupMenu)
        self.toolBar.addAction(self.dropAction)

        # Add to the plug-in menu
        self.iface.addPluginToMenu(self.actiontxt, self.dropAction)
        #######

        self.action_2_4_txt = QCoreApplication.translate("fiberplanitdesigner", u"Create Crossings")
        self.action_2_4 = QAction(
            QIcon(":/plugins/fiberplanitdesigner/icons/crossing.png"),
            self.action_2_4_txt, self.iface.mainWindow())
        QObject.connect(self.action_2_4, SIGNAL("triggered()"), self.createcrossings)
        self.toolBar.addAction(self.action_2_4)
        self.iface.addPluginToMenu(self.actiontxt, self.action_2_4)
        
        ####### AERIAL
        self.aerialActionMenu_txt = QCoreApplication.translate("fiberplanitdesigner", u"Aerial")
        self.aerialActionMenu = QAction(
            QIcon(":/plugins/fiberplanitdesigner/icons/aerial.png"),
            self.aerialActionMenu_txt, self.iface.mainWindow())
        self.aerialAction1_txt = QCoreApplication.translate("fiberplanitdesigner", u"Create Aerial Connections")
        self.aerialAction1 = QAction(
            QIcon(":/plugins/fiberplanitdesigner/icons/aerial.png"),
            self.aerialAction1_txt, self.iface.mainWindow())
        self.aerialAction1.triggered.connect(self.createAerialConnections)

        self.aerialAction2_txt = QCoreApplication.translate("fiberplanitdesigner", u"Create Aerial Drop Connections")
        self.aerialAction2 = QAction(
            QIcon(":/plugins/fiberplanitdesigner/icons/aerial.png"),
            self.aerialAction2_txt, self.iface.mainWindow())
        self.aerialAction2.triggered.connect(self.createAerialDrops)
        
        self.popupMenu = QMenu(self.iface.mainWindow())
        self.popupMenu.addAction(self.aerialAction1)
        self.popupMenu.addAction(self.aerialAction2)

        self.aerialActionMenu.setMenu(self.popupMenu)
        #self.toolBar.addAction(self.aerialActionMenu)
        self.iface.addPluginToMenu(self.actiontxt, self.aerialActionMenu)
        
        #END
        
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

        ####### CALCULATE
        self.calculateAction1_txt = QCoreApplication.translate("fiberplanitdesigner", u"Calculate Network")
        self.calculateAction2_txt = QCoreApplication.translate("fiberplanitdesigner", u"Calculate Distribution Part")
        self.calculateAction3_txt = QCoreApplication.translate("fiberplanitdesigner", u"Calculate Drop Part")

        self.calculateAction = QAction(QIcon(":/plugins/fiberplanitdesigner/icons/fiberplanit.png"), self.calculateAction1_txt, self.iface.mainWindow())
        self.calculateAction1 = QAction(QIcon(":/plugins/fiberplanitdesigner/icons/fiberplanit.png"), self.calculateAction1_txt, self.iface.mainWindow())
        self.calculateAction2 = QAction(QIcon(":/plugins/fiberplanitdesigner/icons/fiberplanit_distribution.png"), self.calculateAction2_txt, self.iface.mainWindow())
        self.calculateAction3 = QAction(QIcon(":/plugins/fiberplanitdesigner/icons/fiberplanit_distribution.png"), self.calculateAction3_txt, self.iface.mainWindow())

        self.popupMenu = QMenu(self.iface.mainWindow())
        self.popupMenu.addAction(self.calculateAction1)
        self.popupMenu.addAction(self.calculateAction2)
        self.popupMenu.addAction(self.calculateAction3)

        self.calculateAction.triggered.connect(self.calculatenetwork)
        self.calculateAction1.triggered.connect(self.calculatenetwork)
        self.calculateAction2.triggered.connect(self.calculatedistribution)
        self.calculateAction3.triggered.connect(self.calculatedrop)

        self.calculateAction.setMenu(self.popupMenu)
        self.toolBar.addAction(self.calculateAction)

        # Add to the plug-in menu
        self.iface.addPluginToMenu(self.actiontxt, self.calculateAction)
        #######

        ####### LOCK
        self.action_3_3_txt = QCoreApplication.translate("fiberplanitdesigner", u"Lock/Unlock Selected Elements")
        self.action_3_3 = QAction(
            QIcon(":/plugins/fiberplanitdesigner/icons/lock.png"),
            self.action_3_3_txt, self.iface.mainWindow())
        QObject.connect(self.action_3_3, SIGNAL("triggered()"), self.lockUnlockElements)
        self.toolBar.addAction(self.action_3_3)
        self.iface.addPluginToMenu(self.actiontxt, self.action_3_3)
         # lockUnlockElements is triggered by the F11
        self.iface.registerMainWindowAction(self.action_3_3, "F11")
        #######

        self.toolBar.addSeparator()

        ####### STATE MANAGER
        self.stateManager_txt = QCoreApplication.translate("fiberplanitdesigner", u"Open State Manager")
        self.manageStatesAction = QAction(
            QIcon(":/plugins/fiberplanitdesigner/icons/file_manager.png"),
            self.stateManager_txt, self.iface.mainWindow())
        QObject.connect(self.manageStatesAction, SIGNAL("triggered()"), self.manageStates)
        self.toolBar.addAction(self.manageStatesAction)
        self.iface.addPluginToMenu(self.actiontxt, self.manageStatesAction)
        #######

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
        self.iface.removePluginMenu(self.actiontxt, self.dropAction)
        self.iface.removePluginMenu(self.actiontxt, self.action_2_4)
        self.iface.removePluginMenu(self.actiontxt, self.action_2_5)
        self.iface.removePluginMenu(self.actiontxt, self.action_3_1)
        self.iface.removePluginMenu(self.actiontxt, self.action_3_3)
         # lockUnlockElements is triggered by the F11
        self.iface.unregisterMainWindowAction(self.action_3_3)
        self.iface.removePluginMenu(self.actiontxt, self.calculateAction)
        self.iface.removePluginMenu(self.actiontxt, self.action_3_5)
        self.iface.removePluginMenu(self.actiontxt, self.manageStatesAction)
        self.iface.removePluginMenu(self.actiontxt, self.action)
        self.iface.removePluginMenu(self.actiontxt, self.aerialActionMenu)
        del self.toolBar

    def setWorkspacedirDir(self, workspacedir):
        self.workspacedir = unicode(workspacedir)
        self.settings.setValue('/fiberplanitdesigner/workspacepath', workspacedir)

    def setCommand(self, command):
        self.command = unicode(command)
        self.settings.setValue('/fiberplanitdesigner/command', command)

    def configure(self):
        self.ensureConfigured()
        output = subprocess.call([self.command, '/configure', self.workspacedir])

    def configure2(self):
        self.dlg.leWorkspaceDir.setText(self.workspacedir)
        self.dlg.leCommand.setText(self.command)
        #self.dlg.show()
        self.dlg.exec_() # makes dialog blocking

    def initWorkspace(self):
        self.dlg.close() #Needs to happens first or dialog freezes
        self.callFPI('/initWorkspace')
        # ok we have a filled workspace now
        # with two projects: 
        # areaview == input 
        # and 
        # designview == output
        # set rendering False so during loading of project there is no map visible
        self.iface.mapCanvas().setRenderFlag(False)
        # load input project
        self.areaview()
        # areaview holds a set of empty shape files which have NO crs
        # and optionally 1 or more shapefiles with an unknown crs
        # THAT unknown crs should be the crs for both the project and ALL layers
        # find project crs of current _Scheme.qgs project
        project_crs_wkt = self.iface.mapCanvas().mapRenderer().destinationCrs().toWkt()
        QMessageBox.warning(self.iface.mainWindow(), "-", "Project crs: "+  project_crs_wkt , QMessageBox.Ok, QMessageBox.Ok)
        # go over all layers to find layers with a known crs
        crs = None
        for lyr in self.iface.mapCanvas().layers():
            crs_wkt = lyr.dataProvider().crs().toWkt()
            if len(crs_wkt)>0:
                crs=QgsCoordinateReferenceSystem(crs_wkt)
                QMessageBox.warning(self.iface.mainWindow(), "-", "Layer crs: "+crs_wkt , QMessageBox.Ok, QMessageBox.Ok)
                break # only taking the first one
        # if none found: return. Probably we keep it 31370 and data will be that crs
        if crs is None:
            # nothing found
            return
        if project_crs_wkt == crs_wkt:
                QMessageBox.warning(self.iface.mainWindow(), "-", "Project crs == data crs: OK" , QMessageBox.Ok, QMessageBox.Ok)
        else:
                QMessageBox.warning(self.iface.mainWindow(), "-", "Project crs != data crs: fixing" , QMessageBox.Ok, QMessageBox.Ok)
        # else: set project crs and ALL layers crs to crs
        self.reset_and_write_crs(crs)
        # now do the same of designview/output
        self.designview()
        self.reset_and_write_crs(crs)
        # cleanup by removing all layers
        QgsMapLayerRegistry.instance().removeAllMapLayers()
        # set rendering to True again
        self.iface.mapCanvas().setRenderFlag(True)

    def reset_and_write_crs(self, crs):
        # set crs of project to crs
        self.iface.mapCanvas().mapRenderer().setDestinationCrs(crs)
        # go over ALL layers and set those to crs too
        for lyr in self.iface.mapCanvas().layers():
            lyr.setCrs(crs)
        # write this project as a TARGET CRS project
        QgsProject.instance().write()

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
            f = QFileInfo(self.workspacedir+'/input/_Scheme.qgs')
            QgsProject.instance().read(f)

    def designview(self):
        if self.nounsavededits():
            # first removing all layers (just to be sure ??)
            QgsMapLayerRegistry.instance().removeAllMapLayers()
            f = QFileInfo(self.workspacedir+'/output/_Scheme.qgs')
            QgsProject.instance().read(f)

    # example to zoom to a layer: self.zoomToLayer('IN_PossibleTrenches')
    def zoomToLayer(self, layername):
        for layer in self.iface.mapCanvas().layers():
            if layer.name() == layername:
                self.iface.mapCanvas().setExtent(layer.extent())
                self.iface.mapCanvas().refresh()

    def ensureConfigured(self):
        # test for empty plugin variables
        if (self.workspacedir is None or self.workspacedir == '') or (self.command is None or self.command == ''):
            self.configure2()

    def callFPI(self, argument):
        self.ensureConfigured()
        # first removing all layers (just to be sure ??)
        QgsMapLayerRegistry.instance().removeAllMapLayers()
        # 'close' project first to be sure we do not mess up the projects
        self.iface.newProject() # newProject(False) == default == NO save dialog
        self.iface.mapCanvas().refresh()
        # run FPI with given argument
        exitcode = subprocess.call([self.command, argument, self.workspacedir], cwd=os.path.dirname(self.command))
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

    def createpairedbuildingtrenches(self):
        if self.nounsavededits():
            self.callFPI('/createPairedBuildingTrenches')
            self.areaview()

    def createcrossings(self):
        if self.nounsavededits():
            self.callFPI('/createCrossings')
            self.areaview()

    def createAerialConnections(self):
        if self.nounsavededits():
            self.callFPI('/createAerialConnections')
            self.areaview()

    def createAerialDrops(self):
        if self.nounsavededits():
            self.callFPI('/createAerialDrops')
            self.areaview()

    def processarea(self):
        if self.nounsavededits():
            self.callFPI('/processInput')
            self.areaview()

    def manageStates(self):
        if self.nounsavededits():
            self.callFPI('/manageStates')
            self.designview()

    def calculatedistribution(self):
        if self.nounsavededits():
            self.callFPI('/calculateDistributionAndLock')
            self.designview()

    def calculatedrop(self):
        if self.nounsavededits():
            self.callFPI('/calculateDropAndLock')
            self.designview()

    def calculatenetwork(self):
        if self.nounsavededits():
            self.callFPI('/calculateAndLock')
            self.designview()

    def showbillofmaterial(self):
        output = subprocess.call([unicode(self.workspacedir)+u'/output/FPI - BoM.xlsx'], shell=True)

    def lockUnlockElements(self):
        layer = self.iface.mapCanvas().currentLayer()
        if layer == None:
            infoString = "No layer selected... \nSelect a layer from the layer list."
            QMessageBox.warning(self.iface.mainWindow(), "Info", infoString, QMessageBox.Ok, QMessageBox.Ok)
            return

        # Get the "LOCKED" attribute index
        locked_index = layer.dataProvider().fieldNameIndex("LOCKED")
        if locked_index == -1:
            infoString = "Locking not possible on selected layer. \nLOCKED attribute missing."
            QMessageBox.warning(self.iface.mainWindow(), "Warning", infoString, QMessageBox.Ok, QMessageBox.Ok)
            return

        # number of features
        nF = layer.selectedFeatureCount()
        if nF == 0:
            # Just select all features in the layer rect
            infoString = "No elements selected in current <b>" + layer.name() + "</b> layer. \nLock/unlock all elements?"
            ret = QMessageBox.warning(self.iface.mainWindow(), "Info", infoString, QMessageBox.Ok, QMessageBox.Cancel)
            if (ret == QMessageBox.Cancel):
                return
            layer.invertSelection()

        if not layer.isEditable():
            layer.startEditing()

        trueValue = "T"
        falseValue = "F"

        mixedLockUnlock = False
        lockedSeen = False
        unlockedSeen = False

        selectedFeats = layer.selectedFeatures()
        for feat in selectedFeats:
            if feat["LOCKED"] == "F":
                unlockedSeen = True
                newValue = trueValue
            else:
                lockedSeen = True
                newValue = falseValue

        if lockedSeen and unlockedSeen:
            infoString = "Both locked and unlocked elements selected. \nEverything will be locked."
            QMessageBox.information(self.iface.mainWindow(), "Warning", infoString)
            newValue = trueValue

        # Change the attributes of the selected features
        attr = { locked_index : newValue }
        for feat in selectedFeats:
            layer.dataProvider().changeAttributeValues({ feat.id() : attr })

        layer.removeSelection()
        return
