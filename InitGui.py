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
__KTS_FILE_NAME__ = "INITGUI"

from kts_PrefsMgmt import prefs_set_file_version
prefs_set_file_version(__KTS_FILE_NAME__, __KTS_FILE_VER__)

global myurlKWB
myurlKWB='https://github.com/mrkensan/kicadStepUpModXXX'

#!# from kts_versions import *
#!# import os

import FreeCADGui

from kicadStepUpCMD import *
from kts_MenuCMD import *  


#!# import ksu_locator, os

#ksuWBpath = os.path.dirname(ksu_locator.__file__)
#!# ksuWB_ui_path = kts_mod_ui_path()         # QT files for Settings panels

# FreeCADGui.addLanguagePath(ksuWBpath+"/translations")

#!# global main_ksu_Icon
#!# main_ksu_Icon = os.path.join( kts_mod_icons_path() , 'kicad-StepUp-tools-WB.svg')
#main_ksu_Icon = kts_mod_path_to_icon('kicad-StepUp-tools-WB.svg')
#!# print(main_ksu_Icon + '\n')
#!# icon_path = "nothing"
#!# icon_path = kts_mod_path_to_icon('kicad-StepUp-tools-WB.svg')
#!# print(icon_path + '\n')
#!# print('(InitGui call this file name)' + kts_this_file_name())


class KiCadStepUpWB ( FreeCADGui.Workbench ):      # 'Workbench' defined in FreeCADGui
    from kts_locator import kts_mod_path_to_icon
    #!# global myurlKWB, mycommitsKWB, verKSU
    global kSU_MainPrefPage     # Must be declared 'global' for FreeCAD to access
    
    "KiCadStepUp WB object"
    Icon = kts_mod_path_to_icon('kicad-StepUp-tools-WB.svg')
    MenuText = "KiCAD to STEP"
    ToolTip = "KiCAD to STEP Workbench"
 
    def GetClassName(self):
        return "Gui::PythonWorkbench"


    def Initialize(self):
        import FreeCADGui
        from kts_locator import kts_mod_ui_path, kts_mod_icons_path

        # Adding KSU Icons to Toolbar
        self.appendToolbar("ksu Tools", ["ksuToolsEditPrefs","ksuToolsOpenBoard",\
                           "ksuToolsExportModel","ksuToolsAddTracks","ksuToolsAddSilks",\
                           "ksuToolsImport3DStep","ksuToolsExport3DStep", "ksuToolsPullPCB"])

        # Adding KTS Icons to Toolbar
        self.appendToolbar("New Tools", ["Separator", "ktsPcbSelect", "ktsPcbImportOutline"])

        # Creating a menu for the Workbench
        self.appendMenu("ksu Tools", ["ksuToolsEditPrefs"])

        # Main Workbench Prefs UI Page(s)
        FreeCADGui.addPreferencePage(kts_mod_ui_path() + '/ksu_prefs.ui', 'kicadStepUpGui')
        # Help Page for Workbench (as a prefs page)
        FreeCADGui.addPreferencePage(kSU_MainPrefPage, "kicadStepUpGui")

        # Path to the Icons for this Workbench
        FreeCADGui.addIconPath(kts_mod_icons_path())
        Log ("Loading KiCAD to STEP... done\n")


    def Activated(self):
        from kts_PrefsMgmt import prefs_get_file_version
        from kts_StackUpEdit import kts_make_stack_edit_tab

        # Create new Combo View tab for Stackup Editor
        our_new_tab, tab_index = kts_make_stack_edit_tab()
        print("Title of 'our_new_tab' = "+str(our_new_tab.tabText(tab_index)))

        Msg ("KiCAD to STEP Workbench is Activated ("+ prefs_get_file_version("KTS_WORKBENCH") +")\n")
        
 
    def Deactivated(self):
                # do something here if needed...
        Msg ("KiCadStepUpWB Deactivated\n")

# END - class KiCadStepUpWB()


class kSU_MainPrefPage:

    def __init__(self):
        from PySide import QtGui, QtCore

        self.form = QtGui.QWidget()
        self.form.setWindowTitle("kSU \'Help Tips\'")
        self.form.verticalLayoutWidget = QtGui.QWidget(self.form)
        self.form.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 530, 650)) #top corner, width, height
        self.form.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.form.verticalLayout = QtGui.QVBoxLayout(self.form.verticalLayoutWidget)
        self.form.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.form.verticalLayout.setObjectName("verticalLayout")

        self.form.textEdit = QtGui.QTextBrowser(self.form.verticalLayoutWidget)
        self.form.textEdit.setGeometry(QtCore.QRect(00, 10, 530, 640)) #top corner, width, height
        self.form.textEdit.setOpenExternalLinks(True)
        self.form.textEdit.setObjectName("textEdit")
        self.form.textEdit.setText(self.make_help_panel())

        print ("(InitGui) Created kSU 'Help Tips' Pref panel")


    def make_help_panel(self):
        # Create the "help" panel in preferences
        import os
        from kts_locator import kts_mod_path
        from kts_PrefsMgmt import prefs_get_file_version

        kts_version = prefs_get_file_version("KTS_WORKBENCH")

        pdf_name='kicadStepUp-starter-Guide.pdf'

        header_txt="""<font color=GoldenRod><b>kicad StepUp version """+kts_version+"""</font></b><br>"""

        help_txt="""<font color=black>"""
        help_txt+="""<b>Kicad StepUp</b> is a tool set to easily <b>collaborate between kicad pcb EDA</b> (board and 3D parts) as STEP models <b>and FreeCAD MCAD</b> modeler.<br>"""
        help_txt+="""</font>"""
        help_txt+="<font color=black>"
        help_txt+="<b>StepUp</b> can also be used <b>to align 3D model to kicad footprint</b>.<br>"
        help_txt+="The artwork can be used for MCAD interchange and collaboration, and for enclosure design.<br>"
        help_txt+="The 3D visualization of components on board assemblies in kicad 3dviewer, will be the same in your mechanical software, "
        help_txt+="because of the STEP interchange format.<br>"
        help_txt+="It is also possible to <b>Update a pcb Edge from a FC Sketcher.</b><br>"
        help_txt+="<b>configuration options:</b><br>Configuration options are located in the preferences system of FreeCAD, which is located in the Edit menu -&gt; Preferences.<br>"
        help_txt+="starter Guide:<br><a href='"+kts_mod_path()+os.sep+"demo"+os.sep+pdf_name+"' target='_blank'>"+pdf_name+"</a><br>"
        help_txt+="<b>Note:</b> each button has its own <b>Tooltip</b><br>"
        help_txt+="useful buttons:<br><b>Load kicad Board directly</b> -> will load kicad board and parts in FreeCAD coming from kicad '.kicad_pcb' file<br>"
        help_txt+="<b>Load kicad Footprint module</b> -> will load directly kicad footprint in FreeCAD to easily align the 3D model to footprint<br>"
        help_txt+="<b>Export to kicad STEP & scaled VRML</b> -> will convert MCAD model to STEP and VRML to be used by Kicad and kicad StepUp<br>"
        help_txt+="<b>   -> VRML can be multipart;<br>   -> STEP must be single part</b><br>(<i>'Part Boolean Union'</i> or <i>'Part Makecompound'</i>)<br>"
        help_txt+="<i>assign material to selected colors and your VRML 3D models will have nice shiny effects</i><br>"
        help_txt+="<b>Push pcb Sketch to kicad_pcb Edge</b> -> will push pcb Sketch to kicad_pcb Edge in your design; it can be done with an empty or with an existing pcb Edge<br>"
        help_txt+="<br>for a more detailed help have a look at <br><b>kicadStepUp-starter-Guide.pdf</b><br>"
        help_txt+="or just follow the <b>YouTube video tutorials</b> <br><a href='https://youtu.be/h6wMU3lE_sA'  target='_blank'>kicadStepUp basics</a><br>"
        help_txt+="<a href='https://youtu.be/O6vr8QFnYGw' target='_blank'>kicadStepUp STEP alignment to Kicad footprint</a><br>"
        help_txt+="<a href='https://github.com/easyw/kicadStepUpMod' target='_blank'>check always the latest release of kicadStepUp</a><br><br>"
        help_txt+="Designing in kicad native 3d-viewer will produce a fully aligned STEP MCAD version "
        help_txt+="with the same view of kicad 3d render.<br>"
        help_txt+="Moreover, KiCad StepUp tool set <b>will let you to load the kicad footprint inside FreeCAD and align the 3D part with a visual real time feedback "
        help_txt+="of the 3d model and footprint reciprocal position.</b><br>"
        help_txt+="With this tool is possible to download a part from on-line libraries, align the model to kicad footprint "
        help_txt+="and export the model to wrl, for immediate 3d-viewer alignment in pcbnew.<br>"
        help_txt+="Now the two words are connected for a better collaboration; just <b>design in kicad EDA</b> and transfer "
        help_txt+="the artwork to <b>MCAD (FreeCAD)</b> smoothly.<br>"
        help_txt+="<b>The workflow is very simple</b> and maintains the usual way to work with kicad:<br>"
        help_txt+="Add models to your library creating 3D models in FreeCAD, or getting models from online libs "
        help_txt+="or from the parametric 3D lib expressly done to kicad <a href='https://github.com/easyw/kicad-3d-models-in-freecad' target='_blank'>kicadStepUp 3D STEP models generator</a><br>"
        help_txt+="Once you have your 3D MCAD model, <b>you need to have a copy of that in STEP and VRML format.</b> <br>"
        help_txt+="(with the latest kicad release you can only have STEP model, VRML is not needed anymore, but <b>it is possible"
        help_txt+=" to mix VRML, STEP and IGES format</b>)<br>"        
        help_txt+="Just exporting the model with FreeCAD and put your model in the same folder in which "
        help_txt+="normally you are used to put vrml models; the script will assembly the MCAD board and models as in 3d-viewer of kicad."       
        help_txt+="<br><b>NB<br>STEP model has to be fused in single object</b><br>(Part Boolean Union of objects)"
        help_txt+="<br><b>or a Compoud</b> (Part Makecompound of objects)</b>"
        help_txt+="<hr><b>enable 'Report view' Panel to see helping messages</b>"
        help_txt+="</font><br>"

        return (header_txt + help_txt)

# END - class kSU_MainPrefPage


# Add Workbench to FreeCAD UI so User can activate/use it
FreeCADGui.addWorkbench(KiCadStepUpWB)

