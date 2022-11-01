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

# *************************************************************************
# Generate Copper Tracks for Top and Bottom Layers
#
def addtracks():
    global use_LinkGroups, use_AppPart
    import sys
    TopLayer = 0
    BotLayer = 31
    
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
        # Read user prefs for board features
        #
        prefs = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/kicadStepUpGui")

        try:
            pcb_color_pref = prefs.GetInt('pcb_color')
        except:
            pcb_color_pref = 0  # Green
        
        pcb_color, trk_color, slk_color, color_name = GetPcbColors(pcb_color_pref)
        #print ("Tracks Stats: ", pcb_color, trk_color, slk_color, color_name)
        
        try:
            minSizeDrill = float(prefs.GetString('drill_size')) # Match PCB Import Parameter
        except:
            minSizeDrill = 0.0  # Drill all holes found
        
        try:
            pcb_pad_pref = prefs.GetInt('Tracks_Cu_Finish')
        except:
            pcb_pad_pref = 0  # Render Bare copper
            
        pad_thk, pad_color, pad_name = GetPadFinish(pcb_pad_pref)
        
        try:
            pcb_copper_pref = prefs.GetInt('Tracks_Cu_Weight')
        except:
            pcb_copper_pref = 0  # Surface Only (no Thickness)
            
        copper_thk, copper_name = GetCuWeight(pcb_copper_pref)
        
        logger.info("PCB Fabrication Parameters:")
        logger.info("         Mask Color: "+color_name)
        logger.info("     Copper Finish: "+pad_name)
        logger.info("    Copper Weight: "+copper_name)
        logger.info(" ")
        

        # **********************************
        # Load PCB from file
        #
        mypcb = KicadPCB.load(filename)
        pcbThickness = float(mypcb.general.thickness)

        deltaz = 0.015 # 10 micron offset for copper from board surface

        import kicad_parser; reload_lib(kicad_parser)
        pcb = kicad_parser.KicadFcad(filename)
        
        
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
        

        # **********************************
        # Generate Top Layer Copper
        #
        pcb.setLayer(TopLayer)
        pcb.makePads(holes=True, shape_type='solid', prefix="Top Layer: ")
        #def makePads(self, shape_type='face', thickness=0.05, holes=False, fit_arcs=True, prefix=''):


        #pcb.makeCopper(holes=True, minSize=minSizeDrill, shape_type='face', prefix="Top Layer: ")
        doc=FreeCAD.ActiveDocument

        composed = doc.ActiveObject
        s = composed.Shape
        doc.addObject('Part::Feature','topTracks'+ftname_sfx).Shape=composed.Shape
        topTracks = doc.ActiveObject

        if 1:
    
                #print (doc.ActiveObject.Label)
                #print (topTracks.Label)
    
            docG=FreeCADGui.ActiveDocument
            docG.ActiveObject.ShapeColor   = docG.getObject(composed.Name).ShapeColor
            docG.ActiveObject.LineColor    = docG.getObject(composed.Name).LineColor
            docG.ActiveObject.PointColor   = docG.getObject(composed.Name).PointColor
            docG.ActiveObject.DiffuseColor = docG.getObject(composed.Name).DiffuseColor
    
            topTracks.Label="topTracks"+ftname_sfx
            topTracks.Placement = FreeCAD.Placement(FreeCAD.Vector(0,0,deltaz),FreeCAD.Rotation(FreeCAD.Vector(0,0,1),0))
    
            if len (doc.getObjectsByLabel('Pcb'+ftname_sfx)) >0:
                topTracks.Placement = doc.getObject('Pcb'+ftname_sfx).Placement
                topTracks.Placement.Base.z += (deltaz * 2)
                if len (doc.getObjectsByLabel('Board_Geoms'+ftname_sfx)) > 0:
                    if use_AppPart and not use_LinkGroups:
                        doc.getObject('Board_Geoms'+ftname_sfx).addObject(topTracks)
                    elif use_LinkGroups:
                        doc.getObject('Board_Geoms'+ftname_sfx).ViewObject.dropObject(topTracks,None,'',[])

            FreeCADGui.Selection.clearSelection()
            FreeCADGui.Selection.addSelection(doc.getObject(composed.Name))

        removesubtree(FreeCADGui.Selection.getSelection())
        
        msg = "Top Layer: Run Time: "+str(get_run_time(start_time))+" Sec"
        logger.info(msg)
        #say_time(start_time)

        if 0:
            # **********************************
            # Generate Bot Layer Copper
            #
            pcb.setLayer(BotLayer)
            pcb.makeCopper(holes=True, minSize=minSizeDrill)
            composed = doc.ActiveObject
            s = composed.Shape
            doc.addObject('Part::Feature','botTracks'+ftname_sfx).Shape=composed.Shape
            botTracks = doc.ActiveObject
            #print (doc.ActiveObject.Label)
            #print (topTracks.Label)
            docG.ActiveObject.ShapeColor   = docG.getObject(composed.Name).ShapeColor
            docG.ActiveObject.LineColor    = docG.getObject(composed.Name).LineColor
            docG.ActiveObject.PointColor   = docG.getObject(composed.Name).PointColor
            docG.ActiveObject.DiffuseColor = docG.getObject(composed.Name).DiffuseColor
            #doc.recompute()
            #doc.addObject('Part::Feature',"topTraks").Shape=s
            botTracks.Label="botTracks"+ftname_sfx
            botTracks.Placement = FreeCAD.Placement(FreeCAD.Vector(0,0,-1.6-deltaz),FreeCAD.Rotation(FreeCAD.Vector(0,0,1),0))            
            #if hasattr(doc.Pcb, 'Shape'):
            ##docG.getObject(botTracks.Name).Transparency=40
            if 0:
                docG.getObject(botTracks.Name).ShapeColor = (0.78,0.46,0.20)
            FreeCADGui.Selection.clearSelection()
            FreeCADGui.Selection.addSelection(doc.getObject(composed.Name))
            
            removesubtree(FreeCADGui.Selection.getSelection())
            #if hasattr(doc.Pcb, 'Shape'):
            if len (doc.getObjectsByLabel('Pcb'+ftname_sfx)) > 0:
                botTracks.Placement = doc.getObject('Pcb'+ftname_sfx).Placement
                #botTracks.Placement = doc.Pcb.Placement
                botTracks.Placement.Base.z-=pcbThickness+deltaz
                if len (doc.getObjectsByLabel('Board_Geoms'+ftname_sfx)) > 0:
                    if use_AppPart and not use_LinkGroups:
                        doc.getObject('Board_Geoms'+ftname_sfx).addObject(botTracks)
                    elif use_LinkGroups:
                        doc.getObject('Board_Geoms'+ftname_sfx).ViewObject.dropObject(botTracks,None,'',[])
            #botTracks = FreeCAD.ActiveDocument.ActiveObject
            #botTracks.Label="botTracks"
            #botTracks.Placement = FreeCAD.Placement(FreeCAD.Vector(0,0,-1.6),FreeCAD.Rotation(FreeCAD.Vector(0,0,1),0))    
            #docG.ActiveObject.Transparency=40
            #except Exception as e:
            #    exc_type, exc_obj, exc_tb = sys.exc_info()
            #    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            #    FreeCAD.Console.PrintError('error class: '+str(exc_type)+'\nfile name: '+str(fname)+'\nerror @line: '+str(exc_tb.tb_lineno)+'\nerror value: '+str(e.args[0])+'\n')
            say_time(start_time)
        
        FreeCADGui.SendMsgToActiveView("ViewFit")
        #docG.activeView().viewAxonometric()
