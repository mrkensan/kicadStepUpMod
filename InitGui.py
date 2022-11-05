# -*- coding: utf-8 -*-
#****************************************************************************
#*                                                                          *
#*  Kicad STEPUP (TM) (3D kicad board and models to STEP) for FreeCAD       *
#*  3D exporter for FreeCAD                                                 *
#*  Kicad STEPUP TOOLS (TM) (3D kicad board and models to STEP) for FreeCAD *
#*  Copyright (c) 2015                                                      *
#*  Maurice easyw@katamail.com                                              *
#*                                                                          *
#*  Kicad STEPUP (TM) is a TradeMark and cannot be freely usable            *
#*                                                                          *
#****************************************************************************
#*                                                                          *
#*   This program is free software; you can redistribute it and/or modify   *
#*   it under the terms of the GNU Affero General Public License            *
#*   as published by the Free Software Foundation to ensure cooperation     *
#*   with the community in the case of network server software;             *
#*   for detail see the LICENCE text file.                                  *
#*   http://www.gnu.org/licenses/agpl-3.0.en.html                           *
#*   Moreover you have to include the original author copyright             *
#*   kicad StepUP made by Maurice easyw@katamail.com                        *
#*                                                                          *
#*   This program is distributed in the hope that it will be useful,        *
#*   but WITHOUT ANY WARRANTY; without even the implied warranty of         *
#*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          *
#*   GNU Library General Public License for more details.                   *
#*                                                                          *
#*   You should have received a copy of the GNU Library General Public      *
#*   License along with this program; if not, write to the Free Software    *
#*   Foundation, Inc.,                                                      *
#*   51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA           *
#*                                                                          *
#****************************************************************************
#*                                                                          *
#*  KiCAD_2STEP - Render KiCAD PCB Models as STEP (No Round Trip, etc...)   *
#*                                                                          *
#*   This FreeCAD workbench is derived from the work of the Kicad STEPUP    *
#*   team including Maurice easyw@katamail.com and numerous others.         *
#*                                                                          *
#*   The purpose of this workbench is to provide a single-function tool     *
#*   for converting KiCAD PCBs to useful STEP models for use in non-FreeCAD *
#*   MCAD packages. Our intent is to add a few enhancements to the original *
#*   while keeping the core functionality similar.                          *
#*                                                                          *
#*   Because our use-case does not require manipulation in FreeCAD of the   *
#*   PCB nor round-tipping of MCAD-ECAD data, we have simplified that part  *
#*   of the workbench core-code and UI.                                     *
#*                                                                          *
#*   We hope that this workbench is useful to the community!                *
#*                                                                          *
#****************************************************************************

global myurlKWB, ksuWBpath
myurlKWB='https://github.com/mrkensan/kicadStepUpModXXX'

from kts_versions import verKSU, mycommitsKWB

import FreeCADGui, os

import ksu_locator
from kicadStepUpCMD import *

ksuWBpath = os.path.dirname(ksu_locator.__file__)
#sys.path.append(ksuWB + '/Gui')
ksuWB_icons_path =  os.path.join( ksuWBpath, 'Resources', 'icons')
ksuWB_ui_path = os.path.join( ksuWBpath, 'Resources','ui' )

# FreeCADGui.addLanguagePath(ksuWBpath+"/translations")

global main_ksu_Icon
main_ksu_Icon = os.path.join( ksuWB_icons_path , 'kicad-StepUp-tools-WB.svg')

#!# from PySide import QtGui

import hlp
header_txt="""<font color=GoldenRod><b>kicad StepUp version """+verKSU+"""</font></b><br>"""
help_t = header_txt+hlp.help_txt


from kts_PrefsMgmt import kSU_MainPrefPage, check_prefs


class KiCadStepUpWB ( Workbench ):

    global main_ksu_Icon, myurlKWB, mycommitsKWB, verKSU
    global ksuWB_ui_path, kSU_MainPrefPage, ksuWB_icons_path
    
    "KiCadStepUp WB object"
    Icon = main_ksu_Icon
    #Icon = ":Resources/icons/kicad-StepUp-tools-WB.svg"
    MenuText = "KiCadStepUp"
    ToolTip = "KiCadStepUp workbench"
 
    def GetClassName(self):
        return "Gui::PythonWorkbench"
    
    def Initialize(self):
        import kicadStepUpCMD, sys
        global pref_page
        pref_page = True # False #True #
        import FreeCADGui


        self.appendToolbar("ksu Tools", ["ksuToolsEditPrefs","ksuToolsOpenBoard",\
                           "ksuToolsExportModel","ksuToolsAddTracks","ksuToolsAddSilks",\
                           "ksuToolsImport3DStep","ksuToolsExport3DStep", "ksuToolsPullPCB"])

        self.appendMenu("ksu Tools", ["ksuToolsEditPrefs"])

        if pref_page:
            FreeCADGui.addPreferencePage(
                ksuWB_ui_path + '/ksu_prefs.ui',
                'kicadStepUpGui'
                )
            FreeCADGui.addPreferencePage(kSU_MainPrefPage,"kicadStepUpGui")

        FreeCADGui.addIconPath(ksuWB_icons_path)
        Log ("Loading ksuModule... done\n")
 
    def Activated(self):
                # do something here if needed...

        from kts_PrefsMgmt import check_prefs
        from kts_versions import KTS_WORKBENCH_VER

        Msg ("KiCAD to STEP Workbench is Activated("+KTS_WORKBENCH_VER+")\n")
        
        prefs = check_prefs()

 
    def Deactivated(self):
                # do something here if needed...
        Msg ("KiCadStepUpWB.Deactivated()\n")
        
FreeCADGui.addWorkbench(KiCadStepUpWB)

