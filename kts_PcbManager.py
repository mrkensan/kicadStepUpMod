# -*- coding: utf-8 -*-
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

    KiCadPCB = None                         # Reference to the S-Expr parser Object
    Layers   = None                         # Reference to our KTS_Layers Object
    Stackup  = None                         # Reference to our KTS_Stackup Object
    KTS_Vars = None                         # Reference to KTS vars stored in PCB or Project file
    BoardOpenSuccess = False                # Local Flag inidcates we successfully fully parsed PCB
    filename = ""                           # Our copy of PCB filename from LoadBoard()

    def __init__(self):
        self.Layers    = KTS_Layers()
        self.Stackup   = KTS_Stackup()
        return

    def FilenameGet(self):
        import os
        pcb_file = os.path.basename(self.filename)
        pcb_folder = os.path.dirname(self.filename)
        return (pcb_file, pcb_folder)

    def StackupGet(self):
        return (self.Stackup)

    def LayersGet(self):
        return (self.Layers)

    def BoardLoad(self, filename: str):
        """Load and parse a KiCAD PCB from a filename.
           Filename must be absolute path to file.
           Returns pointer to KTS_PcbMgr on success, None on Fail."""

        # We've already got an open a board.
        # Name does not matter, we can only have one open board at a time.
        if (self.BoardOpenSuccess): return self

        self.filename = filename

        # Parse KiCAD PCB S-Exp Data structure
        #   Expected that file was previously 
        #   validated as error-free PCB file. 
        from kicad_parser import KicadPCB                       # S-Expr Parser to read-in the PCB file from KiCAD format
        self.KiCadPCB = KicadPCB.load(filename)                 # Parse S-Expr, return List-of-Lists representation

        self.KTSvars = KTS_Vars()
        self.KTSvars.project_vars_load(self)                    # Read KTS-vars from Proj file
        self.KTSvars.project_vars_save(self)                    # Save KTS-vars to Proj file

        self.Layers  = KTS_Layers()
        self.Layers.load_layers(self.KiCadPCB)                  # Extract drawing-layers

        print("The List of Outline Layers is: ", self.Layers.outline_layers_get())

        self.Stackup = KTS_Stackup.load_PCB(self.KiCadPCB)      # Infer stackup from loaded board

        if  ((self.Layers == None) or (self.Stackup == None)):  # Not expected if S-Expr parser loads error-free
            self.BoardOpenSuccess = False
            KtsGblState.delStateItem("BoardOpenSuccess")
            KtsGblState.delStateItem("KTS_Active_PCB")
            return None
        
        # Board Load was Successful
        self.BoardOpenSuccess = True
        print(">>> Global State Obj Ref: ", KtsGblState)
        KtsGblState.myState("BoardOpenSuccess", True)           # Let the world know this went well
        KtsGblState.myState("KTS_Active_PCB", self)             # Let the world know how to find the PCB
        return self

    def BoardForget(self):
        self.BoardOpenSuccess = False
        KtsGblState.delStateItem("BoardOpenSuccess")
        KtsGblState.delStateItem("KTS_Active_PCB")
        return None
        



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
#*    correspond to "Rigid" vs. "Flex" construction.                        *
#*                                                                          *
#*    This class is responsible for finding user-paramters in either/both   *
#*    the loaded 'kicad_pcb' and the 'kicad_pro' files.                     *
#*    File-path and base-name are considered identical between these files  *
#*    (ie. they are in the same folder) and only the extension differs.     *
#*                                                                          *
#*    The files are searched in order, first the PCB, then the Project, in  *
#*    accordance with the way these "user-vars" are migrated from Project   *
#*    to PCB-file by the KiCAD project manager. We use this sequence to     *
#*    find changes in the Project which are not migrated to PCB because     *
#*    User has not yet re-opened the PCB via the KiCAD Project Viewer.      *
#*                                                                          *
#*    The configuration information is merged into the Stackup object as    *
#*    it is constructed, augmented by the info availble in KTS_Vars.        *
#*    Any paramters not present are "defaulted" and later stored in the     *
#*    Project file. We keep a copy of the entire Project file, and merge    *
#*    our vars into this data, then re-write the Project file when User     *
#*    indicates to save. We do not save any info into the PCB file because  *
#*    the file is constructued not strictly conformant to S-Expr rules, so  *
#*    the S-Expr class would not be able to re-write portions of the file   *
#*    in a manner recognized by KiCAD. We rely on migration of this data    *
#*    to the PCB file by the KiCAD Project Viewer.                          *
#*                                                                          *
#****************************************************************************

class KTS_Vars():
    """Create and maintain a dictionary of User-vars stored
       in the selected PCB/Project. File load & save methods.
       Methods to look up vars by name & KiCAD layer Mnemonic."""

    kts_vars_dict  = None
    kicad_prj_dict = None

    def __init__(self):
        self.kts_vars_dict  = None
        self.kicad_prj_dict = None


    def project_vars_load(self, pcb: KTS_PcbMgr):
        import json
        import pprint

        try:
            proj_filename = pcb.filename.replace('.kicad_pcb', '.kicad_pro')
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

        if ("KTS_Outlines_dict" not in self.kts_vars_dict):
            self.kts_vars_dict["KTS_Outlines_dict"] = dict()    # Assure our key is there for later

        ##pprint.pprint(kicad_prj)
        ##print(type(kicad_prj))
        #print("~~~~~~~~~~~~~~~~~~~")
        #print(self.kts_vars_dict)
        #print(type(self.kts_vars_dict))
        #print(self.kts_vars_dict.keys())
        #print(json.dumps(self.kts_vars_dict))
        self.kts_vars_dict['KTS_var2'] = "my new string stuff"
        #print("~~~~~~~~~~~~~~~~~~~")


    def project_vars_save(self, pcb: KTS_PcbMgr):
        import json

        proj_filename = pcb.filename.replace('.kicad_pcb', '.kicad_pro')+".new"

        del self.kicad_prj_dict['text_variables']                   # Delete the read-in version of the vars section
        self.kicad_prj_dict['text_variables'] = self.kts_vars_dict  # Replace it with our new version

        try:
            prj_file = open(proj_filename, 'w', encoding='utf-8')
            json.dump(self.kicad_prj_dict, prj_file, indent=2)
        except:
            print (">>>>>>>>>>> Project file ", proj_filename, " unable to write. Aborting...")
        finally:
            prj_file.close()

        return 

# END - class KTS_Vars



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
class KTS_Stackup:
    """Pull stackup info from named PCB & Project files
       to construct a stackup picture of the PCBA which
       can be aware of both 'flex' and 'rigid' regions.
       
       Provides access methods for extracting this info
       for use when rendering a 3D model of the PCBA."""

    from typing import Tuple    # For return type hinting

    kts_stackup: List[KTS_StackUpRecord] = []   # Init empty class-local layer list

    def load_PCB(kicad_pcb):
        # Init empty layer list each time we init()
        # so we don't accumulate multiple copies of board
        KTS_Stackup.kts_stackup: List[KTS_StackUpRecord] = []
        kts_stackup = KTS_Stackup.kts_stackup

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

            for lyr in kicad_pcb.setup.stackup.layer:
                # Skip physical-layers not used in construction of PCB (like solder paste)
                if (kts_guess_layer_type(unquote(lyr[0])) == ""):
                    continue

                # 'layer' objects are Lists & Lists-of-Lists at their core, 
                # this is how the Sexp parser works.
                # Due to the way "sublayers" are expressed in the PCB file, 
                # 'sublayers' are not distinct. All items with the same key
                # are compiled into a List in order-of-encounter by the parser.
                # This means a key can refer to a single item, or to a list of 
                # such items which exist on that layer. 

                # This is relevant in the case of Dielectric layers, which 
                # contain "sublayers" rather than distinct layers for each 
                # specified in the stackup. For Dielectric layers to make sense,
                # we must require that the user compltely specify the parts
                # of all dielectric sublayers in order to assign attributes
                # correctly. 

                # In order to normalize processing of all layers, we will 
                # construct a canonical layer 'spec' used to populate the
                # KTS stackup data structs. For layers with no "addsublayer"
                # tag, it'll be a List with a single dict() entry. For layers
                # which include sub-layers, we construct a List of dict()s
                # so we can process each layer or sub-layer consistently as
                # we build the KTS view of the stackup.

                # We use the fact that the SexpParser uses 'int' keys for any
                # "orphaned" keys it finds. These are keys found with no value.
                # As currently implemented, these are placed at "end" of the list.
                # We can determine how many "sub-layers" exist by looking at the
                # integer key value at the end of the List for a Dielectric layer. 
                from kicad_parser import SexpList 

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
                    # Iterate over what should be the number of total layers here
                    for idx in range([*lyr][-1]+1):
                        layer_data = _extract_layer(lyr, idx)
                        layer_data['ID'] = layer_data['ID'].replace('dielectric ', 'Dielec_')
                        lyr_has_flex, lyr_has_rigid = KTS_Stackup._parse_stackup_layer(layer_data, copper_finish)
                else:
                    # Process as a single KiCAD-layer which maps to one KTS-layer
                    layer_data = _extract_layer(lyr)
                    layer_data['ID'] = layer_data['ID'].replace('dielectric ', 'Dielec_')
                    lyr_has_flex, lyr_has_rigid = KTS_Stackup._parse_stackup_layer(layer_data, copper_finish)
                
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

            for lyr in kts_stackup:
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

        print("KTS_Stackup.init: ", len(kts_stackup), " stackup layers imported from PCB." )

        return KTS_Stackup.kts_stackup


    # Here we extract the primary information from the KiCAD Stackup
    # We only are called if there is a valid layer to parse.

    def _parse_stackup_layer(lyr, copper_finish) -> Tuple[bool, bool]:
        # Make new row in our KTS Physical Stackup...
        # ...and grab reference to the newly added row
        KTS_Stackup.kts_stackup.append(KTS_StackUpRecord("", "", "", "", 0, "", "", "", "", "", ""))
        stack_this = KTS_Stackup.kts_stackup[-1]

        # Get KiCAD-assigned stackup-layer/drawing-layer & guess a stackup-layer "type".
        # We will refine this later in the next step.
        stack_this.content = lyr['ID']
        stack_this.lyr_type = kts_guess_layer_type(stack_this.content)

        if (stack_this.lyr_type == 'Copper'):
            stack_this.finish = copper_finish

        stack_this.thkness = lyr['THICKNESS']
        raw_material = lyr['MATERIAL']

        #print ("raw_material = ", raw_material)
        if (raw_material != ""):
            stack_this.material = kts_guess_material_type(lyr['MATERIAL'])
        else:
            if ((stack_this.lyr_type == 'Silk') or 
                (stack_this.lyr_type == 'SolMask') or 
                (stack_this.lyr_type == 'Dielec')):
                stack_this.material = '???'
            else:
                stack_this.material = kts_guess_material_type(stack_this.lyr_type)
            raw_material = ""
                
        raw_type = lyr['TYPE']
        stack_this.lyr_func = kts_guess_layer_function(raw_material + raw_type)
        stack_this.lyr_func = stack_this.lyr_func if stack_this.lyr_func!="" else '???'

        raw_color = lyr['COLOR']
        stack_this.color = kts_guess_layer_color(raw_color + raw_type + stack_this.material + stack_this.lyr_type + stack_this.lyr_func)

        # Look at Dielectric types to guess what kind of PCBA this is
        lyr_has_flex   = True if ('Flex'  in stack_this.lyr_func) else False
        lyr_has_rigid  = True if ('Rigid' in stack_this.lyr_func) else False

        return (lyr_has_flex, lyr_has_rigid)


    def get():
        return (KTS_Stackup.kts_stackup)

# END - class KTS_Stackup


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

class KTS_Layers:
    """Create and maintain a dictionary of the activated layers
       in the selected PCB. Methods to look up layer info by
       either KiCAD layer number or layer Mnemonic."""

    layer_name_dict = dict()
    layer_num_dict  = dict()
    outline_list    = []

    # Construct dictionaries from loaded PCB
    def load_layers(self, kicad_pcb):
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
                KTS_Layers.layer_name_dict[layer_mnemonic] = layer_given_name

                # Add layer_given_name -> KiCAD mnemonic
                if (len(kicad_pcb.layers[lyr_num]) > 2):
                    KTS_Layers.layer_name_dict[layer_given_name] = layer_mnemonic

                # Add number -> KiCAD mnemonic
                # Note: lyr_num is type str, despite it looking like a number
                KTS_Layers.layer_name_dict[lyr_num] = layer_mnemonic

                # Add KiCAD mnemonic -> number
                # Note: lyr_num is type str, despite it looking like a number
                KTS_Layers.layer_num_dict[layer_mnemonic] = lyr_num

                # Add KiCAD layer_given_name -> number
                if (len(kicad_pcb.layers[lyr_num]) > 2):
                    KTS_Layers.layer_num_dict[layer_given_name] = lyr_num

            # Build list of drawing-layers for cut-outline assignment by user
            self.outline_list_create()

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


def unquote(item: str) -> str:
    return (item.replace('"', ''))


def kts_guess_layer_type(lyr: str) -> str:
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


def kts_guess_material_type(matl: str) -> str:
    """Guesses the generic type of stackup-layer material"""

    # Dielectric Materials
    if ('FR4' in matl.upper()):
        return "FR4"
    if ('PREPREG' in matl.upper()):
        return "PrePreg"
    if (('POLYIMIDE' in matl.upper()) | ('KAPTON' in matl.upper()) | ('COVER' in matl.upper())):
        return "Polyimide"
    if (('PTFE' in matl.upper()) | ('TEFLON' in matl.upper())):
        return "PTFE"
    if (('POLYOLEFIN' in matl.upper()) | ('CERAMIC' in matl.upper())):
        return "Ceramic"
    if (('AL' in matl.upper()) | ('ALUMINUM' in matl.upper()) | ('ALUMINIUM' in matl.upper())):
        return "Aluminum"

    # Surface Finish Materials
    if (('LPI' in matl.upper()) | ('LIQUID' in matl.upper())):
        return "LPI"
    if (('DRY' in matl.upper()) | ('FILM' in matl.upper())):
        return "DryFilm"
    if (('EPOXY' in matl.upper()) | ('SCREEN' in matl.upper())):
        return "Epoxy"
    if (('DIRECT' in matl.upper()) | ('PRINTING' in matl.upper())):
        return "Ink"

    # Conductive Materials
    if ('COPPER' in matl.upper()):
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

def kts_guess_layer_function(matl: str) -> str:
    """Guesses either the type of layer or "name" of the layer """

    if ('COPPER' in matl.upper()):
        return "Copper"

    # Clues we're on a "flex" stackup-layer
    if ( ('COVER' in matl.upper()) or ('FLEX' in matl.upper()) or ('POLYIMIDE' in matl.upper()) or ('KAPTON' in matl.upper()) ):
        if ( (( 'PREPREG'  in matl.upper()) or ('COVER' in matl.upper())) and 
             (('POLYIMIDE' in matl.upper()) or ('KAPTON' in matl.upper())) ):

            if ('MASK' in matl.upper()):
                return "FlexCoverMask"  # For Flex-only boards, the coverlay and soldermask may be the same entity
            else:
                return "FlexCoverlay"   # For Rigid-Flex boards, coverlay represents its own layer(s) spec'd by drawing-layer(s)

        if ( ((  'CORE'    in matl.upper()) or ('FLEX' in matl.upper())) and
             (('POLYIMIDE' in matl.upper()) or ('KAPTON' in matl.upper())) ):
            return "FlexCore"           # This is a layer to which the copper is attached

    # Remaining "Typical" physical-layers
    if ('CORE' in matl.upper()):        # On Dielectrics with sublayers, the "material" name in KiCAD must include 'Core'
        return "RigidCore"
    if ('PREPREG' in matl.upper()):     # On Dielectrics with sublayers, the "material" name in KiCAD must include 'PrePreg'
        return "RigidPrepreg"
    if ('MASK' in matl.upper()):        # This will refer to 'typical' soldermash on a Rigid substrate
        return "SolderMask"
    if ('SILK' in matl.upper()):        # This will refer to Silkscreen on outermost layer(s). 
        return "Silkscreen"             # Kicad doesn't have a good way to specify "inner" Silkscreen layers.
    return ""


def kts_guess_layer_color(color: str) -> str:
    """Guesses the 'color' the layer should be rendered in"""
    if ('COVER' in color.upper()):
        return "Coverlay"
    if (('POLYIMIDE' in color.upper()) or ('KAPTON' in color.upper())):
        return "Kapton"
    if ('RED' in color.upper()):
        return "Red"
    if ('GREEN' in color.upper()):
        return "Green"
    if ('BLUE' in color.upper()):
        return "Blue"
    if ('YELLOW' in color.upper()):
        return "Yellow"
    if ('PURPLE' in color.upper()):
        return "Purple"
    if ('BLACK' in color.upper()):
        return "Black"
    if ('WHITE' in color.upper()):
        return "White"
    if ('PREPREG' in color.upper()):
        return "PrePreg"
    if ('FR4' in color.upper()):
        return "FR4"
    if ('COPPER' in color.upper()):
        return "Copper"
    return "???"


#****************************************************************************
#*                                                                          *
#*  KtsColor - Map KTS colors to Qt colors for rendering                    *
#*                                                                          *
#*    Here we create a dict() then provide the function to query. We take   *
#*    this approach for two reasons:                                        *
#*      1. Return value is a QColor object                                  *
#*      2. We would like to overwrite this list with stored values,         *
#*         either from the PCB or Workbench defaults.                       *
#*    By allowing update of the dict() we only look in one place for colors.*
#****************************************************************************

class KtsColor:
    from PySide.QtGui import QColor

    kts_layer_color_map = { "Kapton"  : '#B38419', #C4911C
                            "Coverlay": '#D9A01E',
                            "Red"     : '#A2161E',
                            "Green"   : '#008700',
                            "Blue"    : '#164191',
                            "Yellow"  : '#FFD439',
                            "Purple"  : '#542D70',
                            "Black"   : '#1A2127',
                            "White"   : '#EDF0F5',
                            "FR4"     : '#82AA8A',
                            "PrePreg" : '#9FD0A9',
                            "Copper"  : '#EF8E76'}  #EFB18F

    def to_QColor(color: str) -> QColor:
        """Translate the 'layer-color' to Qt Colors"""
        return (KtsColor.QColor(KtsColor.kts_layer_color_map.get(color, '#808080')))

# END - class KtsColor

# END_MODULE - kts_PcbManager
