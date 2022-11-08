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

__KTS_WORKBENCH_VER__  = '11.11.11'
__KTS_WORKBENCH_NAME__ = "KTS_WORKBENCH"

import time
import FreeCAD
from kts_PrefsMgmt import prefs_set_file_version

#from kts_PrefsMgmt import prefs_init

with open('/Users/user/AppData/Roaming/FreeCAD/Mod/KiCad_StepUp/junk.txt', 'w') as f:
    f.write("Starting KiCAD to STEP\n")
    init_start_time = int(round(time.time() * 1000))

    FreeCAD.addImportType("Kicad pcb board/mod File Type (*.kicad_pcb *.kicad_mod)","kicadStepUptools") 
    FreeCAD.addImportType("zip of STEP/FCStd File Type (*.zip)","ZipStepImport")
    prefs_set_file_version(__KTS_WORKBENCH_NAME__, __KTS_WORKBENCH_VER__)

    init_end_time = int(round(time.time() * 1000))
    f.write("\nInit took " + str(init_end_time - init_start_time)  + "ms\n")
