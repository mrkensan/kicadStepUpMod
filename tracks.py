#!/usr/bin/python
# -*- coding: utf-8 -*-
#****************************************************************************

tracks_version = '1.1'

import kicad_parser
#import kicad_parser; import importlib; importlib.reload(kicad_parser)
import time
import PySide
from PySide import QtGui, QtCore
import sys,os
import FreeCAD, FreeCADGui
from  pcb_colors import *

logger = kicad_parser.FCADLogger('tracks')

global FC_export_min_version
FC_export_min_version="11670"  #11670 latest JM

global use_AppPart, use_Links, use_LinkGroups
use_AppPart=False # False
use_Links=False
use_LinkGroups = False

if 'LinkView' in dir(FreeCADGui):
    prefs = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/kicadStepUpGui")
    if prefs.GetBool('asm3_linkGroups'):
        use_LinkGroups = True
        use_Links=True #False
        #print('using \'LinkGroups\' and \'Links\'')
    elif prefs.GetBool('asm3_links'):
        use_Links=True #False
        #print('using \'Part\' container and \'Links\'')
    else:
        use_LinkGroups = False
        #print('using \'Part\' container')
else:
    use_LinkGroups = False
    #print('using \'Part\' container')
#
def getFCversion():
    FC_majorV=int(float(FreeCAD.Version()[0]))
    FC_minorV=int(float(FreeCAD.Version()[1]))
    try:
        FC_git_Nbr=int (float(FreeCAD.Version()[2].strip(" (Git)").split(' ')[0])) #+int(FreeCAD.Version()[2].strip(" (Git)").split(' ')[1])
    except:
        FC_git_Nbr=0
    return FC_majorV,FC_minorV,FC_git_Nbr

FC_majorV,FC_minorV,FC_git_Nbr=getFCversion()
if FC_majorV == 0 and FC_minorV == 17:
    if FC_git_Nbr >= int(FC_export_min_version):
        use_AppPart=True
#if FreeCAD.Version()[2] == 'Unknown':  #workaround for local building
#    use_AppPart=True
if FC_majorV > 0:
    use_AppPart=True
if FC_majorV == 0 and FC_minorV > 17:
    #if FC_git_Nbr >= int(FC_export_min_version):
    use_AppPart=True

current_milli_time = lambda: int(round(time.time() * 1000))

def get_run_time(start_time):
    end_milli_time = current_milli_time()
    running_time=(end_milli_time-start_time)/1000
    return running_time

def say_time(start_time):
    end_milli_time = current_milli_time()
    running_time=(end_milli_time-start_time)/1000
    msg="running time: "+str(running_time)+"sec"
    print(msg)
###

def reload_lib(lib):
    if (sys.version_info > (3, 0)):
        import importlib
        importlib.reload(lib)
    else:
        reload (lib)

def getTracksVersion():
    return tracks_version

def crc_gen_t(data):
    import binascii
    import re
    
    content=re.sub(r'[^\x00-\x7F]+','_', data)
    return u'_'+ make_unicode_t(hex(binascii.crc_hqx(content.encode('utf-8'), 0x0000))[2:])
##

def make_unicode_t(input):
    if (sys.version_info > (3, 0)):  #py3
        if isinstance(input, str):
            return input
        else:
            input =  input.decode('utf-8')
            return input
    else: #py2
        if type(input) != unicode:
            input =  input.decode('utf-8')
            return input
        else:
            return input


from kicadStepUptools import removesubtree, cfg_read_all
from kicadStepUptools import KicadPCB, make_unicode, make_string
TopLayer = 0
BotLayer = 31

# *************************************************************************
# Place new Copper Feature on PCB
#
def placeCopper(doc, renderedCu, deltaz, name, suffix, pcbThickness, cuThickness, layer):
    # Does the newly rendered copper have any features?

#    print(renderedCu)
    if not hasattr(renderedCu, "Shape"):
        logger.warning("Copper Layer '"+name+"' has no features.... skipping.")
        return
    
    # Make a copy we will work with
    doc.addObject('Part::Feature',name+suffix).Shape = renderedCu.Shape
    newCopper = doc.ActiveObject
    newCopper.Label=name+suffix

    # Add color to the newCopper object
    docG=FreeCADGui.ActiveDocument
    docG.ActiveObject.ShapeColor   = docG.getObject(renderedCu.Name).ShapeColor
    docG.ActiveObject.LineColor    = docG.getObject(renderedCu.Name).LineColor
    docG.ActiveObject.PointColor   = docG.getObject(renderedCu.Name).PointColor
    docG.ActiveObject.DiffuseColor = docG.getObject(renderedCu.Name).DiffuseColor
    docG.ActiveObject.DisplayMode  = 'Shaded'

    if layer==BotLayer:
        deltaz += pcbThickness + cuThickness
        deltaz = -deltaz

    # Move the newCopper feature off of the PCB surface as required for visibility
    #   Note movement distance is in negative direction for bottom layer
    newCopper.Placement = FreeCAD.Placement(FreeCAD.Vector(0,0,deltaz),FreeCAD.Rotation(FreeCAD.Vector(0,0,1),0))

    # Move the newCopper feature to the location the PCB is placed, if a PCB is present
    if len (doc.getObjectsByLabel('Pcb'+suffix)) >0:
        logger.info("Moving Tracks to PCB")
        newCopper.Placement = doc.getObject('Pcb'+suffix).Placement
        newCopper.Placement.Base.z += (deltaz)
        if len (doc.getObjectsByLabel('Board_Geoms'+suffix)) > 0:
            if use_AppPart and not use_LinkGroups:
                doc.getObject('Board_Geoms'+suffix).addObject(newCopper)
            elif use_LinkGroups:
                doc.getObject('Board_Geoms'+suffix).ViewObject.dropObject(newCopper,None,'',[])
    else:
        logger.warning("No PCB Found, Tracks are placed at origin")

    # Remove the passed-in Copper feature, we don't need it anymore
    FreeCADGui.Selection.clearSelection()
    FreeCADGui.Selection.addSelection(doc.getObject(renderedCu.Name))
    removesubtree(FreeCADGui.Selection.getSelection())

### 

# *************************************************************************
# Generate Copper Tracks for Top and Bottom Layers
#
def addtracks():
    global use_LinkGroups, use_AppPart
    import sys
    
    #FreeCAD.Console.PrintMessage('tracks version: '+getTracksVersion()+'\n')
    logger.info("***************** Generating Copper Layers *****************")
    
    # **********************************
    # User Selection of PCB File
    #    
    Filter=""
    pg = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/kicadStepUp")
    last_pcb_path = pg.GetString("last_pcb_path")
    if len (last_pcb_path) == 0:
            last_pcb_path = ""
    fname, Filter = PySide.QtGui.QFileDialog.getOpenFileName(None, "Open File...",
            make_unicode(last_pcb_path), "*.kicad_pcb")
    path, name = os.path.split(fname)
    filename = fname
 
    # **********************************
    # Start the process if a file was selected
    #
    if len(fname) > 0:
        start_time=current_milli_time()
        
        # **********************************
        # Record the selected filename in Prefs
        #        
        last_pcb_path=os.path.dirname(fname)
        path, ftname = os.path.split(fname)
        ftname=os.path.splitext(ftname)[0]
        ftname_sfx=crc_gen_t(make_unicode_t(ftname))
        pg = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/kicadStepUp")
        pg.SetString("last_pcb_path", make_string(last_pcb_path)) # py3 .decode("utf-8")

        # **********************************
        # Load PCB from file
        #
        mypcb = KicadPCB.load(filename)
        pcbThickness = float(mypcb.general.thickness)

        import kicad_parser; reload_lib(kicad_parser)
        pcb = kicad_parser.KicadFcad(filename)

        doc=FreeCAD.ActiveDocument
        if doc is None:
            doc=FreeCAD.newDocument(name)

        # **********************************
        # Read user prefs for board features
        #
        prefs = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/kicadStepUpGui")

        try:
            pcb_color_pref = prefs.GetInt('pcb_color')
        except:
            pcb_color_pref = 0  # Green
        
        try:
            minSizeDrill = float(prefs.GetString('drill_size')) # Match PCB Import Parameter
        except:
            minSizeDrill = 0.0  # Drill all holes found
        
        try:
            pcb_pad_pref = prefs.GetInt('Tracks_Cu_Finish')
        except:
            pcb_pad_pref = 0  # Render Bare copper
        
        try:
            pcb_copper_pref = prefs.GetInt('Tracks_Cu_Weight')
        except:
            pcb_copper_pref = 0  # Surface Only (no Thickness)
            
        pcb_color, trk_color, slk_color, color_name = GetPcbColors(pcb_color_pref)
        pad_thk, pad_color, pad_name = GetPadFinish(pcb_pad_pref)
        copper_thk, copper_name = GetCuWeight(pcb_copper_pref)
        
        logger.info("PCB Fabrication Parameters:")
        logger.info("    PCB Thickness: "+str(pcbThickness))
        logger.info("         Mask Color: "+color_name)
        logger.info("     Copper Finish: "+pad_name+" ("+str(1000*pad_thk)+"um)")
        logger.info("    Copper Weight: "+copper_name+" ("+str(1000*copper_thk)+"um)")
        logger.info(" ")
        
        # When rendering copper features, the pads must be "taller" (more in front)
        # of the copper tracks by at least some amount to be rendered correctly.
        # This means:
        # 1. When rendering pads the thickness of the copper is added to the
        #       thickness of the finish layer of the pads to get the full pad thickness.
        # 2. When the pad finish thickness is less than minimum, it is artifically
        #       inflated to at least minimum to allow it to be rendered (visually) correctly. 
        # 3. When 0oz copper is selected (implying just faces are created),
        #       we offset the pads object from the tracks to keep them "on top".
        # 
        # When pads and tracks are rendered as solids, they will be placed with 0 offset
        # from the surface of the PCB. However, when rendered as faces, they will be placed
        # with small offsets from the board surface (and each other, #3 above) so they are
        # rendered in a visually correct manner. 
        
        render_min_thk = 0.001  # 1 micron 
        
        if pcb_copper_pref == 0:  # Means we are rnedering only "Faces"
            logger.warning("Rendering as FACE")
            deltaz = render_min_thk # offsets between board, copper, and pads
            object_type = "face"    # Render features as Face objects (0 thickness)
            pad_thickness = 0.0
            track_thickness = 0.0
            zone_thickness = 0.0
        else:               # Render copper features as "Solids"
            if pad_thk < render_min_thk: pad_thk=render_min_thk # Inflate pads by minimum for visual rendering
            deltaz = 0                              # all copper features places on board surface, no offset
            object_type = "solid"                   # Render features as solids
            
            # Thickness here is important because it controls visualization
            #
            # Tracks are "thinnest" so they are "buried" in Zones and Pads
            # This setting means a Zone is rendered solidly, without artifacts
            # Pads are the thicker than both Tracks and Zones.
            # This is required to assure that "thermal features" of Zones don't obscure Pads
            track_thickness = copper_thk
            zone_thickness = copper_thk + render_min_thk           # This fixes poor rendering for colocated Tracks/Zones
            pad_thickness = pad_thk + copper_thk + render_min_thk  # Pads are thicker than all copper features
            
            # Set colors rendered by kicad_parser when making copper features
            #pcb.colors = {
            #   'board':ColorToFreeCad("0x3A6629"),
            #   'pad':{0:ColorToFreeCad(219,188,126)},
            #   'zone':{0:ColorToFreeCad('#147b9d')},
            #   'track':{0:ColorToFreeCad(26,157,204)},
            #   'copper':{0:ColorToFreeCad(200,117,51)},
            #}
        pcb.colors['track'][0] = ColorToFreeCad(trk_color)  # Set track color rendered in kicad_parser
        pcb.colors['zone'][0]  = ColorToFreeCad(trk_color)   # Set zone color rendered in kicad_parser
        pcb.colors['pad'][0]  = ColorToFreeCad(pad_color)   # Set zone color rendered in kicad_parser

        #def makePads(self, shape_type='face', thickness=0.05, holes=False, fit_arcs=True, prefix=''):
        #def makeTracks(self,shape_type='face',fit_arcs=True, thickness=0.05,holes=False,prefix=''):
        
        # **********************************
        # Generate Top Layer Copper
        #
        pcb.setLayer(TopLayer)
        
        # Pads
        offset = deltaz if not (object_type=="face") else (render_min_thk * 3)
        
        newFeature = pcb.makePads(holes=True, shape_type=object_type, thickness=pad_thickness, prefix="Top Layer: ")
        placeCopper(doc=doc, renderedCu=newFeature, deltaz=offset, name="TopPads", suffix=ftname_sfx,
                    pcbThickness=pcbThickness, cuThickness=pad_thickness, layer=TopLayer)
        
        # Tracks
        newFeature = pcb.makeTracks(holes=True, shape_type=object_type, thickness=track_thickness, prefix="Top Layer: ")
        placeCopper(doc=doc, renderedCu=newFeature, deltaz=deltaz, name="TopTracks", suffix=ftname_sfx,
                    pcbThickness=pcbThickness, cuThickness=track_thickness, layer=TopLayer)
        
        # Zones
        offset = deltaz if not (object_type=="face") else (render_min_thk * 2)
        
        newFeature = pcb.makeZones(holes=True, shape_type=object_type, thickness=zone_thickness, prefix="Top Layer: ")
        placeCopper(doc=doc, renderedCu=newFeature, deltaz=offset, name="TopZones", suffix=ftname_sfx,
                    pcbThickness=pcbThickness, cuThickness=zone_thickness, layer=TopLayer)
        
        # **********************************
        # Generate Top Bottom Copper
        #
        pcb.setLayer(BotLayer)
        
        # Pads
        offset = deltaz if not (object_type=="face") else (render_min_thk * 3)
        
        newFeature = pcb.makePads(holes=True, shape_type=object_type, thickness=pad_thickness, prefix="Bot Layer: ")
        placeCopper(doc=doc, renderedCu=newFeature, deltaz=offset, name="BotPads", suffix=ftname_sfx,
                    pcbThickness=pcbThickness, cuThickness=pad_thickness, layer=BotLayer)
        
        # Tracks
        newFeature = pcb.makeTracks(holes=True, shape_type=object_type, thickness=track_thickness, prefix="Bot Layer: ")
        placeCopper(doc=doc, renderedCu=newFeature, deltaz=deltaz, name="BotTracks", suffix=ftname_sfx,
                    pcbThickness=pcbThickness, cuThickness=track_thickness, layer=BotLayer)
        
        # Zones
        offset = deltaz if not (object_type=="face") else (render_min_thk * 2)
        
        newFeature = pcb.makeZones(holes=True, shape_type=object_type, thickness=track_thickness, prefix="Bot Layer: ")
        placeCopper(doc=doc, renderedCu=newFeature, deltaz=offset, name="BotZones", suffix=ftname_sfx,
                    pcbThickness=pcbThickness, cuThickness=zone_thickness, layer=BotLayer)
        
        msg = "MakeTracks: Run Time: "+str(get_run_time(start_time))+" Sec"
        logger.info(msg)

        FreeCADGui.SendMsgToActiveView("ViewFit")
        docG=FreeCADGui.ActiveDocument
        docG.activeView().viewAxonometric()
