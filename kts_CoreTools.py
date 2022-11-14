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
__KTS_FILE_NAME__ = "KTS_CORETOOLS"

from kts_PrefsMgmt import prefs_set_file_version
prefs_set_file_version(__KTS_FILE_NAME__, __KTS_FILE_VER__)

from kts_utils import *     # Helper utility functions

def select_pcb_file():
    from kts_PrefsMgmt import prefs_get
    import os
    import PySide
    from fcad_parser import KicadPCB
    import inspect
    from collections import OrderedDict
    from kts_StackUpEdit import KTS_Layers

    
    this_func_name = inspect.currentframe().f_code.co_name

    prefs = prefs_get()

    # Start at the folder of the last opened PCB, or home dir.
    pcb_start_folder = prefs.GetString('pcb_prev_folder')
    if not os.path.isdir(make_unicode(pcb_start_folder)):
        pcb_start_folder = os.path.expanduser("~")
    say("Starting Folder = "+pcb_start_folder)

    pcb_selected_file, Filter = PySide.QtGui.QFileDialog.getOpenFileName(None, "Open KiCAD PCB File...", make_unicode(pcb_start_folder), "*.kicad_pcb")

    # Check for Valid Filename
    if len(pcb_selected_file) > 0:
        if os.path.isfile(pcb_selected_file):
            pcb_file = os.path.basename(pcb_selected_file)
            say('opening: '+pcb_file)
            pcb_folder = os.path.dirname(pcb_selected_file)
            say('from folder: '+pcb_folder)
            #default_prefix3d = re.sub("\\\\", "/", default_prefix3d)

            prefs.SetString('pcb_prev_folder', pcb_folder)
            prefs.SetString('pcb_prev_file', pcb_file)
        else:
            say('Not a File: '+pcb_selected_file)
    else:
        say('Cancelled')

    say(this_func_name)
    say_inline("\nReading PCB...")
    kicad_pcb = KicadPCB.load(pcb_selected_file)
    if hasattr(kicad_pcb, 'version'):
        say(" KiCAD Version = "+str(kicad_pcb.version))
    if hasattr(kicad_pcb, 'setup'):
        say("Found setup... Copper Finish is: "+kicad_pcb.setup.stackup.copper_finish)

    KTS_Layers.init(kicad_pcb)

    return

