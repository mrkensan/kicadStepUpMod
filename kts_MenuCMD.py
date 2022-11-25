# -*- coding: utf-8 -*-
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

#import FreeCADGui
from kts_ModState import *


class ktsPcbImportOutline(KtsState):
    """Pull outlines from KiCAD PCB layer into Sketch object"""
    WbGlobal = None     # Reference to our "global" state for this workbook
    check_count = 0

    def __init__(self, WbState):
        self.WbGlobal = WbState
 
    def GetResources(self):     # Resources icon for this tool (Icon, menu text, tool tip, etc...)
        from kts_Locator import kts_mod_path_to_icon
        return {'Pixmap'  : kts_mod_path_to_icon('PCB_ImportOutline.svg'),
                'MenuText': "Create Sketch from PCB Layer",
                'ToolTip' : "Pull KiCAD PCB layer into a Sketch"}
 
    def IsActive(self):
        return True
        #print(">>>>>>>> ktsPcbImportOutline: IsActive Checked [", self.check_count ,"] <<<<<<<<")
        #self.check_count += 1
        #if (self.check_count < 6):
        #    return True     # Command is always active
        #else:
        #    return False

    def Activated(self):
        import kicadStepUptools
        kicadStepUptools.PullPCB()

# END class - ktsPcbImportOutline


class ktsPcbSelect(KtsState):
    """Select PCB File we will use for our operations"""
    WbGlobal = None     # Reference to our "global" state for this workbook

    def __init__(self, WbState):
        self.WbGlobal = WbState
 
    def GetResources(self):
        from kts_Locator import kts_mod_path_to_icon

        return {'Pixmap'   : kts_mod_path_to_icon('PCB_Select.svg'), # Resources icon for this tool
                'MenuText' : "Select PCB File",
                'ToolTip'  : "All operations are performed with this PCB file"}
 
    def IsActive(self):
        # This command is only active if NO PCB file is open
        if (self.WbGlobal.myState('kicad_pcb_filename') == None):
            return True
        else:
            return False

        #print(">>>>>>>> ktsPcbSelect: IsActive Checked <<<<<<<<")
        #filename = ''
        #filename = self.WbGlobal.myState('kicad_pcb_filename')
        #print(">>>>>>>> ktsPcbSelect: IsActive Checked <<<<<<<< '", filename, "'")
        #print("$$$$$$$$ ktsPcbSelect: IsActive State '", self.WbGlobal.delStateItem, "' $$$$$$$$")
        #return True


    def Activated(self):
        import kts_CoreTools
        from kicad_parser import KicadPCB
        from kts_StackUpEdit import kts_make_stack_edit_tab
        from kts_KiCadPCB import KTS_Stackup, KTS_Layers

        # User dialog to select and open a PCB file... Checks file validity, fails gracefully
        if (self.WbGlobal.myState('kicad_pcb_filename') != None):             # If we have an active pcb already...
            kicad_pcb_filename = self.WbGlobal.myState('kicad_pcb_filename')  #   just grab name from global state
            print("We have already read in a PCB!!! >> ", kicad_pcb_filename)
        else:
            self.WbGlobal.delStateItem('kicad_pcb_obj')           
            self.WbGlobal.delStateItem('kts_pcb_layers')           
            self.WbGlobal.delStateItem('kts_pcb_stackup')           
            kicad_pcb_filename = kts_CoreTools.select_pcb_file()    # Otherwise, prompt user to open PCB
            if (kicad_pcb_filename != None):
                self.WbGlobal.myState('kicad_pcb_filename', kicad_pcb_filename)
            else:
                print("No PCB File Selected. Cancelling...")
                return None

        # Parse/grab KiCAD PCB S-Exp Data structure  
        if (self.WbGlobal.myState('kicad_pcb_obj') != None):        # If we have an active pcb already...
            kicad_pcb_obj = self.WbGlobal.myState('kicad_pcb_obj')  #   just grab is from global state
            print("We have already parsed the PCB!!!")
        else:
            self.WbGlobal.delStateItem('kts_pcb_layers')           
            self.WbGlobal.delStateItem('kts_pcb_stackup')
            kicad_pcb_obj = KicadPCB.load(kicad_pcb_filename)
            if (kicad_pcb_obj != None):
                self.WbGlobal.myState('kicad_pcb_obj', kicad_pcb_obj)
            else:
                print("PCB File is Damaged. Cancelling...")
                return None
        
        # Parse the loaded PCB into KTS_Stackup & KTS_Layers
        if ( (self.WbGlobal.myState('kts_pcb_layers') != None) and
             (self.WbGlobal.myState('kts_pcb_stackup') != None) ):      # If we have already built a stackup...
            kts_pcb_layers = self.WbGlobal.myState('kts_pcb_layers')    # grab it!
            kts_pcb_stackup = self.WbGlobal.myState('kts_pcb_stackup')  # grab it!
            print("We have a Stackup!!!")
        else:
            kts_pcb_layers = KTS_Layers.load_layers(kicad_pcb_obj)    # Otherwise, make it from the selected file
            kts_pcb_stackup = KTS_Stackup.load_PCB(kicad_pcb_obj)

            if ( (kts_pcb_layers != None) and (kts_pcb_stackup != None) ):
                self.WbGlobal.myState('kts_pcb_layers', kts_pcb_layers)
                self.WbGlobal.myState('kts_pcb_stackup', kts_pcb_stackup)
            else:
                print ("PCB Stackup Creation Failed")
                return None
        
        # Create new Combo View tab for Stackup Editor
        if (self.WbGlobal.myState('kts_stackup_edit_tab') != None):
            our_new_tab, tab_index = self.WbGlobal.myState('kts_stackup_edit_tab')
            print ("We already have an open stackup editor tab!")
        else:
            our_new_tab, tab_index = kts_make_stack_edit_tab(kts_pcb_stackup)
            self.WbGlobal.myState('kts_stackup_edit_tab', [our_new_tab, tab_index])

        print("Title of 'our_new_tab' = "+str(our_new_tab.tabText(tab_index)))
        return

# END class - ktsPcbSelect


class ktsPcbForget(KtsState):
    """Forget PCB File and associated objects"""
    WbGlobal = None     # Reference to our "global" state for this workbook

    def __init__(self, WbState):
        self.WbGlobal = WbState
 
    def GetResources(self):
        from kts_Locator import kts_mod_path_to_icon

        return {'Pixmap'   : kts_mod_path_to_icon('PCB_Forget.svg'),
                'MenuText' : "Forget PCB",
                'ToolTip'  : "Forget current PCB and associated items",}
#                'Checkable': True}
 
    def IsActive(self):
        # This command is only active if a PCB file is currently open
        return False if (self.WbGlobal.myState('kicad_pcb_filename') == None) else True

   
    def Activated(self):
        self.WbGlobal.delStateItem('kicad_pcb_filename')           
        self.WbGlobal.delStateItem('kicad_pcb_obj')           
        self.WbGlobal.delStateItem('kts_pcb_layers')           
        self.WbGlobal.delStateItem('kts_pcb_stackup')           
        # Remove kts stackup editor window

        return

# END class - ktsPcbForget
