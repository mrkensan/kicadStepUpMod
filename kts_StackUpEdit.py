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
#*    KiCAD_Layers: KTS layer definition & purpose for PCBA                 *
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
__KTS_FILE_NAME__ = "KTS_STACKUPEDIT"

from kts_PrefsMgmt import prefs_set_file_version
prefs_set_file_version(__KTS_FILE_NAME__, __KTS_FILE_VER__)


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
    if ('dielectric' in lyr):
        return "Dielec"
    return ""


def kts_guess_material_type(matl: str) -> str:
    """Guesses the generic type of stackup-layer material"""

    # Dielectric Materials
    if ('FR4' in matl.upper()):
        return "FR4"
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
    if (('COVER' in matl.upper()) or ('POLYIMIDE' in matl.upper()) or ('FLEX' in matl.upper())):
        if (('COVER' in matl.upper()) or (('PREPREG' in matl.upper()) and ('POLYIMIDE' in matl.upper()))):
            return "FlexCoverlay"

        if ((('POLYIMIDE' in matl.upper()) or ('FLEX' in matl.upper())) and ('CORE' in matl.upper())):
            return "FlexCore"

    # Remaining "Typical" physical-layers
    if ('CORE' in matl.upper()):
        return "RigidCore"
    if ('PREPREG' in matl.upper()):
        return "RigidPrepreg"
    if ('MASK' in matl.upper()):
        return "SolderMask"
    if ('SILK' in matl.upper()):
        return "Silkscreen"
    return ""


def kts_guess_layer_color(color: str) -> str:
    """Guesses the 'color' the layer should be rendered in"""
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
    from collections import defaultdict
    from PySide.QtGui import QColor

    kts_layer_color_map = { "Kapton"  : '#C4911C',
                            "Red"     : '#A2161E',
                            "Green"   : '#008700',
                            "Blue"    : '#164191',
                            "Yellow"  : '#FFD439',
                            "Purple"  : '#542D70',
                            "Black"   : '#1A2127',
                            "White"   : '#EDF0F5',
                            "FR4"     : '#82AA8A',
                            "PrePreg" : '#9FD0A9',
                            "Copper"  : '#EFB18F'}

    def to_QColor(color: str) -> QColor:
        """Translate the 'layer-color' to Qt Colors"""
        return (QColor(KtsColor.kts_layer_color_map.get(color, '#808080')))

# END - class KtsColor

        #junk = {'Blue': '#0000FF', 'Red': '#FF0000', 'Green': '#00FF00'}
        #junk2 = str(junk)
        #my_dict = eval(junk2)
        #pprint.pprint(my_dict)




#****************************************************************************
#*                                                                          *
#*  KiCAD_Layers - KTS layer definition & purpose for PCBA                  *
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

class KiCAD_Layers:
    """Create and maintain a dictionary of the activated layers
       in the selected PCB. Methods to look up layer info by
       either KiCAD layer number or layer Mnemonic."""

    layer_dict = dict()     # Init empty class-local dictionary

    def init(kicad_pcb):
        import pprint
        if not hasattr(kicad_pcb, 'layers'):
            # ToDo: Make this into an "Alert"
            print("KiCAD_Layers.init: No Layers found in PCB file." )
        else:
            print("KiCAD_Layers.init: Found ", len(kicad_pcb.layers), " drawing layers." )

            for lyr in kicad_pcb.layers:
                # Add KiCAD mnemonic->number mapping
                KiCAD_Layers.layer_dict[(kicad_pcb.layers[lyr])[0].replace('"', '')] = lyr

                # Add 'user layer name'->number mapping
                if (len(kicad_pcb.layers[lyr]) > 2):
                    KiCAD_Layers.layer_dict[(kicad_pcb.layers[lyr])[2].replace('"', '')] = lyr

                # Add number->[mnemonic, given_name]
                if (len(kicad_pcb.layers[lyr]) > 2):
                    KiCAD_Layers.layer_dict[lyr] = [(kicad_pcb.layers[lyr])[0].replace('"', ''), (kicad_pcb.layers[lyr])[2].replace('"', '')]
                else:
                    KiCAD_Layers.layer_dict[lyr] = [(kicad_pcb.layers[lyr])[0].replace('"', ''), None]
        return

    def kts_layer_get(lyr:str) -> str:
        try:
            return (KiCAD_Layers.layer_dict[lyr])
        except:
            return (None)
        
# END - class KiCAD_Layers


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
    oln_asgn: str   # Outline is assigned from PCB or USER -----------------------> Read from KTS Vars in Project File
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


    def init(kicad_pcb):
        # Init empty layer list each time we init()
        # so we don't accumulate multiple copies of board
        KTS_Stackup.kts_stackup: List[KTS_StackUpRecord] = []
        kts_stackup = KTS_Stackup.kts_stackup

        # Flags used to refine guesses about layers
        has_flex   = False
        has_rigid  = False
        flex_only  = False
        rigid_only = False
        has_both   = False

        if not hasattr(kicad_pcb.setup, 'stackup'):
            # ToDo: Make this into an "Alert"
            print("KTS_Stackup.init: No Stackup found in PCB file." )
        else:
            copper_finish = (kicad_pcb.setup.stackup.copper_finish).replace('"', '')
            copper_finish = copper_finish if(not 'None' in copper_finish) else 'Bare'
            print("Stackup Sections:")
            print(*kicad_pcb.setup.stackup['layer'])
            print("****************************************************")

            for lyr in kicad_pcb.setup.stackup.layer:
                # Look for layers with no "purpose" and skip them
                if (kts_guess_layer_type(lyr[0].replace('"', '')) == ""):
                    continue

                # 'layer' objects are Lists & Lists-of-Lists at their core
                # Due to the way "sublayers" are parsed, the keys on a layer
                # can refer to a single string or a List object. 

                if(kts_guess_layer_type(lyr[0].replace('"', '')) == "Dielec"):
                    print("===================\n", lyr[0].replace('"', ''))
                    print (*lyr)
                    print ("Length lyr = ", len(lyr))
                    print ("Length lyr.type = ", len(lyr.type))
                    print (*lyr.type)
                    print ("Length lyr.material = ", len(lyr.material))
                    print ("Type lyr.material = ", type(lyr.material))
                    print (*lyr.material)
                    if (type(lyr.thickness) is int):
                        print ("Type lyr.thickness = ", type(lyr.thickness))
                        print (lyr.thickness)
                    else:
                        print ("Length lyr.thickness = ", len(lyr.thickness))
                        print ("Type lyr.thickness = ", type(lyr.thickness))
                        print (*lyr.thickness)
                    print("+++++++++++++++++")
                    idx = 0
                    for itm in lyr:
                        print(itm)
                        if (itm == 0):
                            print('inside itm[0]:', " (idx = ", idx, ")")
                            #local = lyr[0]
                            pprint.pprint(lyr[0])
                        if (itm == 1):
                            print('inside itm[1]:', " (idx = ", idx, ")")
                            print(lyr.addsublayer)
                            print(lyr[1])
                            print(*lyr.material)
                            print(*lyr['material'])
                            print(len(lyr['material']))
                            junk = lyr.thickness
                            pprint.pprint(junk[0])
                            pprint.pprint(" = ")
                            pprint.pprint(junk[1])
                            pprint.pprint(junk[2])
                            print('\n')
                            #local = lyr[1]
                            #pprint.pprint(local.material)
                        idx = idx + 1


        print("KTS_Stackup.init: ", len(kts_stackup), " stackup layers imported from PCB." )

            #pprint.pprint(kts_stackup)
        return
            ## Now with the physical stackup imported from the PCB, we make a guess
            ## as to the "region" represented as either being "flex" or "rigid".
            ## These guesses are made available to the user to adjust in the event
            ## that we guessed wrong. Eventually, we may "force" sufficient hinting
            ## in the PCB file to eliminate the need to allow user adjustments here.
 
            #flex_only  = True if (has_flex and not has_rigid) else False
            #rigid_only = True if (has_rigid and not has_flex) else False
            #has_both   = True if (has_rigid and has_flex) else False

            #print("has_flex = ", has_flex)
            #print("has_rigid = ", has_rigid)
            #print("flex_only = ", flex_only)
            #print("rigid_only = ", rigid_only)
            #print("has_both = ", has_both)



            ## We also perform some additional "guessing" to refine our first-pass
            ## for layer characteristics. For instance, on a flex-only board, the
            ## solder mask is also the coverlay. 

            #for lyr in kts_stackup:
            #    if ('Silk' in lyr.lyr_type):
            #        lyr.region = 'Flex' if (flex_only) else '?'
            #        lyr.region = 'Rigid' if (rigid_only or has_both) else '?'
            #        lyr.color  = lyr.color if (not lyr.color == '???') else 'White' # Handle unspecified Silkscreen color
            #    if ('Mask' in lyr.lyr_type):
            #        lyr.region = 'Flex' if (flex_only) else '?'
            #        lyr.region = 'Rigid' if (rigid_only or has_both) else '?'
            #        lyr.color  = lyr.color if (not lyr.color == '???') else 'Green' # Handle unspecified Solder Mask color
            #        if (flex_only):
            #            lyr.lyr_func = 'FlexCoverlayMask'
            #            lyr.color    = 'Kapton'
            #    if ('Dielec' in lyr.lyr_type):
            #        lyr.region = 'Flex'  if (flex_only) else lyr.region
            #        lyr.region = 'Rigid' if (rigid_only) else lyr.region
            #        if (has_both):
            #            lyr.region = 'Flex'  if ('Flex' in lyr.lyr_func) else lyr.region
            #            lyr.region = 'Rigid'  if ('Rigid' in lyr.lyr_func) else lyr.region


            ## Now look through the drawing-layers to see if we have any tagged
            ## with a name which contains a specific stackup-layer purpose.
            ## When we can be confident that there is a drawing-layer specifically
            ## intended for this stackup-layer, we assign it. If there is ambiguity,
            ## we leave it empty for the user to assign. These are ultimately read
            ## from the KTS vars in the Project file, so they are overwritten once
            ## assigned. We "guess" here to make it easier on the user, and also to
            ## keep as much of the definition process in the PCB file rather than Project.




    # Here we extract the primary information from the KiCAD Stackup
    # We only are called if there is a valid layer to parse.

    def _parse_stackup_layer(lyr, lyr_id: int) -> Tuple[bool, bool]:
        # Make new row in our KTS Physical Stackup
        kts_stackup = KTS_Stackup.kts_stackup
        kts_stackup.append(KTS_StackUpRecord("", "", "", "", 0, "", "", "", "", "", ""))

        # Get KiCAD-assigned stackup-layer/drawing-layer & guess a stackup-layer "type".
        # We will refine this later in the next step.
        kts_stackup[-1].content = lyr[0].replace('"', '')
        kts_stackup[-1].lyr_type = kts_guess_layer_type(kts_stackup[-1].content)

        if (kts_stackup[-1].lyr_type == 'Copper'):
            kts_stackup[-1].finish = copper_finish

        if hasattr(lyr, "thickness"):
            kts_stackup[-1].thkness = lyr.thickness

        raw_material = ""
        if hasattr(lyr, "material"):
            kts_stackup[-1].material = kts_guess_material_type((lyr.material).replace('"', ''))
            raw_material = (lyr.material).replace('"', '')
        else:
            kts_stackup[-1].material = kts_guess_material_type(kts_stackup[-1].lyr_type) 
                
        raw_type = ""
        if hasattr(lyr, "type"):
            raw_type = (lyr.type).replace('"', '')
        kts_stackup[-1].lyr_func = kts_guess_layer_function(raw_material + raw_type)

        pcb_color = (lyr.color).replace('"', '') if hasattr(lyr, "color") else ""
        kts_stackup[-1].color = kts_guess_layer_color(pcb_color + raw_type + kts_stackup[-1].material + kts_stackup[-1].lyr_type)

        # Look at Dielectric types to guess what kind of PCBA this is
        #print('Layer Func is: ', kts_stackup[-1].lyr_func)

        if ('Dielec' in kts_stackup[-1].lyr_type):
            print('Dielec Layer')
            has_flex   = True if ('Flex'  in kts_stackup[-1].lyr_func) else False
            has_rigid  = True if ('Rigid' in kts_stackup[-1].lyr_func) else False

        return (lyr_has_flex, lyr_has_rigid)



    def get():
        return (KTS_Stackup.kts_stackup)

    #def kts_layer_get(lyr:str) -> str:
    #    try:
    #        return (KiCAD_Layers.layer_dict[lyr])
    #    except:
    #        return (None)
        
# END - class KiCAD_Layers



# create new Tab in ComboView
from PySide import QtGui    # In FreeCAD the QtWidgets module is subsumed into QtGui (https://wiki.freecadweb.org/PySide)
import FreeCADGui
#from PySide import uic
import pprint


def _getComboView(main_window):
   dock_widgets = main_window.findChildren(QtGui.QDockWidget)
   for i in dock_widgets:
       #print(str(i.objectName()))
       if str(i.objectName()) == "Combo View":
           return i.findChild(QtGui.QTabWidget)
       elif str(i.objectName()) == "Python Console":
           return i.findChild(QtGui.QTabWidget)
   raise Exception ("'Combo View' widget found")


#### ToDo: Only open Window when it's time to Edit stackup
#### ToDo: Make OK & Cancel (and a Save button) do the "right thing"
#### ToDo: Make an Edit-Stackup command button to show our editor

def kts_make_stack_edit_tab(stackup: KTS_Stackup):
    combo_view_tabs = _getComboView(FreeCADGui.getMainWindow())

    if (combo_view_tabs == None):
        print("Combo View Not Found")

    """
    #our_new_tab = QtGui.QDialog()
    our_new_tab = QtGui.QTableView()
    #cell = our_new_tab.QTableWidget.cellWidget(1,1)
    pprint.pprint(dir(our_new_tab))
    """
    #our_new_tab = QtGui.QDialog()
    our_new_tab = StackUpEditDialog(stackup)
    
    # Getting the data Model
    model = CustomTableModel()

    # Creating a QTableView
    table_view = QtGui.QTableView()
    table_view.setModel(model)

    #our_new_tab = table_view

    #combo_view.addTab(our_new_tab,"Stackup Editor")
    tab_index = combo_view_tabs.addTab(our_new_tab,"Stackup Editor")
    print("Tab Index = "+str(tab_index))
    print("Index of 'our_new_tab' = "+str(combo_view_tabs.indexOf(our_new_tab)))
    print("Text of 'our_new_tab' = "+str(combo_view_tabs.tabText(tab_index)))

    
    #uic.loadUi("/myTaskPanelforTabs.ui",combo)
    #our_new_tab.show()
    #combo_view_tabs.removeTab(tab_index)
    #combo_view_tabs.setTabEnabled(tab_index, True)
    #combo_view_tabs.setTabVisible(tab_index, False)

    dw=combo_view_tabs.findChildren(QtGui.QDialog)
    for i in dw:
       print(str(i.objectName()))


    return combo_view_tabs, tab_index;

# END - kts_make_stack_edit_tab()


#from PySide import QtWidgets
#from PySide2.QtWidgets import QApplication, QDialog, QMainWindow, QPushButton, QDialogButtonBox, QVBoxLayout, QLabel
from PySide.QtGui import QDialog, QDialogButtonBox, QVBoxLayout, QHBoxLayout, QBoxLayout, QLabel, QGraphicsRectItem, QGraphicsScene, QGraphicsView, QPushButton
from PySide.QtGui import QPen, QColor, QBrush, QFrame, QComboBox, QLineEdit, QFont, QLabel
from PySide.QtCore import QRectF
#from kts_StackUpEdit import KtsColor


# We subclass QDialog here in order override some
# built-in methods like accept() & cancel(), etc..
class StackUpEditDialog(QDialog):
    """Create the 'Stackup Editor' tab in
       the 'Combo View' Panel of the UI."""

    def __init__(self, stackup: KTS_Stackup):
        super().__init__()
        #self.setFixedHeight(300)

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)


        #my_rect = QGraphicsRectItem(0,0,100,100)
        #print(my_rect)
        #print(my_rect.isWidget())
        #scene.addItem(my_rect)

        layer_height = 13
        layer_spacing = 4
        combo_list_height = 15

        my_rect = QRectF(0,0,50,layer_height)

        scene = QGraphicsScene(self)
        #scene.addRect(my_rect, Qt.NoPen, Qt.red)
        my_color = QColor('#008080')
        #junk = my_color.setRgb(0x008080)
        print("my_color = ", my_color)
        #junk = my_color.setRgbF(0.0, 1.0, 0.0, 1.0)
        scene.addRect(0,0,50,layer_height, Qt.NoPen, KtsColor.to_QColor("Purple"))
        print("Qt.green = ", Qt.green)
        #print("junk = ", junk)
        
        view = QGraphicsView(scene)
        view.setFrameStyle(QFrame.NoFrame)
        #view.setMaximumWidth(200)
        #view.setMaximumHeight(100)
        view.setFixedHeight(layer_height)
        view.setFixedWidth(50)

        combobox = QComboBox()
        font = combobox.font()
        print("Combo Font Size is: ", font.pointSize())
        print("Combo Font name is: ", font.rawName())
        print("Combo sixeHint is: ", combobox.sizeHint())
        font.setPointSize(7)
        combobox.setFont(font)
        combobox.setFixedHeight(layer_height)


        combobox.resize(61,15)
        #combobox.adjustSize()
        #font = QFont('Arial', 10)
        combobox.addItems(['One', 'Two', 'Three', 'Four'])
        #combobox.setFixedHeight(layer_height-15)
        combobox2 = QComboBox()
        combobox2.addItems(['Two', 'Three', 'Four'])
        #combobox2.setFixedHeight(layer_height-10)
        #combobox.setFixedWidth(50)

        entry = QLineEdit()
        entry.setFixedHeight(layer_height)


        scene2 = QGraphicsScene(self)
        scene2.addRect(my_rect, Qt.NoPen, Qt.blue)

        view2 = QGraphicsView(scene2)
        view2.setFrameStyle(QFrame.NoFrame)
        view2.setFixedHeight(layer_height)

        text_box = QLabel()
        text_box.setText("Here's some text")

        row_layout = QHBoxLayout()
        row_layout.setSpacing(2)   # No Horiz space between elements
        row_layout.setMargin(0)   # No Horiz space between elements
        row_layout.setContentsMargins(0, 0, 0, 0)

        row_layout.addStretch()
        row_layout.addWidget(text_box)
        row_layout.addWidget(entry)
        row_layout.addWidget(view)
        row_layout.addWidget(combobox)
        row_layout.addStretch()

        
        row_layout2 = QHBoxLayout()
        row_layout2.addWidget(view2)

        #row_layout.setMaximumHeight(100)


        message = QLabel("Something happened, is that OK?")
        message.setFixedHeight(20)

        message2 = QLabel("Something happened, is that OK?")

        stackup_header_row = self._build_stackup_row_header()
        #row_layout4 = self._build_stackup_row(stackup[0])

        #self.layout.addWidget(message)
        #self.layout.addLayout(row_layout)
        #self.layout.addLayout(row_layout2)



        self.layout = QVBoxLayout() # We use a Vertical Box layout to stack the layers
        self.layout.setSpacing(layer_spacing)   # No vertical space between elements
        #self.layout.setMargin(0)   # No vertical space between elements
        #self.layout.setContentsMargins(0,0,0,0)

        # Add a header, and content row for each physical stackup-layer
        self.layout.addLayout(stackup_header_row)
        for lyr in stackup:
            self.layout.addLayout(self._build_stackup_row(lyr))

        #self.layout.addLayout(row_layout4)
        #self.layout.addWidget(message2)
        self.layout.addStretch()
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

        return


    def _build_stackup_row(self, layer: KTS_StackUpRecord): # Returns a QHBoxLayout element
        item_vert_ht  = 13
        item_horz_wd = 60
        item_horz_spc = 10
        items = []

        # We do this because we can't iterate over the items in 'layer'
        layer_col_vals = []
        layer_col_vals.append(layer.content)
        layer_col_vals.append(layer.outline)
        layer_col_vals.append(layer.lyr_type)
        layer_col_vals.append(str(layer.thkness))
        layer_col_vals.append(layer.material)
        layer_col_vals.append(layer.region)
        layer_col_vals.append(layer.color)
        layer_col_vals.append(layer.finish)
        layer_col_vals.append(layer.lyr_func)

        # A colored rectangle representing the material of layer
        rect = QGraphicsScene(self)                     # Create container (scene) for graphics element
        rect.addRect(0, 0, item_horz_wd, item_vert_ht, 
                     Qt.NoPen, KtsColor.to_QColor(layer.color))  # Add a rectangle to scene
        
        # Adjust characteristics of the containing view object
        items.append(QGraphicsView(rect))           # New view containing rectangle
        items[-1].setFrameStyle(QFrame.NoFrame)     # Remove "frame" around view
        items[-1].setFixedHeight(item_vert_ht)      # Adjust Height to absolute
        items[-1].setFixedWidth(item_horz_wd)       # ... and width

        # We want a Bold header font
        #header_font = QtGui.QFont()
        #header_font.setBold(True)

        for col in layer_col_vals:
            # Construct text elements for Row
            items.append(QLabel())
            items[-1].setText(col)
            items[-1].setAlignment(Qt.AlignCenter)
            #items[-1].setFont(header_font)
            items[-1].setFixedHeight(item_vert_ht)
            items[-1].setFixedWidth(item_horz_wd)
            #items[-1].setStyleSheet("border: 1px solid black;")

        # Create row object
        row_layout = QHBoxLayout()
        row_layout.setSpacing(item_horz_spc) # Horiz space between elements
        row_layout.setMargin(0)              # No Horiz margin inside elements
        row_layout.setContentsMargins(0, 0, 0, 0)

        # Build actual row
        for col in items:
            row_layout.addWidget(col)
        row_layout.addStretch()

        return (row_layout)

# END - _build_stackup_row()


    def _build_stackup_row_header(self): # Returns a QHBoxLayout element
        item_vert_ht  = 13
        item_horz_wd = 60
        item_horz_spc = 10

        headers = []
        column_labels = ["Stack Up", "Content", "Outline", "Type", "Thickness", 
                         "Material", "Region", "STEP Color", "Cu Finish", "Function"]

        # We want a Bold header font
        header_font = QtGui.QFont()
        header_font.setBold(True)

        for col in column_labels:
            # Construct text elements for Row
            headers.append(QLabel())
            headers[-1].setText(col)
            headers[-1].setAlignment(Qt.AlignCenter)
            headers[-1].setFont(header_font)
            headers[-1].setFixedHeight(item_vert_ht)
            headers[-1].setFixedWidth(item_horz_wd)
            #headers[-1].setStyleSheet("border: 1px solid black;")
        
        # Create row object
        row_layout = QHBoxLayout()
        row_layout.setSpacing(item_horz_spc) # No Horiz space between elements
        row_layout.setMargin(0)         # No Horiz space between elements
        row_layout.setContentsMargins(0, 0, 0, 0)

        # Build actual row
        for col in headers:
            row_layout.addWidget(col)
        row_layout.addStretch()

        return (row_layout)

# END - _build_stackup_row_header()





    # This overrides the builtin accept() method
    def accept(stuff):
        print("Accepted", stuff)
        pprint.pprint(stuff)

# END - class StackUpEditDialog


#class StackUpEditDialog(QDialog):
#    def __init__(self):
#        super().__init__()

#        okButton = QPushButton('OK')
#        cancelButton = QPushButton('Cancel')
        
#        hbox = QHBoxLayout()
#        hbox.addStretch(1)
#        hbox.addWidget(okButton)
#        hbox.addWidget(cancelButton)

#        vbox = QVBoxLayout()
#        message = QLabel("Something happened, is that OK?")
#        vbox.addLayout(message)
#        vbox.addStretch(1)
#        vbox.addLayout(hbox)
#        self.setLayout(vbox)


#    # This overrides the builtin accept() method
#    def accept(stuff):
#        print("Accepted", stuff)
#        pprint.pprint(stuff)

## END - class StackUpEditDialog



# This reimplements methods from the "QAbstractTableModel" class
# This is required to provide a "data model" to the TableView

from PySide.QtCore import Qt, QAbstractTableModel
from PySide.QtGui import QColor

headers = ["Scientist name", "Birthdate", "Contribution"]
rows =    [("Newton", "1643-01-04", "Classical mechanics"),
           ("Einstein", "1879-03-14", "Relativity"),
           ("Darwin", "1809-02-12", "Evolution")]

class CustomTableModel(QAbstractTableModel):
    # The methods below must be implemented here in order to
    # understand our data. Via these methods, our data is
    # imported into the inteneral data represenation of the
    # 'QAbstractTableModel' which supplies data to QTableView.

    def rowCount(self, parent):
        # Must return the number of rows in the dataset
        return len(rows)

    def columnCount(self, parent):
        # Must return the number of columns in the dataset
        return len(headers)

    def headerData(self, section, orientation, role):
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            # Returns the header data for the given column
            return headers[section]
        else:
            return "{}".format(section)

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            # returns the cell value at the given index
            # (index specifies row & col)
            return rows[index.row()][index.column()]
        elif role == Qt.BackgroundRole:
            return QColor(Qt.white)
        elif role == Qt.TextAlignmentRole:
            return Qt.AlignRight

        return None

# END - class CustomTableModel()


"""
        self.KiCAD_Layers_json = {
            {'kicad_num': "0",  'kicad_enum': "F.Cu",      'kts_dscr': "", 'kicad_dscr': ""}
            {'kicad_num': "1",  'kicad_enum': "In1.Cu",    'kts_dscr': "", 'kicad_dscr': ""}
            {'kicad_num': "2",  'kicad_enum': "In2.Cu",    'kts_dscr': "", 'kicad_dscr': ""}
            {'kicad_num': "3",  'kicad_enum': "In3.Cu",    'kts_dscr': "", 'kicad_dscr': ""}
            {'kicad_num': "4",  'kicad_enum': "In4.Cu",    'kts_dscr': "", 'kicad_dscr': ""}
            {'kicad_num': "5",  'kicad_enum': "In5.Cu",    'kts_dscr': "", 'kicad_dscr': ""}
            {'kicad_num': "6",  'kicad_enum': "In6.Cu",    'kts_dscr': "", 'kicad_dscr': ""}
            {'kicad_num': "7",  'kicad_enum': "In7.Cu",    'kts_dscr': "", 'kicad_dscr': ""}
            {'kicad_num': "8",  'kicad_enum': "In8.Cu",    'kts_dscr': "", 'kicad_dscr': ""}
            {'kicad_num': "9",  'kicad_enum': "In9.Cu",    'kts_dscr': "", 'kicad_dscr': ""}
            {'kicad_num': "10", 'kicad_enum': "In10.Cu",   'kts_dscr': "", 'kicad_dscr': ""}
            {'kicad_num': "11", 'kicad_enum': "In11.Cu",   'kts_dscr': "", 'kicad_dscr': ""}
            {'kicad_num': "12", 'kicad_enum': "In12.Cu",   'kts_dscr': "", 'kicad_dscr': ""}
            {'kicad_num': "13", 'kicad_enum': "In13.Cu",   'kts_dscr': "", 'kicad_dscr': ""}
            {'kicad_num': "14", 'kicad_enum': "In14.Cu",   'kts_dscr': "", 'kicad_dscr': ""}
            {'kicad_num': "15", 'kicad_enum': "In15.Cu",   'kts_dscr': "", 'kicad_dscr': ""}
            {'kicad_num': "16", 'kicad_enum': "In16.Cu",   'kts_dscr': "", 'kicad_dscr': ""}
            {'kicad_num': "17", 'kicad_enum': "In17.Cu",   'kts_dscr': "", 'kicad_dscr': ""}
            {'kicad_num': "18", 'kicad_enum': "In18.Cu",   'kts_dscr': "", 'kicad_dscr': ""}
            {'kicad_num': "19", 'kicad_enum': "In19.Cu",   'kts_dscr': "", 'kicad_dscr': ""}
            {'kicad_num': "20", 'kicad_enum': "In20.Cu",   'kts_dscr': "", 'kicad_dscr': ""}
            {'kicad_num': "21", 'kicad_enum': "In21.Cu",   'kts_dscr': "", 'kicad_dscr': ""}
            {'kicad_num': "22", 'kicad_enum': "In22.Cu",   'kts_dscr': "", 'kicad_dscr': ""}
            {'kicad_num': "23", 'kicad_enum': "In23.Cu",   'kts_dscr': "", 'kicad_dscr': ""}
            {'kicad_num': "24", 'kicad_enum': "In24.Cu",   'kts_dscr': "", 'kicad_dscr': ""}
            {'kicad_num': "25", 'kicad_enum': "In25.Cu",   'kts_dscr': "", 'kicad_dscr': ""}
            {'kicad_num': "26", 'kicad_enum': "In26.Cu",   'kts_dscr': "", 'kicad_dscr': ""}
            {'kicad_num': "27", 'kicad_enum': "In27.Cu",   'kts_dscr': "", 'kicad_dscr': ""}
            {'kicad_num': "28", 'kicad_enum': "In28.Cu",   'kts_dscr': "", 'kicad_dscr': ""}
            {'kicad_num': "29", 'kicad_enum': "In29.Cu",   'kts_dscr': "", 'kicad_dscr': ""}
            {'kicad_num': "30", 'kicad_enum': "In30.Cu",   'kts_dscr': "", 'kicad_dscr': ""}
            {'kicad_num': "31", 'kicad_enum': "B.Cu",      'kts_dscr': "", 'kicad_dscr': ""}
            {'kicad_num': "32", 'kicad_enum': "B.Adhes",   'kts_dscr': "", 'kicad_dscr': "B.Adhesive"}
            {'kicad_num': "33", 'kicad_enum': "F.Adhes",   'kts_dscr': "", 'kicad_dscr': "F.Adhesive"}
            {'kicad_num': "34", 'kicad_enum': "B.Paste",   'kts_dscr': "", 'kicad_dscr': ""}
            {'kicad_num': "35", 'kicad_enum': "F.Paste",   'kts_dscr': "", 'kicad_dscr': ""}
            {'kicad_num': "36", 'kicad_enum': "B.SilkS",   'kts_dscr': "", 'kicad_dscr': "B.Silkscreen"}
            {'kicad_num': "37", 'kicad_enum': "F.SilkS",   'kts_dscr': "", 'kicad_dscr': "F.Silkscreen"}
            {'kicad_num': "38", 'kicad_enum': "B.Mask",    'kts_dscr': "", 'kicad_dscr': ""}
            {'kicad_num': "39", 'kicad_enum': "F.Mask",    'kts_dscr': "", 'kicad_dscr': ""}
            {'kicad_num': "40", 'kicad_enum': "Dwgs.User", 'kts_dscr': "", 'kicad_dscr': "User.Drawings"}
            {'kicad_num': "41", 'kicad_enum': "Cmts.User", 'kts_dscr': "", 'kicad_dscr': "User.Comments"}
            {'kicad_num': "42", 'kicad_enum': "Eco1.User", 'kts_dscr': "", 'kicad_dscr': "User.Eco1"}
            {'kicad_num': "43", 'kicad_enum': "Eco2.User", 'kts_dscr': "", 'kicad_dscr': "User.Eco2"}
            {'kicad_num': "44", 'kicad_enum': "Edge.Cuts", 'kts_dscr': "", 'kicad_dscr': ""}
            {'kicad_num': "45", 'kicad_enum': "Margin",    'kts_dscr': "", 'kicad_dscr': ""}
            {'kicad_num': "46", 'kicad_enum': "B.CrtYd",   'kts_dscr': "", 'kicad_dscr': "B.Courtyard"}
            {'kicad_num': "47", 'kicad_enum': "F.CrtYd",   'kts_dscr': "", 'kicad_dscr': "F.Courtyard"}
            {'kicad_num': "48", 'kicad_enum': "B.Fab",     'kts_dscr': "", 'kicad_dscr': ""}
            {'kicad_num': "49", 'kicad_enum': "F.Fab",     'kts_dscr': "", 'kicad_dscr': ""}
            {'kicad_num': "50", 'kicad_enum': "User.1",    'kts_dscr': "", 'kicad_dscr': ""}
            {'kicad_num': "51", 'kicad_enum': "User.2",    'kts_dscr': "", 'kicad_dscr': ""}
            {'kicad_num': "52", 'kicad_enum': "User.3",    'kts_dscr': "", 'kicad_dscr': ""}
            {'kicad_num': "53", 'kicad_enum': "User.4",    'kts_dscr': "", 'kicad_dscr': ""}
            {'kicad_num': "54", 'kicad_enum': "User.5",    'kts_dscr': "", 'kicad_dscr': ""}
            {'kicad_num': "55", 'kicad_enum': "User.6",    'kts_dscr': "", 'kicad_dscr': ""}
            {'kicad_num': "56", 'kicad_enum': "User.7",    'kts_dscr': "", 'kicad_dscr': ""}
            {'kicad_num': "57", 'kicad_enum': "User.8",    'kts_dscr': "", 'kicad_dscr': ""}
            {'kicad_num': "58", 'kicad_enum': "User.9",    'kts_dscr': "", 'kicad_dscr': ""}}
"""