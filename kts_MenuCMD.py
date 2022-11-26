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

from kts_ModState import KtsState


class ktsRefreshToolbar():
    """Null command which causes all Toolbar Icons' IsActive() to be re-evaluated"""

    def GetResources(self):
        return {}
 
    def IsActive(self):
        print("%%%%%%%%%%%%%% ktsRefreshToolbar Checking IsActive()")
        return True

    def Activated(self):
        pass
# END class - ktsRefreshToolbar


class ktsPcbOutlineDraw(KtsState):
    """Draws outlines from KiCAD PCB layer into Sketch object"""
    KtsState = None     # Reference to our "global" state for this workbook
    check_count = 0

    def __init__(self, WbState):
        self.KtsState = WbState
 
    def GetResources(self):     # Resources icon for this tool (Icon, menu text, tool tip, etc...)
        from kts_Locator import kts_mod_path_to_icon
        return {'Pixmap'  : kts_mod_path_to_icon('PCB_ImportOutline.svg'),
                'MenuText': "Create Outline Sketch",
                'ToolTip' : "Create layer outline sketch from KiCAD PCB layer drawing"}
 
    def IsActive(self):
        # This command is only active if a PCB file is currently open
        print("%%%%%%%%%%%%%% ktsPcbOutlineDraw Checking IsActive()")
        return (self.KtsState.pcb_is_loaded())

    def Activated(self):
        import kicadStepUptools
        kicadStepUptools.PullPCB()
# END class - ktsPcbOutlineDraw


class ktsPcbStackEdit(KtsState):
    """Stackup Editor. Assigns outline drawings to Stackup-layers."""
    KtsState = None     # Reference to our "global" state for this workbook
    check_count = 0

    def __init__(self, WbState):
        self.KtsState = WbState
 
    def GetResources(self):     # Resources icon for this tool (Icon, menu text, tool tip, etc...)
        from kts_Locator import kts_mod_path_to_icon
        return {'Pixmap'  : kts_mod_path_to_icon('PCB_Stack.svg'),
                'MenuText': "Stackup Editor",
                'ToolTip' : "Assign outline drawings to Stackup-layers"}
 
    def IsActive(self):
        print("%%%%%%%%%%%%%% ktsPcbStackEdit Checking IsActive()")

        return ((self.KtsState.pcb_is_loaded()) and 
                (not self.KtsState.stack_editor_is_active()))

    def Activated(self):
        from kts_StackUpEdit import kts_make_stack_edit_tab, kts_get_stack_edit_tab

        # Create new Combo View tab for Stackup Editor, if we don't already have one
        UserPCB = self.KtsState.myState('KTS_Active_PCB')

        if (not self.KtsState.stack_editor_is_active()):
            (combo_view_obj, tab_index) = kts_make_stack_edit_tab(UserPCB.StackupGet())
        else:
            (combo_view_obj, tab_index) = kts_get_stack_edit_tab(UserPCB.StackupGet())

        if (combo_view_obj != None):
            #print("Title of 'stack_edit_tab' = "+str(combo_view_obj.tabText(tab_index)))
            combo_view_obj.setCurrentIndex(tab_index)   # Bring our tab to Front in Combo-View
        else:
            print("Unable to open Stack Editor Tab in Combo View")

        return
# END class - ktsPcbStackEdit


class ktsPcbSelect(KtsState):
    """Select PCB File we will use for our operations"""
    KtsState = None     # Reference to our "global" state for this Workbench

    def __init__(self, WbState):
        self.KtsState = WbState
 
    def GetResources(self):
        from kts_Locator import kts_mod_path_to_icon

        return {'Pixmap'   : kts_mod_path_to_icon('PCB_Select.svg'), # Resources icon for this tool
                'MenuText' : "Select PCB File",
                'ToolTip'  : "All operations are performed with this PCB file"}
 
    def IsActive(self):
        # This command is only active if NO PCB file is open
        print("%%%%%%%%%%%%%% ktsPcbSelect Checking IsActive()")

        return (not self.KtsState.pcb_is_loaded())

    def Activated(self):
        import kts_CoreTools
        from kts_PcbManager import KTS_PcbMgr

        if (self.KtsState.pcb_is_loaded()):
            print("We have already read in a PCB!!!")
            return None

        # User dialog to select and open a PCB file... 
        #   Checks file validity, fails gracefully
        kicad_pcb_filename = kts_CoreTools.select_pcb_file()
        if (kicad_pcb_filename == None):
            print("No PCB File Selected. Cancelling...")
            return None

        # Parse the PCB file
        UserPCB = KTS_PcbMgr()
        UserPCB.BoardLoad(kicad_pcb_filename)
        pcb_name = UserPCB.FilenameGet()

        if (self.KtsState.pcb_is_loaded()):
            print (">>>>>>>> ktsPcbSelect: BoardLoad Success <<<<<<<< '", pcb_name[0], "'")
            #print ("   Our PCB Object: ", UserPCB)
            #print ("Stored PCB Object: ", self.KtsState.myState('KTS_Active_PCB'))
            #import sys
            #print ("PCB Object RefCnt: ", sys.getrefcount(self.KtsState.myState('KTS_Active_PCB')))
        else:
            print("!!!!!!!! ktsPcbSelect: BoardLoad FAIL !!!!!!!! '", kicad_pcb_filename, "'")
        return
# END class - ktsPcbSelect


class ktsPcbForget(KtsState):
    """Forget PCB File and associated objects"""
    KtsState = None     # Reference to our "global" state for this workbook

    def __init__(self, WbState):
        self.KtsState = WbState
 
    def GetResources(self):
        from kts_Locator import kts_mod_path_to_icon

        return {'Pixmap'   : kts_mod_path_to_icon('PCB_Forget.svg'),
                'MenuText' : "Forget PCB",
                'ToolTip'  : "Forget current PCB and associated items",}
#                'Checkable': True}
 
    def IsActive(self):
        # This command is only active if a PCB file is currently open
        print("%%%%%%%%%%%%%% ktsPcbForget Checking IsActive()")

        return (self.KtsState.pcb_is_loaded())
   
    def Activated(self):
        from kts_StackUpEdit import kts_stack_edit_tab_remove

        UserPCB = self.KtsState.myState('KTS_Active_PCB')
        pcb_name = UserPCB.FilenameGet()

        print(">>>>>>>> ktsPcbForget: ", pcb_name[0], " <<<<<<<<")
        #print ("   Our PCB Object: ", UserPCB)
        #import sys
        #print ("PCB Object RefCnt (before): ", sys.getrefcount(UserPCB))
        UserPCB.BoardForget()
        #print ("PCB Object RefCnt (after): ", sys.getrefcount(UserPCB))

        # Remove kts stackup editor window (if present)
        kts_stack_edit_tab_remove()

        return
# END class - ktsPcbForget
