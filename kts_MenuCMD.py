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

__KTS_FILE_VER__  = "1.0.0"
__KTS_FILE_NAME__ = "KTS_MENUCMD"

from kts_PrefsMgmt import prefs_set_file_version
prefs_set_file_version(__KTS_FILE_NAME__, __KTS_FILE_VER__)

import FreeCADGui

class ktsPcbImportOutline:
    "Pull outlines from KiCAD PCB layer into Sketch object"
 
    def GetResources(self):
        from kts_locator import kts_mod_path_to_icon

        return {'Pixmap'  : kts_mod_path_to_icon('PCB_ImportOutline.svg') , # Resources icon for this tool
                'MenuText': "Create Sketch from PCB Layer" ,
                'ToolTip' : "Pull KiCAD PCB layer into a Sketch"}
 
    def IsActive(self):
        return True     # Command is always active
 
    def Activated(self):
        import kicadStepUptools
        kicadStepUptools.PullPCB()

FreeCADGui.addCommand('ktsPcbImportOutline',ktsPcbImportOutline())
# END Command - ktsPcbImportOutline


class ktsPcbSelect:
    "Select PCB File we will use for our operations"
 
    def GetResources(self):
        from kts_locator import kts_mod_path_to_icon

        return {'Pixmap'  : kts_mod_path_to_icon('PCB_Select.svg') , # Resources icon for this tool
                'MenuText': "Select PCB File" ,
                'ToolTip' : "All operations are performed with this PCB file"}
 
    def IsActive(self):
        return True     # Command is always active
 
    def Activated(self):
        import kts_CoreTools
        from kts_StackUpEdit import kts_make_stack_edit_tab, KTS_Stackup

        # User dialog to select and open a PCB file
        # Parses the file into internal data structures
        kts_CoreTools.select_pcb_file()
        stackup = KTS_Stackup.get()

        # Create new Combo View tab for Stackup Editor
        our_new_tab, tab_index = kts_make_stack_edit_tab(stackup)
        print("Title of 'our_new_tab' = "+str(our_new_tab.tabText(tab_index)))

FreeCADGui.addCommand('ktsPcbSelect',ktsPcbSelect())
# END Command - ktsPcbSelect