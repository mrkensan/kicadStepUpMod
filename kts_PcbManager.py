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

#****************************************************************************
#*                                                                          *
#*  Enhanced Schema for describing PCB Layer Stackup                        *
#*                                                                          *
#*    KiCAD v6.xx has a fairly fixed view of what a PCB stackup consists.   *
#*    In order to represent the "Rigid-Flex" use case, we need to expand    *
#*    this view. We'll do this by incorporating the info saved in the PCB   *
#*    with info also stored in the kicad_prl file. This file has an area    *
#*    to be used for "user variables". Here we'll add our own records to    *
#*    define and augment the additional items required to specify the full  *
#*    rigid-flex stackup.                                                   *
#*                                                                          *
#*    In order for this to work, we need an internal representation which   *
#*    knows where the info comes from (so we can update it) and combines    *
#*    the two data sources to tell us how to render the 3D PCB model here.  *
#*    Perhaps once we accomplish this, we can even consider ways to export  *
#*    appropriate specifications on layers for manufacturing purposes.      *
#*    (i.e. automatic creation of stackup documentation layer for gerbers)  *
#*                                                                          *
#*  Schema (dataclass)                                                      *
#*    KTS_StackUp - Definition of actual PCBA Stackup                       *
#*      layer_posn: int (top=1, etc...) # this is just be list order        *
#*      layer_data: PCB file drawing num contianing layer "content"         *
#*      layer_outline: PCB file drawing num contianing layer outlines       *
#*      layer_type: from kts_LayerTypes enum {Silk, Adhes, SolMask, etc.}   *
#*      layer_thk:  Finished thickness of layer in microns (um)             *
#*      layer_matl: material type of layer (FR4, Polyimide, Prepreg, etc.)  *
#*      layer_region: region of PCB project layer is used on {flex, rigid}  *
#*                                                                          *
#*  Dictionaries                                                            *
#*    KTS_Layers: KTS layer definition & purpose for PCBA                   *
#*                                                                          *
#*  Array (dataclass)                                                       *
#*    kts_dscr:   User-defined name from KTS domain                         *
#*                                                                          *
#*    kts_silk_color:   Color options for Silkscreen                        *
#*    kts_silk_matl:    Material options for Silkscreen                     *
#*                                                                          *
#*  Enums (tuples??)                                                        *
#*    kts_LayerTypes: {Silk, Adhes, SolMask, etc.}                          *
#*                                                                          *
#*    kts_Materials:  {FR4, Polyimide, Prepreg, etc.}                       *
#*      This will probably also have names/types to allow for later         *
#*      generating fab docs... so {{PrePreg, "PrePreg 3080"}, {...}}        *
#*                                                                          *
#*    kts_Regions:    {flex, rigid, stiffner, prepreg, etc.}                *
#*                                                                          *
#****************************************************************************

__KTS_FILE_VER__  = "1.0.0"
__KTS_FILE_NAME__ = "KTS_PCBMANAGER"

from kts_PrefsMgmt import prefs_set_file_version
prefs_set_file_version(__KTS_FILE_NAME__, __KTS_FILE_VER__)

from kts_ModState import *

def unquote(item: str) -> str:
    return (item.replace('"', ''))


#****************************************************************************
#*                                                                          *
#*  KTS_PcbMgr - Manage overall loaded PCB while PCB is "active"            *
#*                                                                          *
#*      Here we hold all state for the loaded PCB and provide methods for   *
#*      initializing, accessing, saving, and destroying the loaded PCB      *
#*      within the Workbench.                                               *
#*                                                                          *
#****************************************************************************

class KTS_PcbMgr:
    """Class representing the open and parsed PCB"""

    def __init__(self, filename: str):
        """Load and parse a KiCAD PCB from a filename.
           Filename must be absolute path to file.
           Returns ref to KTS_PcbMgr on success, None on Fail."""

        self.KiCadPCB = None            # S-Expr Parsed KiCAD PCB dict
        self.KTS_Vars = None            # KTS_vars obj used by this PCB Mgr instance
        self.KTS_Layers = None          # KTS_Layers obj used by this PCB Mgr instance
        self.KTS_Stackup  = None        # Reference to our KTS_Stackup Object
        self.BoardOpenSuccess = False   # Local Flag inidcates we successfully fully parsed PCB
        self.filename = filename        # Our copy of PCB filename

        # Parse KiCAD PCB S-Exp Data structure
        #   Expected that file was previously 
        #   validated as error-free PCB file. 
        from kicad_parser import KicadPCB                   # S-Expr Parser to read-in the PCB file from KiCAD format
        self.KiCadPCB = KicadPCB.load(self.filename)        # Parse S-Expr, return List-of-Lists representation
        if (self.KiCadPCB == None): return None

        self.KTS_Vars = KTS_Vars(self.filename)             # Read KTS-vars from Proj file
        #self.KTS_Vars.project_vars_save(self)                # Save KTS-vars to Proj file

        self.KTS_Layers  = KTS_Layers(self.KiCadPCB)        # Drawing-layers dictionary

        print("The List of Outline Layers is: ", self.KTS_Layers.outline_layers_get())

        # Infer stackup from loaded board
        if ((self.KTS_Vars != None) and (self.KTS_Layers != None)):
           self.KTS_Stackup = KTS_Stackup(self.KiCadPCB, self.KTS_Layers , self.KTS_Vars)

        if  (self.KTS_Stackup == None):  # Not expected if S-Expr parser loads error-free
            KTS_PcbMgr.BoardForget()
            return None
        
        # Board Load was Successful
        self.BoardOpenSuccess = True
        print(">>> Global State Obj Ref: ", KtsGblState)
        KtsGblState.myState("BoardOpenSuccess", True)       # Let the world know this went well
        KtsGblState.myState("KTS_PcbMgr", self)         # Let the world know how to find the PCB
        return

    def BoardForget(self):
        self.BoardOpenSuccess = False
        KtsGblState.delStateItem("BoardOpenSuccess")
        KtsGblState.delStateItem("KTS_PcbMgr")
        return None

    def FilenameGet(self):
        import os
        pcb_file = os.path.basename(self.filename)
        pcb_folder = os.path.dirname(self.filename)
        return (pcb_file, pcb_folder)

    def VarsGet(self):
        return (self.KTS_Vars)

    def LayersGet(self):
        return (self.KTS_Layers)

    def StackupGet(self):
        return (self.KTS_Stackup)
        
# END - class KTS_PcbMgr


#****************************************************************************
#*                                                                          *
#*  KTS_Vars - User-specified parameters for use by KTS                     *
#*                                                                          *
#*    This class implements and provides access to a dictionary of          *
#*    user-specified paramters about the PCB which are particular to the    *
#*    KiCAD-to-STEP workbench. These parameters are stored in so-called     *
#*    'KiCAD User Vars'. In KiCAD these vars are used for various text      *
#*    constants and substitutions to allow paramterization a project.       *
#*    In the context of KiCAD-to-Step, we implement our own vars which are  *
#*    interpreted only by this Workbench, but not used by KiCAD.            *
#*                                                                          *
#*    The parameters augment the standard info inferred from the PCB, as    *
#*    stored by KiCAD in the PCB file, allowing KiCAD-to-STEP to render a   *
#*    solid model of the PCB according to the intentions of the User.       *
#*    Most significantly these paramters help define which PCB areas        *
#*    correspond to "Rigid" vs. "Flex" construction, and which drawing      *
#*    layers define these areas.                                            *
#*                                                                          *
#*    This class is responsible for finding user-paramters stored in the    *
#*    project file (.kicad_pro) associted with the PCB (.kicad_pcb) file.   *
#*    File-path and base-name are considered identical between these files  *
#*    (ie. they are in the same folder) and only the extension differs.     *
#*                                                                          *
#*    The project file is searched for KTS variable definitions. If none    *
#*    are found, default values are used, and these values are added to     *
#*    project file when the User saves the stackup configuration. Params    *
#*    in KTS_Vars are merged into Stackup object as it is constructed.      *
#*                                                                          *
#*    We keep a copy of the entire Project file in memory until we merge    *
#*    our vars into this data, then re-write the Project file when User     *
#*    indicates to save. We do not save any info into the PCB file because  *
#*    the file is constructued not strictly conformant to S-Expr rules, so  *
#*    the S-Expr class would not be able to re-write portions of the file   *
#*    in a manner recognized by KiCAD.                                      *
#*                                                                          *
#****************************************************************************

class KTS_Vars():
    """Create and maintain a dictionary of User-vars stored
       in the selected PCB/Project. File load & save methods.
       Methods to look up vars by name & KiCAD layer Mnemonic."""

    def __init__(self, pcb_filename:str):
        import json

        self.kicad_prj_dict = None  # Read-in JSON->dict() project file
        self.kts_vars_dict  = None  # Local KTS variables

        try:
            proj_filename = pcb_filename.replace('.kicad_pcb', '.kicad_pro')
            prj_file = open(proj_filename, 'r', encoding='utf-8')
            self.kicad_prj_dict = json.load(prj_file)
        except:
            print (">>>>>>>>>>> Project file ", proj_filename, " does not exist. Aborting...")
            self.kicad_prj_dict = None
        else:
            print (">>>>>>>>>>> Loading Vars from: ", proj_filename)
        finally:
            prj_file.close()
            if (self.kicad_prj_dict == None): return None

        self.kts_vars_dict = self.kicad_prj_dict['text_variables']  # Pull the vars section into a dict() for our use

        # KiCAD only allows "strings" to be assigned to the "text variables"
        # Here, we convert the string representation to a dictionary for our use
        # We only do this for our own dict() vars, so the rest are kept in-tact
        for var_name in self.kts_vars_dict.keys():
            if ('KTS_dict_' in var_name):
                print("Dictifying ", var_name)
                self.kts_vars_dict[var_name] = eval(json.loads(self.kts_vars_dict[var_name]))

        if ("KTS_dict_Outlines" not in self.kts_vars_dict):
            self.kts_vars_dict["KTS_dict_Outlines"] = dict()    # Assure our key is there for later

        return


    def project_vars_save(self, pcb: KTS_PcbMgr):
        import json

        proj_filename = pcb.filename.replace('.kicad_pcb', '.kicad_pro')+".new"

        # KiCAD only allows "strings" to be assigned to the "text variables"
        # Here, we convert our dict()s to strings before saving
        # We do this only for our own dict() vars, so the rest are kept in-tact
        vars_texified_dict = self.kts_vars_dict
        for var_name in vars_texified_dict.keys():
            if ('KTS_dict_' in var_name):
                print("Textifying ", var_name)
                vars_texified_dict[var_name] = json.dumps(json.dumps(vars_texified_dict[var_name]))

        del self.kicad_prj_dict['text_variables']       # Delete the read-in version of the vars section
        self.kicad_prj_dict['text_variables'] = vars_texified_dict  # Replace it with our new version

        try:
            prj_file = open(proj_filename, 'w', encoding='utf-8')
            json.dump(self.kicad_prj_dict, prj_file, indent=2)
        except:
            print (">>>>>>>>>>> Project file ", proj_filename, " unable to write. Aborting...")
        finally:
            prj_file.close()

        return 

    # Returns a dict corresponding to one of the stored vars, or an empty dict()
    def var_get(self, var_name: str) -> dict:
        return self.kts_vars_dict.get(var_name, {}) or {}

    # Returns the outline layer_num assigned
    def outline_get(self, stack_layer_id: str) -> str:
        if  ((stack_layer_id != None) and (stack_layer_id != "")):
            print("Finding outline drawing for ", stack_layer_id)
            return (self.kts_vars_dict["KTS_dict_Outlines"].get(stack_layer_id, ""))
        else:
            return ""

    # Sets the outline layer_num for a stackup layer
    def outline_set(self, stack_layer_id: str, outline_id: str) -> str:
        if  ((stack_layer_id != None) and (stack_layer_id != "")
             and (outline_id != None) and (outline_id != "")):
            print("Setting outline drawing for ", stack_layer_id, " to ", outline_id)
            self.kts_vars_dict["KTS_dict_Outlines"][stack_layer_id] = outline_id
        return

    # Moves any changed outline settings into KTS_dict_Outlines 
    # ToDo: Check to be sure this is a stackup object type
    def outline_vars_update(kts_stackup):
        for layer in kts_stackup:
            if (layer.oln_asgn == "USER"):
                pass

        return
# END - class KTS_Vars


#****************************************************************************
#*                                                                          *
#*  KTS_Layers - KTS layer definition & purpose for PCBA                    *
#*                                                                          *
#*    This is a class which implements and provides access to a dictionary  *
#*    allowing for cross-reference between the ACTIVE layers of the loaded  *
#*    KiCAD PCB. Because various facets of the KiCAD to STEP workbench must *
#*    interoperate and reference layers using a number means to identify    *
#*    PCB layers/sheets, this cross-ref gives a single place to accoplish   *
#*    the lookup.                                                           *
#*                                                                          *
#*    All possible "keys" are added to the dictionary:                      *
#*      kicad_num:  Absolute numeric ID of layer from kicad app             *
#*      kicad_enum: Symbolic enum used for each layer                       *
#*      kicad_dscr: User-defined name from KiCAD PCB file                   *
#*                                                                          *
#*    These keys allow us to get to the places we need in the PCB file to   *
#*    extract info used in rendering the PCB here in FreeCAD.               *
#*                                                                          *
#*    The dictionary is "read only" and we don't change any of the data     *
#*    items used to construct the dictionary from the PCB file.             * 
#*                                                                          *
#*    The init() method is called with a S-Expr object containing the PCB   *
#*    file data. The dictionary is constructed from this data, and a single *
#*    method kts_layer_get() is used to look up items. All fields from the  *
#*    "layers" section of the PCB are indexed, so all can be looked up to   *
#*    find their "mate". The only caveat is that all layers must be named   *
#*    uniquely (including user-defined names) within the PCB file.          *
#*    We don't check for collisions, user is expected manage this.          *
#*                                                                          *
#****************************************************************************

class KTS_Layers():
    """Create and maintain a dictionary of the activated layers
       in the selected PCB. Methods to look up layer info by
       either KiCAD layer number or layer Mnemonic."""

    def __init__(self, kicad_pcb):
        self.layer_name_dict = dict()
        self.layer_num_dict  = dict()
        self.outline_list    = []

        # Construct dictionaries from loaded PCB
        if not hasattr(kicad_pcb, 'layers'):
            # ToDo: Make this into an "Alert"
            print("KTS_Layers.init: No Layers found in PCB file." )
            return None
        else:
            print("KTS_Layers.init: Found ", len(kicad_pcb.layers), " drawing layers." )

            for lyr_num in kicad_pcb.layers:
                layer_mnemonic = unquote((kicad_pcb.layers[lyr_num])[0])

                if (len(kicad_pcb.layers[lyr_num]) > 2):
                    layer_given_name = unquote((kicad_pcb.layers[lyr_num])[2])
                else:
                    layer_given_name = layer_mnemonic

                # Add KiCAD mnemonic -> layer_given_name
                # If no given name, will just map to the KiCAD mnemonic
                self.layer_name_dict[layer_mnemonic] = layer_given_name

                # Add layer_given_name -> KiCAD mnemonic
                if (len(kicad_pcb.layers[lyr_num]) > 2):
                    self.layer_name_dict[layer_given_name] = layer_mnemonic

                # Add number -> KiCAD mnemonic
                # Note: lyr_num is type str, despite it looking like a number
                self.layer_name_dict[lyr_num] = layer_mnemonic

                # Add KiCAD mnemonic -> number
                # Note: lyr_num is type str, despite it looking like a number
                self.layer_num_dict[layer_mnemonic] = lyr_num

                # Add KiCAD layer_given_name -> number
                if (len(kicad_pcb.layers[lyr_num]) > 2):
                    self.layer_num_dict[layer_given_name] = lyr_num

            # Build list of drawing-layers for cut-outline assignment by user
            self.outline_list_create()
        return

    # Add layer dict items for Dielectric layers
    def dielectric_add(self, name: str):
        if (not "Dielec_" in name): return

        num = name.replace("Dielec", "D")
        self.layer_name_dict[num] = name    # Add number -> mnemonic
        self.layer_num_dict[name] = num     # Add mnemonic -> number
        return

    # Retrieve the mnemonic or given name of a drawing layer
    def get_name(self, lyr:str) -> str:
        return self.layer_name_dict.get(lyr, "")

    # Retrieve the "number" of a drawing layer
    def get_num(self, lyr:str) -> str:
        return self.layer_num_dict.get(lyr, "")

    # Return list of candidate outline layers
    def outline_layers_get(self):
        return self.outline_list

    # Generate list of candidate outline layers
    def outline_list_create(self):
        self.outline_list = []

        for idx in range(0, 64):
            mnemonic   = self.get_name(str(idx))
            given_name = self.get_name(mnemonic)

            if (""    == mnemonic): continue        # Numbered layer not present
            if ("B."  in mnemonic): continue        # KiCAD 'B.' don't have outlines
            if ("F."  in mnemonic): continue        # KiCAD 'F.' don't have outlines
            if ("cut" in mnemonic.lower()):         # A layer that spec's 'cut' could be an outline
                self.outline_list.append(mnemonic)
                continue
            if ("cut" in mnemonic.lower()):         # A layer that spec's 'cut' could be an outline
                self.outline_list.append(given_name)# in case user renamed "Edge.Cuts"
                continue
            if ("cut" in given_name.lower()):       # A layer that spec's 'cut' could be an outline
                self.outline_list.append(given_name)
                continue
            if ("out" in given_name):               # A layer that spec's 'out' could be an outline
                self.outline_list.append(given_name)
                continue
            if ("user." in mnemonic.lower()):       # A 'user' layer could be an outline
                self.outline_list.append(given_name)
                continue
            if (".Cu" in mnemonic): continue        # Copper layers don't have outlines
        print("The List we made is: ", self.outline_list)
        return

# END - class KTS_Layers


#****************************************************************************
#*                                                                          *
#*  Manage KiCAD to STEP PCB Layer Stackup                                  *
#*                                                                          *
#*    KiCAD v6.xx (and beyond) has the facility to store "User Variables".  *
#*    These are stored in both the PCB file and in the project file. The    *
#*    definitions in the PROJECT file seem to be the controlling def'ns,    *
#*    as the PCB file is updated with any vars which exist in the PROJECT   *
#*    file when 'pcbnew' is started from the project dialog. Updated vars   *
#*    are stored in the PCB file ONLY UPON SAVING and exiting pcbnew.       *
#*                                                                          *
#*        If the PCB file is not saved by the user, the vars are only       *
#*        present in the current running instance of pcbnew! User is not    *
#*        prompted to save the file on exit despite inherited changes to    *
#*        the environment.                                                  *
#*                                                                          *
#*    The project file is updated upon exit from the KiCAD project browser. *
#*                                                                          *
#*    In order to avoid "lost information" we will require that user exits  *
#*    KiCAD before using this tool, since state stored in the active KiCAD  *
#*    instances will overwrite both files on save/exit. As the controlling  *
#*    data source for User Variables is the PROJECT file, we will focus     *
#*    here to store KiCAD to STEP PCB stackup into info the PROJECT file.   *
#*    We use the project file in order to keep our info within native KiCAD *
#*    files and not introduce new files for user to manage. We also do this *
#*    with the hope that eventually these capabilities will be incorporated *
#*    into KiCAD and this entire project becomes obsolete!                  *
#*                                                                          *
#*    The Project file is JSON encoded (vs S-expr of PCB file) so we use    *
#*    the python JSON parser and keep a copy of the project file data as an *
#*    instance element which we can update and save out when we are ready.  *
#*    Initialization of this data should be done concurrently with opening  *
#*    the PCB file. It's probably best to update the file any time we make  *
#*    a change to assure that we don't exit with uncommitted user work.     *
#*    We'll make a backup file of the original project file, so the user    *
#*    revert in the event any of our additions "break" the file.            *
#*                                                                          *
#*    As KiCAD PCBs have some stackup information present in the PCB file,  *
#*    we build our local database from a combination of the native stackup  *
#*    info in the PCB file KiCAD to STEP managed info. if a conflict occurs,*
#*    KiCAD-native stackup parameters are given precident. This is meant to *
#*    minimize unexpected/inconsistent behaviors between the tools.         *
#*                                                                          *
#*    The stackup is mostly defined using stackup info from the PCB file.   *
#*    However, since 'pcbnew' has limited scope in terms of listing layers  *
#*    which might be present for a "rigid-flex" stackup, we augment this    *
#*    data by defining our own "stackup" in the user-var kts_stackup.       *
#*                                                                          *
#*    For this to work out, and have some basic representation in both the  *
#*    KiCAD and KiCAD-to-STEP (KTS) contexts, we define all stackup layers  *
#*    in KiCAD. The material is not relevant in KiCAD for rendering the     *
#*    PCBA in FreeCAD, as this info will be held in the KTS stackup def'n.  *
#*    thickness of the layers are pulled from the KiCAD stackup. This allows*
#*    the user to see the total thickness in KiCAD and also for the KiCAD   *
#*    rendering tools to create a board that "looks right" (except for the  *
#*    rigid-flex regions). KiCAD considers all of these added internal      *
#*    stackup layers to be "dielectric" layers, with no corresponding       *
#*    drawing layer. When KiCAD renders the board, it assumes the layer     *
#*    "Edge.Cuts" defines the boundaries of all of these additional layers. *
#*    KiCAD re-numbers these layers any time a dielectric layer is inserted *
#*    or removed. Hence, it is important to define all stackup layers in    *
#*    KiCAD prior to using this plug-in to associate drawing layers with    *
#*    dielectric layers. Any changes in the dielectric layer layout will    *
#*    render the KTS mapping in accurate and lead to dubious results.       *
#*                                                                          *
#*    ToDo: Try to intelligently deal with PCB-file changes without wiping  *
#*          out the previously defined mappings.                            *
#*                                                                          *
#****************************************************************************

from dataclasses import dataclass
from typing import List

@dataclass
class KTS_StackUpRecord:    # Definition of PCBA Stackup-layer Record
   #position:       # (topmost=0, etc...) # this is just list order (index)
    content:  str   # PCB layer with "content" (tracks, mask, silk, ...) ---------> Exactly from PCB
    outline:  str   # PCB layer ID with region outlines (flex, rigid, ...) -------> Read from KTS vars in Project File
    oln_asgn: str   # Outline is assigned from: DEFAULT, PCB or USER -------------> Read from KTS Vars in Project File
    lyr_type: str   # From kts_LayerTypes enum {Silk, Adhes, SolMask, ...} -------> Mapped by us on PCB Import
    thkness:  float # Finished thickness of layer in millimeters (mm) ------------> Exactly from PCB
    material: str   # Layer material type (FR4, Polyimide, Prepreg, ...) ---------> Mapped by us on PCB Import
    region:   str   # Region-type for this stackup element {flex, rigid, ...} ----> Read from KTS vars in Project File
    rgn_asgn: str   # Region is assigned from PCB or USER ------------------------> Read from KTS vars in Project File
    color:    str   # Color of layers for which color is an option (mask, silk) --> Exactly from PCB
    finish:   str   # Finish for outer copper (gold, nickel, etc..) --------------> Read from PCB, applied to copper only
    lyr_func: str   # Function of the layer in this stackup ----------------------> Inferred from layer material (when possible)
                                                                                  # Read also from KTS vars in Project File
                                                                                  # KTS & PCB versions compared to detect stack changes

from typing import Tuple    # For return type hinting
from kicad_parser import SexpList 

class KTS_Stackup():
    """Pull stackup info from named PCB & Project files
       to construct a stackup picture of the PCBA which
       can be aware of both 'flex' and 'rigid' regions.
       
       Provides access methods for extracting this info
       for use when rendering a 3D model of the PCBA."""

    # Here we need access to three things...
    # 1. The Parsed PCB file
    # 2. The layers dictionaries
    # 3. The imported KTS variables
    #
    # We generate the "stackup" data struct which is used elsewhere

    def __init__(self, kicad_pcb:SexpList, kts_layers:KTS_Layers, kts_vars:KTS_Vars ):
        # Init empty layer list each time we init()
        # so we don't accumulate multiple copies of board
        self.kts_stackup: List[KTS_StackUpRecord] = []
        #ThisPcbMgrObj = None           # Ref to our parent object
        self.KTS_Layers  = kts_layers
        self.KTS_Vars = kts_vars

        # Flags used to refine guesses about layers
        stack_has_flex   = False
        stack_has_rigid  = False
        stack_flex_only  = False
        stack_rigid_only = False
        stack_has_both   = False

        if not hasattr(kicad_pcb.setup, 'stackup'):
            # ToDo: Make this into an "Alert"
            print("KTS_Stackup.init: No Stackup found in PCB file." )
            return None
        else:
            copper_finish = unquote(kicad_pcb.setup.stackup.copper_finish)
            copper_finish = copper_finish if(not 'None' in copper_finish) else 'Bare'

            print("****************************************************")
            print("Stackup Sections:")
            print(*kicad_pcb.setup.stackup['layer'], sep = "\n")
            print("****************************************************")

            # Layers within the S-Exp-parsed PCB file are Lists & Lists-of-Lists.
            # The 'SexpList' class, upon which the parser is based, provides the 
            # mechanism to reference groups using dotted notation to traverse the tree. 

            # Due to the way "sublayers" are expressed in the KiCAD PCB file, 'sublayers' 
            # are not distinctly identified within a set of parens. This becomes relevant
            # in the case of Dielectric layers, which can have an unspecificed number of 
            # sublayers. Within a "layer" there are parameters which specify characteristics
            # of the layer. For sublayers, these parameters are not tightly bound to a
            # specific sublayer. Instead, they are compiled into ordered lists 
            # (by the parser) for each of these named characteristics. 
            # Items are added to the lists in the order encountered in the PCB file. 

            # The upshot is that stackup layers with sublayers present 'List' items where
            # we would normally expect a single name-value pair. We have to parse these
            # stackup-layers differently than the others. We do so by determining how many
            # sublayers there are (by examining items on the layer), then separately
            # iterating through the elements in the sublayer, and processing each "slice"
            # of the sublayer. 

            # One upshot of this method is that the resulting data we reconstruct the
            # stackup with depends on ALL items in the KiCAD stackup to be specified.
            # Missing items for any of the subvalues result in a shorter list for that
            # parameter. There is no way for us to know which sublayer it's missing for
            # so the "later" layers always appear to have the missing data. 

            # In order to normalize processing of both layer-specification types, we
            # normalize the relevant paramters before submitting this info to the
            # method which populates our own view of the stackup.  

            # For layers with no "addsublayer" tag, we add the layer data directly
            # to corresponding items in a dict() we pass to the next-level parser. 
            # For layers which include sub-layers, we construct a List of dict()s,
            # one for each sublayer, and submit them iterately to the next-level parser. 

            # We use the fact that the SexpParser uses 'int' keys for any "orphaned" 
            # keys it finds. These are keys found with no value (like "addsublayer").
            # As currently implemented, each one found is placed at "end" of the list, 
            # with an integer key. We can determine how many "sub-layers" exist by looking 
            # at the integer key value at the end of the List for a Dielectric with sublayers. 

            for lyr in kicad_pcb.setup.stackup.layer:
                # Skip physical-layers not used in construction of PCB (like solder paste)
                if (KTS_Stackup._kts_guess_layer_type(unquote(lyr[0])) == ""):
                    continue

                # Extract values from fields, if they exist, in the PCB-layer
                def _add_if(key:str, pcb_lyr:SexpList, idx=None) -> str:
                    if (idx == None):
                        return unquote(str(pcb_lyr[key])) if key in pcb_lyr else ""
                    else:
                        return unquote(str((pcb_lyr[key])[idx])) if ((key in pcb_lyr) and (idx < len(pcb_lyr[key]))) else ""

                # Here we pull layer params into a standard List-of-Lists
                # We do this as a prior step to parsing the info because
                # KiCAD treats Dielectric stackup-layers differently than
                # other layers. We standardize this to keep our parser simple.
                # The ID value has an index appended if it has 'sublayers'.
                def _extract_layer(lyr: SexpList, idx=None):
                    return {'ID'        : unquote(lyr[0]) + (('.'+str(idx+1)) if idx!=None else ""),
                            'TYPE'      : _add_if('type', lyr, idx) if idx==None else "",
                            'MATERIAL'  : _add_if('material', lyr, idx),
                            'THICKNESS' : _add_if('thickness', lyr, idx),
                            'COLOR'     : _add_if('color', lyr, idx)}

                # Look for a layer which has "un-named values" and check
                # that one of them is "addsublayer". This tells us that
                # we'll pull multiple KTS-layers from this one KiCAD-layer.
                if ((type([*lyr][-1]) is int) and ("addsublayer" in lyr[[*lyr][-1]])):
                    print (">>>>>> Found ", [*lyr][-1], " sublayer(s)")
                    # Iterate over what should be the number of total sub-layers here
                    for idx in range([*lyr][-1]+1):
                        layer_data = _extract_layer(lyr, idx)
                        lyr_has_flex, lyr_has_rigid = self._parse_stackup_layer(layer_data, copper_finish)
                else:
                    # Process as a single KiCAD-layer which maps to one KTS-layer
                    layer_data = _extract_layer(lyr)
                    lyr_has_flex, lyr_has_rigid = self._parse_stackup_layer(layer_data, copper_finish)
                
                # Running tally of entire stackup
                stack_has_flex  = True if lyr_has_flex else stack_has_flex
                stack_has_rigid = True if lyr_has_rigid else stack_has_rigid

            # Now with the physical stackup imported from the PCB, we make a guess
            # as to the "region" represented as either being "flex" or "rigid".
            # These guesses are made available to the user to adjust in the event
            # that we guessed wrong. Eventually, we may "force" sufficient hinting
            # in the PCB file to eliminate the need to allow user adjustments here.

            stack_flex_only  = True if (stack_has_flex and not stack_has_rigid) else False
            stack_rigid_only = True if (stack_has_rigid and not stack_has_flex) else False
            stack_has_both   = True if (stack_has_rigid and stack_has_flex) else False

            print("stack_has_flex   = ", stack_has_flex)
            print("stack_has_rigid  = ", stack_has_rigid)
            print("stack_flex_only  = ", stack_flex_only)
            print("stack_rigid_only = ", stack_rigid_only)
            print("stack_has_both   = ", stack_has_both)

            # We also perform some additional "guessing" to refine our first-pass
            # for layer characteristics. For instance, on a flex-only board, the
            # solder mask is also the coverlay. 

            for lyr in self.kts_stackup:
                if ('Silk' in lyr.lyr_type):
                    lyr.region = 'Flex' if (stack_flex_only) else '?'
                    lyr.region = 'Rigid' if (stack_rigid_only or stack_has_both) else '?'
                    lyr.color  = lyr.color if (not lyr.color == '???') else 'White' # Handle unspecified Silkscreen color
                if ('Mask' in lyr.lyr_type):
                    lyr.region = 'Flex' if (stack_flex_only) else '?'
                    lyr.region = 'Rigid' if (stack_rigid_only or stack_has_both) else '?'
                    lyr.color  = lyr.color if (not lyr.color == '???') else 'Green' # Handle unspecified Solder Mask color
                    if (stack_flex_only):
                        lyr.lyr_func = 'FlexCoverMask'
                        lyr.color    = 'Coverlay'
                if ('Dielec' in lyr.lyr_type):
                    lyr.region = 'Flex'  if (stack_flex_only) else lyr.region
                    lyr.region = 'Rigid' if (stack_rigid_only) else lyr.region
                    if (stack_has_both):
                        lyr.region = 'Flex'  if ('Flex' in lyr.lyr_func) else lyr.region
                        lyr.region = 'Rigid'  if ('Rigid' in lyr.lyr_func) else lyr.region


            # Now look through the drawing-layers to see if we have any tagged
            # with a name which contains a specific stackup-layer purpose.
            # When we can be confident that there is a drawing-layer specifically
            # intended for this stackup-layer, we assign it. If there is ambiguity,
            # we leave it empty for the user to assign. These are ultimately read
            # from the KTS vars in the Project file, so they are overwritten once
            # assigned. We "guess" here to make it easier on the user, and also to
            # keep as much of the definition process in the PCB file rather than Project.

        print("KTS_Stackup.init: ", len(self.kts_stackup), " stackup layers imported from PCB." )

        return


    # Here we extract the primary information from the KiCAD Stackup
    # We only are called if there is a valid layer to parse.
    def _parse_stackup_layer(self, lyr, copper_finish) -> Tuple[bool, bool]:
        # Make new row in our KTS Physical Stackup...
        # ...and grab reference to the newly added row
        self.kts_stackup.append(KTS_StackUpRecord("", "", "", "", 0, "", "", "", "", "", ""))
        stack_layer = self.kts_stackup[-1]

        # Get KiCAD-assigned stackup-layer/drawing-layer & guess a stackup-layer "type".
        # We will refine this later in the next step.
        stack_layer.content = lyr['ID'].replace('dielectric ', 'Dielec_')
        stack_layer.lyr_type = KTS_Stackup._kts_guess_layer_type(stack_layer.content)

        # Add any dielectric layers found to the layer dictionary
        if ('Dielec_' in stack_layer.content):
            self.KTS_Layers.dielectric_add(stack_layer.content)

        # Look in loaded KTS_Vars to see if there are any outlines for this stackup layer
        # We store the "ID" of the outline-layer drawing, and attribution
        stack_lyr_id = self.KTS_Layers.get_num(stack_layer.content)
        outline_id = self.KTS_Vars.outline_get(stack_lyr_id)
        if (outline_id != ""):
            stack_layer.outline = outline_id
            stack_layer.oln_asgn = 'VAR'
        else:
            stack_layer.outline = self.KTS_Layers.get_num("Edge.Cuts")
            stack_layer.oln_asgn = 'DEFAULT'

        if (stack_layer.lyr_type == 'Copper'):
            stack_layer.finish = copper_finish

        stack_layer.thkness = lyr['THICKNESS']
        raw_material = lyr['MATERIAL']

        #print ("raw_material = ", raw_material)
        if (raw_material != ""):
            stack_layer.material = KTS_Stackup._kts_guess_material_type(lyr['MATERIAL'])
        else:
            if ((stack_layer.lyr_type == 'Silk') or 
                (stack_layer.lyr_type == 'SolMask') or 
                (stack_layer.lyr_type == 'Dielec')):
                stack_layer.material = '???'
            else:
                stack_layer.material = KTS_Stackup._kts_guess_material_type(stack_layer.lyr_type)
            raw_material = ""
                
        raw_type = lyr['TYPE']
        stack_layer.lyr_func = KTS_Stackup._kts_guess_layer_function(raw_material + raw_type)
        stack_layer.lyr_func = stack_layer.lyr_func if stack_layer.lyr_func!="" else '???'

        raw_color = lyr['COLOR']
        stack_layer.color = KTS_Stackup._kts_guess_layer_color(raw_color + raw_type 
                                                               + stack_layer.material 
                                                               + stack_layer.lyr_type 
                                                               + stack_layer.lyr_func)

        # Look at Dielectric types to guess what kind of PCBA this is
        lyr_has_flex   = True if ('Flex'  in stack_layer.lyr_func) else False
        lyr_has_rigid  = True if ('Rigid' in stack_layer.lyr_func) else False

        return (lyr_has_flex, lyr_has_rigid)

    def get(self):
        return (self.kts_stackup)


    def _kts_guess_layer_type(lyr: str) -> str:
        """Guesses the generic type of stackup-layer"""
        if ('Cu' in lyr):
            return "Copper"
        if ('SilkS' in lyr):
            return "Silk"
        if ('Paste' in lyr):
            return ""
        if ('Mask' in lyr):
            return "SolMask"
        if ('Dielec' in lyr):
            return "Dielec"
        if ('dielectric' in lyr):
            return "Dielec"
        return ""


    def _kts_guess_material_type(matl: str) -> str:
        """Guesses the generic type of stackup-layer material"""
        matl = matl.upper()

        # Dielectric Materials
        if ('FR4' in matl):
            return "FR4"
        if ('PREPREG' in matl):
            return "PrePreg"
        if (('POLYIMIDE' in matl) | ('KAPTON' in matl) | ('COVER' in matl)):
            return "Polyimide"
        if (('PTFE' in matl) | ('TEFLON' in matl)):
            return "PTFE"
        if (('POLYOLEFIN' in matl) | ('CERAMIC' in matl)):
            return "Ceramic"
        if (('AL' in matl) | ('ALUMINUM' in matl) | ('ALUMINIUM' in matl)):
            return "Aluminum"

        # Surface Finish Materials
        if (('LPI' in matl) | ('LIQUID' in matl)):
            return "LPI"
        if (('DRY' in matl) | ('FILM' in matl)):
            return "DryFilm"
        if (('EPOXY' in matl) | ('SCREEN' in matl)):
            return "Epoxy"
        if (('DIRECT' in matl) | ('PRINTING' in matl)):
            return "Ink"

        # Conductive Materials
        if ('COPPER' in matl):
            return "Copper"

        return ""


    #****************************************************************************
    #*  These "Layer Function" definitions are guesses as to what the purpose   *
    #*  of a physical layer is in the stackup. These are based on the type of   *
    #*  material the layer is composed of and any "hint" contained in the name  *
    #*  of the material. These same name hints, ideally, are used when naming   *
    #*  drawing-layers. This helps to inform guesses as to which drawing-layer  *
    #*  to consider as a cut-pattern (outline) for that stackup physical layer. *
    #*                                                                          *
    #*  After parsing the entire PCB stackup, we refine our guesses to add some *
    #*  additional layer functions, once we understand the topology.            *
    #*      FlexCoverlayMask - applied to soldermask when a "flex_only" stackup *
    #****************************************************************************

    def _kts_guess_layer_function(matl: str) -> str:
        """Guesses either the type of layer or "name" of the layer """
        matl = matl.upper()

        if ('COPPER' in matl):
            return "Copper"

        # Clues we're on a "flex" stackup-layer
        if ( ('COVER' in matl) or ('FLEX' in matl) or ('POLYIMIDE' in matl) or ('KAPTON' in matl) ):
            if ( (( 'PREPREG'  in matl) or ('COVER' in matl)) and 
                 (('POLYIMIDE' in matl) or ('KAPTON' in matl)) ):

                if ('MASK' in matl):
                    return "FlexCoverMask"  # For Flex-only boards, the coverlay and soldermask may be the same entity
                else:
                    return "FlexCoverlay"   # For Rigid-Flex boards, coverlay represents its own layer(s) spec'd by drawing-layer(s)

            if ( ((  'CORE'    in matl) or ('FLEX' in matl)) and
                 (('POLYIMIDE' in matl) or ('KAPTON' in matl)) ):
                return "FlexCore"           # This is a layer to which the copper is attached

        # Remaining "Typical" physical-layers
        if ('CORE' in matl):        # On Dielectrics with sublayers, the "material" name in KiCAD must include 'Core'
            return "RigidCore"
        if ('PREPREG' in matl):     # On Dielectrics with sublayers, the "material" name in KiCAD must include 'PrePreg'
            return "RigidPrepreg"
        if ('MASK' in matl):        # This will refer to 'typical' soldermash on a Rigid substrate
            return "SolderMask"
        if ('SILK' in matl):        # This will refer to Silkscreen on outermost layer(s). 
            return "Silkscreen"             # Kicad doesn't have a good way to specify "inner" Silkscreen layers.
        return ""


    def _kts_guess_layer_color(color: str) -> str:
        """Guesses the 'color' the layer should be rendered in"""
        color = color.upper()

        if ('COVER' in color):
            return "Coverlay"
        if (('POLYIMIDE' in color) or ('KAPTON' in color)):
            return "Kapton"
        if ('RED' in color):
            return "Red"
        if ('GREEN' in color):
            return "Green"
        if ('BLUE' in color):
            return "Blue"
        if ('YELLOW' in color):
            return "Yellow"
        if ('PURPLE' in color):
            return "Purple"
        if ('BLACK' in color):
            return "Black"
        if ('WHITE' in color):
            return "White"
        if ('PREPREG' in color):
            return "PrePreg"
        if ('FR4' in color):
            return "FR4"
        if ('COPPER' in color):
            return "Copper"
        return "???"

# END - class KTS_Stackup

# END_MODULE - kts_PcbManager
