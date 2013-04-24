# -*- coding: utf-8 -*-
"""
/***************************************************************************
 FiberPlanITDesigner
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
 This script initializes the plugin, making it known to QGIS.
"""


def name():
    return "FiberPlanIT Designer"


def description():
    return "FiberPlanIT QGis Plugin"


def version():
    return "Version 1.2.1"


def icon():
    return "icon.png"


def qgisMinimumVersion():
    return "1.8"

def author():
    return "Comsof"

def email():
    return "luc.deheyn@comsof.com"

def classFactory(iface):
    # load FiberPlanITDesigner class from file FiberPlanITDesigner
    from fiberplanitdesigner import FiberPlanITDesigner
    return FiberPlanITDesigner(iface)
