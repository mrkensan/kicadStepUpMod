#!/usr/bin/python
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
#*   code partially based on:                                               *
#*      Printed Circuit Board Workbench for FreeCAD  FreeCAD-PCB            *
#*      Copyright (c) 2013, 2014, 2015                                      *
#*      marmni <marmni@onet.eu>                                             *
#*                                                                          *
#*      and IDF import for FreeCAD                                          *
#*      (c) Milos Koutny (milos.koutny@gmail.com) 2012                      *
#*      and (c) hyOzd ecad-3d-model-generator                               *
#*                                                                          *
#*   this macro rotates, translates and scales one object                   *
#*   scale for VRML export and open footprint for easy alignment            *
#*   this sw is a part of kicad StepUp code                                 *
#*   all credits and licence details in kicad StepUp code                   *
#*   Macro_Move_Rotate_Scale                                                *
#*   ver in ___ver___                                                       *
#*     Copyright (c) 2015, 2016, 2017                                       *
#*     Maurice easyw@katamail.com                                           *
#*                                                                          *
#*     Collisions routines from Highlight Common parts Macro                *
#*     author JMG, galou and other contributors                             *
#*     from FreeCAD OpenSCAD Workbench - 2D helper functions                *
#*     __author__ = "Sebastian Hoogen"                                      *
#*                                                                          *
#*     semantic parser from __author__ = "Zheng, Lei"  fcad_pcb             *
#*                                                                          *
#* IDF_ImporterVersion="3.9.2"                                              *
#*  ignoring step search associations (too old models)                      *
#*  displaying Flat Mode models                                             *
#*  checking version 3 for both Geometry and Part Number                    *
#*  supporting Z position                                                   *
#*  skipping PROP in emp file                                               *
#*  adding color to shapes opt IDF_colorize                                 *
#*  adding emp library/single model load support                            *
#*  aligning IDF shape to both Geom and PartNBR for exactly match           *
#*  to do: .ROUTE_OUTLINE ECAD, .PLACE_OUTLINE MCAD,                        *
#*         .ROUTE_KEPOUT ECAD, .PLACE_KEEPOUT ECAD                          *
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

##With kicad StepUp you’ll get an exact representation of your physical board in Native 3D PCB

## kicad StepUp tools
##done
# upgrade kicadstepup version
# resized font size
# add bbox and volume images on the starter guide
# add ksu config more detailed description
# complete volume_minimum config in doc
# improved OSX QtGui File Open
# better arc and line import
# remove test button
# enable confirm on exit
# replace FreeCAD.Console.Message -> say 
##todo list
# collision and proximity as microelly
## kicad StepUp
# added messages on missing emn files
# added messages on missing models
# added path to adapt your KISYS3DMOD
# added blacklist for unwanted modules
# added messages on blacklisted modules
# added pcb color attribute
# added bounding box option
# added bounding box white list to leave real model on connector or peripheral models
# added auxorigin, base origin, base point placement option
# added vrml models z-rotation angle
# added virtual models option
# added fusion export option
# added saving in native format, export to STEP
# added arcs and circles for calculate board position
# added idf_to_origin flag for version >6091
# added reset properties for FC 016 bug
# added ${KIPRJMOD} support
# added v3,v4 pcb version support
# added multi 3D vrml model support
# added compatibility to kicad version >=3
# added auto color assigning in bboxes
# added minimum volume per model
# added minimum height per model
# updated findPcbCenter method
# added support for .stp extension beside .step
# added support for .igs extension beside .step
# added support for .iges extension beside .step
# because of hole sovrapposition prob...
# cutting hole by hole instead of hole compound
# added holes_solid var
# to have holes as solid to guarantee cutting
# handled single circle 
# used OpenSCAD2Dgeom instead of wire + face (best option)
# http://www.freecadweb.org/wiki/index.php?title=Macro_Creating_faces_from_a_DXF_file
# fixed unicode text parsing
# double option .kicad_pcb .emn
# in case of non coincidences .emn is more tolerant
# try to build wires on closed shaped for make the cutting faster
# try to optimize cutting changing creation/type of holes
# manage bklist and volume
# accept with or without /\ at the end of 3Dpath
# search models in KIPRJMOD and in KISYS3DMOD 
# removed unicode chars in .kicad_pcb
# exported wrl, step from python
# reload & display ini cfg file
# display/edit ini file with syntax highlight
# msg first ksu config
# added warning for import step multi part fixed v3035
# commented warning in load footprint and in placing step mod if x,y are different from 0 0 0
# added message if scale are different from 1 1 1
# non stopping warning for footprint
# added command line args to load board(/emn)
# avoid argv in memory in case of opened from  command line
# used multi cut also for footprint too
# enabled loadB, loadI, loadF with filename=None to align Mod and Macro
# enabled Macro & Mod
# added ico tools info
# added checkbox export_2_step
# added export2STEP var in ini file
# subst print to say
# fixed cursor wait
# angle on pads for footprint pads angle i.e. DB25M_V ok
# improved multipart load checking
# added virtual checkbox
# added VRML with material properties exporter
# added metal grey material
# added multipart VRML option
# improved export resolution from %.3f, %.5f to %g
# added config for material props
# pad & holes as circles when possible
# improved multipart load checking
# removed illegal characters in filenames when exporting VRML and STEP
# message of missing models at the end
# implemented caching for 3D models
# optimized for fusion w/ colors
# added support for alias i.e. :Kicad3D: as for environment variables
# added crease angle for wrl export 
# added support for ${KISYS3DMOD}/ in new 3d viewer path resolver
# accepting .wrl .step .stp .iges .igs as 3d models directly in kicad_pcb
# added fixedPosition for aligning part to footprint in assembly2
# message if scale values are not assigned to 1 1 1
# added support for wrl offset in position & rotation when loadboard
# added bbox creation based on scaled values (1mm as base unit)
# added height and volume blacklist for scaled shapes
# added error message in case of scale factor not 1:1 for non scaled box
# fixed base point for lower case settings
# added single instance
# added open file type 'rb' 'ab' and write file 'wb' type binary for utf8 full support
# added fix to rect pads in footprint loader
# non blocking warning only for scale <> 1
# fixed minor issues in FC015 loading fp
# added models3Dprefix as default saving location
# added $HOME support for unix systems (it doesn't resolve on win)
# added OCC >=7 FC 0.17 compatibility for Footprint pads, lines, arcs
# added check if the models3Dprefix is writable, otherwise will write on $HOME
# added 2nd path to resolver prefix3d_2
# added wrl materials dialog theme compatibility
# reduced export file size
# accept the new Part.LineSegment using yorik help function FC 0.17 >= 9123
# EdgeCuts for footprint will generate a path on FP loader
# EdgeCuts in footprint will generate Cuts in Board
# accepted utf8 for model in kysys3mod or alias
# checked spaces in name
# added edge tolerance on vertex coincidence
# added /n to say() and removed extra /n in each say msg
# removed print in all doc ()<print "here  ... etc
# removed unnecessary messages (when non coincident edges)
# removed extra messages helping debug
# fixed edge tolerance on FC 017 >9255
# message when adjusting edges
# animation when assembled
# moved config read-write to my own method for full utf-8 support
# accept utf8 on 3D prefix path
# accept utf8 on saving loading last path
# tidy up a bit the utf-8 code
# regenerate ksu-config if too short
# enabled upper case on config
# added message on edge not coincident
# added turntable section
# added 'no layers' for pads
# allowed STEP multipart (creating compound)
# added exception on import step model
# added better theme integration
# improved tolerance on edges <0.005 #edge coincidence tolerance (5000nm = 1/2 centesimo) base is mm
# updated import IDF mod
# added font size in config
# added improved way to load step files as compound from vejmarie
# accepted lower and upper case for extension (linux is case sensitive os)
# added align_vrml_step_colors when saving with material properties
# assigned shininess and specular color for single color Shapes
# fixed position for rotated fp-modules with offset
# fixed position for all rotation and offset
# fixed edge cuts for bottom modules
# fixed circle in circle edges
# added tolerance warning > 1e-6 #(1nm) base is mm
# substituted  (== None) -> (is None)
# disabling VBO during loading modules to avoid crashing (new bug from 0.17 after 10101)
# disabling Part-o-Magic observer if exists (not possible without calling the PoM function)
# added full unicode support for names in compounds
# removed activateWorkbench("PartWorkbench") if Assembly2 is active
# added Glass materials to exporting
# added virtual parts skipped message
# added recursive App::Part single copy (thx nico!) to compatibility with FC > 10647
# implemented App::Part also for moving/rotating obj and exporting model
# added support for opening footprints kicad_mod from command line
# disabling VBO during loading footprints to avoid crashing (new bug from 0.17 after 10101)
# removed IDF import
# removed Move X,Y,Z buttons
# resetP always enabled
# collision cb, virtual cb, expstep cb, reset placement cb, setGeometry
# textEdit -> textBrowser for html links to tutorials
# link to local config file on disk
# moved to icon based GUI
# minor dock fixing
# temporary_undock to enable dock left & right memory on edit/help
# fusion & compound buttons (App::Part compatible)
# handling bad fusion redirect to compound
# added toggle on minimize button
# fixed Qt5 OSX issues
# removed App. changed to FreeCAD in remaining instances
# fixed App::Part relative placement
# started moving toward compatibility to py3
# small fix to avoid VRML selection when exporting
# added pcb colors for exporting
# fixed bug on multiple mixed models per footprint position/rotation
# compatibility py3
# added Step_Virtual_Models folder for mechanical parts
# added workaround for "bug for ImportGui *.iges" -> using "Part.insert"
# cleaned License for App::Part containers (.License .LicenseURL)
# added warning_nbr in case of too many missing models
# added reset placement before exporting wrl & STEP model
# added warning in case of drill and volume used in config
# added ReadShapeCompoundMode parameter for step import shapes with colors on LoadBoard and (+)Import Step
# added ReadShapeCompoundMode var also when (+) importing step models
# added force_oldGroups to force old method if set to True
# use_AppPart instead of Groups for FC0.17 > FC_export_min_version="11670"
# managed Export2MCAD for exporting hierarchy and not if fused selected
# added semantic parser to speed up .kicad_pcb parsing up to 70 times faster for pcb loading
# added Top & Bottom containers for STEP models
# added allow_compound mode 'simplify' to enable fast loading (losing colors)
# removing empty Top/Bot containers after loading models (only on FC 0.17)
# added relative 3d path '../'
# added F.Fab F.CrtYd to loadFootprint function
# added StepUp WorkBench
# fixed utf-8 str to Label
# recurse placement for Collision check ['Placement.multiply']: now it works also with App::Part, Body & Compound in FC0.17
# added links to pdf files in Help
# added config value for autoconstraints in sketcher
# auto constraint coincident points and vertical/horizontal
# some cleaning on warn messages for wrong scale, missing models
# boost in cutting drills
# added sketch button
# started experimental Sketch support
# improve help and add sketch functionality
# auto constraint coincident points and vertical/horizontal
# edge_width from kicad_pcb
# managed not supported geometry BSplines & Ellipses with optimized deviation   # loop in App.ActiveDocument.PCB_Sketch.Geometry searching for coincident vertex 
# aligned Sketch to center of A4 in pcbnew if first time 
# removing sketches from export 3d to step button
# removing sketches in FC0.16 and when exporting automatically
# added use grid_origin as reference point for placing the board and for sketch!!!
   # this will allow to copy sketches between boards releases to keep constraints
# managed write permissions error message
# fixed App::Part list inverted after FC 12090 https://github.com/FreeCAD/FreeCAD/pull/916
# fixed case of pcb with one drill only
# minor fix when exporting wrl from multi objects 
# fixed tabify
# added better support for Body (hidden Parts)
# fixed a regression in Sketch
# fixed Sketch inverted
# converted Bspline to Arcs https://github.com/FreeCAD/FreeCAD/commit/6d9cf80
# fixed Arc orientation when creating Sketch from dxf,svg
# improved FC0.16 compatibility
# aligned GridOrigin also in case of Sketch copy/paste from empty board
# aligned pushing pcb to GridOrigin from empty Sketch/Board (only GridOrigin set)
# removed draftify bugged function
# added support for arc of 360 deg
# added oval exception if only one value is done
# starting py3 compatibility
# added offset in mm after kicad_pcb version 20171114
# moved edgestofaces to internal function
# fixed ellipses
# added new materials
# improved bspline to arcs
# started footprint exporter (smd [rect, oval, circle])
# added Round Rectangles and Poly Lines (for RF design)
# simple copy button added
# improved TH, NPTH and SMD pads
# bspline allowed on footprint F_Silks
# solder Mask Zones for Polylines
# ZLength for BBox height
# added Check for Solid property
# skipped Points in geometry of sketch
# added loading pad poly in fp
# fixed simplify sketch
# improved Qt5 compatibility
# added workaround for STEP exporting OCC 7.2.0
# improved STEP exporting with hierarchy, onelevel, flat options
# added QtGui.QApplication.processEvents() for Qt5
# skipping \" characters
# added 'links' for import mode settings
# moved the generation of PCB inside the Sketch to Face process
# adding Geometry and Constraints as a single instruction to avoid long delay with sketches
# added Constrainator
# allowed ArcOfCircle for Polyline Pads
# roundrect pads for import footprint supported
# assigned combobox to defined colors
# improved generation of complex footprint with arcs
# partially implemented Circle Geometry primitive
# improved writing fp data 
# push Moved 3D model(s) to kicad PCB
# sync Reference in case of lost correct Label (import export STEP file with Links)
# improved precision on board data using "{:.3f}".format for pushpcb & Pushfootprint and angles
# re-introduced ability to use footprints with edge cuts inside
# restored ability to load pcb edge from footprint instead of Sketch
# added option (not used) to simplify compsolid to solid
# added support for pcb reading gr_poly on Edge.Cuts
# improved fp parsing for custom geo
# improved fp parsing for custom geo again
# first implementation of bspline edge import (TBD: spline w control points, push to pcb)
# pushpcb working with gr_curves, downgrading to arcs and lines (TBD: use spline)
# spline w control points
# fixing pushing pcb
# adding support for double quotes on kicad_pcb and kicad_mod format
# bsplines allowed for push&pull kicad_pcb
# fixed freezing issue on AppImages (thread)
# improved simplify sketch
# workaround force saving before exporting VRML (win freeze bug)
# importing custom Geo also for bottom layer
# fixed wbs ordering
# added edges2sketch function
# local coordinate system reference added
# improved search for 3d models on local path without using KIPRJMOD
# initial support for App::Link & App::LinkGroup
# added 3d model position pull&push update
# added Sketches pull&push update
# added 'stpZ', 'wrz' compressed files support
# hide main kSU dialog unless when opening a footprint model
# full import of kicad_pcb allowed
# generating uid for pcb & containers
# pcb as solid (removed compsolid)
# applying transparency in case of LED or GLASS material found in wrl/wrz file model
# most clean code and comments done

##todo

## collaps the App::LinkGroups at the end of loading
## multi-board compatibility with asm3 A3
## check "{:.3f}".format for pushpcb & Pushfootprint
## check utf-8 directories and spaces compatibility

## add edit and help to WB menu (self unresolved)
## copy objects and apply absolute placement to each one, then check collisions
## remove print and makesketch

## remove print say etc, remove shape show, remove extra import, remove extra functions FC_016
## App -> FreeCAD

# done: allow bspline on fp generator 
# done: completing py3 compatibility

## started to implement isInside using bboxes to check if drills are nested, and then
##    use dxf2face to extrude pcb instead of actual cutting (it should be much faster again)
##    or use a python feature as in pcb for having the board updated live
## approximate arcs from segments https://www.freecadweb.org/wiki/Macro_EdgesToArc

## add AP214-203 settings read,set,restore both on step-step(h) 
##    when exporting step and step+wrl
## ... there is a mess in Tool variables after jm pr910
## use float in all data from semantic parser  !!!!!
## export AppPart groups in a single STEP file with hierarchy also when fuseall is selected

## evaluate to add comment line and behavior for font_size = 0 for default size
## evaluate makeCompound as comment line and option beside fuseAll (not useful)
## check basepoint 
## simplify pdf manual and update internal help
## assign shininess and specular color for faces? available?
## adding top bottom lights

## load local config if exists
## add transp 25 50 75 to asis in exp wrl or keep transp ?

### knowing issues
## VBO with multipart crash on loading parts -> disabled when loading
## Part-oMagic trigs errors on loading parts -> disabled when loading
# none atm :)

# use isInside/common ( TopoShape ) to cut only intersection objs
# multi board
# test option placement
# check line 772 abs ZMax = height? -> ZLength
# fix fonts for html and new buttons
# ...
# respect transparency on shapes NOT possible on STEP objects because of FC
# pad type trapez, rect rounded


## import statements

import FreeCAD,FreeCADGui,Part,Mesh
#import PySide
from collections import namedtuple

import PySide
from PySide import QtGui, QtCore

from time import sleep
from math import sqrt, tan, atan, atan2, degrees, radians, hypot, sin, cos, pi, fmod
import Draft, Part, DraftVecUtils
#from Draft import *
from FreeCAD import Vector
import Sketcher

from collections import namedtuple
from FreeCAD import Base
import sys, os
from os.path import expanduser
import shutil
from shutil import copyfile
import tempfile, errno
import re
import time

import kts_Locator

# This is where we are putting the small "helper" functions
from kts_Utils import *


if (sys.version_info > (3, 0)):  #py3
    import builtins as builtin  #py3
    import gzip as gz
else:  #py2
    import __builtin__ as builtin #py2
    try:
        import gzip_utf8 as gz
    except:
        FreeCAD.Console.PrintError("'.stpZ' not supported")
        pass

import zipfile  as zf
# sys.path.append('C:\Cad\Progetti_K\3D-FreeCad-tools/')
#sys.path.append(os.path.realpath(__file__)) #workaround to test OpenSCAD2DgeomMau
#import OpenSCAD2DgeomMau #
#reload(OpenSCAD2DgeomMau)
#import OpenSCAD2Dgeom
import ImportGui
from math import sqrt, atan, sin, cos, radians, degrees, pi

import argparse
from threading import Timer

#try:
#    import __builtin__ as builtin #py2
#except:
#    import builtins as builtin  #py3

if FreeCAD.GuiUp:
    from PySide import QtCore, QtGui

# import OpenSCADFeatures
import DraftGeomUtils
#from DraftGeomUtils import *

from pivy.coin import SoDirectionalLight

import codecs #utf-8 config parser
import io
#import configparser #utf-8
#from codecs import open #maui to verify
import unicodedata

pythonopen = builtin.open # to distinguish python built-in open function from the one declared here

## Constant definitions
___ver___ = "10.7.6"
__title__ = "kicad_StepUp"
__author__ = "maurice & mg"
__Comment__ = 'Kicad STEPUP(TM) (3D kicad board and models exported to STEP) for FreeCAD'
___ver_ksu___ = "4.1.3.0  April 2017" 
___ver_GUI___ = "ksu-docked-v3.2"
IDF_ImporterVersion="3.9.2"
__Icon__ = "stepup.png"


global userCancelled, userOK, show_mouse_pos, min_val, last_file_path, resetP
global start_time, show_messages
global show_messages, applymaterials
global real_board_pos_x, real_board_pos_y, board_base_point_x, board_base_point_y
global ksu_config_fname, ini_content, configFilePath
global models3D_prefix, models3D_prefix2, models3D_prefix3, models3D_prefix4
global blacklisted_model_elements, col, colr, colg, colb
global bbox, volume_minimum, height_minimum, idf_to_origin, aux_orig
global base_orig, base_point, bbox_all, bbox_list, whitelisted_model_elements
global fusion, addVirtual, blacklisted_models, exportFusing, min_drill_size
global last_fp_path, last_pcb_path, plcmnt, xp, yp, exportFusing, exportS
global full_placement, shape_col, align_vrml_step_colors
global timer_Collisions, last_3d_path, expanded_view, mingui
global textEdit_dim_base, textEdit_dim_hide #textEdit dimensions for hiding showing text content
global warning_nbr, original_filename, edge_width, load_sketch, grid_orig, dvm, pt_osx, pt_lnx, dqd, running_time
global addConstraints, precision, conv_offs, maxRadius, pad_nbr, use_pypro, accept_spline, maxDegree, maxSegments
global zfit

zfit = False

maxRadius = 500.0 # 500mm maxRadius of arc from bspline
pad_nbr = 1 #first nbr of fp pads
use_pypro = False #False #enable/disable timestamp as python property; False=disabled -> use the Label
accept_spline = True # include spline in PCB_Sketch for KiCAD >= v5.1
maxDegree = 3 # spline degree for KiCAD integration
maxSegments = 999 #for splines

conv_offs = 1.0 #conversion offset from decimils to mm pcb version >= 20171114
original_filename=""
edge_width = None
load_sketch=True 
dvm = 3.0 # obsolete: discretizer multiplier factor
dqd = 0.02 #discretize(QuasiDeflection=d) => gives a list of points with a maximum deflection 'd' to the edge (faster)
precision = 0.1 # precision in spline or bezier conversion
pt_osx=False #platform OSX
pt_lnx=False #platform Linux
running_time = 0
warning_nbr=10 #if missing more than 'warning_nbr' models, a warning will raise
               #set to -1 for skipping the test

timer_Collisions= 3000 # ms
mingui = 0 #Gui status: mingui = 1 -> minimized
last_3d_path=u''
expanded_view=0 # 0=not expanded; 1 edit expanded; 2 help expanded
shape_col=(1.0, 0.0, 0.0)
align_vrml_step_colors=True

textEdit_dim_base=(176,36,305,453) #default value
textEdit_dim_hide=(30000,30000,0,0) #hide value fake position

last_pcb_path=u'' #py3
exportS=True
last_file_path=''
pcb_path =u''
resetP=True
global rot_wrl, test_flag, test_flag_pads
rot_wrl=0.0
#global module_3D_dir
userCancelled        = "Cancelled"
userOK            = "OK"
show_mouse_pos = True
#module_3D_dir="C:/Cad/Progetti_K/a_mod"
min_val=0.001
conflict_tolerance=1e-6  #volume tolerance
#edge_tolerance=0.005 #edge coincidence tolerance (5000nm = 1/2 centesimo) base is mm
edge_tolerance=0.01 #edge coincidence tolerance (500nm = 0.1 decimo) base is mm
edge_tolerance_warning = 1e-6 #(1nm) base is mm
apply_edge_tolerance = False #True
simplifyComSolid = False #True  this can be quite time consuming

font_size=8
bbox_r_col=(0.411765, 0.411765, 0.411765)  #dimgrey
bbox_c_col=(0.823529, 0.411765, 0.117647)  #chocolate
bbox_x_col=(0.862745, 0.862745, 0.862745) #gainsboro
bbox_l_col=(0.333333, 0.333333, 0.333333) #sgidarkgrey
bbox_IC_col=(0.156863, 0.156863, 0.156863)  #sgiverydarkgrey
bbox_default_col=(0.439216, 0.501961, 0.564706)  #slategrey
mat_section=u"""
[Materials]
mat = enablematerials
;; VRML models to be or not exported with material properties
;mat = enablematerials\n;mat = nomaterials
"""
dock_section=u"""
[docking]
dkmode = float
;;docking mode
;dkmode = left
;dkmode = right
;dkmode = float
"""
turntable_section=u"""
[turntable]
spin = enabled
;;turntable spin after loading
;spin = disabled
;spin = enabled
"""
compound_section=u"""
[compound]
compound = allowed
;;allow compound for STEP models
;compound = allowed
;compound = disallowed
;compound = simplified
"""
constraints_section=u"""
[sketch_constraints]
constraints = all
;constraints = all
;constraints = coincident
;constraints = none
;;constraints generated for pcb sketch
"""
exporting_mode_section=u"""
[step_exporting_mode]
exporting_mode = hierarchy
;exporting_mode = hierarchy
;exporting_mode = flat
;exporting_mode = onelevel
;;step exporting mode 
"""

font_section=u"""
[fonts]
font_size = 8
;;font size for ksu widget
"""

links_importing_mode_section=u"""
[links_importing_mode]
importing_mode = standard
;importing_mode = links
;importing_mode = standard
;;models importing mode: use Assembly3 Links or Standard mode
"""

global ini_vars, num_min_lines
ini_vars=[]
for i in range (0,20):
    ini_vars.append('-')
num_min_lines=22 #min numbers of ini lines for a ksu-config file

#FreeCAD.Console.PrintError(len(ini_vars))
#FreeCAD.Console.PrintWarning('\n')

test_flag=False
#test_flag=True
test_flag_pads=False #True 4 testing
remove_pcbPad=True #False 4 testing
close_doc=False

show_border=False #False
show_data=False #False
show_debug=False #False

show_shapes=False #False
disable_cutting=False
# enable_materials=True not used
test_extrude=False #False
holes_solid=False #False
emn_version=3.0
show_messages=True #False 4 testing
#show_messages=False # mauitest
full_placement=True  # for offset in xyz and rotation in xyz
# FreeCAD.Console.PrintWarning(full_placement)
# FreeCAD.Console.PrintWarning('\n')

global disable_VBO
disable_VBO = True # False to test crash
if disable_VBO == False:
    FreeCAD.Console.PrintWarning("VBO check disabled\n")
global disable_PoM_Observer
disable_PoM_Observer = False
try:
    import PartOMagic
    import PartOMagic.Gui.Observer as Observer
    disable_PoM_Observer = True
    FreeCAD.Console.PrintWarning("PoM present\n")
except:
    FreeCAD.Console.PrintWarning("PoM not present\n")

##
#!#def say_inline(msg):
#!#    FreeCAD.Console.PrintMessage(msg+' ')
#!#
#!#def say(msg):
#!#    FreeCAD.Console.PrintMessage(msg)
#!#    FreeCAD.Console.PrintMessage('\n')
#!#
#!#def sayw(msg):
#!#    FreeCAD.Console.PrintWarning(msg)
#!#    FreeCAD.Console.PrintWarning('\n')
#!#    
#!#def sayerr(msg):
#!#    FreeCAD.Console.PrintError(msg)
#!#    FreeCAD.Console.PrintMessage('\n')
##

global use_AppPart, use_Links, use_LinkGroups
use_AppPart=False # False
use_Links=False

use_LinkGroups = False
if 'LinkView' in dir(FreeCADGui):
    prefs = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/kicadStepUpGui")
    if prefs.GetBool('asm3_linkGroups'):
        use_LinkGroups = True
        use_Links=True #False
        sayw('using \'LinkGroups\' and \'Links\'')
    elif prefs.GetBool('asm3_links'):
        use_Links=True #False
        sayw('using \'Part\' container and \'Links\'')
    else:
        use_LinkGroups = False
        sayw('using \'Part\' container')
else:
    use_LinkGroups = False
    sayw('using \'Part\' container')
#
global FC_export_min_version
FC_export_min_version="11670"  #11670 latest JM

def ZoomFitThread():
    FreeCAD.Console.PrintWarning('thread ViewFitting\n')
    if FreeCAD.ActiveDocument is not None:
        FreeCADGui.SendMsgToActiveView("ViewFit")
    #stop

#!#def collaps_Tree():
#!#   FreeCAD.Console.PrintWarning('thread Collapsing\n')
#!#   if FreeCAD.ActiveDocument is not None:
#!#       mw1 = FreeCADGui.getMainWindow()
#!#       treesSel = mw1.findChildren(QtGui.QTreeWidget)
#!#       for tree in treesSel:
#!#           items = tree.selectedItems()
#!#           for item in items:
#!#               if item.isExpanded() == True:
#!#                   collapse = True
#!#                   print ("collapsing")
#!#                   tree.collapseItem(item)
#!#   FreeCADGui.Selection.clearSelection()
#

##--------------------------------------------------------------------------------------
py2=False
try:  ## maui py3
    unicode = unicode
except NameError:
    # 'unicode' is undefined, must be Python 3
    str = str
    unicode = str
    bytes = bytes
    basestring = (str,bytes)
else:
    # 'unicode' exists, must be Python 2
    str = str
    unicode = unicode
    bytes = str
    basestring = basestring
    py2=True

def isConstruction(geo):
    if hasattr(geo,'Construction'):
        return geo.Construction
    else:
        if 'geometryModeFlags="00000000000000000000000000000010"/>' in geo.Content:
            return True
        else:
            return False
#

PY3 = sys.version_info[0] == 3  # maui @realthunder fcad_pcb py3
if PY3:
    string_types = str,
else:
    string_types = basestring,

###
# sexp
# maui
import fcad_parser
from fcad_parser import KicadPCB,SexpList
import kicad_parser

###
def rotatePoint(r,sa,da,c):
    # sa, da in degrees
    x = c[0] - cos(radians(sa+da)) * r
    y = c[1] - sin(radians(sa+da)) * r
    return [x,y]
###
def getFCversion():

    FC_majorV=int(float(FreeCAD.Version()[0]))
    FC_minorV=int(float(FreeCAD.Version()[1]))
    try:
        FC_git_Nbr=int (float(FreeCAD.Version()[2].strip(" (Git)").split(' ')[0])) #+int(FreeCAD.Version()[2].strip(" (Git)").split(' ')[1])
    except:
        FC_git_Nbr=0
    return FC_majorV,FC_minorV,FC_git_Nbr

FC_majorV,FC_minorV,FC_git_Nbr=getFCversion()
FreeCAD.Console.PrintWarning('FC Version '+str(FC_majorV)+str(FC_minorV)+"-"+str(FC_git_Nbr)+'\n')    
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
#if use_AppPart:
#    FreeCAD.Console.PrintWarning("creating hierarchy\n")
if int(FC_majorV) <= 0:
    if int(FC_minorV) == 15:
        load_sketch=False
        
global force_oldGroups
force_oldGroups=False # False

try:
    from freecad.asm3 import assembly as asm
    #use_Links=True #False
    FreeCAD.Console.PrintWarning('Asm3 WB present\n')
except:
    pass
    #FreeCAD.Console.PrintWarning('Asm3 WB not present\n')

global export_board_2step
#export_board_2step=False
save_temp_data=False
global ignore_utf8
ignore_utf8=False
global ignore_utf8_incfg
ignore_utf8_incfg=True
global animate_result
animate_result=True #False turntable
global allow_compound
allow_compound='False' #allow compound in ksu

global apply_reflex
apply_reflex=True #True adds shininess for Single Color Shapes valid ONLY if turntable is enabled
global apply_reflex_all
apply_reflex_all=False #True not suggested wip simulate shininess for faces
global force_transparency
force_transparency = False #True for testing wip

global apply_light
apply_light=False #True not suggested wip add light up and down

# disabling pcurves
paramGet = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/Part/General")
paramGet.SetInt("WriteSurfaceCurveMode", 0)

current_milli_time = lambda: int(round(time.time() * 1000))

Materials=True
## "PIN-01";"metal grey pins"
## "PIN-02";"gold pins"
## "IC-BODY-EPOXY-04";"black body"
## "RES-SMD-01";"resistor black body"
## "IC-BODY-EPOXY-01";"grey body"
## "CAP-CERAMIC-05";"dark grey body"
## "CAP-CERAMIC-06";"brown body"
## "PLASTIC-GREEN-01";"green body"
## "PLASTIC-BLUE-01";"blue body"
## "PLASTIC-WHITE-01";"white body"
## "IC-LABEL-01";"light brown label"
## LED-GREEN, LED-RED, LED-BLUE

as_is=""

metal_grey_pins="""material DEF PIN-01 Material {
        ambientIntensity 0.271
        diffuseColor 0.824 0.820 0.781
        specularColor 0.328 0.258 0.172
        emissiveColor 0.0 0.0 0.0
        shininess 0.70
        transparency 0.0
        }"""
        
# http://vrmlstuff.free.fr/materials/
metal_grey="""material DEF MET-01 Material {
        ambientIntensity 0.249999
        diffuseColor 0.298 0.298 0.298
        specularColor 0.398 0.398 0.398
        emissiveColor 0.0 0.0 0.0
        shininess 0.056122
        transparency 0.0
        }"""
    
gold_pins="""material DEF PIN-02 Material {
        ambientIntensity 0.379
        diffuseColor 0.859 0.738 0.496
        specularColor 0.137 0.145 0.184
        emissiveColor 0.0 0.0 0.0
        shininess 0.40
        transparency 0.0
        }"""

black_body="""material DEF IC-BODY-EPOXY-04 Material {
        ambientIntensity 0.293
        diffuseColor 0.148 0.145 0.145
        specularColor 0.180 0.168 0.160
        emissiveColor 0.0 0.0 0.0
        shininess 0.35
        transparency 0.0
        }"""

resistor_black_body="""material DEF RES-SMD-01 Material {
        diffuseColor 0.082 0.086 0.094
        emissiveColor 0.000 0.000 0.000
        specularColor 0.066 0.063 0.063
        ambientIntensity 0.638
        transparency 0.0
        shininess 0.3
        }"""

dark_grey_body="""material DEF CAP-CERAMIC-05 Material {
        ambientIntensity 0.179
        diffuseColor 0.273 0.273 0.273
        specularColor 0.203 0.188 0.176
        emissiveColor 0.0 0.0 0.0
        shininess 0.15
        transparency 0.0
        }"""

grey_body="""material DEF IC-BODY-EPOXY-01 Material {
        ambientIntensity 0.117
        diffuseColor 0.250 0.262 0.281
        specularColor 0.316 0.281 0.176
        emissiveColor 0.0 0.0 0.0
        shininess 0.25
        transparency 0.0
        }"""

brown_body="""material DEF CAP-CERAMIC-06 Material {
        ambientIntensity 0.453
        diffuseColor 0.379 0.270 0.215
        specularColor 0.223 0.223 0.223
        emissiveColor 0.0 0.0 0.0
        shininess 0.15
        transparency 0.0
        }"""

light_brown_body="""material DEF RES-THT-01 Material {
        ambientIntensity 0.149
        diffuseColor 0.883 0.711 0.492
        specularColor 0.043 0.121 0.281
        emissiveColor 0.0 0.0 0.0
        shininess 0.40
        transparency 0.0
        }"""

blue_body="""material DEF PLASTIC-BLUE-01 Material {
        ambientIntensity 0.565
        diffuseColor 0.137 0.402 0.727
        specularColor 0.359 0.379 0.270
        emissiveColor 0.0 0.0 0.0
        shininess 0.25
        transparency 0.0
        }"""

green_body="""material DEF PLASTIC-GREEN-01 Material {
        ambientIntensity 0.315
        diffuseColor 0.340 0.680 0.445
        specularColor 0.176 0.105 0.195
        emissiveColor 0.0 0.0 0.0
        shininess 0.25
        transparency 0.0
        }"""

orange_body="""material DEF PLASTIC-ORANGE-01 Material {
        ambientIntensity 0.284
        diffuseColor 0.809 0.426 0.148
        specularColor 0.039 0.102 0.145
        emissiveColor 0.0 0.0 0.0
        shininess 0.25
        transparency 0.0
        }"""

red_body="""material DEF RED-BODY Material {
        ambientIntensity 0.683
        diffuseColor 0.700 0.100 0.050
        emissiveColor 0.000 0.000 0.000
        specularColor 0.300 0.400 0.150
        shininess 0.25
        transparency 0.0
        }"""

pink_body="""material DEF CAP-CERAMIC-02 Material {
        ambientIntensity 0.683
        diffuseColor 0.578 0.336 0.352
        specularColor 0.105 0.273 0.270
        emissiveColor 0.0 0.0 0.0
        shininess 0.25
        transparency 0.0
        }"""

yellow_body="""material DEF PLASTIC-YELLOW-01 Material {
        ambientIntensity 0.522
        diffuseColor 0.832 0.680 0.066
        specularColor 0.160 0.203 0.320
        emissiveColor 0.0 0.0 0.0
        shininess 0.25
        transparency 0.0
        }"""

white_body="""material DEF PLASTIC-WHITE-01 Material {
        ambientIntensity 0.494
        diffuseColor 0.895 0.891 0.813
        specularColor 0.047 0.055 0.109
        emissiveColor 0.0 0.0 0.0
        shininess 0.25
        transparency 0.0
        }"""

light_brown_label="""material DEF IC-LABEL-01 Material {
        ambientIntensity 0.082
        diffuseColor 0.691 0.664 0.598
        specularColor 0.000 0.000 0.000
        emissiveColor 0.0 0.0 0.0
        shininess 0.01
        transparency 0.0
        }"""

led_red="""material DEF LED-RED Material {
        ambientIntensity 0.789
        diffuseColor 0.700 0.100 0.050
        emissiveColor 0.000 0.000 0.000
        specularColor 0.300 0.400 0.150
        shininess 0.125
        transparency 0.15
        }"""

led_green="""material DEF LED-GREEN Material {
        ambientIntensity 0.789
        diffuseColor 0.400 0.700 0.150
        emissiveColor 0.000 0.000 0.000
        specularColor 0.600 0.300 0.100
        shininess 0.05
        transparency 0.15
        }"""

led_blue="""material DEF LED-BLUE Material {
        ambientIntensity 0.789
        diffuseColor 0.100 0.250 0.700
        emissiveColor 0.000 0.000 0.000
        specularColor 0.500 0.600 0.300
        shininess 0.125
        transparency 0.15
        }"""

led_yellow="""material DEF LED-YELLOW Material {
        ambientIntensity 0.522
        diffuseColor 0.98 0.840 0.066
        specularColor 0.160 0.203 0.320
        emissiveColor 0.0 0.0 0.0
        shininess 0.125
        transparency 0.15
        }"""

led_white="""material DEF LED-WHITE Material {
        ambientIntensity 0.494
        diffuseColor 0.895 0.891 0.813
        specularColor 0.047 0.055 0.109
        emissiveColor 0.0 0.0 0.0
        shininess 0.125
        transparency 0.15
        }"""

led_grey="""material DEF LED-GREY Material {
        ambientIntensity 0.494
        diffuseColor 0.27 0.25 0.27
        specularColor 0.5 0.5 0.6
        emissiveColor 0.0 0.0 0.0
        shininess 0.35
        transparency 0.15
        }"""

led_black="""material DEF LED-BLACK Material {
        ambientIntensity 0.494
        diffuseColor 0.1 0.05 0.1
        specularColor 0.6 0.5 0.6
        emissiveColor 0.0 0.0 0.0
        shininess 0.5
        transparency 0.15
        }"""

glass_grey="""material DEF GLASS-19 Material {
        ambientIntensity 2.018212
        diffuseColor 0.400769 0.441922 0.459091
        specularColor 0.573887 0.649271 0.810811
        emissiveColor 0.000000 0.000000 0.000000
        shininess 0.127273
        transparency 0.37
        }"""

glass_gold="""material DEF GLASS-29 Material {
        ambientIntensity 0.379
        diffuseColor 0.859 0.738 0.496
        specularColor 0.137 0.145 0.184
        emissiveColor 0.0 0.0 0.0
        shininess 0.40
        transparency 0.39
        }"""

glass_blue="""material DEF GLASS-13 Material {
        ambientIntensity 0.250000
        diffuseColor 0.000000 0.631244 0.748016
        specularColor 0.915152 0.915152 0.915152
        emissiveColor 0.000000 0.000000 0.000000
        shininess 0.642424
        transparency 0.39
        }"""

glass_green="""material DEF GLASS-GREEN Material {
        ambientIntensity 0.250000
        diffuseColor 0.000000 0.75 0.44
        specularColor 0.915152 0.915152 0.915152
        emissiveColor 0.000000 0.000000 0.000000
        shininess 0.642424
        transparency 0.39
        }"""

glass_orange="""material DEF GLASS-ORANGE Material {
        ambientIntensity 0.250000
        diffuseColor 0.75 0.44 0.000000
        specularColor 0.915152 0.915152 0.915152
        emissiveColor 0.000000 0.000000 0.000000
        shininess 0.642424
        transparency 0.39
        }"""

pcb_green="""material DEF BOARD-GREEN-02 Material {
        ambientIntensity 1
        diffuseColor 0.07 0.3 0.12
        specularColor 0.07 0.3 0.12
        emissiveColor 0.0 0.0 0.0
        shininess 0.40
        transparency 0.0
        }"""  

pcb_blue="""material DEF BOARD-BLUE-01 Material {
        ambientIntensity 1
        diffuseColor 0.07 0.12 0.3
        specularColor 0.07 0.12 0.3
        emissiveColor 0.0 0.0 0.0
        shininess 0.40
        transparency 0.0
        }"""

pcb_black="""material DEF BOARD-BLACK-03 Material {
        ambientIntensity 1
        diffuseColor 0.16 0.16 0.16
        specularColor 0.16 0.16 0.16
        emissiveColor 0.0 0.0 0.0
        shininess 0.40
        transparency 0.0
        }"""

metal_aluminum="""material DEF MET-ALUMINUM Material {
        ambientIntensity 0.256000
        diffuseColor 0.372322 0.371574 0.373173
        specularColor 0.556122 0.554201 0.556122
        emissiveColor 0.0 0.0 0.0
        shininess 0.127551
        transparency 0.0
        }"""
##http://vrmlstuff.free.fr/materials/metalsframe.html

# metal_bronze="""material DEF MET-BRONZE Material {
#         ambientIntensity 0.022727
#         diffuseColor 0.314286 0.074365 0.000000
#         specularColor 0.780612 0.598604 0.000000
#         emissiveColor 0.000000 0.000000 0.000000
#         shininess 0.107143
#         transparency 0.0
#         }"""
metal_bronze="""material DEF MET-BRONZE Material {
        ambientIntensity 0.022727
        diffuseColor 0.714 0.4284 0.18144
        specularColor 0.393548 0.271906 0.166721
        emissiveColor 0.000000 0.000000 0.000000
        shininess 0.2
        transparency 0.0
        }"""
       
#bronze     0.2125  0.1275  0.054   0.714   0.4284  0.18144     0.393548    0.271906    0.166721    0.2
#http://devernay.free.fr/cours/opengl/materials.html

#silver     0.19225     0.19225     0.19225     0.50754     0.50754     0.50754     0.508273    0.508273    0.508273    0.4
metal_silver="""material DEF MET-SILVER Material {
        ambientIntensity 0.022727
        diffuseColor 0.50754 0.50754 0.50754
        specularColor 0.508273 0.508273 0.508273
        emissiveColor 0.000000 0.000000 0.000000
        shininess 0.4
        transparency 0.0
        }"""

metal_copper="""material DEF MET-COPPER Material {
        ambientIntensity 0.022727
        diffuseColor 0.7038 0.27048 0.0828
        specularColor 0.780612 0.37 0.000000
        emissiveColor 0.000000 0.000000 0.000000
        shininess 0.2
        transparency 0.0
        }"""
#specularColor 0.780612 0.598604 0.000000

material_properties_names=["as is","metal grey pins","metal grey","gold pins",
                           "black body","resistor black body","grey body","dark grey body","brown body",\
                           "light brown body","blue body","green body","orange body","red_body",\
                           "pink body","yellow body","white body",\
                           "light brown label",\
                           "led red","led green","led blue","led yellow","led white", "led grey", "led black",\
                           "glass grey","glass gold","glass blue","glass green","glass orange", \
                           "pcb green", "pcb blue", "pcb black",\
                           "metal aluminum", "metal bronze", "metal silver", "metal copper"]

material_properties=[as_is, metal_grey_pins, metal_grey, gold_pins,\
                     black_body,resistor_black_body, grey_body,dark_grey_body,brown_body,\
                     light_brown_body,blue_body, green_body,orange_body,red_body,\
                     pink_body,yellow_body,white_body,
                     light_brown_label,\
                     led_red,led_green,led_blue,led_yellow,led_white, led_grey, led_black, \
                     glass_grey, glass_gold, glass_blue, glass_green,glass_orange, \
                     pcb_green, pcb_blue, pcb_black,\
                     metal_aluminum, metal_bronze, metal_silver, metal_copper]

material_properties_diffuse=[(0.,0.,0.,0.),(0.824,0.820,0.781,0.),( 0.298, 0.298, 0.298,0.),(0.859,0.738,0.496,0.), \
                             (0.148, 0.145, 0.145,0.), (0.082, 0.086, 0.094,0.),(0.250, 0.262, 0.281,0.), (0.273, 0.273, 0.273,0.), (0.379, 0.270, 0.215,0.), \
                             (0.883, 0.711, 0.492,0.), (0.137, 0.402, 0.727,0.),(0.340, 0.680, 0.445,0.), (0.809, 0.426, 0.148,0.), (0.700, 0.100, 0.050,0.), \
                             (0.578, 0.336, 0.352,0.), (0.832, 0.680, 0.066,0.), (0.895, 0.891, 0.813,0.), \
                             (0.691, 0.664, 0.598,0.), \
                             (0.700, 0.100, 0.050,0.15), (0.400, 0.700, 0.150,0.15), (0.100, 0.250, 0.700,0.15), (0.98, 0.840, 0.066,0.15), (0.895, 0.891, 0.813,0.15),(0.27, 0.25, 0.27,0.15), (0.1, 0.05, 0.1,0.15),\
                             (0.400769, 0.441922, 0.459091,0.37), (0.859, 0.738, 0.496,0.39), (0.000000, 0.631244, 0.748016,0.39), (0.000000, 0.75, 0.44,0.39), (0.75, 0.44, 0.0,0.39), \
                             (0.07, 0.3, 0.12,0.), (0.07, 0.12, 0.3,0.), (0.16, 0.16, 0.16,0.), \
                             (0.372322, 0.371574, 0.373173,0.), (0.714, 0.4284, 0.18144,0.), (0.50754, 0.50754, 0.50754,0.), (0.7038, 0.27048, 0.0828,0.)] # (0.314286, 0.074365, 0.000000)]

#FreeCAD.Console.PrintMessage (len (material_properties_names))
#FreeCAD.Console.PrintMessage (len (material_properties))
#FreeCAD.Console.PrintMessage (len (material_properties_diffuse))
#stop

material_definitions=""
for mat in material_properties[1:]:
    material_definitions+="Shape {\n    appearance Appearance {"+mat+"\n    }\n}\n"

material_ids=[]
material_ids.append("")

for mat in material_properties[1:]:
    m = re.search('DEF\s(.+?)\sMaterial', mat)
    if m:
        found = m.group(1)
        #say(found)
        material_ids.append(found)
#say(material_ids)    
#say (material_definitions)

def clear_console():
    #clearing previous messages
    mw=FreeCADGui.getMainWindow()
    c=mw.findChild(QtGui.QPlainTextEdit, "Python console")
    c.clear()
    r=mw.findChild(QtGui.QTextEdit, "Report view")
    r.clear()

#if not Mod_ENABLED:
clear_console()
    
# points: [Vector, Vector, ...]
# faces: [(pi, pi, pi), ], pi: point index
# color: (Red, Green, Blue), values range from 0 to 1.0
Mesh = namedtuple('Mesh', ['points', 'faces', 'color', 'transp'])


###############################################
def find_name(n):
    n=n.lower()
    return {
        'prefix3d_1'    : 1,
        'prefix3d_2'    : 2,
        'pcb_color'     : 3,
        'bklist'        : 4,
        'bbox'          : 5,
        'placement'     : 6,
        'virt'          : 7,
        'exportfusing'  : 8,
        'min_drill_size': 9,
        'last_pcb_path' :10,
        'last_fp_path'  :11,
        'export_to_step':12,
        'mat'           :13,
        'spin'          :14,
        'compound'      :15,
        'dkmode'        :16,
        'font_size'     :17,
        'exporting_mode':18,
        'importing_mode':19,
    }.get(n, 0)    # 0 is default if x not found

#

#import ConfigParser
#import configobj

def insert(filename, other):
    if os.path.exists(filename):
        open(filename,True)
    else:
        FreeCAD.Console.PrintError("File does not exist.\n")
        reply = QtGui.QMessageBox.information(None,"info", "File does not exist.\n")

def reload_lib(lib):
    if (sys.version_info > (3, 0)):
        import importlib
        importlib.reload(lib)
    else:
        reload (lib)

def open(filename,insert=None):
    #reply = QtGui.QMessageBox.information(None,"info", filename)
    #onLoadBoard_cmd(filename)
    global original_filename
    ext = os.path.splitext(os.path.basename(filename))[1]
    sayw("kicad StepUp version "+str(___ver___))
    #say("tolerance on vertex = "+str(edge_tolerance))
    say("tolerance on vertex applied")
    if ext==".kicad_pcb":
        original_filename=filename
        onLoadBoard(filename,None,insert)
        # zf= Timer (1.0,ZoomFitThread)
        # zf.start()
    #elif ext==".emn":
    #    onLoadBoard_idf(filename)
    elif ext==".kicad_mod":
        import kicadStepUptools
        reload_lib( kicadStepUptools )
        KSUWidget.activateWindow()
        KSUWidget.show()
        KSUWidget.raise_()
        onLoadFootprint(filename)

#!#def make_unicode(input):
#!#    if (sys.version_info > (3, 0)):  #py3
#!#        if isinstance(input, str):
#!#            return input
#!#        else:
#!#            input =  input.decode('utf-8')
#!#            return input
#!##!#   else: #py2
#!##!#       if type(input) != unicode:
#!##!#           input =  input.decode('utf-8')
#!##!#           return input
#!##!#       else:
#!##!#           return input

def make_string(input):
    if (sys.version_info > (3, 0)):  #py3
        if isinstance(input, str):
            return input
        else:
            input =  input.encode('utf-8')
            return input
#!#   else:  #py2
#!#       if type(input) == unicode:
#!#           input =  input.encode('utf-8')
#!#           return input
#!#       else:
#!#           return input

def PLine(prm1,prm2):
    if hasattr(Part,"LineSegment"):
        return Part.LineSegment(prm1, prm2)
    else:
        return Part.Line(prm1, prm2)
        
def light1(x,y,z):
  light = SoDirectionalLight()
  light.on = True
  # 40W Tungsten 2600 255, 197, 143
  #light.color = (1,197/255,143/255)
  light.color = (1,0.839,0.66667)
  light.intensity = 0.7
  light.direction = (x,y,z)
  return light

def light2(x,y,z):
  light = SoDirectionalLight()
  light.on = True
  #Overcast Sky 7000 201, 226, 255
  #light.color = (201/255,226/255,1)
  light.color = (0.2509,0.6117,1)
  light.intensity = 0.5
  light.direction = (x,y,z)
  return light

def simple_copy_link(obj): #simple copy with incremental placement
    if obj.ViewObject.Visibility != False:
        __shape = Part.getShape(obj,'',needSubElement=False,refine=False)
        FreeCAD.ActiveDocument.addObject('Part::Feature','LinkGroup').Shape=__shape
        nobj = FreeCAD.ActiveDocument.ActiveObject
        nobjV = FreeCADGui.ActiveDocument.ActiveObject
        nobj.Label=obj.Label
        if obj.TypeId == 'App::Part':
            for subobj in obj.OutList:
                if hasattr(FreeCADGui.ActiveDocument.getObject(subobj.Name),'ShapeColor'):
                    nobjV.ShapeColor=FreeCADGui.ActiveDocument.getObject(subobj.Name).ShapeColor
                    if hasattr(FreeCADGui.ActiveDocument.getObject(subobj.Name),'LineColor'):
                        #FreeCAD.Console.PrintMessage(subobj.Label);FreeCAD.Console.PrintMessage(' LineColor ' +str(FreeCADGui.ActiveDocument.getObject(subobj.Name).LineColor)+ '\n')
                        nobjV.LineColor=FreeCADGui.ActiveDocument.getObject(subobj.Name).LineColor
                        nobjV.PointColor=FreeCADGui.ActiveDocument.getObject(subobj.Name).PointColor
                    if hasattr(FreeCADGui.ActiveDocument.getObject(subobj.Name),'DiffuseColor'):
                        #FreeCAD.Console.PrintMessage(subobj.Label);FreeCAD.Console.PrintMessage(' DiffuseColor ' +str(FreeCADGui.ActiveDocument.getObject(subobj.Name).DiffuseColor)+ '\n')
                        nobjV.DiffuseColor=FreeCADGui.ActiveDocument.getObject(subobj.Name).DiffuseColor
                    if hasattr(FreeCADGui.ActiveDocument.getObject(subobj.Name),'Transparency'):
                        #FreeCAD.Console.PrintMessage(subobj.Label);FreeCAD.Console.PrintMessage(' Transparency ' +str(FreeCADGui.ActiveDocument.getObject(subobj.Name).Transparency)+ '\n')
                        nobjV.Transparency=FreeCADGui.ActiveDocument.getObject(subobj.Name).Transparency
        else:
            nobj.ViewObject.ShapeColor=getattr(obj.getLinkedObject(True).ViewObject,'ShapeColor',nobj.ViewObject.ShapeColor)
            nobj.ViewObject.LineColor= getattr(obj.getLinkedObject(True).ViewObject,'LineColor' ,nobj.ViewObject.LineColor)
            nobj.ViewObject.PointColor=getattr(obj.getLinkedObject(True).ViewObject,'PointColor',nobj.ViewObject.PointColor)
        FreeCAD.ActiveDocument.recompute()

def simple_cpy_plc(obj,proot): #simple copy with incremental placement

    if '::CoordinateSystem' not in obj.TypeId and '::DocumentObjectGroup' not in obj.TypeId \
     and '::FeaturePython' not in obj.TypeId and 'GeoFeature' not in obj.TypeId and 'Origin' not in obj.TypeId and obj.ViewObject.Visibility != False:
        s=obj.Shape
        t=s.copy()
        r=s.copy()
        r.Placement=FreeCAD.Placement(proot)
        t.Placement=r.Placement.multiply(t.Placement)  #incremental Placement
        FreeCAD.ActiveDocument.addObject('Part::Feature',obj.Name+"_cp").Shape=t
        if hasattr(FreeCADGui.ActiveDocument.getObject(obj.Name),'ShapeColor'):
            FreeCADGui.ActiveDocument.ActiveObject.ShapeColor=FreeCADGui.ActiveDocument.getObject(obj.Name).ShapeColor
        if hasattr(FreeCADGui.ActiveDocument.getObject(obj.Name),'LineColor'):
            FreeCADGui.ActiveDocument.ActiveObject.LineColor=FreeCADGui.ActiveDocument.getObject(obj.Name).LineColor
        if hasattr(FreeCADGui.ActiveDocument.getObject(obj.Name),'PointColor'):
            FreeCADGui.ActiveDocument.ActiveObject.PointColor=FreeCADGui.ActiveDocument.getObject(obj.Name).PointColor
        if hasattr(FreeCADGui.ActiveDocument.getObject(obj.Name),'DiffuseColor'):
            FreeCADGui.ActiveDocument.ActiveObject.DiffuseColor=FreeCADGui.ActiveDocument.getObject(obj.Name).DiffuseColor
        if hasattr(FreeCADGui.ActiveDocument.getObject(obj.Name),'Transparency'):
            FreeCADGui.ActiveDocument.ActiveObject.Transparency=FreeCADGui.ActiveDocument.getObject(obj.Name).Transparency
        new_label=make_string(obj.Label)+"_cp"
        FreeCAD.ActiveDocument.ActiveObject.Label=new_label
        #stop

def get_node_plc(o,obj):  # get node placement in App::Part
    
    child = FreeCAD.ActiveDocument.addObject("Part::Box","BoxC")
    node = FreeCAD.ActiveDocument.addObject("Part::Box","BoxN")
    child.Placement=o.Placement
    node.Placement=obj.Placement
    new_Placement=node.Placement.multiply(child.Placement)
    FreeCAD.ActiveDocument.removeObject("BoxC")
    FreeCAD.ActiveDocument.removeObject("BoxN")
    FreeCAD.ActiveDocument.recompute()
    return new_Placement
    
def recurse_node(obj,plcm,scl):  # recursive function to make a simple copy of App::Part hierarchy
    if "App::Part" in obj.TypeId or 'Body' in obj.TypeId or 'App::LinkGroup' in obj.TypeId:
        #sayerr(obj.Label)
        if 'LinkGroup' in obj.TypeId:
            group = obj.OutList
        else:
            group = obj.Group
        #for o in obj.Group:
        #sayw(str(group))
        for o in group:
            #sayerr(o.Name);sayw(o.TypeId)
            if "App::Part" in o.TypeId or 'Body' in o.TypeId or 'App::LinkGroup' in o.TypeId:
                #sayerr(o.Label)#+" * "+obj.Name)
                new_plcm=get_node_plc(o,obj)
                recurse_node(o,new_plcm,scl)
            else:
                if "Sketcher" not in o.TypeId and "DocumentObjectGroup" not in o.TypeId:
                    if FreeCADGui.ActiveDocument.getObject(o.Name).Visibility:
                        if 'Compound2' in o.TypeId:
                            simple_copy_link(o)
                            #simple_cpy_plc(o,plcm)
                        else:
                            simple_cpy_plc(o,plcm)
                        scl.append(FreeCAD.ActiveDocument.ActiveObject)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 164)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(30, 110, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.comboBox = QtGui.QComboBox(Dialog)
        self.comboBox.setGeometry(QtCore.QRect(180, 40, 191, 22))
        self.comboBox.setMaxVisibleItems(33) #25
        self.comboBox.setObjectName("comboBox")
        self.label = QtGui.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(180, 20, 53, 16))
        self.label.setObjectName("label")
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(20, 20, 53, 16))
        self.label_2.setObjectName("label_2")
        self.plainTextEdit = QtGui.QTextEdit(Dialog)
        self.plainTextEdit.setEnabled(False)
        self.plainTextEdit.setGeometry(QtCore.QRect(20, 40, 31, 31))
        #self.plainTextEdit.setBackgroundVisible(True)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.plainTextEdit_2 = QtGui.QTextEdit(Dialog)
        self.plainTextEdit_2.setEnabled(False)
        self.plainTextEdit_2.setGeometry(QtCore.QRect(120, 40, 31, 31))
        #self.plainTextEdit_2.setBackgroundVisible(True)
        self.plainTextEdit_2.setObjectName("plainTextEdit_2")
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(120, 20, 41, 16))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtGui.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(20, 80, 351, 16))
        self.label_4.setObjectName("label_4")
        QtCore.QObject.connect(self.comboBox, QtCore.SIGNAL("currentIndexChanged(QString)"), self.SIGNAL_comboBox_Changed)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def SIGNAL_comboBox_Changed(self,text):
        #say("combo changed "+text)
        comboBox_Changed(text)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle("Material Properties")
        self.label.setText("Materials")
        self.label_2.setText("Original")
        self.plainTextEdit.setToolTip("Shape Color")
        self.plainTextEdit_2.setToolTip("Diffuse Color")
        self.label_3.setText("New")
        self.label_4.setText("NB: set Material will unmatch colors between wrl and STEP")
###
def isWritable(path):
    try:
        testfile = tempfile.TemporaryFile(dir = path)
        testfile.close()
        #sayw('ok')
        return True
    except:
    #except OSError as e:
        #sayw('ko')
        sayw('folder not writable!') 
        pass        
        return False
        #if e.errno == errno.EACCES:  # 13
        #    return False
        #e.filename = path
        #return False        
        #raise
    sayw('folder not writable!')    
    return False
###
def comboBox_Changed(text_combo):
    global ui, shape_col
    #say(text_combo)
    material_index=material_properties_names.index(text_combo)
    #say(material_index)
    mat_prop = material_properties[material_index].split('\n')
    if len(mat_prop)>1:
        # say(mat_prop[2])
        color_rgb=mat_prop[2].split(' ')
        # say (color_rgb)
        # say(color_rgb[9]+" "+color_rgb[10]+" "+color_rgb[11])
        ## pal = QtGui.QPalette()
        ## bgc = QtGui.QColor(float(color_rgb[9])*255,float(color_rgb[10])*255, float(color_rgb[11])*255)
        ## pal.setColor(QtGui.QPalette.Base, bgc)
        ## ui.plainTextEdit_2.viewport().setPalette(pal)
        #say(material_index)
        ui.plainTextEdit_2.setStyleSheet("#plainTextEdit_2 {background-color:rgb("+str(float(color_rgb[9])*255)+","+str(float(color_rgb[10])*255)+","+str(float(color_rgb[11])*255)+");}") 
    else:
        #say(str(material_index)+" here")
        #ui.plainTextEdit_2.setStyleSheet("#plainTextEdit_2 {background-color:rgb("+str(0*255)+","+str(1*255)+","+str(0*255)+");}") 
        ui.plainTextEdit_2.setStyleSheet("#plainTextEdit_2 {background-color:rgb("+str(shape_col[0]*255)+","+str(shape_col[1]*255)+","+str(shape_col[2]*255)+");}") 

###

def shapeToMesh(shape, color, transp, mesh_deviation, scale=None):
    #mesh_deviation=0.1 #the smaller the best quality, 1 coarse
    #say(mesh_deviation)
    mesh_data = shape.tessellate(mesh_deviation)
    points = mesh_data[0]
    if scale is not None:
        points = map(lambda p: p*scale, points)
    newMesh= Mesh(points = points,
                faces = mesh_data[1],
                color = color, transp=transp)
    return newMesh

def exportVRMLmaterials(objects, filepath):
    """Export given list of Mesh objects to a VRML file.
    with material properties
    `Mesh` structure is defined at root."""
    global ui, creaseAngle, shape_col
    global color_list, color_list_mat
    #material_list=["as is","metal pins","gold pins","black body","dark brown body","brown body","grey body","green body","white body","black label","white label"]
    #material_properties_names=["as is","metal grey pins","gold pins","black body","resistor black body",\
    #                       "grey body","dark grey body","brown body","light brown body","blue body",\
    #                       "green body","orange body","pink body","yellow body","white body","light brown label",\
    #                       "led red","led green","led blue"]
    #global color_list_mat, col_index
    #with __builtin__.open(filepath, 'w') as f:
    # with builtin.open(filepath, 'wb') as f: #py2
    if filepath.endswith('wrz'):
        fname=os.path.splitext(os.path.basename(filepath))[0]
        tempdir = tempfile.gettempdir() # get the current temporary directory
        tempfilepath = os.path.join(tempdir,fname + u'.wrl')
        fpath=tempfilepath
    else:
        fpath=filepath
    with builtin.open(fpath, 'w') as f: #py3
        # write the standard VRML header
        f.write("#VRML V2.0 utf8\n#kicad StepUp wrl exported\n\n")
        f.write(material_definitions)
        color_list=[]
        color_list_mat=[]
        index_color=-1
        Dialog = QtGui.QDialog()
        ui = Ui_Dialog()
        ui.setupUi(Dialog)
        ui.comboBox.addItems(material_properties_names)
        material="as is"
        for obj in objects:
            if creaseAngle==0:
                f.write("Shape { geometry IndexedFaceSet \n{ coordIndex [")
            else:
                f.write("Shape { geometry IndexedFaceSet \n{ creaseAngle %.2f coordIndex [" % creaseAngle)
            # write coordinate indexes for each face
            f.write(','.join("%d,%d,%d,-1" % f for f in obj.faces))
            f.write("]\n") # closes coordIndex
            f.write("coord Coordinate { point [")
            # write coordinate points for each vertex
            #f.write(','.join('%.3f %.3f %.3f' % (p.x, p.y, p.z) for p in obj.points))
            f.write(','.join('%g %g %g' % (p.x, p.y, p.z) for p in obj.points))
            f.write("]\n}") # closes Coordinate
            #shape_col=(1.0, 0.0, 0.0)#, 0.0)
            f.write("}\n") # closes points
            #say(obj.color)
            ##shape_col=obj.color[:-1] #remove last item
            shape_col=obj.color
            #say(shape_col)
            if shape_col not in color_list:
                #sayw(shape_col);say('not found')
                idc=0;material_index=0
                found_mat=False
                for mat_diff_col in material_properties_diffuse:
                    #say(mat_diff_col)
                    delta_col=0.01
                    if ((abs(shape_col[0]-mat_diff_col[0])<delta_col) and (abs(shape_col[1]-mat_diff_col[1])<delta_col)\
                        and (abs(shape_col[2]-mat_diff_col[2])<delta_col) and (abs(shape_col[3]-mat_diff_col[3])<delta_col)) and not found_mat:
                        #sayw('found a match')
                        material_index=idc
                        found_mat=True
                        #stop
                    idc+=1
                ## pal = QtGui.QPalette()
                ## bgc = QtGui.QColor(shape_col[0]*255,shape_col[1]*255, shape_col[2]*255)
                ## pal.setColor(QtGui.QPalette.Base, bgc)
                ## ui.plainTextEdit.viewport().setPalette(pal)
                ui.plainTextEdit.setStyleSheet("#plainTextEdit {background-color:rgb("+str(shape_col[0]*255)+","+str(shape_col[1]*255)+","+str(shape_col[2]*255)+");}") 
                ui.plainTextEdit_2.setStyleSheet("#plainTextEdit_2 {background-color:rgb("+str(shape_col[0]*255)+","+str(shape_col[1]*255)+","+str(shape_col[2]*255)+");}") 
                ui.comboBox.setCurrentIndex(material_index)
                #ui.comboBox.clear()
                color_list.append(shape_col)
                #print(shape_col, 'shape_col')
                index_color=index_color+1
                #say(color_list)
                #ui.comboBox.addItems(color_list)
                if Materials:
                    ## material_index=material_properties_names.index(color_list_mat[col_index])
                    ## ui.comboBox.setCurrentIndex(index_color)
                    reply=Dialog.exec_()
                    #Dialog.exec_()
                    #say(reply)
                    if reply==1:
                        material=str(ui.comboBox.currentText())
                    else:
                        material="as is"
                color_list_mat.append(material)
                sayw(material)
            #else:
            #    sayw(shape_col);say('Found!')
            #    col_index=color_list.index(shape_col)
            #    ui.plainTextEdit.setStyleSheet("#plainTextEdit {background-color:rgb("+str(shape_col[0]*255)+","+str(shape_col[1]*255)+","+str(shape_col[2]*255)+");}") 
            #    ui.comboBox.setCurrentIndex(col_index)
            #say("searching")
            col_index=color_list.index(shape_col)
            #print (color_list_mat[col_index],col_index)
            #say(color_list_mat[col_index])
            if not Materials or color_list_mat[col_index]=="as is":
                shape_transparency=obj.transp
                f.write("appearance Appearance{material Material{diffuseColor %g %g %g\n" % shape_col[:-1])
                f.write("transparency %g}}" % shape_transparency)
                f.write("}\n") # closes Shape
            else:
                material_index=material_properties_names.index(color_list_mat[col_index])
                #say(material_properties[material_index])
                #f.write("appearance Appearance{"+material_properties[material_index]+"}}\n")
                f.write("appearance Appearance{material USE "+material_ids[material_index]+" }}\n")
        #say(fpath+' written')
        
    if filepath.endswith('wrz'):
        with builtin.open(fpath, 'rb') as f_in:
            file_content = f_in.read()
            new_f_content = file_content
            f_in.close()
        #filepath=filepath[:filepath.rfind('.')]+u'.wrz'
        with gz.open(filepath, 'wb') as f_out:
            f_out.write(new_f_content)
            f_out.close()
    say(filepath+' written')
        #if os.path.exists(fpath):
        #    #os.remove(outfpath)
        #    os.rename(fpath, filepath)  
            #os.remove(outfpathT_stp)
         #else:
         #    os.rename(outfpathT_str, outfpath)
            #os.remove(outfpathT_stp)                

    #sayw (color_list); sayw(color_list_mat);
    #for obj in objects:
    #    sayw(obj.Label)
    #stop
    #index_color=-1
    #Dialog = QtGui.QDialog()
    #ui = Ui_Dialog()
    #ui.setupUi(Dialog)
    #ui.comboBox.addItems(material_properties_names)
    ##for obj in componentObjs:
    #reply=Dialog.exec_()


###
def exportVRML(objects, filepath):
    """Export given list of Mesh objects to a VRML file.

    `Mesh` structure is defined at root."""

    global creaseAngle
    #with __builtin__.open(filepath, 'w') as f:
    # with builtin.open(filepath, 'wb') as f: #py2
    if filepath.endswith('wrz'):
        fname=os.path.splitext(os.path.basename(filepath))[0]
        tempdir = tempfile.gettempdir() # get the current temporary directory
        tempfilepath = os.path.join(tempdir,fname + u'.wrl')
        fpath=tempfilepath
    else:
        fpath=filepath
    with builtin.open(fpath, 'w') as f:  #py3
        # write the standard VRML header
        f.write("#VRML V2.0 utf8\n#kicad StepUp wrl exported\n\n")
        for obj in objects:
            if creaseAngle==0:
                f.write("Shape { geometry IndexedFaceSet \n{ coordIndex [")
            else:
                f.write("Shape { geometry IndexedFaceSet \n{ creaseAngle %.2f coordIndex [" % creaseAngle)
            #f.write("Shape { geometry IndexedFaceSet \n{ coordIndex [")
            # write coordinate indexes for each face
            f.write(','.join("%d,%d,%d,-1" % f for f in obj.faces))
            f.write("]\n") # closes coordIndex
            f.write("coord Coordinate { point [")
            # write coordinate points for each vertex
            #f.write(','.join('%.3f %.3f %.3f' % (p.x, p.y, p.z) for p in obj.points))
            f.write(','.join('%g %g %g' % (p.x, p.y, p.z) for p in obj.points))
            f.write("]\n}") # closes Coordinate
            #shape_col=(1.0, 0.0, 0.0)#, 0.0)
            f.write("}\n") # closes points
            #say(obj.color)
            shape_col=obj.color[:-1] #remove last item
            #say(shape_col)
            shape_transparency=obj.transp
            f.write("appearance Appearance{material Material{diffuseColor %g %g %g\n" % shape_col)
            f.write("transparency %g}}" % shape_transparency)
            f.write("}\n") # closes Shape
    if filepath.endswith('wrz'):
        with builtin.open(fpath, 'rb') as f_in:
            file_content = f_in.read()
            new_f_content = file_content
            f_in.close()
        #filepath=filepath[:filepath.rfind('.')]+u'.wrz'
        with gz.open(filepath, 'wb') as f_out:
            f_out.write(new_f_content)
            f_out.close()    
    say(filepath+' written')
###

def export(componentObjs, fullfilePathName, scale=None, label=None):
    """ Exports given ComponentModel object using FreeCAD.

    `componentObjs` : a ComponentObjs list
    `fullfilePathName` : name of the FC file, extension is important
    
    """
    
    global exportV, applymaterials, ui, creaseAngle
    
    if label is None:
        exp_name=componentObjs[0].Label
    else:
        exp_name=label
    #removing not allowed chars
    translation_table = dict.fromkeys(map(ord, '<>:"/\|?*,;:\\'), None)
    exp_name=exp_name.translate(translation_table)
    path, fname = os.path.split(fullfilePathName)
    fname=os.path.splitext(fname)[0]
    save_wrz=False
    prefs = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/kicadStepUpGui")
    if prefs.GetBool('wrz_export_enabled'):
        #'stpz'
        save_wrz=True
        #print('stpZ',fullFilePathNameStep)
    if scale is not None:
        if save_wrz:
            filename=path+os.sep+exp_name+'.wrz'
        else:
            filename=path+os.sep+exp_name+'.wrl'
    else:
        if save_wrz:
            filename=path+os.sep+exp_name+'_1_1.wrz'
        else:
            filename=path+os.sep+exp_name+'_1_1.wrl'
    say(filename)
    exportV=True
    mesh_deviation_default=0.03 # 0.03 or 0.1
    mesh_dev=mesh_deviation_default #the smaller the best quality, 1 coarse
    if os.path.exists(filename):
        say('file exists')
        QtGui.QApplication.restoreOverrideCursor()
        reply = QtGui.QMessageBox.question(None, "Info", filename+"\nwrl file exists, overwrite?",
        QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            # this is where the code relevant to a 'Yes' answer goes
            exportV=True
            #pass
        if reply == QtGui.QMessageBox.No:
            # this is where the code relevant to a 'No' answer goes
            exportV=False
            #pass
    if exportV:
        reply = QtGui.QInputDialog.getText(None, "Mesh Deviation","Mesh Deviation (the smaller the better quality)",QtGui.QLineEdit.Normal,str(mesh_deviation_default))
        if reply[1]:
                # user clicked OK
                replyText = reply[0]
                mesh_dev = float (replyText)
        else:
                # user clicked Cancel
                replyText = reply[0] # which will be "" if they clicked Cancel
                mesh_dev=mesh_deviation_default #the smaller the best quality, 1 coarse
                #default
        creaseAngle_default=0.5
        reply = QtGui.QInputDialog.getText(None, "creaseAngle","creaseAngle (range:0-1.5)\ncheck your wrl result\n(0->None)",QtGui.QLineEdit.Normal,str(creaseAngle_default))
        if reply[1]:
                # user clicked OK
                replyText = reply[0]
                creaseAngle = float (replyText)
        else:
                # user clicked Cancel
                replyText = reply[0] # which will be "" if they clicked Cancel
                creaseAngle=creaseAngle_default #the bigger the best quality, 1 coarse
                #default
        #say(mesh_deviation)
        #say(mesh_dev)
        color=[]
        Diffuse_color=[]
        transparency=[]
        for obj in componentObjs:
            #say(obj.Label)
            color.append(FreeCADGui.ActiveDocument.getObject(obj.Name).ShapeColor)
            transparency.append(FreeCADGui.ActiveDocument.getObject(obj.Name).Transparency/100.0)
            #say("color")
            #say(FreeCADGui.ActiveDocument.getObject(obj.Name).DiffuseColor)
            Diffuse_color.append(FreeCADGui.ActiveDocument.getObject(obj.Name).DiffuseColor)
        i=0
        meshes=[]
        #say("diffuse color")
        #say(Diffuse_color)
        indexColor=0;
        color_vector=[]
        applyDiffuse=0
        for obj in componentObjs:
            shape1=obj.Shape
            single_color=Diffuse_color[i];
            #check length color
            #say("len color")
            #say(len(single_color))
            #colors less then faces
            if(len(single_color)!=len(shape1.Faces)):
                applyDiffuse=0;
                #copy color to all faces
            #else copy singular colors for faces
            else:
                applyDiffuse=1;
                for color in single_color:
                    color_vector.append(color)
            #say("color_vector")
            #say(color_vector)
            for index in range(len(shape1.Faces)):
                #say("color x")
                #say(color_vector[indexColor])
                singleFace=shape1.Faces[index]
                if(applyDiffuse):
                    #say(color_vector[indexColor])
                    meshes.append(shapeToMesh(singleFace, color_vector[indexColor], transparency[i], mesh_dev, scale))
                else:
                    #say(single_color[0])
                    meshes.append(shapeToMesh(singleFace, single_color[0], transparency[i], mesh_dev, scale))
                indexColor=indexColor+1
                #meshes.append(shapeToMesh(face, Diffuse_color[i], transparency[i], scale))
            color_vector=[]
            indexColor=0;
            i=i+1
        if enable_materials == 1:
        #    print 'ciao'
        #if applymaterials==1:
            exportVRMLmaterials(meshes, filename)
        else:
            exportVRML(meshes, filename)
    return
###
def check_AP():
    #say("AP")
    sel = FreeCADGui.Selection.getSelection()
    if 'App::Part' in sel[0].TypeId:
        sc_list=[]
        FreeCADGui.ActiveDocument.getObject(sel[0].Name).Visibility=False
        #sel[0].Visibility=False
        for obj in FreeCADGui.Selection.getSelection():
            recurse_node(obj,obj.Placement, sc_list)
        no_shape=True
        for ob in sc_list:
            #print(ob.Label,hasattr(ob,'Shape'))
            if hasattr(ob,'Shape'):
                no_shape=False
        if no_shape:
            msg="Select one or more objects with a Shape!"
            sayerr(msg)
            say_warning(msg)
            stop
        FreeCAD.activeDocument().addObject("Part::Compound",FreeCADGui.Selection.getSelection()[0].Label+"_cp")
        FreeCAD.activeDocument().ActiveObject.Links = sc_list #[FreeCAD.activeDocument().Part__Feature,FreeCAD.activeDocument().Shape,]
        mycompound=FreeCAD.activeDocument().ActiveObject
        FreeCAD.activeDocument().recompute()
        FreeCADGui.Selection.removeSelection(sel[0])
        FreeCADGui.Selection.addSelection(FreeCAD.activeDocument().ActiveObject)

def simple_copy(obj):

    s=obj.Shape
    FreeCAD.ActiveDocument.addObject('Part::Feature',make_string(obj.Label)+"_cp").Shape=s
    FreeCADGui.ActiveDocument.ActiveObject.ShapeColor=FreeCADGui.ActiveDocument.getObject(obj.Name).ShapeColor
    FreeCADGui.ActiveDocument.ActiveObject.LineColor=FreeCADGui.ActiveDocument.getObject(obj.Name).LineColor
    FreeCADGui.ActiveDocument.ActiveObject.PointColor=FreeCADGui.ActiveDocument.getObject(obj.Name).PointColor
    FreeCADGui.ActiveDocument.ActiveObject.DiffuseColor=FreeCADGui.ActiveDocument.getObject(obj.Name).DiffuseColor
    FreeCADGui.ActiveDocument.ActiveObject.Transparency=FreeCADGui.ActiveDocument.getObject(obj.Name).Transparency
    new_label=make_string(obj.Label)+"_cp"
    FreeCAD.ActiveDocument.ActiveObject.Label=new_label
    FreeCAD.ActiveDocument.recompute()

def group_part():
    #say("gp")
    sel = FreeCADGui.Selection.getSelection()
    if len(sel)==0:
        sayw("None selected!")
        msg="Select a Compound or a Part Design group\nor more than one Part object!"
        sayerr(msg)
        say_select_obj()
    if len(sel)==1:
        found=0
        p0 =  FreeCAD.Placement (FreeCAD.Vector(0,0,0), FreeCAD.Rotation(0,0,0), FreeCAD.Vector(0,0,0))
        if 'App::Part' in sel[0].TypeId or 'Body' in sel[0].TypeId:
            sayw("doing compound and single copy")
            sc_list=[]
            FreeCADGui.ActiveDocument.getObject(sel[0].Name).Visibility=False
            original_label=make_string(sel[0].Label)
            #sayerr(original_label)
            #sel[0].Visibility=False
            pOriginal=FreeCADGui.Selection.getSelection()[0].Placement
            FreeCADGui.Selection.getSelection()[0].Placement=p0
            for obj in FreeCADGui.Selection.getSelection():
                recurse_node(obj,obj.Placement, sc_list)       
            #print sc_list
            #stop
            if len (sc_list) == 1:
                #simple_copy(FreeCAD.activeDocument().getObject(sc_list[0].Name))
                #print pOriginal
                simple_cpy_plc(sc_list[0],pOriginal)
                FreeCAD.ActiveDocument.removeObject(sc_list[0].Name)
                FreeCAD.ActiveDocument.ActiveObject.Label=original_label+"_sc"
                found=1
                #stop
            else:
                FreeCADGui.Selection.getSelection()[0].Placement=pOriginal
                FreeCAD.activeDocument().addObject("Part::Compound",FreeCADGui.Selection.getSelection()[0].Label+"_cp")
                FreeCAD.activeDocument().ActiveObject.Links = sc_list #[FreeCAD.activeDocument().Part__Feature,FreeCAD.activeDocument().Shape,]
                mycompound=FreeCAD.activeDocument().ActiveObject
                FreeCAD.activeDocument().ActiveObject.Placement = pOriginal
                FreeCAD.activeDocument().recompute()
                FreeCADGui.Selection.removeSelection(sel[0])
                FreeCADGui.Selection.addSelection(FreeCAD.activeDocument().ActiveObject)
                simple_copy(FreeCAD.activeDocument().getObject(mycompound.Name))
                FreeCADGui.ActiveDocument.getObject(mycompound.Name).Visibility=False
                FreeCAD.ActiveDocument.ActiveObject.Label=original_label+"_sp"      
                FreeCAD.ActiveDocument.recompute()            
                found=1
        if 'Part::Compound' in sel[0].TypeId:
            sayw("doing single copy")
            original_label=make_string(FreeCADGui.Selection.getSelection()[0].Label)
            original_name=FreeCADGui.Selection.getSelection()[0].Name
            n_objs=0
            solids=FreeCAD.ActiveDocument.getObject(FreeCADGui.Selection.getSelection()[0].Name).Shape.Solids
            for solid in solids:
                solids.index(solid)
                n_objs=n_objs+1
            simple_copy(sel[0])
            FreeCADGui.ActiveDocument.getObject(original_name).Visibility=False
            FreeCAD.ActiveDocument.ActiveObject.Label=original_label+"_sp"
            FreeCAD.ActiveDocument.recompute()
            found=1
        if "Part::MultiFuse" in sel[0].TypeId:
            sayw("doing single copy")
            original_label=make_string(FreeCADGui.Selection.getSelection()[0].Label)
            original_name=FreeCADGui.Selection.getSelection()[0].Name
            n_objs=0
            solids=FreeCAD.ActiveDocument.getObject(FreeCADGui.Selection.getSelection()[0].Name).Shape.Solids
            for solid in solids:
                solids.index(solid)
                n_objs=n_objs+1
            simple_copy(sel[0])
            FreeCADGui.ActiveDocument.getObject(original_name).Visibility=False
            FreeCAD.ActiveDocument.ActiveObject.Label=original_label+"_sp"
            FreeCAD.ActiveDocument.recompute()
            found=1
        if found==0:
            say_select_obj()
    if len(sel)>1:
        objs=[]
        for obj in sel:
            #say(obj.Label)
            if 'Part::' in obj.TypeId:
                objs.append(obj)
                #say(obj.Label)
        if len(objs)>1:
            sayw("doing compound and single copy")
            CopyName = FreeCAD.activeDocument().getObject(objs[0].Name).Name
            original_label=make_string(objs[0].Label)
            FreeCAD.activeDocument().addObject("Part::Compound",original_label+"_mp")
            FreeCAD.activeDocument().ActiveObject.Links = objs #[FreeCAD.activeDocument().Part__Feature,FreeCAD.activeDocument().Shape,]
            mycompound=FreeCAD.activeDocument().ActiveObject
            FreeCAD.activeDocument().recompute()

            simple_copy(FreeCAD.activeDocument().getObject(mycompound.Name))
            FreeCADGui.ActiveDocument.getObject(mycompound.Name).Visibility=False
            FreeCAD.ActiveDocument.ActiveObject.Label=original_label+"_sp"      
            FreeCAD.ActiveDocument.recompute()
        else:
            say_select_obj()

        
def group_part_union():
    #say("gp union")
    sel = FreeCADGui.Selection.getSelection()
    if len(sel)==0:
        sayw("None selected!")
        msg="Select a Compound or a Part Design group\nor more than one Part object!"
        sayerr(msg)
        say_select_obj()
    if len(sel)==1:
        found=0
        p0 =  FreeCAD.Placement (FreeCAD.Vector(0,0,0), FreeCAD.Rotation(0,0,0), FreeCAD.Vector(0,0,0))
        if 'App::Part' in sel[0].TypeId or 'Body' in sel[0].TypeId:
            sayw("doing union and single copy")
            original_label=make_string(sel[0].Label)
            sc_list=[]
            FreeCADGui.ActiveDocument.getObject(sel[0].Name).Visibility=False
            #sel[0].Visibility=False
            pOriginal=FreeCADGui.Selection.getSelection()[0].Placement
            FreeCADGui.Selection.getSelection()[0].Placement=p0
            for obj in FreeCADGui.Selection.getSelection():
                recurse_node(obj,obj.Placement, sc_list)       
            FreeCADGui.Selection.getSelection()[0].Placement=pOriginal
            #print sc_list
            #stop
            if len (sc_list) == 1:
                #simple_copy(FreeCAD.activeDocument().getObject(sc_list[0].Name))
                #print pOriginal
                simple_cpy_plc(sc_list[0],pOriginal)
                FreeCAD.ActiveDocument.removeObject(sc_list[0].Name)
                FreeCAD.ActiveDocument.ActiveObject.Label=original_label+"_sp"
                #stop
            else:
                FreeCAD.activeDocument().addObject("Part::Compound",FreeCADGui.Selection.getSelection()[0].Label+"_cp")
                FreeCAD.activeDocument().ActiveObject.Links = sc_list #[FreeCAD.activeDocument().Part__Feature,FreeCAD.activeDocument().Shape,]
                mycompound=FreeCAD.activeDocument().ActiveObject
                FreeCAD.activeDocument().ActiveObject.Placement = pOriginal
                FreeCAD.activeDocument().recompute()
                FreeCADGui.Selection.removeSelection(sel[0])
                FreeCADGui.Selection.addSelection(FreeCAD.activeDocument().ActiveObject)
                CopyName = FreeCAD.activeDocument().ActiveObject.Name
                FreeCAD.activeDocument().addObject("Part::MultiFuse",original_label+"_mp_cp")
                FusionName = FreeCAD.activeDocument().ActiveObject.Name
                #say(FusionName)
                FreeCAD.activeDocument().getObject(FusionName).Shapes = [FreeCAD.activeDocument().getObject(CopyName),]
                FreeCADGui.activeDocument().getObject(CopyName).Visibility=False
                FreeCADGui.ActiveDocument.getObject(FusionName).ShapeColor=FreeCADGui.ActiveDocument.getObject(CopyName).ShapeColor
                FreeCADGui.ActiveDocument.getObject(FusionName).DisplayMode=FreeCADGui.ActiveDocument.getObject(CopyName).DisplayMode
                FreeCAD.ActiveDocument.getObject(FusionName).Label=original_label+"_fd"
                FreeCAD.ActiveDocument.recompute()
                if 'Invalid' in FreeCAD.ActiveDocument.getObject(FusionName).State:
                    # fusion failed code...
                    sayerr("fusion failed! doing compound & single copy")
                    msg="""Union of parts <b><font color='red'>failed!</font></b><br>... doing Compound & single copy"""
                    say_warning(msg)
                    FreeCAD.ActiveDocument.removeObject(FusionName)
                    FreeCAD.ActiveDocument.recompute()
                    #mycompound=FreeCAD.activeDocument().getObject
                    #FreeCAD.activeDocument().recompute()
                    simple_copy(FreeCAD.activeDocument().getObject(mycompound.Name))
                    FreeCADGui.ActiveDocument.getObject(mycompound.Name).Visibility=False
                    FreeCAD.ActiveDocument.ActiveObject.Label=original_label+"_sp"      
                    FreeCAD.ActiveDocument.recompute()
                else:
                    simple_copy(FreeCAD.activeDocument().getObject(FusionName))
                    FreeCADGui.ActiveDocument.getObject(FusionName).Visibility=False
                    FreeCAD.ActiveDocument.ActiveObject.Label=original_label+"_sp"      
                    FreeCAD.ActiveDocument.recompute()
            found=1
        if 'Part::Compound' in sel[0].TypeId:
            sayw("doing single copy")
            original_label=make_string(FreeCADGui.Selection.getSelection()[0].Label)
            original_name=FreeCADGui.Selection.getSelection()[0].Name
            n_objs=0
            solids=FreeCAD.ActiveDocument.getObject(FreeCADGui.Selection.getSelection()[0].Name).Shape.Solids
            for solid in solids:
                solids.index(solid)
                n_objs=n_objs+1
            simple_copy(sel[0])
            FreeCADGui.ActiveDocument.getObject(original_name).Visibility=False
            FreeCAD.ActiveDocument.ActiveObject.Label=original_label+"_sp"
            FreeCAD.ActiveDocument.recompute()
            found=1
        if "Part::MultiFuse" in sel[0].TypeId:
            sayw("doing single copy")
            original_label=make_string(FreeCADGui.Selection.getSelection()[0].Label)
            original_name=FreeCADGui.Selection.getSelection()[0].Name
            n_objs=0
            solids=FreeCAD.ActiveDocument.getObject(FreeCADGui.Selection.getSelection()[0].Name).Shape.Solids
            for solid in solids:
                solids.index(solid)
                n_objs=n_objs+1
            simple_copy(sel[0])
            FreeCADGui.ActiveDocument.getObject(original_name).Visibility=False
            FreeCAD.ActiveDocument.ActiveObject.Label=original_label+"_sp"
            FreeCAD.ActiveDocument.recompute()
            found=1
        if found==0:
            say_select_obj()
    if len(sel)>1:
        objs=[]
        for obj in sel:
            #say(obj.Label)
            if 'Part' in obj.TypeId and 'App::Part' not in sel[0].TypeId and 'Body' not in sel[0].TypeId:
                objs.append(obj)
                #say(obj.Label)
        if len(objs)>1:
            sayw("doing union and single copy")
            CopyName = FreeCAD.activeDocument().getObject(objs[0].Name).Name
            original_label=make_string(objs[0].Label)
            FreeCAD.activeDocument().addObject("Part::MultiFuse",original_label+"_mp_cp")
            FusionName = FreeCAD.activeDocument().ActiveObject.Name
            #say(FusionName)
            FreeCAD.activeDocument().getObject(FusionName).Shapes = objs
            FreeCADGui.activeDocument().getObject(CopyName).Visibility=False
            FreeCADGui.ActiveDocument.getObject(FusionName).ShapeColor=FreeCADGui.ActiveDocument.getObject(CopyName).ShapeColor
            FreeCADGui.ActiveDocument.getObject(FusionName).DisplayMode=FreeCADGui.ActiveDocument.getObject(CopyName).DisplayMode
            FreeCAD.ActiveDocument.getObject(FusionName).Label=original_label+"_fd"
            FreeCAD.ActiveDocument.recompute()
            if 'Invalid' in FreeCAD.ActiveDocument.getObject(FusionName).State:
                # fusion failed code...
                sayerr("fusion failed! doing compound & single copy")
                msg="""Union of parts <b><font color='red'>failed!</font></b><br>... doing Compound & single copy"""
                say_warning(msg)
                FreeCAD.ActiveDocument.removeObject(FusionName)
                FreeCAD.ActiveDocument.recompute()
                FreeCAD.activeDocument().addObject("Part::Compound",original_label+"_mp")
                FreeCAD.activeDocument().ActiveObject.Links = objs #[FreeCAD.activeDocument().Part__Feature,FreeCAD.activeDocument().Shape,]
                mycompound=FreeCAD.activeDocument().ActiveObject
                FreeCAD.activeDocument().recompute()
                simple_copy(FreeCAD.activeDocument().getObject(mycompound.Name))
                FreeCADGui.ActiveDocument.getObject(mycompound.Name).Visibility=False
                FreeCAD.ActiveDocument.ActiveObject.Label=original_label+"_sp"      
                FreeCAD.ActiveDocument.recompute()
            #mw=Gui.getMainWindow()
            ##c=mw.findChild(QtGui.QPlainTextEdit, "Python console")
            ##c.clear()
            #r=mw.findChild(QtGui.QTextEdit, "Report view")
            #say(r.toPlainText())
            #if r.toPlainText().find("MultiFusion failed") != -1:
            ##if "MultiFusion failed" in r.toPlainText():
            #    sayerr("fusion failed!")
            #say("here again")
            #stop
            else:
                simple_copy(FreeCAD.activeDocument().getObject(FusionName))
                FreeCADGui.ActiveDocument.getObject(FusionName).Visibility=False
                FreeCAD.ActiveDocument.ActiveObject.Label=original_label+"_sp"      
                FreeCAD.ActiveDocument.recompute()
        else:
            say_select_obj()
        
def go_export(fPathName):
    global exportV, exportS
    sel = FreeCADGui.Selection.getSelection()
    if not sel:
        FreeCAD.Console.PrintWarning("Select something first!\n\n")
        msg="export VRML from FreeCAD is a python macro that will export simplified VRML of "
        msg+="a (multi)selected Part or fused Part to VRML optimized to Kicad and compatible with Blender "
        msg+="the size of VRML is much smaller compared to the one exported from FC Gui "
        msg+="and the loading/rendering time is also smaller\n"
        msg+="change mesh deviation to increase quality of VRML"
        say(msg)
    else:
        objs = []
        #check_AP()
        sel = FreeCADGui.Selection.getSelection()
        for obj in sel:
            FreeCADGui.Selection.removeSelection(obj)
        wrl_selected=False
        say(sel[0].Label)
        lbl=sel[0].Label
        for obj in sel:
            if not 'App::VRMLObject' in obj.TypeId:
                if 'App::Part' in obj.TypeId:
                    for o in obj.Group:
                        if 'Part' in obj.TypeId:
                            objs.append(o)
                else:
                    objs.append(obj)
                    #say(obj.Label)
                    #say(obj.Name)
            else:
                wrl_selected=True
        if wrl_selected==False:
            say(fPathName)
            # say(objs[0].Label)
            # lbl=objs[0].Label
            #say(objs)
            #export(objs, fullFilePathName, scale=None, lbl=None)
            export(objs, fPathName, 0.3937, lbl)
            align_colors_to_materials(objs)
            if len(objs) == 1 or 'App::Part' in sel[0].TypeId:
                exportS=True
                if 'App::Part' in sel[0].TypeId:
                    exportStep([sel[0]], fPathName)
                    # need to refresh color changing
                    FreeCADGui.Selection.addSelection(sel[0])
                    #FreeCADGui.Selection.clearSelection()
                else:
                    exportStep(objs, fPathName)
            else:
                #say("Select ONE single part object !")
                exportS=False
                #QtGui.QMessageBox.information(None,"Info ...","Select ONE single part object !\r\n"+"\r\n")
        else:
            exportS=False;exportV=False
            say("Do not select VRML object(s)!")
            say_single_obj()
        #lbl='empty'
        #if len(objs)>0:
        #    lbl=objs[0].Label
        return lbl
###
def align_colors_to_materials(objects):
    global exportS, applymaterials, enable_materials
    global color_list, color_list_mat
    
    newobj_list= objects
    
    if align_vrml_step_colors and  enable_materials == 1: #(applymaterials==1):
        sayw('aligning VRML colors to Materials')
        applyDiffuse=0
        color_vector=[]
        for obj in newobj_list: #objs:
            color_vector=[]
            shape1=obj.Shape
            single_color=FreeCADGui.ActiveDocument.getObject(obj.Name).DiffuseColor
            if(len(single_color)!=len(shape1.Faces)):
                applyDiffuse=0;
                #copy color to all faces
            #else copy singular colors for faces
            else:
                applyDiffuse=1;
            for color in single_color:
                color_vector.append((color[0], color[1], color[2], color[3]))
            #sayw(color_vector)
            #sayerr (color_list)
            #sayw(color_list_mat)
            idx=0
            if 'color_list' in globals():
                for color in color_vector:
                    if color in color_list:
                        #sayerr('found')
                        pos = color_list.index(color)
                        #sayw(pos)
                        if color_list_mat[pos]!='as is':
                            if color_list_mat[pos] in material_properties_names:
                                pos2 = material_properties_names.index(color_list_mat[pos])
                                color_vector[idx]=material_properties_diffuse[pos2]
                        else:
                            color_vector[idx]=color
                    idx+=1
                if(applyDiffuse):
                    FreeCADGui.ActiveDocument.getObject(obj.Name).DiffuseColor=color_vector
                else:
                    #say(color_vector)
                    #FreeCADGui.ActiveDocument.getObject(obj.Name).ShapeColor=color_vector[0]
                    FreeCADGui.ActiveDocument.getObject(obj.Name).DiffuseColor=color_vector #[0]
                    FreeCADGui.ActiveDocument.getObject(obj.Name).Transparency=int(float(color_vector[0][3])*100)
    # end test aligning colors
##
##
def exportStep(objs, ffPathName):
    #Export fused object
    global exportS, applymaterials, enable_materials
    global color_list, color_list_mat
    
    #if applymaterials==1:
    #    sayw(color_list); sayw(color_list_mat)
    
    exp_name=objs[0].Label
    #removing not allower chars
    translation_table = dict.fromkeys(map(ord, '<>:"/\|?*,;:\\'), None)
    exp_name=exp_name.translate(translation_table)
    path, fname = os.path.split(ffPathName)
    #fname=os.path.splitext(fname)[0]
    prefs = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/kicadStepUpGui")
    if prefs.GetBool('stpz_export_enabled'):
        #'stpz'
        fullFilePathNameStep=path+os.sep+exp_name+'.stpZ'
        #print('stpZ',fullFilePathNameStep)
    else:
        #not 'stpz'
        fullFilePathNameStep=path+os.sep+exp_name+'.step'
    exportS=True
    if os.path.exists(fullFilePathNameStep):
        say('file exists')
        QtGui.QApplication.restoreOverrideCursor()
        reply = QtGui.QMessageBox.question(None, "Info", fullFilePathNameStep+"\nstep file exists, overwrite?",
        QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            # this is where the code relevant to a 'Yes' answer goes
            exportS=True
            pass
        if reply == QtGui.QMessageBox.No:
            # this is where the code relevant to a 'No' answer goes
            exportS=False
            pass
    if exportS:
        ## resetting placement TBD for Part & Shape
        if 'App::Part' not in objs[0].TypeId:
            ## evaluate to modify reset placement 
            base_shape = FreeCAD.ActiveDocument.getObject(objs[0].Name)
            if base_shape.Placement.Base != FreeCAD.Vector(0,0,0) or base_shape.Placement.Rotation != FreeCAD.Rotation (0.0, 0.0, 0.0, 1.0):
                newobj=reset_prop_shapes(FreeCAD.ActiveDocument.getObject(objs[0].Name),FreeCAD.ActiveDocument, FreeCAD,FreeCADGui)
                new_name=FreeCAD.ActiveDocument.ActiveObject.Name
            else:
                newobj=objs[0]
                new_name=objs[0].Name
            #newobj.Label="TEST"
            newobj_list=[FreeCAD.ActiveDocument.getObject(new_name)]
        else:
            import kicadStepUpCMD
            FreeCADGui.Selection.addSelection(FreeCAD.ActiveDocument.getObject(objs[0].Name))
            kicadStepUpCMD.ksuToolsResetPartPlacement.Activated(FreeCAD.ActiveDocument.getObject(objs[0].Name))
            newobj_list=[FreeCAD.ActiveDocument.getObject(objs[0].Name)]
        
        #test aligning colors
        
        # reducing STEP file size
        #NB WriteSurfaceCurveMode parameter get after FC close-reopen
        # paramGet = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/Part/General")
        # paramGet.SetInt("WriteSurfaceCurveMode", 1)
        #paramGet = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/Part/General")
        #paramGet.SetInt("WriteSurfaceCurveMode", 0)
        paramGet = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/Part/STEP")
        old_Auth = paramGet.GetString("Author")
        old_Comp = paramGet.GetString("Company")
        # old_Prod = paramGet.GetString("Product")
        paramGet.SetString("Author", "kicad StepUp")
        paramGet.SetString("Company", "ksu MCAD")
        paramGet = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/Part/STEP")
        #old_Scheme = paramGet.GetString("Scheme")
        #if old_Scheme != 'AP214CD':
        #    paramGet.SetString("Scheme", "AP214CD")
        #paramGetVS1 = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/Import/hSTEP")
        #old_hScheme1 = paramGetVS1.GetBool("Scheme_203")
        #paramGetVS2 = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/Import/hSTEP")
        #old_hScheme2 = paramGetVS2.GetBool("Scheme_214")
        #sayw (old_hScheme1)
        #sayw (old_hScheme2)
        #sayw (old_Scheme)
        #stop
        #if old_hScheme1:
        #    paramGetVS1.SetBool("Scheme_203",0)
        #if not old_hScheme2:
        #    paramGetVS2.SetBool("Scheme_214",1)
        ##  not to be used paramGet.SetString("Product", "Open CASCADE STEP processor 7.0")
        #print(fullFilePathNameStep)
        #stop
        if fullFilePathNameStep.endswith('stpZ'):
            try:
                import stepZ
                stepZ.export(newobj_list,fullFilePathNameStep)
            except:
                sayerr('.stpZ not supported!')
        else:
            ImportGui.export(newobj_list,fullFilePathNameStep)
        #del __objs__ 
        say(fullFilePathNameStep+' written')
        ##ImportGui.export(objs,fullFilePathNameStep)
        #restoring old Author
        #paramGet = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/Part/STEP")
        paramGet.SetString("Author", old_Auth)
        paramGet.SetString("Company", old_Comp)
        ##if old_Scheme != 'AP214CD':
        ##    paramGet.SetString("Scheme",old_Scheme)
        ##if old_hScheme1:
        ##    paramGetVS1.SetBool("Scheme_203",1)
        ##    paramGetVS2.SetBool("Scheme_214",1)
        # paramGet.SetString("Product", old_Prod)
        #say(old_Auth)
        #say(old_Comp)
        FreeCAD.activeDocument().recompute()
    return
###

home = expanduser("~")
#QtGui.QMessageBox.information(None,"info ...","your home path is \r\n"+ home+"\r\n")
sayw("KiCAD 2STEP version "+str(___ver___))
#say("tolerance on vertex = "+str(edge_tolerance))
say("tolerance on vertex applied")
if apply_light==True:
    say("applying Lights")
if apply_reflex==True:
    say("applying Materials to Shapes")
say("your home path is "+ home)
fname_ksu=home+os.sep+'ksu-config.ini'
ksu_config_fname=fname_ksu

#!#   default_ksu_config_ini=u"""[info]
#!#   ;; kicad StepUp tools config file utf-8
#!#   ;; each line starting with a semicolon is a comment
#!#   [prefix3D]
#!#   ;; put here your KISYS3DMOD path or 3D model prefix path or 3D Alias
#!#   ;; only TWO prefixs are allowed; MUST finish with slash or backslash
#!#   ;prefix3D_1 = C:\\Program Files\\KiCad\share\\kicad\\modules\\packages3d\\
#!#   ;prefix3D_1 = kicad/share/modules/packages3d/
#!#   ;prefix3D_1 = /Library/Application Support/kicad/modules/packages3d/
#!#   ;prefix3D_2 = C:\\extra_packages3d\\
#!#   prefix3D_1 = C:\\Program Files\\KiCad\share\\kicad\\modules\\packages3d\\
#!#   prefix3D_2 = kicad/share/modules/packages3d/
#!#   [PcbColor]
#!#   ;; pcb color r,g,b e.g. 0.0,0.5,0.0,light green
#!#   ;pcb_color=0.3333,0.3333,0.5,blue
#!#   ;pcb_color=0.0,0.5,0.0,light green
#!#   ;pcb_color = 1.0,0.1,0.0,red (255,25,0)
#!#   pcb_color=0.0,0.298,1.0,lightblue (0,76,255)
#!#   ;pcb_color=0.211,0.305,0.455,darkblue (54,79,116)
#!#   [Blacklist]
#!#   ;; put here your model names that you don't want to load (e.g. smallest ones)
#!#   ;; separated by a comma (none means all the models will be parsed)
#!#   ;; (volume=1 means all models with a volume < 1mm3 will not be included)
#!#   ;; (height=1 means all models with a height < 1mm  will not be included)
#!#   ;bklist = r_0603,r_0402,c_0402,c_0603
#!#   ;bklist = height=1.0
#!#   ;bklist = volume=1.0
#!#   ;bklist = none
#!#   bklist = none
#!#   [BoundingBox]
#!#   ;; bounding box option LIST=>whitelist (not converted to bbox)
#!#   ;bbox = LIST dpak-to252,sod80
#!#   ;bbox = ALL
#!#   ;bbox = off default
#!#   bbox = off default
#!#   [Placement]
#!#   ;; placement options
#!#   ;placement options: useGridOrigin, useAuxOrigin, useBaseOrigin, useBasePoint;x;y, usedefault, +AutoAdjust
#!#   ;placement = useGridOrigin
#!#   ;placement = useAuxOrigin
#!#   ;placement = useAuxOrigin +AutoAdjust
#!#   ;placement = useBasePoint;37.0;50.0;
#!#   ;placement = useBasePoint;37.0;50.0; +AutoAdjust
#!#   ;placement = useBaseOrigin #place board @ 0,0,0
#!#   ;placement = useBaseOrigin +AutoAdjust #place board @ 0,0,0
#!#   ;placement = usedefault
#!#   ;placement = usedefault +AutoAdjust
#!#   placement = useBaseOrigin #place board @ 0,0,0
#!#   [Virtual]
#!#   ;; virtual modules to be or not added to board
#!#   virt = addVirtual
#!#   ;virt = addVirtual
#!#   ;virt = noVirtual
#!#   [ExportFuse]
#!#   ;; fuse modules to board
#!#   ;; be careful ... fusion can be heavy or generate FC crash with a lot of objects
#!#   ;; please consider to use bbox or blacklist small objs
#!#   ;exportFusing = fuseAll
#!#   ;exportFusing = nofuse  #default
#!#   exportFusing = nofuse  #default
#!#   [minimum_drill_size]
#!#   ;; minimum drill size to be handled 
#!#   ;; set 0.0 to handle all sizes
#!#   min_drill_size = 0.0
#!#   [last_pcb_path]
#!#   ;; last pcb file path used
#!#   last_pcb_path =
#!#   [last_footprint_path]
#!#   ;; last footprint file path used
#!#   last_fp_path =
#!#   [export]
#!#   export_to_STEP = yes
#!#   ;; export to STEP 
#!#   ;export_to_STEP = yes
#!#   ;export_to_STEP = no
#!#   [Materials]
#!#   mat = enablematerials
#!#   ;; VRML models to be or not exported with material properties
#!#   ;mat = enablematerials
#!#   ;mat = nomaterials
#!#   [turntable]
#!#   spin = disabled
#!#   ;;turntable spin after loading
#!#   ;spin = disabled
#!#   ;spin = enabled
#!#   [compound]
#!#   compound = allowed
#!#   ;;allow compound for STEP models
#!#   ;compound = allowed
#!#   ;compound = disallowed
#!#   ;compound = simplified
#!#   [docking]
#!#   dkmode = right
#!#   ;;docking mode
#!#   ;dkmode = left
#!#   ;dkmode = right
#!#   ;dkmode = float
#!#   [sketch_constraints]
#!#   constraints = all
#!#   ;constraints = all
#!#   ;constraints = coincident
#!#   ;constraints = none
#!#   ;;constraints generated for pcb sketch
#!#   [step_exporting_mode]
#!#   exporting_mode = hierarchy
#!#   ;exporting_mode = hierarchy
#!#   ;exporting_mode = flat
#!#   ;exporting_mode = onelevel
#!#   ;;step exporting mode
#!#   [links_importing_mode]
#!#   importing_mode = standard
#!#   ;importing_mode = links
#!#   ;importing_mode = standard
#!#   ;;models importing mode: use Assembly3 Links or Standard mode
#!#   [fonts]
#!#   font_size = 8
#!#   ;;font size for ksu widget
#!#   """

def cfg_read_all():
    global ksu_config_fname, default_ksu_config_ini, applymaterials
    ##ksu pre-set
    global models3D_prefix, models3D_prefix2, models3D_prefix3, models3D_prefix4
    global blacklisted_model_elements, col, colr, colg, colb
    global bbox, volume_minimum, height_minimum, idf_to_origin, aux_orig
    global base_orig, base_point, bbox_all, bbox_list, whitelisted_model_elements
    global fusion, addVirtual, blacklisted_models, exportFusing, min_drill_size
    global last_fp_path, last_pcb_path, plcmnt, xp, yp, exportFusing, export_board_2step
    global enable_materials, docking_mode, mat_section, dock_section, compound_section, turntable_section
    global font_section, ini_vars, num_min_lines, animate_result, allow_compound, font_size, grid_orig
    global constraints_section, addConstraints, exporting_mode_section, stp_exp_mode
    global links_importing_mode_section, links_imp_mode, generate_sketch, edge_tolerance
    
#!#   import os, sys, re
#!#   from sys import platform as _platform
#!#   
#!#   # window GUI dimensions parameters
#!#   pt_lnx = False;pt_osx = False;pt_win = False;
#!#   if _platform == "linux" or _platform == "linux2":
#!#       # linux
#!#       pt_lnx = True
#!#       default_prefix3d = '/usr/share/kicad/modules/packages3d'
#!#       #'/usr/share/kicad/modules/packages3d'
#!#   elif _platform == "darwin":
#!#       #osx
#!#       pt_osx = True
#!#       default_prefix3d = '/Library/Application Support/kicad/packages3d' 
#!#       #/Library/Application Support/kicad/modules/packages3d/' wrong location
#!#   else:
#!#       # Windows
#!#       pt_win = True
#!#       #default_prefix3d = os.path.join(os.environ["ProgramFiles"],u'\\KiCad\\share\\kicad\\modules\\packages3d')
#!#       default_prefix3d = (os.environ["ProgramFiles"]+u'\\KiCad\\share\\kicad\\modules\\packages3d')
#!#       #print (default_prefix3d)
#!#       default_prefix3d = re.sub("\\\\", "/", default_prefix3d) #default_prefix3d.replace('\\','/')
#!#       #print (default_prefix3d)

    prefs = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/kicadStepUpGui")
    ## if prefs.GetContents() is not None:
    ##     for i,p in enumerate (prefs.GetContents()):
    ##         print (p)
    ## else:
    ##     print('preferences null')
    # print (prefs)
    # for i,p in enumerate (prefs.GetContents()):
    #     print (p)
    # stop
    
    #if prefs.GetContents() is None:
    #    print('Creating first time ksu preferences')
    #    stop #TBD
    #else:
    #    for i,p in enumerate (prefs.GetContents()):
    #        print (p)
            
    models3D_prefix = prefs.GetString('prefix3d_1')
    
    # sayw(prefs.GetString('prefix3d_1'))
    # sayw(prefs.GetString('prefix3d_2'))
    # sayw(prefs.GetString('prefix3d_3'))
    # sayw(prefs.GetString('prefix3d_4'))
    
#!#   if len (models3D_prefix) == 0:
#!#       prefs.SetString('prefix3d_1',make_string(default_prefix3d))
#!#       models3D_prefix = prefs.GetString('prefix3d_1')
    models3D_prefix2 = prefs.GetString('prefix3d_2')
    models3D_prefix3 = prefs.GetString('prefix3d_3')
    models3D_prefix4 = prefs.GetString('prefix3d_4')
    light_green = [0.20,0.60,0.40] # std Green
    blue = [0.13,0.40,0.73] # Deep Sea Blue
    red = [1.0,0.16,0.0] # Ferrari Red
    purple = [0.498,0.090,0.424] # oshpark purple #6D0A8E
    darkgreen = [0.180,0.373,0.275] # (45,95,70)
    darkblue = [0.211,0.305,0.455] # (54,79,116)
    lightblue = [0.0,0.298,1.0] # (0,76,255)
    yellow = [0.98,0.98,0.34] #sunshine yellow
    black = [0.18,0.18,0.18] #slick black
    white = [0.973,0.973,0.941] #[0.98,0.92,0.84] #antique white
    pcb_color_values = [light_green,blue,red,purple,darkgreen,darkblue,lightblue,yellow,black,white]
    pcb_color_pos = prefs.GetInt('pcb_color')
    pcb_color = pcb_color_values [pcb_color_pos]
    col = []
    col.append(pcb_color[0]);col.append(pcb_color[1]);col.append(pcb_color[2])
    colr=col[0];colg=col[1];colb=col[2]
    #print(colr,colg,colb)
    try:
        min_drill_size = float(prefs.GetString('drill_size'))
    except:
        min_drill_size = 0.0
    try:
        edge_tolerance = float(prefs.GetString('edge_tolerance'))
    except:
        edge_tolerance = 0.01
    #print(min_drill_size)
    if prefs.GetBool('vrml_materials'):
        enable_materials=1
    else:
        enable_materials=0
    if prefs.GetBool('mode_virtual'):
        addVirtual=1
    else:
        addVirtual=0
    fusion = prefs.GetBool('make_union')
    export_board_2step = prefs.GetBool('exp_step')
    animate_result = prefs.GetBool('turntable')
    generate_sketch = prefs.GetBool('generate_sketch')
    if prefs.GetBool('asm3_links'):
        links_imp_mode = 'links_allowed'
    else:
        links_imp_mode = 'links_not_allowed'
    if prefs.GetBool('asm3_linkGroups'):
        use_LinkGroups = True
    else:
        use_LinkGroups = False
    aux_orig=0;base_orig=0;base_point=0; grid_orig=0
    #grid_orig -> 0; aux_orig-> 1; base_orig -> 2
    pcb_placement = prefs.GetInt('pcb_placement')
    if pcb_placement == 0:
        grid_orig = 1
    elif pcb_placement == 1:
        aux_orig = 1
    else:
        base_orig = 1
    step_exp_mode = prefs.GetInt('step_exp_mode')    
    if step_exp_mode == 0:
        stp_exp_mode = 'hierarchy'
    elif step_exp_mode == 1:
        stp_exp_mode = 'flat'
    else:
        stp_exp_mode = 'onelevel'
    m3D_loading_mode = prefs.GetInt('3D_loading_mode')
    if m3D_loading_mode == 0: #old Standard
        #allow_compound = 'True' #old Standard
        allow_compound = 'Hierarchy' #full hierarchy allowed
        if 'LinkView' not in dir(FreeCADGui):
            allow_compound = 'True' #old Standard
            sayw('Links not allowed... \nfalling from Hierarchy to Compound')
    elif m3D_loading_mode == 1:
        allow_compound = 'Simplified'
    elif m3D_loading_mode == 2:
        allow_compound = 'False' #NotAllowedMultiParts
    else:
        #allow_compound = 'Hierarchy' #full hierarchy allowed
        allow_compound = 'True' #old Standard
    sketch_constraints = prefs.GetInt('sketch_constraints')
    if sketch_constraints == 1:
        addConstraints='all'
    elif sketch_constraints == 0:
        addConstraints='coincident'
    elif sketch_constraints == 2:
        addConstraints='full'
    else:
        addConstraints='none'
    bbox_all=0; bbox_list=0; whitelisted_model_elements=''
    bbox_opt = prefs.GetString('bbox_list')
    if bbox_opt.upper().find('ALL') !=-1:
        bbox_all=1
        whitelisted_model_elements=''
    elif bbox_opt.upper().find('LIST') !=-1:
        bbox_list=1
        whitelisted_model_elements=bbox_opt.strip('\r\n')
        #whitelisted_models=whitelisted_model_elements.split(",")
    #elif len(bbox_opt) > 0:
        
    bbox=0;blacklisted_model_elements=''
    volume_minimum=0. #0.8  ##1 #mm^3, 0 skipped #global var default
    height_minimum=0. #0.8  ##1 #mm, 0 skipped   #global var default
    bklist = prefs.GetString('blacklist')
    bkl_none=False
    if bklist.lower().find('none') !=-1 or len(bklist) == 0:
        blacklisted_model_elements=''
        bkl_none=True
    if bklist.lower().find('volume=') !=-1 and not bkl_none:
        vval=bklist.strip('\r\n')
        bklist_s=bklist
        vvalst=vval.split(";")
        #print(vvalst)
        for l in vvalst:
            #print(l)
            if l.lower().find('volume=') !=-1:
                vvalue=l.split("=")
                volume_minimum=float(vvalue[1].replace(',','.'))
                #print(height_minimum)
                bklist_s=bklist.strip(l)
                #if l.lower().find(';height=') !=-1: 
                #    bklist=bklist.strip(';'+l)
                #else:
                #    bklist=bklist.strip(l+';')
        #print(bklist)
        bklist_n=[x for x in bklist_s.split(";") if x]
        #print('bklist_n',bklist_n)
        ##removing empty elements
        bklist=''
        for bm in bklist_n:
            bklist+=bm+';'
        #vvalue=vval.split("=")
        #height_minimum=float(vvalue[1])
        #reply = QtGui.QMessageBox.information(None,"info ...","height "+str(height_minimum))
        #vvalue=vval.split("=")
        #volume_minimum=float(vvalue[1])
        #reply = QtGui.QMessageBox.information(None,"info ...","volume "+str(volume_minimum))
    #print('bklist 1',bklist)
    if bklist.lower().find('height=') !=-1 and not bkl_none:
        vval=bklist.strip('\r\n')
        bklist_s=bklist
        vvalst=vval.split(";")
        #print(vvalst)
        for l in vvalst:
            #print(l)
            if l.lower().find('height=') !=-1:
                vvalue=l.split("=")
                height_minimum=float(vvalue[1].replace(',','.'))
                #print(height_minimum)
                bklist_s=bklist.strip(l)
                #if l.lower().find(';height=') !=-1: 
                #    bklist=bklist.strip(';'+l)
                #else:
                #    bklist=bklist.strip(l+';')
        #print(bklist)
        bklist_n=[x for x in bklist.split(";") if x]
        #print(bklist_n)
        ##removing empty elements
        bklist=''
        for bm in bklist_n:
            bklist+=bm+';'
        #vvalue=vval.split("=")
        #height_minimum=float(vvalue[1])
        #reply = QtGui.QMessageBox.information(None,"info ...","height "+str(height_minimum))
    if bklist.find(';') !=-1 and not bkl_none:
        blacklisted_model_elements=bklist.strip('\r\n')
        #say(bklist);
        bklist_m=[x for x in blacklisted_model_elements.split(";") if x]
        ##removing empty elements
        #blacklisted_models=blacklisted_model_elements.split(";")
        blacklisted_models= bklist_m
        #say(blacklisted_models)
    #print('bklist',bklist,'height_minimum',height_minimum,'volume_minimum',volume_minimum)
    pg = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/kicadStepUp")
    dock_mode = pg.GetInt("dockingMode")
    if dock_mode == 0:
        docking_mode='float'
    elif dock_mode == 1:
        docking_mode='left'
    else:
        docking_mode='right'
    idf_to_origin = True
    pg = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/kicadStepUp")
    last_pcb_path = pg.GetString("last_pcb_path")
    last_fp_path = pg.GetString("last_fp_path")
            
    #stop
    
##
#!# END - cfg_read_all()

#ini_content=read_ini_file()
#!# ini_content=cfg_read_all()
cfg_read_all()


#ini_vars[2]=u'd:\extrà3D'
#print cfg_get('prefix3D','prefix3d_2')
#cfg_read_all()
# cfg_update_all()
# stop

#time.sleep(0.5)
# configParser = ConfigParser.RawConfigParser()  
# configParser = ConfigParser.ConfigParser(allow_no_value = True) 
# configFilePath = ksu_config_fname
# cfgParsRead(configFilePath)

#assign params

def say_time():
    global running_time
    
    end_milli_time = current_milli_time()
    running_time=(end_milli_time-start_time)/1000
    msg="running time: "+str(round(running_time,3))+"sec"
    say(msg)
###

def get_time():
    global running_time
    
    end_milli_time = current_milli_time()
    running_time=(end_milli_time-start_time)/1000
    #msg="running time: "+str(running_time)+"sec"
    #say(msg)
###

#!#def reset_prop(obj,doc,App,Gui):
#!#   #say('resetting props')
#!#   ##try:
#!#   newObj =FreeCAD.ActiveDocument.addObject('Part::Feature',obj.Name)
#!#   newObj.Shape=FreeCAD.ActiveDocument.getObject(obj.Name).Shape
#!#   FreeCAD.ActiveDocument.ActiveObject.Label=FreeCAD.ActiveDocument.getObject(obj.Name).Label
#!#   #tsp = FreeCADGui.ActiveDocument.ActiveObject.Transparency=FreeCADGui.ActiveDocument.getObject(obj.Name).Transparency
#!#   final_Label=FreeCAD.ActiveDocument.getObject(obj.Name).Label
#!#   #say(final_Label)
#!#   FreeCADGui.ActiveDocument.ActiveObject.ShapeColor=FreeCADGui.ActiveDocument.getObject(obj.Name).ShapeColor
#!#   FreeCADGui.ActiveDocument.ActiveObject.LineColor=FreeCADGui.ActiveDocument.getObject(obj.Name).LineColor
#!#   FreeCADGui.ActiveDocument.ActiveObject.PointColor=FreeCADGui.ActiveDocument.getObject(obj.Name).PointColor
#!#   FreeCADGui.ActiveDocument.ActiveObject.DiffuseColor=FreeCADGui.ActiveDocument.getObject(obj.Name).DiffuseColor
#!#   FreeCAD.ActiveDocument.recompute()
#!#   newObjCommon=FreeCAD.activeDocument().addObject("Part::MultiCommon","Common")
#!#   newObjCommon.Shapes = [FreeCAD.activeDocument().getObject(obj.Name),FreeCAD.activeDocument().getObject(newObj.Name),]
#!#   FreeCADGui.activeDocument().getObject(obj.Name).Visibility=False
#!#   FreeCADGui.activeDocument().getObject(newObj.Name).Visibility=False
#!#   FreeCADGui.ActiveDocument.Common.ShapeColor=FreeCADGui.ActiveDocument.getObject(obj.Name).ShapeColor
#!#   FreeCADGui.ActiveDocument.Common.DisplayMode=FreeCADGui.ActiveDocument.getObject(obj.Name).DisplayMode
#!#   FreeCAD.ActiveDocument.recompute()
#!#   # sleep
#!#   FreeCAD.ActiveDocument.addObject('Part::Feature','Common').Shape=FreeCAD.ActiveDocument.Common.Shape
#!#   FreeCAD.ActiveDocument.ActiveObject.Label=final_Label
#!#   rstObj=FreeCAD.ActiveDocument.ActiveObject
#!#   #
#!#   FreeCADGui.ActiveDocument.ActiveObject.ShapeColor=FreeCADGui.ActiveDocument.Common.ShapeColor
#!#   FreeCADGui.ActiveDocument.ActiveObject.LineColor=FreeCADGui.ActiveDocument.Common.LineColor
#!#   FreeCADGui.ActiveDocument.ActiveObject.PointColor=FreeCADGui.ActiveDocument.Common.PointColor
#!#   FreeCADGui.ActiveDocument.ActiveObject.DiffuseColor=FreeCADGui.ActiveDocument.Common.DiffuseColor
#!#   #FreeCADGui.ActiveDocument.ActiveObject.Transparency=tsp
#!#   FreeCAD.ActiveDocument.removeObject("Common")
#!#   FreeCAD.ActiveDocument.recompute()
#!#   #
#!#   return rstObj
###
def reset_prop_shapes(obj,doc,App,Gui,rmv=None):

    s=obj.Shape
    #say('resetting props #2')
    r=[]
    t=s.copy()
    for i in t.childShapes():
        #print t.childShapes
        c=i.copy()
        c.Placement=t.Placement.multiply(c.Placement)
        r.append((i,c))

    w=t.replaceShape(r)
    w.Placement=FreeCAD.Placement()
    Part.show(w)
    #w1 = Part.Solid(w)
    #Part.show(w1)
    #say(w)
    #
    FreeCADGui.ActiveDocument.ActiveObject.ShapeColor=FreeCADGui.ActiveDocument.getObject(obj.Name).ShapeColor
    FreeCADGui.ActiveDocument.ActiveObject.LineColor=FreeCADGui.ActiveDocument.getObject(obj.Name).LineColor
    FreeCADGui.ActiveDocument.ActiveObject.PointColor=FreeCADGui.ActiveDocument.getObject(obj.Name).PointColor
    FreeCADGui.ActiveDocument.ActiveObject.DiffuseColor=FreeCADGui.ActiveDocument.getObject(obj.Name).DiffuseColor
    FreeCADGui.ActiveDocument.ActiveObject.Transparency=FreeCADGui.ActiveDocument.getObject(obj.Name).Transparency
    #FreeCADGui.ActiveDocument.ActiveObject.ShapeColor=FreeCADGui.ActiveDocument.getObject(obj.Name).ShapeColor
    #FreeCADGui.ActiveDocument.ActiveObject.LineColor=FreeCADGui.ActiveDocument.getObject(obj.Name).LineColor
    #FreeCADGui.ActiveDocument.ActiveObject.PointColor=FreeCADGui.ActiveDocument.getObject(obj.Name).PointColor
    #FreeCADGui.ActiveDocument.ActiveObject.DiffuseColor=FreeCADGui.ActiveDocument.getObject(obj.Name).DiffuseColor
    new_label=make_string(obj.Label)
    #if (obj.TypeId == 'App::Part'):
    #    removesubtree(obj)
    #else:
    #    FreeCAD.ActiveDocument.removeObject(obj.Name)
    # if 0:
    #     FreeCAD.ActiveDocument.removeObject(obj.Name)
    # else:
    say('renaming not in Origin object')
    if rmv == True:
        FreeCAD.ActiveDocument.removeObject(obj.Name)
    else:
        FreeCAD.ActiveDocument.getObject(obj.Name).ViewObject.Visibility = False
        FreeCAD.ActiveDocument.getObject(obj.Name).Label = new_label + '_'
    FreeCAD.ActiveDocument.recompute()
    FreeCAD.ActiveDocument.ActiveObject.Label=new_label
    rstObj=FreeCAD.ActiveDocument.ActiveObject
    #say(rstObj)
    #

    return rstObj
###
#!#def reset_prop_shapes2(obj,doc,App,Gui):
#!#
#!#   s=obj.Shape
#!#   #say('resetting props #2')
#!#   r=[]
#!#   t=s.copy()
#!#   for i in t.childShapes():
#!#       c=i.copy()
#!#       c.Placement=t.Placement.multiply(c.Placement)
#!#       r.append((i,c))
#!#
#!#   w=t.replaceShape(r)
#!#   w.Placement=FreeCAD.Placement()
#!#   Part.show(w)
#!#   #say(w)
#!#   #
#!#   #FreeCADGui.ActiveDocument.ActiveObject.ShapeColor=FreeCADGui.ActiveDocument.Part__Feature.ShapeColor
#!#   #FreeCADGui.ActiveDocument.ActiveObject.LineColor=FreeCADGui.ActiveDocument.Part__Feature.LineColor
#!#   #FreeCADGui.ActiveDocument.ActiveObject.PointColor=FreeCADGui.ActiveDocument.Part__Feature.PointColor
#!#   #FreeCADGui.ActiveDocument.ActiveObject.DiffuseColor=FreeCADGui.ActiveDocument.Part__Feature.DiffuseColor
#!#   FreeCADGui.ActiveDocument.ActiveObject.ShapeColor=FreeCADGui.ActiveDocument.getObject(obj.Name).ShapeColor
#!#   FreeCADGui.ActiveDocument.ActiveObject.LineColor=FreeCADGui.ActiveDocument.getObject(obj.Name).LineColor
#!#   FreeCADGui.ActiveDocument.ActiveObject.PointColor=FreeCADGui.ActiveDocument.getObject(obj.Name).PointColor
#!#   FreeCADGui.ActiveDocument.ActiveObject.DiffuseColor=FreeCADGui.ActiveDocument.getObject(obj.Name).DiffuseColor
#!#   #FreeCADGui.ActiveDocument.ActiveObject.Transparency=FreeCADGui.ActiveDocument.getObject(obj.Name).Transparency
#!#   new_label=obj.Label
#!#   FreeCAD.ActiveDocument.removeObject(obj.Name)
#!#   FreeCAD.ActiveDocument.recompute()
#!#   FreeCAD.ActiveDocument.ActiveObject.Label=new_label
#!#   rstObj=FreeCAD.ActiveDocument.ActiveObject
#!#   #say(rstObj)
#!#   #
#!#
#!#   return rstObj
###
def copy_objs(obj,doc):

    FreeCAD.ActiveDocument.addObject('Part::Feature',obj.Label).Shape=obj.Shape
    #App.ActiveDocument.ActiveObject.Label=obj.Label
    
    FreeCADGui.ActiveDocument.ActiveObject.ShapeColor=FreeCADGui.ActiveDocument.getObject(obj.Name).ShapeColor
    FreeCADGui.ActiveDocument.ActiveObject.LineColor=FreeCADGui.ActiveDocument.getObject(obj.Name).LineColor
    FreeCADGui.ActiveDocument.ActiveObject.PointColor=FreeCADGui.ActiveDocument.getObject(obj.Name).PointColor
    FreeCADGui.ActiveDocument.ActiveObject.DiffuseColor=FreeCADGui.ActiveDocument.getObject(obj.Name).DiffuseColor
    #FreeCADGui.ActiveDocument.ActiveObject.Transparency=FreeCADGui.ActiveDocument.getObject(obj.Name).Transparency
    FreeCAD.ActiveDocument.recompute()
    #App.ActiveDocument.ActiveObject.ViewObject.Visibility = False
    
    return FreeCAD.ActiveDocument.ActiveObject
###

#!#def copy_objs_BAD(obj,doc,App,Gui):
#!#
#!#   #cpObj = App.ActiveDocument.addObject('Part::Feature', obj.Label+"cp_")
#!#   #cpObj.Shape = obj.Shape
#!#   #cpObj.Label = obj.Label + "_cp"
#!#   #App.ActiveDocument.addObject('Part::Feature',obj.Label+"cp_").Shape=obj.Shape
#!#   App.ActiveDocument.addObject('Part::Feature',obj.Label).Shape=obj.Shape
#!#   #App.ActiveDocument.ActiveObject.Label=obj.Label
#!#   
#!#   Gui.ActiveDocument.ActiveObject.ShapeColor=Gui.ActiveDocument.getObject(obj.Name).ShapeColor
#!#   Gui.ActiveDocument.ActiveObject.LineColor=Gui.ActiveDocument.getObject(obj.Name).LineColor
#!#   Gui.ActiveDocument.ActiveObject.PointColor=Gui.ActiveDocument.getObject(obj.Name).PointColor
#!#   Gui.ActiveDocument.ActiveObject.DiffuseColor=Gui.ActiveDocument.getObject(obj.Name).DiffuseColor
#!#   App.ActiveDocument.recompute()
#!#   #App.ActiveDocument.ActiveObject.ViewObject.Visibility = False
#!#   
#!#   return App.ActiveDocument.ActiveObject
###
def createSolidBBox3(objIn):
    s = objIn.Shape
    name=objIn.Label
    FreeCAD.Console.PrintMessage(name+" name ")
    FreeCAD.activeDocument().removeObject(objIn.Name)
    # boundBox
    boundBox_ = s.BoundBox
    boundBoxLX = boundBox_.XLength
    boundBoxLY = boundBox_.YLength
    boundBoxLZ = boundBox_.ZLength
    a = str(boundBox_)
    a,b = a.split('(')
    c = b.split(',')
    oripl_X = float(c[0])
    oripl_Y = float(c[1])
    oripl_Z = float(c[2])
    #say(str(boundBox_))
    #say("Rectangle : "+str(boundBox_.XLength)+" x "+str(boundBox_.YLength)+" x "+str(boundBox_.ZLength))
    #say("_____________________")
    #say("x: "+str(oripl_X)+" y: "+str(oripl_Y)+"z: "+str(oripl_Z))
    obj=FreeCAD.ActiveDocument.addObject('Part::Feature',name)
    obj.Shape=Part.makeBox(boundBox_.XLength, boundBox_.YLength, boundBox_.ZLength, FreeCAD.Vector(oripl_X,oripl_Y,oripl_Z), FreeCAD.Vector(0,0,1))
    bbox_col=bbox_default_col
    if (obj.Name.upper().startswith('X')):
        bbox_col=bbox_x_col
    if (obj.Name.upper().startswith('L')):
        bbox_col=bbox_l_col
    if (obj.Name.upper().startswith('R')):
        bbox_col=bbox_r_col
    if (obj.Name.upper().startswith('C')):
        bbox_col=bbox_c_col
    if (obj.Name.upper().startswith('S')|obj.Name.upper().startswith('Q')|obj.Name.upper().startswith('D')|obj.Name.upper().startswith('T')):
        bbox_col=bbox_IC_col
    FreeCADGui.ActiveDocument.getObject(obj.Name).ShapeColor=bbox_col
    return obj
###
###
def createScaledBBox(name,scale):
    # type: box, cylV, cylH 
    say(name)
    if name == "box_mcad":
        type = "cube"
    if name == "cylV_mcad":
        type = "cylinder_vert"
    if name == "cylH_mcad":
        type = "cylinder_horz"
    say(type+" type")
    # boundBox
    boundBoxLX = float(scale[0])
    boundBoxLY = float(scale[1])
    boundBoxLZ = float(scale[2])
    #oripl_X = float(position[0])
    #oripl_Y = float(position[1])
    #oripl_Z = float(position[2])
    obj=FreeCAD.ActiveDocument.addObject('Part::Feature',name+"_")
    bbox_col=bbox_default_col
    if type == "cube":
    #makeBox(length,width,height,[pnt,dir]) – Make a box located in pnt with the dimensions (length,width,height) By default pnt=Vector(0,0,0) and dir=Vector(0,0,1)
        obj.Shape=Part.makeBox(boundBoxLX, boundBoxLY, boundBoxLZ, FreeCAD.Vector(-boundBoxLX/2,-boundBoxLY/2,0))
        bbox_col=bbox_r_col
# makeCylinder(radius,height,[pnt,dir,angle]) 
# Make a cylinder with a given radius and height By default pnt=Vector(0,0,0),dir=Vector(0,0,1) and angle=360
    if type == "cylinder_vert":
        obj.Shape=Part.makeCylinder(boundBoxLX/2, boundBoxLZ) #, FreeCAD.Vector(-boundBoxLX/2,-boundBoxLY/2,0))
        bbox_col=bbox_c_col
    if type == "cylinder_horz":
        obj.Shape=Part.makeCylinder(boundBoxLX/2, boundBoxLY, FreeCAD.Vector(0,-boundBoxLY/2,boundBoxLX/2), FreeCAD.Vector(0,1,0)) #, FreeCAD.Vector(-boundBoxLX/2,-boundBoxLY/2,0))
        bbox_col=bbox_default_col
    FreeCADGui.ActiveDocument.getObject(obj.Name).ShapeColor=bbox_col
    return obj
###

def Display_info(blacklisted_models):
    global bbox_all, bbox_list, fusion, show_messages, last_pcb_path
    global height_minimum, volume_minimum, idf_to_origin, ksu_config_fname
    global board_base_point_x, board_base_point_y, real_board_pos_x, real_board_pos_y
    global animate_result, apply_reflex, apply_reflex_all, addVirtual, fname_sfx
    global running_time, missingHeight
    
    say('info message')
    if blacklisted_model_elements != '':
        sayw("black-listed module \n"+ ''.join(map(str, blacklisted_models)))
        if (show_messages==True):
            QtGui.QApplication.restoreOverrideCursor()
            reply = QtGui.QMessageBox.information(None,"Info ...","... black-listed module(s)\r\n"+ ''.join(map(str, blacklisted_models)).replace(',','\n'))
        #FreeCAD.Console.PrintMessage("black-listed module "+ '\r\n'.join(map(str, blacklisted_models)))    
    
    msg="""<b>kicad StepUp</b> ver. """
    msg+=___ver___
    #if len(msgpath)>15:
    #    insert_return(msgpath, 15)
    if (idf_to_origin==True):
        new_pos_x=board_base_point_x+real_board_pos_x
        new_pos_y=board_base_point_y+real_board_pos_y
    else:
        new_pos_x=board_base_point_x
        new_pos_y=board_base_point_y
    if (grid_orig==1):
        msg+="<br>Board Placed @ "+"{0:.2f}".format(board_base_point_x)+";"+"{0:.2f}".format(board_base_point_y)+";0.0"
    else:
        msg+="<br>Board Placed @ "+"{0:.2f}".format(new_pos_x)+";"+"{0:.2f}".format(new_pos_y)+";0.0"
    msg+="<br>kicad pcb pos: ("+"{0:.2f}".format(real_board_pos_x)+";"+"{0:.2f}".format(real_board_pos_y)+";"+"{0:.2f}".format(0)+")"
    if (bbox_all==1) or (bbox_list==1):
        msg+="<br>bounding box modules applied"
    if (volume_minimum!=0):
        msg+="<br><b><font color=blue>modules with volume less than "+str(volume_minimum)+"mm^3 not included</font></b>"
    if (height_minimum!=0):
        msg+="<br><b><font color=blue>modules with height less than "+str(height_minimum)+"mm not included</font></b>"    
    if (min_drill_size>0):
        msg+="<br><b><font color=blue>drills with size less than "+str(min_drill_size)+"mm not included</font></b>"
    if (min_drill_size==-1):
        msg+="<br><b><font color=red>ALL via drills included</font></b>"
    if (compound_found):
        msg+="<br>found  <b><font color=red>multi-part</font></b></b> object(s)"
    if addVirtual==0:
        msg+="<br><b>Virtual models skipped</b>"
    #msg+="<br>kicad StepUp config file in:<br><b>"+ksu_config_fname+"</b><br>location."
    doc = FreeCAD.ActiveDocument
    pcb_name=u'Pcb'+fname_sfx
    pcb_bbx = doc.getObject(pcb_name).Shape.BoundBox
    msg+="<br>pcb dimensions: ("+"{0:.2f}".format(pcb_bbx.XLength)+";"+"{0:.2f}".format(pcb_bbx.YLength)+";"+"{0:.2f}".format(pcb_bbx.ZLength)+")"
    if missingHeight:
        msg+="<br><b><font color=red>MISSING pcb height from stack; forced 1.6mm value</font></b>"
    msg+="<br>running time: "+str(round(running_time,2))+"sec"
    msg+="<br>StepUp configuration options are located in the preferences system of FreeCAD."
    if (grid_orig==1):
        say("Board Placed @ "+"{0:.2f}".format(board_base_point_x)+";"+"{0:.2f}".format(board_base_point_y)+";0.0")
    else:
        say("Board Placed @ "+"{0:.2f}".format(new_pos_x)+";"+"{0:.2f}".format(new_pos_y)+";0.0")
    say("kicad pcb pos: ("+"{0:.2f}".format(real_board_pos_x)+";"+"{0:.2f}".format(real_board_pos_y)+";"+"{0:.2f}".format(0)+")")      
    say("pcb dimensions: ("+"{0:.2f}".format(pcb_bbx.XLength)+";"+"{0:.2f}".format(pcb_bbx.YLength)+";"+"{0:.2f}".format(pcb_bbx.ZLength)+")")          
    if missingHeight:
        sayerr('MISSING pcb height from stack; forced 1.6mm value')
    if (show_messages==True):
        QtGui.QApplication.restoreOverrideCursor()
        #RotateXYZGuiClass().setGeometry(25, 250, 500, 500)
        reply = QtGui.QMessageBox.information(None,"Info ...",msg)
    if apply_light==True:
        # attach a light to every visible scene graph
        for obj in FreeCAD.ActiveDocument.Objects:
            if obj.ViewObject.Visibility:
                obj.ViewObject.RootNode.insertChild(light1(1,1,-1),2)
                obj.ViewObject.RootNode.insertChild(light2(1,1,1),2)
    if animate_result==True and apply_reflex==True:  #(apply_reflex==True):
        doc=FreeCAD.ActiveDocument
        for obj in doc.Objects:
            if ("Board_Geoms" not in obj.Label) and ("Step_Models" not in obj.Label) and ("Step_Virtual_Models" not in obj.Label)\
              and (obj.TypeId != "App::Line") and (obj.TypeId != "App::Plane") and (obj.TypeId != "App::Origin")\
              and (obj.TypeId != "App::Part") and ("Local_CS" not in obj.Name):
                if show_data:
                    say(obj.Name)
                shape1=obj.Shape
                single_color=FreeCADGui.ActiveDocument.getObject(obj.Name).DiffuseColor
                if(len(single_color)!=len(shape1.Faces)):
                    applyDiffuse=0;
                    if show_data:
                        say(FreeCADGui.ActiveDocument.getObject(obj.Name).ShapeMaterial.DiffuseColor)
                    #copy color to all faces
                #else copy singular colors for faces
                else:
                    applyDiffuse=1;
                    if show_data:
                        say(FreeCADGui.ActiveDocument.getObject(obj.Name).ShapeMaterial.DiffuseColor)
                color_vector=[]
                for color in single_color:
                    color_vector.append((color[0], color[1], color[2]))
                if show_data:
                    sayw(color_vector)
                if show_data:
                    for f in shape1.Faces:
                        sayw('faces')
                    #say(f.ShapeMaterial.DiffuseColor)
                #sayerr (color_list)
                #sayw(color_list_mat)
                idx2=0
                if(applyDiffuse):
                    if (apply_reflex_all==True):
                        shiny=0.6;sun=(201/255, 226/255, 255/255)
                        if show_data:
                            sayw(FreeCADGui.ActiveDocument.getObject(obj.Name).ShapeMaterial.Shininess)
                            sayerr('multiple colors on faces')
                        FreeCADGui.ActiveDocument.getObject(obj.Name).ShapeMaterial.Shininess=shiny
                        if show_data:
                            sayw(FreeCADGui.ActiveDocument.getObject(obj.Name).ShapeMaterial.SpecularColor)
                        FreeCADGui.ActiveDocument.getObject(obj.Name).ShapeMaterial.SpecularColor=sun
                        #for color_v in color_vector:
                        #    color_vector[idx2]=((color_v[0]*shiny,color_v[1]*shiny,color_v[2]*shiny))
                        #    idx2+=1
                        #sayw(color_vector)
                        FreeCADGui.ActiveDocument.getObject(obj.Name).DiffuseColor=color_vector
                else:
                    #say(color_vector)
                    shiny=0.4;bright=1.1
                    if color_vector[0][0]*bright >1:
                        cv0=1
                    elif color_vector[0][0]==0:
                        cv0=0.25
                    else:
                        cv0=color_vector[0][0]*bright
                    if color_vector[0][1]*bright >1:
                        cv1=1
                    elif color_vector[0][1]==0:
                        cv1=0.25
                    else:
                        cv1=color_vector[0][1]*bright
                    if color_vector[0][2]*bright >1:
                        cv2=1
                    elif color_vector[0][2]==0:
                        cv2=0.25
                    else:
                        cv2=color_vector[0][2]*bright
                    #sayerr(str(cv0)+' '+str(cv1)+' '+str(cv2))
                    FreeCADGui.ActiveDocument.getObject(obj.Name).ShapeMaterial.SpecularColor=(cv0,cv1,cv2)
                    FreeCADGui.ActiveDocument.getObject(obj.Name).ShapeMaterial.Shininess=shiny
    if (animate_result==True):
        FreeCADGui.ActiveDocument.ActiveView.startAnimating(0,1,0,0.2)
###
def checkFCbug(fcv):
    """ step hierarchy export bug """     
    if ((fcv[0] == 0) and (fcv[1] == 17) and (fcv[2] >= 13509) and (fcv[2] < 13515))\
       or ((fcv[0] == 0) and (fcv[1] == 18) and (fcv[2] >= 13509) and (fcv[2] < 13548)):
        #if int(fcv[2]) >= 13509 and int(fcv[2]) < 13548: # or fcv[2] == 13516:     
            import Part
            if hasattr(Part, "OCC_VERSION"):
                if (Part.OCC_VERSION=='7.2.0'):
                    return True
    return False
##
def find_skt_in_Doc():
    """ is returning a list of Sketches and relative Group"""
    #print sel_name
    sk_list=[]
    for MObject1 in FreeCAD.ActiveDocument.Objects:
        if MObject1.TypeId=="App::Part":
            #if hasattr(MObject1 ,"Group"):
            if MObject1.Group is not None:
                for MObject2 in MObject1.Group:
                        #print MObject1.Name,MObject2.TypeId
                        if 'Sketch' in MObject2.TypeId:
                            #print MObject2.TypeId
                            if MObject2.Name not in sk_list:
                                sk_list.append([MObject2.Name,MObject1.Name])
                            #return MObject2.Name, MObject1.Name
    #print 'loop closed'
    return sk_list
    
###

def Export2MCAD(blacklisted_model_elements):
    global bbox_all, bbox_list, fusion, show_messages, last_pcb_path
    global height_minimum, volume_minimum, idf_to_origin, ksu_config_fname
    global board_base_point_x, board_base_point_y, real_board_pos_x, real_board_pos_y
    global animate_result, pcb_path, addVirtual, use_AppPart, force_oldGroups, stp_exp_mode, links_imp_mode
    global use_Links, fname_sfx
    say('exporting to MCAD')
    ## exporting
    __objs__=[]
    doc=FreeCAD.ActiveDocument
    for obj in doc.Objects:
        # do what you want to automate
        if ("Board_Geoms" not in obj.Label) and ("Step_Models" not in obj.Label) and ("Step_Virtual_Models" not in obj.Label)\
           and (obj.TypeId != "App::Line") and (obj.TypeId != "App::Plane") and (obj.TypeId != "App::Origin")\
           and (obj.TypeId != "App::Part") and (obj.TypeId != "Sketcher::SketchObject"):
            FreeCADGui.Selection.addSelection(obj)
            __objs__.append(obj)
    filePath=last_pcb_path
    if (bbox_all==1) or (bbox_list==1):
        fpath=filePath+os.sep+doc.Label+"_bbox"+'.step'
    else:
        fpath=filePath+os.sep+doc.Label+'.step'
    # reducing STEP file size
    #NB WriteSurfaceCurveMode parameter get after FC close-reopen
    # paramGet = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/Part/General")
    # paramGet.SetInt("WriteSurfaceCurveMode", 1)
    #paramGet = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/Part/General")
    #paramGet.SetInt("WriteSurfaceCurveMode", 0)
    paramGet = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/Part/STEP")
    old_Auth = paramGet.GetString("Author")
    old_Comp = paramGet.GetString("Company")
    # old_Prod = paramGet.GetString("Product")
    paramGet.SetString("Author", "kicad StepUp")
    paramGet.SetString("Company", "ksu MCAD")
    #sayw("use_AppPart "+str(use_AppPart)+" force_oldGroups "+str(force_oldGroups)+" fusion "+str(fusion))
    #stop
    sayw(stp_exp_mode)
    # stop
    # workaround for OCC7.2 & FC bug
    fcv = getFCversion()
    fcb = checkFCbug(fcv)
    #sayw(fcv)
    #say(fcv[0])
    #stop
    sel = FreeCADGui.Selection.getSelection()
    selN=sel[0].Name
    doc = FreeCAD.ActiveDocument
    paramGet = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/Part/STEP")
    old_Auth = paramGet.GetString("Author")
    old_Comp = paramGet.GetString("Company")
    # old_Prod = paramGet.GetString("Product")
    paramGet.SetString("Author", "kicad StepUp")
    paramGet.SetString("Company", "ksu MCAD")
    
    if use_AppPart and not force_oldGroups: # and not fusion:
        #sayw("exporting STEP with Hierarchy")
        #stop
        __ob__=[]
        skl=[]
        skl=find_skt_in_Doc()
        #print skl
        #print sk_name,';',grp_name
        for sk in skl:
            say('moving sketch from grp')
            #print sk
            FreeCAD.ActiveDocument.getObject(sk[1]).removeObject(FreeCAD.ActiveDocument.getObject(sk[0]))
                #FreeCAD.ActiveDocument.getObject(selN).removeObject(FreeCAD.ActiveDocument.getObject(sk_name))
        
    #sayerr(__ob__[0].Name)
    if (fusion==True):
        ## be careful ... fusion can be heavy or generate FC crash with a lot of objects
        ## please consider to use bbox or blacklist small objs
        # Fuse objects
        doc.addObject("Part::MultiFuse","ksuFusion_")
        doc.ksuFusion_.Shapes = __objs__
    #    doc.ActiveObject.Label=doc.Name+"_union"
        doc.recompute()
        doc.addObject('Part::Feature','ksuFusion').Shape=FreeCAD.ActiveDocument.ksuFusion_.Shape
        if (bbox_all==1) or (bbox_list==1):
            doc.ActiveObject.Label=doc.Name+"_bbox_union"
        else:
            doc.ActiveObject.Label=doc.Name+"_union"
        FreeCADGui.ActiveDocument.ActiveObject.ShapeColor=FreeCADGui.ActiveDocument.ksuFusion_.ShapeColor
        FreeCADGui.ActiveDocument.ActiveObject.LineColor=FreeCADGui.ActiveDocument.ksuFusion_.LineColor
        FreeCADGui.ActiveDocument.ActiveObject.PointColor=FreeCADGui.ActiveDocument.ksuFusion_.PointColor
        FreeCADGui.ActiveDocument.ActiveObject.DiffuseColor=FreeCADGui.ActiveDocument.ksuFusion_.DiffuseColor
        # Remove the fusion object
        doc.removeObject("ksuFusion_")
        doc.recompute()
        fobjs=[]
        fused_obj=doc.ActiveObject
        FreeCAD.Console.PrintMessage(fused_obj)
        fobjs.append(fused_obj)
        if (bbox_all==1) or (bbox_list==1):
            fpath=filePath+os.sep+doc.Label+"_bbox_union"+'.step'
        else:
            fpath=filePath+os.sep+doc.Label+"_union"+'.step'
        FreeCAD.Console.PrintMessage(fpath+" fusion path")
        FreeCAD.Console.PrintMessage(fobjs)
        #Export fused object
        # reducing STEP file size
        #NB WriteSurfaceCurveMode parameter get after FC close-reopen
        # paramGet = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/Part/General")
        # paramGet.SetInt("WriteSurfaceCurveMode", 1)
        #paramGet = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/Part/General")
        #paramGet.SetInt("WriteSurfaceCurveMode", 0)
        #paramGet = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/Part/STEP")
        #old_Auth = paramGet.GetString("Author")
        #old_Comp = paramGet.GetString("Company")
        # old_Prod = paramGet.GetString("Product")
        #paramGet.SetString("Author", "kicad StepUp")
        #paramGet.SetString("Company", "ksu MCAD")
        ##  not to be used paramGet.SetString("Product", "Open CASCADE STEP processor 7.0")
        ImportGui.export(fobjs,fpath)
        #restoring old Author
        #paramGet = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/Part/STEP")
        # paramGet.SetString("Author", old_Auth)
        # paramGet.SetString("Company", old_Comp)
        # paramGet.SetString("Product", old_Prod)
        #say(old_Auth)
        #say(old_Comp)
        FreeCAD.activeDocument().recompute()
        del fobjs
        #ImportGui.export(doc.ActiveObject,filePath+os.sep+doc.Label+'.step')
    elif (fcv[0]==0 and fcv[1]<=16):  # FC < 0.17
        sayw('exporting flat FC 0.16')
        ImportGui.export(__objs__,fpath)
    elif (stp_exp_mode == 'hierarchy' and not fcb):  # FC not bugged or < 0.17
        sayw('exporting hierarchy')
        __obtoexp__=[]
        # FreeCADGui.Selection.removeSelection(obj)
        # FreeCADGui.Selection.addSelection(doc.getObject("Board"))
        __obtoexp__.append(doc.getObject("Board"+fname_sfx))
        ImportGui.export(__obtoexp__,fpath)
        del __obtoexp__
    elif (stp_exp_mode == 'onelevel') or (stp_exp_mode == 'hierarchy' and fcb):
        sayw('exporting ONE level hierarchy')
        FreeCADGui.Selection.removeSelection(obj)
        FreeCADGui.Selection.addSelection(doc.getObject("Board"+ fname_sfx))
        try:
            import kicadStepUpCMD
        except:
            sayerr('to export STEP it is necessary to use StepUp Workbench<br>instead of the single Macro<br>(because of '+str(fcv)+' FC bug)')
            msg="""<font color='red'><b>to export STEP it is necessary to use StepUp Workbench<br>instead of the single Macro<br>(because of """+str(fcv)+""" FC bug</b></font>"""
            say_warning(msg)
            for sk in skl:
                say('including sketch in grp')
                FreeCAD.ActiveDocument.getObject(sk[1]).addObject(FreeCAD.ActiveDocument.getObject(sk[0]))
            stop
        if fcb:
            cpmode='compound'
        else:
            cpmode='part'
        suffix='_'
        to_export_name=kicadStepUpCMD.deep_copy(doc,cpmode,suffix)
        # to_export_name=FreeCAD.ActiveDocument.ActiveObject.Name
        #sayw(FreeCAD.ActiveDocument.getObject(to_export_name).Label)
        #say(sel[0])
        __objs__=[]
        __objs__.append(FreeCAD.ActiveDocument.getObject(to_export_name))
        #import ImportGui
        ImportGui.export(__objs__,fpath)
        #FreeCAD.ActiveDocument.removeObject(to_export_nam)
        removesubtree(__objs__)
        #del __objs__
        if fcb: # bugged FC version
            sayerr('exported a simplified STEP hierarchy because of '+str(fcv)+' FC bug')
            msg="""<font color='red'><b>exported a simplified STEP hierarchy<br>because of """+str(fcv)+""" FC bug</b></font>"""
            say_warning(msg)
                            
            for sk in skl:
                say('including sketch in grp')
                FreeCAD.ActiveDocument.getObject(sk[1]).addObject(FreeCAD.ActiveDocument.getObject(sk[0]))
            #stop
    elif stp_exp_mode == 'flat':  # FC >=0.17
        # need to deselect all 'Part' containers and select all simple objs
        #say('flat')
        if len(sel)==1 and 'App::Part' in sel[0].TypeId: ## flattening a Part hierarchy container
            sayw('flattening Part container')
            # FreeCADGui.Selection.removeSelection(sel[0])
            __objs__=[]
            for o in FreeCAD.ActiveDocument.getObject(selN).OutListRecursive:
                #print o.TypeId
                # if 'Part::Feature' in o.TypeId:
                if hasattr(o, 'Shape'):
                    # print o.Label
                    # say ('adding ') 
                    # FreeCADGui.Selection.addSelection(o)
                    __objs__.append(o)
            ImportGui.export(__objs__,fpath)
            #del __objs__
        else:
            sayw('exporting selection')
            ImportGui.export(sel,fpath)

    if use_AppPart and not force_oldGroups: # and not fusion:
        for sk in skl:
            say('including sketch in grp')
            FreeCAD.ActiveDocument.getObject(sk[1]).addObject(FreeCAD.ActiveDocument.getObject(sk[0]))

    #paramGet = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/Part/STEP")
    ## restoring old Author
    paramGet.SetString("Author", old_Auth)
    paramGet.SetString("Company", old_Comp)
    # paramGet.SetString("Product", old_Prod)
    #say(old_Auth)
    #say(old_Comp)
    #fusion=False
    mcompound=False #True #to create a Compound instead of a fusion ... to evaluate after Export STEP has improved vejmarie
    ##mcompound=True
    ##fusion=True
    if (mcompound==True):
        doc.addObject("Part::Compound","ksuCompound_")
        #say(cObjs)
        doc.ksuCompound_.Links = __objs__ #cObjs
        doc.recompute()
        doc.addObject('Part::Feature','ksuCompound').Shape=FreeCAD.ActiveDocument.ksuCompound_.Shape
        FreeCADGui.ActiveDocument.ActiveObject.ShapeColor=FreeCADGui.ActiveDocument.ksuCompound_.ShapeColor
        FreeCADGui.ActiveDocument.ActiveObject.LineColor=FreeCADGui.ActiveDocument.ksuCompound_.LineColor
        FreeCADGui.ActiveDocument.ActiveObject.PointColor=FreeCADGui.ActiveDocument.ksuCompound_.PointColor
        FreeCADGui.ActiveDocument.ActiveObject.DiffuseColor=FreeCADGui.ActiveDocument.ksuCompound_.DiffuseColor
        # Remove the fusion object
        doc.removeObject("ksuCompound_")
        doc.recompute()
        
        stop
    for obj in doc.Objects:
        # do what you want to automate
        FreeCADGui.Selection.removeSelection(obj)
    if blacklisted_model_elements != '':
        sayw("black-listed module \n"+ ''.join(map(str, blacklisted_models)))
        if (show_messages==True):
            QtGui.QApplication.restoreOverrideCursor()
            reply = QtGui.QMessageBox.information(None,"Info ...","... black-listed module(s)\r\n"+ ''.join(map(str, blacklisted_models)).replace(',','\n'))
        #FreeCAD.Console.PrintMessage("black-listed module "+ '\r\n'.join(map(str, blacklisted_models)))    
    del __objs__
    ## Save to disk in native format
    FreeCAD.ActiveDocument=None
    FreeCADGui.ActiveDocument=None
    FreeCAD.setActiveDocument(doc.Name)
    FreeCAD.ActiveDocument=FreeCAD.getDocument(doc.Name)
    FreeCADGui.ActiveDocument=FreeCADGui.getDocument(doc.Name)
    if (bbox_all==1) or (bbox_list==1):
        fpath=filePath+os.sep+doc.Name+"_bbox"
    else:
        fpath=filePath+os.sep+doc.Name
    if (fusion==True):
        fpath=fpath+"_union"
    say(fpath+".FCStd")
    #fpath = re.sub("\\\\", "/", fpath)
    #fpath= make_unicode(fpath)
    #freeCADFileName = pcb_path + "/" + doc.Name + ".FCStd" #utf-8 test
    #sayw (pcb_path); sayw(freeCADFileName)
    #fcfilenametest=(freeCADFileName.encode('utf-8'))
    #sayw(fcfilenametest)
    #FreeCAD.getDocument(doc.Name).saveAs(fcfilenametest) #utf-8 test
    #FreeCAD.getDocument(doc.Name).saveAs(freeCADFileName) #utf-8 test
    #stop
    
    try:
        FreeCAD.getDocument(doc.Name).saveAs((fpath+".FCStd").encode('utf-8'))  #bug in FC need to encode utf-8
        FreeCAD.ActiveDocument.recompute()
    except:
        say_warning("error writing FreeCAD file. You do not have write permissions to save file!")
    #FreeCAD.getDocument(doc.Name).Label = doc.Name
    #FreeCADGui.SendMsgToActiveView("Save")
    #FreeCAD.getDocument(doc.Name).save()
    msgpath=filePath+os.sep+doc.Name
    if (bbox_all==1) or (bbox_list==1):
        msgpath=msgpath+"_bbox"
    msg="""<b>kicad StepUp</b> ver. """
    msg+=___ver___
    msg+="<br>file exported<br><b>"+msgpath+'.step</b>'
    #if len(msgpath)>15:
    #    insert_return(msgpath, 15)
    if (fusion==True):
        msgpath=msgpath+"_union"
        msg+="<br>fused file exported<br><b>"+msgpath+'.step</b>'    
    if (idf_to_origin==True):
        new_pos_x=board_base_point_x+real_board_pos_x
        new_pos_y=board_base_point_y+real_board_pos_y
    else:
        new_pos_x=board_base_point_x
        new_pos_y=board_base_point_y
    if (grid_orig==1):
        msg+="<br>Board Placed @ "+"{0:.2f}".format(board_base_point_x)+";"+"{0:.2f}".format(board_base_point_y)+";0.0"
    else:
        msg+="<br>Board Placed @ "+"{0:.2f}".format(new_pos_x)+";"+"{0:.2f}".format(new_pos_y)+";0.0"
    msg+="<br>kicad pcb pos: ("+"{0:.2f}".format(real_board_pos_x)+";"+"{0:.2f}".format(real_board_pos_y)+";"+"{0:.2f}".format(0)+")"
    if (bbox_all==1) or (bbox_list==1):
        msg+="<br>bounding box modules applied"
    if (volume_minimum!=0):
        msg+="<br><b><font color=blue>modules with volume less than "+str(volume_minimum)+"mm^3 not included</font></b>"
    if (height_minimum!=0):
        msg+="<br><b><font color=blue>modules with height less than "+str(height_minimum)+"mm not included</font></b>"    
    if (min_drill_size!=0):
        msg+="<br><b><font color=blue>drills with size less than "+str(min_drill_size)+"mm not included</font></b>"
    if (compound_found):
        msg+="<br>found  <b><font color=red>multi-part</font></b></b> object(s)"
    if addVirtual==0:
        msg+="<br><b>Virtual models skipped</b>"
    #msg+="<br>kicad StepUp config file in:<br><b>"+ksu_config_fname+"</b><br>location."
    msg+="<br>StepUp configuration options are located in the preferences system of FreeCAD."
    if (grid_orig==1):
        say("Board Placed @ "+"{0:.2f}".format(board_base_point_x)+";"+"{0:.2f}".format(board_base_point_y)+";0.0")
    else:
        say("Board Placed @ "+"{0:.2f}".format(new_pos_x)+";"+"{0:.2f}".format(new_pos_y)+";0.0")
    say("kicad pcb pos: ("+"{0:.2f}".format(real_board_pos_x)+";"+"{0:.2f}".format(real_board_pos_y)+";"+"{0:.2f}".format(0)+")")    
    say_time()
    if (show_messages==True):
        QtGui.QApplication.restoreOverrideCursor()
        #RotateXYZGuiClass().setGeometry(25, 250, 500, 500)
        reply = QtGui.QMessageBox.information(None,"Info ...",msg)
    if (animate_result==True):
        FreeCADGui.ActiveDocument.ActiveView.startAnimating(0,1,0,0.2)
###
def removesubtree(objs):
    def addsubobjs(obj,toremoveset):
        if isinstance(obj, list):
            for o in obj:
                toremove.add(o)
                for subobj in o.OutList:
                    addsubobjs(subobj,toremoveset)
        else:
            toremove.add(obj)
            for subobj in obj.OutList:
                addsubobjs(subobj,toremoveset)

    import FreeCAD
    toremove=set()
    for obj in objs:
        addsubobjs(obj,toremove)
    checkinlistcomplete =False
    while not checkinlistcomplete:
        for obj in toremove:
            if (obj not in objs) and (frozenset(obj.InList) - toremove):
                try:
                    toremove.remove(obj)
                except:
                    print('exception')
                    pass
                break
        else:
            checkinlistcomplete = True
    for obj in toremove:
        try:
            obj.Document.removeObject(obj.Name)
        except:
            print('exception')
            pass

###
def create_compound(count,modelnm):  #create compound function when a multipart is loaded
    
    global allow_compound, compound_found, use_Links, use_LinkGroups
    
    counter=0
    for ObJ in FreeCAD.activeDocument().Objects:
        counter+=1
        #sayw(str(counter)+" ");say(str(count))
    if count+1 != counter:
        sayerr('multipart found! ...')
        compound_found=True
        counter=0
        objs_to_remove = []
        for ObJ in FreeCAD.activeDocument().Objects:
            counter+=1
            if counter > count:
                ##sayw(ObJ.TypeId)
                if 'App::Plane' not in ObJ.TypeId and 'App::Origin' not in ObJ.TypeId and 'App::Line' not in ObJ.TypeId:
                    #FreeCADGui.Selection.addSelection(ObJ)
                    objs_to_remove.append(ObJ)
        #sel = FreeCADGui.Selection.getSelection()
        #lsel = len (sel)
        lotr = len (objs_to_remove)
        #print (lsel)
        #print (sel[lsel-1].Label)
        #for s in sel:
        #    print(s.Label)
        #tobeimproved for App:Links
        # sayw(str(objs_to_remove))
        #stop
        #mycompound_new=FreeCAD.activeDocument().ActiveObject
        #sayw (sel.Type)
        #sayw (sel[0].TypeId)
        #stop
        nbr_cmpd=0
        if 'App::LinkGroup' in objs_to_remove[0].TypeId:
            simple_copy_link(objs_to_remove[0])
            mycompound=FreeCAD.activeDocument().ActiveObject
            FreeCAD.ActiveDocument.recompute()
            removesubtree([objs_to_remove[0]])
        elif 'LinkView' in dir(FreeCADGui):
            if 'App::Part' in objs_to_remove[lotr-1].TypeId:  #from FC 0.17-12090 multipart STEPs are loded as App::Part and have a list inverted
                simple_copy_link(objs_to_remove[lotr-1])
                mycompound=FreeCAD.activeDocument().ActiveObject
                FreeCAD.ActiveDocument.recompute()
                removesubtree([objs_to_remove[lotr-1]])
        elif 'App::Part' in objs_to_remove[0].TypeId:  #from FC 0.17-10647 multipart STEPs are loded as App::Part
            sc_list=[]
            recurse_node(objs_to_remove[0],objs_to_remove[0].Placement, sc_list)
        #else:  #from FC 0.17-10647 multipart STEPs are loded as App::Part
            sc_list_compound=[]
            for o in sc_list:
                if 'Part' in o.TypeId and 'App::Part' not in o.TypeId:
                    sc_list_compound.append(o)
            FreeCAD.ActiveDocument.recompute()
            #sayw(sc_list_compound)
            #stop
            FreeCAD.activeDocument().addObject("Part::Compound",objs_to_remove[0].Label+"_mp")
            FreeCAD.activeDocument().ActiveObject.Links = sc_list_compound #[FreeCAD.activeDocument().Part__Feature,FreeCAD.activeDocument().Shape,]
            mycompound=FreeCAD.activeDocument().ActiveObject
            if 1:
                #FreeCAD.ActiveDocument.getObject(objs_to_remove[0].Name).removeObjectsFromDocument()
                FreeCAD.ActiveDocument.removeObject(objs_to_remove[0].Name)
            else:
                FreeCADGui.Selection.removeSelection(FreeCADGui.Selection.getSelection()[0])
            #FreeCADGui.Selection.addSelection(FreeCAD.activeDocument().ActiveObject)
            FreeCAD.ActiveDocument.recompute()
            #simple_copy(FreeCAD.activeDocument().ActiveObject)
        elif 'App::Part' in objs_to_remove[lotr-1].TypeId:  #from FC 0.17-12090 multipart STEPs are loded as App::Part and have a list inverted
            sc_list=[]
            recurse_node(objs_to_remove[lotr-1],objs_to_remove[lotr-1].Placement, sc_list)
        #else:  #from FC 0.17-10647 multipart STEPs are loded as App::Part
            sc_list_compound=[]
            for o in sc_list:
                if 'Part' in o.TypeId and 'App::Part' not in o.TypeId and 'Compound' not in o.TypeId:
                    sc_list_compound.append(o)
            FreeCAD.ActiveDocument.recompute()
            #sayw(sc_list_compound)
            #say('Part container found')
            #stop
            FreeCAD.activeDocument().addObject("Part::Compound",objs_to_remove[lotr-1].Label+"_mp")
            FreeCAD.activeDocument().ActiveObject.Links = sc_list_compound #[FreeCAD.activeDocument().Part__Feature,FreeCAD.activeDocument().Shape,]
            mycompound=FreeCAD.activeDocument().ActiveObject
            if 1:
                #for ob in objs_to_remove:
                #    FreeCAD.ActiveDocument.removeObject(ob.Name)
                FreeCAD.ActiveDocument.removeObject(objs_to_remove[lotr-1].Name)
                FreeCAD.ActiveDocument.removeObject(objs_to_remove[0].Name)
            else:
                FreeCADGui.Selection.removeSelection(FreeCADGui.Selection.getSelection()[0])
            #FreeCADGui.Selection.addSelection(FreeCAD.activeDocument().ActiveObject)
            FreeCAD.ActiveDocument.recompute()
            #simple_copy(FreeCAD.activeDocument().ActiveObject)
        elif 'Compound' in objs_to_remove[0].TypeId: #new release will load already a compound
            for Obj in objs_to_remove:
                if 'Compound' in Obj.TypeId:
                    nbr_cmpd+=1
            if nbr_cmpd == 1:
                mycompound=FreeCAD.activeDocument().getObject(objs_to_remove[0].Name)
                #FreeCADGui.Selection.addSelection(mycompound)
                sayw('single Compound part')
        #print sel[0].TypeId
        #stop
        else:    
        #if nbr_cmpd > 1 or nbr_cmpd == 0:
        #if 'App::Part' not in sel[0].TypeId:
        #if nbr_cmpd > 1 or nbr_cmpd == 0: #new release will load already a compound
            if nbr_cmpd>=1:
                sayw('multi Compound part ...')
            sayw('... doing compound')    
            sc_list_compound=[]
            for o in objs_to_remove:
                if 'Compound2' in o.TypeId or 'App::LinkGroup' in o.TypeId:
                    sc_list_compound.append(o)
            if len(sc_list_compound) == 0:
                for o in objs_to_remove:
                    if 'Part' in o.TypeId and 'App::Part' not in o.TypeId:
                        sc_list_compound.append(o)
            #print (sc_list_compound)
            FreeCAD.ActiveDocument.addObject("Part::Compound",'MultiPart')
            FreeCAD.ActiveDocument.ActiveObject.Links = sc_list_compound #[FreeCAD.activeDocument().Part__Feature,FreeCAD.activeDocument().Shape,]
            FreeCADGui.Selection.clearSelection()
            mycompound=FreeCAD.ActiveDocument.ActiveObject
            #FreeCADGui.Selection.addSelection(FreeCAD.ActiveDocument.ActiveObject)
            FreeCAD.ActiveDocument.recompute()
        #stop
        modelnm_norm=make_string(modelnm) #to manage utf-8
        FreeCAD.ActiveDocument.addObject('Part::Feature',modelnm_norm).Shape=FreeCAD.ActiveDocument.getObject(mycompound.Name).Shape
        mynewObj = FreeCAD.ActiveDocument.ActiveObject
        FreeCADGui.ActiveDocument.ActiveObject.ShapeColor=FreeCADGui.ActiveDocument.getObject(mycompound.Name).ShapeColor
        FreeCADGui.ActiveDocument.ActiveObject.LineColor=FreeCADGui.ActiveDocument.getObject(mycompound.Name).LineColor
        FreeCADGui.ActiveDocument.ActiveObject.PointColor=FreeCADGui.ActiveDocument.getObject(mycompound.Name).PointColor
        FreeCADGui.ActiveDocument.ActiveObject.DiffuseColor=FreeCADGui.ActiveDocument.getObject(mycompound.Name).DiffuseColor
        ## if use_Links: # compound2 colors to be fixed
        ##     FreeCADGui.ActiveDocument.ActiveObject.mapShapeColors(FreeCAD.ActiveDocument)
        #FreeCAD.ActiveDocument.removeObject(mycompound.Name)
        #FreeCAD.ActiveDocument.recompute()
        #stop
        #for ob in objs_to_remove:
        #   FreeCAD.ActiveDocument.removeObject(ob.Name)
        #removesubtree(FreeCADGui.Selection.getSelection())
        removesubtree([mycompound])
        ## reference mode for labels
        mynewObj.Label=modelnm_norm
        #sayerr('HERE')
        #workaround to remove all extra objects instead of searching for top level container
        for o in objs_to_remove:
            try:
                FreeCAD.ActiveDocument.removeObject(o.Name)
            except:
                pass
        #App.ActiveDocument.getObject(FreeCADGui.Selection.getSelection()[0].Name).removeObjectsFromDocument()
        #App.ActiveDocument.removeObject(FreeCADGui.Selection.getSelection()[0].Name)
        #removesubtree(mycompound.Name)
        FreeCAD.ActiveDocument.recompute()
        #stop
        FreeCADGui.Selection.clearSelection()
###

def find_top_container(objs_list):
    '''searching for top level Part container'''
    ap_list = []
    cp_list = []
    ag_list = []
    for o in objs_list:
        #say(o.Label)
        if o.TypeId == 'App::Part':
            ap_list.append(o)
        elif o.TypeId == 'Part::Compound2':
            cp_list.append(o)
        elif o.TypeId == 'App::LinkGroup':
            ag_list.append(o)
    top_ap=None
    top_cp=None
    for ap in ap_list:
        if len(ap.InListRecursive) == 0:
            top_ap = ap
            break
    #say(str(ap_list));stop
    if top_ap is not None:
        say(top_ap.Label)
        sayw('multi Part found! ...')
        return top_ap
    else:
        for cp in cp_list:
            if len(cp.InListRecursive) == 0:
                top_cp = cp
                say(top_cp.Label)
                sayw('multi Compound found! ...')
                break
    if top_cp is not None:
        return top_cp
    else:
        top_ag = None
        for ag in ag_list:
            if len(ag.InListRecursive) == 0:
                top_ag = ag
                say(top_ag.Label)
                sayw('multi LinkGroup found! ...')
                break
        return top_ag
##

def check_wrl_transparency(step_module):
    prefs = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/kicadStepUpGui")
    step_transparency = 0
    Led_enabled = prefs.GetBool('transparency_material_led_enabled')
    Glass_enabled = prefs.GetBool('transparency_material_glass_enabled')
    if Led_enabled or Glass_enabled:
        #sayw('force transparency for glass or led materials'
        if step_module.lower().endswith('wrl'):
            if os.path.exists(step_module):  # a wrl model could be missing
                read_mode = 'r'
                if (sys.version_info > (3, 0)):  #py3
                    read_mode = 'rb'
                    LedM=b'material USE LED'
                    GlassM=b'material USE GLASS'
                else:
                    read_mode = 'r'
                    LedM='material USE LED'
                    GlassM='material USE GLASS'
                with builtin.open(step_module, read_mode) as f:
                    #FreeCAD.Console.PrintError(step_module)
                    #FreeCAD.Console.PrintError(' WRL MATERIALS\n')
                    model_content = f.read()
                    if Led_enabled and LedM in model_content:
                        sayw('force transparency for led materials')
                        step_transparency = 30
                    if Glass_enabled and GlassM in model_content:
                        sayw('force transparency for glass materials')
                        step_transparency = 70
        elif step_module.lower().endswith('wrz'):
            read_mode = 'r'
            if (sys.version_info > (3, 0)):  #py3
                read_mode = 'rb'
                LedM=b'material USE LED'
                GlassM=b'material USE GLASS'
            else:
                read_mode = 'r'
                LedM='material USE LED'
                GlassM='material USE GLASS'
            try:
                with gz.open(step_module, read_mode) as f:
                    model_content = f.read()
                    #FreeCAD.Console.PrintError(model_content)
                    if Led_enabled and LedM in model_content:
                        sayw('force transparency for led materials')
                        step_transparency = 30
                    if Glass_enabled and GlassM in model_content:
                        sayw('force transparency for glass materials')
                        step_transparency = 70
            except:
                step_transparency = 0
                sayerr('wrz transparency NOT supported')
    return step_transparency
##
def findModelPath(model_type, path_list):
    """ Find module in all paths and types specified """
    global models3D_prefix, models3D_prefix2, models3D_prefix3, models3D_prefix4

    module_path='not-found'
    # model_type = [step_module,step_module_lw,step_module_up,step_module2,step_module2_up,step_module3,step_module3_up,step_module4,step_module4_up,step_module5,step_module5_up]
    # path_list  = [models3D_prefix,models3D_prefix2,models3D_prefix3,models3D_prefix4]
    path_list = list(filter(None, path_list)) #removing empty paths
    # sayw('searching models:'+str(model_type))
    # sayw('on '+str(len(path_list))+' paths: '+str(path_list))
    for model in model_type:
        if (module_path=='not-found'):
            # sayerr('trying '+model)
            if os.path.exists(model): # absolute path
                module_path=model
                break
        for mpath in path_list:
            if (module_path=='not-found'):
                model=model.replace(u'"', u'')  # strip out '"'
                mpath_U = re.sub("\\\\", "/", mpath)
                # mpath_U = mpath_U.replace("\\", "/")
                utf_path=os.path.join(make_unicode(mpath_U),make_unicode(model))
                # sayerr('trying '+utf_path)
                if os.path.exists(utf_path):
                    module_path=utf_path
                    # say('model found! on path: '+re.sub("\\\\", "/", module_path))
                    break

    return module_path
##
def Load_models(pcbThickness,modules):
    global off_x, off_y, volume_minimum, height_minimum, bbox_all, bbox_list
    global whitelisted_model_elements
    global models3D_prefix, models3D_prefix2, models3D_prefix3, models3D_prefix4
    global last_pcb_path, full_placement
    global allow_compound, compound_found, bklist, force_transparency, warning_nbr, use_AppPart
    global conv_offs, use_Links, links_imp_mode, use_pypro, use_LinkGroups, fname_sfx
    
    #say (modules)
    missing_models = ''
    compound_found=False
    loaded_models = []
    loaded_model_objs = []
    loaded_models_skipped = []
    createScaledObjs=False #box and cyl from wrl scale params
    virtual_nbr=0
    virtualTop_nbr=0
    virtualBot_nbr=0
    modelTop_nbr=0
    modelBot_nbr=0
    mod_cnt=0
    top_name='Top'+fname_sfx
    bot_name='Bot'+fname_sfx
    topV_name='TopV'+fname_sfx
    botV_name='BotV'+fname_sfx
    stepM_name='Step_Models'+fname_sfx
    stepV_name='Step_Virtual_Models'+fname_sfx
    
    my_hide_list=""

    for i in range(len(modules)):
        step_module=modules[i][0]
        module_container = step_module
        #print(type(step_module))  #maui test py3
        #sayw('added '+str(i)+' model(s)')
        #say(modules[i]);
        #FreeCAD.Console.PrintMessage('step-module '+step_module)
        encoded=0
        sayw(step_module) # utf-8 test
        if (step_module.startswith(':')) or (step_module.startswith('":')):  #alias 3D path
            step_module_t=step_module.split(':', 1)[-1]
            step_module=step_module_t.split(':', 1)[-1]
            #step_module=step_module.decode("utf-8").replace(u'"', u'')  # name with spaces
            step_module=step_module.replace(u'"', u'')  # name with spaces
            if (step_module.startswith('/')) or  (step_module.startswith('\\')):
                step_module=step_module[1:]
            encoded=1
            #say(step_module)
            #step_module=step_module_t[1]
            #say(step_module.split(':')[1:])
            say('adjusting Alias Path')
            say('step-module-replaced '+step_module)
        elif (step_module.find('${HOME}')!=-1):  #local 3D path
            #step_module=step_module.replace('${KIPRJMOD}', '.')
            home = expanduser("~")
            #step_module=step_module.decode("utf-8").replace(u'${HOME}', home.decode("utf-8"))
            step_module=step_module.replace(u'${HOME}', home)
            step_module=step_module.replace(u'"', u'')  # name with spaces
            encoded=1
            say('adjusting Local Path')
            say('step-module-replaced '+step_module)
        elif (step_module.find('${KIPRJMOD}')!=-1):  #local 3D path
            step_module = re.sub("\\\\", "/", step_module)
            #if isinstance(step_module, str):
            #    step_module = step_module.decode('unicode_escape')
            last_pcb_path = re.sub("\\\\", "/", last_pcb_path)
            #if isinstance(last_pcb_path, str):
            #    last_pcb_path = last_pcb_path.decode('unicode_escape')
            step_module=step_module.replace(u'${KIPRJMOD}', last_pcb_path)
            #sm=step_module
            #step_module=re.sub(r"^\$\{KIPRJMOD\}.*$",last_pcb_path, sm)
            #step_module=re.sub('\${.KIPRJMOD}/', '', step_module)
            step_module=step_module.replace(u'"', u'')  # name with spaces
            encoded=1
            say('adjusting Relative Path')
            say('step-module-replaced '+step_module)
        elif (step_module.startswith('.')) or (step_module.startswith('".')):  #relative path
            #step_module=last_pcb_path+"/"+step_module
            step_module=last_pcb_path+os.sep+step_module
            step_module=step_module.replace(u'"', u'')  # name with spaces
            #step_module=last_pcb_path+step_module[14:]
            encoded=1
            sayw('adjusting Relative Path')
            say('step-module-replaced '+step_module)
            #stop
        elif (step_module.find('${KISYS3DMOD}/')!=-1):  #local ${KISYS3DMOD} 3D path
            #step_module=step_module.replace('${KIPRJMOD}', '.')
            #step_module=step_module.decode("utf-8").replace(u'${KISYS3DMOD}/', u'')
            step_module=step_module.replace(u'${KISYS3DMOD}/', u'')
            step_module=step_module.replace(u'"', u'')  # name with spaces
            #step_module=last_pcb_path+step_module[14:]
            encoded=1
            say('adjusting Local Path')
            say('step-module-replaced '+step_module)
        elif (step_module.find('${')!=-1) and encoded==0:  #extra local ${ENV} 3D path
            step_module= re.sub('\${.*?}/', '', step_module)
            #step_module=step_module.decode("utf-8").replace(u'${}/', u'')
            step_module=step_module.replace(u'${}/', u'')
            step_module=step_module.replace(u'"', u'')  # name with spaces
            encoded=1
            say('adjusting 2nd Local Path')
            say('step-module-replaced '+step_module)      
        elif (step_module.find('$(')!=-1) and encoded==0:  #extra local $(ENV) 3D path
            step_module= re.sub('\$(.*?)/', '', step_module)
            #step_module=step_module.decode("utf-8").replace(u'${}/', u'')
            step_module=step_module.replace(u'$()/', u'')
            step_module=step_module.replace(u'"', u'')  # name with spaces
            encoded=1
            say('adjusting 2nd Local Path')
            say('step-module-replaced '+step_module)      
        if (encoded == 0):  #test local 3D path without the use of KIPRJMOD or ENV
            step_module_local = re.sub("\\\\", "/", step_module)     #subst '\\' with '/'
            # step_module_local = step_module_local.replace("\\", "/") #subst '\'  with '/'
            last_pcb_path_local = re.sub("\\\\", "/", last_pcb_path)
            # print(step_module)
            # print(step_module_local)
            step_module_local=step_module_local.replace(u'"', u'')  # name with spaces
            #print(step_module_local)
            utf_path_local=os.path.join(make_unicode(last_pcb_path_local),make_unicode(step_module_local))
            #print(utf_path_local)
            pos=utf_path_local.rfind('.')
            #sayw(pos)
            rel_pos=len(utf_path_local)-pos
            local_path=utf_path_local[:-rel_pos+1]
            #print(local_path)
            #stop
            if os.path.exists(local_path+u'stpZ'):
                step_module = local_path+u'stpZ'
                encoded=1
                say('adjusting Relative Path to pcb file')
                say('step-module-replaced '+step_module)
            elif os.path.exists(local_path+u'stpz'):
                step_module = local_path+u'stpz'
                encoded=1
                say('adjusting Relative Path to pcb file')
                say('step-module-replaced '+step_module)
            elif os.path.exists(local_path+u'STPZ'):
                step_module = local_path+u'STPZ'
                encoded=1
                say('adjusting Relative Path to pcb file')
                say('step-module-replaced '+step_module)
            elif os.path.exists(local_path+u'step'):
                step_module = local_path+u'step'
                encoded=1
                say('adjusting Relative Path to pcb file')
                say('step-module-replaced '+step_module)
            elif os.path.exists(local_path+u'STEP'):
                step_module = local_path+u'STEP'
                encoded=1
                say('adjusting Relative Path to pcb file')
                say('step-module-replaced '+step_module)
            elif os.path.exists(local_path+u'stp'):
                step_module = local_path+u'stp'
                encoded=1
                say('adjusting Relative Path to pcb file')
                say('step-module-replaced '+step_module)
            elif os.path.exists(local_path+u'STP'):
                step_module = local_path+u'STP'
                encoded=1
                say('adjusting Relative Path to pcb file')
                say('step-module-replaced '+step_module)
            
            elif os.path.exists(local_path+u'iges'):
                step_module = local_path+u'iges'
                encoded=1
                say('adjusting Relative Path to pcb file')
                say('step-module-replaced '+step_module)
            elif os.path.exists(local_path+u'IGES'):
                step_module = local_path+u'IGES'
                encoded=1
                say('adjusting Relative Path to pcb file')
                say('step-module-replaced '+step_module)
            elif os.path.exists(local_path+u'igs'):
                step_module = local_path+u'igs'
                encoded=1
                say('adjusting Relative Path to pcb file')
                say('step-module-replaced '+step_module)
            elif os.path.exists(local_path+u'IGS'):
                step_module = local_path+u'IGS'
                encoded=1
                say('adjusting Relative Path to pcb file')
                say('step-module-replaced '+step_module)
        if step_module != 'no3Dmodel':
            #model_type = step_module.split('.')[1]
            #if encoded!=1:
            step_module = re.sub("\\\\", "/", step_module)      #subst '\\' with '/'
            # step_module =  step_module.replace("\\", "/") #subst '\'  with '/'
            
            wrl_model = ''
            if step_module.lower().endswith('wrl') or step_module.lower().endswith('wrz'):
                wrl_model = step_module
            #step_transparency = check_wrl_transparency
            step_module=step_module.replace(u'"', u'')  # name with spaces
            pos=step_module.rfind('.')
            #sayw(pos)
            rel_pos=len(step_module)-pos
            #sayw(rel_pos)
            #stop
            step_module=step_module[:-rel_pos+1]+u'stpZ'
            step_module_lw=step_module[:-4]+u'stpz'
            step_module_up=step_module[:-4]+u'STPZ'
            #step_module=step_module[:-3]+'step'
            step_module2=step_module[:-4]+u'step'
            step_module2_up=step_module[:-4]+u'STEP'
            step_module3=step_module[:-4]+u'stp'
            step_module3_up=step_module[:-4]+u'stp'
            step_module4=step_module[:-4]+u'iges'
            step_module4_up=step_module[:-4]+u'IGES'
            step_module5=step_module[:-4]+u'igs'
            step_module5_up=step_module[:-4]+u'IGS'
            # step_module=step_module[:-rel_pos+1]+u'step'
            # #step_module=step_module[:-3]+'step'
            # step_module2=step_module[:-4]+u'stp'
            # step_module3=step_module[:-4]+u'iges'
            # step_module4=step_module[:-4]+u'igs'
            # step_module5=step_module[:-4]+u'stpz'
            #if encoded!=1:
            #    #step_module=step_module.decode("utf-8").replace(u'"', u'')  # name with spaces
            #    step_module=step_module.replace(u'"', u'')  # name with spaces
            model_name=step_module[:-5]
            last_slash_pos1=model_name.rfind('/')
            last_slash_pos2=model_name.rfind('\\')
            last_slash_pos=max(last_slash_pos1,last_slash_pos2)
            model_name=model_name[last_slash_pos+1:]
            #say('model name '+model_name+'.'+model_type)
            say('model name '+model_name)
        else:
            model_name='no3Dmodel'
        blacklisted=0
        if blacklisted_model_elements != '':
            if blacklisted_model_elements.find(model_name) != -1:
                blacklisted=1
        ###

        if (blacklisted==0):
            if step_module != 'no3Dmodel':
                createScaledObjs=False
                if model_name=="box_mcad" or model_name=="cylV_mcad" or model_name=="cylH_mcad":
                    createScaledObjs=True
                if not createScaledObjs:
                    path_list = [models3D_prefix,models3D_prefix2,models3D_prefix3,models3D_prefix4]
                    model_type = [step_module,step_module_lw,step_module_up,step_module2,step_module2_up,step_module3,step_module3_up,step_module4,step_module4_up,step_module5,step_module5_up]
                    module_path = findModelPath(model_type, path_list)     # Find module in all paths and types specified
                else:
                    scale_vrml=modules[i][8]
                    #sayw(scale_vrml)
                    #scale_val=scale_vrml.split(" ")
                    scale_val=scale_vrml
                    #sayw(scale_val)
                    createScaledBBox(model_name,scale_val)
                    module_path='internal shape'
                if module_path!='not-found' and module_path!='internal shape':
                    #FreeCADGui.Selection.removeSelection(FreeCAD.activeDocument().ActiveObject)  mauitemp volume diff
                    say("opening "+ module_path)
                    mod_cnt+=1
                    doc1=FreeCAD.ActiveDocument
                    counterObj=0;counter=0
                    prevObjs = doc1.Objects
                    for ObJ in doc1.Objects:
                        counterObj+=1
                    say(model_name)
                    Links_available = False
                    if 'LinkView' in dir(FreeCADGui):
                        Links_available = True
                    if model_name not in loaded_models:
                        loaded_models.append(model_name)
                        #sayw(module_path)
                        #make_unicode(module_path)
                        #module_path_n = re.sub("/", "\\\\", module_path)
                        #sayerr(module_path_n)
                        #ImportGui.insert(module_path_n,FreeCAD.ActiveDocument.Name)
                        try: #tobefixed HERE
                            # support for stpZ files
                            if module_path.lower().endswith('stpz'):
                                import stepZ
                                stepZ.insert(module_path,FreeCAD.ActiveDocument.Name)
                            elif module_path.lower().endswith('iges') or module_path.lower().endswith('igs'):
                                sayerr("bug for ImportGui *.iges ... using Part.insert")
                                Part.insert(module_path,FreeCAD.ActiveDocument.Name)
                            else:
                                ImportGui.insert(module_path,FreeCAD.ActiveDocument.Name)
                                # on FC0.20+ there is an issue in inserting a 'compound'
                                # FreeCAD.ActiveDocument.ActiveObject.recompute(True)
                                # say('model imported w ImportGui')
                            #FreeCADGui.Selection.clearSelection()
                            imported_obj_list = []
                            counterTmp=0
                            for ObJ in doc1.Objects:
                                counterTmp+=1#stop
                            mp_found=False
                            if counterTmp!=counterObj+1:
                                #multipart loaded
                                #print ('allow_compound ',allow_compound)
                                FreeCADGui.Selection.clearSelection()
                                mp_found=True
                                #if allow_compound != 'False' and allow_compound != 'Hierarchy':
                                if allow_compound != 'False' and (allow_compound != 'Hierarchy' or not Links_available):
                                    create_compound(counterObj,model_name)
                                    myStep = FreeCAD.ActiveDocument.ActiveObject
                                    impLabel = myStep.Label
                                elif allow_compound == 'Hierarchy' and Links_available:
                                    imported_obj_list = doc1.Objects[counterObj+1:]
                                    compound_found=True
                                    #say(str(doc1.Objects)+' HERE')
                                    #sayw(str(imported_obj_list)+' HERE')
                                    newStep = find_top_container(imported_obj_list)
                                    if newStep is not None:
                                        impLabel = make_string(newStep.Label)
                                    else: #old format import multi objs without a Part container
                                        actObjs = doc1.Objects
                                        actObjNum = len (actObjs)
                                        newStep = doc1.addObject('App::Part',model_name)
                                        impLabel = make_string(newStep.Label)
                                        for o in actObjs[counterObj:]:
                                            doc1.getObject(newStep.Name).addObject(doc1.getObject(o.Name))
                                            #print(o.Label)
                                        
                            #myStep = FreeCAD.ActiveDocument.ActiveObject
                            #print(myStep.Label)
                            #impLabel = myStep.Label
                            if (allow_compound != 'Hierarchy' or not Links_available) or not mp_found :
                                newStep=reset_prop_shapes(FreeCAD.ActiveDocument.ActiveObject,FreeCAD.ActiveDocument, FreeCAD,FreeCADGui,True)
                                myStep=newStep
                                if wrl_model != '':
                                    wrl_module_path = module_path[:module_path.rfind(u'.')]+wrl_model[-4:]
                                    step_transparency = check_wrl_transparency(wrl_module_path)
                                    FreeCADGui.ActiveDocument.getObject(myStep.Name).Transparency = step_transparency
                                impLabel = make_string(myStep.Label)
                            #use_pypro=False
                            if use_pypro:  #use python property for timestamp
                                myObj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython","model3D")
                                myObj.ViewObject.Proxy = 0 # this is mandatory unless we code the ViewProvider too
                                myObj.Shape = newStep.Shape
                                newStep.Label = 'old'
                                #myObj.Label = impLabel
                                #print(modules[i][10]);print(modules[i][11])
                                myObj.addProperty("App::PropertyString","TimeStamp")
                                myObj.TimeStamp=str(modules[i][10])
                                myObj.addProperty("App::PropertyString","Reference")
                                myObj.Reference=str(modules[i][11])
                                if '*' not in myObj.Reference:
                                    myObj.Label = myObj.Reference + '_'+ impLabel
                                else:
                                    myObj.Label = 'REF_'+impLabel + '_'
                                FreeCADGui.ActiveDocument.ActiveObject.ShapeColor=FreeCADGui.ActiveDocument.getObject(newStep.Name).ShapeColor
                                FreeCADGui.ActiveDocument.ActiveObject.LineColor=FreeCADGui.ActiveDocument.getObject(newStep.Name).LineColor
                                FreeCADGui.ActiveDocument.ActiveObject.PointColor=FreeCADGui.ActiveDocument.getObject(newStep.Name).PointColor
                                FreeCADGui.ActiveDocument.ActiveObject.DiffuseColor=FreeCADGui.ActiveDocument.getObject(newStep.Name).DiffuseColor
                                FreeCADGui.ActiveDocument.ActiveObject.Transparency=FreeCADGui.ActiveDocument.getObject(newStep.Name).Transparency
                                FreeCAD.ActiveDocument.removeObject(newStep.Name)
                            else: #use Label for timestamp
                                myReference=str(modules[i][11]).rstrip('"').lstrip('"')
                                myTimeStamp=str(modules[i][10])
                                if len(myTimeStamp)> 8:
                                    myTimeStamp=myTimeStamp[-12:]
                                myModelNbr=(modules[i][12])
                                #print (myModelNbr)#;stop
                                if myModelNbr == 1:
                                    myModelNbr = ''
                                else:
                                    myModelNbr = '['+str(myModelNbr)+']'
                                if '*' not in myReference:
                                    newStep.Label = myReference + '_'+ impLabel + '_' + myTimeStamp + myModelNbr
                                else:
                                    newStep.Label = 'REF_'+impLabel + '_'  + myTimeStamp + myModelNbr
                                #stop
                            #sayerr('loading first time!!!')
                            counterTmp=0
                            for ObJ in doc1.Objects:
                                counterTmp+=1#stop
                            #sayw(str(counterObj)+":"+str(counterTmp))
                            #stop
                            if counterTmp==counterObj:
                                #bug in ImportGui.insert iges file
                                sayerr("bug for ImportGui *.iges ... using Part.insert")
                                Part.insert(module_path,FreeCAD.ActiveDocument.Name)
                            # s = Part.Shape()
                            # s.read(module_path)       # incoming file igs, stp, stl, brep NO colors!
                            # Part.show(s)
                            #Part.Shape.read(module_path)
                            #Part.insert(module_path,FreeCAD.ActiveDocument.Name)
                        except: #tobefixed
                            sayerr('3D STEP model '+model_name+' is WRONG')
                            msg="""3D STEP model <b><font color=red>"""
                            msg+=model_name+"</font> is WRONG</b><br>or are not allowed Multi Part objects...<br>"
                            msg+="@ "+module_path+" <br>...stopping execution! <br>Please <b>fix</b> the model or change your settings."
                            QtGui.QApplication.restoreOverrideCursor()
                            reply = QtGui.QMessageBox.information(None,"Info ...",msg)
                            stop   
                        if allow_compound != 'False' and (allow_compound != 'Hierarchy' or not Links_available):
                            create_compound(counterObj,model_name)
                            newobj = FreeCAD.ActiveDocument.ActiveObject
                            if not use_pypro:
                                if '*' not in myReference:
                                    newobj.Label = myReference + '_'+ impLabel + '_' + myTimeStamp + myModelNbr
                                else:
                                    newobj.Label = 'REF_'+impLabel + '_'  + myTimeStamp + myModelNbr
                        ##addProperty mod
                        #newobj=reset_prop_shapes(FreeCAD.ActiveDocument.ActiveObject,FreeCAD.ActiveDocument, FreeCAD,FreeCADGui)
                        elif allow_compound == 'Hierarchy' and mp_found:
                            newobj = newStep
                            #tobefixed
                            if not use_pypro:
                                if '*' not in myReference:
                                    newobj.Label = myReference + '_'+ impLabel + '_' + myTimeStamp + myModelNbr
                                else:
                                    newobj.Label = 'REF_'+impLabel + '_'  + myTimeStamp + myModelNbr
                        else:
                            newobj = FreeCAD.ActiveDocument.ActiveObject                        ##addProperty mod
                        #newobj=reset_prop_shapes(FreeCAD.ActiveDocument.ActiveObject,FreeCAD.ActiveDocument, FreeCAD,FreeCADGui)
                        #newobj = FreeCAD.ActiveDocument.ActiveObject
                        #stop
                        ##newobj.Label=newobj.Label+"_"
                        # not adding '_' at the end of the name
                        if (bbox_all==1) or (bbox_list==1):
                            if whitelisted_model_elements.find(model_name) == -1:
                                bboxLabel=newobj.Label=newobj.Label
                                newobj=createSolidBBox3(newobj)
                        skip_status="not"
                        #tobefixed volume for App::Part
                        if volume_minimum != 0 or height_minimum != 0: #if checking volume or height
                            if newobj.Shape.Volume>volume_minimum:  #mauitemp min vol
                                if abs(newobj.Shape.BoundBox.ZLength)>height_minimum:  #mauitemp min height
                                    if (height_minimum!=0):
                                        say("height > Min height "+ str(newobj.Shape.BoundBox.ZLength) + " "+newobj.Label)
                                    if (volume_minimum!=0):
                                        say("Volume > Min Volume "+ str(newobj.Shape.Volume) + " "+newobj.Label)
                                else:
                                    skip_status="skip"
                                    say("height <= Min height "+ str(newobj.Shape.BoundBox.ZLength) + " "+newobj.Label)
                            else:
                                skip_status="skip"
                                say("Volume <= Min Volume "+ str(newobj.Shape.BoundBox.ZLength) + " "+newobj.Label)
                        loaded_models_skipped.append(skip_status)
                        use_cache=0
                        #say("NO use_cache")
                        FreeCADGui.Selection.clearSelection()
                        for ObJ in doc1.Objects:
                            counter+=1
                        if counterObj+1 != counter and (allow_compound != 'Hierarchy' or not Links_available):
                            msg="""3D STEP model <b><font color=red>"""
                            msg+=model_name+"</font> is NOT fused ('union') in a single part</b> ...<br>"
                            msg+="@ "+module_path+" <br>...stopping execution! <br>Please <b>fix</b> the model."
                            QtGui.QApplication.restoreOverrideCursor()
                            reply = QtGui.QMessageBox.information(None,"Info ...",msg)
                            stop
                        if skip_status!="skip":
                            loaded_model_objs.append(newobj)
                        else:
                            loaded_model_objs.append(None)
                            FreeCAD.activeDocument().removeObject(newobj.Name)
                    else:
                        use_cache=1
                        #sayw("using cache!!!")
                    #say(loaded_models);say(" models")
                    #say(str(len(loaded_model_objs))+" nbr loaded objs")
                    if use_cache:
                        counterObj=counterObj-2
                    pos_x=modules[i][1]-off_x
                    pos_y=modules[i][2]-off_y
                    rot=modules[i][3]
                    step_layer=modules[i][4]
                    #wrl_off_x=modules[i][6]
                    #rotz_vrml_norm=modules[i][7][0].replace("(xyz ","")
                    #rotz_vrml_norm=modules[i][7].replace("(xyz ","")
                    #say("rotz_vrml_norm ");sayw(rotz_vrml_norm)
                    wrl_rot=modules[i][7]
                    #sayerr(wrl_rot);sayw(float(wrl_rot[0]));stop
                    pos_vrml=modules[i][6]
                    wrl_pos=pos_vrml
                    #sayerr(wrl_pos);sayw(float(wrl_pos[0]));stop
                    isVirtual=modules[i][9]
                    isHidden=modules[i][13]
                    if (isHidden):
                        md_hide=True
                    else:
                        md_hide=False
                    
                    #if show_debug:
                    #    sayw(wrl_rot)
                    #    sayerr(modules[i])
                    #wrl_pos=pos_vrml[0].split(" ")
                    #wrl_pos=pos_vrml.split(" ")
                    #say(rotz_vrml_norm)
                    #sayw("wrl rot ");sayw(wrl_rot)
                    #say("wrl pos ");sayw(wrl_pos)                   
                    #say (str(rot))
                    for j in range(len(loaded_models)):
                        if loaded_models[j]==model_name:
                            #say (str(i)+" i")
                            idxO=j
                    if loaded_models_skipped[idxO]!="skip":
                        if use_cache:
                            #mod_cnt+=1
                            sayw('copying from cache')
                            ##impPart=copy_objs(loaded_model_objs[idxO],FreeCAD.ActiveDocument, FreeCAD,FreeCADGui)
                            ### FreeCAD.ActiveDocument.addObject('Part::Feature',loaded_model_objs[idxO].Label).Shape=loaded_model_objs[idxO].Shape
                            ### #FreeCAD.ActiveDocument.ActiveObject.Label=obj.Label
                            ### FreeCADGui.ActiveDocument.ActiveObject.ShapeColor=Gui.ActiveDocument.getObject(loaded_model_objs[idxO].Name).ShapeColor
                            ### FreeCADGui.ActiveDocument.ActiveObject.LineColor=Gui.ActiveDocument.getObject(loaded_model_objs[idxO].Name).LineColor
                            ### FreeCADGui.ActiveDocument.ActiveObject.PointColor=Gui.ActiveDocument.getObject(loaded_model_objs[idxO].Name).PointColor
                            ### FreeCADGui.ActiveDocument.ActiveObject.DiffuseColor=Gui.ActiveDocument.getObject(loaded_model_objs[idxO].Name).DiffuseColor
                            ### FreeCAD.ActiveDocument.recompute()
                            try: # Links ATM don't support added proprierties
                                if use_Links and links_imp_mode == 'links_allowed':
                                    o = loaded_model_objs[idxO]
                                    # FreeCAD.ActiveDocument.addObject('App::Link',o.Label+'_ln_').setLink(o)
                                    if use_pypro:
                                        FreeCAD.ActiveDocument.addObject('App::LinkPython',o.Label).setLink(o)
                                        FreeCAD.ActiveDocument.ActiveObject.addProperty("App::PropertyString","TimeStamp")
                                        #FreeCAD.ActiveDocument.ActiveObject.TimeStamp=str(modules[i][10])
                                        FreeCAD.ActiveDocument.ActiveObject.addProperty("App::PropertyString","Reference")
                                        #FreeCAD.ActiveDocument.ActiveObject.Reference=str(modules[i][11])
                                        FreeCAD.ActiveDocument.ActiveObject.ViewObject.Proxy = 0
                                    else:
                                        FreeCAD.ActiveDocument.addObject('App::Link',o.Label+'_ln_').setLink(o)
                                else:
                                    FreeCAD.ActiveDocument.copyObject(loaded_model_objs[idxO], True)
                                #allow_compound != 'Hierarchy':
                                impPart=FreeCAD.ActiveDocument.ActiveObject
                                if use_pypro:
                                    impPart.TimeStamp=str(modules[i][10])
                                    impPart.Reference=str(modules[i][11])
                                    if '*' not in impPart.Reference:
                                        impPart.Label = loaded_model_objs[idxO].Label[loaded_model_objs[idxO].Label.find('_')+1:]
                                        impPart.Label = impPart.Reference + '_' + impPart.Label # loaded_model_objs[idxO].Label
                                        #impPart.Label = impPart.Reference + '_'+ impLabel
                                    #say("FC 0.15 copy method for preserving color in fusion")
                                    else:
                                        impPart.Label = 'REF_'+loaded_model_objs[idxO].Label + '_' + myTimeStamp
                                else:
                                    myTimeStamp=str(modules[i][10])
                                    if len(myTimeStamp)> 8:
                                        myTimeStamp=myTimeStamp[-12:]
                                    myReference=str(modules[i][11]).rstrip('"').lstrip('"')
                                    myModelNbr=(modules[i][12])
                                    #print (myModelNbr);stop
                                    if myModelNbr == 1:
                                        myModelNbr = ''
                                    else:
                                        myModelNbr = '['+str(myModelNbr)+']'
                                    if '*' not in myReference:
                                        impPart.Label = loaded_model_objs[idxO].Label[loaded_model_objs[idxO].Label.find('_')+1:loaded_model_objs[idxO].Label.rfind('_')]
                                        impPart.Label = myReference + '_' + impPart.Label + '_' + myTimeStamp + myModelNbr
                                        # loaded_model_objs[idxO].Label
                                    else:
                                        impPart.Label = 'REF_'+loaded_model_objs[idxO].Label[:loaded_model_objs[idxO].Label.rfind('_')] + '_'  + myTimeStamp + myModelNbr
                            except:
                                #impPart=copy_objs(loaded_model_objs[idxO],FreeCAD.ActiveDocument, FreeCAD,FreeCADGui)
                                impPart=copy_objs(loaded_model_objs[idxO],FreeCAD.ActiveDocument)
                                sayw("fusion color problem in FC earlier than 0.15\n")
                                pass
                            ##
                            #impPart=reset_prop_shapes2(impPart,FreeCAD.ActiveDocument, FreeCAD,FreeCADGui)
                            ##resetting placement properties
                            impPart.Placement = FreeCAD.Placement(FreeCAD.Vector(pos_x,pos_y,-pcbThickness),FreeCAD.Rotation(FreeCAD.Vector(0,1,0),180))
                            #obj.Placement = impPart.Placement
                            if use_Links and links_imp_mode == 'links_allowed':
                                shape=Part.getShape(o)
                            else:
                                shape=impPart.Shape.copy()
                            shape.Placement=impPart.Placement;
                            shape.rotate((pos_x,pos_y,0),(0,0,1),rot)
                            impPart.Placement=shape.Placement
                            #impPart.Label = impPart.Label + '_ch_'
                            #sayerr('caching')
                        else:
                            impPart=loaded_model_objs[idxO]
                            #impPart.Label = impPart.Label + '_nc_'
                        ## say(loaded_model_objs)
                        say("module "+step_module)
                        #say("selection 3D model "+ impPart.Label)
                        #to verify!!!! next row
                        ##impPart=reset_prop_shapes(impPart,FreeCAD.ActiveDocument, FreeCAD,FreeCADGui)                        
                        model3D=impPart.Name
                        #say("impPart "+ impPart.Name)
                        obj = FreeCAD.ActiveDocument.getObject(model3D)
                        FreeCADGui.Selection.addSelection(obj)
                        obj=FreeCAD.ActiveDocument.ActiveObject
                        #volume_minimum=1
                        myPart=FreeCAD.ActiveDocument.getObject(obj.Name)   #mauitemp min vol
                        if md_hide:
                            myPart.ViewObject.Visibility=False
                            # myPart.ViewObject.Transparency=70
                            sayerr('hiding '+myPart.Label)
                            my_hide_list+=myPart.Label+'\r\n'
                        #else:
                        #    myPart.ViewObject.Transparency=0
                            # sayerr('hiding '+myPart.Label)
                        #sayw(obj.Label)
                        #sayw(step_layer);
                        #sayw(str(myPart.Shape.Volume))
                        #sayw(str(myPart.Shape.BoundBox.ZLength))
                        if step_layer == 'Top':
                            if full_placement:
                                ## new placement wip
                                #impPart.Placement = FreeCAD.Placement(FreeCAD.Vector(pos_x+float(wrl_pos[0]),pos_y+float(wrl_pos[1]),0+float(wrl_pos[2])),FreeCAD.Rotation(FreeCAD.Vector(0,0,1),rot))
                                #                                                                                                                                                         (yaw z, pitch y, roll x) 
                                #impPart.Placement = FreeCAD.Placement(FreeCAD.Vector(pos_x+float(wrl_pos[0])*25.4,pos_y+float(wrl_pos[1])*25.4,0+float(wrl_pos[2])*25.4),FreeCAD.Rotation(-float(wrl_rot[2]),-float(wrl_rot[1]),-float(wrl_rot[0])))
                                ##impPart.Placement = FreeCAD.Placement(FreeCAD.Vector(pos_x+float(wrl_pos[0])*25.4,pos_y+float(wrl_pos[1])*25.4,0+float(wrl_pos[2])*25.4),FreeCAD.Rotation(rot,-float(wrl_rot[1]),-float(wrl_rot[0]))) #rot is already rot fp -rot wrl
                                #say("rot z top ");sayw(wrl_rot);sayw(rot)
                                impPart.Placement = FreeCAD.Placement(FreeCAD.Vector(pos_x+float(wrl_pos[0])*25.4,pos_y+float(wrl_pos[1])*25.4,0+float(wrl_pos[2])*25.4),FreeCAD.Rotation(-float(wrl_rot[2]),-float(wrl_rot[1]),-float(wrl_rot[0]))) #rot is already rot fp -rot wrl
                                if impPart.TypeId=='App::Link' or impPart.TypeId=='App::LinkPython':
                                    shape=Part.getShape(o)
                                elif impPart.TypeId=='App::Part': #tobefixed
                                    shape=Part.getShape(impPart)
                                else:
                                    shape=impPart.Shape.copy()
                                shape.Placement=impPart.Placement;
                                shape.rotate((pos_x,pos_y,0),(0,0,1),rot+float(wrl_rot[2]))
                                impPart.Placement=shape.Placement;
                                ##TBChecked
                                if force_transparency:
                                    FreeCADGui.ActiveDocument.ActiveObject.Transparency=70
                                ##TBChecked
                            else:
                                impPart.Placement = FreeCAD.Placement(FreeCAD.Vector(pos_x,pos_y,0),FreeCAD.Rotation(FreeCAD.Vector(0,0,1),rot))
                            FreeCADGui.Selection.addSelection(impPart)
                            ## to evaluate to add App::Part hierarchy
                            # App.activeDocument().Tip = App.activeDocument().addObject('App::Part','Part')
                            # App.activeDocument().Part.Label = 'Part'
                            # Gui.activeView().setActiveObject('part', App.activeDocument().Part)
                            # App.ActiveDocument.recompute()
                            if isVirtual == 0:
                                if use_AppPart and not use_LinkGroups: #layer Top                                  
                                    FreeCAD.ActiveDocument.getObject(top_name).addObject(impPart)
                                    modelTop_nbr+=1
                                elif use_LinkGroups:
                                    #FreeCAD.ActiveDocument.getObject(impPart.Name).adjustRelativeLinks(FreeCAD.ActiveDocument.getObject('Top'))
                                    FreeCAD.ActiveDocument.getObject(top_name).ViewObject.dropObject(FreeCAD.ActiveDocument.getObject(impPart.Name),FreeCAD.ActiveDocument.getObject(impPart.Name),'',[])
                                    modelTop_nbr+=1
                                else:
                                    FreeCAD.ActiveDocument.getObject(stepM_name).addObject(impPart)
                            else:  #virtual
                                if use_AppPart and not use_LinkGroups: #layer Top                                  
                                    #print(topV_name)
                                    FreeCAD.ActiveDocument.getObject(topV_name).addObject(impPart)
                                    virtualTop_nbr+=1
                                elif use_LinkGroups:
                                    #FreeCAD.ActiveDocument.getObject(impPart.Name).adjustRelativeLinks(FreeCAD.ActiveDocument.getObject('TopV'))
                                    FreeCAD.ActiveDocument.getObject(topV_name).ViewObject.dropObject(FreeCAD.ActiveDocument.getObject(impPart.Name),FreeCAD.ActiveDocument.getObject(impPart.Name),'',[])
                                    virtualTop_nbr+=1
                                else:
                                    FreeCAD.ActiveDocument.getObject(stepV_name).addObject(impPart)
                                virtual_nbr+=1
                        ###
                        else:
                        #Bottom
                        #Bottom
                            #impPart=reset_prop_shapes2(impPart,FreeCAD.ActiveDocument, FreeCAD,FreeCADGui)
                            if full_placement:
                                #impPart.Placement = FreeCAD.Placement(FreeCAD.Vector(pos_x,pos_y,-pcbThickness),FreeCAD.Rotation(FreeCAD.Vector(0,1,0),180))
                                ## new placement wip
                                #impPart.Placement = FreeCAD.Placement(FreeCAD.Vector(pos_x+float(wrl_pos[1])*25.4,pos_y+float(wrl_pos[0])*25.4,-pcbThickness-float(wrl_pos[2])*25.4),FreeCAD.Rotation(-float(wrl_rot[2])-rot+180,-float(wrl_rot[1])+180,-float(wrl_rot[0])))
                                ##impPart.Placement = FreeCAD.Placement(FreeCAD.Vector(pos_x+float(wrl_pos[1])*25.4,pos_y+float(wrl_pos[0])*25.4,-pcbThickness-float(wrl_pos[2])*25.4),FreeCAD.Rotation(-rot+180,-float(wrl_rot[1])+180,-float(wrl_rot[0])))  #rot is already rot fp -rot wrl
                                impPart.Placement = FreeCAD.Placement(FreeCAD.Vector(pos_x+float(wrl_pos[0])*25.4,pos_y+float(wrl_pos[1])*25.4,+pcbThickness+float(wrl_pos[2])*25.4),FreeCAD.Rotation(-float(wrl_rot[2]),-float(wrl_rot[1]),-float(wrl_rot[0]))) #rot is already rot fp -rot wrl
                                if impPart.TypeId=='App::Link' or impPart.TypeId=='App::LinkPython':
                                    shape=Part.getShape(o)
                                else:
                                    shape=impPart.Shape.copy()
                                shape.Placement=impPart.Placement;
                                shape.rotate((pos_x,pos_y,0),(0,0,1),180+rot+float(wrl_rot[2]))
                                impPart.Placement=shape.Placement;
                                if impPart.TypeId=='App::Link' or impPart.TypeId=='App::LinkPython':
                                    shape=Part.getShape(o)
                                else:
                                    shape=impPart.Shape.copy()
                                shape.Placement=impPart.Placement;
                                shape.rotate((pos_x,pos_y,0),(0,1,0),180)
                                impPart.Placement=shape.Placement;
                                if force_transparency:
                                    FreeCADGui.ActiveDocument.ActiveObject.Transparency=60
                                #say("rot z bot ");sayw(wrl_rot);sayw(rot)
                                #impPart.Placement = FreeCAD.Placement(FreeCAD.Vector(pos_x+float(wrl_pos[0])*25.4,pos_y+float(wrl_pos[1])*25.4,-pcbThickness+float(wrl_pos[2])*25.4),FreeCAD.Rotation(FreeCAD.Vector(0,1,0),180))
                            else:
                                impPart.Placement = FreeCAD.Placement(FreeCAD.Vector(pos_x,pos_y,-pcbThickness),FreeCAD.Rotation(FreeCAD.Vector(0,1,0),180))
                            #obj.Placement = impPart.Placement
                                if impPart.TypeId=='App::Link' or impPart.TypeId=='App::LinkPython':
                                    shape=Part.getShape(o)
                                else:
                                    shape=impPart.Shape.copy()
                                shape.Placement=impPart.Placement;
                            #if not full_placement:
                                #shape.rotate((pos_x+float(wrl_pos[0])*25.4,pos_y+float(wrl_pos[1])*25.4,-pcbThickness+float(wrl_pos[2])*25.4),FreeCAD.Rotation(-float(wrl_rot[2]),-float(wrl_rot[1])+180,-float(wrl_rot[0])))
                            #else:
                                shape.rotate((pos_x,pos_y,-pcbThickness),(0,0,1),-rot+180)
                                impPart.Placement=shape.Placement
                            FreeCADGui.Selection.addSelection(impPart)
                            FreeCAD.ActiveDocument.getObject(impPart.Name)
                            if isVirtual == 0:
                                if use_AppPart and not use_LinkGroups: #layer Top                                  
                                    FreeCAD.ActiveDocument.getObject(bot_name).addObject(impPart)
                                    modelBot_nbr+=1
                                elif use_LinkGroups:
                                    #FreeCAD.ActiveDocument.getObject(impPart.Name).adjustRelativeLinks(FreeCAD.ActiveDocument.getObject('Bot'))
                                    FreeCAD.ActiveDocument.getObject(bot_name).ViewObject.dropObject(FreeCAD.ActiveDocument.getObject(impPart.Name),FreeCAD.ActiveDocument.getObject(impPart.Name),'',[])
                                    modelBot_nbr+=1
                                else:
                                    FreeCAD.ActiveDocument.getObject(stepM_name).addObject(impPart)
                            else:  #virtual
                                if use_AppPart and not use_LinkGroups: #layer Top
                                    FreeCAD.ActiveDocument.getObject(botV_name).addObject(impPart)
                                    virtualBot_nbr+=1
                                elif use_LinkGroups:
                                    #FreeCAD.ActiveDocument.getObject(impPart.Name).adjustRelativeLinks(FreeCAD.ActiveDocument.getObject('BotV'))
                                    FreeCAD.ActiveDocument.getObject(botV_name).ViewObject.dropObject(FreeCAD.ActiveDocument.getObject(impPart.Name),FreeCAD.ActiveDocument.getObject(impPart.Name),'',[])
                                    virtualBot_nbr+=1
                                else:
                                    FreeCAD.ActiveDocument.getObject(stepV_name).addObject(impPart)
                                virtual_nbr+=1
                ###
                elif module_path=='internal shape':
                    impPart=FreeCAD.ActiveDocument.ActiveObject
                    scale_vrml=modules[i][8]
                    #sayw(scale_vrml)
                    #scale_val=scale_vrml.split(" ")
                    scale_val=scale_vrml
                    #sayw(scale_val)
                    pos_x=modules[i][1]-off_x
                    pos_y=modules[i][2]-off_y
                    rot=modules[i][3]
                    wrl_rot=modules[i][7]
                    step_layer=modules[i][4]
                    #wrl_off_x=modules[i][6]
                    #rotz_vrml_norm=modules[i][7][0].replace("(xyz ","")
                    #rotz_vrml_norm=modules[i][7].replace("(xyz ","")
                    #say("rotz_vrml_norm ");sayw(rotz_vrml_norm)
                    #wrl_rot=rotz_vrml_norm.split(" ")
                    pos_vrml=modules[i][6]
                    wrl_pos=pos_vrml
                    #wrl_pos=pos_vrml[0].split(" ")
                    #wrl_pos=pos_vrml.split(" ")
                    #say(rotz_vrml_norm)
                    #sayw("wrl rot ");sayw(wrl_rot)
                    #say("wrl pos ");sayw(wrl_pos)
                    shape_vol=abs(float(scale_val[0])*float(scale_val[1])*float(scale_val[2]))
                    skip_status="not"
                    if shape_vol>volume_minimum:  #mauitemp min vol
                        if abs(float(scale_val[2]))>height_minimum:  #mauitemp min height
                            if (height_minimum!=0):
                                say("height > Min height "+ str(scale_val[2]) + " "+impPart.Label)
                            if (volume_minimum!=0):
                                say("Volume > Min Volume "+ str(shape_vol) + " "+impPart.Label)
                        else:
                            skip_status="skip"
                            say("height <= Min height "+ str(scale_val[2]) + " "+impPart.Label)
                    else:
                        skip_status="skip"
                        say("Volume <= Min Volume "+ str(shape_vol) + " "+impPart.Label)
                    if skip_status=="not":
                        if step_layer == 'Top':
                            if full_placement:
                                ## new placement wip
                                #impPart.Placement = FreeCAD.Placement(FreeCAD.Vector(pos_x+float(wrl_pos[0]),pos_y+float(wrl_pos[1]),0+float(wrl_pos[2])),FreeCAD.Rotation(FreeCAD.Vector(0,0,1),rot))
                                #                                                                                                                                                         (yaw z, pitch y, roll x) 
                                #impPart.Placement = FreeCAD.Placement(FreeCAD.Vector(pos_x+float(wrl_pos[0])*25.4,pos_y+float(wrl_pos[1])*25.4,0+float(wrl_pos[2])*25.4),FreeCAD.Rotation(-float(wrl_rot[2]),-float(wrl_rot[1]),-float(wrl_rot[0])))
                                #impPart.Placement = FreeCAD.Placement(FreeCAD.Vector(pos_x+float(wrl_pos[0])*25.4,pos_y+float(wrl_pos[1])*25.4,0+float(wrl_pos[2])*25.4),FreeCAD.Rotation(rot,-float(wrl_rot[1]),-float(wrl_rot[0]))) #rot is already rot fp -rot wrl
                                #impPart.Placement = FreeCAD.Placement(FreeCAD.Vector(pos_x+float(wrl_pos[0])*25.4,pos_y+float(wrl_pos[1])*25.4,0+float(wrl_pos[2])*25.4),FreeCAD.Rotation(rot,-float(wrl_rot[1]),-float(wrl_rot[0]))) #rot is already rot fp -rot wrl
                                impPart.Placement = FreeCAD.Placement(FreeCAD.Vector(pos_x+float(wrl_pos[0])*25.4,pos_y+float(wrl_pos[1])*25.4,0+float(wrl_pos[2])*25.4),FreeCAD.Rotation(-float(wrl_rot[2]),-float(wrl_rot[1]),-float(wrl_rot[0]))) #rot is already rot fp -rot wrl
                                shape=impPart.Shape.copy()
                                shape.Placement=impPart.Placement;
                                shape.rotate((pos_x,pos_y,0),(0,0,1),rot+float(wrl_rot[2]))
                                impPart.Placement=shape.Placement;
                                if force_transparency:
                                    FreeCADGui.ActiveDocument.ActiveObject.Transparency=100
                                ##TBChecked shapes
                                #say("rot z top ");sayw(wrl_rot);sayw(rot)
                            else:
                                impPart.Placement = FreeCAD.Placement(FreeCAD.Vector(pos_x,pos_y,0),FreeCAD.Rotation(FreeCAD.Vector(0,0,1),rot))
                            FreeCADGui.Selection.addSelection(impPart)
                            if use_AppPart: #Top
                                FreeCAD.ActiveDocument.getObject(top_name).addObject(impPart)
                                modelTop_nbr+=1
                            else:
                                FreeCAD.ActiveDocument.getObject(stepM_name).addObject(impPart)
                        else:
                        #Bottom
                        #Bottom
                            #impPart=reset_prop_shapes2(impPart,FreeCAD.ActiveDocument, FreeCAD,FreeCADGui)
                            if full_placement:
                                #impPart.Placement = FreeCAD.Placement(FreeCAD.Vector(pos_x,pos_y,-pcbThickness),FreeCAD.Rotation(FreeCAD.Vector(0,1,0),180))
                                ## new placement wip
                                #impPart.Placement = FreeCAD.Placement(FreeCAD.Vector(pos_x+float(wrl_pos[1])*25.4,pos_y+float(wrl_pos[0])*25.4,-pcbThickness-float(wrl_pos[2])*25.4),FreeCAD.Rotation(-float(wrl_rot[2])-rot+180,-float(wrl_rot[1])+180,-float(wrl_rot[0])))
                                # impPart.Placement = FreeCAD.Placement(FreeCAD.Vector(pos_x+float(wrl_pos[1])*25.4,pos_y+float(wrl_pos[0])*25.4,-pcbThickness),FreeCAD.Rotation(-float(wrl_rot[2])+180,-float(wrl_rot[1])+180,-float(wrl_rot[0])))  #rot is already rot fp -rot wrl
                                # #impPart.Placement = FreeCAD.Placement(FreeCAD.Vector(pos_x+float(wrl_pos[1])*25.4,pos_y+float(wrl_pos[0])*25.4,-pcbThickness-float(wrl_pos[2])*25.4),FreeCAD.Rotation(float(wrl_rot[2]),-float(wrl_rot[1]),-float(wrl_rot[0]))) #rot is already rot fp -rot wrl
                                # shape=impPart.Shape.copy()
                                # shape.Placement=impPart.Placement;
                                # shape.rotate((pos_x+float(wrl_pos[1])*25.4,pos_y+float(wrl_pos[0])*25.4,-pcbThickness-float(wrl_pos[2])*25.4),(0,0,1),-180+rot-float(wrl_rot[2]))
                                # impPart.Placement=shape.Placement;
                                #impPart.Placement = FreeCAD.Placement(FreeCAD.Vector(pos_x+float(wrl_pos[1])*25.4,pos_y+float(wrl_pos[0])*25.4,-pcbThickness-float(wrl_pos[2])*25.4),FreeCAD.Rotation(-float(wrl_rot[2])-rot+180,-float(wrl_rot[1])+180,-float(wrl_rot[0])))
                                impPart.Placement = FreeCAD.Placement(FreeCAD.Vector(pos_x+float(wrl_pos[0])*25.4,pos_y+float(wrl_pos[1])*25.4,+pcbThickness+float(wrl_pos[2])*25.4),FreeCAD.Rotation(-float(wrl_rot[2]),-float(wrl_rot[1]),-float(wrl_rot[0]))) #rot is already rot fp -rot wrl
                                shape=impPart.Shape.copy()
                                shape.Placement=impPart.Placement;
                                shape.rotate((pos_x,pos_y,0),(0,0,1),180+rot+float(wrl_rot[2]))
                                impPart.Placement=shape.Placement;
                                shape=impPart.Shape.copy()
                                shape.Placement=impPart.Placement;
                                shape.rotate((pos_x,pos_y,0),(0,1,0),180)
                                impPart.Placement=shape.Placement;
                                if force_transparency:
                                    FreeCADGui.ActiveDocument.ActiveObject.Transparency=60
                                ##TBChecked shapes
                                #say("rot z bot ");sayw(wrl_rot);sayw(rot)
                                #impPart.Placement = FreeCAD.Placement(FreeCAD.Vector(pos_x+float(wrl_pos[0])*25.4,pos_y+float(wrl_pos[1])*25.4,-pcbThickness+float(wrl_pos[2])*25.4),FreeCAD.Rotation(FreeCAD.Vector(0,1,0),180))
                            else:
                                impPart.Placement = FreeCAD.Placement(FreeCAD.Vector(pos_x,pos_y,-pcbThickness),FreeCAD.Rotation(FreeCAD.Vector(0,1,0),180))
                            #obj.Placement = impPart.Placement
                                shape=impPart.Shape.copy()
                                shape.Placement=impPart.Placement;
                            #if not full_placement:
                                #shape.rotate((pos_x+float(wrl_pos[0])*25.4,pos_y+float(wrl_pos[1])*25.4,-pcbThickness+float(wrl_pos[2])*25.4),FreeCAD.Rotation(-float(wrl_rot[2]),-float(wrl_rot[1])+180,-float(wrl_rot[0])))
                            #else:
                                shape.rotate((pos_x,pos_y,-pcbThickness),(0,0,1),-rot+180)
                                impPart.Placement=shape.Placement
                            FreeCADGui.Selection.addSelection(impPart)
                            FreeCAD.ActiveDocument.getObject(impPart.Name)
                            if use_AppPart: #Bot
                                FreeCAD.ActiveDocument.getObject("Bot").addObject(impPart)
                                modelBot_nbr+=1
                            else:
                                FreeCAD.ActiveDocument.getObject(stepM_name).addObject(impPart)
                    else:                        
                        FreeCAD.ActiveDocument.removeObject(impPart.Name)
                else:
                    #say("error missing "+ make_string(models3D_prefix)+make_string(step_module))
                    say("error missing "+ make_string(module_container))
                    #test = missing_models.find(make_string(step_module))
                    test = missing_models.find(make_string(module_container))
                    if test == -1:
                        #missing_models += make_string(models3D_prefix)+make_string(step_module)+'\r\n' #matched        
                        # missing_models += make_string(step_module)+'\r\n' #matched  
                        missing_models += make_string(module_container)+' (.stp or .step)\r\n' #matched 
            ###
        gui_refresh=20
        if int(PySide.QtCore.qVersion().split('.')[0]) > 4 or use_Links:  # Qt5 or Links refresh
            if mod_cnt%gui_refresh == 0: # (one on 'gui_refresh' times)
                #FreeCADGui.updateGui()
                QtGui.QApplication.processEvents()
        ###
        sayw('added '+str(mod_cnt)+' model(s)')
        ###
    ###
    #say(loaded_models);
    #sleep
    if virtual_nbr==0:
        #FreeCAD.ActiveDocument.getObject("Step_Virtual_Models").removeObjectsFromDocument()
        FreeCAD.ActiveDocument.removeObject(stepV_name)
        if use_AppPart:
            FreeCAD.ActiveDocument.removeObject(botV_name)
            FreeCAD.ActiveDocument.removeObject(topV_name)
    else:
        if use_AppPart:
            if virtualTop_nbr==0:
                #FreeCAD.ActiveDocument.getObject("TopV").removeObjectsFromDocument()
                FreeCAD.ActiveDocument.removeObject(topV_name)
                #FreeCAD.ActiveDocument.recompute()
            if virtualBot_nbr==0:
                #FreeCAD.ActiveDocument.getObject("BotV").removeObjectsFromDocument()
                FreeCAD.ActiveDocument.removeObject(botV_name)
                #FreeCAD.ActiveDocument.recompute()  
    if use_AppPart:
        if modelTop_nbr==0:
            #FreeCAD.ActiveDocument.getObject("Top").removeObjectsFromDocument()
            FreeCAD.ActiveDocument.removeObject(top_name)    
        if modelBot_nbr==0:
            #FreeCAD.ActiveDocument.getObject("Bot").removeObjectsFromDocument()
            FreeCAD.ActiveDocument.removeObject(bot_name)    
    
    FreeCAD.ActiveDocument.recompute()
    say_time()
    FreeCADGui.Selection.clearSelection()
    if 0: #try
        print('TreeView Test collapsing')
        FreeCADGui.Selection.addSelection(FreeCAD.ActiveDocument.Board)
        import kicadStepUpCMD
#!#        FreeCADGui.runCommand('ksuToolsToggleTreeView',0)
        s=FreeCADGui.Selection.getSelection()[0]
        print(s.Label)
#!#        FreeCADGui.runCommand('ksuToolsToggleTreeView',0)
#!#        #kicadStepUpCMD.ksuToolsToggleTreeView.Activated(s)
        #FreeCADGui.Selection.clearSelection()
        #FreeCADGui.Selection.addSelection(FreeCAD.ActiveDocument.Board)
        #s=FreeCADGui.Selection.getSelection()[0]
        #print(s.Label)
#!#        #kicadStepUpCMD.ksuToolsToggleTreeView.Activated(s)
        FreeCADGui.Selection.clearSelection()
    elif 0: #except:
        import expTree; 
        print('TreeView Test collapsing 2')
        #import importlib; importlib.reload(expTree);
        FreeCADGui.Selection.clearSelection()
        FreeCADGui.Selection.addSelection(FreeCAD.ActiveDocument.Board)
        expTree.collS_Tree()
        FreeCADGui.Selection.clearSelection()
        print('TreeView Test collapsing 2 step 2')
    else:
        pass
    #print (my_hide_list)
    if my_hide_list != "":
        n_rpt_max=10
        sayw(str(len(my_hide_list.split('\r\n'))-1)+" model[s] hidden")
        sayw(str(my_hide_list.split('\r\n')[:-1]))
        my_hide_res = []
        my_hide_res = my_hide_list.split('\r\n')
        wmsg="""... model[s] hidden<br>"""
        for i in range(min(len (my_hide_res),n_rpt_max)):
            wmsg=wmsg+my_hide_res[i]+'<br>'
        QtGui.QApplication.restoreOverrideCursor()
        reply = QtGui.QMessageBox.information(None,"Warning ...",wmsg+'<b><font color=blue>. . . '+str(len(my_hide_res)-1)+' model[s] hidden</font></b>' )
        
    if missing_models != '':
        last_pcb_path_local = re.sub("\\\\", "/", last_pcb_path)
        last_pcb_path_local_U = make_unicode(last_pcb_path_local)
        say("missing models");say (missing_models)
        say("searching path")
        for mpath in path_list:
            say(mpath)
        #say(models3D_prefix_U);say (models3D_prefix2_U)
        say(last_pcb_path_local_U)
        missings=[]
        missings=missing_models.split('\r\n')
        n_rpt_max=10
        #if len (missings) > n_rpt_max: #warning_nbr =-1 for skipping the test
        wmsg="""... missing module(s)<br>"""
        wmsg+="""... searching path:<br>"""
        for mpath in path_list:
            wmsg+=mpath+"""<br>"""
        #wmsg+=models3D_prefix_U+"""<br>"""
        #wmsg+=models3D_prefix2_U+"""<br>"""
        wmsg+=last_pcb_path_local_U+"""<br>"""
        wmsg+="""... missing module(s) '.step' or '.stp' or .iges' or '.igs'<br>"""
        for i in range(min(len (missings),n_rpt_max)):
            wmsg=wmsg+missings[i]+'<br>'
        QtGui.QApplication.restoreOverrideCursor()
        reply = QtGui.QMessageBox.information(None,"Error ...",wmsg+'<br><b>. . . missing '+str(len(missings)-1)+' model(s)</b>' )
        if len (missings) > warning_nbr and warning_nbr != -1: #warning_nbr =-1 for skipping the test
            QtGui.QApplication.restoreOverrideCursor()
            wmsg="""<font color=red>"""
            wmsg+="too many missing modules <b>["
            wmsg+=str(len (missings))+"]<br></b></font><font color=blue><b>Have you configured your KISYS3DMOD path<br>or 3d model prefix path?</font></b>"
            wmsg+="<br>StepUp configuration options are located in the preferences system of FreeCAD."
            wmsg+="<br></b></font><font color=blue><b>Are you on FC Snap or Flatpack?</b></font><br><i>You may need to \'bind mount\' your 3d models folder</i>"
            reply = QtGui.QMessageBox.information(None,"Error ...",wmsg)
    #if blacklisted_model_elements != '':
    #    FreeCAD.Console.PrintMessage("black-listed module "+ '\n'.join(map(str, blacklisted_models)))
    #    reply = QtGui.QMessageBox.information(None,"Info ...","... black-listed module(s)\n"+ '\n'.join(map(str, blacklisted_models)))
    #    #FreeCAD.Console.PrintMessage("black-listed module "+ '\n'.join(map(str, blacklisted_models)))
    return blacklisted_model_elements
###

def getPads(board_elab,pcbThickness):
    # pad
    TopPadList=[]
    BotPadList=[]
    HoleList=[]
    THPList=[]
    for module in re.findall(r'\[start\]\(module(.+?)\)\[stop\]', board_elab, re.MULTILINE|re.DOTALL):
        [X1, Y1, ROT] = re.search(r'\(at\s+([0-9\.-]*?)\s+([0-9\.-]*?)(\s+[0-9\.-]*?|)\)', module).groups()
        #
        X1 = float(X1)
        Y1 = float(Y1) * (-1)
        if ROT == '':
            ROT = 0.0
        else:
            ROT = float(ROT)
        #say('module pos & rot '+str(X1)+' '+str(Y1)+' '+str(ROT))
        #
        for pad in getPadsList(module):
            #say (pad)
            #   pads.append({'x': x, 'y': y, 'rot': rot, 'padType': pType, 'padShape': pShape, 'rx': drill_x, 'ry': drill_y, 'dx': dx, 'dy': dy, 'holeType': hType, 'xOF': xOF, 'yOF': yOF, 'layers': layers})
            pType = pad['padType']
            pShape = pad['padShape']
            xs = pad['x'] + X1
            ys = pad['y'] + Y1
            dx = pad['dx']
            dy = pad['dy']
            hType = pad['holeType']
            drill_x = pad['rx']
            drill_y = pad['ry']
            xOF = pad['xOF']
            yOF = pad['yOF']
            rot = pad['rot']
            if ROT != 0:
                rot -= ROT
            rx=drill_x
            ry=drill_y
            rx=float(rx)
            ry=float(ry)
            numberOfLayers = pad['layers'].split(' ')
            #if pType=="thru_hole":
            #pad shape - circle/rec/oval/trapezoid
            perc=0
            if pShape=="circle" or pShape=="oval":
                pShape="oval"
                perc=100
                # pad type - SMD/thru_hole/connect
            if dx>rx and dy>ry:
                #say(pType)
                #say(str(dx)+"+"+str(rx)+" dx,rx")
                #say(str(dy)+"+"+str(ry)+" dy,ry")
                #say(str(xOF)+"+"+str(yOF)+" xOF,yOF")
                x1=xs+xOF
                y1=ys-yOF #yoffset opposite
                #say(str(x1)+"+"+str(y1)+" x1,y1")
                top=False
                bot=False
                if 'F.Cu' in numberOfLayers:
                    top=True
                if '*.Cu' in numberOfLayers:
                    top=True
                    bot=True
                if 'B.Cu' in numberOfLayers:
                    bot=True
            if rx!=0:
                #say(str(min_drill_size));say(' ');say(rx);say(' ');say(str(ry));
                if (rx >= min_drill_size) or (ry >= min_drill_size):
                    obj=createHole3(xs,ys,rx,ry,"oval",pcbThickness) #need to be separated instructions
                    #say(HoleList)
                    if rot!=0:
                        rotateObj(obj, [xs, ys, rot])
                    rotateObj(obj, [X1, Y1, ROT])
                    HoleList.append(obj)    
            ### cmt- #todo: pad type trapez
    return HoleList
###
def getPads_flat(board_elab):
    # pad
    TopPadList=[]
    BotPadList=[]
    HoleList=[]
    THPList=[]
    for module in re.findall(r'\[start\]\(module(.+?)\)\[stop\]', board_elab, re.MULTILINE|re.DOTALL):
        [X1, Y1, ROT] = re.search(r'\(at\s+([0-9\.-]*?)\s+([0-9\.-]*?)(\s+[0-9\.-]*?|)\)', module).groups()
        #
        X1 = float(X1)
        Y1 = float(Y1) * (-1)
        if ROT == '':
            ROT = 0.0
        else:
            ROT = float(ROT)
        #say('module pos & rot '+str(X1)+' '+str(Y1)+' '+str(ROT))
        #
        for pad in getPadsList(module):
            #say (pad)
            #
            #   pads.append({'x': x, 'y': y, 'rot': rot, 'padType': pType, 'padShape': pShape, 'rx': drill_x, 'ry': drill_y, 'dx': dx, 'dy': dy, 'holeType': hType, 'xOF': xOF, 'yOF': yOF, 'layers': layers})
            pType = pad['padType']
            pShape = pad['padShape']
            xs = pad['x'] + X1
            ys = pad['y'] + Y1
            dx = pad['dx']
            dy = pad['dy']
            hType = pad['holeType']
            drill_x = pad['rx']
            drill_y = pad['ry']
            xOF = pad['xOF']
            yOF = pad['yOF']
            rot = pad['rot']
            if ROT != 0:
                rot -= ROT
            rx=drill_x
            ry=drill_y
            rx=float(rx)
            ry=float(ry)
            numberOfLayers = pad['layers'].split(' ')
            #say(numberOfLayers )
            #if pType=="thru_hole":
            #pad shape - circle/rec/oval/trapezoid
            perc=0
            if pShape=="circle" or pShape=="oval":
                pShape="oval"
                perc=100
                # pad type - SMD/thru_hole/connect
            if dx>rx and dy>ry:
                #say(pType+"")
                #say(str(dx)+"+"+str(rx)+" dx,rx")
                #say(str(dy)+"+"+str(ry)+" dy,ry")
                #say(str(xOF)+"+"+str(yOF)+" xOF,yOF")
                x1=xs+xOF
                y1=ys-yOF #yoffset opposite
                #say(str(x1)+"+"+str(y1)+" x1,y1")
                top=False
                bot=False
                if 'F.Cu' in numberOfLayers:
                    top=True
                if '*.Cu' in numberOfLayers:
                    top=True
                    bot=True
                if 'B.Cu' in numberOfLayers:
                    bot=True
            if rx!=0:
                #say(str(min_drill_size));say(' ');say(rx);say(' ');say(str(ry));
                #if (rx > min_drill_size):
                if (rx >= min_drill_size) or (ry >= min_drill_size):
                    #obj=createHole3(xs,ys,rx,ry,"oval",pcbThickness) #need to be separated instructions
                    obj=createHole4(xs,ys,rx,ry,"oval") #need to be separated instructions
                    #say(HoleList)
                    if rot!=0:
                        rotateObj(obj, [xs, ys, rot])
                    rotateObj(obj, [X1, Y1, ROT])
                    HoleList.append(obj)
            ### cmt- #todo: pad type trapez
    return HoleList
###

def Elaborate_Kicad_Board(filename):
    global xMax, xmin, yMax, ymin
    global ignore_utf8, ignore_utf8_incfg
    Levels={}
    content=[]
    #txtFile = __builtin__.open(filename,"r")
    ##txtFile = __builtin__.open(filename,"rb")
    txtFile = codecs.open(filename, mode='rb', encoding='utf-8', errors='replace', buffering=1)  #test maui utf-8
    content = txtFile.readlines()
    content.append(" ")
    txtFile.close()
    data=''.join(content)
    if ignore_utf8:
        content=re.sub(r'[^\x00-\x7F]+',' ', data) #workaround to remove utf8 extra chars
        sayw('removing utf-8 chars')
    else:
        content=data
    ## content=data
    #say(len(content))
    Kicad_Board_elaborated = content #''.join(content)
    if save_temp_data:
        home = expanduser("~")
        t1_name=home+os.sep+'test.txt'
        #f = __builtin__.open(t1_name,'w')
        # f = builtin.open(t1_name,'wb') #py2
        f = builtin.open(t1_name,'w')  #py3
        f.write(Kicad_Board_elaborated) # python will convert \n to os.linesep
        f.close() # you can omit in most cases as the destructor will call it        
    #say(len(Kicad_Board_elaborated))
    #stop
    version=getPCBVersion(Kicad_Board_elaborated)
    pcbThickness=getPCBThickness(Kicad_Board_elaborated)
    say('kicad_pcb version ' +str(version))
    if version < 3:
        QtGui.QApplication.restoreOverrideCursor()
        reply = QtGui.QMessageBox.information(None,"Error ...","... KICAD pcb version "+ str(version)+" not supported \r\n"+"\r\nplease open and save your board with the latest kicad version")
        sys.exit("pcb version not supported")
    if version==3:
        Edge_Cuts_lvl=28
        Top_lvl=15
    if version>=4:
        Edge_Cuts_lvl=44
        Top_lvl=0
    # say(Kicad_Board)
    modified = ''
    j = 0; txt = ''; start = 0; s=0; prev_char="_"
    closing_char=""
    #say (len(Kicad_Board_elaborated))
    for i in Kicad_Board_elaborated[1:]:
        if i in ['"', "'"] and s == 0:
            closing_char=i
            if prev_char!="\\":
                s = 1
        elif i in [closing_char] and s == 1:
            if prev_char!="\\":
                s = 0
        if s == 0:
            if i == '(':
                j += 1
                start = 1
            elif i == ')':
                j -= 1
        txt += i
        prev_char=i
        if j == 0 and start == 1:
            modified += '[start]' + txt.strip() + '[stop]'
            txt = ''
            start = 0
    #say(len(modified))
    #stop #maui
    layers = re.search(r'\[start\]\(layers(.+?)\)\[stop\]', modified, re.MULTILINE|re.DOTALL).group(0)
    for k in re.findall(r'\((.*?) (.*?) .*?\)', layers):
        Levels[k[1]] = int(k[0])
        if Levels[k[1]] == Edge_Cuts_lvl: ##Edge.Cuts pcb version 4
            #myfile3.write(str(k)[8:-2])
            pcbEdgeName=str(k)[8:-2]
    if save_temp_data:
        home = expanduser("~")
        t2_name=home+os.sep+'testM.txt'
        #f = __builtin__.open(t2_name,'w')
        #f = builtin.open(t2_name,'wb')  #py2
        f = builtin.open(t2_name,'w')  #p3
        f.write(modified) # python will convert \n to os.linesep
        f.close() # you can omit in most cases as the destructor will call it
    return modified,Levels,Edge_Cuts_lvl,Top_lvl,version,pcbThickness
### end Elaborate_Kicad_Board

def get3DParams (mdl_name,params,rot, virtual):
    ''' list of single 3D model with parameters 
    '''
    global addVirtual
    
    rotz_vrml_m = re.findall(r'\(rotate.*$', params)  #bug on multiple model per footprint wrl, step sequence !!!
    #sayw(rotz_vrml_m);sayw("here")
    rotz=''
    if rotz_vrml_m:
        rotz_vrml=rotz_vrml_m[0].lstrip('(rotate').lstrip(' ')
        #say('rotation ');sayw(rotz_vrml)#;
        rotz=rotz_vrml
        #rotz=rotz.lstrip('(rotate')
        #rotz=rotz[13:-1]
        rotz=rotz[5:]
        #sayw("rotz:"+rotz)
        #stop
        #say("rotz:"+rotz)
        temp=rotz.split(" ")
        #say("rotz temp:"+temp[2])
        rotz=temp[2]
        rotx=temp[0]
        roty=temp[1]
        #warn=None
        warn=""
        # if float(rotx)!=0:
        #     warn=("rx ")
        # if float(roty)!=0:
        #     warn+=("ry ")
        #if warn:
        #    sayw(warn)
        #say("rotate vrml: "+rotz)
    else:
        rotz_vrml_m="(xyz 0 0 0"
    if rotz=='':
        rotz=0.0
    else:
        rotz=float(rotz)
    rot_comb=rot-rotz  #adding vrml module z-rotation
    #re.findall(r'\(rotate\s+(.+?)\)', i)
    pos_vrml_m = re.findall(r'\(at\s\(xyz\s+(.+?)\)', params)
    pos_vrml=pos_vrml_m[0] #len(model_list)-j-1] #bug on multiple model per footprint
    #if pos_vrml:
    #    say('pos ');sayw(pos_vrml)#;
    #say(i)
    scale_vrml_m = re.findall(r'\(scale\s\(xyz\s+(.+?)\)', params)
    scale_vrml=scale_vrml_m[0] #len(model_list)-j-1] #bug on multiple model per footprint
    error_scale_module=False
    if scale_vrml:
        #say('scale ');sayw(scale_vrml)#;
        #error_scale_module=False
        scale_vrml_vals=scale_vrml.split(" ")
        xsc_vrml_val=scale_vrml_vals[0]
        ysc_vrml_val=scale_vrml_vals[1]
        zsc_vrml_val=scale_vrml_vals[2]        
        # if scale_vrml!='1 1 1':
        if float(xsc_vrml_val)!=1 or float(ysc_vrml_val)!=1 or float(zsc_vrml_val)!=1:
            if "box_mcad" not in params and "cylV_mcad" not in params and "cylH_mcad" not in params:
                sayw('wrong scale!!! set scale to (1 1 1)')
            error_scale_module=True
    #model_list.append(mdl_name[0])
    #model=model_list[j]+'.wrl'
    model=mdl_name[0]+'.wrl'
    # if show_debug:
    #     sayerr(model_list)
    #     #stop
    if (virtual==1 and addVirtual==0):
        model_name='no3Dmodel'
        side='noLayer'
        if model:
            sayw("virtual model "+model+" skipped") #virtual found warning
    else:
        if model:
            # say (model.group(0))
            #model_name=model.group(0)[6:]
            #model_name=model[6:]
            model_name=model
            #sayw(model_name)
            if "box_mcad" not in model_name and "cylV_mcad" not in model_name and "cylH_mcad" not in model_name:
                if error_scale_module:
                    sayw('wrong scale!!! for '+model_name+' Set scale to (1 1 1)')
                    msg="""<b>Error in '.kicad_pcb' model footprint</b><br>"""
                    msg+="<br>reset values of<br><b>"+model_name+"</b><br> to:<br>"
                    msg+="(scale (xyz 1 1 1))<br>"
                    warn+=("reset values of scale to (xyz 1 1 1)")
                    ##reply = QtGui.QMessageBox.information(None,"info", msg)
                    #stop
            #model_name=model_name[1:]
            #say(model_name)
            #sayw("here")
        else:
            model_name='no3Dmodel'
            side='noLayer'
            #sayerr('no3Dmodel')
    return model_name, rot_comb, warn, pos_vrml, rotz_vrml, scale_vrml
###

def getPCBThickness(Board):
    #say(len(Kicad_Board))
    return float(re.findall(r'\(thickness (.+?)\)', Board)[0])

def getPCBVersion(Board):
    return int(re.findall(r'\(kicad_pcb \(version (.+?)\)', Board)[0])

def getPCBArea(Kicad_Board):
    area = (re.findall(r'\(area (.+?)\)', Kicad_Board)[0])
    # say(area)
    return area

def createSolidBBox(model3D):
    selEx=model3D
    selEx = FreeCADGui.Selection.getSelectionEx()
    objs = [selobj.Object for selobj in selEx]
    if len(objs) == 1:
        s = objs[0].Shape
        name=objs[0].Label
        FreeCAD.Console.PrintMessage(name+" name \r\n")
        # boundBox
        boundBox_ = s.BoundBox
        boundBoxLX = boundBox_.XLength
        boundBoxLY = boundBox_.YLength
        boundBoxLZ = boundBox_.ZLength
        a = str(boundBox_)
        a,b = a.split('(')
        c = b.split(',')
        oripl_X = float(c[0])
        oripl_Y = float(c[1])
        oripl_Z = float(c[2])
        #say(str(boundBox_))
        #say("Rectangle : "+str(boundBox_.XLength)+" x "+str(boundBox_.YLength)+" x "+str(boundBox_.ZLength))
        #say("_____________________")
        #say("x: "+str(oripl_X)+" y: "+str(oripl_Y)+"z: "+str(oripl_Z))
        obj=FreeCAD.ActiveDocument.addObject('Part::Feature',name)
        obj.Shape=Part.makeBox(boundBox_.XLength, boundBox_.YLength, boundBox_.ZLength, FreeCAD.Vector(oripl_X,oripl_Y,oripl_Z), FreeCAD.Vector(0,0,1))
        # Part.show(cube)
        #say("cube name "+ obj.Name)
    else:
        FreeCAD.Console.PrintMessage("Select a single part object !"+"\r\n")
    #end bbox macro
    name=obj.Name
    #say("bbox name "+name)
    return name
    del objs
### end createSolidBBox  

def findPcbCenter(pcbName):
    pcb = FreeCAD.ActiveDocument.getObject(pcbName)
    s=pcb.Shape
    name=pcb.Label
    # boundBox
    boundBox_ = s.BoundBox
    boundBoxLX = boundBox_.XLength
    boundBoxLY = boundBox_.YLength
    boundBoxLZ = boundBox_.ZLength
    center = s.BoundBox.Center
    #say(center)
    #say("["+str(center.x)+"],["+str(center.y)+"] center of pcb")
    a = str(boundBox_)
    a,b = a.split('(')
    c = b.split(',')
    oripl_X = float(c[0])
    oripl_Y = float(c[1])
    oripl_Z = float(c[2])
    #say(str(boundBox_))
    #say("Rectangle : "+str(boundBox_.XLength)+" x "+str(boundBox_.YLength)+" x "+str(boundBox_.ZLength))
    #say("_____________________")
    #say("x: "+str(oripl_X)+" y: "+str(oripl_Y)+"z: "+str(oripl_Z))
    center_x=center.x; center_y=center.y
    bb_x=boundBox_.XLength; bb_y=boundBox_.YLength
    return center_x, center_y, bb_x, bb_y
### end findPcbCenter

def getArc_minMax(xC,xA,yC,yA,alpha):
    # x1=xA start point; x2=xC center; xB end point; alpha=angle
    global xMax, xmin, yMax, ymin
    j=0
    R=sqrt((xA-xC)**2+(yA-yC)**2)
    #say('R = '+str(R))
    if (xA>=xC) and (yA<yC):
        beta=atan(abs(xA-xC)/abs(yA-yC))
        j=1; ABeta=(alpha+beta)
        #say(str(degrees(beta))+" beta "+ str(degrees(ABeta))+" ABeta")
        #cases if (xA>xC) and (yA<yC):
        if ABeta >= beta and ABeta <= pi/2:
            xB=R*sin(alpha+beta)+xC
            xMax=max(xB,xMax)
            xmin= min(xA,xmin)
            yB=yC-R*cos(alpha+beta)
            yMax= max(yB, yMax)
            ymin= min(yA, ymin)
        if ABeta >pi/2 and ABeta <=pi:
            xMax = max(R+xC,xMax)
            xB=R*sin(alpha+beta)+xC
            xmin = min(xA, xB, xmin)
            # yB = yC+R*cos(pi-(alpha+beta))
            yB=yC-R*cos(alpha+beta)
            yMax = max(yB, yMax)
            ymin = min(yA, ymin)
        if ABeta >pi and ABeta <=3/2*pi:
            xB=R*sin(alpha+beta)+xC
            xMax=max(R+xC,xMax)
            xmin = min(xB,xmin)
            yB=yC-R*cos(alpha+beta)
            yMax = max(yC+R, yMax)
            ymin = min(yA, ymin)
        if ABeta >3/2*pi and ABeta <= 2*pi:
            xB=R*sin(alpha+beta)+xC
            xMax=max(R+xC,xMax)
            xmin = min(xC-R,xmin)
            yB=yC-R*cos(alpha+beta)
            yMax = max(yC+R, yMax)
            ymin = min(yA, yB, ymin)
        if ABeta >2*pi and ABeta <= 2*pi+beta:
            xmin = min(xC-R,xmin)
            xMax = max(R+xC,xMax)
            ymin = min(yC-R, ymin)
            yMax = max(yC+R, yMax)
    if (xA>xC) and (yA>=yC):
        beta=atan(abs(yA-yC)/abs(xA-xC))
        j=2; ABeta=(alpha+beta)
        #say(str(degrees(beta))+" beta "+ str(degrees(ABeta))+" ABeta")
        yB=yC+R*sin(ABeta)
        xB=xC+R*cos(ABeta)
        if ABeta >= beta and ABeta <= pi/2:
            xMax=max(xA,xMax)
            xmin= min(xB,xmin)
            yMax= max(yB, yMax)
            ymin= min(yA, ymin)
        if ABeta > pi/2 and ABeta <= pi:
            xmin= min(xB,xmin)
            xMax=max(xA,xMax)
            ymin= min(yA, yB, ymin)
            yMax= max(yC+R, yMax)
        if ABeta > pi and ABeta <= 3/2*pi:
            xmin= min(xC-R,xmin)
            xMax=max(xA,xMax)
            ymin= min(yB, ymin)
            yMax= max(yC+R, yMax)
        if ABeta > 3/2*pi and ABeta <= 2*pi:
            xmin= min(xC-R,xmin)
            xMax= max(xA,xB,xMax)
            ymin= min(yC-R, ymin)
            yMax= max(yC+R, yMax)
        if ABeta > 2*pi and ABeta <= beta+2*pi:
            xmin= min(xC-R,xmin)
            xMax= max(xC+R,xMax)
            ymin= min(yC-R, ymin)
            yMax= max(yC+R, yMax)
    if (xA<=xC) and (yA>yC):
        beta=atan(abs(xA-xC)/abs(yA-yC))
        j=3; ABeta=(alpha+beta)
        #say(str(degrees(beta))+" beta "+ str(degrees(ABeta))+" ABeta")
        yB=yC+R*cos(ABeta)
        xB=xC-R*sin(ABeta)
        if ABeta >= beta and ABeta <= pi/2:
            xMax= max(xA,xMax)
            xmin= min(xB,xmin)
            yMax= max(yA, yMax)
            ymin= min(yB, ymin)
        if ABeta > pi/2 and ABeta <= pi:
            xmin= min(xC-R,xmin)
            xMax= max(xA,xB,xMax)
            ymin= min(yB,ymin)
            yMax= max(yA,yMax)
        if ABeta > pi and ABeta <= 3/2*pi:
            xmin= min(xC-R,xmin)
            xMax= max(xB,xMax)
            ymin= min(yC-R, ymin)
            yMax= max(yA, yMax)
        if ABeta > 3/2*pi and ABeta <= 2*pi:
            xmin= min(xC-R,xmin)
            xMax= max(xC+R,xMax)
            ymin= min(yC-R, ymin)
            yMax= max(yA,yB, yMax)
        if ABeta > 2*pi and ABeta <= beta+2*pi:
            xmin= min(xC-R,xmin)
            xMax= max(xC+R,xMax)
            ymin= min(yC-R, ymin)
            yMax= max(yC+R, yMax)
    if (xA<xC) and (yA<=yC):
        beta=atan(abs(yA-yC)/abs(xA-xC))
        j=4; ABeta=(alpha+beta)
        #say(str(degrees(beta))+" beta "+ str(degrees(ABeta))+" ABeta")
        yB=yC-R*sin(ABeta)
        xB=xC-R*cos(ABeta)
        if ABeta >= beta and ABeta <= pi/2:
            xMax= max(xB,xMax)
            xmin= min(xA,xmin)
            yMax= max(yA, yMax)
            ymin= min(yB, ymin)
        if ABeta > pi/2 and ABeta <= pi:
            xmin= min(xA,xmin)
            xMax= max(xB,xMax)
            ymin= min(yC-R,ymin)
            yMax= max(yA,yB,yMax)
        if ABeta > pi and ABeta <= 3/2*pi:
            xmin= min(xA,xmin)
            xMax= max(xC+R,xMax)
            ymin= min(yC-R, ymin)
            yMax= max(yB, yMax)
        if ABeta > 3/2*pi and ABeta <= 2*pi:
            xmin= min(xA,xB,xmin)
            xMax= max(xC+R,xMax)
            ymin= min(yC-R,ymin)
            yMax= max(yC+R, yMax)
        if ABeta > 2*pi and ABeta <= beta+2*pi:
            xmin= min(xC-R,xmin)
            xMax= max(xC+R,xMax)
            ymin= min(yC-R, ymin)
            yMax= max(yC+R, yMax)
    #say(str(j)+" case j")
    #say('xC='+str(xC)+';yC='+str(yC)+';xA='+str(xA)+';yA='+str(yA))
    #print x1,x2,y1,y2
    #calculating xmin of arc
    R=sqrt((xA-xC)**2+(yA-yC)**2)
    #say('R = '+str(R))
    #say(str(xMax)+" xMax")
    #say(str(xmin)+" xmin")
    # print xMax, xmin, yMax, ymin
    # print pcbarcs[n]
    #print (pcbarcs[n][8:].split(' ')[0])
    return 0
### end getArc_minMax

def mid_point(prev_vertex,vertex,angle):
    """mid_point(prev_vertex,vertex,angle)-> mid_vertex
       returns mid point on arc of angle between prev_vertex and vertex"""
    angle=radians(angle/2)
    basic_angle=atan2(vertex.y-prev_vertex.y,vertex.x-prev_vertex.x)-pi/2
    shift=(1-cos(angle))*hypot(vertex.y-prev_vertex.y,vertex.x-prev_vertex.x)/2/sin(angle)
    midpoint=Base.Vector((vertex.x+prev_vertex.x)/2+shift*cos(basic_angle),(vertex.y+prev_vertex.y)/2+shift*sin(basic_angle),0)
    return midpoint
###

def Per_point(prev_vertex,vertex):
    """Per_point(center,vertex)->per point

       returns opposite perimeter point of circle"""
    #basic_angle=atan2(prev_vertex.y-vertex.y,prev_vertex.x-vertex.x)
    #shift=hypot(prev_vertex.y-vertex.y,prev_vertex.x-vertex.x)
    #perpoint=Base.Vector(prev_vertex.x+shift*cos(basic_angle),prev_vertex.y+shift*sin(basic_angle),0)
    perpoint=Base.Vector(2*prev_vertex.x-vertex.x,2*prev_vertex.y-vertex.y,0)
    return perpoint
###    

#os.system("ps -C 'kicad-SteUp-tool' -o pid=|xargs kill -9")

# UI Class definitions
##if _platform == "linux" or _platform == "linux2":
##   # linux
##elif _platform == "darwin":
##   # MAC OS X
##elif _platform == "win32":
##   # Windows

#####################################
# Function infoDialog 
#####################################
def infoDialog(msg):
    #QtGui.qFreeCAD.setOverrideCursor(QtCore.Qt.WaitCursor)
    QtGui.qFreeCAD.restoreOverrideCursor()
    QtGui.QApplication.restoreOverrideCursor()
    diag = QtGui.QMessageBox(QtGui.QMessageBox.Information,u"Info Message",msg )
    diag.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
    diag.exec_()
    QtGui.qFreeCAD.restoreOverrideCursor()


##  getAuxAxisOrigin
def getAuxAxisOrigin():
    match = re.search(r'\(aux_axis_origin (.+?) (.+?)\)', Kicad_Board)
    return [float(match.group(1)), float(match.group(2))];


#####################################
# Main Class old
#####################################
# Class definitions

# Function definitions
def onLoadFootprint(file_name=None):
    #name=QtGui.QFileDialog.getOpenFileName(this,tr("Open Image"), "/home/jana", tr("Image Files (*.png *.jpg *.bmp)"))[0]
    #global module_3D_dir
    global last_fp_path, test_flag, pt_lnx
    global configParser, configFilePath, start_time
    global ignore_utf8, ignore_utf8_incfg, disable_PoM_Observer
    #self.setGeometry(25, 250, 500, 500)
    clear_console()
    default_value='/'
    module_3D_dir=os.getenv('KISYS3DMOD', default_value)
    module_3D_dir=module_3D_dir+'/../'
    ## getting 3D models path
    # say('KISYS3DMOD=')
    say('KISYS3DMOD='+os.getenv('KISYS3DMOD', default_value)+'\n'+'module_3D_dir='+module_3D_dir)
    if not os.path.isdir(module_3D_dir):
        module_3D_dir="/"
    if last_fp_path=='':
        last_fp_path=module_3D_dir
    if file_name is not None:
        #export_board_2step=True #for cmd line force exporting to STEP
        name=file_name
    elif test_flag==False:
    #if test_flag==False:
        Filter=""
        ##if _platform == "darwin":
        ##    ##workaround for OSX not opening native fileopen
        ##    name=QtGui.QFileDialog.getOpenFileName(self, 'Open file',
        ##         last_file_path,"kicad module files (*.kicad_mod)",
        ##         options=QtGui.QFileDialog.DontUseNativeDialog )[0]
        ##else:
        ##    name=QtGui.QFileDialog.getOpenFileName(self, "Open File...", last_file_path,
        ##        "kicad module files (*.kicad_mod)")[0]
        #path = FreeCAD.ConfigGet("AppHomePath")
        #path = FreeCAD.ConfigGet("UserAppData")
        #path=last_file_path
        #try:
        #    name, Filter = PySide.QtGui.QFileDialog.getOpenFileName(None, "Open File", last_file_path, "*.kicad_mod")#PySide
        #except Exception:
        #    FreeCAD.Console.PrintError("Error : " + str(name) + "\n")
        name, Filter = PySide.QtGui.QFileDialog.getOpenFileName(None, "Open File...",
             make_unicode(last_fp_path), "*.kicad_mod")
    else:
        name="C:/Cad/Progetti_K/ksu-test/test.kicad_mod"
    if len(name) > 0:
        #txtFile = __builtin__.open(name,"r")
        #with io.open(name,'r', encoding='utf-8') as txtFile:
        with codecs.open(name,'r', encoding='utf-8') as txtFile:
            #text = f.read()
            content = txtFile.readlines() # problems?

        ## txtFile = __builtin__.open(name,"rb")
        ## content = txtFile.readlines()
        content.append(u" ")
        last_fp_path=os.path.dirname(txtFile.name)
        txtFile.close()
        last_fp_path = re.sub("\\\\", "/", last_fp_path)
            #stop        
        ini_vars[11] = last_fp_path
        ##with __builtin__.open(configFilePath, 'wb') as configfile:
        #    configParser.write(configfile)
        #cfg_update_all()
        pg = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/kicadStepUp")
        pg.SetString("last_fp_path", make_string(last_fp_path))
        data=u''.join(content)
        #for item in content:
        #    data += item
        #print content; print data;stop
        if ignore_utf8:
            content=re.sub(r'[^\x00-\x7F]+',' ', data)  #workaround to remove utf8 extra chars
            sayw('removing utf-8 chars')
        else:
            content=data
        #print content; stop
        
        #content=data
        #FreeCAD.Console.PrintMessage(content)
        #FreeCAD.Console.PrintMessage(data)
        FC_majorV=int(float(FreeCAD.Version()[0]))
        FC_minorV=int(float(FreeCAD.Version()[1]))
        say('FC Version '+str(FC_majorV)+str(FC_minorV))    
        if int(FC_majorV) <= 0 and int(FC_minorV) < 16:
            routineDrawFootPrint_old(content,name)
        else:
            if disable_VBO:
                paramGetV = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/View")
                VBO_status=paramGetV.GetBool("UseVBO")
                #sayerr("checking VBO")
                say("VBO status "+str(VBO_status))
                if VBO_status:
                    paramGetV.SetBool("UseVBO",False)
                    sayw("disabling VBO")
            if disable_PoM_Observer:
                #paramGetPoM = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/PartOMagic")
                #PoMObs_status=paramGetPoM.GetBool("EnableObserver")
                PoMObs_status = False
                if Observer.isRunning():
                    PoMObs_status=True
                #if PoMObs_status:
                    Observer.stop()
        #        paramGetPoM.SetBool("EnableObserver",False)
                    sayw("disabling PoM Observer")
            routineDrawFootPrint(content,name)
            if (not pt_lnx): # and (not pt_osx): issue on AppImages hanging on loading 
                FreeCADGui.SendMsgToActiveView("ViewFit")
            else:
                zf= Timer (0.3,ZoomFitThread)
                zf.start()
            #zf= Timer (0.3,ZoomFitThread)
            #zf.start()
            if disable_VBO:
                if VBO_status:
                    paramGetV.SetBool("UseVBO",True)
                    sayw("enabling VBO")
            if disable_PoM_Observer:
                if PoMObs_status:
                    Observer.start()
        #        paramGetPoM.SetBool("EnableObserver",True)
                    sayw("enabling PoM Observer")
        #txtFile.close()
###

def check_requirements():
    # checking FC version requirement
    ######################################################################
    #say("FC Version ")
    #say(FreeCAD.Version())
    global start_time, fusion, FC_export_min_version, use_AppPart, force_oldGroups, use_Links, use_LinkGroups
    FC_majorV,FC_minorV,FC_git_Nbr=getFCversion()
    #FC_majorV=FreeCAD.Version()[0]
    #FC_minorV=FreeCAD.Version()[1]
    ##FC_majorV=int(FreeCAD.Version()[0])
    ##FC_minorV=int(FreeCAD.Version()[1])
    #try:
    #    FC_git_Nbr=int(FreeCAD.Version()[2].strip(" (Git)"))
    #except:
    #    FC_git_Nbr=0
    #FC_git_Nbr=(FreeCAD.Version()[2].strip(" (Git)"))
    sayw('FC Version '+str(FC_majorV)+str(FC_minorV)+"-"+str(FC_git_Nbr))   
    msg1="use ONLY FreeCAD STABLE version 0.15 or later\r\n"
    #msg1+="to generate your STEP and VRML models\r\nFC 016 dev version results are still unpredictable"
    msg1+="to generate your STEP and VRML models\r\n"
    if int(FC_majorV) <= 0:
        if int(FC_minorV) < 15:
            QtGui.QApplication.restoreOverrideCursor()
            reply = QtGui.QMessageBox.information(None,"Warning! ...",msg1)    
    msg=''
    if FC_majorV == 0 and FC_minorV == 17:
        if FC_git_Nbr >= int(FC_export_min_version):
            use_AppPart=True
    if FC_majorV > 0:
        use_AppPart=True
    if FC_majorV == 0 and FC_minorV > 17:
        if FC_git_Nbr >= int(FC_export_min_version):
            use_AppPart=True
    if use_AppPart and not force_oldGroups:
        sayw("creating hierarchy")
    if (fusion==True):
        msg+="you have chosen: fuse modules to board\r\nbe careful ... fusion can be heavy or generate FC crash"
        msg+="when fusing a lot of objects\r\nplease consider to use bbox or blacklist small objects\r\n\r\n"    
    ##start_time=current_milli_time()
###
def sanitizeSketch(s_name):
    ''' simplifying & sanitizing sketches '''
    global edge_tolerance
    
    s=FreeCAD.ActiveDocument.getObject(s_name)
    sayw('check to sanitize')
    if 'Sketcher' in s.TypeId:
        idx_to_del=[]
        for i,g in enumerate (s.Geometry):
            #print(g,i)
            if 'Line' in str(g):
                #print(g.length())
                if g.length() <= edge_tolerance:
                    print(g,i,'too short')
                    idx_to_del.append(i)
            elif 'Circle' in str(g):
                if g.Radius <= edge_tolerance:
                    print(g,i,'too short')
                    idx_to_del.append(i)
        j=0
        if len(idx_to_del) >0:
            print(u'sanitizing '+s.Label)
        for i in idx_to_del:
            s.delGeometry(i-j)
            j+=1
##
def add_constraints(s_name):
    """ adding coincident points constraints """
    global addConstraints, edge_tolerance
    
    s=FreeCAD.ActiveDocument.getObject(s_name)
    
    if hasattr(Part,"LineSegment"):
        g_geom_points = {
            Base.Vector: [1],
            Part.LineSegment: [1, 2],  # first point, last point
            Part.Circle: [0, 3],  # curve, center
            Part.ArcOfCircle: [1, 2, 3],  # first point, last point, center
            Part.BSplineCurve: [0,1,2,3], # for poles
            Part.ArcOfEllipse: [0,1,2,3], #
            Part.Ellipse: [0,1], #
            Part.ArcOfHyperbola: [0,1,2], #
            Part.Point: [0], #            
        }
    else:
        g_geom_points = {
            Base.Vector: [1],
            Part.Line: [1, 2],  # first point, last point
            Part.Circle: [0, 3],  # curve, center
            Part.ArcOfCircle: [1, 2, 3],  # first point, last point, center
            Part.BSplineCurve: [0,1,2,3], # for poles
            Part.ArcOfEllipse: [0,1,2,3], #
            Part.Ellipse: [0,1], #
            Part.ArcOfHyperbola: [0,1,2], #
            Part.Point: [0], #            
        }
    points=[]
    geoms=[]
    #print len((s.Geometry))
    #stop
    for geom_index in range(len((s.Geometry))):
        point_indexes = g_geom_points[type(s.Geometry[geom_index])]
        #sayerr(point_indexes), say (geom_index)
        #if 'Line' in type(PCB_Sketch.Geometry[geom_index]).__name__:
        
        if 'ArcOfCircle' in type(s.Geometry[geom_index]).__name__\
         or 'Line' in type(s.Geometry[geom_index]).__name__:
            point1 = s.getPoint(geom_index, point_indexes[0])
            #sayerr(str(point1[0])+';'+str(point1[1]))
            point2 = s.getPoint(geom_index, point_indexes[1])
            #sayw(str(point2[0])+';'+str(point1[1]))
            #points.append([[point1[0],point1[1]],[geom_index],[1]])
            #points.append([[point2[0],point2[1]],[geom_index],[2]])
            #points.append([[point1[0],point1[1]],[geom_index]]) #,[1]])
            #points.append([[point2[0],point2[1]],[geom_index]]) #,[2]])
            if 'Line' in type(s.Geometry[geom_index]).__name__:
                tp = 'Line'
            else:
                tp = 'Arc'
            geoms.append([point1[0],point1[1],point2[0],point2[1],tp])
        elif 'ArcOfEllipse' in type(s.Geometry[geom_index]).__name__:
            point1 = s.getPoint(geom_index, point_indexes[1])
            point2 = s.getPoint(geom_index, point_indexes[2])
            tp = 'Arc'
            geoms.append([point1[0],point1[1],point2[0],point2[1],tp])

    #print points
    def simu_distance(p0, p1):
        return max (abs(p0[0] - p1[0]), abs(p0[1] - p1[1]))
    #
    #print geom
    sk_constraints = []
    cnt=1
    #print (addConstraints, ' constraints')
    #stop
    if addConstraints=='all':
        for i, geo in enumerate(geoms):
        #for i in range(len(geom)):
            p_g0_0=[geo[0],geo[1]]
            p_g0_1=[geo[2],geo[3]]
            #print p_g0_0,pg_g0_1
            if abs(p_g0_0[0]-p_g0_1[0])< edge_tolerance and geo[4] == 'Line':
                #s.addConstraint(Sketcher.Constraint('Vertical',i))
                sk_constraints.append(Sketcher.Constraint('Vertical',i))
            elif abs(p_g0_0[1]-p_g0_1[1])< edge_tolerance and geo[4] == 'Line':
                #s.addConstraint(Sketcher.Constraint('Horizontal',i))
                sk_constraints.append(Sketcher.Constraint('Horizontal',i))
            j=i+1
            for geo2 in geoms[(i + 1):]:
                p_g1_0=[geo2[0],geo2[1]]
                p_g1_1=[geo2[2],geo2[3]]
                #rint p_g0_0, p_g0_1
                #rint p_g1_0, p_g1_1
                if distance(p_g0_0,p_g1_0)< edge_tolerance:
                ##App.ActiveDocument.PCB_Sketch.addConstraint(Sketcher.Constraint('Coincident',0,2,3,1)) 
                    #s.addConstraint(Sketcher.Constraint('Coincident',i,1,j,1))
                    sk_constraints.append(Sketcher.Constraint('Coincident',i,1,j,1))
                    #print i,1,i+1,1
                elif distance(p_g0_0,p_g1_1)< edge_tolerance:
                    #s.addConstraint(Sketcher.Constraint('Coincident',i,1,j,2))
                    sk_constraints.append(Sketcher.Constraint('Coincident',i,1,j,2))
                    #print i,1,i+1,2
                elif distance(p_g0_1,p_g1_0)< edge_tolerance:
                    #s.addConstraint(Sketcher.Constraint('Coincident',i,2,j,1))
                    sk_constraints.append(Sketcher.Constraint('Coincident',i,2,j,1))
                    #print i,2,i+1,1
                elif distance(p_g0_1,p_g1_1)< edge_tolerance:
                    #s.addConstraint(Sketcher.Constraint('Coincident',i,2,j,2))
                    sk_constraints.append(Sketcher.Constraint('Coincident',i,2,j,2))                   
                    #print i,2,i+1,2
                j=j+1
                cnt=cnt+1
    elif addConstraints=='coincident' or addConstraints=='full':
        if hasattr (FreeCAD.ActiveDocument.getObject(s_name), "autoconstraint"):
            sayw('using constrainator')
            sanitizeSketch(s_name)
            sk1=FreeCAD.ActiveDocument.getObject(s_name)
            sk1.detectMissingPointOnPointConstraints(edge_tolerance)
            sk1.makeMissingPointOnPointCoincident()
            FreeCAD.activeDocument().recompute()
            sk1.autoRemoveRedundants(True)
            sk1.solve()
            FreeCAD.activeDocument().recompute()
        else:
            sayw('using old constrainator')
            for i, geo in enumerate(geoms):
            #for i in range(len(geom)):
                #print (geo)
                #stop
                p_g0_0=[geo[0],geo[1]]
                p_g0_1=[geo[2],geo[3]]
                #print p_g0_0,pg_g0_1
                #if addConstraints=='all':
                #    if abs(p_g0_0[0]-p_g0_1[0])< edge_tolerance:
                #        s.addConstraint(Sketcher.Constraint('Vertical',i))
                #    elif abs(p_g0_0[1]-p_g0_1[1])< edge_tolerance:
                #        s.addConstraint(Sketcher.Constraint('Horizontal',i))
                j=i+1
                for geo2 in geoms[(i + 1):]:
                    p_g1_0=[geo2[0],geo2[1]]
                    p_g1_1=[geo2[2],geo2[3]]
                    #rint p_g0_0, p_g0_1
                    #rint p_g1_0, p_g1_1
                    if distance(p_g0_0,p_g1_0)< edge_tolerance:
                    ##App.ActiveDocument.PCB_Sketch.addConstraint(Sketcher.Constraint('Coincident',0,2,3,1)) 
                        #s.addConstraint(Sketcher.Constraint('Coincident',i,1,j,1))
                        sk_constraints.append(Sketcher.Constraint('Coincident',i,1,j,1))
                        #print i,1,i+1,1
                    elif distance(p_g0_0,p_g1_1)< edge_tolerance:
                        #s.addConstraint(Sketcher.Constraint('Coincident',i,1,j,2))
                        sk_constraints.append(Sketcher.Constraint('Coincident',i,1,j,2))
                        #print i,1,i+1,2
                    elif distance(p_g0_1,p_g1_0)< edge_tolerance:
                        #s.addConstraint(Sketcher.Constraint('Coincident',i,2,j,1))
                        sk_constraints.append(Sketcher.Constraint('Coincident',i,2,j,1))                    
                        #print i,2,i+1,1
                    elif distance(p_g0_1,p_g1_1)< edge_tolerance:
                        #s.addConstraint(Sketcher.Constraint('Coincident',i,2,j,2))
                        sk_constraints.append(Sketcher.Constraint('Coincident',i,2,j,2))
                        #print i,2,i+1,2
                    j=j+1
                    cnt=cnt+1
    if len(sk_constraints) > 0:
        s.addConstraint(sk_constraints)
        #print 'counter ',cnt
            #print geo2
            
###        
def add_missing_geo(s_name):
    """ adding missing geo on near but non coincident points"""
    
    s=FreeCAD.ActiveDocument.getObject(s_name)
    
    if hasattr(Part,"LineSegment"):
        g_geom_points = {
            Base.Vector: [1],
            Part.LineSegment: [1, 2],  # first point, last point
            Part.Circle: [0, 3],  # curve, center
            Part.ArcOfCircle: [1, 2, 3],  # first point, last point, center
            Part.BSplineCurve: [0,1,2,3], # for poles
            Part.ArcOfEllipse: [0,1,2,3], # 
            Part.Ellipse: [0,1], #
            Part.ArcOfHyperbola: [0,1,2], #
            Part.Point: [0], #
        }
    else:
        g_geom_points = {
            Base.Vector: [1],
            Part.Line: [1, 2],  # first point, last point
            Part.Circle: [0, 3],  # curve, center
            Part.ArcOfCircle: [1, 2, 3],  # first point, last point, center
            Part.BSplineCurve: [0,1,2,3], # for poles
            Part.ArcOfEllipse: [0,1,2,3], # 
            Part.Ellipse: [0,1], #
            Part.ArcOfHyperbola: [0,1,2], #
            Part.Point: [0], #
        }
    geo_points=[]
    geoms=[]
    #print len((s.Geometry))
    #stop
    for geom_index in range(len((s.Geometry))):
        point_indexes = g_geom_points[type(s.Geometry[geom_index])]
        #sayerr(point_indexes), say (geom_index)
        #if 'Line' in type(PCB_Sketch.Geometry[geom_index]).__name__:
        if 'ArcOfCircle' in type(s.Geometry[geom_index]).__name__\
         or 'Line' in type(s.Geometry[geom_index]).__name__:
            point1 = s.getPoint(geom_index, point_indexes[0])
            #sayerr(str(point1[0])+';'+str(point1[1]))
            point2 = s.getPoint(geom_index, point_indexes[1])
            #sayw(str(point2[0])+';'+str(point1[1]))
            #points.append([[point1[0],point1[1]],[geom_index],[1]])
            #points.append([[point2[0],point2[1]],[geom_index],[2]])
            #points.append([[point1[0],point1[1]],[geom_index]]) #,[1]])
            #points.append([[point2[0],point2[1]],[geom_index]]) #,[2]])
            #points.append([[point1[0],point1[1]],[geom_index]]) #,[1]])
            #geo_points.append([[point1[0],point1[1]],[point2[0],point2[1]],[geom_index]]) #,[2]])
            geoms.append([point1[0],point1[1],point2[0],point2[1]])
        # elif 'ArcOfEllipse' in type(s.Geometry[geom_index]).__name__\
        #  or 'ArcOfHyperbola' in type(s.Geometry[geom_index]).__name__:
        #     point1 = s.getPoint(geom_index, point_indexes[1])
        #     point2 = s.getPoint(geom_index, point_indexes[2])
        #     geoms.append([point1[0],point1[1],point2[0],point2[1],tp])
        # elif 'Ellipse' in type(s.Geometry[geom_index]).__name__:
        #     pass
        # elif 'Point' in type(s.Geometry[geom_index]).__name__:
        #     pass
    sk_add_geo = []
    #say(geoms)
    for i, geo in enumerate(geoms):
        p_g0_0=[geo[0],geo[1]]
        p_g0_1=[geo[2],geo[3]]
        j=i+1
        for geo2 in geoms[(i + 1):]:
            p_g2_0_0=[geo2[0],geo2[1]]
            p_g2_0_1=[geo2[2],geo2[3]]
            d = distance(p_g0_0,p_g2_0_0)
            if d < edge_tolerance and d > 0:
                sk_add_geo.append(PLine(Base.Vector(p_g0_0[0],p_g0_0[1],0), Base.Vector(p_g2_0_0[0],p_g2_0_0[1],0)))
                #print i,1,i+1,1
            d = distance(p_g0_1,p_g2_0_0)
            if d < edge_tolerance and d>0:
                #s.addConstraint(Sketcher.Constraint('Coincident',i,1,j,2))
                sk_add_geo.append(PLine(Base.Vector(p_g0_1[0],p_g0_1[1],0), Base.Vector(p_g2_0_0[0],p_g2_0_0[1],0)))
                #print i,1,i+1,2
            d = distance(p_g0_0,p_g2_0_1)
            if d < edge_tolerance and d>0:
                #s.addConstraint(Sketcher.Constraint('Coincident',i,2,j,1))
                sk_add_geo.append(PLine(Base.Vector(p_g0_0[0],p_g0_0[1],0), Base.Vector(p_g2_0_1[0],p_g2_0_1[1],0)))
                #print i,2,i+1,1
            d = distance(p_g0_1,p_g2_0_1)
            if d < edge_tolerance and d >0:
                #s.addConstraint(Sketcher.Constraint('Coincident',i,2,j,2))
                sk_add_geo.append(PLine(Base.Vector(p_g0_1[0],p_g0_1[1],0), Base.Vector(p_g2_0_1[0],p_g2_0_1[1],0)))
                #print i,2,i+1,2
            j=j+1    
    sayerr('added Geometry')
    sayerr(sk_add_geo)
    if len(sk_add_geo) > 0:
        s.addGeometry(sk_add_geo)
            
###        

def cpy_sketch(sname,nname=None):
    """ copy Sketch NB Geometry sequence is not conserved!!! """
    
    s=FreeCAD.ActiveDocument.getObject(sname)
    #geoL=len(App.ActiveDocument.getObject(sname).Geometry)
    if nname is None:
        nname="Temp_Sketch"
    tsk= FreeCAD.activeDocument().addObject('Sketcher::SketchObject',nname)
    tsk.addGeometry(FreeCAD.ActiveDocument.getObject(sname).Geometry)
    tsk.addConstraint(FreeCAD.ActiveDocument.getObject(sname).Constraints)
    tsk.Placement=FreeCAD.ActiveDocument.getObject(sname).Placement
    #print tsk.Geometry
    FreeCAD.ActiveDocument.recompute()
    #stop
    return FreeCAD.ActiveDocument.ActiveObject.Name
## 

def shift_sketch(sname, ofs, nname):
    """ shift Sketch Geometry (Geom sequence is not conserved!!!) """
    
    s1n=cpy_sketch(sname,nname)
    FreeCAD.ActiveDocument.recompute()
    s1=FreeCAD.ActiveDocument.getObject(s1n)
    lg=len (s1.Geometry)
    #print lg
    geo=[]
    for k in range(lg):
        geo.append(str(FreeCAD.ActiveDocument.getObject(s1.Name).Geometry[k]))
    #geo=FreeCAD.ActiveDocument.getObject(s1.Name).Geometry
    for k in range(lg):
        FreeCAD.ActiveDocument.getObject(s1.Name).addCopy([k],FreeCAD.Vector(ofs[0],-ofs[1],0),False)
        #print FreeCAD.ActiveDocument.getObject(s1.Name).Geometry[k]
        #FreeCAD.ActiveDocument.getObject(s1.Name).delGeometry(k)
    FreeCAD.ActiveDocument.recompute()
    #print len (s1.Geometry)
    #stop
    #print (s1.Geometry) 
    nlg=len (s1.Geometry)
    idx_to_del=[]
    idx_to_del_str=[]
    #print geo
    for k in range(nlg):
        if str(FreeCAD.ActiveDocument.getObject(s1.Name).Geometry[k]) in geo:
            idx_to_del.append(k)
    #for j in range (len(idx_to_del)):
    #    idx_to_del_str.append(str(idx_to_del[j]))
    #print idx_to_del
    #stop
    #print idx_to_del_str
    for i in range (nlg-1,-1,-1):
    #    #FreeCAD.ActiveDocument.getObject(s_name).delGeometry(k)
        #print i
        if i in idx_to_del:
            FreeCAD.ActiveDocument.getObject(s1.Name).delGeometry(i)
    FreeCAD.ActiveDocument.recompute()
    #FreeCAD.ActiveDocument.getObject(s1.Name).Placement = FreeCAD.Placement(FreeCAD.Vector(2*ofs[0],2*ofs[1],0),FreeCAD.Rotation(FreeCAD.Vector(0,0,1),0))
        
    #geoL=len(App.ActiveDocument.getObject(sname).Geometry)
    #Temp_Sketch_Sft= FreeCAD.activeDocument().addObject('Sketcher::SketchObject','Temp_Sketch_Sft')
    #geo=[]
    #for k in range(len (s.Geometry)):
    #    App.ActiveDocument.Temp_Sketch_Sft.addCopy([k],App.Vector(100,100,0),False)
    #    
    #    #if 'LineSegment' in type(s.Geometry[k]).__name__:
    #    ##if 'Line' in type(s.Geometry[k]).__name__:
    #    #    #ls='<Line segment ({0},{1}) ({2},{3}) >'.format(s.Geometry[k].StartPoint.x+ofs[0],s.Geometry[k].StartPoint.y+ofs[1], s.Geometry[k].EndPoint.x+ofs[0],s.Geometry[k].EndPoint.y+ofs[1])
    #    #    #geo.append(ls);geo.append(le)
    #    #    #Temp_Sketch_Sft.addGeometry(FreeCAD.ActiveDocument.getObject(sname).Geometry[k])
    #    #    #Temp_Sketch_Sft.addGeometry(geo)
    #    #    spx=s.Geometry[k].StartPoint.x+ofs[0]
    #    #    spy=s.Geometry[k].StartPoint.y+ofs[1]
    #    #    epx=s.Geometry[k].EndPoint.x+ofs[0]
    #    #    epy=s.Geometry[k].EndPoint.y+ofs[1]
    #    #    
    #    #    FreeCAD.ActiveDocument.Temp_Sketch_Sft.addGeometry(PLine(Base.Vector(spx,spy,0), Base.Vector(epx,epy,0)))
    #        
    #Temp_Sketch_Sft.Placement.Base[0]=FreeCAD.ActiveDocument.getObject(sname).Placement.Base[0]+ofs[0]
    #Temp_Sketch_Sft.Placement.Base[1]=FreeCAD.ActiveDocument.getObject(sname).Placement.Base[1]+ofs[1]
    
    #print Temp_Sketch.Geometry
    #FreeCAD.ActiveDocument.recompute()
    return FreeCAD.ActiveDocument.ActiveObject.Name
## 
def PullPCB(file_name=None):
    onLoadBoard(None,False)
   #layer_list = ['Edge.Cuts','Dwgs.User','Eco1.User','Eco2.User']
   #LayerSelectionDlg = QtGui.QDialog()
   #ui = Ui_LayerSelection()
   #ui.setupUi(LayerSelectionDlg)
   #ui.comboBoxLayerSel.addItems(layer_list)
   #ui.label.setText("Select the layer to pull into the Sketch\nDefault \'Edge.Cuts\'")
   #reply=LayerSelectionDlg.exec_()
   #if reply==1: # ok
   #    SketchLayer=str(ui.comboBoxLayerSel.currentText())
   #    print(SketchLayer)
   #else:
   #    print('Cancel')
##

def crc_gen(data):
    import binascii
    import re
    
    #data=u'Würfel'
    content=re.sub(r'[^\x00-\x7F]+','_', data)
    #make_unicode(hex(binascii.crc_hqx(content.encode('utf-8'), 0x0000))[2:])
    #hex(binascii.crc_hqx(content.encode('utf-8'), 0x0000))[2:].encode('utf-8')
    #print(data +u'_'+ hex(binascii.crc_hqx(content.encode('utf-8'), 0x0000))[2:])
    return u'_'+ make_unicode(hex(binascii.crc_hqx(content.encode('utf-8'), 0x0000))[2:])
##
def onLoadBoard(file_name=None,load_models=None,insert=None):
    #name=QtGui.QFileDialog.getOpenFileName(this,tr("Open Image"), "/home/jana", tr("Image Files (*.png *.jpg *.bmp)"))[0]
    #global module_3D_dir
    global test_flag, last_pcb_path, configParser, configFilePath, start_time
    global aux_orig, base_orig, base_point, idf_to_origin, off_x, off_y, export_board_2step
    global real_board_pos_x, real_board_pos_y, board_base_point_x, board_base_point_y
    global models3D_prefix, models3D_prefix2, models3D_prefix3, models3D_prefix4
    global blacklisted_model_elements, col, colr, colg, colb
    global bbox, volume_minimum, height_minimum, idf_to_origin, aux_orig
    global base_orig, base_point, bbox_all, bbox_list, whitelisted_model_elements
    global fusion, addVirtual, blacklisted_models, exportFusing, min_drill_size
    global last_fp_path, last_pcb_path, plcmnt, xp, yp, exportFusing
    global ignore_utf8, ignore_utf8_incfg, pcb_path, disable_VBO, use_AppPart, force_oldGroups, use_Links, use_LinkGroups
    global original_filename, edge_width, load_sketch, grid_orig, warning_nbr, running_time, addConstraints
    global conv_offs, zfit, fname_sfx, missingHeight

    import fcad_parser
    from fcad_parser import KicadPCB,SexpList
    import kicad_parser
    objs_toberemoved = []
    ImportMode_status=0

    pull_sketch = False
    override_pcb = None
    keep_pcb_sketch = None
    SketchLayer = 'Edge.Cuts' #None
    if load_models is None:
        load_models = True

    # This means we load board layer into a sketch
    if load_models == False:
        # layer_list = ['Edge.Cuts','Dwgs.User','Cmts.User','Eco1.User','Eco2.User','Margin']
        layer_list = ['Edge.Cuts','Dwgs.User','Cmts.User','Eco1.User','Eco2.User','Margin', 'F.FillZone', 'F.KeepOutZone', 'F.MaskZone','B.FillZone', 'B.KeepOutZone', 'B.MaskZone',]
        LayerSelectionDlg = QtGui.QDialog()
        ui = Ui_LayerSelection()
        ui.setupUi(LayerSelectionDlg)
        ui.comboBoxLayerSel.addItems(layer_list)
        ui.label.setText("Select the layer to pull into the Sketch\nDefault: \'Edge.Cuts\'")
        reply=LayerSelectionDlg.exec_()
        if reply==1: # ok
            SketchLayer=str(ui.comboBoxLayerSel.currentText())
            print(SketchLayer)
            if SketchLayer == 'Edge.Cuts':
                #override_pcb = ui.checkBox_replace.isChecked()
                if ui.radioBtn_replace_pcb.isChecked():
                    override_pcb = True
                elif ui.radioBtn_keep_sketch.isChecked(): #enabling keep sketch only if override is True 
                    override_pcb = True
                    keep_pcb_sketch = True
            pull_sketch = True
        else:
            print('Cancel')

    # If we either successfully selected a layer, 
    # or plan to read in the whole board...
    if pull_sketch or load_models:
        # Determine the target Filename
        default_value='/'
        clear_console()

        if not os.path.isdir(make_unicode(last_pcb_path)):
            last_pcb_path=u"./"

        if file_name is not None:
            #export_board_2step=True #for cmd line force exporting to STEP
            name=file_name
        elif test_flag==False:
            Filter=""
                    #minimize main window
                    #self.setWindowState(QtCore.Qt.WindowMinimized)
                    #infoDialog('ciao')
                    #reply = QtGui.QInputDialog.getText(None, "Hello","Enter your thoughts for the day:")
                    #if reply[1]:
                    #        # user clicked OK
                    #        replyText = reply[0]
                    #else:
                    #        # user clicked Cancel
                    #        replyText = reply[0] # which will be "" if they clicked Cancel
                    #restore main window
                    #self.setWindowState(QtCore.Qt.WindowActive)
            name, Filter = PySide.QtGui.QFileDialog.getOpenFileName(None, "Open kicad PCB File...",
                make_unicode(last_pcb_path), "*.kicad_pcb")
        else:
            name="C:/Cad/Progetti_K/ksu-test/multidrill.kicad_pcb"

        # Check if we have a Valid Filename
        if len(name) > 0:
            if os.path.isfile(name):
                original_filename=name
                say('opening '+name)

                # Generate Unique tag for layers for THIS board
                path, fname = os.path.split(name)
                fname=os.path.splitext(fname)[0]
                fname_sfx=crc_gen(make_unicode(fname))

                # Name each layer with unique tag
                top_name='Top'+fname_sfx
                bot_name='Bot'+fname_sfx
                topV_name='TopV'+fname_sfx
                botV_name='BotV'+fname_sfx
                stepM_name='Step_Models'+fname_sfx
                stepV_name='Step_Virtual_Models'+fname_sfx
                pcb_name='Pcb'+fname_sfx
                sketch_name_sfx = 'PCB_Sketch'+fname_sfx
                board_name='Board'+fname_sfx
                boardG_name='Board_Geoms'+fname_sfx
                LCS_name = 'Local_CS'+fname_sfx

                #say(fname_sfx)
                #fpth = os.path.dirname(os.path.abspath(__file__))
                fpth = os.path.dirname(os.path.abspath(name))
                #filePath = os.path.split(os.path.realpath(__file__))[0]
                say ('my file path '+fpth)
                if fpth == "":
                    fpth = u"."
                last_pcb_path = fpth
                #last_pcb_path=path
                pcb_path=fpth
                # update existing value
                #say(default_ksu_msg)
                #stop
                last_pcb_path = re.sub("\\\\", "/", last_pcb_path)
                #    configParser.write(configfile)
                ##stop utf-8 test
                ini_vars[10] = last_pcb_path
                #cfg_update_all()

                # Create new FreeCAD document, or reuse current one
                test_import = False
                if override_pcb == True:
                    insert=True
                if insert == True:
                    test_import = True
                if test_import:
                    doc=FreeCAD.ActiveDocument
                    if doc is None:
                        doc=FreeCAD.newDocument(fname)
                        override_pcb = False
                        try:
                            doc.removeObject(LCS_name)
                        except:
                            pass
                    elif override_pcb == True:
                        if doc.getObject(boardG_name) in doc.Objects: #if 1: #try:
                            if keep_pcb_sketch==True:
                                #doc.getObject(boardG_name).removeObject(doc.getObject(sketch_name_sfx)) #keep sketck & constrains
                                doc.getObject(boardG_name).ViewObject.dragObject(doc.getObject(sketch_name_sfx))
                                #objs_toberemoved.append([doc.getObject(sketch_name_sfx)])
                            removesubtree([doc.getObject(boardG_name)])
                            #objs_toberemoved.append([doc.getObject(boardG_name)])
                            #doc.recompute()
                            try:
                                doc.removeObject(LCS_name)
                            except:
                                pass
                            sayw('old Pcb removed')
                            #stop
                        else: #except:
                            override_pcb = False
                            say('Pcb not present')
                else:
                    doc=FreeCAD.newDocument(fname)

                # Open the KiCAD PCB File
                doc.commitTransaction()
                doc.openTransaction('opening_kicad')
                say('opening Transaction \'opening_kicad\'')
                pg = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/kicadStepUp")
                pg.SetString("last_pcb_path", make_string(last_pcb_path)) # py3 .decode("utf-8")
                #pg.SetString("last_pcb_path", last_pcb_path.decode("utf-8"))
                modules=[]
                start_time=current_milli_time()
                #filename="C:/Cad/Progetti_K/D-can-term/can-term-test-fcad.kicad_pcb"
                #filename="c:\\Temp\\backpanel3.kicad_pcb"
                mypcb = KicadPCB.load(name) #test parser


                off_x=0; off_y=0  #offset of the board & modules
                grid_orig_warn=False
                if (grid_orig==1):
                    #xp=getAuxAxisOrigin()[0]; yp=-getAuxAxisOrigin()[1]  #offset of the board & modules
                    if hasattr(mypcb, 'setup'):
                        if hasattr(mypcb.setup, 'grid_origin'):
                            #say('aux_axis_origin' + str(mypcb.setup.aux_axis_origin))
                            xp=-mypcb.setup.grid_origin[0]; yp=mypcb.setup.grid_origin[1]
                            sayw('grid origin found @ ('+str(xp)+', '+str(yp)+')') 
                        else:
                            say('grid origin not set\nusing default top left corner')
                            xp=0;yp=0
                            grid_orig_warn=True
                    else:
                        say('grid origin not set\nusing default top left corner')
                        xp=0;yp=0
                        grid_orig_warn=True
                    ##off_x=-xp+xmin+(xMax-xmin)/2; off_y=-yp-(ymin+(yMax-ymin)/2)  #offset of the board & modules
                    #off_x=-xp+center_x;off_y=-yp+center_y
                    off_x=-xp;off_y=-yp


                if (aux_orig==1):
                    #xp=getAuxAxisOrigin()[0]; yp=-getAuxAxisOrigin()[1]  #offset of the board & modules
                    if hasattr(mypcb, 'setup'):
                        if hasattr(mypcb.setup, 'aux_axis_origin'):
                            #say('aux_axis_origin' + str(mypcb.setup.aux_axis_origin))
                            sayw('aux origin used: '+str(mypcb.setup.aux_axis_origin)) 
                            xp=-mypcb.setup.aux_axis_origin[0]; yp=mypcb.setup.aux_axis_origin[1]
                        else:
                            say('aux origin not used') 
                            xp=-148.5;yp=98.5
                    else:
                        say('aux origin not used') 
                        xp=-148.5;yp=98.5
                    ##off_x=-xp+xmin+(xMax-xmin)/2; off_y=-yp-(ymin+(yMax-ymin)/2)  #offset of the board & modules
                    #off_x=-xp+center_x;off_y=-yp+center_y
                    off_x=-xp;off_y=-yp
                #if (aux_orig==1):
                #    #xp=getAuxAxisOrigin()[0]; yp=-getAuxAxisOrigin()[1]  #offset of the board & modules
                #    if hasattr(mypcb.setup, 'aux_axis_origin'):
                #        #say('aux_axis_origin' + str(mypcb.setup.aux_axis_origin))
                #        xp=mypcb.setup.aux_axis_origin[0]; yp=-mypcb.setup.aux_axis_origin[1]
                #    else:
                #        say('aux origin not used') 
                #    ##off_x=-xp+xmin+(xMax-xmin)/2; off_y=-yp-(ymin+(yMax-ymin)/2)  #offset of the board & modules
                #    off_x=-xp+center_x;off_y=-yp+center_y
                #    #off_x=-xp;off_y=-yp


                modules,nsk = DrawPCB(mypcb,SketchLayer,override_pcb,keep_pcb_sketch)
                if override_pcb == True:
                    if use_AppPart and not force_oldGroups and not use_LinkGroups:
                        doc.getObject(board_name).addObject(doc.getObject(boardG_name))
                    elif use_LinkGroups:
                        doc.getObject(board_name).ViewObject.dropObject(doc.getObject(boardG_name),doc.getObject(boardG_name),'',[])
                if SketchLayer == 'Edge.Cuts':
                    FreeCAD.ActiveDocument.getObject(board_name).Label = fname
                if hasattr(mypcb, 'general'):
                    pcbThickness=float(mypcb.general.thickness)
                else:
                    pcbThickness=1.6
                ## stop  #test parser
                check_requirements()    #!# Check FreeCAD version, and whether Assy module is present
                #stop
                #pcbThickness,modules,board_elab,mod_lines,mod_arcs,mod_circles=LoadKicadBoard(name)
                #say(modules)
                #routineDrawPCB(pcbThickness,board_elab,mod_lines,mod_arcs,mod_circles)
                doc.commitTransaction()
                say('closing Transaction \'opening_kicad\'')
            else:
                # Specified filename was not located
                say(name+' missing\r')
                stop



            ##Placing board at configured position
            # pos objs x,-y
            # pos board xm+(xM-xm)/2
            # pos board -(ym+(yM-ym)/2)        
            if SketchLayer == 'Edge.Cuts':
                #center_x, center_y, bb_x, bb_y = findPcbCenter("Pcb")
                center_x, center_y, bb_x, bb_y = findPcbCenter(u"Pcb"+fname_sfx)
            else:
                draw=FreeCAD.ActiveDocument.PCB_Sketch_draft
                center_x, center_y, bb_x, bb_y = findPcbCenter(draw.Name)
            ## using PcbCenter
            xMax=center_x+bb_x/2
            xmin=center_x-bb_x/2
            yMax=center_y+bb_y/2
            ymin=center_y-bb_y/2
            #off_x=0; off_y=0  #offset of the board & modules
            if hasattr(mypcb, 'setup'):
                if hasattr(mypcb.setup, 'edge_width'): #maui edge width
                    edge_width=mypcb.setup.edge_width
                elif hasattr(mypcb.setup, 'edge_cuts_line_width'): #maui edge cuts new width k 5.99
                    edge_width=mypcb.setup.edge_cuts_line_width
            #if (grid_orig==1):
            #    #xp=getAuxAxisOrigin()[0]; yp=-getAuxAxisOrigin()[1]  #offset of the board & modules
            #    if hasattr(mypcb.setup, 'grid_origin'):
            #        #say('aux_axis_origin' + str(mypcb.setup.aux_axis_origin))
            #        xp=-mypcb.setup.grid_origin[0]; yp=mypcb.setup.grid_origin[1]
            #    else:
            #        say('grid origin not found\nplacing at center of an A4')
            #        xp=-148.5;yp=98.5
            #    ##off_x=-xp+xmin+(xMax-xmin)/2; off_y=-yp-(ymin+(yMax-ymin)/2)  #offset of the board & modules
            #    #off_x=-xp+center_x;off_y=-yp+center_y
            #    off_x=-xp;off_y=-yp
            if (base_orig==1):
                ##off_x=xmin+(xMax-xmin)/2; off_y=-(ymin+(yMax-ymin)/2)  #offset of the board & modules
                off_x=center_x;off_y=center_y
            #sayw(base_point);sayw(" base point")
            if (base_point==1):
                ##off_x=-xp+xmin+(xMax-xmin)/2; off_y=-yp-(ymin+(yMax-ymin)/2)  #offset of the board & modules
                #off_x=-xp+center_x;off_y=-yp+center_y
                off_x=-xp+center_x;off_y=-yp+center_y
                #sayw(off_x)
            ## test maui board_base_point_x=(xMax-xmin)/2-off_x
            ## test maui board_base_point_y=-((yMax-ymin)/2)-off_y
            #real_board_pos_x=xmin+(xMax-xmin)/2
            #real_board_pos_y=-(ymin+(yMax-ymin)/2)
            ## using PcbCenter
            real_board_pos_x=center_x
            real_board_pos_y=center_y
            # doc = FreeCAD.ActiveDocument
            if idf_to_origin == True:
                board_base_point_x=-off_x
                board_base_point_y=-off_y
            else:
            ## using PcbCenter
                say ('using PcbCenter')
                #board_base_point_x=xmin+(xMax-xmin)/2-off_x
                #board_base_point_y=-(ymin+(yMax-ymin)/2)-off_y
                board_base_point_x=center_x-off_x
                board_base_point_y=center_y-off_y
            sayw('placing board @ '+str(board_base_point_x)+','+str(board_base_point_y))
            if SketchLayer == 'Edge.Cuts':
                #FreeCAD.ActiveDocument.getObject("Pcb").Placement = FreeCAD.Placement(FreeCAD.Vector(board_base_point_x,board_base_point_y,0),FreeCAD.Rotation(FreeCAD.Vector(0,0,1),0))
                FreeCAD.ActiveDocument.getObject(pcb_name).Placement = FreeCAD.Placement(FreeCAD.Vector(board_base_point_x,board_base_point_y,0),FreeCAD.Rotation(FreeCAD.Vector(0,0,1),0))
            #else:
            #    draw.Placement = FreeCAD.Placement(FreeCAD.Vector(board_base_point_x,board_base_point_y,0),FreeCAD.Rotation(FreeCAD.Vector(0,0,1),0))
            newname="PCB_Sketch"+fname_sfx
            if load_sketch:
                if SketchLayer != 'Edge.Cuts' and SketchLayer is not None:
                    newname = SketchLayer.split('.')[0]+'_Sketch'
                say_inline('building up pcb time')
                get_time()
                say(str(running_time))
                t1=(running_time)
                #add_constraints("PCB_Sketch_draft")
                #FreeCAD.ActiveDocument.recompute()
                if aux_orig==1 or grid_orig ==1:
                    s_name=cpy_sketch("PCB_Sketch_draft",newname)
                    FreeCAD.ActiveDocument.recompute()
                    #add_constraints(s_name)
                    #say_time()
                #stop
                elif (base_point==1):
                    s_name=shift_sketch("PCB_Sketch_draft", [-center_x,center_y],newname)
                    #stop
                    #add_constraints(s_name)
                    FreeCAD.ActiveDocument.getObject(s_name).Placement = FreeCAD.Placement(FreeCAD.Vector(xp,yp,0),FreeCAD.Rotation(FreeCAD.Vector(0,0,1),0))
                    #say_time()            
                elif (base_orig==1):
                    s_name=shift_sketch("PCB_Sketch_draft", [-center_x,center_y],newname)
                    #stop
                    #add_constraints(s_name)
                    FreeCAD.ActiveDocument.getObject(s_name).Placement = FreeCAD.Placement(FreeCAD.Vector(0,0,0),FreeCAD.Rotation(FreeCAD.Vector(0,0,1),0))
                    #say_time()            
                else:
                    s_name=shift_sketch("PCB_Sketch_draft", [-center_x,center_y],newname)
                    #stop
                    #add_constraints(s_name)
                    #sayerr('usebasepoint')
                    #sayerr('usedefault')
                    FreeCAD.ActiveDocument.getObject(s_name).Placement = FreeCAD.Placement(FreeCAD.Vector(center_x,center_y,0),FreeCAD.Rotation(FreeCAD.Vector(0,0,1),0))
                    #stop
                    #say_time()
                # FreeCAD.ActiveDocument.removeObject("PCB_Sketch_draft")
                objs_toberemoved.append([FreeCAD.ActiveDocument.getObject("PCB_Sketch_draft")])
                if (zfit):
                    FreeCADGui.SendMsgToActiveView("ViewFit")
                if 0: # test_face # addConstraints!='none': 
                    say('start adding constraints to pcb sketch')
                    add_constraints(s_name)
                    get_time()
                    #say('adding constraints time ' +str(running_time-t1))
                    say('adding constraints time ' + "{0:.3f}".format(running_time-t1))
    
                ##FreeCAD.ActiveDocument.recompute()
                pcb_sk=FreeCAD.ActiveDocument.getObject(newname)
                gi = 0
                for g in pcb_sk.Geometry:
                    if 'BSplineCurve object' in str(g):
                        # say(str(g))
                        FreeCAD.ActiveDocument.getObject(newname).exposeInternalGeometry(gi)
                    gi+=1
                if use_LinkGroups and SketchLayer == 'Edge.Cuts':
                    FreeCAD.ActiveDocument.getObject(boardG_name).ViewObject.dropObject(FreeCAD.ActiveDocument.getObject(newname),FreeCAD.ActiveDocument.getObject(newname),'',[])
                    FreeCADGui.Selection.clearSelection()
                    sl = FreeCADGui.Selection.addSelection(FreeCAD.ActiveDocument.getObject(newname))
                    #FreeCADGui.runCommand('Std_HideSelection',0)
                    FreeCADGui.runCommand('Std_ToggleVisibility',0)
                    FreeCADGui.Selection.clearSelection()
                    #FreeCADGui.ActiveDocument.PCB_Sketch.Visibility = False
                    #FreeCAD.ActiveDocument.getObject('PCB_Sketch').adjustRelativeLinks(FreeCAD.ActiveDocument.getObject('Board_Geoms'))
                elif SketchLayer == 'Edge.Cuts':
                    FreeCAD.ActiveDocument.getObject(boardG_name).addObject(pcb_sk)
                
            #updating pcb_sketch
            if SketchLayer != 'Edge.Cuts' and SketchLayer is not None:
                pcb_sk.Label = SketchLayer
                if nsk > 1:
                    pcb_sk.Label+="s"
                    pcb_sk.ViewObject.Visibility=False
            #FreeCAD.ActiveDocument.getObject("PCB_Sketch").Placement = FreeCAD.Placement(FreeCAD.Vector(board_base_point_x,board_base_point_y,0),FreeCAD.Rotation(FreeCAD.Vector(0,0,1),0))
            #FreeCAD.ActiveDocument.getObject("PCB_SketchN").Placement = FreeCAD.Placement(FreeCAD.Vector(board_base_point_x,board_base_point_y,0),FreeCAD.Rotation(FreeCAD.Vector(0,0,1),0))
            ## FreeCAD.ActiveDocument.getObject("Pcb").Placement = FreeCAD.Placement(FreeCAD.Vector(-off_x,-off_y,0),FreeCAD.Rotation(FreeCAD.Vector(0,0,1),0))
            if (zfit):
                FreeCADGui.SendMsgToActiveView("ViewFit")
            #ImportGui.insert(u"./c0603.step","demo_5D_vrml_from_step")
            if (not pt_lnx): # and (not pt_osx): issue on AppImages hanging on loading 
                FreeCADGui.SendMsgToActiveView("ViewFit")
            else:
                zf= Timer (0.1,ZoomFitThread)
                zf.start()
            if keep_pcb_sketch == True:
                #sayw(sketch_name_sfx+'001')
                if doc.getObject(sketch_name_sfx+'001') in doc.Objects: #if 1: #try:
                    doc.removeObject(sketch_name_sfx+'001') #keep sketck & constrains
                    #objs_toberemoved.append([doc.getObject(sketch_name_sfx+'001')])
                    docG = FreeCADGui.ActiveDocument
                    docG.getObject(sketch_name_sfx).Visibility=True
            elif override_pcb == True:
                if doc.getObject(sketch_name_sfx) in doc.Objects: #if 1: #try:
                    docG = FreeCADGui.ActiveDocument
                    docG.getObject(sketch_name_sfx).Visibility=True
            if not pull_sketch or load_models:
                if use_AppPart and not force_oldGroups and not use_LinkGroups:
                    #sayw("creating hierarchy")
                    ## to evaluate to add App::Part hierarchy
                    doc.Tip = doc.addObject('App::Part',stepM_name)
                    stepM = doc.ActiveObject
                    stepM.Label = stepM_name
                    doc.Tip = doc.addObject('App::Part',top_name)
                    topG = doc.ActiveObject
                    topG.Label = top_name
                    doc.Tip = doc.addObject('App::Part',bot_name)
                    botG = doc.ActiveObject
                    botG.Label = bot_name
                    doc.getObject(stepM_name).addObject(doc.getObject(top_name))
                    doc.getObject(stepM_name).addObject(doc.getObject(bot_name))            
                    try:
                        doc.Step_Models.License = ''
                        doc.Step_Models.LicenseURL = ''
                    except:
                        pass
                    #FreeCADGui.activeView().setActiveObject('Step_Models', doc.Step_Models)
                    doc.getObject(board_name).addObject(doc.getObject(stepM_name))
                    doc.Tip = doc.addObject('App::Part',stepV_name)
                    stepV = doc.ActiveObject
                    stepV.Label = stepV_name
                    doc.Tip = doc.addObject('App::Part',topV_name)
                    topV = doc.ActiveObject
                    topV.Label = topV_name
                    doc.Tip = doc.addObject('App::Part',botV_name)
                    botV = doc.ActiveObject
                    botV.Label = botV_name
                    doc.getObject(stepV_name).addObject(doc.getObject(topV_name))
                    doc.getObject(stepV_name).addObject(doc.getObject(botV_name))
                    try:
                        stepV.License = ''
                        stepV.LicenseURL = ''
                    except:
                        pass
                    FreeCADGui.activeView().setActiveObject(stepV_name, stepV)
                    doc.getObject(board_name).addObject(doc.getObject(stepV_name))
                    doc.getObject(board_name).Label=fname
                    try:
                        doc.getObject(board_name).License=''
                        doc.getObject(board_name).LicenseURL=''
                    except:
                        pass
                    ## end hierarchy
                elif use_LinkGroups:
                    doc.Tip = doc.addObject('App::LinkGroup',stepM_name)
                    stepM=doc.ActiveObject
                    stepM.Label = stepM_name
                    doc.Tip = doc.addObject('App::LinkGroup',stepV_name)
                    stepV=doc.ActiveObject
                    stepV.Label = stepV_name
                    doc.addObject('App::LinkGroup',top_name)
                    topG=doc.ActiveObject
                    topG.Label = top_name
                    doc.addObject('App::LinkGroup',bot_name)
                    botG=doc.ActiveObject
                    botG.Label = bot_name
                    doc.addObject('App::LinkGroup',topV_name)
                    topVG=doc.ActiveObject
                    topVG.Label = topV_name
                    doc.addObject('App::LinkGroup',botV_name)
                    botVG=doc.ActiveObject
                    botVG.Label = botV_name
                    #doc.getObject('Top').adjustRelativeLinks(doc.getObject('Step_Models'))
                    doc.getObject(stepM_name).ViewObject.dropObject(doc.getObject(top_name),doc.getObject(top_name),'',[])
                    #doc.getObject('TopV').adjustRelativeLinks(doc.getObject('Step_Virtual_Models'))
                    doc.getObject(stepV_name).ViewObject.dropObject(doc.getObject(topV_name),doc.getObject(topV_name),'',[])
                    #doc.getObject('Bot').adjustRelativeLinks(doc.getObject('Step_Models'))
                    doc.getObject(stepM_name).ViewObject.dropObject(doc.getObject(bot_name),doc.getObject(bot_name),'',[])
                    #doc.getObject('BotV').adjustRelativeLinks(doc.getObject('Step_Virtual_Models'))
                    doc.getObject(stepV_name).ViewObject.dropObject(doc.getObject(botV_name),doc.getObject(botV_name),'',[])
                    #doc.getObject('Step_Models').adjustRelativeLinks(doc.getObject('Board'))
                    doc.getObject(board_name).ViewObject.dropObject(doc.getObject(stepM_name),doc.getObject(stepM_name),'',[])
                    #doc.getObject('Step_Virtual_Models').adjustRelativeLinks(doc.getObject('Board'))
                    doc.getObject(board_name).ViewObject.dropObject(doc.getObject(stepV_name),doc.getObject(stepV_name),'',[])
                    FreeCADGui.Selection.clearSelection()
                else:
                    #sayerr("creating flat groups")
                    doc.addObject("App::DocumentObjectGroup", stepM_name)
                    doc.addObject("App::DocumentObjectGroup", stepV_name)
                doc.recompute()
                say_time()
                if disable_VBO:
                    paramGetV = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/View")
                    VBO_status=paramGetV.GetBool("UseVBO")
                    #sayerr("checking VBO")
                    say("VBO status "+str(VBO_status))
                    if VBO_status:
                        paramGetV.SetBool("UseVBO",False)
                        sayw("disabling VBO")
                    #stop
                #stop   
                if disable_PoM_Observer:
                    #paramGetPoM = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/PartOMagic")
                    #PoMObs_status=paramGetPoM.GetBool("EnableObserver")
                    PoMObs_status = False
                    if Observer.isRunning():
                        PoMObs_status=True
                    #if PoMObs_status:
                        Observer.stop()
                #    paramGetPoM.SetBool("EnableObserver",False)
                        sayw("disabling PoM Observer")
        
                prefs = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/Import")
                ImportMode_status = 0
                if hasattr(prefs, 'GetInts'):
                    if len(prefs.GetInts()) > 0:
                        if prefs.GetInt('ImportMode') != 0:
                            ImportMode_status = prefs.GetInt('ImportMode')
                            prefs.SetInt('ImportMode', 0)
                            sayerr('STEP ImportMode NOT as \'Single document\''+'\n')
                ##ReadShapeCompoundMode
                paramGetVS = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/Import/hSTEP")
                ReadShapeCompoundMode_status=paramGetVS.GetBool("ReadShapeCompoundMode")
                #sayerr("checking ReadShapeCompoundMode")
                sayw("ReadShapeCompoundMode status "+str(ReadShapeCompoundMode_status))
                #FreeCAD.Console.PrintLog("ReadShapeCompoundMode status "+str(ReadShapeCompoundMode_status)+"\n")
                #stop
                enable_ReadShapeCompoundMode=False
                if ReadShapeCompoundMode_status and allow_compound=='True' \
                   or ReadShapeCompoundMode_status and allow_compound=='Hierarchy':
                    paramGetVS = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/Import/hSTEP")
                    paramGetVS.SetBool("ReadShapeCompoundMode",False)
                    sayw("disabling ReadShapeCompoundMode")
                    enable_ReadShapeCompoundMode=True
                elif not ReadShapeCompoundMode_status and allow_compound=='Simplified':
                    paramGetVS = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/Import/hSTEP")
                    paramGetVS.SetBool("ReadShapeCompoundMode",True)
                    sayw("enabling ReadShapeCompoundMode -> Simplified Mode")
                    enable_ReadShapeCompoundMode=True
                #paramGetVS.SetBool("ReadShapeCompoundMode",False)
                if load_sketch:
                    FreeCADGui.ActiveDocument.getObject(newname).Visibility=False # hidden Sketch
                ##Load 3D models
                #Load_models(pcbThickness,modules)
                if (zfit):
                    FreeCADGui.SendMsgToActiveView("ViewFit")
                #else:        
                Load_models(pcbThickness,modules)
        
                #enable_ReadShapeCompoundMode=False
                if enable_ReadShapeCompoundMode:
                    paramGetVS = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/Import/hSTEP")
                    paramGetVS.SetBool("ReadShapeCompoundMode",ReadShapeCompoundMode_status)
                    sayw("enabling ReadShapeCompoundMode")
                if disable_VBO:
                    if VBO_status:
                        paramGetV.SetBool("UseVBO",True)
                        sayw("enabling VBO")
                if disable_PoM_Observer:
                    if PoMObs_status:
                        Observer.start()
                #    paramGetPoM.SetBool("EnableObserver",True)
                        sayw("enabling PoM Observer")
                
                def find_nth(haystack, needle, n):
                    start = haystack.find(needle)
                    while start >= 0 and n > 1:
                        start = haystack.find(needle, start+len(needle))
                        n -= 1
                    return start
                
                msg=""
                n_rpt=0
                for mod3d in modules:
                    #say(mod3d)
                    #for e in mod3d:
                    #    print e #.decode("utf-8")
                    #if mod3d[5] is not None:
                    if mod3d[5] != "":
                        say(mod3d[0]);sayw(" error: reset"+mod3d[5])
                        #stop 
                        #msg+=""+mod3d[0].decode("utf-8")+" error: "+mod3d[5]+"<br>"
                        msg+=""+mod3d[0]+"<br>error: "+mod3d[5]+"<br>"
                        n_rpt=n_rpt+1
                n_rpt_max=10
                zf= Timer (0.3,ZoomFitThread)
                zf.start()
                if (show_messages==True) and msg!="":
                    msg="""<b>error in model(s)</b><br>"""+msg
                    QtGui.QApplication.restoreOverrideCursor()
                    #print n_rpt,'-',p_rpt
                    if n_rpt >  n_rpt_max:
                        p_rpt=find_nth(msg, '<br>', n_rpt_max)
                        #print n_rpt,'-',p_rpt
                        reply = QtGui.QMessageBox.information(None,"Info ...",msg[:p_rpt]+'<br><b> . . .</b>')
                    else:
                        reply = QtGui.QMessageBox.information(None,"Info ...",msg)
                
                #if 'LinkView' in dir(FreeCADGui):
                #    FreeCADGui.Selection.clearSelection()
                #    o=FreeCAD.ActiveDocument.getObject('Board')
                #    #FreeCADGui.Selection.addSelection('Board')
                #    FreeCADGui.Selection.addSelection(doc.Name,o.Name)
                #    #import expTree; #import importlib;importlib.reload(expTree)
                #    #print('collapsing selection')
                #    #expTree.collS_Tree() #toggle_Tree()
                #    clps = Timer (3,collaps_Tree)
                #    clps.start()
                if export_board_2step:
                    #say('aliveTrue')
                    Export2MCAD(blacklisted_model_elements)
                else:
                    #say('aliveFalse')
                    Display_info(blacklisted_model_elements)
                if (zfit):
                    FreeCADGui.SendMsgToActiveView("ViewFit")
            msg="running time: "+str(round(running_time,3))+"sec"    
            say(msg)
            zf= Timer (0.3,ZoomFitThread)
            zf.start()
            zf.cancel()
            if SketchLayer != 'Edge.Cuts' and SketchLayer is not None:
                FreeCADGui.ActiveDocument.ActiveView.viewTop()
            if grid_orig_warn: #adding a warning message because GridOrigin is set in FC Preferences but not set in KiCAD pcbnew file
                msg = 'GridOrigin is set in FC Preferences but not set in KiCAD pcbnew file'
                sayw(msg)
                QtGui.QApplication.restoreOverrideCursor()
                msg="""<b><font color='red'>GridOrigin is set in FreeCAD Preferences<br>but not set in KiCAD pcbnew file</font></b>"""
                msg+="""<br><br>Please assign Grid Origin to your KiCAD pcbnew board file"""
                msg+="""<br>for a better Mechanical integration"""
                reply = QtGui.QMessageBox.information(None,"Warning ...",msg)
            prefsKSU = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/kicadStepUpGui")
            prefs = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/Import")
            paramGetVS = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/Import/hSTEP")
            ReadShapeCompoundMode_status=paramGetVS.GetBool("ReadShapeCompoundMode")
            if ImportMode_status != 0:
                prefs.SetInt('ImportMode',ImportMode_status)
            FCV_date = ''
            STEP_UseAppPart_available = False
            if len (FreeCAD.Version()) >= 5:
                FCV_date = str(FreeCAD.Version()[4])
                FCV_date = FCV_date[0:FCV_date.find(' ')]
                say('FreeCAD build date: '+FCV_date)
                if FCV_date >= '2020/06/27':
                    STEP_UseAppPart_available = True #new STEP import export mode available
                    say('STEP UseAppPart available')
            if hasattr(prefs, 'GetBools'):
                if (('UseAppPart' in prefs.GetBools() or 'UseLinkGroup' in prefs.GetBools()) and STEP_UseAppPart_available) or len (prefs.GetBools()) == 0:
                    if (not prefs.GetBool('UseAppPart') and not ('UseLinkGroup' in prefs.GetBools()))  or prefs.GetBool('UseLegacyImporter') or not prefs.GetBool('UseBaseName')\
                        or prefs.GetBool('ExportLegacy') or ReadShapeCompoundMode_status or prefs.GetBool('UseLinkGroup'): #  or ImportMode_status != 0:
                        msg = "Please set your preferences for STEP Import Export as in the displayed image\n"
                        msg += "(you can disable this warning on StepUp preferences)\n"
                        if 'help_warning_enabled' in prefsKSU.GetBools():
                            if prefsKSU.GetBool('help_warning_enabled'):
                                StepPrefsDlg = QtGui.QDialog()
                                ui = Ui_STEP_Preferences()
                                ui.setupUi(StepPrefsDlg)
                                reply=StepPrefsDlg.exec_()
                                sayw(msg)
                                #QtGui.QApplication.restoreOverrideCursor()
                                #reply = QtGui.QMessageBox.information(None,"Info ...",msg)
                        else: #first time new settings parameter
                            StepPrefsDlg = QtGui.QDialog()
                            ui = Ui_STEP_Preferences()
                            ui.setupUi(StepPrefsDlg)
                            reply=StepPrefsDlg.exec_()
                            sayw(msg)
            
            #say_time()
            #stop
    def removing_kobjs():
        ''' removing objects after delay ''' 
        from kicadStepUptools import removesubtree
        doc=FreeCAD.ActiveDocument
        if doc is not None:
            doc.openTransaction('rmv_objs_kicad')
            for tbr in objs_toberemoved:
                removesubtree(tbr)
            doc.commitTransaction()
        # doc.undo()
        # doc.undo()
        # adding a timer to allow double transactions during the python code
    QtCore.QTimer.singleShot(0.2,removing_kobjs)
    if (zfit):
        FreeCADGui.SendMsgToActiveView("ViewFit")
    #ImportGui.insert(u"./c0603.step","demo_5D_vrml_from_step")
    if (not pt_lnx): # and (not pt_osx): issue on AppImages hanging on loading 
        FreeCADGui.SendMsgToActiveView("ViewFit")
    else:
        zf= Timer (0.25,ZoomFitThread)
        zf.start()
    
        
###

def routineR_XYZ(axe,alpha):
    global resetP
    say('routine Rotate XYZ')
    if "Assembly2Workbench" not in FreeCADGui.activeWorkbench().name():
        if "PartWorkbench" not in FreeCADGui.activeWorkbench().name():
            FreeCADGui.activateWorkbench("PartWorkbench")
    #FreeCADGui.SendMsgToActiveView("ViewFit")
    ##FreeCADGui.activeDocument().activeView().viewTop()
    doc = FreeCAD.ActiveDocument
    #FreeCAD.Console.PrintMessage("hereXYZ !")
    selEx = FreeCADGui.Selection.getSelectionEx()
    objs = [selobj.Object for selobj in selEx]
    if len(objs) == 1:
    #if len(sel[0]) == 1:
        check_AP()
        selEx = FreeCADGui.Selection.getSelectionEx()
        objs = [selobj.Object for selobj in selEx]
        s = objs[0].Shape
        shape=s.copy()
        shape.Placement=s.Placement;
        boundBox_ = s.BoundBox
        boundBoxLX = boundBox_.XLength
        boundBoxLY = boundBox_.YLength
        boundBoxLZ = boundBox_.ZLength
        a = str(boundBox_)
        a,b = a.split('(')
        c = b.split(',')
        oripl_X = float(c[0])
        oripl_Y = float(c[1])
        oripl_Z = float(c[2])
        #say("bbx: "+str(boundBoxLX)+" bby: "+str(boundBoxLY)+"bbz: "+str(boundBoxLZ))
        #say("x: "+str(oripl_X)+" y: "+str(oripl_Y)+"z: "+str(oripl_Z))
        #shape.rotate((oripl_X,oripl_Y,oripl_Z),(1,0,0),90)
        angle=alpha
        if axe=='x':
            #shape.rotate((0,0,0),(1,0,0),90)
            shape.rotate((oripl_X+boundBoxLX/2,oripl_Y+boundBoxLY/2,oripl_Z+boundBoxLZ/2),(1,0,0),int(angle))
        if axe=='y':
            #shape.rotate((0,0,0),(0,1,0),90)
            shape.rotate((oripl_X+boundBoxLX/2,oripl_Y+boundBoxLY/2,oripl_Z+boundBoxLZ/2),(0,1,0),int(angle))
        if axe=='z':
            #shape.rotate((0,0,0),(0,0,1),90)
            shape.rotate((oripl_X+boundBoxLX/2,oripl_Y+boundBoxLY/2,oripl_Z+boundBoxLZ/2),(0,0,1),int(angle))
        #Part.show(shape)
        objs[0].Placement=shape.Placement
        FreeCADGui.Selection.addSelection(objs[0])
        FreeCAD.activeDocument().recompute()
        if resetP==True:
            routineResetPlacement()
        #say("end of rotineZ!")
    else:
        say("Select ONE single part object !")
        say_single_obj()
        #QtGui.QMessageBox.information(None,"Info ...","Select ONE single part object !\r\n"+"\r\n")
###  end RotateXYZ

def routineT_XYZ(axe,v):
    global resetP
    say('routine Translate XYZ')
    if "Assembly2Workbench" not in FreeCADGui.activeWorkbench().name():
        if "PartWorkbench" not in FreeCADGui.activeWorkbench().name():
            FreeCADGui.activateWorkbench("PartWorkbench")
    #FreeCADGui.SendMsgToActiveView("ViewFit")
    ##FreeCADGui.activeDocument().activeView().viewTop()
    doc = FreeCAD.ActiveDocument
    selEx = FreeCADGui.Selection.getSelectionEx()
    objs = [selobj.Object for selobj in selEx]
    if len(objs) == 1:
        check_AP()
        selEx = FreeCADGui.Selection.getSelectionEx()
        objs = [selobj.Object for selobj in selEx]
        s = objs[0].Shape
        shape=s.copy()
        shape.Placement=s.Placement;
        #shape.rotate((oripl_X,oripl_Y,oripl_Z),(1,0,0),90)
        #say("axe "+axe+", value "+v)
        if axe=='x':
            shape.translate((float(v),0,0))
        if axe=='y':
            shape.translate((0,float(v),0))
        if axe=='z':
            shape.translate((0,0,float(v)))
        #Part.show(shape)
        objs[0].Placement=shape.Placement
        FreeCADGui.Selection.addSelection(objs[0])
        FreeCAD.activeDocument().recompute()
        if resetP==True:
            routineResetPlacement()
        #say("end of rotineT!")
    else:
        say("Select ONE single part object !")
        say_single_obj()
        #QtGui.QMessageBox.information(None,"Info ...","Select ONE single part object !\r\n"+"\r\n")
###  end TranslateXYZ

def routineResetPlacement(keepWB=None):
    objs=[]
    if "Assembly2Workbench" not in FreeCADGui.activeWorkbench().name():
        if "PartWorkbench" not in FreeCADGui.activeWorkbench().name():
            if keepWB is None:
                FreeCADGui.activateWorkbench("PartWorkbench")
    #FreeCADGui.SendMsgToActiveView("ViewFit")
    ##FreeCADGui.activeDocument().activeView().viewTop()
    doc = FreeCAD.ActiveDocument
    selEx = FreeCADGui.Selection.getSelectionEx()
    objs = [selobj.Object for selobj in selEx]
    #print 'here'
    if len(objs) == 1:
        say('routine reset Placement properties')

        s=objs[0].Shape
        r=[]
        t=s.copy()
        for i in t.childShapes():
            c=i.copy()
            c.Placement=t.Placement.multiply(c.Placement)
            r.append((i,c))

        w=t.replaceShape(r)
        w.Placement=FreeCAD.Placement()
        Part.show(w)
        #say(w)

        if hasattr(FreeCADGui.ActiveDocument.getObject(objs[0].Name),'ShapeColor'):
            FreeCADGui.ActiveDocument.ActiveObject.ShapeColor=FreeCADGui.ActiveDocument.getObject(objs[0].Name).ShapeColor
            FreeCADGui.ActiveDocument.ActiveObject.LineColor=FreeCADGui.ActiveDocument.getObject(objs[0].Name).LineColor
            FreeCADGui.ActiveDocument.ActiveObject.PointColor=FreeCADGui.ActiveDocument.getObject(objs[0].Name).PointColor
            FreeCADGui.ActiveDocument.ActiveObject.DiffuseColor=FreeCADGui.ActiveDocument.getObject(objs[0].Name).DiffuseColor
        FreeCADGui.ActiveDocument.ActiveObject.Transparency=FreeCADGui.ActiveDocument.getObject(objs[0].Name).Transparency

        new_label=objs[0].Label
        FreeCAD.ActiveDocument.removeObject(objs[0].Name)
        FreeCAD.ActiveDocument.recompute()
        FreeCAD.ActiveDocument.ActiveObject.Label=new_label
        rObj=FreeCAD.ActiveDocument.ActiveObject
        del objs
        FreeCADGui.Selection.addSelection(rObj)
        #FreeCAD.activeDocument().recompute()
        #say("end of rotineRP!")
    else:
        say("Select ONE single part object !")
        say_single_obj()
        #QtGui.QMessageBox.information(None,"Info ...","Select ONE single part object !\r\n"+"\r\n")
        del objs
### end reset prop

def routineScaleVRML():
    global exportV, exportS, applymaterials
    if FreeCAD.ActiveDocument.FileName == "":
        msg="""please <b>save</b> your job file before exporting."""
        QtGui.QApplication.restoreOverrideCursor()
        QtGui.QMessageBox.information(None,"Info ...",msg)
        FreeCADGui.SendMsgToActiveView("Save")
    say('routine Scale to VRML 1/2.54')
    cfg_read_all()
    doc = FreeCAD.ActiveDocument
    doc.openTransaction('exportModel')
    selEx = FreeCADGui.Selection.getSelectionEx()
    objs = [selobj.Object for selobj in selEx]
    if len(objs) >= 1:  #allow more than 1 obj for vrml
        say('exporting')
        fullFilePathName=doc.FileName
        if fullFilePathName=="":
            if os.path.exists(models3D_prefix):
                if isWritable(models3D_prefix):
                #if os.access(models3D_prefix, os.W_OK | os.X_OK):
                    models3D_prefix_tosave = re.sub("\\\\", "/", models3D_prefix)
                    if models3D_prefix_tosave.endswith('/'):
                        fullFilePathName=models3D_prefix+doc.Label+'.FCStd'
                    else:
                        fullFilePathName=models3D_prefix+os.sep+doc.Label+'.FCStd'
                    say('saving to '+models3D_prefix_tosave)
                else:
                    home = expanduser("~")
                    fullFilePathName=home+os.sep+doc.Label+'.FCStd'
                    say('path not found/writable, saving to '+home)
                    #say(fullFilePathName)
            else:
                    home = expanduser("~")
                    fullFilePathName=home+os.sep+doc.Label+'.FCStd'
                    say('path not found/writable, saving to '+home)
                    #say(fullFilePathName)
        else:
            say(fullFilePathName)
        lbl=go_export(fullFilePathName)
        path, fname = os.path.split(fullFilePathName)
        #fname=os.path.splitext(fname)[0]
        #fname=objs[0].Label
        ##fname=FreeCAD.ActiveDocument.ActiveObject.Label  #step reset placement
        fname=lbl  #step reset placement
        #removing not allowed chars
        translation_table = dict.fromkeys(map(ord, '<>:"/\|?*,;:\\'), None)
        fname=fname.translate(translation_table)
        vrml_ext='.wrl'
        prefs = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/kicadStepUpGui")
        if prefs.GetBool('wrz_export_enabled'):
            #'stpz'
            vrml_ext='.wrz'
        stp_ext='.step'
        if prefs.GetBool('stpz_export_enabled'):
            stp_ext='.stpZ'
        #print('stpZ',fullFilePathNameStep)
        if exportV or exportS:
            msg="""<b>export STEP & scaled VRML file for kicad!</b>
            <font color='white'>****************************************************************************</font><br>
            <i>exporting folder: </i><br><b>- <a href='"""+path+"""' target='_blank'>"""+path+"""</a></b>"""
            msg+="""<br><i>exporting filename: </i><br>"""
            if exportV:
                msg+="""- <b>"""+fname+vrml_ext+"""<br>"""
            if exportS:
                msg+="""</b>- <b>"""+fname+stp_ext+"""</b>"""
            else:
                if len(objs) >= 1:
                    msg+="""<br></b>- <b>step file not exported; multi-part selected</b>"""
            #msg="export scaled VRML file for kicad!\r\n"
            #msg=msg+"****************************************************************************"
            msg=msg+"<br><br><i>3D settings in kicad Module Editor:</i><br>"
            msg=msg+"<b>- scale 1 1 1\r\n- offset 0 0 0<br>- rotation 0 0 "+str(rot_wrl)+"</b>"
            ##self.setWindowState(QtCore.Qt.WindowMinimized)
            QtGui.QApplication.restoreOverrideCursor()
            QtGui.QMessageBox.information(None,"Info ...",msg)
            ##self.setWindowState(QtCore.Qt.WindowActive)
            say('done')
            FreeCAD.ActiveDocument.commitTransaction()
    else:
        say("Select ONE single part object !")
        say_single_obj()
        #QtGui.QMessageBox.information(None,"Info ...","Select ONE single part object !\r\n"+"\r\n")
    return 0    
###

###
def routineScaleVRML_1():
    global rot_wrl, zfit
    say('routine Scale to VRML 1/2.54')
    if "Assembly2Workbench" not in FreeCADGui.activeWorkbench().name():
        if "PartWorkbench" not in FreeCADGui.activeWorkbench().name():
            FreeCADGui.activateWorkbench("PartWorkbench")
    #FreeCADGui.SendMsgToActiveView("ViewFit")
    ##FreeCADGui.activeDocument().activeView().viewTop()
    doc = FreeCAD.ActiveDocument
    selEx = FreeCADGui.Selection.getSelectionEx()
    objs = [selobj.Object for selobj in selEx]
    if len(objs) == 1:
        objS=FreeCAD.ActiveDocument.getObject(objs[0].Name).Shape
        #FreeCADGui.ActiveDocument.getObject(objs[0].Name).BoundingBox = True
        final_Label=FreeCAD.ActiveDocument.getObject(objs[0].Name).Label
        myobjG=FreeCADGui.ActiveDocument.getObject(objs[0].Name)
        myobjA=FreeCAD.ActiveDocument.getObject(objs[0].Name)
        mynewdoc=FreeCAD.newDocument()
        FreeCAD.ActiveDocument.addObject('Part::Feature',objs[0].Name).Shape=objS

        #print 'here'
        myobjA1=FreeCAD.ActiveDocument.ActiveObject
        #myobjA1.Label=final_Label
        myobjG1=FreeCADGui.ActiveDocument.ActiveObject
        myobjG1.ShapeColor=myobjG.ShapeColor
        myobjG1.LineColor=myobjG.LineColor
        myobjG1.PointColor=myobjG.PointColor
        myobjG1.DiffuseColor=myobjG.DiffuseColor
        myobjG1.Transparency=myobjG.Transparency
        FreeCAD.ActiveDocument.recompute()

        FreeCAD.ActiveDocument.ActiveObject.Label=final_Label+'_vrml'
        say( final_Label+'_vrml' )
        #FreeCADGui.ActiveDocument.getObject(objs[0].Name).Visibility=False

        FreeCAD.ActiveDocument.recompute()
        vrml_obj = Draft.scale(FreeCAD.ActiveDocument.ActiveObject,delta=FreeCAD.Vector(0.3937,0.3937,0.3937),center=FreeCAD.Vector(0,0,0),legacy=True)
        FreeCAD.ActiveDocument.recompute()
        #FreeCAD.ActiveDocument.ActiveObject.ViewObject.DisplayMode = 'Shaded'
        FreeCADGui.ActiveDocument.ActiveObject.BoundingBox = False
        #FreeCAD.ActiveDocument.ActiveObject.ViewObject.DisplayMode = 'Shaded'
        #vrml_obj.ViewObject.DisplayMode = u'Shaded'
        shade_val='Shaded'
        #FreeCAD.ActiveDocument.ActiveObject.ViewObject.DisplayMode = 'Shaded'
        FreeCAD.ActiveDocument.ActiveObject.ViewObject.DisplayMode = 1 #Shaded
        if (zfit):
            FreeCADGui.SendMsgToActiveView("ViewFit")
        msg="""<b>export scaled VRML file for kicad!</b>
            <font color='white'>****************************************************************************</font><br>
            <i>3D settings in kicad Module Editor:</i><br>
            <font color='white'>- </font><b>scale 1 1 1\r\n- offset 0 0 0\r\n- rotation 0 0 {0}</b>
            """.format(rot_wrl)
        #msg="export scaled VRML file for kicad!\r\n"
        #msg=msg+"****************************************************************************"
        #msg=msg+"\r\n3D settings in kicad Module Editor:\r\n"
        #msg=msg+"- scale 1 1 1\r\n- offset 0 0 0\r\n- rotation 0 0 "+str(rot_wrl)
        self.setWindowState(QtCore.Qt.WindowMinimized)
        QtGui.QApplication.restoreOverrideCursor()
        QtGui.QMessageBox.information(None,"Info ...",msg)
        self.setWindowState(QtCore.Qt.WindowActive)
    else:
        say("Select ONE single part object !")
        say_single_obj()
        #QtGui.QMessageBox.information(None,"Info ...","Select ONE single part object !\r\n"+"\r\n")
    return 0

###  end ScaleVRML_1
def routineC_XYZ(axe):
    global resetP
    say('routine center position')
    #if self.checkBox_1.isChecked():
    #    routineResetPlacement()
    if "Assembly2Workbench" not in FreeCADGui.activeWorkbench().name():
        if "PartWorkbench" not in FreeCADGui.activeWorkbench().name():
            FreeCADGui.activateWorkbench("PartWorkbench")
    #FreeCADGui.SendMsgToActiveView("ViewFit")
    ##FreeCADGui.activeDocument().activeView().viewTop()
    doc = FreeCAD.ActiveDocument
    say("Centering on Axe XYZ !")
    selEx = FreeCADGui.Selection.getSelectionEx()
    objs = [selobj.Object for selobj in selEx]
    if len(objs) == 1:
        check_AP()
        selEx = FreeCADGui.Selection.getSelectionEx()
        objs = [selobj.Object for selobj in selEx]
        s = objs[0].Shape
        shape=s.copy()
        #shape.Placement=s.Placement;
        shape.Placement= FreeCAD.Placement(FreeCAD.Vector(0,0,0),FreeCAD.Rotation(FreeCAD.Vector(0,0,1),0))
        boundBox_ = s.BoundBox
        boundBoxLX = boundBox_.XLength
        boundBoxLY = boundBox_.YLength
        boundBoxLZ = boundBox_.ZLength
        say("bbox: "+str(boundBox_))

        a = str(boundBox_)
        a,b = a.split('(')
        c = b.split(',')
        oripl_X = float(c[0])
        oripl_Y = float(c[1])
        oripl_Z = float(c[2])
        #say("bbx: "+str(boundBoxLX)+" bby: "+str(boundBoxLY)+"bbz: "+str(boundBoxLZ))
        #say("x: "+str(oripl_X)+" y: "+str(oripl_Y)+"z: "+str(oripl_Z))

        p=s.Placement
        #say("PlacementBase  : "+str(p))
        #say(str(p.Base[0])+' '+str(p.Base[1])+' '+str(p.Base[2]))
        if axe=='x':
            #shape.translate((0,0,0))
            diffPl=-oripl_X-boundBoxLX/2
            #shape.Placement.move(diffPl,0,0)
            #shape.translate(Base.Vector(diffPl,0,0))
            shape.translate((diffPl,p.Base[1],p.Base[2]))
        if axe=='y':
            diffPl=-oripl_Y-boundBoxLY/2
            #shape.translate(Base.Vector(0,diffPl,0))
            shape.translate((p.Base[0],diffPl,p.Base[2]))
        if axe=='z':
            diffPl=-oripl_Z-boundBoxLZ/2
            shape.translate((p.Base[0],p.Base[1],diffPl))
            #shape.translate(Base.Vector(0,0,diffPl))
        ### to zero posX -bboxX/2
        #say("x: "+str(oripl_X)+" y: "+str(oripl_Y)+"z: "+str(oripl_Z))
        #say("axe "+axe+" placement"+str(diffPl))
        #Part.show(shape)
        objs[0].Placement=shape.Placement
        FreeCADGui.Selection.addSelection(objs[0])
        FreeCAD.activeDocument().recompute()
        #say("x: "+str(oripl_X)+"\r\ny: "+str(oripl_Y)+"\r\nz: "+str(oripl_Z))
        if resetP==True:
            routineResetPlacement()
            #say("pos reset done")
        #say("done")
    else:
        say("Select an object !")
        say_single_obj()
        #QtGui.QMessageBox.information(None,"Info ...","Select an object !")
###  end routineC_XYZ

def routineP_XYZ(axe):
    global resetP
    say('routine put on axe')
    #routineResetPlacement()
    if "Assembly2Workbench" not in FreeCADGui.activeWorkbench().name():
        if "PartWorkbench" not in FreeCADGui.activeWorkbench().name():
            FreeCADGui.activateWorkbench("PartWorkbench")
    #FreeCADGui.SendMsgToActiveView("ViewFit")
    ##FreeCADGui.activeDocument().activeView().viewTop()
    doc = FreeCAD.ActiveDocument
    say("Put on Axe XYZ !")
    selEx = FreeCADGui.Selection.getSelectionEx()
    objs = [selobj.Object for selobj in selEx]
    if len(objs) == 1:
        check_AP()
        selEx = FreeCADGui.Selection.getSelectionEx()
        objs = [selobj.Object for selobj in selEx]
        s = objs[0].Shape
        shape=s.copy()
        #shape.Placement=s.Placement;
        shape.Placement= FreeCAD.Placement(FreeCAD.Vector(0,0,0),FreeCAD.Rotation(FreeCAD.Vector(0,0,1),0))
        boundBox_ = s.BoundBox
        boundBoxLX = boundBox_.XLength
        boundBoxLY = boundBox_.YLength
        boundBoxLZ = boundBox_.ZLength
        a = str(boundBox_)
        a,b = a.split('(')
        c = b.split(',')
        oripl_X = float(c[0])
        oripl_Y = float(c[1])
        oripl_Z = float(c[2])
        p=s.Placement
        say("PlacementBase  : "+str(p))
        #say(str(p.Base[0])+' '+str(p.Base[1])+' '+str(p.Base[2]))
        if axe=='x':
            #shape.translate((0,0,0))
            diffPl=p.Base[0]-oripl_X
            #shape.Placement.move(diffPl,0,0)
            #shape.translate(Base.Vector(diffPl,0,0))
            shape.translate((diffPl,p.Base[1],p.Base[2]))
        if axe=='y':
            diffPl=p.Base[1]-oripl_Y
            #shape.translate(Base.Vector(0,diffPl,0))
            shape.translate((p.Base[0],diffPl,p.Base[2]))
        if axe=='z':
            diffPl=p.Base[2]-oripl_Z
            shape.translate((p.Base[0],p.Base[1],diffPl))
            #shape.translate(Base.Vector(0,0,diffPl))
        ### to zero posX -bboxX/2
        #say("x: "+str(oripl_X)+" y: "+str(oripl_Y)+"z: "+str(oripl_Z))
        #say("axe "+axe+" placement"+str(diffPl))
        #Part.show(shape)
        objs[0].Placement=shape.Placement
        FreeCADGui.Selection.addSelection(objs[0])
        FreeCAD.activeDocument().recompute()
        #say("x: "+str(oripl_X)+"\r\ny: "+str(oripl_Y)+"\r\nz: "+str(oripl_Z))
        #say("placement "+str(p[0]))
        #return [oripl_X, oripl_Y, oripl_Z,p.Base[0],p.Base[1],p.Base[2]];
        if resetP==True:
            routineResetPlacement()
    else:
        say("Select ONE single part object !")
        say_single_obj()
        #QtGui.QMessageBox.information(None,"Info ...","Select ONE single part object !\r\n")
###  end routineP_XYZ

def say_single_obj():
        QtGui.QApplication.restoreOverrideCursor()
        msg="""Select <b>ONE single part</b> object !<br>
        suggestion for multi-part:<br>&nbsp;&nbsp;<b>Part Boolean Union (recommended)</b><br><i>or<br>&nbsp;&nbsp;Part Make compound (alternative choice)</i>"""
        spc="""<font color='white'>*******************************************************************************</font><br>
        """
        msg1="Error in selection"
        QtGui.QApplication.restoreOverrideCursor()
        #RotateXYZGuiClass().setGeometry(25, 250, 500, 500)
        diag = QtGui.QMessageBox(QtGui.QMessageBox.Icon.Critical,
                                msg1,
                                msg)
        diag.setWindowModality(QtCore.Qt.ApplicationModal)
        diag.exec_()

def say_select_obj():
        QtGui.QApplication.restoreOverrideCursor()
        msg="""Select <b>a Compound</b> or <br><b>a Part Design group</b><br>or <b>more than one Part</b> object !<br>"""
        spc="""<font color='white'>*******************************************************************************</font><br>
        """
        msg1="Error in selection"
        QtGui.QApplication.restoreOverrideCursor()
        #RotateXYZGuiClass().setGeometry(25, 250, 500, 500)
        diag = QtGui.QMessageBox(QtGui.QMessageBox.Icon.Critical,
                                msg1,
                                msg)
        diag.setWindowModality(QtCore.Qt.ApplicationModal)
        diag.exec_()

def say_warning(msg):
        QtGui.QApplication.restoreOverrideCursor()
        # msg="""Select <b>a Compound</b> or <br><b>a Part Design group</b><br>or <b>more than one Part</b> object !<br>"""
        spc="""<font color='white'>*******************************************************************************</font><br>
        """
        msg1="Warning ..."
        QtGui.QApplication.restoreOverrideCursor()
        #RotateXYZGuiClass().setGeometry(25, 250, 500, 500)
        diag = QtGui.QMessageBox(QtGui.QMessageBox.Icon.Warning,
                                msg1,
                                msg)
        diag.setWindowModality(QtCore.Qt.ApplicationModal)
        diag.exec_()

def say_info(msg):
        QtGui.QApplication.restoreOverrideCursor()
        # msg="""Select <b>a Compound</b> or <br><b>a Part Design group</b><br>or <b>more than one Part</b> object !<br>"""
        spc="""<font color='white'>*******************************************************************************</font><br>
        """
        msg1="Info ..."
        QtGui.QApplication.restoreOverrideCursor()
        #RotateXYZGuiClass().setGeometry(25, 250, 500, 500)
        diag = QtGui.QMessageBox(QtGui.QMessageBox.Icon.Information,
                                msg1,
                                msg)
        diag.setWindowModality(QtCore.Qt.ApplicationModal)
        diag.exec_()

def get_position():
    global min_val, exportS
    say('routine get base position')
    if "Assembly2Workbench" not in FreeCADGui.activeWorkbench().name():
        if "PartWorkbench" not in FreeCADGui.activeWorkbench().name():
            FreeCADGui.activateWorkbench("PartWorkbench")
    #FreeCADGui.SendMsgToActiveView("ViewFit")
    ##FreeCADGui.activeDocument().activeView().viewTop()
    doc = FreeCAD.ActiveDocument
    #say("hereXYZ !")
    selEx = FreeCADGui.Selection.getSelectionEx()
    objs = [selobj.Object for selobj in selEx]
    if len(objs) == 1:
        try:
            s = objs[0].Shape
            boundBox_ = s.BoundBox
            boundBoxLX = boundBox_.XLength
            boundBoxLY = boundBox_.YLength
            boundBoxLZ = boundBox_.ZLength
            a = str(boundBox_)
            a,b = a.split('(')
            c = b.split(',')
            oripl_X = float(c[0])
            oripl_Y = float(c[1])
            oripl_Z = float(c[2])
            FreeCADGui.Selection.addSelection(objs[0])
            FreeCAD.activeDocument().recompute()
            #say("x: "+str(oripl_X)+"\r\ny: "+str(oripl_Y)+"\r\nz: "+str(oripl_Z))
            p=s.Placement
            #say("PlacementBase  : "+str(p))
            #say(str(p.Base[0])+' '+str(p.Base[1])+' '+str(p.Base[2]))
            ### to zero posX -bboxX/2
            #say("placement "+str(p[0]))
            #min_val=10e-16
            #say("min_val "+str(min_val))
            if abs(oripl_X) < min_val:
                oripl_X=0
            if abs(oripl_Y) < min_val:
                oripl_Y=0
            if abs(oripl_Z) < min_val:
                oripl_Z=0
            return [oripl_X, oripl_Y, oripl_Z,p.Base[0],p.Base[1],p.Base[2]];
        except:
            pass
    else:
        if exportS:
            say("Select ONE single part object !")
            ##QtGui.QMessageBox.information(None,"Info ...","Select ONE single part object !\r\n"+"\r\n")
            #QtGui.QApplication.restoreOverrideCursor()
            #msg="""Select <b>ONE single part</b> object !<br>
            #suggestion for multi-part:<br>&nbsp;&nbsp;<b>Part Boolean Union (recommended)</b><br><i>or<br>&nbsp;&nbsp;Part Make compound (alternative choice)</i>"""
            #spc="""<font color='white'>*******************************************************************************</font><br>
            #"""
            #msg1="Error in selection"
            #QtGui.QApplication.restoreOverrideCursor()
            ##RotateXYZGuiClass().setGeometry(25, 250, 500, 500)
            #diag = QtGui.QMessageBox(QtGui.QMessageBox.Icon.Critical,
            #                        msg1,
            #                        msg)
            #diag.setWindowModality(QtCore.Qt.ApplicationModal)
            #diag.exec_()
###  end get position

def routineM_XYZ(axe,v):
    global resetP
    mydoc=FreeCAD.ActiveDocument
    say('routine Move to point XYZ')
    if "Assembly2Workbench" not in FreeCADGui.activeWorkbench().name():
        if "PartWorkbench" not in FreeCADGui.activeWorkbench().name():
            FreeCADGui.activateWorkbench("PartWorkbench")
    #FreeCADGui.SendMsgToActiveView("ViewFit")
    ##FreeCADGui.activeDocument().activeView().viewTop()
    doc = FreeCAD.ActiveDocument
    selEx = FreeCADGui.Selection.getSelectionEx()
    objs = [selobj.Object for selobj in selEx]
    if len(objs) == 1:
        check_AP()
        selEx = FreeCADGui.Selection.getSelectionEx()
        objs = [selobj.Object for selobj in selEx]
        s = objs[0].Shape
        boundBox_ = s.BoundBox
        boundBoxLX = boundBox_.XLength
        boundBoxLY = boundBox_.YLength
        boundBoxLZ = boundBox_.ZLength
        a = str(boundBox_)
        a,b = a.split('(')
        c = b.split(',')
        oripl_X = float(c[0])
        oripl_Y = float(c[1])
        oripl_Z = float(c[2])
        shape=s.copy()
        shape.Placement=s.Placement;p=s.Placement
        #shape.rotate((oripl_X,oripl_Y,oripl_Z),(1,0,0),90)
        #say("axe "+axe+", value "+v)
        if axe=='x':
            #if abs(float(v)-p.Base[0])>min_val:
            shape.translate((float(v)-oripl_X,0,0))
        if axe=='y':
            shape.translate((0,float(v)-oripl_Y,0))
        if axe=='z':
            shape.translate((0,0,float(v)-oripl_Z))
        #Part.show(shape)
        objs[0].Placement=shape.Placement
        FreeCADGui.Selection.addSelection(objs[0])
        FreeCAD.activeDocument().recompute()
        if resetP==True:
            routineResetPlacement()
        #say("end of rotineM!")
    else:
        say("Select an object !")
        #QtGui.QMessageBox.information(None,"Info ...","Select ONE single part object !\r\n"+"\r\n")
###  end Move to Point XYZ

def recurse_app_part(ap,apl):  # recursive function to get a list of Part objects contained in an AppPart obj
    if "App::Part" in ap.TypeId or "Body" in ap.TypeId:
        for o in ap.Group:
            #sayw(o.Name)
            if "App::Part" in o.TypeId or "Body" in o.TypeId:
                recurse_app_part(o,apl)
            elif "Sketch" not in o.TypeId:
                #print str(apl)
                #print o
                #if str(o.Name) not in str(apl):
                apl.append(o)
        return apl
    elif "Compound" in ap.TypeId:
        for e in ap.Links:
            if 'Compound' in e.Name:
                recurse_app_part(e,apl)
            else:
                apl.append(e)
        return apl
##

def routineCollisions():
    global conflict_tolerance
    def error_dialog(msg):
        """Create a simple dialog QMessageBox with an error message"""
        FreeCAD.Console.PrintError(msg + '\n')
        QtGui.QApplication.restoreOverrideCursor()
        diag = QtGui.QMessageBox(QtGui.QMessageBox.Icon.Critical,
                                'Error in checking Collisions                                                       ."+"\r\n"',
                                msg)
        diag.setWindowModality(QtCore.Qt.ApplicationModal)
        diag.exec_()

    #if len(FreeCADGui.Selection.getSelectionEx()) < 2:
    if len(FreeCADGui.Selection.getSelection()) < 2:
        error_dialog('Select at least two objects')
        collisions=2
        return collisions

    object_list = []
    object_names_list = []
    collisions=0
    #for obj in FreeCADGui.Selection.getSelectionEx():
    #        object_list.append(obj.Object)
    n_objs=0
    apl=[]
    for obj in FreeCADGui.Selection.getSelection():
        #print obj.TypeId
        if ('Part' in obj.TypeId or 'App::Link' in obj.TypeId or 'App::LinkPython' in obj.TypeId) and 'App::Part' not in obj.TypeId and 'Compound' not in obj.TypeId and 'Body' not in obj.TypeId:
            #print obj.TypeId
            #object_list.append(obj)
            if obj.Name not in object_names_list:
                if hasattr(obj,"Placement"):
                    object_list.append(obj)
                    n_objs=n_objs+1
                    #object_names_list.append(obj.Name)
                    #n_objs=n_objs+1
        elif 'App::Part' in obj.TypeId or 'Compound' in obj.TypeId or 'Body' in obj.TypeId:
            # adding any single part of the group
            #say('recursing AppPart or Compound')
            apl=[]
            recurse_app_part(obj,apl)
            apl_names=[]
            for o in apl:
                #print o.Name,' ','apl'
                ##if o.Name not in apl_names:
                    ##apl_names.append(o.Name)
                apl_names.append(o.Name)
                #print o.Name,' name appended'
            #print apl_names,' apl names'
            for on in apl_names:
                object_list.append(FreeCAD.ActiveDocument.getObject(on))
                n_objs=n_objs+1
            #print object_list
    #stop
    if n_objs < 2:
        error_dialog('Select at least two simple objects')
        collisions=2
        return collisions
    for i, object_a in enumerate(object_list):
        for object_b in object_list[(i + 1):]:
            say(make_string(object_a.Label)+" "+make_string(object_b.Label))
            if not hasattr(object_a,'Shape'): # use_Links
                shape_a = Part.getShape(object_a)
            else:
                shape_a = object_a.Shape
            #shape_a = object_a.Shape
            if not hasattr(object_b,'Shape'): # use_Links
                shape_b = Part.getShape(object_b)
            else:
                shape_b = object_b.Shape
            #shape_b = object_b.Shape
            label_a = make_string(object_a.Label)
            label_b = make_string(object_b.Label)
            try:
                ## find the real position of the Part inside App::Part, then check collisions
                if use_AppPart:
                    #print object_a.InListRecursive
                    #print object_b.InListRecursive
                    ## copy objects and apply absolute placement to each one, then check collisions
                    p0 =  FreeCAD.Placement (FreeCAD.Vector(0,0,0), FreeCAD.Rotation(0,0,0), FreeCAD.Vector(0,0,0))
                    pa_Original=shape_a.Placement
                    s=shape_a
                    #say('resetting props #2')
                    r=[]
                    t=s.copy()
                    for i in t.childShapes():
                        c=i.copy()
                        c.Placement=t.Placement.multiply(c.Placement)
                        r.append((i,c))
                    acpy=t.replaceShape(r)
                    acpy.Placement=FreeCAD.Placement()
                    #Part.show(acpy)         
                    #stop
                    lrl=len(object_a.InListRecursive)
                    #for o in object_a.InListRecursive:
                    #    say(o.Name)
                    inverted=True
                    if len(object_a.InList):
                        if object_a.InListRecursive[0].Name == object_a.InList[0].Name:
                            inverted=False
                    if inverted:
                        for i in range (0,lrl):
                            if hasattr(object_a.InListRecursive[i],'Placement'):
                                acpy.Placement=acpy.Placement.multiply(object_a.InListRecursive[i].Placement)
                    else:
                        for i in range (0,lrl):
                            if hasattr(object_a.InListRecursive[i],'Placement'):
                                acpy.Placement=acpy.Placement.multiply(object_a.InListRecursive[lrl-1-i].Placement)
                    #acpy.Placement=acpy.Placement.multiply(pa_Original)
                    # Part.show(acpy)         
                    # stop
                    pb_Original=shape_b.Placement
                    s=shape_b
                    #say('resetting props #2')
                    r=[]
                    t=s.copy()
                    for i in t.childShapes():
                        c=i.copy()
                        c.Placement=t.Placement.multiply(c.Placement)
                        r.append((i,c))
                    bcpy=t.replaceShape(r)
                    bcpy.Placement=FreeCAD.Placement()
                    lrl=len(object_b.InListRecursive)
                    if len(object_b.InList):
                        if object_b.InListRecursive[0].Name == object_b.InList[0].Name:
                            inverted=False
                    if inverted:
                        for i in range (0,lrl):
                            if hasattr(object_b.InListRecursive[i],'Placement'):
                                bcpy.Placement=bcpy.Placement.multiply(object_b.InListRecursive[i].Placement)
                    else:
                        for i in range (0,lrl):
                            if hasattr(object_b.InListRecursive[i],'Placement'):
                                bcpy.Placement=bcpy.Placement.multiply(object_b.InListRecursive[lrl-1-i].Placement)
                    #Part.show(bcpy)         
                    common = acpy.common(bcpy)
                    #FreeCAD.ActiveDocument.removeObject(acpy)
                    #FreeCAD.ActiveDocument.removeObject(bcpy)
                    FreeCAD.ActiveDocument.recompute()
                #stop
            ##try:
            ##    ## find the real position of the Part inside App::Part, then check collisions
            ##    ## print object_a.InListRecursive
            ##    ## 
            ##    #b=App.ActiveDocument.addObject("Part::Box","Box")
            ##    if use_AppPart:
            ##        acpy= FreeCAD.ActiveDocument.copyObject(object_a,False)
            ##        bcpy= FreeCAD.ActiveDocument.copyObject(object_b,False)
            ##        #shape=acpy.Shape.copy()
            ##        #shape.Placement=acpy.Placement
            ##        #impPart.Placement=shape.Placement;
            ##        ## copy objects and apply absolute placement to each one, then check collisions
            ##        for o in object_b.InListRecursive:
            ##            acpy.Placement=acpy.Placement.multiply(o.Placement)
            ##        #Part.show(shape)
            ##        #acpy.Placement=shape.Placement
            ##        #stop
            ##        #lr=len(object_a.InListRecursive)
            ##        #for i in range(lr-1,-1,-1):
            ##        #    print object_a.InListRecursive[i].Label
            ##        #    #print get_node_plc(object_a.InListRecursive[i],acpy)
            ##        #    shape.Placement=shape.Placement.multiply(object_a.InListRecursive[i].Placement)
            ##        #    #acpy.Placement=acpy.Placement.multiply(object_a.InListRecursive[i].Placement)
            ##        #acpy.Placement=shape.Placement
            ##        #stop
            ##        for o in object_b.InListRecursive:
            ##            bcpy.Placement=bcpy.Placement.multiply(o.Placement)
            ##            #print 'doing'
            ##        #print bcpy.Name, 'here'
            ##        common = acpy.Shape.common(bcpy.Shape)
            ##        #FreeCAD.ActiveDocument.removeObject(acpy.Name)
            ##        #FreeCAD.ActiveDocument.removeObject(bcpy.Name)
            ##        #FreeCAD.ActiveDocument.recompute()
            ##    #stop
                else:
                    common = shape_a.common(shape_b)
                #d = shape_a.distToShape(shape_b)
                #sayw(d)
                #sayerr(d[0])
                if common.Volume > conflict_tolerance:
                    say(
                        'Volume of the intersection between {} and {}: {}\n'.format(
                            label_a,
                            label_b,
                            common.Volume))
                    redundant=False
                    for o in FreeCAD.ActiveDocument.Objects:
                        if make_string(o.Label) == 'Collisions ({} - {})'.format(label_a, label_b):
                            sayw('collision redundant')
                            redundant=True
                    if not redundant:
                        intersection_object = FreeCAD.ActiveDocument.addObject(
                            'Part::Feature')
                        intersection_object.Label = 'Collisions ({} - {})'.format(
                            label_a, label_b)
                        intersection_object.Shape = common
                        ## print object_a.InListRecursive
                        ## for o in object_a.InListRecursive:
                        ##     intersection_object.Placement=intersection_object.Placement.multiply(o.Placement)
                        ##     print o.Name
                        
                        ## bg=App.ActiveDocument.getObject('Board')
                        ## intersection_object.Placement=bg.Placement.multiply(common.Placement)
                        intersection_object.ViewObject.ShapeColor = (1.0, 0.0, 0.0, 1.0)
                        #object_a.ViewObject.Transparency = 80
                        #object_b.ViewObject.Transparency = 80
                        #object_a.ViewObject.Visibility=False
                        #object_b.ViewObject.Visibility=False
                        sel1 = FreeCADGui.Selection.getSelection()
                        for e in sel1:
                            FreeCADGui.ActiveDocument.getObject(e.Name).Visibility=False
                        ##for e in FreeCAD.ActiveDocument.Objects:
                        ##    if 'Compound' in e.TypeId:
                        ##        if object_a in e.Links or object_b in e.Links:
                        ##            e.ViewObject.Visibility=False
                        ##    elif 'App::Part' in e.TypeId:
                        ##        if object_a in e.Group: # and object_a not in sel1:
                        ##            object_a.ViewObject.Visibility=True
                        ##            FreeCADGui.ActiveDocument.getObject(e.Name).Visibility=False
                        ##        if object_b in e.Group: # and object_b not in sel1:
                        ##            object_b.ViewObject.Visibility=True
                        ##            FreeCADGui.ActiveDocument.getObject(e.Name).Visibility=False
                        ##        if FreeCADGui.ActiveDocument.getObject(e.Name).Visibility==False:
                        ##            for a in FreeCAD.ActiveDocument.Objects:
                        ##                if 'App::Part' in a.TypeId and a.Name != e.Name:
                        ##                    #if a not in sel1:
                        ##                        #print a.Group, e
                        ##                    if e in a.Group and: e not in sel1:
                        ##                        FreeCADGui.ActiveDocument.getObject(e.Name).Visibility=True
                        collisions=1
                else:
                    say(
                        'No intersection between {} and {}\n'.format(
                            label_a,
                            label_b))
                    #collisions=0
            except Exception as e:
                FreeCAD.Console.PrintWarning(u"{0}\n".format(e))
            #say("here_collision\r\n")
    return collisions

### end Collisions

def create_axis():

    global disablePoM_Observer
    if disable_PoM_Observer:
        #paramGetPoM = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/PartOMagic")
        #PoMObs_status=paramGetPoM.GetBool("EnableObserver")
        PoMObs_status = False
        if Observer.isRunning():
            PoMObs_status=True
        #if PoMObs_status:
            Observer.stop()
            sayw("disabling PoM Observer")
    FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroup", "axis")
    #Z axis
    FreeCAD.ActiveDocument.addObject("Part::Box","AxisBoxZ")
    FreeCAD.ActiveDocument.ActiveObject.Label = "CubeZ"
    FreeCAD.ActiveDocument.addObject("Part::Cone","AxisConeZ")
    FreeCAD.ActiveDocument.ActiveObject.Label = "ConeZ"
    FreeCAD.ActiveDocument.getObject("AxisBoxZ").Width = '0 mm'
    FreeCAD.ActiveDocument.getObject("AxisBoxZ").Width = '0.1 mm'
    FreeCAD.ActiveDocument.getObject("AxisBoxZ").Length = '0 mm'
    FreeCAD.ActiveDocument.getObject("AxisBoxZ").Length = '0.2 mm'
    FreeCAD.ActiveDocument.getObject("AxisConeZ").Radius1 = '0 mm'
    FreeCAD.ActiveDocument.getObject("AxisConeZ").Radius1 = '0.4 mm'
    FreeCAD.ActiveDocument.getObject("AxisConeZ").Radius2 = '0 mm'
    FreeCAD.ActiveDocument.getObject("AxisConeZ").Radius2 = '0.1 mm'
    FreeCAD.ActiveDocument.getObject("AxisConeZ").Placement = FreeCAD.Placement(FreeCAD.Vector(0,0,9),FreeCAD.Rotation(FreeCAD.Vector(0,0,1),0))
    FreeCAD.ActiveDocument.getObject("AxisConeZ").Height = '5 mm'
    FreeCAD.ActiveDocument.getObject("AxisBoxZ").Placement = FreeCAD.Placement(FreeCAD.Vector(-0.1,-0.05,0),FreeCAD.Rotation(FreeCAD.Vector(0,0,1),0))
    FreeCADGui.ActiveDocument.getObject("AxisConeZ").ShapeColor = (0.0000,0.0000,1.0000)
    FreeCADGui.ActiveDocument.getObject("AxisBoxZ").ShapeColor = (0.0000,0.0000,1.0000)
    FreeCAD.activeDocument().addObject("Part::MultiFuse","FusionAxisZ")
    FreeCAD.activeDocument().FusionAxisZ.Shapes = [FreeCAD.activeDocument().AxisBoxZ,FreeCAD.activeDocument().AxisConeZ,]
    FreeCADGui.activeDocument().AxisBoxZ.Visibility=False
    FreeCADGui.activeDocument().AxisConeZ.Visibility=False
    FreeCADGui.ActiveDocument.FusionAxisZ.ShapeColor=FreeCADGui.ActiveDocument.AxisBoxZ.ShapeColor
    FreeCADGui.ActiveDocument.FusionAxisZ.DisplayMode=FreeCADGui.ActiveDocument.AxisBoxZ.DisplayMode
    FreeCAD.ActiveDocument.recompute()
    FreeCAD.ActiveDocument.addObject('Part::Feature','FusionAxisZ1').Shape=FreeCAD.ActiveDocument.FusionAxisZ.Shape
    FreeCAD.ActiveDocument.ActiveObject.Label = "Z"

    FreeCADGui.ActiveDocument.ActiveObject.ShapeColor=(0.0000,0.0000,1.0000)
    obj=FreeCAD.ActiveDocument.ActiveObject
    FreeCAD.ActiveDocument.getObject("axis").addObject(obj)
    FreeCAD.ActiveDocument.recompute()
    FreeCAD.ActiveDocument.removeObject("FusionAxisZ")
    FreeCAD.ActiveDocument.removeObject("AxisBoxZ")
    FreeCAD.ActiveDocument.removeObject("AxisConeZ")
    FreeCAD.ActiveDocument.recompute()

    #Y axis
    FreeCAD.ActiveDocument.addObject("Part::Box","AxisBoxY")
    FreeCAD.ActiveDocument.ActiveObject.Label = "CubeY"
    FreeCAD.ActiveDocument.addObject("Part::Cone","AxisConeY")
    FreeCAD.ActiveDocument.ActiveObject.Label = "ConeY"
    FreeCAD.ActiveDocument.getObject("AxisBoxY").Width = '0 mm'
    FreeCAD.ActiveDocument.getObject("AxisBoxY").Width = '0.1 mm'
    FreeCAD.ActiveDocument.getObject("AxisBoxY").Length = '0 mm'
    FreeCAD.ActiveDocument.getObject("AxisBoxY").Length = '0.2 mm'
    FreeCAD.ActiveDocument.getObject("AxisConeY").Radius1 = '0 mm'
    FreeCAD.ActiveDocument.getObject("AxisConeY").Radius1 = '0.4 mm'
    FreeCAD.ActiveDocument.getObject("AxisConeY").Radius2 = '0 mm'
    FreeCAD.ActiveDocument.getObject("AxisConeY").Radius2 = '0.1 mm'
    FreeCAD.ActiveDocument.getObject("AxisConeY").Placement = FreeCAD.Placement(FreeCAD.Vector(0,0,9),FreeCAD.Rotation(FreeCAD.Vector(0,0,1),0))
    FreeCAD.ActiveDocument.getObject("AxisConeY").Height = '5 mm'
    FreeCAD.ActiveDocument.getObject("AxisBoxY").Placement = FreeCAD.Placement(FreeCAD.Vector(-0.1,-0.05,0),FreeCAD.Rotation(FreeCAD.Vector(0,0,1),0))
    FreeCADGui.ActiveDocument.getObject("AxisConeY").ShapeColor = (0.0000,1.0000,0.0000)
    FreeCADGui.ActiveDocument.getObject("AxisBoxY").ShapeColor = (0.0000,1.0000,0.0000)
    FreeCAD.activeDocument().addObject("Part::MultiFuse","FusionAxisY")
    FreeCAD.activeDocument().FusionAxisY.Shapes = [FreeCAD.activeDocument().AxisBoxY,FreeCAD.activeDocument().AxisConeY,]
    FreeCADGui.activeDocument().AxisBoxY.Visibility=False
    FreeCADGui.activeDocument().AxisConeY.Visibility=False
    FreeCADGui.ActiveDocument.FusionAxisY.ShapeColor=FreeCADGui.ActiveDocument.AxisBoxY.ShapeColor
    FreeCADGui.ActiveDocument.FusionAxisY.DisplayMode=FreeCADGui.ActiveDocument.AxisBoxY.DisplayMode
    FreeCAD.ActiveDocument.recompute()
    FreeCAD.ActiveDocument.addObject('Part::Feature','FusionAxisY1').Shape=FreeCAD.ActiveDocument.FusionAxisY.Shape
    FreeCAD.ActiveDocument.ActiveObject.Label = "Y"

    FreeCADGui.ActiveDocument.ActiveObject.ShapeColor=(0.0000,1.0000,0.000)
    obj=FreeCAD.ActiveDocument.ActiveObject
    FreeCAD.ActiveDocument.getObject("axis").addObject(obj)
    FreeCAD.ActiveDocument.recompute()
    FreeCAD.ActiveDocument.removeObject("FusionAxisY")
    FreeCAD.ActiveDocument.removeObject("AxisBoxY")
    FreeCAD.ActiveDocument.removeObject("AxisConeY")
    FreeCAD.ActiveDocument.recompute()
    FreeCAD.ActiveDocument.ActiveObject.Placement = FreeCAD.Placement(FreeCAD.Vector(0,0,0.05),FreeCAD.Rotation(FreeCAD.Vector(1,0,0),-90))

    #X axis
    FreeCAD.ActiveDocument.addObject("Part::Box","AxisBoxX")
    FreeCAD.ActiveDocument.ActiveObject.Label = "CubeX"
    FreeCAD.ActiveDocument.addObject("Part::Cone","AxisConeX")
    FreeCAD.ActiveDocument.ActiveObject.Label = "ConeX"
    FreeCAD.ActiveDocument.getObject("AxisBoxX").Width = '0 mm'
    FreeCAD.ActiveDocument.getObject("AxisBoxX").Width = '0.2 mm'
    FreeCAD.ActiveDocument.getObject("AxisBoxX").Length = '0 mm'
    FreeCAD.ActiveDocument.getObject("AxisBoxX").Length = '0.1 mm'
    FreeCAD.ActiveDocument.getObject("AxisConeX").Radius1 = '0 mm'
    FreeCAD.ActiveDocument.getObject("AxisConeX").Radius1 = '0.4 mm'
    FreeCAD.ActiveDocument.getObject("AxisConeX").Radius2 = '0 mm'
    FreeCAD.ActiveDocument.getObject("AxisConeX").Radius2 = '0.1 mm'
    FreeCAD.ActiveDocument.getObject("AxisConeX").Placement = FreeCAD.Placement(FreeCAD.Vector(0,0,9),FreeCAD.Rotation(FreeCAD.Vector(0,0,1),0))
    FreeCAD.ActiveDocument.getObject("AxisConeX").Height = '5 mm'
    FreeCAD.ActiveDocument.getObject("AxisBoxX").Placement = FreeCAD.Placement(FreeCAD.Vector(-0.1,-0.05,0),FreeCAD.Rotation(FreeCAD.Vector(0,0,1),0))
    FreeCADGui.ActiveDocument.getObject("AxisConeX").ShapeColor = (1.0000,0.0000,0.0000)
    FreeCADGui.ActiveDocument.getObject("AxisBoxX").ShapeColor = (1.0000,0.0000,0.0000)
    FreeCAD.activeDocument().addObject("Part::MultiFuse","FusionAxisX")
    FreeCAD.activeDocument().FusionAxisX.Shapes = [FreeCAD.activeDocument().AxisBoxX,FreeCAD.activeDocument().AxisConeX,]
    FreeCADGui.activeDocument().AxisBoxX.Visibility=False
    FreeCADGui.activeDocument().AxisConeX.Visibility=False
    FreeCADGui.ActiveDocument.FusionAxisX.ShapeColor=FreeCADGui.ActiveDocument.AxisBoxX.ShapeColor
    FreeCADGui.ActiveDocument.FusionAxisX.DisplayMode=FreeCADGui.ActiveDocument.AxisBoxX.DisplayMode
    FreeCAD.ActiveDocument.recompute()
    FreeCAD.ActiveDocument.addObject('Part::Feature','FusionAxisX1').Shape=FreeCAD.ActiveDocument.FusionAxisX.Shape
    FreeCAD.ActiveDocument.ActiveObject.Label="X"

    FreeCADGui.ActiveDocument.ActiveObject.ShapeColor=(1.0000,0.0000,0.0000)
    obj=FreeCAD.ActiveDocument.ActiveObject
    FreeCAD.ActiveDocument.getObject("axis").addObject(obj)
    FreeCAD.ActiveDocument.recompute()
    FreeCAD.ActiveDocument.removeObject("FusionAxisX")
    FreeCAD.ActiveDocument.removeObject("AxisBoxX")
    FreeCAD.ActiveDocument.removeObject("AxisConeX")
    FreeCAD.ActiveDocument.getObject("FusionAxisX1").Placement = FreeCAD.Placement(FreeCAD.Vector(0,-0.05,0),FreeCAD.Rotation(FreeCAD.Vector(0,1,0),90))

    FreeCAD.ActiveDocument.recompute()
    if disable_PoM_Observer:
        if PoMObs_status:
            Observer.start()
            sayw("enabling PoM Observer")
    
###
#############################
def createSolidBBox2(model3D):
    #FreeCADGui.Selection.removeSelection(FreeCAD.activeDocument().ActiveObject)
    selEx=model3D
    selEx = FreeCADGui.Selection.getSelectionEx()
    objs = [selobj.Object for selobj in selEx]
    if len(objs) == 1:
        s = objs[0].Shape
        name=objs[0].Label
        #say(name+" name")
        # boundBox
        delta=0.6
        boundBox_ = s.BoundBox
        boundBoxLX = boundBox_.XLength*(1+delta)
        boundBoxLY = boundBox_.YLength*(1+delta)
        #boundBoxLZ = boundBox_.ZLength
        boundBoxLZ = 1.58
        offX=boundBox_.XLength*(-delta)/2
        offY=boundBox_.YLength*(-delta)/2
        offZ=-0.01
        a = str(boundBox_)
        a,b = a.split('(')
        c = b.split(',')
        oripl_X = float(c[0])+offX
        oripl_Y = float(c[1])+offY
        #oripl_Z = float(c[2])+offZ
        oripl_Z = -boundBoxLZ+offZ

        #say(str(boundBox_))
        #say("Rectangle : "+str(boundBox_.XLength)+" x "+str(boundBox_.YLength)+" x "+str(boundBox_.ZLength))
        #say("_____________________")
        #say("x: "+str(oripl_X)+" y: "+str(oripl_Y)+"z: "+str(oripl_Z))

        obj=FreeCAD.ActiveDocument.addObject('Part::Feature',name)
        #obj.Shape=Part.makeBox(boundBox_.XLength, boundBox_.YLength, boundBox_.ZLength, FreeCAD.Vector(oripl_X,oripl_Y,oripl_Z), FreeCAD.Vector(0,0,01))
        #obj.Shape=Part.makeBox(boundBoxLX, boundBoxLY, boundBoxLZ, FreeCAD.Vector(oripl_X,oripl_Y,oripl_Z), FreeCAD.Vector(0,0,01))
        obj.Shape=Part.makeBox(boundBoxLX, boundBoxLY, boundBoxLZ, FreeCAD.Vector(oripl_X,oripl_Y,oripl_Z), FreeCAD.Vector(0,0,1))

        #obj.translate(offX,offY,0)
        # Part.show(cube)
        #say("cube name "+ obj.Name)
        ### FreeCAD.ActiveDocument.recompute()
    else:
        say("Select a single part object !")
    #end bbox macro

    name=obj.Name
    #say("bbox name "+name)
    del objs
    return name

###
def rotateObj(mainObj, rot):
    return mainObj.rotate(FreeCAD.Vector(rot[0], rot[1], 0), FreeCAD.Vector(0, 0, 1), rot[2])
###
def rotateObjs(listObjs, rot):
    #listObjs.rotate(FreeCAD.Vector(rot[0], rot[1], 0), FreeCAD.Vector(0, 0, 1), rot[2])
    Draft.rotate(listObjs,rot[2],FreeCAD.Vector(rot[0],rot[1],0.0),axis=FreeCAD.Vector(0.0,0.0,1.0),copy=False)
###
def changeSide(self, mainObj, X1, Y1, top):
    if top == 0:  #to bot side
        mainObj.rotate(FreeCAD.Vector(X1, Y1, 0), FreeCAD.Vector(0, 1, 0), 180)
###
def arcMidPoint(prev_vertex, vertex, angle):
    if len(prev_vertex) == 3:
        [x1, y1, z1] = prev_vertex
    else:
        [x1, y1] = prev_vertex

    if len(vertex) == 3:
        [x2, y2, z2] = vertex
    else:
        [x2, y2] = vertex

    angle = radians(angle / 2)
    basic_angle = atan2(y2 - y1, x2 - x1) - pi / 2
    shift = (1 - cos(angle)) * hypot(y2 - y1, x2 - x1) / 2 / sin(angle)
    midpoint = [(x2 + x1) / 2 + shift * cos(basic_angle), (y2 + y1) / 2 + shift * sin(basic_angle)]

    return midpoint

###

def sinus(angle):
    return float("%4.10f" % sin(radians(angle)))

def cosinus(angle):
    return float("%4.10f" % cos(radians(angle)))

def arcCenter(x1, y1, x2, y2, x3, y3):
    Xs = 0.5 * (x2 * x2 * y3 + y2 * y2 * y3 - x1 * x1 * y3 + x1 * x1 * y2 - y1 * y1 * y3 + y1 * y1 * y2 + y1 * x3 * x3 + y1 * y3 * y3 - y1 * x2 * x2 - y1 * y2 * y2 - y2 * x3 * x3 - y2 * y3 * y3) / (y1 * x3 - y1 * x2 - y2 * x3 - y3 * x1 + y3 * x2 + y2 * x1)
    Ys = 0.5 * (-x1 * x3 * x3 - x1 * y3 * y3 + x1 * x2 * x2 + x1 * y2 * y2 + x2 * x3 * x3 + x2 * y3 * y3 - x2 * x2 * x3 - y2 * y2 * x3 + x1 * x1 * x3 - x1 * x1 * x2 + y1 * y1 * x3 - y1 * y1 * x2) / (y1 * x3 - y1 * x2 - y2 * x3 - y3 * x1 + y3 * x2 + y2 * x1)

    return [Xs, Ys]

#def arcCenter2(x1, y1, x2, y2, angle):
#    # point M - center point between p1 and p2
#    Mx = (x1 + x2) / 2.
#    My = (y1 + y2) / 2.
#    
#    # p1_M - distance between point p1 and M
#    p1_M = sqrt((x1 - Mx) ** 2 + (y1 - My) ** 2)
#    radius = float("%4.9f" % abs(p1_M / sin(radians(angle / 2.))))  # radius of searching circle - line C_p1
#    CenterDist = float("%4.9f" % abs(radius * cos(radians(angle / 2.))))  # radius of searching circle - line C_p1
#    
#    return CenterDist

def arcRadius(x1, y1, x2, y2, angle):
    #dx = abs(x2 - x1)
    #dy = abs(y2 - y1)
    #d = sqrt(dx ** 2 + dy ** 2)  # distance between p1 and p2

    # point M - center point between p1 and p2
    Mx = (x1 + x2) / 2.
    My = (y1 + y2) / 2.
    
    # p1_M - distance between point p1 and M
    p1_M = sqrt((x1 - Mx) ** 2 + (y1 - My) ** 2)
    radius = float("%4.9f" % abs(p1_M / sin(radians(angle / 2.))))  # radius of searching circle - line C_p1
    
    return radius

def arcAngles2 (edge,angle): #(xs, ys, xe, ye, cx, cy, angle):

    #sa = atan2 (ys-cy, xs-cx)
    #ea = atan2 (ye-cy, xe-cx)
    ##if angle > 0:
    ##    sa = atan2 (ys-cy, xs-cx)
    ##    ea = sa + radians(angle) #2*pi+angle #atan2 (ye-cy, xe-cx)
    ##else:
    ##    sa = atan2 (ye-cy, xe-cx)
    ##    ea = sa + radians(abs(angle)) # 2*pi+angle #atan2 (ye-cy, xe-cx)
    #ea = ea - pi/2
    #sa = sa - pi/2
    #if ea == sa:
    #    ea = pi/2
    
    if DraftGeomUtils.geomType(edge) == "Circle":
        Radius = edge.Curve.Radius
        placement = FreeCAD.Placement(edge.Placement)
        #delta = edge.Curve.Center.sub(placement.Base)
        #placement.move(delta)
        if len(edge.Vertexes) > 1:
            ref = placement.multVec(FreeCAD.Vector(1,0,0))
            v1 = (edge.Vertexes[0].Point).sub(edge.Curve.Center)
            v2 = (edge.Vertexes[-1].Point).sub(edge.Curve.Center)
            a1 = -(DraftVecUtils.angle(v1,ref))
            a2 = -(DraftVecUtils.angle(v2,ref))
            FirstAngle = a1
            LastAngle = a2
    if angle <0:
        return [a2, a1]
    else:
        return [a1, a2]
    
def arcAngles(x1, y1, x2, y2, Cx, Cy, angle):
    if angle > 0:
        startAngle = atan2(y1 - Cy, x1 - Cx)
        if startAngle < 0.:
            startAngle = 6.28 + startAngle
                
        stopAngle = startAngle + radians(angle)  # STOP ANGLE
    else:
        startAngle = atan2(y2 - Cy, x2 - Cx)
        if startAngle < 0.:
            startAngle = 6.28 + startAngle

        stopAngle = startAngle + radians(abs(angle))  # STOP ANGLE
    #
    startAngle = float("%4.2f" % startAngle) - pi/2
    stopAngle = float("%4.2f" % stopAngle) - pi/2
    
    return [startAngle, stopAngle]

def shiftPointOnLine(x1, y1, x2, y2, distance):
    if x2 - x1 == 0:  # vertical line
        x_T1 = x1
        y_T1 = y1 - distance
    else:
        a = (y2 - y1) / (x2 - x1)
        if a == 0:  # horizontal line
            x_T1 = x1 - distance
            y_T1 = y1
        else:
            alfa = atan(a)
            #alfa = tan(a)

            x_T1 = x1 - distance * cos(alfa)
            y_T1 = y1 - distance * sin(alfa)

    return [x_T1, y_T1]

###
def getLine(layer, content, oType):
    layer=layer.replace('"','')
    data = []
    source = ''.join(content)
    source=source.replace('"','')
    #
    #data1 = re.findall(r'\({1}\s+\(start\s+([0-9\.-]*?)\s+([0-9\.-]*?)\)\s+\(end\s+([0-9\.-]*?)\s+([0-9\.-]*?)\)(\s+\(angle\s+[0-9\.-]*?\)\s+|\s+)\(layer\s+{0}\)\s+\(width\s+([0-9\.]*?)\)\)'.format(layer, oType), source, re.MULTILINE|re.DOTALL)
    data1 = re.findall(r'\({1}\s+\(start\s+([0-9\.-]*?)\s+([0-9\.-]*?)\)\s+\(end\s+([0-9\.-]*?)\s+([0-9\.-]*?)\)(\s+\(angle\s+[0-9\.-]*?\)\s+|\s+)\(layer\s+{0}\)\s+\(width\s+([0-9\.]*?)\)'.format(layer, oType), source, re.MULTILINE|re.DOTALL)
    #TBD fp_line kv7
    #say(data1)
    for i in data1:
        x1 = float(i[0])
        y1 = float(i[1]) * (-1)
        x2 = float(i[2])
        y2 = float(i[3]) * (-1)
        width = float(i[5])

        data.append([x1, y1, x2, y2, width])
    #
    return data

###
def getLineF(layer, content, oType, m=[0,0]):
    data = []
    source = ''.join(content)
    #
    #data1 = re.findall(r'\({1}\s+\(start\s+([0-9\.-]*?)\s+([0-9\.-]*?)\)\s+\(end\s+([0-9\.-]*?)\s+([0-9\.-]*?)\)(\s+\(angle\s+[0-9\.-]*?\)\s+|\s+)\(layer\s+{0}\)\s+\(width\s+([0-9\.]*?)\)\)'.format(layer, oType), source, re.MULTILINE|re.DOTALL)
    data1 = re.findall(r'\({1}\s+\(start\s+([0-9\.-]*?)\s+([0-9\.-]*?)\)\s+\(end\s+([0-9\.-]*?)\s+([0-9\.-]*?)\)(\s+\(angle\s+[0-9\.-]*?\)\s+|\s+)\(layer\s+{0}\)\s+\(width\s+([0-9\.]*?)\)'.format(layer, oType), source, re.MULTILINE|re.DOTALL)
    #say(data1)
    for i in data1:
        x1 = float(i[0])
        y1 = float(i[1]) * (-1)
        x2 = float(i[2])
        y2 = float(i[3]) * (-1)
        width = float(i[5])
        if [x1, y1] == [x2, y2]:
                        continue
        if m[0] != 0:
            x1 += m[0]
            x2 += m[0]
        if m[1] != 0:
            y1 += m[1]
            y2 += m[1]

        data.append([x1, y1, x2, y2, width])
    #
    return data

def getCircle(layer, content, oType):
    data = []
    #
    source = ''.join(content)
    layer=layer.replace('"','')
    source=source.replace('"','')
    #data1 = re.findall(r'\({1}\s+\(center\s+([0-9\.-]*?)\s+([0-9\.-]*?)\)\s+\(end\s+([0-9\.-]*?)\s+([0-9\.-]*?)\)\s+\(layer\s+{0}\)(\s+\(width\s+([0-9\.]*?)\)|)\)'.format(layer, oType), source, re.MULTILINE|re.DOTALL)
    data1 = re.findall(r'\({1}\s+\(center\s+([0-9\.-]*?)\s+([0-9\.-]*?)\)\s+\(end\s+([0-9\.-]*?)\s+([0-9\.-]*?)\)\s+\(layer\s+{0}\)(\s+\(width\s+([0-9\.]*?)\)|)'.format(layer, oType), source, re.MULTILINE|re.DOTALL)
    #say(source)
    #say(data1)
    for i in data1:
        xs = float(i[0])
        ys = float(i[1]) * (-1)
        x1 = float(i[2])
        y1 = float(i[3]) * (-1)

        radius = sqrt((xs - x1) ** 2 + (ys - y1) ** 2)

        if i[5] == '':
            width = 0.01
        else:
            width = float(i[5])

        data.append([xs, ys, radius, width])
    #
    #say(data)
    return data
###
def getCircleF(layer, content, oType, m=[0,0]):
    data = []
    #
    source = ''.join(content)
    #data1 = re.findall(r'\({1}\s+\(center\s+([0-9\.-]*?)\s+([0-9\.-]*?)\)\s+\(end\s+([0-9\.-]*?)\s+([0-9\.-]*?)\)\s+\(layer\s+{0}\)(\s+\(width\s+([0-9\.]*?)\)|)\)'.format(layer, oType), source, re.MULTILINE|re.DOTALL)
    data1 = re.findall(r'\({1}\s+\(center\s+([0-9\.-]*?)\s+([0-9\.-]*?)\)\s+\(end\s+([0-9\.-]*?)\s+([0-9\.-]*?)\)\s+\(layer\s+{0}\)(\s+\(width\s+([0-9\.]*?)\)|)'.format(layer, oType), source, re.MULTILINE|re.DOTALL)
    #say(source)
    #say(data1)
    for i in data1:
        xs = float(i[0])
        ys = float(i[1]) * (-1)
        x1 = float(i[2])
        y1 = float(i[3]) * (-1)

        radius = sqrt((xs - x1) ** 2 + (ys - y1) ** 2)

        if i[5] == '':
            width = 0.01
        else:
            width = float(i[5])
        if m[0] != 0:
            xs += m[0]
        if m[1] != 0:
            ys += m[1]

        data.append([xs, ys, radius, width])
    #
    #say(data)
    return data
###
def rotPoint(point, ref, angle):
    sinKAT = self.sinus(angle)
    cosKAT = self.cosinus(angle)

    x1R = (point[0] * cosKAT) - (point[1] * sinKAT) + ref[0]
    y1R = (point[0] * sinKAT) + (point[1] * cosKAT) + ref[1]
    return [x1R, y1R]

###
def rotPoint2(point, ref, angle):
    sinKAT = sinus(angle)
    cosKAT = cosinus(angle)
    x1R = ((point[0] - ref[0]) * cosKAT) - sinKAT * (point[1] - ref[1]) + ref[0]
    y1R = ((point[0] - ref[0]) * sinKAT) + cosKAT * (point[1] - ref[1]) + ref[1]
    return [x1R, y1R]
###
def getArc(layer, content, oType):
    data = []
    source = ''.join(content)
    source = source.replace('"','')
    layer = layer.replace('"','')
    #data1 = re.findall(r'\({1}\s+\(start\s+([0-9\.-]*?)\s+([0-9\.-]*?)\)\s+\(end\s+([0-9\.-]*?)\s+([0-9\.-]*?)\)\s+\(angle\s+([0-9\.-]*?)\)\s+\(layer\s+{0}\)(\s+\(width\s+([0-9\.]*?)\)|)\)'.format(layer, oType), source, re.MULTILINE|re.DOTALL)
    #(fp_arc (start 0.015 -0.03) (end 22.348 -2.772) (angle -17) (layer Edge.Cuts) (width 0.16))
    data1 = re.findall(r'\({1}\s+\(start\s+([0-9\.-]*?)\s+([0-9\.-]*?)\)\s+\(end\s+([0-9\.-]*?)\s+([0-9\.-]*?)\)\s+\(angle\s+([0-9\.-]*?)\)\s+\(layer\s+{0}\)(\s+\(width\s+([0-9\.]*?)|)\)'.format(layer, oType), source, re.MULTILINE|re.DOTALL)
    for i in data1:
        xs = float(i[0])
        ys = float(i[1])
        x1 = float(i[2])
        y1 = float(i[3])
        curve = float(i[4])
        if i[6].strip() != '':
            width = float(i[6])
        else:
            width = 0
        if abs(curve)==360: 
            [x2, y2] = [xs, ys]
        else:
            [x2, y2] = rotPoint2([x1, y1], [xs, ys], curve)
        data.append([x1, y1 * (-1), x2, y2 * (-1), curve, width])
    if len (data) == 0:
        # (fp_arc (start 20.570471 -9.181725) (mid 21.697398 -6.042909) (end 22.348 -2.772) (layer "Edge.Cuts") (width 0.16) (tstamp 30b75c25-1d2c-45e7-83e2-bb3be98f8f83))
        data2 = re.findall(r'\({1}\s+\(start\s+([0-9\.-]*?)\s+([0-9\.-]*?)\)\s+\(mid\s+([0-9\.-]*?)\s+([0-9\.-]*?)\)\s+\(end\s+([0-9\.-]*?)\s+([0-9\.-]*?)\)\s+\(layer\s+{0}\)\s+\(width\s+([0-9\.]*?)\)'.format(layer, oType), source, re.MULTILINE|re.DOTALL)
        #print(data2,data,data1)
        for i in data2:
            xs = float(i[0])
            ys = float(i[1])
            xm = float(i[2])
            ym = float(i[3])
            x1 = float(i[4])
            y1 = float(i[5])
            if i[6].strip() != '':
                width = float(i[6])
            else:
                width = 0
            data.append([xs, ys * (-1), xm, ym * (-1), x1, y1 * (-1), width])
    #
    return data

###
def getArcF(layer, content, oType, m=[0,0]):
    data = []
    #
    source = ''.join(content)
    #data1 = re.findall(r'\({1}\s+\(start\s+([0-9\.-]*?)\s+([0-9\.-]*?)\)\s+\(end\s+([0-9\.-]*?)\s+([0-9\.-]*?)\)\s+\(angle\s+([0-9\.-]*?)\)\s+\(layer\s+{0}\)(\s+\(width\s+([0-9\.]*?)\)|)\)'.format(layer, oType), source, re.MULTILINE|re.DOTALL)
    data1 = re.findall(r'\({1}\s+\(start\s+([0-9\.-]*?)\s+([0-9\.-]*?)\)\s+\(end\s+([0-9\.-]*?)\s+([0-9\.-]*?)\)\s+\(angle\s+([0-9\.-]*?)\)\s+\(layer\s+{0}\)(\s+\(width\s+([0-9\.]*?)|)\)'.format(layer, oType), source, re.MULTILINE|re.DOTALL)
    for i in data1:
        xs = float(i[0])
        ys = float(i[1])
        x1 = float(i[2])
        y1 = float(i[3])
        curve = float(i[4])
        if i[6].strip() != '':
            width = float(i[6])
        else:
            width = 0

        [x2, y2] = rotPoint2([x1, y1], [xs, ys], curve)
        y1 *= -1
        y2 *= -1
        if m[0] != 0:
            x1 += m[0]
            x2 += m[0]
        if m[1] != 0:
            y1 += m[1]
            y2 += m[1]

        data.append([x1, y1 , x2, y2, curve, width])
        #data.append([x1, y1 * (-1), x2, y2 * (-1), curve, width])
    #
    return data

def getModName(source):
    #say("here test0")
    #for x in source:
    #    x.encode('utf-8')
    #    say(x)

    #say("here test1")
    #model = ''.join(u)
    model = ''.join(source)
    #sayw("here")#;
    #sayw("here test2")
    match = re.search(r'((\(module\s)|(\(footprint\s))+(.+?)\(layer', model, re.MULTILINE|re.DOTALL)
    if match is not None:
        model_name = match.groups(0)[3]
        if ' (version' in model_name:
            model_name = model_name[:model_name.index(' (version')]
        model_name = model_name.replace('"','').rstrip()+'-'
    
    return model_name
###
def getwrlData(source):
    model = ''.join(source)
    wrl_pos=['0', '0', '0']
    if re.search(r'\(at\s+\(xyz+\s(.+?)\)', model, re.MULTILINE|re.DOTALL) is not None:
        pos_vrml = re.search(r'\(at\s+\(xyz+\s(.+?)\)', model, re.MULTILINE|re.DOTALL).groups(0)[0]
        #pos_vrml=pos_vrml[5:]
        wrl_pos=pos_vrml.split(" ")
        xp_vrml=wrl_pos[0]
        #say('alive')
        yp_vrml=wrl_pos[1]
        zp_vrml=wrl_pos[2]
        #say(wrl_pos);
        #wrl_pos=(xp_vrml,yp_vrml,zp_vrml)
    #say(wrl_pos);
    #    
    if re.search(r'\(offset\s+\(xyz+\s(.+?)\)', model, re.MULTILINE|re.DOTALL) is not None:
        pos_vrml = re.search(r'\(offset\s+\(xyz+\s(.+?)\)', model, re.MULTILINE|re.DOTALL).groups(0)[0]
        #pos_vrml=pos_vrml[5:]
        wrl_pos=pos_vrml.split(" ")
        xp_vrml=wrl_pos[0]
        #say('alive')
        yp_vrml=wrl_pos[1]
        zp_vrml=wrl_pos[2]
        #say(wrl_pos);
        #wrl_pos=(xp_vrml,yp_vrml,zp_vrml)
    #
    scale_vrml=['1', '1', '1']
    if re.search(r'\(scale\s+(.+?)\)', model, re.MULTILINE|re.DOTALL) is not None:
        sc_vrml = re.search(r'\(scale\s+(.+?)\)', model, re.MULTILINE|re.DOTALL).groups(0)[0]
        sc_vrml=sc_vrml[5:]
        scale_vrml=sc_vrml.split(" ")
        xsc_vrml=scale_vrml[0]
        ysc_vrml=scale_vrml[1]
        zsc_vrml=scale_vrml[2]        
        #say(scale_vrml);
    #say(scale_vrml);
    #
    rot_wrl=['0', '0', '0']
    zrot_vrml=''
    if re.search(r'\(rotate\s+(.+?)\)', model, re.MULTILINE|re.DOTALL) is not None:
        rot_vrml = re.search(r'\(rotate\s+(.+?)\)', model, re.MULTILINE|re.DOTALL).groups(0)[0]
        rot_vrml=rot_vrml[5:]
        rot_wrl=rot_vrml.split(" ")
        xrot_vrml=rot_wrl[0]
        yrot_vrml=rot_wrl[1]
        zrot_vrml=rot_wrl[2]
        #say(rot_wrl);
    else:
        rotz_vrml=False
    #say("hereA")
    #if rotz_vrml:
    #    zrot_vrml=zrot_vrml
    #    #say("rotz:"+rotz)
    #    ##rotz=rotz[5:]
    #    #say("rotz:"+rotz)
    #    ##temp=rotz.split(" ")
    #    #say("rotz temp:"+temp[2])
    #    ##rotz=temp[2]
    #    #say("rotate vrml: "+rotz)
    if zrot_vrml=='':
        zrot_vrml=0.0
    else:
        zrot_vrml=float(zrot_vrml)
    rot=zrot_vrml  #adding vrml module z-rotation
    #say(rot_wrl);
    return wrl_pos, scale_vrml, rot_wrl

def getwrlRot(source):
    model = ''.join(source)
    if re.search(r'\(rotate\s+(.+?)\)', model, re.MULTILINE|re.DOTALL) is not None:
        rotz_vrml = re.search(r'\(rotate\s+(.+?)\)', model, re.MULTILINE|re.DOTALL).groups(0)[0]
    else:
        rotz_vrml=False
    #say("hereA")
    rotz=''
    if rotz_vrml:
        rotz=rotz_vrml
        #say("rotz:"+rotz)
        rotz=rotz[5:]
        #say("rotz:"+rotz)
        temp=rotz.split(" ")
        #say("rotz temp:"+temp[2])
        rotz=temp[2]
        #say("rotate vrml: "+rotz)
    if rotz=='':
        rotz=0.0
    else:
        rotz=float(rotz)
    rot=rotz  #adding vrml module z-rotation
    return rot

###
def getPadsList(content):
    pads = []
    #
    model = ''.join(content)
    #model_name = re.search(r'\(module\s+(.+?)\(layer', model, re.MULTILINE|re.DOTALL).groups(0)[0]
    #say(model_name)

    found = re.findall(r'\(pad .*', model, re.MULTILINE|re.DOTALL)
    #found_fp = re.findall(r'\(fp_poly .*', model, re.MULTILINE|re.DOTALL)
    zones = re.findall(r'\(zone .*', model, re.MULTILINE|re.DOTALL)
    if len(zones):
        zones = zones[0].strip().split('(zone ')
        ## TBD create sketch for zones
        #print(zones)
        #for z in zones:
        #    if z != '':
    if len(found):
        found = found[0].strip().split('(pad ')
        #removing extra keepout zones
        for count, p in enumerate(found):
            if '(zone ' in p:
                #print (len(p))
                idx = p.index("(zone ")
                z = p[0:idx]
                found[count] = z
        for j in found:
            if j != '':
                [x, y, rot] = re.search(r'\(at\s+([0-9\.-]*?)\s+([0-9\.-]*?)(\s+[0-9\.-]*?|)\)', j).groups()
                pType= re.search(r'^.*?\s+([a-zA-Z_]+?)\s+', j).groups(0)[0]  # pad type - SMD/thru_hole/connect
                pShape = re.search(r'^.+?\s+.+?\s+([a-zA-Z_]+?)\s+', j).groups(0)[0]  # pad shape - circle/rec/oval/trapezoid/roundrect
                pRoundG = re.search(r'\(roundrect_rratio\s+([0-9\.-]+?)\)', j)
                if pRoundG is not None:
                    pRound = pRoundG.groups(0)[0]
                else:
                    pRound=None
                #pCircleG = re.search(r'\(gr_circle+.+?\)\)', j, re.MULTILINE|re.DOTALL)   #re.search(r'\(gr_circle\s.+(?=\)\)$)', j)  #(?<=^startstr).+(?=stopstr$)
                pCircleG = re.search(r'(\(gr_circle)\s+(.+?)\)\)', j) #, re.MULTILINE|re.DOTALL)   #re.search(r'\(gr_circle\s.+(?=\)\)$)', j)  #(?<=^startstr).+(?=stopstr$)
                #print(pCircleG);print(j);stop
                if pCircleG is not None:
                    pCircleG = pCircleG.groups(0)[1].split(')')
                    pCircleG[1]=pCircleG[1].lstrip(' ')
                    pCircleG[2]=pCircleG[2].lstrip(' ')
                    #say(pCircleG);stop
                else:
                    pCircleG=None                
                #sayw(pShape)
                #sayw(pRound)
                [dx, dy] = re.search(r'\(size\s+([0-9\.-]+?)\s+([0-9\.-]+?)\)', j).groups(0)  #
                try:
                    layers = re.search(r'\(layers\s+(.+?)\)', j).groups(0)[0]  #
                except:
                    layers = 'F.SilkS'
                    #layers = None
                    sayerr('NO LAYERS on PAD') #test utf-8 test pads
                # print(layers)
                # stop
                data = re.search(r'\(drill(\s+oval\s+|\s+)(.*?)(\s+[-0-9\.]*?|)(\s+\(offset\s+(.*?)\s+(.*?)\)|)\)', j)
                data_off = re.search(r'\(offset\s+([0-9\.-]+?)\s+([0-9\.-]+?)\)', j)
                pnts = re.search(r'\(gr_poly\s\(pts(.*?)\)\s\(width', j, re.MULTILINE|re.DOTALL)
                #pnts_nt = re.search(r'\(fp_poly\s\(pts(.*?)\)\s\(width', j, re.MULTILINE|re.DOTALL)
                #if pnts_nt is not None:
                #    pnts = pnts_nt #re.search(r'\(fp_poly\s\(pts(.*?)\)\s\(width', j, re.MULTILINE|re.DOTALL)
                #    pShape = 'NetTie'
                anchor = re.search(r'\(anchor\s(.*?)\)\)', j)
                if anchor is not None:
                    anchor=anchor.groups()[0]
                #print anchor
                #if pnts is not None:
                #    print pnts.groups(0)[0].split('(xy')
                #
                x = float(x)
                y = float(y) * (-1)
                dx = float(dx)
                dy = float(dy)
                if rot == '' or len(rot.strip(' '))==0:
                    rot = 0.0
                else:
                    #print rot
                    rot = float(rot)
                #print(pType)
                if pType == 'smd' or pType == 'connect' or data is None:
                    drill_x = 0.0
                    drill_y = 0.0
                    hType = None
                    if data_off is None:
                        [xOF, yOF] = [0.0, 0.0]
                    else:
                        data_off = data_off.groups()
                        if not data_off[0] or data_off[0].strip() == '':
                            xOF = 0.0
                        else:
                            xOF = float(data_off[0])

                        if not data_off[1] or data_off[1].strip() == '':
                            yOF = 0.0
                        else:
                            yOF = float(data_off[1])
                else:
                    data = data.groups()
                    hType = data[0]
                    if hType.strip() == '':
                        hType = 'circle'

                    drill_x = float(data[1]) #/ 2.0
                    if not data[2] or data[2].strip() == '':
                        drill_y=drill_x
                    else:
                        drill_y = float(data[2]) #/ 2.0
                    #drill_y=drill_x

                    if not data[4] or data[4].strip() == '':
                        xOF = 0.0
                    else:
                        xOF = float(data[4])

                    if not data[5] or data[5].strip() == '':
                        yOF = 0.0
                    else:
                        yOF = float(data[5])
                ##
                #say(data)
                pads.append({'x': x, 'y': y, 'rot': rot, 'padType': pType, 'padShape': pShape, 'rx': drill_x, 'ry': drill_y, 'dx': dx, 'dy': dy, \
                             'holeType': hType, 'xOF': xOF, 'yOF': yOF, 'layers': layers, 'points': pnts, 'anchor': anchor, 'rratio': pRound, 'geomC':pCircleG})

    #say(pads)
    #
    return pads
###
###
def getPolyList(content):
    pads = []
    #
    model = ''.join(content)
    #model_name = re.search(r'\(module\s+(.+?)\(layer', model, re.MULTILINE|re.DOTALL).groups(0)[0]
    #say(model_name)
    fp_pnts = []
    width = 0.16
    found = re.findall(r'\(fp_poly.*', model, re.MULTILINE|re.DOTALL)
    if len(found):
        found = found[0].strip().split('(fp_poly ')
        for j in found:
            #print('j',j)
            if j != '':
                try:
                    layers = re.search(r'\(layer\s+(.+?)\)', j).groups(0)[0]  #
                except:
                    layers = 'F.SilkS'
                    #layers = None
                    sayerr('NO LAYER on NetTie') #test utf-8 test pads
                #print(layers)
                # stop
                #pnts = re.search(r'\(fp_poly\s\(pts(.*?)\)\s\(width', j, re.MULTILINE|re.DOTALL)
                pnts = re.search(r'\(pts(.*?)(.*?)\(width', j, re.MULTILINE|re.DOTALL)
                #pnts_nt = re.search(r'\(fp_poly\s\(pts(.*?)\)\s\(width', j, re.MULTILINE|re.DOTALL)
                #if pnts_nt is not None:
                #    pnts = pnts_nt #re.search(r'\(fp_poly\s\(pts(.*?)\)\s\(width', j, re.MULTILINE|re.DOTALL)
                #    pShape = 'NetTie'
                #print('pnts',pnts.group())
                width = re.search(r'\(width(.*?)\)', j, re.MULTILINE|re.DOTALL)
                width = float(width[0].strip().split('(width ')[1].strip(')'))
                #print('width',width)
                fp_pnts.append({'layers': layers, 'points': pnts})

    #say(fp_pnts)
    #
    return fp_pnts, width
###

def makePoint(self, x, y):
    wir = []
    wir.append(Part.Point(FreeCAD.Base.Vector(x, y, 0)))
    mainObj = Part.Shape(wir)
    return mainObj
###
def makeFace(mainObj):
    return Part.Face(mainObj)
###

def cutHole(mainObj, hole):
    if hole[2] > min_val:
        hole = [Part.Circle(FreeCAD.Vector(hole[0], hole[1]), FreeCAD.Vector(0, 0, 1), hole[2]).toShape()]
        hole = Part.Wire(hole)
        hole = Part.Face(hole)

        mainObj = mainObj.cut(hole)
    return mainObj
###
def cutObj(mainObj, hole):
    mainObj = mainObj.cut(hole)
    return mainObj
###
def createCircle(x, y, r, w=0):

    if w > min_val:
        mainObj = Part.Wire([Part.Circle(FreeCAD.Vector(x, y), FreeCAD.Vector(0, 0, 1), r + w / 2.).toShape()])
        mainObj = makeFace(mainObj)
        mainObj = cutHole(mainObj, [x, y, r - w / 2.])

        return mainObj
    else:
        mainObj = [Part.Circle(FreeCAD.Vector(x, y), FreeCAD.Vector(0, 0, 1), r).toShape()]

        return makeFace(Part.Wire(mainObj))

###
def createArc_OLD(p1, p2, curve, width=0.02, cap='round'):
    try:
        wir = []
        if width <= 0:
            width = 0.02
        width /= 2.
        [x3, y3] = arcMidPoint(p1, p2, curve)
        [xs, ys] = arcCenter(p1[0], p1[1], p2[0], p2[1], x3, y3)
        ##
        #a = (ys - p1[1]) / (xs - p1[0])
        [xT_1, yT_1] = shiftPointOnLine(p1[0], p1[1], xs, ys, width)
        [xT_4, yT_4] = shiftPointOnLine(p1[0], p1[1], xs, ys, -width)
        ###
        [xT_2, yT_2] = rotPoint2([xT_1, yT_1], [xs, ys], curve)
        [xT_5, yT_5] = rotPoint2([xT_4, yT_4], [xs, ys], curve)
        ########
        ########
        wir = []
        ## outer arc
        [xT_3, yT_3] = arcMidPoint([xT_1, yT_1], [xT_2, yT_2], curve)
        wir.append(Part.Arc(FreeCAD.Base.Vector(xT_1, yT_1, 0), FreeCAD.Base.Vector(xT_3, yT_3, 0), FreeCAD.Base.Vector(xT_2, yT_2, 0)))
        ## inner arc
        [xT_6, yT_6] = arcMidPoint([xT_4, yT_4], [xT_5, yT_5], curve)
        wir.append(Part.Arc(FreeCAD.Base.Vector(xT_4, yT_4, 0), FreeCAD.Base.Vector(xT_6, yT_6, 0), FreeCAD.Base.Vector(xT_5, yT_5, 0)))
        ##
        if cap == 'flat':
            wir.append(PLine(FreeCAD.Base.Vector(xT_1, yT_1, 0), FreeCAD.Base.Vector(xT_4, yT_4, 0)))
            wir.append(PLine(FreeCAD.Base.Vector(xT_2, yT_2, 0), FreeCAD.Base.Vector(xT_5, yT_5, 0)))
        else:
            #wir.append(PLine(FreeCAD.Base.Vector(xT_1, yT_1, 0), FreeCAD.Base.Vector(xT_4, yT_4, 0)))
            #wir.append(PLine(FreeCAD.Base.Vector(xT_2, yT_2, 0), FreeCAD.Base.Vector(xT_5, yT_5, 0)))
            #start
            if xs - p1[0] == 0:  # vertical line
                if curve > 0:
                    [xT_7, yT_7] = arcMidPoint([xT_1, yT_1], [xT_4, yT_4], 180)
                else:
                    [xT_7, yT_7] = arcMidPoint([xT_1, yT_1], [xT_4, yT_4], -180)
            else:
                a = (ys - p1[1]) / (xs - p1[0])

                if a == 0:  # horizontal line
                    if curve > 0:
                        [xT_7, yT_7] = arcMidPoint([xT_1, yT_1], [xT_4, yT_4], 180)
                    else:
                        [xT_7, yT_7] = arcMidPoint([xT_1, yT_1], [xT_4, yT_4], -180)
                    pass
                else:
                    #a = (ys - p1[1]) / (xs - p1[0])
                    if curve > 0:
                        if a > 0:
                            if xT_1 > xs:
                                [xT_7, yT_7] = arcMidPoint([xT_1, yT_1], [xT_4, yT_4], 180)
                            else:
                                [xT_7, yT_7] = arcMidPoint([xT_1, yT_1], [xT_4, yT_4], -180)
                        else:
                            if xT_1 > xs:
                                [xT_7, yT_7] = arcMidPoint([xT_1, yT_1], [xT_4, yT_4], 180)
                            else:
                                [xT_7, yT_7] = arcMidPoint([xT_1, yT_1], [xT_4, yT_4], -180)
                    else:
                        if a > 0:
                            if xT_1 > xs:
                                [xT_7, yT_7] = arcMidPoint([xT_1, yT_1], [xT_4, yT_4], -180)
                            else:
                                [xT_7, yT_7] = arcMidPoint([xT_1, yT_1], [xT_4, yT_4], 180)
                        else:
                            if xT_1 > xs:
                                [xT_7, yT_7] = arcMidPoint([xT_1, yT_1], [xT_4, yT_4], -180)
                            else:
                                [xT_7, yT_7] = arcMidPoint([xT_1, yT_1], [xT_4, yT_4], 180)

            wir.append(Part.Arc(FreeCAD.Base.Vector(xT_1, yT_1, 0), FreeCAD.Base.Vector(xT_7, yT_7, 0), FreeCAD.Base.Vector(xT_4, yT_4, 0)))

            #end
            #b = (ys - p2[1]) / (xs - p2[0])

            if curve > 0:
                if xT_2 > xs:
                    if xT_2 >= xT_5:
                        [xT_8, yT_8] = arcMidPoint([xT_2, yT_2], [xT_5, yT_5], 180)
                    else:
                        [xT_8, yT_8] = arcMidPoint([xT_2, yT_2], [xT_5, yT_5], -180)
                else:
                    if xT_2 >= xT_5:
                        [xT_8, yT_8] = arcMidPoint([xT_2, yT_2], [xT_5, yT_5], -180)
                    else:
                        [xT_8, yT_8] = arcMidPoint([xT_2, yT_2], [xT_5, yT_5], 180)
            else:
                if xT_2 > xs:
                    if xT_2 >= xT_5:
                        [xT_8, yT_8] = arcMidPoint([xT_2, yT_2], [xT_5, yT_5], -180)
                    else:
                        [xT_8, yT_8] = arcMidPoint([xT_2, yT_2], [xT_5, yT_5], 180)
                else:
                    if xT_2 >= xT_5:
                        [xT_8, yT_8] = arcMidPoint([xT_2, yT_2], [xT_5, yT_5], 180)
                    else:
                        [xT_8, yT_8] = arcMidPoint([xT_2, yT_2], [xT_5, yT_5], -180)

            wir.append(Part.Arc(FreeCAD.Base.Vector(xT_2, yT_2, 0), FreeCAD.Base.Vector(xT_8, yT_8, 0), FreeCAD.Base.Vector(xT_5, yT_5, 0)))

        ####
        mainObj = Part.Shape(wir)
        mainObj = Part.Wire(mainObj.Edges)
        return makeFace(mainObj)

    except Exception as e:
        FreeCAD.Console.PrintWarning(u"{0}\n".format(e))

###
###
def createArc(p1, p2, curve, width=0.02, cap='round'):
    try:
        #wir = []
        # create edges
        edges = []
        if width <= 0:
            width = 0.02
        width /= 2.
        [x3, y3] = arcMidPoint(p1, p2, curve)
        [xs, ys] = arcCenter(p1[0], p1[1], p2[0], p2[1], x3, y3)
        ##
        #a = (ys - p1[1]) / (xs - p1[0])
        [xT_1, yT_1] = shiftPointOnLine(p1[0], p1[1], xs, ys, width)
        [xT_4, yT_4] = shiftPointOnLine(p1[0], p1[1], xs, ys, -width)
        ###
        [xT_2, yT_2] = rotPoint2([xT_1, yT_1], [xs, ys], curve)
        [xT_5, yT_5] = rotPoint2([xT_4, yT_4], [xs, ys], curve)
        ########
        ########
        wir = []
        ## outer arc
        [xT_3, yT_3] = arcMidPoint([xT_1, yT_1], [xT_2, yT_2], curve)
        edges.append(Part.Edge(Part.Arc(FreeCAD.Base.Vector(xT_1, yT_1, 0), FreeCAD.Base.Vector(xT_3, yT_3, 0), FreeCAD.Base.Vector(xT_2, yT_2, 0))))
        #wir.append(Part.Arc(FreeCAD.Base.Vector(xT_1, yT_1, 0), FreeCAD.Base.Vector(xT_3, yT_3, 0), FreeCAD.Base.Vector(xT_2, yT_2, 0)))
        ## inner arc
        [xT_6, yT_6] = arcMidPoint([xT_4, yT_4], [xT_5, yT_5], curve)
        edges.append(Part.Edge(Part.Arc(FreeCAD.Base.Vector(xT_4, yT_4, 0), FreeCAD.Base.Vector(xT_6, yT_6, 0), FreeCAD.Base.Vector(xT_5, yT_5, 0))))
        #wir.append(Part.Arc(FreeCAD.Base.Vector(xT_4, yT_4, 0), FreeCAD.Base.Vector(xT_6, yT_6, 0), FreeCAD.Base.Vector(xT_5, yT_5, 0)))
        ##
        if cap == 'flat':
            edges.append(Part.Edge(PLine(FreeCAD.Base.Vector(xT_1, yT_1, 0), FreeCAD.Base.Vector(xT_4, yT_4, 0))))
            edges.append(Part.Edge(PLine(FreeCAD.Base.Vector(xT_2, yT_2, 0), FreeCAD.Base.Vector(xT_5, yT_5, 0))))
            #wir.append(PLine(FreeCAD.Base.Vector(xT_1, yT_1, 0), FreeCAD.Base.Vector(xT_4, yT_4, 0)))
            #wir.append(PLine(FreeCAD.Base.Vector(xT_2, yT_2, 0), FreeCAD.Base.Vector(xT_5, yT_5, 0)))
        else:
            #wir.append(PLine(FreeCAD.Base.Vector(xT_1, yT_1, 0), FreeCAD.Base.Vector(xT_4, yT_4, 0)))
            #wir.append(PLine(FreeCAD.Base.Vector(xT_2, yT_2, 0), FreeCAD.Base.Vector(xT_5, yT_5, 0)))
            #start
            if xs - p1[0] == 0:  # vertical line
                if curve > 0:
                    [xT_7, yT_7] = arcMidPoint([xT_1, yT_1], [xT_4, yT_4], 180)
                else:
                    [xT_7, yT_7] = arcMidPoint([xT_1, yT_1], [xT_4, yT_4], -180)
            else:
                a = (ys - p1[1]) / (xs - p1[0])

                if a == 0:  # horizontal line
                    if curve > 0:
                        [xT_7, yT_7] = arcMidPoint([xT_1, yT_1], [xT_4, yT_4], 180)
                    else:
                        [xT_7, yT_7] = arcMidPoint([xT_1, yT_1], [xT_4, yT_4], -180)
                    pass
                else:
                    #a = (ys - p1[1]) / (xs - p1[0])
                    if curve > 0:
                        if a > 0:
                            if xT_1 > xs:
                                [xT_7, yT_7] = arcMidPoint([xT_1, yT_1], [xT_4, yT_4], 180)
                            else:
                                [xT_7, yT_7] = arcMidPoint([xT_1, yT_1], [xT_4, yT_4], -180)
                        else:
                            if xT_1 > xs:
                                [xT_7, yT_7] = arcMidPoint([xT_1, yT_1], [xT_4, yT_4], 180)
                            else:
                                [xT_7, yT_7] = arcMidPoint([xT_1, yT_1], [xT_4, yT_4], -180)
                    else:
                        if a > 0:
                            if xT_1 > xs:
                                [xT_7, yT_7] = arcMidPoint([xT_1, yT_1], [xT_4, yT_4], -180)
                            else:
                                [xT_7, yT_7] = arcMidPoint([xT_1, yT_1], [xT_4, yT_4], 180)
                        else:
                            if xT_1 > xs:
                                [xT_7, yT_7] = arcMidPoint([xT_1, yT_1], [xT_4, yT_4], -180)
                            else:
                                [xT_7, yT_7] = arcMidPoint([xT_1, yT_1], [xT_4, yT_4], 180)

            edges.append(Part.Edge(Part.Arc(FreeCAD.Base.Vector(xT_1, yT_1, 0), FreeCAD.Base.Vector(xT_7, yT_7, 0), FreeCAD.Base.Vector(xT_4, yT_4, 0))))
            #wir.append(Part.Arc(FreeCAD.Base.Vector(xT_1, yT_1, 0), FreeCAD.Base.Vector(xT_7, yT_7, 0), FreeCAD.Base.Vector(xT_4, yT_4, 0)))

            #end
            #b = (ys - p2[1]) / (xs - p2[0])

            if curve > 0:
                if xT_2 > xs:
                    if xT_2 >= xT_5:
                        [xT_8, yT_8] = arcMidPoint([xT_2, yT_2], [xT_5, yT_5], 180)
                    else:
                        [xT_8, yT_8] = arcMidPoint([xT_2, yT_2], [xT_5, yT_5], -180)
                else:
                    if xT_2 >= xT_5:
                        [xT_8, yT_8] = arcMidPoint([xT_2, yT_2], [xT_5, yT_5], -180)
                    else:
                        [xT_8, yT_8] = arcMidPoint([xT_2, yT_2], [xT_5, yT_5], 180)
            else:
                if xT_2 > xs:
                    if xT_2 >= xT_5:
                        [xT_8, yT_8] = arcMidPoint([xT_2, yT_2], [xT_5, yT_5], -180)
                    else:
                        [xT_8, yT_8] = arcMidPoint([xT_2, yT_2], [xT_5, yT_5], 180)
                else:
                    if xT_2 >= xT_5:
                        [xT_8, yT_8] = arcMidPoint([xT_2, yT_2], [xT_5, yT_5], 180)
                    else:
                        [xT_8, yT_8] = arcMidPoint([xT_2, yT_2], [xT_5, yT_5], -180)

            edges.append(Part.Edge(Part.Arc(FreeCAD.Base.Vector(xT_2, yT_2, 0), FreeCAD.Base.Vector(xT_8, yT_8, 0), FreeCAD.Base.Vector(xT_5, yT_5, 0))))
            #wir.append(Part.Arc(FreeCAD.Base.Vector(xT_2, yT_2, 0), FreeCAD.Base.Vector(xT_8, yT_8, 0), FreeCAD.Base.Vector(xT_5, yT_5, 0)))

        ####
        sortedEdges = Part.__sortEdges__(edges)
        wire = Part.Wire(sortedEdges)
        return Part.Face(wire)
        # Part.show(wObj)
        # mainObj = Part.Shape(wir)
        # mainObj = Part.Wire(mainObj.Edges)
        # return makeFace(mainObj)

    except Exception as e:
        FreeCAD.Console.PrintWarning(u"{0}\n".format(e))

###

###
def addArc_3(p1, p2, curve, width=0, cap='round'):
    #print curve, ' arc angle' 
    if abs(curve) == 360:
        #print p1
        #print p2
        r = sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)
        #print r
        return createCircle(p1[0], p1[1], r, width)
    else:
        return createArc(p1, p2, curve, width, cap)

###
def addLine_2(x1, y1, x2, y2, width=0.01):
    if x1 == x2 and y1 == y2:
        return makePoint(x1, y1, 0)
    else:
        return createLine(x1, y1, x2, y2, width)
###
def addCircle_2(x, y, r, w=0):
    return createCircle(x, y, r, w)
###
def createLine(x1, y1, x2, y2, width=0.01):
    #say("create line routine")
    z_silk_offset=0.01
    if width <= 0:
        width = 0.01

    # line length
    length = sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    # angle of inclination
    if x1 > x2:
        iang = degrees(atan2(y1 - y2, x1 - x2)) - 90
    else:
        iang = degrees(atan2(y2 - y1, x2 - x1)) - 90
    if x1 > x2:
        iang += 180

    # radius of curvature at both ends of the path
    r = width / 2.

    # create edges
    edges = []
    edges.append(Part.Edge(PLine(FreeCAD.Base.Vector(0 - r, 0, 0), FreeCAD.Base.Vector(0 - r, length, 0))))
    edges.append(Part.Edge(PLine(FreeCAD.Base.Vector(0 + r, 0, 0), FreeCAD.Base.Vector(0 + r, length, 0))))
    
    # create wire
    #wir = []
    #wir.append(PLine(FreeCAD.Base.Vector(0 - r, 0, 0), FreeCAD.Base.Vector(0 - r, length, 0)))
    #wir.append(PLine(FreeCAD.Base.Vector(0 + r, 0, 0), FreeCAD.Base.Vector(0 + r, length, 0)))

    p1 = [0 - r, 0]
    p2 = [0, 0 - r]
    p3 = [0 + r, 0]
    edges.append(Part.Edge(Part.Arc(FreeCAD.Base.Vector(p1[0], p1[1], 0), FreeCAD.Base.Vector(p2[0], p2[1], 0), FreeCAD.Base.Vector(p3[0], p3[1], 0))))
    #wir.append(Part.Arc(FreeCAD.Base.Vector(p1[0], p1[1], 0), FreeCAD.Base.Vector(p2[0], p2[1], 0), FreeCAD.Base.Vector(p3[0], p3[1], 0)))

    p1 = [0 - r, length]
    p2 = [0, length + r]
    p3 = [0 + r, length]
    edges.append(Part.Edge(Part.Arc(FreeCAD.Base.Vector(p1[0], p1[1], 0), FreeCAD.Base.Vector(p2[0], p2[1], 0), FreeCAD.Base.Vector(p3[0], p3[1], 0))))
    #wir.append(Part.Arc(FreeCAD.Base.Vector(p1[0], p1[1], 0), FreeCAD.Base.Vector(p2[0], p2[1], 0), FreeCAD.Base.Vector(p3[0], p3[1], 0)))
    sortedEdges = Part.__sortEdges__(edges)
    
    #mainObj = Part.Shape(wir)
    ##mainObj = wir.toShape()
    ## sayw(wir)
    #mainObj = Part.Wire(mainObj.Edges)
    ##mainObj = Part.Face(mainObj)
    #mainObj=makeFace(Part.Wire(mainObj))
    ##mainObj = Part.Wire(wir)
    ##mainObj = Part.Face(mainObj)
    wire = Part.Wire(sortedEdges)
    mainObj = Part.Face(wire)
    #Part.show(mainObj)
    
    pos_1 = FreeCAD.Base.Vector(x1, y1, z_silk_offset) #z offset Front Silk 0.1
    center = FreeCAD.Base.Vector(0, 0, 0)
    rot = FreeCAD.Rotation(FreeCAD.Vector(0, 0, 1), iang)
    mainObj.Placement = FreeCAD.Base.Placement(pos_1, rot, center)
    #Part.show(mainObj)
    #stop
    
    return mainObj
###
def addPadLong2(x, y, dx, dy, perc, typ, z_off, type=None, ratio=None):
              #pad center x,y pad dimension dx,dy, type, z offset
    #if ratio is not None:
    #    sayw(type);sayerr(ratio)
    dx=dx/2.
    dy=dy/2.
    curve = 90.
    if typ == 0:  # %
        if perc > 100.:
            perc == 100.
        if dx > dy:
            e = dy * perc / 100.
        else:
            e = dx * perc / 100.
    else:  # mm
        e = perc
    if ratio is not None:
        #rratio=r1/min(sx,sy)
        e = float(ratio) * 2.0 * min(dx,dy)
        #sayerr(e)
    p1 = [x - dx + e, y - dy, z_off]
    p2 = [x + dx - e, y - dy, z_off]
    p3 = [x + dx, y - dy + e, z_off]
    p4 = [x + dx, y + dy - e, z_off]
    p5 = [x + dx - e, y + dy, z_off]
    p6 = [x - dx + e, y + dy, z_off]
    p7 = [x - dx, y + dy - e, z_off]
    p8 = [x - dx, y - dy + e, z_off]
    #
    points = []
    if p1 != p2:
        points.append(PLine(FreeCAD.Base.Vector(p1[0], p1[1], z_off), FreeCAD.Base.Vector(p2[0], p2[1], z_off)))
    if p2 != p3:
        p9 = arcMidPoint(p2, p3, curve)
        points.append(Part.Arc(FreeCAD.Base.Vector(p2[0], p2[1], z_off), FreeCAD.Base.Vector(p9[0], p9[1], z_off), FreeCAD.Base.Vector(p3[0], p3[1], z_off)))
    if p3 != p4:
        points.append(PLine(FreeCAD.Base.Vector(p3[0], p3[1], z_off), FreeCAD.Base.Vector(p4[0], p4[1], z_off)))
    if p4 != p5:
        p10 = arcMidPoint(p4, p5, curve)
        points.append(Part.Arc(FreeCAD.Base.Vector(p4[0], p4[1], z_off), FreeCAD.Base.Vector(p10[0], p10[1], z_off), FreeCAD.Base.Vector(p5[0], p5[1], z_off)))
    if p5 != p6:
        points.append(PLine(FreeCAD.Base.Vector(p5[0], p5[1], z_off), FreeCAD.Base.Vector(p6[0], p6[1], z_off)))
    if p6 != p7:
        p11 = arcMidPoint(p6, p7, curve)
        points.append(Part.Arc(FreeCAD.Base.Vector(p6[0], p6[1], z_off), FreeCAD.Base.Vector(p11[0], p11[1], z_off), FreeCAD.Base.Vector(p7[0], p7[1], z_off)))
    if p7 != p8:
        points.append(PLine(FreeCAD.Base.Vector(p7[0], p7[1], z_off), FreeCAD.Base.Vector(p8[0], p8[1], z_off)))
    if p8 != p1:
        p12 = arcMidPoint(p8, p1, curve)
        points.append(Part.Arc(FreeCAD.Base.Vector(p8[0], p8[1], z_off), FreeCAD.Base.Vector(p12[0], p12[1], z_off), FreeCAD.Base.Vector(p1[0], p1[1], z_off)))

    if dx==dy and type != "rect" and type != "roundrect": # "circle"
        r=dx
        obj=[Part.Circle(FreeCAD.Vector(x, y, z_off), FreeCAD.Vector(0, 0, 1), r).toShape()]
        obj=Part.Wire(obj) #maui evaluate FC0.17
        #obj=Draft.makeWire(obj,closed=True,face=False,support=None)   # create the wire
        #Part.show(obj)
        #stop
    else:
        # obj = Part.Shape(points)  #maui evaluate FC0.17
        # #obj=[points.toShape()]
        # obj = Part.Wire(obj.Edges) #maui evaluate FC0.17
        objs=[]  # asm3 Links compatible way
        for e in points:
            objs.append(e.toShape())
        obj = Part.Wire(objs)
        #obj=Draft.makeWire(obj.Edges,closed=True,face=False,support=None)   # create the wire

    #if hole==0:
    #    obj = makeFace(obj)
    ###return makeFace(obj)
    ##list=[]
    ##list.append(obj)
    ##obj1=Part.makeCompound(list)
    ##return obj1
    return obj

###
def addPadLong(x, y, dx, dy, perc, typ, z_off):
              # center x,y dimension x,y, type, z offset
    dx=dx/2
    dy=dy/2
    curve = 90.
    if typ == 0:  # %
        if perc > 100.:
            perc == 100.
        if dx > dy:
            e = dy * perc / 100.
        else:
            e = dx * perc / 100.
    else:  # mm
        e = perc
    p1 = [x - dx + e, y - dy, z_off]
    p2 = [x + dx - e, y - dy, z_off]
    p3 = [x + dx, y - dy + e, z_off]
    p4 = [x + dx, y + dy - e, z_off]
    p5 = [x + dx - e, y + dy, z_off]
    p6 = [x - dx + e, y + dy, z_off]
    p7 = [x - dx, y + dy - e, z_off]
    p8 = [x - dx, y - dy + e, z_off]
    #
    points = []
    if p1 != p2:
        points.append(PLine(FreeCAD.Base.Vector(p1[0], p1[1], z_off), FreeCAD.Base.Vector(p2[0], p2[1], z_off)))
    if p2 != p3:
        p9 = arcMidPoint(p2, p3, curve)
        points.append(Part.Arc(FreeCAD.Base.Vector(p2[0], p2[1], z_off), FreeCAD.Base.Vector(p9[0], p9[1], z_off), FreeCAD.Base.Vector(p3[0], p3[1], z_off)))
    if p3 != p4:
        points.append(PLine(FreeCAD.Base.Vector(p3[0], p3[1], z_off), FreeCAD.Base.Vector(p4[0], p4[1], z_off)))
    if p4 != p5:
        p10 = arcMidPoint(p4, p5, curve)
        points.append(Part.Arc(FreeCAD.Base.Vector(p4[0], p4[1], z_off), FreeCAD.Base.Vector(p10[0], p10[1], z_off), FreeCAD.Base.Vector(p5[0], p5[1], z_off)))
    if p5 != p6:
        points.append(PLine(FreeCAD.Base.Vector(p5[0], p5[1], z_off), FreeCAD.Base.Vector(p6[0], p6[1], z_off)))
    if p6 != p7:
        p11 = arcMidPoint(p6, p7, curve)
        points.append(Part.Arc(FreeCAD.Base.Vector(p6[0], p6[1], z_off), FreeCAD.Base.Vector(p11[0], p11[1], z_off), FreeCAD.Base.Vector(p7[0], p7[1], z_off)))
    if p7 != p8:
        points.append(PLine(FreeCAD.Base.Vector(p7[0], p7[1], z_off), FreeCAD.Base.Vector(p8[0], p8[1], z_off)))
    if p8 != p1:
        p12 = arcMidPoint(p8, p1, curve)
        points.append(Part.Arc(FreeCAD.Base.Vector(p8[0], p8[1], z_off), FreeCAD.Base.Vector(p12[0], p12[1], z_off), FreeCAD.Base.Vector(p1[0], p1[1], z_off)))

    if dx==dy: # "circle"
        r=dx
        obj=[Part.Circle(FreeCAD.Vector(x, y, z_off), FreeCAD.Vector(0, 0, 1), r).toShape()]
        obj=Part.Wire(obj)
    else:
        # obj = Part.Shape(points)
        # obj = Part.Wire(obj.Edges)
        objs=[]  # asm3 Links compatible way
        for e in points:
            objs.append(e.toShape())
        obj = Part.Wire(objs)
    obj = makeFace(obj)
    #return makeFace(obj)
    list=[]
    list.append(obj)
    obj1=Part.makeCompound(list)
    return obj1
###
def cutHole2(mainObj, holep, holed):
    if holed[1] > min_val:
        #hole = [Part.Circle(FreeCAD.Vector(hole[0], hole[1]), FreeCAD.Vector(0, 0, 1), hole[2]).toShape()]
        z_off=0

        hole = addPadLong(holep[0], holep[1], holed[0], holed[1], 100, 0, z_off)
        mainObj = mainObj.cut(hole)
        Part.show(mainObj)
    return mainObj
###
###
def createPad2(x,y,sx,sy,dcx,dcy,dx,dy,type,layer):
    ##pad pos x,y; pad size x,y; drillcenter x,y; drill size x,y, layer
    z_offset=0
    remove=1
    if type=="oval":
        perc=100
        tp=0
    else:
        perc=0
        tp=0
    if layer=="top":
        thick=-0.01
        z_offset=0
    else:
        thick=0.01
        z_offset=-1.6
    #say(str(x)+"x "+str(y)+"y "+str(sx)+"sx "+str(sy)+"sy ")
    #say(str(dcx)+"dcx "+str(dcy)+"dcy "+str(dx)+"dx "+str(dy)+"dy ")
    mypad=addPadLong2(x, y, sx, sy, perc, tp, z_offset)
    Part.show(mypad)
    FreeCAD.ActiveDocument.ActiveObject.Label="mypad"
    pad_name=FreeCAD.ActiveDocument.ActiveObject.Name
    if dx!=0:
        perc=100 #drill always oval
        tp=0
        mydrill=addPadLong2(dcx, dcy, dx, dy, perc, tp, 0)
        Part.show(mydrill)
        FreeCAD.ActiveDocument.ActiveObject.Label="mydrill"
        drill_name=FreeCAD.ActiveDocument.ActiveObject.Name
        myannular=addPadLong2(dcx, dcy, dx+0.01, dy+0.01, perc, tp, 0)
        Part.show(myannular)
        FreeCAD.ActiveDocument.ActiveObject.Label="myannular"
        ann_name=FreeCAD.ActiveDocument.ActiveObject.Name
        #myhole=addPadLong2(dcx, dcy, dx, dy, perc, tp, z_offset)
        #Part.show(myhole)
        #FreeCAD.ActiveDocument.ActiveObject.Label="myhole"
        # workaround FC 0.17 OCC 7
        try:
            if float(Part.OCC_VERSION.split('.')[0]) >= 7:
                mydrill.reverse()
        except:
            pass
        wire = [mypad,mydrill]
        wire2 = [myannular,mydrill]
        face = Part.Face(wire)
        face2 = Part.Face(mydrill)
        face3 = Part.Face(wire2)
        extr = face.extrude(FreeCAD.Vector(0,0,-.01))
        Part.show(extr)
        FreeCAD.ActiveDocument.ActiveObject.Label="drilled_pad"
        extr2 = face2.extrude(FreeCAD.Vector(0,0,-1.58))
        Part.show(extr2)
        FreeCAD.ActiveDocument.ActiveObject.Label="hole"
        extr3 = face3.extrude(FreeCAD.Vector(0,0,-1.58))
        Part.show(extr3)
        FreeCAD.ActiveDocument.ActiveObject.Label="annular"
        FreeCAD.ActiveDocument.removeObject(pad_name)
        FreeCAD.ActiveDocument.removeObject(drill_name)
        FreeCAD.ActiveDocument.removeObject(ann_name)
        FreeCAD.ActiveDocument.recompute()
    else:
        face = Part.Face(mypad)
        extr = face.extrude(FreeCAD.Vector(0,0,-.01))
        Part.show(extr)
        FreeCAD.ActiveDocument.ActiveObject.Label="smd_pad"
        FreeCAD.ActiveDocument.removeObject(pad_name)
        FreeCAD.ActiveDocument.recompute()
    return extr
###
def createPad(x,y,sx,sy,dcx,dcy,dx,dy,type,layer):
    ##pad pos x,y; pad size x,y; drillcenter x,y; drill size x,y
    z_offset=0
    remove=1
    if type=="oval":
        perc=100
        tp=0
    else:
        perc=0
        tp=0
    if layer=="top":
        thick=-0.01
        z_offset=0
    else:
        thick=0.01
        z_offset=-1.6
    #say(str(x)+"x "+str(y)+"y "+str(sx)+"sx "+str(sy)+"sy ")
    #say(str(dcx)+"dcx "+str(dcy)+"dcy "+str(dx)+"dx "+str(dy)+"dy ")
    mypad=addPadLong(x, y, sx, sy, perc, tp, z_offset)
    Part.show(mypad)
    FreeCAD.ActiveDocument.ActiveObject.Label="mypad"
    pad_name=FreeCAD.ActiveDocument.ActiveObject.Name
    FreeCAD.ActiveDocument.addObject("Part::Extrusion","Extrude_pad")
    extrude_name=FreeCAD.ActiveDocument.ActiveObject.Name
    FreeCAD.ActiveDocument.Extrude_pad.Base = FreeCAD.ActiveDocument.getObject(pad_name)
    FreeCAD.ActiveDocument.Extrude_pad.Dir = (0,0,thick)
    FreeCAD.ActiveDocument.Extrude_pad.Solid = (True)
    FreeCAD.ActiveDocument.Extrude_pad.TaperAngle = (0)
    FreeCADGui.ActiveDocument.getObject(pad_name).Visibility = False
    FreeCAD.ActiveDocument.Extrude_pad.Label = 'mypad_solid'
    extrude_pad_name=FreeCAD.ActiveDocument.ActiveObject.Name
    #FreeCAD.ActiveDocument.recompute()
    if dx!=0:
        perc=100 #drill always oval
        mydrill=addPadLong(dcx, dcy, dx, dy, perc, tp, z_offset)
        # workaround FC 0.17 OCC 7
        try:
            if float(Part.OCC_VERSION.split('.')[0]) >= 7:
                mydrill.reverse()
        except:
            pass
        Part.show(mydrill)
        FreeCAD.ActiveDocument.ActiveObject.Label="mydrill"
        drill_name=FreeCAD.ActiveDocument.ActiveObject.Name
        FreeCAD.ActiveDocument.addObject("Part::Extrusion","Extrude_d")
        extrude_d_name=FreeCAD.ActiveDocument.ActiveObject.Name
        FreeCAD.ActiveDocument.Extrude_d.Base = FreeCAD.ActiveDocument.getObject(drill_name)
        FreeCAD.ActiveDocument.Extrude_d.Dir = (0,0,thick)
        FreeCAD.ActiveDocument.Extrude_d.Solid = (True)
        FreeCAD.ActiveDocument.Extrude_d.TaperAngle = (0)
        FreeCADGui.ActiveDocument.getObject(drill_name).Visibility = False
        FreeCAD.ActiveDocument.Extrude_d.Label = 'mydrill_solid'
        extrude_drill_name=FreeCAD.ActiveDocument.ActiveObject.Name
        #FreeCAD.ActiveDocument.recompute()

        FreeCAD.activeDocument().addObject("Part::Cut","myCut")
        cut_name=FreeCAD.ActiveDocument.ActiveObject.Name
        FreeCAD.activeDocument().getObject(cut_name).Base = FreeCAD.activeDocument().Extrude_pad
        FreeCAD.activeDocument().getObject(cut_name).Tool = FreeCAD.activeDocument().Extrude_d
        FreeCADGui.activeDocument().Extrude_pad.Visibility=False
        FreeCADGui.activeDocument().Extrude_d.Visibility=False
        #FreeCADGui.ActiveDocument.getObject(cut_name).ShapeColor=FreeCADGui.ActiveDocument.Extrude.ShapeColor
        FreeCADGui.ActiveDocument.ActiveObject.ShapeColor =  (0.81,0.71,0.23) #(0.85,0.53,0.10)
        FreeCADGui.ActiveDocument.ActiveObject.DisplayMode=FreeCADGui.ActiveDocument.Extrude_pad.DisplayMode
        FreeCAD.ActiveDocument.recompute()
        pad_d_name="TH_Pad"
        FreeCAD.ActiveDocument.addObject('Part::Feature',pad_d_name).Shape=FreeCAD.ActiveDocument.ActiveObject.Shape
        FreeCADGui.ActiveDocument.ActiveObject.ShapeColor =  (0.81,0.71,0.23) #(0.85,0.53,0.10)
        myObj=FreeCAD.ActiveDocument.getObject(pad_d_name)
        if remove==1:
            FreeCAD.ActiveDocument.removeObject(cut_name)
            FreeCAD.ActiveDocument.removeObject(extrude_pad_name)
            FreeCAD.ActiveDocument.removeObject(pad_name)
            FreeCAD.ActiveDocument.removeObject(drill_name)
            FreeCAD.ActiveDocument.removeObject(extrude_drill_name)
        FreeCAD.ActiveDocument.recompute()
    else:
        FreeCAD.ActiveDocument.recompute()
        pad_d_name="smdPad"
        FreeCAD.ActiveDocument.addObject('Part::Feature',pad_d_name).Shape=FreeCAD.ActiveDocument.ActiveObject.Shape
        myObj=FreeCAD.ActiveDocument.getObject(pad_d_name)
        FreeCADGui.ActiveDocument.ActiveObject.ShapeColor =  (0.81,0.71,0.23) #(0.85,0.53,0.10)
        FreeCAD.ActiveDocument.removeObject(extrude_pad_name)
        FreeCAD.ActiveDocument.removeObject(pad_name)
        FreeCAD.ActiveDocument.recompute()
    return myObj
###
def createPad3(x,y,sx,sy,dcx,dcy,dx,dy,type,layer, ratio=None):
    ##pad pos x,y; pad size x,y; drillcenter x,y; drill size x,y, type, layer, rratio
    z_offset=0
    remove=1
    if type=="oval" or type=="circle":
        perc=100
        tp=0
    else:
        perc=0
        tp=0
    if layer=="top":
        thick=-0.01
        z_offset=0
    else:
        thick=0.01
        z_offset=-1.6
    #say(str(x)+"x "+str(y)+"y "+str(sx)+"sx "+str(sy)+"sy ")
    #say(str(dcx)+"dcx "+str(dcy)+"dcy "+str(dx)+"dx "+str(dy)+"dy ")
    mypad=addPadLong2(x, y, sx, sy, perc, tp, z_offset, type, ratio)
    Part.show(mypad)
    FreeCAD.ActiveDocument.ActiveObject.Label="mypad"
    pad_name=FreeCAD.ActiveDocument.ActiveObject.Name
    if dx!=0:
        perc=100 #drill always oval
        tp=0
        mydrill=addPadLong2(dcx, dcy, dx, dy, perc, tp, z_offset)
        # workaround FC 0.17 OCC 7
        try:
            if float(Part.OCC_VERSION.split('.')[0]) >= 7:
                mydrill.reverse()
        except:
            pass
        if test_flag_pads==True:
            Part.show(mydrill)
            FreeCAD.ActiveDocument.ActiveObject.Label="mydrill"
            drill_name=FreeCAD.ActiveDocument.ActiveObject.Name
        myannular=addPadLong2(dcx, dcy, dx+0.01, dy+0.01, perc, tp, z_offset)
        if test_flag_pads==True:
            Part.show(myannular)
            FreeCAD.ActiveDocument.ActiveObject.Label="myannular"
            ann_name=FreeCAD.ActiveDocument.ActiveObject.Name
        myhole=addPadLong2(dcx, dcy, dx, dy, perc, tp, z_offset)
        if test_flag_pads==True:
            Part.show(myhole)
            FreeCAD.ActiveDocument.ActiveObject.Label="myhole"
        wire = [mypad,mydrill] 
        face = Part.Face(wire) 
        extr = face.extrude(FreeCAD.Vector(0,0,thick))
        if test_flag_pads==True:
            Part.show(extr)
            FreeCAD.ActiveDocument.ActiveObject.Label="drilled_pad"
        FreeCAD.ActiveDocument.removeObject(pad_name)
        FreeCAD.ActiveDocument.recompute()
    else:
        face = Part.Face(mypad)
        extr = face.extrude(FreeCAD.Vector(0,0,thick))
        #Part.show(extr)
        #FreeCAD.ActiveDocument.ActiveObject.Label="smd_pad"
        FreeCAD.ActiveDocument.removeObject(pad_name)
        FreeCAD.ActiveDocument.recompute()
    return extr
###
def createPad(x,y,sx,sy,dcx,dcy,dx,dy,type,layer):
    ##pad pos x,y; pad size x,y; drillcenter x,y; drill size x,y
    z_offset=0
    remove=1
    if type=="oval":
        perc=100
        tp=0
    else:
        perc=0
        tp=0
    if layer=="top":
        thick=-0.01
        z_offset=0
    else:
        thick=0.01
        z_offset=-1.6
    #say(str(x)+"x "+str(y)+"y "+str(sx)+"sx "+str(sy)+"sy ")
    #say(str(dcx)+"dcx "+str(dcy)+"dcy "+str(dx)+"dx "+str(dy)+"dy ")
    mypad=addPadLong(x, y, sx, sy, perc, tp, z_offset)
    Part.show(mypad)
    FreeCAD.ActiveDocument.ActiveObject.Label="mypad"
    pad_name=FreeCAD.ActiveDocument.ActiveObject.Name
    FreeCAD.ActiveDocument.addObject("Part::Extrusion","Extrude_pad")
    extrude_name=FreeCAD.ActiveDocument.ActiveObject.Name
    FreeCAD.ActiveDocument.Extrude_pad.Base = FreeCAD.ActiveDocument.getObject(pad_name)
    FreeCAD.ActiveDocument.Extrude_pad.Dir = (0,0,thick)
    FreeCAD.ActiveDocument.Extrude_pad.Solid = (True)
    FreeCAD.ActiveDocument.Extrude_pad.TaperAngle = (0)
    FreeCADGui.ActiveDocument.getObject(pad_name).Visibility = False
    FreeCAD.ActiveDocument.Extrude_pad.Label = 'mypad_solid'
    extrude_pad_name=FreeCAD.ActiveDocument.ActiveObject.Name
    #FreeCAD.ActiveDocument.recompute()
    if dx!=0:
        perc=100 #drill always oval
        mydrill=addPadLong(dcx, dcy, dx, dy, perc, tp, z_offset)
        # workaround FC 0.17 OCC 7
        try:
            if float(Part.OCC_VERSION.split('.')[0]) >= 7:
                mydrill.reverse()
        except:
            pass
        Part.show(mydrill)
        FreeCAD.ActiveDocument.ActiveObject.Label="mydrill"
        drill_name=FreeCAD.ActiveDocument.ActiveObject.Name
        FreeCAD.ActiveDocument.addObject("Part::Extrusion","Extrude_d")
        extrude_d_name=FreeCAD.ActiveDocument.ActiveObject.Name
        FreeCAD.ActiveDocument.Extrude_d.Base = FreeCAD.ActiveDocument.getObject(drill_name)
        FreeCAD.ActiveDocument.Extrude_d.Dir = (0,0,thick)
        FreeCAD.ActiveDocument.Extrude_d.Solid = (True)
        FreeCAD.ActiveDocument.Extrude_d.TaperAngle = (0)
        FreeCADGui.ActiveDocument.getObject(drill_name).Visibility = False
        FreeCAD.ActiveDocument.Extrude_d.Label = 'mydrill_solid'
        extrude_drill_name=FreeCAD.ActiveDocument.ActiveObject.Name
        #FreeCAD.ActiveDocument.recompute()

        FreeCAD.activeDocument().addObject("Part::Cut","myCut")
        cut_name=FreeCAD.ActiveDocument.ActiveObject.Name
        FreeCAD.activeDocument().getObject(cut_name).Base = FreeCAD.activeDocument().Extrude_pad
        FreeCAD.activeDocument().getObject(cut_name).Tool = FreeCAD.activeDocument().Extrude_d
        FreeCADGui.activeDocument().Extrude_pad.Visibility=False
        FreeCADGui.activeDocument().Extrude_d.Visibility=False
        #FreeCADGui.ActiveDocument.getObject(cut_name).ShapeColor=FreeCADGui.ActiveDocument.Extrude.ShapeColor
        FreeCADGui.ActiveDocument.ActiveObject.ShapeColor =  (0.81,0.71,0.23) #(0.85,0.53,0.10)
        FreeCADGui.ActiveDocument.ActiveObject.DisplayMode=FreeCADGui.ActiveDocument.Extrude_pad.DisplayMode
        FreeCAD.ActiveDocument.recompute()
        pad_d_name="TH_Pad"
        FreeCAD.ActiveDocument.addObject('Part::Feature',pad_d_name).Shape=FreeCAD.ActiveDocument.ActiveObject.Shape
        FreeCADGui.ActiveDocument.ActiveObject.ShapeColor =  (0.81,0.71,0.23) #(0.85,0.53,0.10)
        myObj=FreeCAD.ActiveDocument.getObject(pad_d_name)
        if remove==1:
            FreeCAD.ActiveDocument.removeObject(cut_name)
            FreeCAD.ActiveDocument.removeObject(extrude_pad_name)
            FreeCAD.ActiveDocument.removeObject(pad_name)
            FreeCAD.ActiveDocument.removeObject(drill_name)
            FreeCAD.ActiveDocument.removeObject(extrude_drill_name)
        FreeCAD.ActiveDocument.recompute()
    else:
        FreeCAD.ActiveDocument.recompute()
        pad_d_name="smdPad"
        FreeCAD.ActiveDocument.addObject('Part::Feature',pad_d_name).Shape=FreeCAD.ActiveDocument.ActiveObject.Shape
        myObj=FreeCAD.ActiveDocument.getObject(pad_d_name)
        FreeCADGui.ActiveDocument.ActiveObject.ShapeColor =  (0.81,0.71,0.23) #(0.85,0.53,0.10)
        FreeCAD.ActiveDocument.removeObject(extrude_pad_name)
        FreeCAD.ActiveDocument.removeObject(pad_name)
        FreeCAD.ActiveDocument.recompute()
    return myObj
###

def createHole(x,y,dx,dy,type):
    if type=="oval":
        perc=100
        tp=0
    else:
        perc=0
        tp=0
    mydrill=addPadLong(x, y, dx, dy, perc, tp, 0)
    Part.show(mydrill)
    FreeCAD.ActiveDocument.ActiveObject.Label="mydrill"
    drill_name=FreeCAD.ActiveDocument.ActiveObject.Name
    FreeCAD.ActiveDocument.addObject("Part::Extrusion","Extrude_d")
    FreeCAD.ActiveDocument.Extrude_d.Base = FreeCAD.ActiveDocument.getObject(drill_name)
    FreeCAD.ActiveDocument.Extrude_d.Dir = (0,0,-1.6)
    FreeCAD.ActiveDocument.Extrude_d.Solid = (True)
    FreeCAD.ActiveDocument.Extrude_d.TaperAngle = (0)
    FreeCADGui.ActiveDocument.getObject(drill_name).Visibility = False
    FreeCAD.ActiveDocument.Extrude_d.Label = 'mydrill_hole'
    extrude_hole_name=FreeCAD.ActiveDocument.ActiveObject.Name
    FreeCAD.ActiveDocument.recompute()

    hole_name="hole"
    FreeCAD.ActiveDocument.addObject('Part::Feature',hole_name).Shape=FreeCAD.ActiveDocument.getObject(extrude_hole_name).Shape
    FreeCADGui.ActiveDocument.ActiveObject.ShapeColor = (0.67,1.00,0.50)
    FreeCADGui.ActiveDocument.ActiveObject.Transparency = 70
    myObj=FreeCADGui.ActiveDocument.ActiveObject
    FreeCAD.ActiveDocument.removeObject(drill_name)
    FreeCAD.ActiveDocument.removeObject(extrude_hole_name)
    FreeCAD.ActiveDocument.recompute()

    return myObj

###
def createHole2(x,y,dx,dy,type):
    if type=="oval" or type=="circle":
        perc=100
        tp=0
    else:
        perc=0
        tp=0
    #mydrill=addPadLong(x, y, dx, dy, perc, tp, -0.01)
    mydrill=addPadLong(x, y, dx, dy, perc, tp, .01)
    # workaround FC 0.17 OCC 7
    try:
        if float(Part.OCC_VERSION.split('.')[0]) >= 7:
            mydrill.reverse()
    except:
        pass
    #Part.show(mydrill)
    #hole = mydrill.extrude(FreeCAD.Base.Vector(0, 0, -1.58))
    hole = mydrill.extrude(FreeCAD.Base.Vector(0, 0, -1.61))
    holeModel=[]
    holeModel.append(hole)
    holeModel = Part.makeCompound(holeModel)
    #say("hereHole")
    #FreeCAD.ActiveDocument.recompute()
    return holeModel

###
def createHole3(x,y,dx,dy,type,height):
    if type=="oval":
        perc=100
        tp=0
    else:
        perc=0
        tp=0
    #mydrill=addPadLong(x, y, dx, dy, perc, tp, -0.01)
    mydrill=addPadLong(x, y, dx, dy, perc, tp, 0.1)
    #Part.show(mydrill)
    #hole = mydrill.extrude(FreeCAD.Base.Vector(0, 0, -1.58))
    hole = mydrill.extrude(FreeCAD.Base.Vector(0, 0, -(height+0.2)))
    holeModel=[]
    holeModel.append(hole)
    holeModel = Part.makeCompound(holeModel)
    #say("hereHole")
    #FreeCAD.ActiveDocument.recompute()

    return holeModel

###
###
def createHole4(x,y,dx,dy,type):
    if type=="oval":
        perc=100
        tp=0
    else:
        perc=0
        tp=0
    #mydrill=addPadLong(x, y, dx, dy, perc, tp, -0.01)
    #mydrill=addPadLong(x, y, dx, dy, perc, tp, .01)
    mydrill=addPadLong2(x, y, dx, dy, perc, tp, 0)
    holeModel=[]
    #holeModel.append(hole)
    #holeModel.append(mydrill)
    ##holeModel = Part.makeCompound(holeModel)
    #holeModel = Part.Face(holeModel)
    face = OSCD2Dg_edgestofaces(mydrill.Edges,3 , edge_tolerance)
    face.fix(0,0,0)
    #Part.show(face)
    holeModel = face
    #sayerr('x'+str(x)+' y'+str(y)+' dx'+str(dx)+' dy'+str(dy)+' perc'+str(perc)+' tp'+str(tp)+'0')
    #stop
    #say("hereHole")
    #FreeCAD.ActiveDocument.recompute()
    return holeModel

###
def createTHPlate(x,y,dx,dy,type):
    if type=="oval" or type=="circle":
        perc=100
        tp=0
    else:
        perc=0
        tp=0
    #mydrill=addPadLong(x, y, dx, dy, perc, tp, -0.01)
    mydrill=addPadLong2(x, y, dx, dy, perc, tp, -0.01)
    # workaround FC 0.17 OCC 7
    try:
        if float(Part.OCC_VERSION.split('.')[0]) >= 7:
            mydrill.reverse()
    except:
        pass
    myannular=addPadLong2(x, y, dx+0.01, dy+0.01, perc, tp, -0.01)
    wire2 = [myannular,mydrill]
    face3 = Part.Face(wire2)
    THP = face3.extrude(FreeCAD.Vector(0,0,-1.58))
    #Part.show(extr3)
    #FreeCAD.ActiveDocument.ActiveObject.Label="annular"
    ##hole = mydrill.extrude(FreeCAD.Base.Vector(0, 0, -1.58))
    #THP = myannular.extrude(FreeCAD.Base.Vector(0, 0, -1.58))
    THPModel=[]
    THPModel.append(THP)
    THPModel = Part.makeCompound(THPModel)
    #say("hereHole")
    #FreeCAD.ActiveDocument.recompute()

    return THPModel

###
def createGeomC(cx, cy, radius, layer, width):
    #createGeomC(Gcx, Gcy, GRad,'top', Gw)
    if layer == 'top':
    #if top==True:
        thick=-0.01
        z_offset=0
    else:
        thick=0.01
        z_offset=-1.6
    bv = Base.Vector
    circ = Part.makeCircle(radius+width/2, bv(cx,cy,z_offset))    
    mw = Part.Wire(circ.Edges)
    myp= Part.Face(mw)
    #Part.show(mypad)
    circ = Part.makeCircle(radius-width/2, bv(cx,cy,z_offset))    
    mw2 = Part.Wire(circ.Edges)
    myp2 = Part.Face(mw2)
    mypad=myp.cut(myp2)
    Part.show(mypad)
    FreeCAD.ActiveDocument.ActiveObject.Label="mypad"
    pad_name=FreeCAD.ActiveDocument.ActiveObject.Name
    #    face = Part.Face(mypad)
    #    Part.show(face)
    extr = mypad.extrude(FreeCAD.Vector(0,0,thick))
    #Part.show(extr)
    #FreeCAD.ActiveDocument.ActiveObject.Label="smd_pad"
    FreeCAD.ActiveDocument.removeObject(pad_name)
    FreeCAD.ActiveDocument.recompute()

    #extr = sface.extrude(FreeCAD.Vector(0,0,-.01))
    #Part.show(extr)
    #stop
    
    return extr
    

def createPoly(x, y, sx, sy, dcx,dcy,dx,dy,pShape, layer, poly_points):
    #createPad3(x1, y1, dx, dy, xs,  ys,rx,ry,pShape,'top')
    #createPad3(x,  y,  sx,sy,  dcx,dcy,dx,dy,type,layer):
    pts=[]
    bv = Base.Vector
    p0 = poly_points[0].split(' ')
    if layer == 'top':
    #if top==True:
        thick=-0.01
        z_offset=0
    else:
        thick=0.01
        z_offset=-1.6
    for p in poly_points:
        pc = p.split(' ')                
        pts.append(bv(float(pc[1])+x,-1*float(pc[2][0:pc[2].index(')')])+y,z_offset))
        # print (float(pc[1])+x1,-1*float(pc[2][0:pc[2].index(')')])+y1,z_offset)
    # closing poly
    pts.append(bv(float(p0[1])+x,-1*float(p0[2][0:p0[2].index(')')])+y,z_offset))
    # print (float(p0[1])+x1,-1*float(p0[2][0:p0[2].index(')')])+y1,z_offset)
    # f = Draft.makeWire(pts,closed=True)
    # obj=f.Shape.copy()
    lshape_wire = Part.makePolygon(pts) 
    mypad = Part.Face(lshape_wire)
    Part.show(mypad)
    FreeCAD.ActiveDocument.ActiveObject.Label="mypad"
    pad_name=FreeCAD.ActiveDocument.ActiveObject.Name
    if dx!=0:
        perc=100 #drill always oval
        tp=0
        mydrill=addPadLong2(dcx, dcy, dx, dy, perc, tp, z_offset)
        # workaround FC 0.17 OCC 7
        try:
            if float(Part.OCC_VERSION.split('.')[0]) >= 7:
                mydrill.reverse()
        except:
            pass
        if test_flag_pads==True:
            Part.show(mydrill)
            FreeCAD.ActiveDocument.ActiveObject.Label="mydrill"
            drill_name=FreeCAD.ActiveDocument.ActiveObject.Name
        myannular=addPadLong2(dcx, dcy, dx+0.01, dy+0.01, perc, tp, z_offset)
        if test_flag_pads==True:
            Part.show(myannular)
            FreeCAD.ActiveDocument.ActiveObject.Label="myannular"
            ann_name=FreeCAD.ActiveDocument.ActiveObject.Name
        myhole=addPadLong2(dcx, dcy, dx, dy, perc, tp, z_offset)
        if test_flag_pads==True:
            Part.show(myhole)
            FreeCAD.ActiveDocument.ActiveObject.Label="myhole"
        #wire = [mypad,mydrill] 
        wire = [mydrill] 
        drl = Part.Face(wire) 
        #Part.show(drl)
        face = mypad.cut(drl)
        extr = face.extrude(FreeCAD.Vector(0,0,thick))
        #Part.show(extr);stop
        if test_flag_pads==True:
            Part.show(extr)
            FreeCAD.ActiveDocument.ActiveObject.Label="drilled_pad"
        FreeCAD.ActiveDocument.removeObject(pad_name)
        FreeCAD.ActiveDocument.recompute()
    else:
        face = Part.Face(mypad)
        extr = face.extrude(FreeCAD.Vector(0,0,thick))
        #Part.show(extr)
        #FreeCAD.ActiveDocument.ActiveObject.Label="smd_pad"
        FreeCAD.ActiveDocument.removeObject(pad_name)
        FreeCAD.ActiveDocument.recompute()

    #extr = sface.extrude(FreeCAD.Vector(0,0,-.01))
    #Part.show(extr)
    #stop
    
    return extr
    
###
def createArcW (layer, content, arc_prim, layer_list):

    fpArc = getArc(layer, content, arc_prim)
    #print(layer,fpArc)
    for i in fpArc:
        if len(i) == 6:  #kv5
            x1 = i[0] #+ X1
            y1 = i[1] #+ Y1
            x2 = i[2] #+ X1
            y2 = i[3] #+ Y1
            _angle = i[4]
            # print('center=',x1,y1,' end=',x2,y2,' angle=',i[4],' width=',i[5])
            arc1=addArc_3([x1, y1], [x2, y2], i[4], i[5])
            # kv5 fp_arc start=center coord, end=arc_end coord, angle=delta angle
            # getArc -> [x2, y2] = rotPoint2([x1, y1], [xc, yc], curve)
            xm=(x1+x2)/2
            ym=(y1+y2)/2
            rotateObj(arc1, [xm, ym, 180])
            layer_list.append(arc1)
        elif len(i) == 7: #kv6
            # kv6 fp_arc start=arc_start coord, mid=arc_mid coord, end=arc_end coord
            # start, mid, end
            xs = i[0]; ys = i[1] #+ Y1
            xm = i[2]; ym = i[3] #+ Y1
            xe = i[4]; ye = i[5] #+ Y1
            edge_arc = Part.ArcOfCircle(kicad_parser.makeVect([xs,-ys]),
                                    kicad_parser.makeVect([xm,-ym]),
                                    kicad_parser.makeVect([xe,-ye])).toShape() 
            #Draft.makeSketch(edge_arc)
            # e => arc Edge
            delta_angle=degrees(edge_arc.LastParameter-edge_arc.FirstParameter)
            center = edge_arc.Curve.Center
            xc,yc,zc= center[0],center[1],center[2]
            #print (center);  print(delta_angle)
            # arc1_kv5=addArc_3([x1, y1], [x2, y2], i[4], i[5])
            # kv5 fp_arc start=center coord, end=arc_end coord, angle=delta angle
            [x1,y1] = [xe, ye]
            [x2,y2] = [xs,ys] #rotPoint2([x1, y1], [xs, ys], -curve)
            # if curve <0:
            #     curve*=-1
            #if curve >90:
            #    curve=(curve-90)/4
            # arc1 = addArc_3([x1, y1], [x2, y2], curve, i[6])
            arc1 = addArc_3([x1, y1], [x2, y2], delta_angle, i[6])
            #arc1 = addArc_3([center[0], -center[1]], [x2, y2], -curve+180/2, i[6])
            xm=(x1+x2)/2
            ym=(y1+y2)/2
            #rotateObj(arc1, [xm, ym, 180])
            #.rotate(Vector(),Vector(0,0,1),180)
            layer_list.append(arc1)
        #else:
        #    print(len(i),str(i))
        #if mksketch:
        #    skt = Draft.makeSketch(arc1)
###
def routineDrawFootPrint(content,name):
    global rot_wrl, zfit
    #for item in content:
    #    say(item)

    #                      x1, y1, x2, y2, width
    say("FootPrint Loader "+name)
    footprint_name=getModName(content)
    rot_wrl=getwrlRot(content)
    posiz, scale, rot = getwrlData(content)
    #say(posiz);say(scale);say(rot);
    error_mod=False
    #if scale!=['1', '1', '1']:
    xsc_vrml_val=scale[0]
    ysc_vrml_val=scale[1]
    zsc_vrml_val=scale[2]        
    # if scale_vrml!='1 1 1':
    #sayw(scale)
    if float(xsc_vrml_val)!=1.0 or float(ysc_vrml_val)!=1.0 or float(zsc_vrml_val)!=1.0:
        sayw('wrong scale!!! set scale to (1 1 1)\n')
        error_mod=True
    if posiz!=['0', '0', '0']:
        sayw('wrong xyx position!!! set xyz to (0 0 0)\n')
        error_mod=True
    if rot[0]!='0' or rot[1]!='0':
        sayw('wrong rotation!!! set rotate x and y to (0 0 z)\n')
        error_mod=True
    if error_mod:
        msg="""<b>Error in '.kicad_mod' footprint</b><br>"""
        msg+="<br>reset values to:<br>"
        msg+="<b>(at (xyz 0 0 0))<br>"
        msg+="(scale (xyz 1 1 1))<br>"
        msg+="(rotate (xyz 0 0 z))<br>"
        msg+="</b><br>Only z rotation is allowed!"
        reply = QtGui.QMessageBox.information(None,"info", msg)
        #stop
    #say(footprint_name+" wrl rotation:"+str(rot_wrl))
    if FreeCAD.activeDocument():
        doc=FreeCAD.activeDocument()
    else:
        doc=FreeCAD.newDocument()
    #doc.UndoMode = 1
    #doc.openTransaction()
    doc.openTransaction('opening_kicad_footprint')
    say('opening Transaction \'opening_kicad_footprint\'')
    for obj in FreeCAD.ActiveDocument.Objects:
        FreeCADGui.Selection.removeSelection(obj)

    TopPadList=[]
    BotPadList=[]
    HoleList=[]
    THPList=[]
    TopNetTieList=[]
    BotNetTieList=[]
    for pad in getPadsList(content):
        # sayerr(pad)
        #
        #   pads.append({'x': x, 'y': y, 'rot': rot, 'padType': pType, 'padShape': pShape, 'rx': drill_x, 'ry': drill_y, 'dx': dx, 'dy': dy, 'holeType': hType, 'xOF': xOF, 'yOF': yOF, 'layers': layers})
        pType = pad['padType']
        pShape = pad['padShape']
        pRratio = pad['rratio']
        pGeomC = pad['geomC']
        xs = pad['x'] #+ X1
        ys = pad['y'] #+ Y1
        dx = pad['dx']
        dy = pad['dy']
        hType = pad['holeType']
        drill_x = pad['rx']
        drill_y = pad['ry']
        xOF = pad['xOF']
        yOF = pad['yOF']
        rot = pad['rot']
        rx=drill_x
        ry=drill_y
        numberOfLayers = pad['layers'].replace('"', '').split(' ')  # fixing double quotes in layers & pads
        # print(numberOfLayers)
        # print('F.Cu' in numberOfLayers)
        pnts = pad['points']
        anchor = pad['anchor']
        #if pnts is not None:
        #    sayw(pnts.groups(0)[0].split('(xy'))
            #sayw(pnts)
        #say(str(rx))
        #say(numberOfLayers)
        #if pType=="thru_hole":
        #pad shape - circle/rec/oval/trapezoid
        perc=0
        if pShape=="circle" or pShape=="oval":
            ##pShape="oval"
            perc=100
            # pad type - SMD/thru_hole/connect
        #say(pType+"here")
        if dx>rx and dy>ry:
            #say(pType)
            #say(str(dx)+"+"+str(rx)+" dx,rx")
            #say(str(dy)+"+"+str(ry)+" dy,ry")
            #say(str(xOF)+"+"+str(yOF)+" xOF,yOF")
            #def addPadLong(x, y, dx, dy, perc, typ, z_off):
            #say(str(x1)+"+"+str(y1)+" x1,y1")
            top=False
            bot=False
            if 'F.Cu' in numberOfLayers:
                top=True
            if '*.Cu' in numberOfLayers:
                top=True
                bot=True
            if 'B.Cu' in numberOfLayers:
                bot=True
            # print(numberOfLayers)
            pattern = 'In+([0-9]*?).Cu'
            result = re.search(pattern, str(numberOfLayers))
            if result is not None:
                sayerr('internal layers not supported!')
                sayw(result.group())
            if top==True:
                x1=xs+xOF
                y1=ys-yOF #yoffset opposite
                #mypad=addPadLong(x1, y1, dx, dy, perc, 0, 0)
                mypad2 = None
                skip = False
                if pShape=='custom' and pGeomC is None:
                #if (pShape=='custom' or pShape=='NetTie') and pGeomC is None:
                    #sayw(pnts.groups(0)[0].split('(xy'))
                    #print(pGeomC)
                    try:
                        poly_points=pnts.groups(0)[0].split('(xy')[1:]
                        mypad=createPoly(x1, y1, dx, dy, xs,ys,rx,ry,pShape,'top', poly_points)
                        if anchor is not None:
                            if anchor[0]=="circle":
                                perc=100
                            #print 'anchor ',anchor[0]
                            mypad2=createPad3(x1, y1, dx, dy, xs,ys,rx,ry,anchor,'top')
                            #Part.show(mypad2)
                            #print anchor
                            #stop
                    except:
                        sayerr('geometry unsupported')
                        skip = True
                elif pShape=='custom' and pGeomC is not None:
                    #sayerr(pGeomC)
                    #print('pGeomC',(pGeomC))
                    #print ('x1',x1,'y1',y1)
                    Gc=pGeomC[0].split(' ')
                    #Gcx=-float(Gc[1])-x1;Gcy=float(Gc[2])-y1
                    Gr=pGeomC[1].split(' ')
                    GRad=abs(float(Gr[1])-float(Gc[1]))
                    Gcx=x1+float(Gc[1])
                    Gcy=float(Gc[2])-y1
                    #print('Gr',Gr,'GR',GRad,'Gc1',Gc[1],'Gc2',Gc[2],'Gcx',Gcx)
                    Gw=pGeomC[2].split(' ')
                    Gw=float(Gw[1])
                    #print (Gcx,Gcy,GRad,Gw)
                    mypad=createGeomC(Gcx, Gcy, GRad,'top', Gw)
                    if anchor is not None:
                        if anchor[0]=="circle":
                            perc=100
                        #print 'anchor ',anchor[0]
                        mypad2=createPad3(x1, y1, dx, dy, xs,ys,rx,ry,anchor,'top')
                        #Part.show(mypad2)
                        
                    #print TopPadList
                #stop
                else:
                    #mypad=createPad3(x1, y1, dx, dy, xs,ys,rx,ry,pShape,'top')
                    mypad=createPad3(x1, y1, dx, dy, xs,ys,rx,ry,pShape,'top',pRratio)
                ##pad pos x,y; pad size x,y; drillcenter x,y; drill size x,y, layer
                obj=mypad
                if rot != 0 and not skip:
                    rotateObj(obj, [xs, ys, rot])
                    if mypad2 is not None:
                        rotateObj(mypad2, [xs, ys, rot])
                if not skip:
                    TopPadList.append(obj)
                if mypad2 is not None:
                    TopPadList.append(mypad2)
                
            if bot==True:
                #on Bot layer offset is opposite
                x1=xs-xOF
                y1=ys+yOF #yoffset opposite
                #mypad=addPadLong(x1, y1, dx, dy, perc, 0, -1.6)
                mypad2=None; skip = False
                #if pShape=='custom':
                if pShape=='custom' and pGeomC is None:
                    #sayw(pnts.groups(0)[0].split('(xy'))
                    try:
                        poly_points=pnts.groups(0)[0].split('(xy')[1:]
                        mypad=createPoly(x1, y1, dx, dy, xs,ys,rx,ry,pShape,'bot', poly_points)
                        if anchor is not None:
                            if anchor=="circle":
                                perc=100
                            mypad2=createPad3(x1, y1, dx, dy, xs,ys,rx,ry,anchor,'bot')
                    except:
                        sayerr('geometry unsupported')
                        skip = True
                elif pShape=='custom' and pGeomC is not None:
                    #sayerr(pGeomC)
                    #print('pGeomC',(pGeomC))
                    #print ('x1',x1,'y1',y1)
                    Gc=pGeomC[0].split(' ')
                    #Gcx=-float(Gc[1])-x1;Gcy=float(Gc[2])-y1
                    Gr=pGeomC[1].split(' ')
                    GRad=abs(float(Gr[1])-float(Gc[1]))
                    Gcx=x1+float(Gc[1])
                    Gcy=float(Gc[2])-y1
                    #print('Gr',Gr,'GR',GRad,'Gc1',Gc[1],'Gc2',Gc[2],'Gcx',Gcx)
                    Gw=pGeomC[2].split(' ')
                    Gw=float(Gw[1])
                    #print (Gcx,Gcy,GRad,Gw)
                    mypad=createGeomC(Gcx, Gcy, GRad,'bot', Gw)
                    if anchor is not None:
                        if anchor[0]=="circle":
                            perc=100
                        #print 'anchor ',anchor[0]
                        mypad2=createPad3(x1, y1, dx, dy, xs,ys,rx,ry,anchor,'bot')
                        Part.show(mypad2)
                        #stop
                else:
                    mypad=createPad3(x1, y1, dx, dy, xs,ys,rx,ry,pShape,'bot',pRratio)
                ##pad pos x,y; pad size x,y; drillcenter x,y; drill size x,y, layerobj=mypad
                obj=mypad
                if rot!=0 and not skip:
                    rotateObj(obj, [xs, ys, +rot+180])
                    #rotateObj(obj, [xs, ys, -rot+180])
                    if mypad2 is not None:
                        rotateObj(mypad2, [xs, ys, +rot+180])
                        #rotateObj(mypad2, [xs, ys, -rot+180])
                if not skip:
                    BotPadList.append(obj)
                if mypad2 is not None:
                    BotPadList.append(mypad2)
        if rx!=0:
            #obj=createHole2(xs,ys,rx,ry,"oval") #need to be separated instructions
            #print pShape
            #stop
            hole_tp=hType.strip()
            #sayw(hole_tp)
            obj=createHole2(xs,ys,rx,ry,hole_tp) #need to be separated instructions
            ##obj=createHole2(xs,ys,rx,ry,pShape) #need to be separated instructions
            #say(HoleList)
            if rot!=0:
                rotateObj(obj, [xs, ys, rot])
            HoleList.append(obj)
            #obj2=createTHPlate(xs,ys,rx,ry,"oval")
            obj2=createTHPlate(xs,ys,rx,ry,hole_tp)
            ##obj2=createTHPlate(xs,ys,rx,ry,pShape)
            THPList.append(obj2)
            if rot!=0:
                rotateObj(obj2, [xs, ys, rot])

        
        #say(pType+"here")
        ### cmt- #da gestire: pad type trapez
    FrontSilk = []
    FCrtYd = []
    FFab = []
    EdgeCuts = []
    BotSilk = []
    BCrtYd = []
    BFab = []
    
    layer_names = ['F.SilkS','F.CrtYd','F.Fab','Edge.Cuts','B.SilkS','B.CrtYd','B.Fab']
    layers_name_list = [FrontSilk,FCrtYd,FFab,EdgeCuts,BotSilk,BCrtYd,BFab]
    
    fp_list,width = getPolyList(content)
    for fp in fp_list:
        pnts = fp['points']
        layers = fp['layers']
        #print(layers)
        pShape = 'NetTie'
        skip = False
        if 'B.Cu' in layers or 'B.Mask' in layers:
            lyr = 'bot'
        elif 'F.Cu' in layers:
            lyr = 'top'
        elif 'Edge.Cuts' in layers:
            lyr = 'Edge.Cuts'
        else:
            lyr = None
            sayw('geometry unsupported')
        if pnts is not None and lyr is not None and lyr != 'Edge.Cuts': # minimal closed shape points
            #sayw(pnts.groups(0)[0].split('(xy'))
            #print(pGeomC)
            try:
                poly_points=pnts.groups(0)[0].split('(xy')[1:]
                #print(poly_points)
                mypad=createPoly(0.0, 0.0, 0.0, 0.0, 0.0,0.0,0.0,0.0,pShape,lyr, poly_points)
            except:
                sayerr('geometry unsupported')
                skip = True
            if not skip:
                if lyr == 'top':
                    #TopPadList.append(mypad)
                    TopNetTieList.append(mypad)
                else:
                    #BotPadList.append(mypad)
                    BotNetTieList.append(mypad)
        # polyline fp_poly
        elif lyr == 'Edge.Cuts':
            #print(pnts.groups(0)[1])
            poly_points=pnts.groups(0)[1].split('(xy')[1:]
            #print(poly_points)
            for i,p in enumerate (poly_points[:-1]):
                p=p[1:].split(')')[0].split(' ')
                p1 = poly_points[i+1][1:].split(')')[0].split(' ')
                x1 = float(p[0]) #+ X1
                y1 = -float(p[1]) #+ Y1
                x2 = float(p1[0]) #+ X1
                y2 = -float(p1[1]) #+ Y1
                obj = addLine_2(x1, y1, x2, y2, 0.12)
                layers_name_list[3].append(addLine_2(x1, y1, x2, y2, width))
            #closing poly
            p = poly_points[0][1:].split(')')[0].split(' ')
            x1 = float(p[0]) #+ X1
            y1 = -float(p[1]) #+ Y1
            obj = addLine_2(x2, y2, x1, y1, width)
            layers_name_list[3].append(addLine_2(x1, y1, x2, y2, width))
            #stop
        
##

    #FrontSilk = []
    #FCrtYd = []
    #FFab = []
    #EdgeCuts = []
    #BotSilk = []
    #BCrtYd = []
    #BFab = []
    #
    #layer_names = ['F.SilkS','F.CrtYd','F.Fab','Edge.Cuts','B.SilkS','B.CrtYd','B.Fab']
    #layers_name_list = [FrontSilk,FCrtYd,FFab,EdgeCuts,BotSilk,BCrtYd,BFab]
        
    #TBD 
    #for n,lay in enumerate (layer_names):
    #    getPolyList
    
    # line
    #getLine('F.SilkS', content, 'fp_line')
    for n,lay in enumerate (layer_names):
        for i in getLine(lay, content, 'fp_line'):
            x1 = i[0] #+ X1
            y1 = i[1] #+ Y1
            x2 = i[2] #+ X1
            y2 = i[3] #+ Y1
            obj = addLine_2(x1, y1, x2, y2, i[4])
            layers_name_list[n].append(addLine_2(x1, y1, x2, y2, i[4]))
    for n,lay in enumerate (layer_names):
        for i in getLine(lay, content, 'fp_rect'):
            x1 = i[0] #+ X1
            y1 = i[1] #+ Y1
            x2 = i[2] #+ X1
            y2 = i[3] #+ Y1
            obj = addLine_2(x1, y1, x2, y2, i[4])
            layers_name_list[n].append(addLine_2(x1, y1, x2, y1, i[4]))
            layers_name_list[n].append(addLine_2(x2, y1, x2, y2, i[4]))
            layers_name_list[n].append(addLine_2(x2, y2, x1, y2, i[4]))
            layers_name_list[n].append(addLine_2(x1, y2, x1, y1, i[4]))
    
    # circle
    for n,lay in enumerate (layer_names):
        for i in getCircle(lay, content, 'fp_circle'):
            xs = i[0] #+ X1
            ys = i[1] #+ Y1
            layers_name_list[n].append(addCircle_2(xs, ys, i[2], i[3]))
    # arc
    for n,lay in enumerate (layer_names):
        # print(l,lay,content)
        arc1 = createArcW (lay, content, 'fp_arc', layers_name_list[n])
    
    if len(FCrtYd)>0:
        #FSilk_lines = Part.makeCompound(FrontSilk)
        #Part.show(FSilk_lines)
        FCrtYd_lines = FreeCAD.ActiveDocument.addObject("Part::FeaturePython","FCrtYd_lines")
        #FSilk_lines.Label="FSilk_lines"
        #FSilk_lines_name=FSilk_lines.Name
        FCrtYd_lines.addProperty("App::PropertyBool","fixedPosition","importPart")
        FCrtYd_lines.Shape = Part.makeCompound(FCrtYd) #TopPadsBase.Shape.copy()
        FCrtYd_lines.ViewObject.Proxy=0
        FCrtYd_lines.fixedPosition = True
        FreeCAD.ActiveDocument.ActiveObject.Label="FCrtYd"
        FCrtYd_name=FreeCAD.ActiveDocument.ActiveObject.Name
        FreeCADGui.ActiveDocument.ActiveObject.ShapeColor = (0.0000,0.0000,1.0000)
        FreeCADGui.ActiveDocument.ActiveObject.Transparency = 60
    #
    if len(BCrtYd)>0:
        BCrtYd_lines = FreeCAD.ActiveDocument.addObject("Part::FeaturePython","BCrtYd_lines")
        BCrtYd_lines.addProperty("App::PropertyBool","fixedPosition","importPart")
        BCrtYd_lines.Shape = Part.makeCompound(BCrtYd) #TopPadsBase.Shape.copy()
        BCrtYd_lines.ViewObject.Proxy=0
        BCrtYd_lines.fixedPosition = True
        FreeCAD.ActiveDocument.ActiveObject.Label="BCrtYd"
        BCrtYd_name=FreeCAD.ActiveDocument.ActiveObject.Name
        FreeCADGui.ActiveDocument.ActiveObject.ShapeColor = (0.0000,0.0000,1.0000)
        FreeCADGui.ActiveDocument.ActiveObject.Transparency = 60
        FreeCAD.ActiveDocument.ActiveObject.Placement.Base.z-=1.6
    #
    if len(FFab)>0:
        #FSilk_lines = Part.makeCompound(FrontSilk)
        #Part.show(FSilk_lines)
        FFab_lines = FreeCAD.ActiveDocument.addObject("Part::FeaturePython","FFab_lines")
        #FSilk_lines.Label="FSilk_lines"
        #FSilk_lines_name=FSilk_lines.Name
        FFab_lines.addProperty("App::PropertyBool","fixedPosition","importPart")
        FFab_lines.Shape = Part.makeCompound(FFab) #TopPadsBase.Shape.copy()
        FFab_lines.ViewObject.Proxy=0
        FFab_lines.fixedPosition = True
        FreeCAD.ActiveDocument.ActiveObject.Label="FFab"
        FFab_name=FreeCAD.ActiveDocument.ActiveObject.Name
        FreeCADGui.ActiveDocument.ActiveObject.ShapeColor = (0.0000,1.0000,0.0000)
        FreeCADGui.ActiveDocument.ActiveObject.Transparency = 60
    #
    if len(BFab)>0:
        BFab_lines = FreeCAD.ActiveDocument.addObject("Part::FeaturePython","BFab_lines")
        BFab_lines.addProperty("App::PropertyBool","fixedPosition","importPart")
        BFab_lines.Shape = Part.makeCompound(BFab) #TopPadsBase.Shape.copy()
        BFab_lines.ViewObject.Proxy=0
        BFab_lines.fixedPosition = True
        FreeCAD.ActiveDocument.ActiveObject.Label="BFab"
        FFab_name=FreeCAD.ActiveDocument.ActiveObject.Name
        FreeCADGui.ActiveDocument.ActiveObject.ShapeColor = (0.0000,1.0000,0.0000)
        FreeCADGui.ActiveDocument.ActiveObject.Transparency = 60
        FreeCAD.ActiveDocument.ActiveObject.Placement.Base.z-=1.6
    #
    if len(FrontSilk)>0:
        #FSilk_lines = Part.makeCompound(FrontSilk)
        #Part.show(FSilk_lines)
        FSilk_lines = FreeCAD.ActiveDocument.addObject("Part::FeaturePython","FSilk_lines")
        #FSilk_lines.Label="FSilk_lines"
        #FSilk_lines_name=FSilk_lines.Name
        FSilk_lines.addProperty("App::PropertyBool","fixedPosition","importPart")
        FSilk_lines.Shape = Part.makeCompound(FrontSilk) #TopPadsBase.Shape.copy()
        FSilk_lines.ViewObject.Proxy=0
        FSilk_lines.fixedPosition = True
        FreeCAD.ActiveDocument.ActiveObject.Label="FrontSilk"
        FSilk_name=FreeCAD.ActiveDocument.ActiveObject.Name
        FreeCADGui.ActiveDocument.ActiveObject.ShapeColor = (1.0000,1.0000,1.0000)
        FreeCADGui.ActiveDocument.ActiveObject.Transparency = 60
    #
    if len(BotSilk)>0:
        #FSilk_lines = Part.makeCompound(FrontSilk)
        #Part.show(FSilk_lines)
        BSilk_lines = FreeCAD.ActiveDocument.addObject("Part::FeaturePython","BSilk_lines")
        #FSilk_lines.Label="FSilk_lines"
        #FSilk_lines_name=FSilk_lines.Name
        BSilk_lines.addProperty("App::PropertyBool","fixedPosition","importPart")
        BSilk_lines.Shape = Part.makeCompound(BotSilk) #TopPadsBase.Shape.copy()
        BSilk_lines.ViewObject.Proxy=0
        BSilk_lines.fixedPosition = True
        FreeCAD.ActiveDocument.ActiveObject.Label="BotSilk"
        BSilk_name=FreeCAD.ActiveDocument.ActiveObject.Name
        FreeCADGui.ActiveDocument.ActiveObject.ShapeColor = (1.0000,1.0000,1.0000)
        FreeCADGui.ActiveDocument.ActiveObject.Transparency = 60
        FreeCAD.ActiveDocument.ActiveObject.Placement.Base.z-=1.6
    #
    if len(EdgeCuts)>0:
        #FSilk_lines = Part.makeCompound(FrontSilk)
        #Part.show(FSilk_lines)
        ECuts_lines = FreeCAD.ActiveDocument.addObject("Part::FeaturePython","EdgeCuts_lines")
        #FSilk_lines.Label="FSilk_lines"
        #FSilk_lines_name=FSilk_lines.Name
        ECuts_lines.addProperty("App::PropertyBool","fixedPosition","importPart")
        ECuts_lines.Shape = Part.makeCompound(EdgeCuts) #TopPadsBase.Shape.copy()
        ECuts_lines.ViewObject.Proxy=0
        ECuts_lines.fixedPosition = True
        FreeCAD.ActiveDocument.ActiveObject.Label="EdgeCuts"
        ECuts_name=FreeCAD.ActiveDocument.ActiveObject.Name
        FreeCADGui.ActiveDocument.ActiveObject.ShapeColor = (1.0000,0.0000,0.0000)
        FreeCADGui.ActiveDocument.ActiveObject.Transparency = 30
    #

    if len(TopPadList)>0:
        # TopPadsBase = Part.makeCompound(TopPadList)
        # Part.show(TopPadsBase)
        # FreeCAD.ActiveDocument.ActiveObject.Label="TopPadsBase"
        # TopPadsBase_name=FreeCAD.ActiveDocument.ActiveObject.Name
        TopPads = FreeCAD.ActiveDocument.addObject("Part::FeaturePython","TopPads")
        TopPads.Label="TopPads"
        TopPads_name=TopPads.Name
        TopPads.addProperty("App::PropertyBool","fixedPosition","importPart")
        TopPads.Shape = Part.makeCompound(TopPadList) #TopPadsBase.Shape.copy()
        TopPads.ViewObject.Proxy=0
        TopPads.fixedPosition = True
        #fp_group.addObject(TopPads)
        #FreeCAD.ActiveDocument.removeObject(TopPadsBase.Name)
        FreeCADGui.ActiveDocument.ActiveObject.ShapeColor = (0.81,0.71,0.23) #(0.85,0.53,0.10)
        FreeCADGui.ActiveDocument.ActiveObject.Transparency = 60
    if len(BotPadList)>0:
        #BotPads = Part.makeCompound(BotPadList)
        #Part.show(BotPads)
        BotPads = FreeCAD.ActiveDocument.addObject("Part::FeaturePython","BotPads")
        #BotPads.Label="BotPads"
        BotPads_name=BotPads.Name
        BotPads.addProperty("App::PropertyBool","fixedPosition","importPart")
        BotPads.Shape = Part.makeCompound(BotPadList) #TopPadsBase.Shape.copy()
        BotPads.ViewObject.Proxy=0
        BotPads.fixedPosition = True
        FreeCAD.ActiveDocument.ActiveObject.Label="BotPads"
        BotPads_name=FreeCAD.ActiveDocument.ActiveObject.Name
        FreeCADGui.ActiveDocument.ActiveObject.ShapeColor = (0.81,0.71,0.23) #(0.85,0.53,0.10)
        FreeCADGui.ActiveDocument.ActiveObject.Transparency = 60
#
    if len(TopNetTieList)>0:
        TopNetTie = FreeCAD.ActiveDocument.addObject("Part::FeaturePython","TopNetTie")
        TopNetTie.Label="TopNetTie"
        TopNetTie_name=TopNetTie.Name
        TopNetTie.addProperty("App::PropertyBool","fixedPosition","importPart")
        TopNetTie.Shape = Part.makeCompound(TopNetTieList) #TopPadsBase.Shape.copy()
        TopNetTie.ViewObject.Proxy=0
        TopNetTie.fixedPosition = True
        FreeCADGui.ActiveDocument.ActiveObject.ShapeColor = (0.81,0.71,0.23) #(0.85,0.53,0.10)
        FreeCADGui.ActiveDocument.ActiveObject.Transparency = 60
    if len(BotNetTieList)>0:
        BotNetTie = FreeCAD.ActiveDocument.addObject("Part::FeaturePython","BotNetTie")
        BotNetTie.Label="BotNetTie"
        BotNetTie_name=BotNetTie.Name
        BotNetTie.addProperty("App::PropertyBool","fixedPosition","importPart")
        BotNetTie.Shape = Part.makeCompound(BotNetTieList) #TopPadsBase.Shape.copy()
        BotNetTie.ViewObject.Proxy=0
        BotNetTie.fixedPosition = True
        FreeCAD.ActiveDocument.ActiveObject.Label="BotNetTie"
        BotNetTie_name=FreeCAD.ActiveDocument.ActiveObject.Name
        FreeCADGui.ActiveDocument.ActiveObject.ShapeColor = (0.81,0.71,0.23) #(0.85,0.53,0.10)
        FreeCADGui.ActiveDocument.ActiveObject.Transparency = 60
    #
    if len(HoleList)>0:
        Holes = Part.makeCompound(HoleList)
        Holes = Part.makeSolid(Holes)
        Part.show(Holes)
        #say(FreeCAD.ActiveDocument.ActiveObject.Name)
        FreeCAD.ActiveDocument.ActiveObject.Label="Holes"
        Holes_name=FreeCAD.ActiveDocument.ActiveObject.Name
        #say(Holes_name)
        FreeCADGui.ActiveDocument.ActiveObject.ShapeColor = (0.67,1.00,0.50)
        FreeCADGui.ActiveDocument.ActiveObject.Transparency = 70
        #THPs = Part.makeCompound(THPList)
        #THPs = Part.makeSolid(THPs) ##evaluate solid
        #Part.show(THPs)
        THPs = FreeCAD.ActiveDocument.addObject("Part::FeaturePython","THPs")
        #THPs.Label="THPs"
        THPs_name=THPs.Name
        THPs.addProperty("App::PropertyBool","fixedPosition","importPart")
        THPs.Shape = Part.makeCompound(THPList) #TopPadsBase.Shape.copy()
        #THPs = Part.makeSolid(THPs)
        THPs.ViewObject.Proxy=0
        THPs.fixedPosition = True
        #say(FreeCAD.ActiveDocument.ActiveObject.Name)
        FreeCAD.ActiveDocument.ActiveObject.Label="PTHs"
        THPs_name=FreeCAD.ActiveDocument.ActiveObject.Name
        #say(Holes_name)
        FreeCADGui.ActiveDocument.ActiveObject.ShapeColor = (0.67,1.00,0.50)
        FreeCADGui.ActiveDocument.ActiveObject.Transparency = 70

    fp_group=FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroup", footprint_name+'fp')
    say(fp_group.Label)
    some_element = False
    list=[]
    if len(FCrtYd)>0:
        obj6 = FreeCAD.ActiveDocument.getObject(FCrtYd_name)
        list.append(FCrtYd_name)
        fp_group.addObject(obj6)
        some_element = True
    if len(FFab)>0:
        obj7 = FreeCAD.ActiveDocument.getObject(FFab_name)
        list.append(FFab_name)
        fp_group.addObject(obj7)
        some_element = True
    if len(FrontSilk)>0:
        obj2 = FreeCAD.ActiveDocument.getObject(FSilk_name)
        list.append(FSilk_name)
        fp_group.addObject(obj2)
        some_element = True
    if len(BCrtYd)>0:
        obj6 = FreeCAD.ActiveDocument.getObject(BCrtYd_name)
        list.append(BCrtYd_name)
        fp_group.addObject(obj6)
        some_element = True
    if len(BFab)>0:
        obj7 = FreeCAD.ActiveDocument.getObject(BFab_name)
        list.append(BFab_name)
        fp_group.addObject(obj7)
        some_element = True
    if len(BotSilk)>0:
        obj2 = FreeCAD.ActiveDocument.getObject(BSilk_name)
        list.append(BSilk_name)
        fp_group.addObject(obj2)
        some_element = True
    if len(EdgeCuts)>0:
        obj2 = FreeCAD.ActiveDocument.getObject(ECuts_name)
        list.append(ECuts_name)
        fp_group.addObject(obj2)
        some_element = True
    if len(TopPadList)>0:
        obj3 = FreeCAD.ActiveDocument.getObject(TopPads_name)
        fp_group.addObject(obj3)
        list.append(TopPads_name)
        some_element = True
    if len(BotPadList)>0:
        obj4 = FreeCAD.ActiveDocument.getObject(BotPads_name)
        fp_group.addObject(obj4)
        list.append(BotPads_name)
        some_element = True
    if len(TopNetTieList)>0:
        obj_3 = FreeCAD.ActiveDocument.getObject(TopNetTie_name)
        fp_group.addObject(obj_3)
        list.append(TopNetTie_name)
        some_element = True
    if len(BotNetTieList)>0:
        obj_4 = FreeCAD.ActiveDocument.getObject(BotNetTie_name)
        fp_group.addObject(obj_4)
        list.append(BotNetTie_name)
        some_element = True
    #objFp=Part.makeCompound(list)
    #Part.show(objFp)
    #say(list)
    if some_element:    
        doc=FreeCAD.ActiveDocument
        fp_objs=[]
        list1=[]
        for obj in fp_group.Group:
            #if (obj.Label==fp_group.Label):
            #FreeCADGui.Selection.addSelection(obj)
            shape=obj.Shape.copy()
            #shape_name=FreeCAD.ActiveDocument.ActiveObject.Name
            list1.append(shape)
            #Part.show(shape)
            fp_objs.append(obj)
            #say("added")
            #
        #fp_objs.copy
        #objFp=Part.makeCompound(shape)
        objFp=Part.makeCompound(list1)
        Part.show(objFp)
        
        obj = FreeCAD.ActiveDocument.ActiveObject
        #say("h")
        FreeCADGui.Selection.addSelection(obj)            # select the object
        createSolidBBox2(obj)
        bbox=FreeCAD.ActiveDocument.ActiveObject
        FreeCAD.ActiveDocument.ActiveObject.Label ="Pcb_solid"
        pcb_solid_name=FreeCAD.ActiveDocument.ActiveObject.Name
        FreeCAD.ActiveDocument.removeObject(obj.Name)
    
        #FreeCADGui.ActiveDocument.getObject(bbox.Name).BoundingBox = True
        FreeCADGui.ActiveDocument.ActiveObject.ShapeColor = (0.664,0.664,0.496)
        FreeCADGui.ActiveDocument.ActiveObject.Transparency = 80
        #obj6 = FreeCAD.ActiveDocument.getObject(bbox.Name)
        fp_group.addObject(bbox)
        
        if len(HoleList)>0:
            cut_base = FreeCAD.ActiveDocument.getObject(pcb_solid_name).Shape
            for drill in HoleList:
                #Holes = Part.makeCompound(HoleList)
                hole = Part.makeSolid(drill)
                #Part.show(hole)
                #hole_name=FreeCAD.ActiveDocument.ActiveObject.Name
                #cutter = FreeCAD.ActiveDocument.getObject(hole_name).Shape
                cut_base=cut_base.cut(hole)
            Part.show(cut_base)
            pcb_name=FreeCAD.ActiveDocument.ActiveObject.Name
            FreeCAD.ActiveDocument.ActiveObject.Label ="Pcb-base"
            FreeCADGui.ActiveDocument.ActiveObject.ShapeColor = (0.664,0.664,0.496)
            FreeCADGui.ActiveDocument.ActiveObject.Transparency = 80
            #say("cut")
            pcb=FreeCAD.ActiveDocument.ActiveObject
            fp_group.addObject(pcb)
            #say("added")
            #FreeCAD.activeDocument().recompute()
            FreeCAD.ActiveDocument.removeObject(pcb_solid_name)
            if len(TopPadList)>0:
                FreeCAD.ActiveDocument.getObject(TopPads_name).Label = "TopPads_"
                cut_base = FreeCAD.ActiveDocument.getObject(TopPads_name).Shape
                holes=FreeCAD.ActiveDocument.getObject(Holes_name)
                cut_base=cut_base.cut(holes.Shape)
                Part.show(cut_base)
                Pads_top_name=FreeCAD.ActiveDocument.ActiveObject.Name
                FreeCAD.ActiveDocument.ActiveObject.Label = "TopPads"
                FreeCADGui.ActiveDocument.ActiveObject.ShapeColor = (0.664,0.664,0.496)
                FreeCADGui.ActiveDocument.ActiveObject.Transparency = 80
                #say("cut")
                Pads_top=FreeCAD.ActiveDocument.ActiveObject
                fp_group.addObject(Pads_top)
                #say("added")
                #FreeCAD.activeDocument().recompute()
                FreeCAD.ActiveDocument.removeObject(TopPads_name)
            if len(BotPadList)>0:
                cut_base = FreeCAD.ActiveDocument.getObject(BotPads_name).Shape
                FreeCAD.ActiveDocument.getObject(BotPads_name).Label = "BotPads_"
                holes=FreeCAD.ActiveDocument.getObject(Holes_name)
                cut_base=cut_base.cut(holes.Shape)
                Part.show(cut_base)
                Pads_bot_name=FreeCAD.ActiveDocument.ActiveObject.Name
                FreeCAD.ActiveDocument.ActiveObject.Label = "BotPads"
                FreeCADGui.ActiveDocument.ActiveObject.ShapeColor = (0.664,0.664,0.496)
                FreeCADGui.ActiveDocument.ActiveObject.Transparency = 80
                #say("cut")
                Pads_bot=FreeCAD.ActiveDocument.ActiveObject
                fp_group.addObject(Pads_bot)
                #say("added")
                #FreeCAD.activeDocument().recompute()
                FreeCAD.ActiveDocument.removeObject(BotPads_name)
    
            if len(TopNetTieList)>0:
                FreeCAD.ActiveDocument.getObject(TopNetTie_name).Label = "TopNetTie_"
                cut_base = FreeCAD.ActiveDocument.getObject(TopNetTie_name).Shape
                holes=FreeCAD.ActiveDocument.getObject(Holes_name)
                cut_base=cut_base.cut(holes.Shape)
                Part.show(cut_base)
                NetTie_top_name=FreeCAD.ActiveDocument.ActiveObject.Name
                FreeCAD.ActiveDocument.ActiveObject.Label = "TopNetTie"
                FreeCADGui.ActiveDocument.ActiveObject.ShapeColor = (0.664,0.664,0.496)
                FreeCADGui.ActiveDocument.ActiveObject.Transparency = 80
                #say("cut")
                NetTie_top=FreeCAD.ActiveDocument.ActiveObject
                fp_group.addObject(NetTie_top)
                #say("added")
                #FreeCAD.activeDocument().recompute()
                FreeCAD.ActiveDocument.removeObject(TopNetTie_name)
            if len(BotNetTieList)>0:
                FreeCAD.ActiveDocument.getObject(BotNetTie_name).Label = "BotNetTie_"
                cut_base = FreeCAD.ActiveDocument.getObject(BotNetTie_name).Shape
                holes=FreeCAD.ActiveDocument.getObject(Holes_name)
                cut_base=cut_base.cut(holes.Shape)
                Part.show(cut_base)
                NetTie_bot_name=FreeCAD.ActiveDocument.ActiveObject.Name
                FreeCAD.ActiveDocument.ActiveObject.Label = "BotNetTie"
                FreeCADGui.ActiveDocument.ActiveObject.ShapeColor = (0.664,0.664,0.496)
                FreeCADGui.ActiveDocument.ActiveObject.Transparency = 80
                #say("cut")
                NetTie_bot=FreeCAD.ActiveDocument.ActiveObject
                fp_group.addObject(NetTie_bot)
                #say("added")
                #FreeCAD.activeDocument().recompute()
                FreeCAD.ActiveDocument.removeObject(BotNetTie_name)
    
            obj5 = FreeCAD.ActiveDocument.getObject(Holes_name)
            fp_group.addObject(obj5)
            list.append(Holes_name)
            obj6 = FreeCAD.ActiveDocument.getObject(THPs_name)
            fp_group.addObject(obj6)
            list.append(THPs_name)
            FreeCAD.ActiveDocument.removeObject(Holes_name)
    
        else:
            pcb=FreeCAD.ActiveDocument.ActiveObject    
        # copying pcb to FeaturePython to assign fixedPosition for assembly2
        Pcb_obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython","newPCB")
        Pcb_obj.Label="Pcb"
        Pcb_obj.addProperty("App::PropertyBool","fixedPosition","importPart")
        Pcb_obj.Shape = pcb.Shape.copy()
        Pcb_obj.ViewObject.Proxy=0
        # for p in pcb.ViewObject.PropertiesList: #assuming that the user may change the appearance of parts differently depending on the assembly.
        #     if hasattr(Pcb_obj.ViewObject, p) and p not in ['DiffuseColor']:
        #         setattr(Pcb_obj.ViewObject, p, getattr(pcb.ViewObject, p))
        Pcb_obj.ViewObject.DiffuseColor = pcb.ViewObject.DiffuseColor
        Pcb_obj.fixedPosition = True
        fp_group.addObject(Pcb_obj)
        # workaround for FC 0.17 OCC 7 (double change transparency)
        # FreeCADGui.ActiveDocument.getObject("newPCB").Transparency = 79
        # FreeCADGui.ActiveDocument.getObject("newPCB").Transparency = 80
        # workaround for FC 0.17 OCC 7 (double change transparency)
        FreeCADGui.ActiveDocument.ActiveObject.Transparency = 79
        FreeCADGui.ActiveDocument.ActiveObject.Transparency = 80
        FreeCAD.ActiveDocument.removeObject(pcb.Name)
        
        list2=[]
        list2_objs=[]
        for obj in fp_group.Group:
            # do what you want to automate
            #if (obj.Label==fp_group.Label):
            #FreeCADGui.Selection.addSelection(obj)
            shape=obj.Shape.copy()
            #shape_name=FreeCAD.ActiveDocument.ActiveObject.Name
            list2.append(shape)
            #Part.show(shape)
            list2_objs.append(obj)
            #say("added")
        #say(list2)
        #say('here1')
    
        #Draft.rotate(list2_objs,90.0,FreeCAD.Vector(0.0,0.0,0.0),axis=FreeCAD.Vector(-0.0,-0.0,1.0),copy=False)
        #say('here1')
    
        rot=[0,0,rot_wrl]
        rotateObjs(list2_objs, rot)
    
        for obj in fp_group.Group:
            FreeCADGui.Selection.removeSelection(obj)
        #say('here2')
        FreeCAD.activeDocument().recompute()
        if len(sys.argv)<4:
            #sayerr("view fitting3")
            #sayerr(sys.argv)
            if (zfit):
                FreeCADGui.SendMsgToActiveView("ViewFit")
        #pads_found=getPadsList(content)
    else:
        sayerr('internal layers not supported or fotprint empty')
    doc.commitTransaction()
    say('closing Transaction \'opening_kicad_footprint\'')
###

def routineDrawIDF(doc,filename):
    """process_emn(document, filename)-> adds emn geometry from emn file"""
    global start_time
    msg='IDF_ImporterVersion='+IDF_ImporterVersion
    say(msg)
    #emnfile=pythonopen(filename, "r")
    emnfile=pythonopen(filename, "rb")
    emn_unit=1.0 #presume millimeter like emn unit
    emn_version=2 #presume emn_version 2
    board_thickness=0 #presume 0 board height
    board_outline=[] #no outline
    drills=[] #no drills
    placement=[] #no placement
    place_item=[] #empty place item
    emnlines=emnfile.readlines()
    emnfile.close()   
    passed_sections=[]
    current_section=""
    section_counter=0
    ignore_hole_size=min_drill_size
    #say((emnlines))
    for emnline in emnlines:
        emnrecords=split_records(emnline)
        if len( emnrecords )==0 : continue
        if len( emnrecords[0] )>4 and emnrecords[0][0:4]==".END":
            passed_sections.append(current_section)
            current_section=""
        elif emnrecords[0][0]==".":
            current_section=emnrecords[0]
            section_counter=0
        section_counter+=1
        if current_section==".HEADER"  and section_counter==2:
            emn_version=int(float(emnrecords[1]))
            say("Emn version: "+emnrecords[1])
        if current_section==".HEADER"  and section_counter==3 and emnrecords[1]=="THOU":
            emn_unit=0.0254
            say("UNIT THOU" )
        if current_section==".HEADER"  and section_counter==3 and emnrecords[1]=="TNM":
            emn_unit=0.000010
            say("TNM" )
        if current_section==".BOARD_OUTLINE"  and section_counter==2:
            board_thickness=emn_unit*float(emnrecords[0])
            say("Found board thickness "+emnrecords[0])
        if current_section==".BOARD_OUTLINE"  and section_counter>2:
            board_outline.append([int(emnrecords[0]),float(emnrecords[1])*emn_unit,float(emnrecords[2])*emn_unit,float(emnrecords[3])])
        if current_section==".DRILLED_HOLES"  and section_counter>1 and float(emnrecords[0])*emn_unit>ignore_hole_size:
            drills.append([float(emnrecords[0])*emn_unit,float(emnrecords[1])*emn_unit,float(emnrecords[2])*emn_unit])
        if current_section==".PLACEMENT"  and section_counter>1 and fmod(section_counter,2)==0:
            place_item=[]
            place_item.append(emnrecords[2]) #Reference designator
            place_item.append(emnrecords[1]) #Component part number
            place_item.append(emnrecords[0]) #Package name
        if current_section==".PLACEMENT"  and section_counter>1 and fmod(section_counter,2)==1:
            place_item.append(float(emnrecords[0])*emn_unit) #X
            place_item.append(float(emnrecords[1])*emn_unit) #Y
            if emn_version==3:
                place_item.append(float(emnrecords[2])*emn_unit) #Z  maui
                #say("\nZ="+(str(float(emnrecords[2]))))   
            place_item.append(float(emnrecords[emn_version])) #Rotation
            place_item.append(emnrecords[emn_version+1]) #Side
            place_item.append(emnrecords[emn_version+2]) #Place Status
            say(str(place_item))
            placement.append(place_item)
        
    say("\n".join(passed_sections))
    #say(board_outline)
    say("Proceed "+str(Process_board_outline(doc,board_outline,drills,board_thickness))+" outlines")
    ## place_steps(doc,placement,board_thickness)
    
###
def Process_board_outline(doc,board_outline,drills,board_thickness):
    """Process_board_outline(doc,board_outline,drills,board_thickness)-> number proccesed loops
        adds emn geometry from emn file"""
    global start_time, use_AppPart, force_oldGroups, use_Links, use_LinkGroups
    
    vertex_index=-1; #presume no vertex
    lines=-1 #presume no lines
    out_shape=[]
    out_face=[]
    for point in board_outline:
        vertex=Base.Vector(point[1],point[2],0) 
        vertex_index+=1
        if vertex_index==0:
            lines=point[0] 
        elif lines==point[0]:
            if point[3]!=0 and point[3]!=360:
                out_shape.append(Part.Arc(prev_vertex,mid_point(prev_vertex,vertex,point[3]),vertex))
                #say("mid point "+str(mid_point))
            elif point[3]==360:
                per_point=Per_point(prev_vertex,vertex)
                out_shape.append(Part.Arc(per_point,mid_point(per_point,vertex,point[3]/2),vertex))
                out_shape.append(Part.Arc(per_point,mid_point(per_point,vertex,-point[3]/2),vertex))
            else:
                out_shape.append(PLine(prev_vertex,vertex))
        else:
            out_shape=Part.Shape(out_shape)
            out_shape=Part.Wire(out_shape.Edges)
            out_face.append(Part.Face(out_shape))
            out_shape=[]
            vertex_index=0 
            lines=point[0] 
        prev_vertex=vertex
    if lines!=-1:
        out_shape=Part.Shape(out_shape)
        out_shape=Part.Wire(out_shape.Edges)
        out_face.append(Part.Face(out_shape))
        outline=out_face[0]
        say("Added outline")
        if len(out_face)>1:
            say("Cutting shape inside outline")
            for otl_cut in out_face[1: ]:
                outline=outline.cut(otl_cut)
                #say("Cutting shape inside outline")
        if len(drills)>0:
            say("Cutting holes inside outline")
        for drill in drills:
            #say("Cutting hole inside outline")
            out_shape=Part.makeCircle(drill[0]/2, Base.Vector(drill[1],drill[2],0))
            out_shape=Part.Wire(out_shape.Edges)
            outline=outline.cut(Part.Face(out_shape))
        doc_outline=doc.addObject("Part::Feature","Pcb")
        doc_outline.Shape=outline 
        #FreeCADGui.Selection.addSelection(doc_outline)
        #FreeCADGui.runCommand("Draft_Upgrade")
        #outline=FreeCAD.ActiveDocument.getObject("Union").Shape
        #FreeCAD.ActiveDocument.removeObject("Union")
        #doc_outline=doc.addObject("Part::Feature","Board_outline")
        doc_outline.Shape=outline.extrude(Base.Vector(0,0,-board_thickness))
        if use_AppPart and not force_oldGroups:
            #sayw("creating hierarchy")
            ## to evaluate to add App::Part hierarchy
            doc.Tip = doc.addObject('App::Part','Board_Geoms')
            doc.Board_Geoms.Label = 'Board_Geoms'
            try:
                doc.Board_Geoms.License = ''
                doc.Board_Geoms.LicenseURL = ''
            except:
                pass
            grp=doc.Board_Geoms
            #FreeCADGui.activeView().setActiveObject('Board_Geoms', doc.Board_Geoms)
            ## end hierarchy
        else:
            #sayerr("creating flat groups")
            grp=doc.addObject("App::DocumentObjectGroup", "Board_Geoms")
        grp.addObject(doc_outline)
        #grp.addObject(Sketch)
        doc.Pcb.ViewObject.ShapeColor = (colr,colg,colb)
        say_time()
        #say(str(start_time));say('*'+str(end_milli_time)+'start-end')
        FreeCADGui.activeDocument().activeView().viewAxometric()
        if (zfit):
            FreeCADGui.SendMsgToActiveView("ViewFit")
        #doc.Pcb.ViewObject.ShapeColor=(0.0, 0.5, 0.0, 0.0)
    return lines+1


###
def split_records(line_record):
    """split_records(line_record)-> list of strings(records)
       
       standard separator list separator is space, records containing encapsulated by " """
    split_result=[]
    quote_pos=line_record.find('"')
    while quote_pos!=-1:
        if quote_pos>0:
            split_result.extend(line_record[ :quote_pos].split())
            line_record=line_record[quote_pos: ]
            quote_pos=line_record.find('"',1)
        else: 
            quote_pos=line_record.find('"',1)
        if quote_pos!=-1:
            split_result.append(line_record[ :quote_pos+1])
            line_record=line_record[quote_pos+1: ]
        else:
            split_result.append(line_record) 
            line_record=""
        quote_pos=line_record.find('"')
    split_result.extend(line_record.split())
    return split_result
###
def findWires(edges):
    def verts(shape):
        return [shape.Vertexes[0].Point,shape.Vertexes[-1].Point]
    def group(shapes):
        shapesIn = shapes[:]
        pointTst = []
        pointOut =[]
        for s in shapesIn :
            pointTst=pointTst+[s.Vertexes[0].Point]
            pointTst=pointTst+[s.Vertexes[-1].Point]
        say( pointTst )
        changed = False
        for s in shapesIn:
            if len(s.Vertexes) < 2:
                say( "one vertex, its a circle, just add" )
            else:                             
                for v in verts(s):
                    twoDot=0
                    for vv in pointTst:
                        if v == vv:
                            twoDot=twoDot+1                           
                        if v==vv and twoDot==2 :                   
                            changed = True
                            say( "found matching vert" )
                            break
                        if twoDot<2:
                            say( "didn't find any matching vert..." )
                            pointOut.append(v)
                            say( "Dots non connected"); say(pointOut)
        return(changed,pointOut)
    def joint(point):
        for p in range(len(point)/2) :
            say(point)
            deltI=Part.Vertex(100,100,100).Point
            pos=1
            for pp in range(len(point)-1) :
                say( "position:") ;say( pp+1 )
                if len(point)-1>1:
                    deltN=(point[0]-point[pp+1])
                    if deltN.Length<deltI.Length:
                        deltI=deltN
                        pos=pp+1
                        say( "changement" );say( pos )
                else:
                    pos=1   
            say(  "points a joindre");say(point[0]);say( point[pos] )
            if point[0]!=point[pos]:
                Part.show(Part.makePolygon([point[0],point[pos]]))
            else:
                say( "WARNING les points ont la meme valeurs " )
            point.pop(0)
            point.pop(pos-1)
        point=0 #to have a return normally void
        return(point)
    working = True
    edgeSet = edges
    result = group(edgeSet)
    working = result[0]
    edgeSet = result[1]
    joint(result[1])
    return result[1] 
#

def distance(p0, p1):
    return sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)
#
class OSCD2Dg_Overlappingfaces():
    '''combines overlapping faces together'''
    def __init__(self,facelist):
        self.sortedfaces = sorted(facelist,key=(lambda shape: shape.Area),reverse=True)
        self.builddepdict()
        #self.faceindex = {}
        #for idx,face in enumerate(self.sortesfaces):
        #    self.faceindex[face.hashCode()] = idx

#    def __len__(self):
#        return len(self.sortedfaces)

    @staticmethod
    def dofacesoverlapboundbox(bigface,smallface):
        return bigface.BoundBox.isIntersection(smallface.BoundBox)

    @staticmethod
    def dofacesoverlapallverts(bigface,smallface):
        def vertsinface(f1,verts,tol=0.001,inface=True):
            '''check if all given verts are inside shape f1'''
            return all([f1.isInside(vert.Point,tol,inface) for vert in verts])
        return vertsinface(bigface,smallface.Vertexes)

    @staticmethod
    def dofacesoverlapproximity(bigface,smallface):
        l1,l2 = bigface.proximity(smallface)
        return len(l1) > 0 or len(l2) > 0

    @staticmethod
    def dofacesoverlapboolean(bigface,smallface):
        #import FreeCAD,FreeCADGui
        #FreeCAD.Console.PrintLog('intersecting %d %d\n'%(bigfacei,smallfacei))
        #FreeCADGui.updateGui()
        return bigface.common(smallface).Area > 0

    def builddepdict(self):
        import Part
        import itertools
        #isinsidelist = []
        self.isinsidedict = {}
        #for bigface, smallface in itertools.combinations(sortedfaces,2):
        for bigfacei, smallfacei in\
                itertools.combinations(range(len(self.sortedfaces)),2):
            try:
                overlap = OSCD2Dg_Overlappingfaces.dofacesoverlapproximity(\
                        self.sortedfaces[bigfacei],self.sortedfaces[smallfacei])
            except (NotImplementedError, Part.OCCError) as e:
                try:
                    overlap = OSCD2Dg_Overlappingfaces.dofacesoverlapboolean(\
                            self.sortedfaces[bigfacei],\
                            self.sortedfaces[smallfacei])
                except Part.OCCError:
                    overlap = OSCD2Dg_Overlappingfaces.dofacesoverlapallverts(\
                            self.sortedfaces[bigfacei],\
                            self.sortedfaces[smallfacei])
            if overlap:
                #isinsidelist.append((bigfacei,smallfacei))
                smallinbig = self.isinsidedict.get(bigfacei,[])
                smallinbig.append(smallfacei)
                if len(smallinbig) == 1:
                    self.isinsidedict[bigfacei] = smallinbig

    @staticmethod
    def finddepth(dict1,faceidx,curdepth=0):
        if faceidx not in dict1:
            return curdepth+1
        else:
        #print dict1[faceidx],[(finddepth(dict1,childface,curdepth)) for childface in dict1[faceidx]]
            return max([(OSCD2Dg_Overlappingfaces.finddepth(dict1,childface,curdepth+1)) for childface in dict1[faceidx]])

    def findrootdepth(self):
        return max([OSCD2Dg_Overlappingfaces.finddepth(self.isinsidedict,fi) for fi in range(len(self.sortedfaces))])

    def hasnoparent(self,faceindex):
        return OSCD2Dg_Overlappingfaces.hasnoparentstatic(self.isinsidedict,faceindex)

    @staticmethod
    def hasnoparentstatic(isinsidedict,faceindex):
        if (sys.version_info > (3, 0)):  #py3
            for smalllist in isinsidedict.values():
                if faceindex in smalllist:
                    return False
        else:   #py2
            for smalllist in isinsidedict.itervalues():
                if faceindex in smalllist:
                    return False
        return True

    #@staticmethod
    #def subtreedict(rootface,parantdict):
    #    '''biuld a subtree dictinary'''
    #    newdict = parantdict.copy()
    #    del newdict[rootface]
    #    return newdict

    @staticmethod
    def directchildren(isinsidedict,parent):
        #return [child for child in isinsidedict.get(parent,[]) if child not in isinsidedict]
        dchildren=[]
        for child in isinsidedict.get(parent,[]):
            direct = True
            import sys
            if sys.version_info[0] == 2: #if py2:
                #print('py2')
                py2=True
            else:
                py2=False
            if py2:
                for key, value in isinsidedict.iteritems():
                    if key != parent and child in value and parent not in value:
                        direct = False
            else:
                for key, value in isinsidedict.items():
                    if key != parent and child in value and parent not in value:
                        direct = False            
            if direct:
                dchildren.append(child)
        return dchildren

    #@staticmethod
    #def indirectchildren(isinsidedict,parent):
     #   return [child for child in isinsidedict.get(parent,[]) if child in isinsidedict]

    @staticmethod
    def printtree(isinsidedict,facenum):
        def printtreechild(isinsidedict,facenum,parent):
            children=OSCD2Dg_Overlappingfaces.directchildren(isinsidedict,parent)
            #say 'parent %d directchild %s' % (parent,children)
            if children:
                subdict=isinsidedict.copy()
                del subdict[parent]
                for child in children:
                        printtreechild(subdict,facenum,child)

        rootitems=[fi for fi in range(facenum) if OSCD2Dg_Overlappingfaces.hasnoparentstatic(isinsidedict,fi)]
        for rootitem in rootitems:
            printtreechild(isinsidedict,facenum,rootitem)

    def makefeatures(self,doc):
        import FreeCAD
        def addshape(faceindex):
            obj=doc.addObject('Part::Feature','facefromedges_%d' % faceindex)
            obj.Shape = self.sortedfaces[faceindex]
            obj.ViewObject.hide()
            return obj

        def addfeature(faceindex,isinsidedict):
            directchildren = OSCD2Dg_Overlappingfaces.directchildren(isinsidedict,faceindex)
            if len(directchildren) == 0:
                obj=addshape(faceindex)
            else:
                subdict=isinsidedict.copy()
                del subdict[faceindex]
                obj=doc.addObject("Part::Cut","facesfromedges_%d" % faceindex)
                obj.Base= addshape(faceindex) #we only do subtraction
                if len(directchildren) == 1:
                        obj.Tool = addfeature(directchildren[0],subdict)
                else:
                        obj.Tool = doc.addObject("Part::MultiFuse",\
                                "facesfromedges_union")
                        obj.Tool.Shapes = [addfeature(child,subdict)\
                                for child in directchildren]
                        obj.Tool.ViewObject.hide()
            obj.ViewObject.hide()
            return obj

        rootitems = [fi for fi in range(len(self.sortedfaces)) if self.hasnoparent(fi)]
        for rootitem in rootitems:
            addfeature(rootitem,self.isinsidedict).ViewObject.show()


    def makeshape(self):
        def removefaces(rfaces):
            for tfi in directchildren[::-1]:
                finishedwith.append(tfi)
                #del faces[tfi]
                if tfi in isinsidedict:
                    del isinsidedict[tfi]
                if (sys.version_info > (3, 0)):  #py3
                    for key,value in isinsidedict.items():
                        if tfi in value:
                            newlist=value[:] #we work on a shallow copy of isinsidedict
                            newlist.remove(tfi)
                            isinsidedict[key]=newlist
                else:  #py2
                    for key,value in isinsidedict.iteritems():
                        if tfi in value:
                            newlist=value[:] #we work on a shallow copy of isinsidedict
                            newlist.remove(tfi)
                            isinsidedict[key]=newlist
               
        def hasnoparent(faceindex):
            if (sys.version_info > (3, 0)):  #py3
                for smalllist in self.isinsidedict.values():
                    if faceindex in smalllist:
                        return False
            else:  #py2
                for smalllist in self.isinsidedict.itervalues():
                    if faceindex in smalllist:
                        return False            
            return True

        faces=self.sortedfaces[:]
        isinsidedict=self.isinsidedict.copy()
        finishedwith=[]
        while not all([OSCD2Dg_Overlappingfaces.hasnoparentstatic(isinsidedict,fi) for fi in range(len(faces))]):
            #print [(Overlappingfaces.hasnoparentstatic(isinsidedict,fi),\
                #Overlappingfaces.directchildren(isinsidedict,fi)) for fi in range(len(faces))]
            for fi in range(len(faces))[::-1]:
                directchildren = OSCD2Dg_Overlappingfaces.directchildren(isinsidedict,fi)
                if not directchildren:
                    continue
                elif len(directchildren) == 1:
                    faces[fi]=faces[fi].cut(faces[directchildren[0]])
                    #print fi,'-' ,directchildren[0], faces[fi],faces[directchildren[0]]
                    removefaces(directchildren)
                else:
                    toolface=OSCD2Dg_fusefaces([faces[tfi] for tfi in directchildren])
                    faces[fi]=faces[fi].cut(toolface)
                    #print fi, '- ()', directchildren, [faces[tfi] for tfi in directchildren]
                    removefaces(directchildren)
                #print fi,directchildren
        faces =[face for index,face in enumerate(faces) if index not in finishedwith]
#        return faces
        return OSCD2Dg_fusefaces(faces)
#   
def OSCD2Dg_superWireReverse(debuglist,closed=False):
    '''superWireReverse(debuglist,[closed]): forces a wire between edges
    that don't necessarily have coincident endpoints. If closed=True, wire
    will always be closed. debuglist has a tuple for every edge.The first
    entry is the edge, the second is the flag 'does not need to be inverted'
    '''
    #taken from draftlibs
    sayerr('edges not closed... trying to solve it')
    def median(v1,v2):
        vd = v2.sub(v1)
        vd.scale(.5,.5,.5)
        return v1.add(vd)
    try:
        from DraftGeomUtils import findMidpoint
    except ImportError: #workaround for Version 0.12
        from draftlibs.fcgeo import findMidpoint #workaround for Version 0.12
    import Part
    #edges = sortEdges(edgeslist)
    # print "here 7"
    # print debuglist
    newedges = []
    edge_added=False
    for i in range(len(debuglist)):
        curr = debuglist[i]
        if i == 0:
            if closed:
                prev = debuglist[-1]
            else:
                prev = None
        else:
            prev = debuglist[i-1]
            #print "prev=",prev
        if i == (len(debuglist)-1):
            if closed:
                nexte = debuglist[0]
            else:
                nexte = None
        else:
            nexte = debuglist[i+1]
        # print i,prev,curr,nexte
        # print "here loop"
        if prev:
            if curr[0].Vertexes[-1*(not curr[1])].Point == \
                    prev[0].Vertexes[-1*prev[1]].Point:
                p1 = curr[0].Vertexes[-1*(not curr[1])].Point
            else:
                p1 = median(curr[0].Vertexes[-1*(not curr[1])].Point,\
                        prev[0].Vertexes[-1*prev[1]].Point)
        else:
            p1 = curr[0].Vertexes[-1*(not curr[1])].Point
        if nexte:
            if curr[0].Vertexes[-1*curr[1]].Point == \
                nexte[0].Vertexes[-1*(not nexte[1])].Point:
                p2 = nexte[0].Vertexes[-1*(not nexte[1])].Point
            else:
                p2 = median(curr[0].Vertexes[-1*(curr[1])].Point,\
                        nexte[0].Vertexes[-1*(not nexte[1])].Point)
        else:
            p2 = curr[0].Vertexes[-1*(curr[1])].Point
        # print "here 8"
        # print "curr[0].Curve ",curr[0].Curve
        if hasattr(Part,"LineSegment"):
            if isinstance(curr[0].Curve,Part.Line) or isinstance(curr[0].Curve,Part.LineSegment):
                #print "line",p1,p2
                newedges.append(Part.LineSegment(p1,p2).toShape())
                edge_added=True
        elif hasattr(Part,"Line"):
            if isinstance(curr[0].Curve,Part.Line):
                #print "line",p1,p2
                newedges.append(Part.Line(p1,p2).toShape())
                edge_added=True
        if isinstance(curr[0].Curve,Part.Circle):
            p3 = findMidpoint(curr[0])
            #print "arc",p1,p3,p2
            newedges.append(Part.Arc(p1,p3,p2).toShape())
            edge_added=True
        #else:
        if not edge_added:
            say( "Cannot superWire edges that are not lines or arcs" )
            return None
    # print newedges
    return Part.Wire(newedges)
#
def OSCD2Dg_endpointdistance(edges):
    '''return the distance of of vertices in path (list of edges) as
    maximum, minimum and distance between start and endpoint
    it expects the edges to be traversed forward from starting from Vertex 0'''
    numedges=len(edges)
    if numedges == 1 and len(edges[0].Vertexes) == 1:
            return 0.0,0.0,0.0
    outerdistance = edges[0].Vertexes[0].Point.sub(\
        edges[-1].Vertexes[-1].Point).Length
    if numedges > 1:
        innerdistances=[edges[i].Vertexes[-1].Point.sub(edges[i+1].\
                Vertexes[0].Point).Length for i in range(numedges-1)]
        return max(innerdistances),min(innerdistances),outerdistance
    else:
        return 0.0,0.0,outerdistance

def OSCD2Dg_endpointdistancedebuglist(debuglist):
    '''return the distance of of vertices in path (list of edges) as
    maximum, minimum and distance between start and endpoint
    it it expects a 'not reversed' flag for every edge'''
    numedges=len(debuglist)
    if numedges == 1 and len(debuglist[0][0].Vertexes) == 1:
            return 0.0,0.0,0.0
    outerdistance = debuglist[0][0].Vertexes[(not debuglist[0][1])*-1].\
            Point.sub(debuglist[-1][0].Vertexes[(debuglist[-1][1])*-1].\
            Point).Length
    if numedges > 1:
        innerdistances=[debuglist[i][0].Vertexes[debuglist[i][1]*-1].\
                Point.sub(debuglist[i+1][0].Vertexes[(not debuglist[i+1][1])*\
                -1].Point).Length for i in range(numedges-1)]
        return max(innerdistances),min(innerdistances),outerdistance
    else:
        return 0.0,0.0,outerdistance
#
def OSCD2Dg_findConnectedEdges(edgelist,eps=1e-6,debug=False):
    '''returns a list of list of connected edges'''

    def vertequals(v1,v2,eps=1e-6):
        '''check two vertices for equality'''
        #return all([abs(c1-c2)<eps for c1,c2 in zip(v1.Point,v2.Point)])
        return v1.Point.sub(v2.Point).Length<eps

    def vertindex(forward):
        '''return index of last or first element'''
        return -1 if forward else 0

    freeedges = edgelist[:]
    retlist = []
    debuglist = []
    while freeedges:
        startwire = freeedges.pop(0)
        forward = True
        newedge = [(startwire,True)]
        for forward in (True, False):
            found = True
            while found:
                lastvert = newedge[vertindex(forward)][0].Vertexes[vertindex(forward == newedge[vertindex(forward)][1])]
                for ceindex, checkedge in enumerate(freeedges):
                    found = False
                    for cvindex, cvert in enumerate([checkedge.Vertexes[0],checkedge.Vertexes[-1]]):
                        if vertequals(lastvert,cvert,eps):
                            if forward:
                                newedge.append((checkedge,cvindex == 0))
                            else:
                                newedge.insert(0,(checkedge,cvindex == 1))
                            del freeedges[ceindex]
                            found = True
                            break
                    else:
                        found = False
                    if found:
                        break
                else:
                    found = False
        #we are finished for this edge
        debuglist.append(newedge)
        retlist.append([item[0] for item in newedge]) #strip off direction
    #print debuglist
    if debug:
        return retlist,debuglist
    else:
        return retlist
#
def OSCD2Dg_subtractfaces(faces):
    '''searches for the biggest face and subtracts all smaller ones from the
    first. Only makes sense if all faces overlap.'''
    if len(faces)==1:
        return faces[0]
    else:
        facelist=sorted(faces,key=(lambda shape: shape.Area),reverse=True)
        base=facelist[0]
        tool=reduce(lambda p1,p2: p1.fuse(p2),facelist[1:])
        return base.cut(tool)
#
def OSCD2Dg_fusefaces(faces):
    if len(faces)==1:
        return faces[0]
    else:
        from functools import reduce
        return reduce(lambda p1,p2: p1.fuse(p2),faces)

#
def OSCD2Dg_subtractfaces2(faces):
    '''Sort faces, check if they overlap. Subtract overlapping face and fuse
    nonoverlapping groups.'''
    return OSCD2Dg_fusefaces([subtractfaces(facegroup) for facegroup in findoverlappingfaces(faces)])
#
def OSCD2Dg_edgestowires(edgelist,eps=0.001):
    '''takes list of edges and returns a list of wires'''
    import Part, Draft
    # todo remove double edges
    # sayerr(eps)     #
    wirelist=[]
    #for path in findConnectedEdges(edgelist,eps=eps):
    for path,debug in zip(*OSCD2Dg_findConnectedEdges(edgelist,eps=eps,debug=True)):
        maxd,mind,outerd = OSCD2Dg_endpointdistancedebuglist(debug)
        assert(maxd <= eps*2) # Assume the input to be broken
        if maxd < eps*2 and maxd > 0.000001: #OCC wont like it if maxd > 0.02:
            # print 'endpointdistance max:%f min:%f, ends:%f' %(maxd,mind,outerd)
            # print "here 5"

            if True:
                tobeclosed = outerd < eps*2
                # OpenSCAD uses 0.001 for corase grid
                #from draftlibs import fcvec, fcgeo
                #w2=fcgeo.superWire(path,tobeclosed)
                #print "here 6a"
                w2=OSCD2Dg_superWireReverse(debug,tobeclosed)
                if w2 is not None:
                    wirelist.append(w2)
            else:#this locks up FreeCAD
                #print "here 6b"
                comp=Part.Compound(path)
                wirelist.append(comp.connectEdgesToWires(False,eps).Wires[0])
                #wirelist.append(comp.connectEdgesToWires(False,0.1).Wires[0])
        else:
            done = False
            try:
                wire=Part.Wire(path)
                #if not close or wire.isClosed or outerd > 0.0001:
                wirelist.append(Part.Wire(path))
                done = True
            except Part.OCCError:
                pass
            if not done:
                comp=Part.Compound(path)
                wirelist.append(comp.connectEdgesToWires(False,eps).Wires[0])
    return wirelist
#
def OSCD2Dg_edgestofaces(edges,algo=3,eps=0.001):
    #edges=[]
    #for shapeobj in (objs):
    #    edges.extend(shapeobj.Shape.Edges)
    #taken from Drafttools
    #from draftlibs import fcvec, fcgeo
    import Part
    #wires = fcgeo.findWires(edges)
    #print "edges: "
    # for e in edges:
    #     print "e.Vertexes: ", e.Vertexes
    #     for p in e.Vertexes:
    #         print "points", p.Point
    # print "here 4"
    wires = OSCD2Dg_edgestowires(edges,eps)
    facel=[]
    for w in wires:
        #assert(len(w.Edges)>1)
        if not w.isClosed():
            p0 = w.Vertexes[0].Point
            p1 = w.Vertexes[-1].Point
            # print "p0",p0," ";print "p1",p1
            edges2 = w.Edges[:]
            try:
                if hasattr(Part,"LineSegment"):
                    edges2.append(Part.LineSegment(p1,p0).toShape())
                else:
                    edges2.append(Part.Line(p1,p0).toShape())
                #edges2.append(Part.LineSegment(p1,p0).toShape())
                w = Part.Wire(edges2)
                #w = Part.Wire(fcgeo.sortEdges(edges2))
            except Part.OCCError:
                comp=Part.Compound(edges2)
                w = comp.connectEdgesToWires(False,eps).Wires[0]
        facel.append(Part.Face(w))
        #if w.isValid: #debugging
        #    facel.append(Part.Face(w))
        #else:
        #    Part.show(w)
    if algo is None:
        return facel
    elif algo == 1: #stabale behavior
        return subtractfaces(facel)
    elif algo == 0: #return all faces
        return Part.Compound(facel)
    elif algo == 2:
        return subtractfaces2(facel)
    elif algo == 3:
        return OSCD2Dg_Overlappingfaces(facel).makeshape()
#

###
def DrawPCB(mypcb,lyr=None,rmv_container=None,keep_sketch=None):
    global start_time, use_AppPart, force_oldGroups, min_drill_size
    global addVirtual, load_sketch, off_x, off_y, aux_orig, grid_orig
    global running_time, conv_offs, use_Links, apply_edge_tolerance, simplifyComSolid
    global zfit, use_LinkGroups, fname_sfx, missingHeight
    
    def simu_distance(p0, p1):
        return max (abs(p0[0] - p1[0]), abs(p0[1] - p1[1]))
    
    import PySide
    import FreeCAD, Part
    from PySide import QtGui, QtCore
    from math import pi
    
    say(sys._getframe().f_code.co_name + "() :PCB Loader ")
    ## NB use always float() to guarantee number not string!!!
    max_edges_admitted = 1500 # after this number, no sketcher would be created
    
    if lyr is None:
        lyr = 'Edge.Cuts'
    #load_sketch=True
    get_time()
    t0=(running_time)
    #say(start_time)
    
    doc=FreeCAD.activeDocument()
    for obj in FreeCAD.ActiveDocument.Objects:
        FreeCADGui.Selection.removeSelection(obj)

    EdgeCuts = []
    EdgeCuts_face = []
    EdgeCuts_shape = []
    PCB = []
    PCB_Models = []
    PCB_Geo = []
    FpEdges_Geo = []
    edges=[]
    PCBs = []
    #print (mypcb.general) #maui errorchecking
    if hasattr(mypcb, 'general'):
        totalHeight=float(mypcb.general.thickness)
    else:
        totalHeight=1.6
    missingHeight = False
    if totalHeight == 0:
        totalHeight = 1.6
        missingHeight = True
        sayerr('pcb thickness = 0mm! CHANGED to 1.6mm Please fix your pcb design!')
    say('pcb thickness '+str(totalHeight)+'mm')
    version=mypcb.version
    say('kicad_pcb version ' +str(version))
    if version < 3:
        QtGui.QApplication.restoreOverrideCursor()
        reply = QtGui.QMessageBox.information(None,"Error ...","... KICAD pcb version "+ str(version)+" not supported \r\n"+"\r\nplease open and save your board with the latest kicad version")
        sys.exit("pcb version not supported")
    elif version==3:
        Edge_Cuts_lvl=28
        Top_lvl=15
    elif version>=4:
        Edge_Cuts_lvl=44
        Top_lvl=0
    conv_offs=1.0
    if version >= 20171114:
        conv_offs=25.4
    #getting pcb version for the internal use of 'virtual' modules
    pcbv = 4
    if version == 20171130:
        pcbv = 5
    elif version == 20211014:
        pcbv = 6
    elif version >= 20220000:
        pcbv = 6.99
    #load_sketch=False
    # sayerr(len(mypcb.gr_line))
    # say(len(mypcb.gr_arc))
    #edg_segms = len(mypcb.gr_line)+len(mypcb.gr_arc)
    edg_segms = 0
    sayw('parsing')
    sk_label = lyr
    if 'Mask' in lyr:
        lyr = lyr[:-4]
        #print(lyr)
    keepout=False
    if 'Fill' in lyr or 'KeepOut' in lyr:
        if 'KeepOut' in lyr:
            keepout=True
        lyr = lyr[:2]+'Cu'
        #print(lyr)
    
    for ln in mypcb.gr_line:
        if lyr in ln.layer:
            #say(ln.layer)
            edg_segms+=1
    for ar in mypcb.gr_arc:
        if lyr in ar.layer:
            #say(ln.layer)
            edg_segms+=1
    for lp in mypcb.gr_poly:
        #print(lp)
        #print(lp.layer)
        #print(lp.pts)
        if lyr in lp.layer:
            #sayerr(lp.layer)
            for p in lp.pts.xy:
                edg_segms+=1
                #sayerr(p)
            #stop
            #edg_segms+=1
    for bs in mypcb.gr_curve:
        if lyr in bs.layer:
            #sayerr(bs.layer)
            for p in bs.pts.xy:
                edg_segms+=1
            #edg_segms+=1
    for r in mypcb.gr_rect:
        if lyr in r.layer:
            #sayerr(bs.layer)
            edg_segms+=4
            #edg_segms+=1
    for zn in mypcb.zone:
        #print (zn,zn.layer,zn.polygon)
        if hasattr(zn,'layer'):
            zlayer=zn.layer
        else:
            zlayer=zn.layers
            for i,l in enumerate(zlayer):
                l=l.replace('"','')
                if isinstance(zlayer, list):
                    zlayer[i]=l
                else:
                    zlayer=l
        if not keepout:
            if lyr in zlayer and not hasattr(zn,'keepout'):
                for p in zn.polygon.pts.xy:
                    edg_segms+=1
        else:
            #print(zlayer,lyr,lyr in zlayer, hasattr(zn,'keepout'))
            if lyr in zlayer and hasattr(zn,'keepout'):
                for p in zn.polygon.pts.xy:
                    edg_segms+=1 
    
    sayw(str(edg_segms)+' edge segments')
    #for lp in mypcb.gr_poly: #pcb polylines
    #    if lp.layer != 'Edge.Cuts':
    #        continue
    if edg_segms > max_edges_admitted:
        sayerr('too many segments ('+str(edg_segms)+'), skipping sketches & constraints')
        # load_sketch = False
    
    if load_sketch:
        PCB_Sketch_draft= FreeCAD.activeDocument().addObject('Sketcher::SketchObject','PCB_Sketch_draft')
        FreeCAD.activeDocument().PCB_Sketch_draft.Placement = FreeCAD.Placement(FreeCAD.Vector(0.000000,0.000000,0.000000),FreeCAD.Rotation(0.000000,0.000000,0.000000,1.000000))            
        
    #stop
    #sayerr(mypcb.layers['0'])
    if hasattr(mypcb, 'layers'):
        for lynbr in mypcb.layers: #getting layers name
            if float(lynbr) == Top_lvl:
                LvlTopName=(mypcb.layers['{0}'.format(str(lynbr))][0])
            if float(lynbr) == Edge_Cuts_lvl:
                LvlEdgeName=(mypcb.layers['{0}'.format(str(lynbr))][0])
    else:
        LvlTopName = 'F.Cu'
        LvlEdgeName = 'Edge.Cuts'
    #    #    sayerr(lyr[0])
    #    #    sayerr('top')
    if hasattr(mypcb, 'general'):
        if hasattr(mypcb.general, 'area'):
            say('board area '+str(mypcb.general.area))
    #sayerr('aux_axis_origin' + str(mypcb.setup.aux_axis_origin))
    #stop
    origin = None
    if hasattr(mypcb, 'setup'):
        if hasattr(mypcb.setup, 'grid_origin'):
            say('grid_origin' + str(mypcb.setup.grid_origin))
            origin = 'grid origin'
            #say(mypcb.setup.aux_axis_origin)
            #xp=mypcb.setup.aux_axis_origin[0]; yp=-mypcb.setup.aux_axis_origin[1]
        elif hasattr(mypcb.setup, 'aux_axis_origin'):
            say('aux_axis_origin' + str(mypcb.setup.aux_axis_origin))
            origin = 'aux origin'
            #say(mypcb.setup.aux_axis_origin)
            #xp=mypcb.setup.aux_axis_origin[0]; yp=-mypcb.setup.aux_axis_origin[1]
        else:
            say('aux or grid origin not found')
            origin = 'grid origin'  #temp workaround for kv6 missing aux origin
    else:
        say('grid origin not set\ndefault value on top left corner')
        origin = 'grid origin'  #temp workaround for kv6 missing aux origin
    #if hasattr(mypcb.setup, 'aux origin'):
    #    say('aux origin' + str(mypcb.setup.aux_axis_origin))
    #else:
    #    say('aux origin not used')
    ## NB use always float() to guarantee number not string!!!
       
    for l in mypcb.gr_line: #pcb lines
        #if l.layer != 'Edge.Cuts':
        if lyr not in l.layer:
            continue
        #edges.append(Part.makeLine(makeVect(l.start),makeVect(l.end)))
        #say(l.start);say(l.end)
        #edge_tolerance_warning
        if simu_distance((l.start[0],-l.start[1],0), ((l.end[0],-l.end[1],0))) > edge_tolerance: #non coincident points
        #if (Base.Vector(l.start[0],-l.start[1],0)) != (Base.Vector(l.end[0],-l.end[1],0)): #non coincident points
            line1=Part.Edge(PLine(Base.Vector(l.start[0],-l.start[1],0), Base.Vector(l.end[0],-l.end[1],0)))
            if load_sketch:
                if aux_orig ==1 or grid_orig ==1:
                    #FreeCAD.ActiveDocument.PCB_Sketch_draft.addGeometry(PLine(Base.Vector(l.start[0]-off_x,-l.start[1]-off_y,0), Base.Vector(l.end[0]-off_x,-l.end[1]-off_y,0)))
                    PCB_Geo.append(PLine(Base.Vector(l.start[0]-off_x,-l.start[1]-off_y,0), Base.Vector(l.end[0]-off_x,-l.end[1]-off_y,0)))
                else:
                    #FreeCAD.ActiveDocument.PCB_Sketch_draft.addGeometry(PLine(Base.Vector(l.start[0],-l.start[1],0), Base.Vector(l.end[0],-l.end[1],0)))
                    PCB_Geo.append(PLine(Base.Vector(l.start[0],-l.start[1],0), Base.Vector(l.end[0],-l.end[1],0)))
            edges.append(line1);
            PCB.append(['Line', l.start[0], -l.start[1], l.end[0], -l.end[1]])
            if show_border:
                Part.show(line1)

    for r in mypcb.gr_rect: #pcb lines from rect
        #if l.layer != 'Edge.Cuts':
        if lyr not in r.layer:
            continue
        #segms = [r.start[0],r.start[1]][r.end[0],r.start[1]]
        line1=Part.Edge(PLine(Base.Vector(r.start[0],-r.start[1],0), Base.Vector(r.end[0],-r.start[1],0)))
        if load_sketch:
            if aux_orig ==1 or grid_orig ==1:
                PCB_Geo.append(PLine(Base.Vector(r.start[0]-off_x,-r.start[1]-off_y,0), Base.Vector(r.end[0]-off_x,-r.start[1]-off_y,0)))
            else:
                PCB_Geo.append(PLine(Base.Vector(r.start[0],-r.start[1],0), Base.Vector(r.end[0],-r.start[1],0)))
        edges.append(line1);
        PCB.append(['Line', r.end[0], -r.start[1], r.end[0], -r.end[1]])
        if show_border:
            Part.show(line1)
        #segms = [r.end[0],r.start[1]][r.end[0],r.end[1]]
        line1=Part.Edge(PLine(Base.Vector(r.end[0],-r.start[1],0), Base.Vector(r.end[0],-r.end[1],0)))
        if load_sketch:
            if aux_orig ==1 or grid_orig ==1:
                PCB_Geo.append(PLine(Base.Vector(r.end[0]-off_x,-r.start[1]-off_y,0), Base.Vector(r.end[0]-off_x,-r.end[1]-off_y,0)))
            else:
                PCB_Geo.append(PLine(Base.Vector(r.end[0],-r.start[1],0), Base.Vector(r.end[0],-r.end[1],0)))
        edges.append(line1);
        PCB.append(['Line', r.end[0], -r.start[1], r.end[0], -r.end[1]])
        if show_border:
            Part.show(line1)
        #segms = [r.end[0],r.end[1]][r.start[0],r.end[1]]
        line1=Part.Edge(PLine(Base.Vector(r.end[0],-r.end[1],0), Base.Vector(r.start[0],-r.end[1],0)))
        if load_sketch:
            if aux_orig ==1 or grid_orig ==1:
                PCB_Geo.append(PLine(Base.Vector(r.end[0]-off_x,-r.end[1]-off_y,0), Base.Vector(r.start[0]-off_x,-r.end[1]-off_y,0)))
            else:
                PCB_Geo.append(PLine(Base.Vector(r.end[0],-r.end[1],0), Base.Vector(r.start[0],-r.end[1],0)))
        edges.append(line1);
        PCB.append(['Line', r.end[0], -r.end[1], r.start[0], -r.end[1]])
        if show_border:
            Part.show(line1)
        #segms = [r.start[0],r.end[1]][r.start[0],r.start[1]]
        line1=Part.Edge(PLine(Base.Vector(r.start[0],-r.end[1],0), Base.Vector(r.start[0],-r.start[1],0)))
        if load_sketch:
            if aux_orig ==1 or grid_orig ==1:
                PCB_Geo.append(PLine(Base.Vector(r.start[0]-off_x,-r.end[1]-off_y,0), Base.Vector(r.start[0]-off_x,-r.start[1]-off_y,0)))
            else:
                PCB_Geo.append(PLine(Base.Vector(r.start[0],-r.end[1],0), Base.Vector(r.start[0],-r.start[1],0)))
        edges.append(line1);
        PCB.append(['Line', r.start[0], -r.end[1], r.start[0], -r.start[1]])
        if show_border:
            Part.show(line1)

    k_index = 0
    for zn in mypcb.zone:
        #print(zn.layer)
        if hasattr(zn,'layer'):
            zlayer=zn.layer
        else:
            zlayer=zn.layers
            for i,l in enumerate(zlayer):
                l=l.replace('"','')
                if isinstance(zlayer, list):
                    zlayer[i]=l
                else:
                    zlayer=l
        # print(lyr[0],zlayer,lyr[0] in zlayer,lyr[0]+'.Cu' in zlayer)
        zl_found = False
        for zl in zlayer:
            if lyr[0]+'.Cu' in zlayer:
                zl_found = True
        if not zl_found:
               continue
        if 'Mask' in lyr and 'Mask' not in zlayer:
            continue
        #print(zn.polygon.pts.xy)
        if not keepout:
            if hasattr(zn,'keepout'):
                continue
        else:
            if not hasattr(zn,'keepout'):
                continue
        ind = 0
        l = len(zn.polygon.pts.xy)
        z_lines = []
        for p in zn.polygon.pts.xy:
            if ind == 0:
                line1=Part.Edge(PLine(Base.Vector(zn.polygon.pts.xy[l-1][0],-zn.polygon.pts.xy[l-1][1],0), Base.Vector(zn.polygon.pts.xy[0][0],-zn.polygon.pts.xy[0][1],0)))
                edges.append(line1);
                if load_sketch:
                    if aux_orig ==1 or grid_orig ==1:
                        #FreeCAD.ActiveDocument.PCB_Sketch_draft.addGeometry(PLine(Base.Vector(l.start[0]-off_x,-l.start[1]-off_y,0), Base.Vector(l.end[0]-off_x,-l.end[1]-off_y,0)))
                        PCB_Geo.append(PLine(Base.Vector(zn.polygon.pts.xy[l-1][0]-off_x,-zn.polygon.pts.xy[l-1][1]-off_y,0), Base.Vector(zn.polygon.pts.xy[0][0]-off_x,-zn.polygon.pts.xy[0][1]-off_y,0)))
                        line2=Part.Edge(PLine(Base.Vector(zn.polygon.pts.xy[l-1][0]-off_x,-zn.polygon.pts.xy[l-1][1]-off_y,0), Base.Vector(zn.polygon.pts.xy[0][0]-off_x,-zn.polygon.pts.xy[0][1]-off_y,0)))
                    else:
                        #FreeCAD.ActiveDocument.PCB_Sketch_draft.addGeometry(PLine(Base.Vector(l.start[0],-l.start[1],0), Base.Vector(l.end[0],-l.end[1],0)))
                        PCB_Geo.append(PLine(Base.Vector(zn.polygon.pts.xy[l-1][0],-zn.polygon.pts.xy[l-1][1],0), Base.Vector(zn.polygon.pts.xy[0][0],-zn.polygon.pts.xy[0][1],0)))
                        line2=Part.Edge(PLine(Base.Vector(zn.polygon.pts.xy[l-1][0],-zn.polygon.pts.xy[l-1][1],0), Base.Vector(zn.polygon.pts.xy[0][0],-zn.polygon.pts.xy[0][1],0)))
                z_lines.append(line2)
            else:
                line1=Part.Edge(PLine(Base.Vector(zn.polygon.pts.xy[ind-1][0],-zn.polygon.pts.xy[ind-1][1],0), Base.Vector(zn.polygon.pts.xy[ind][0],-zn.polygon.pts.xy[ind][1],0)))
                edges.append(line1);
                if load_sketch:
                    if aux_orig ==1 or grid_orig ==1:
                        #FreeCAD.ActiveDocument.PCB_Sketch_draft.addGeometry(PLine(Base.Vector(l.start[0]-off_x,-l.start[1]-off_y,0), Base.Vector(l.end[0]-off_x,-l.end[1]-off_y,0)))
                        PCB_Geo.append(PLine(Base.Vector(zn.polygon.pts.xy[ind-1][0]-off_x,-zn.polygon.pts.xy[ind-1][1]-off_y,0), Base.Vector(zn.polygon.pts.xy[ind][0]-off_x,-zn.polygon.pts.xy[ind][1]-off_y,0)))
                        line2=Part.Edge(PLine(Base.Vector(zn.polygon.pts.xy[ind-1][0]-off_x,-zn.polygon.pts.xy[ind-1][1]-off_y,0), Base.Vector(zn.polygon.pts.xy[ind][0]-off_x,-zn.polygon.pts.xy[ind][1]-off_y,0)))
                    else:
                        #FreeCAD.ActiveDocument.PCB_Sketch_draft.addGeometry(PLine(Base.Vector(l.start[0],-l.start[1],0), Base.Vector(l.end[0],-l.end[1],0)))
                        PCB_Geo.append(PLine(Base.Vector(zn.polygon.pts.xy[ind-1][0],-zn.polygon.pts.xy[ind-1][1],0), Base.Vector(zn.polygon.pts.xy[ind][0],-zn.polygon.pts.xy[ind][1],0)))
                        line2=Part.Edge(PLine(Base.Vector(zn.polygon.pts.xy[ind-1][0],-zn.polygon.pts.xy[ind-1][1],0), Base.Vector(zn.polygon.pts.xy[ind][0],-zn.polygon.pts.xy[ind][1],0)))
                z_lines.append(line2)
            ind+=1
        Draft.makeSketch(z_lines)
        ndsk = FreeCAD.ActiveDocument.ActiveObject
        ndsk.Label = sk_label + '_' + str(k_index)
        ndsk.ViewObject.LineColor = (1.00,1.00,1.00)
        ndsk.ViewObject.PointColor = (1.00,1.00,1.00)
        k_index += 1
        #closing edge

    # k_index = 0
    for lp in mypcb.gr_poly: #pcb polylines
        if lyr not in lp.layer:
        # if lp.layer != 'Edge.Cuts':
            continue
        ply_lines = []
        ind = 0
        l = len(lp.pts.xy)
        for p in lp.pts.xy:
            if ind == 0:
                line1=Part.Edge(PLine(Base.Vector(lp.pts.xy[l-1][0],-lp.pts.xy[l-1][1],0), Base.Vector(lp.pts.xy[0][0],-lp.pts.xy[0][1],0)))
                edges.append(line1);
                if load_sketch:
                    if aux_orig ==1 or grid_orig ==1:
                        #FreeCAD.ActiveDocument.PCB_Sketch_draft.addGeometry(PLine(Base.Vector(l.start[0]-off_x,-l.start[1]-off_y,0), Base.Vector(l.end[0]-off_x,-l.end[1]-off_y,0)))
                        PCB_Geo.append(PLine(Base.Vector(lp.pts.xy[l-1][0]-off_x,-lp.pts.xy[l-1][1]-off_y,0), Base.Vector(lp.pts.xy[0][0]-off_x,-lp.pts.xy[0][1]-off_y,0)))
                        if lp.layer != 'Edge.Cuts':
                            line2=Part.Edge(PLine(Base.Vector(lp.pts.xy[l-1][0]-off_x,-lp.pts.xy[l-1][1]-off_y,0), Base.Vector(lp.pts.xy[0][0]-off_x,-lp.pts.xy[0][1]-off_y,0)))
                    else:
                        #FreeCAD.ActiveDocument.PCB_Sketch_draft.addGeometry(PLine(Base.Vector(l.start[0],-l.start[1],0), Base.Vector(l.end[0],-l.end[1],0)))
                        PCB_Geo.append(PLine(Base.Vector(lp.pts.xy[l-1][0],-lp.pts.xy[l-1][1],0), Base.Vector(lp.pts.xy[0][0],-lp.pts.xy[0][1],0)))
                        if lp.layer != 'Edge.Cuts':
                            line2=Part.Edge(PLine(Base.Vector(lp.pts.xy[l-1][0],-lp.pts.xy[l-1][1],0), Base.Vector(lp.pts.xy[0][0],-lp.pts.xy[0][1],0)))
                if lp.layer != 'Edge.Cuts':
                    ply_lines.append(line2)
            else:
                line1=Part.Edge(PLine(Base.Vector(lp.pts.xy[ind-1][0],-lp.pts.xy[ind-1][1],0), Base.Vector(lp.pts.xy[ind][0],-lp.pts.xy[ind][1],0)))
                edges.append(line1);
                if load_sketch:
                    if aux_orig ==1 or grid_orig ==1:
                        #FreeCAD.ActiveDocument.PCB_Sketch_draft.addGeometry(PLine(Base.Vector(l.start[0]-off_x,-l.start[1]-off_y,0), Base.Vector(l.end[0]-off_x,-l.end[1]-off_y,0)))
                        PCB_Geo.append(PLine(Base.Vector(lp.pts.xy[ind-1][0]-off_x,-lp.pts.xy[ind-1][1]-off_y,0), Base.Vector(lp.pts.xy[ind][0]-off_x,-lp.pts.xy[ind][1]-off_y,0)))
                        if lp.layer != 'Edge.Cuts':
                            line2=Part.Edge(PLine(Base.Vector(lp.pts.xy[ind-1][0]-off_x,-lp.pts.xy[ind-1][1]-off_y,0), Base.Vector(lp.pts.xy[ind][0]-off_x,-lp.pts.xy[ind][1]-off_y,0)))
                    else:
                        #FreeCAD.ActiveDocument.PCB_Sketch_draft.addGeometry(PLine(Base.Vector(l.start[0],-l.start[1],0), Base.Vector(l.end[0],-l.end[1],0)))
                        PCB_Geo.append(PLine(Base.Vector(lp.pts.xy[ind-1][0],-lp.pts.xy[ind-1][1],0), Base.Vector(lp.pts.xy[ind][0],-lp.pts.xy[ind][1],0)))
                        if lp.layer != 'Edge.Cuts':
                            line2=Part.Edge(PLine(Base.Vector(lp.pts.xy[ind-1][0],-lp.pts.xy[ind-1][1],0), Base.Vector(lp.pts.xy[ind][0],-lp.pts.xy[ind][1],0)))
                if lp.layer != 'Edge.Cuts':
                    ply_lines.append(line2)
            ind+=1
        if lp.layer != 'Edge.Cuts':
            Draft.makeSketch(ply_lines)
            ndsk = FreeCAD.ActiveDocument.ActiveObject
            ndsk.Label = sk_label + '_Poly_' + str(k_index)
            ndsk.ViewObject.LineColor = (1.00,1.00,1.00)
            ndsk.ViewObject.PointColor = (1.00,1.00,1.00)
            k_index += 1
        #closing edge

    #bsplines
    for bs in mypcb.gr_curve:
        # if bs.layer != 'Edge.Cuts':
        if lyr not in bs.layer:
            continue
        ind = 0
        #sayerr(bs.layer)
        poles = []
        for p in bs.pts.xy:
            # sayerr(p)
            poles.append(FreeCAD.Vector (p[0]-off_x,-p[1]-off_y,0.0))
            # sayerr(poles)
        spline=Part.BSplineCurve()
        spline.buildFromPoles(poles, False, 3)
        edges.append(Part.Edge(spline))
        #stop
        #edges.append(Part.Edge(spline2))
        # Part.show(spline.toShape())
        # import kicadStepUptools; import importlib; importlib.reload(kicadStepUptools);kicadStepUptools.open(u"C:/Temp/bspline.kicad_pcb")
        if load_sketch:
            if aux_orig ==1 or grid_orig ==1:
                PCB_Geo.append(spline)
                # pi = 0
                #for p in bs.pts.xy:
                #    if (pi == 1) or (pi == 2):
                #        PCB_Geo.append(Part.Circle (FreeCAD.Vector(p[0]-off_x, -p[1]-off_y), FreeCAD.Vector(0, 0, 1), 0.5))
                #        l = len(PCB_Geo)
                #        print(PCB_Geo[l-1].Construction)
                #        PCB_Geo[l-1].Construction = True
                #        #PCB_Geo.append(Part.Circle (0.5, Base.Vector(p[0]-off_x, -p[1]-off_y, 0.0), Base.Vector(1,0,0)))
                #    pi+=1
                #for p in bs.pts.xy:
                #    if (pi == 0) or (pi == 4):
                #        PCB_Geo.append(Part.Point (FreeCAD.Vector(p[0]-off_x, -p[1]-off_y, 0.0)))
                #        l = len(PCB_Geo)
                #        print(PCB_Geo[l-1].Construction)
                #        PCB_Geo[l-1].Construction = True
                #        #PCB_Geo.append(Part.Circle (0.5, Base.Vector(p[0]-off_x, -p[1]-off_y, 0.0), Base.Vector(1,0,0)))
                #    pi+=1
            else:
                PCB_Geo.append(spline)
                # pi = 0
                # for p in bs.pts.xy:
                #     if (pi == 1) or (pi == 2):
                #         PCB_Geo.append(Part.makeCircle (0.5, Base.Vector(p[0]-off_x, -p[1]-off_y, 0.0), Base.Vector(1,0,0)))
                #     pi+=1                
    #stop
    ## NB use always float() to guarantee number not string!!!
    for a in mypcb.gr_arc: #pcb arcs
        # if a.layer != 'Edge.Cuts':
        if lyr not in a.layer:
            continue
        # for gr_arc, 'start' is actual the center, and 'end' is the start
        #edges.append(makeArc(makeVect(l.start),makeVect(l.end),l.angle))
        [xs, ys] = a.start
        [x1, y1] = a.end
        if hasattr (a, 'mid'):
            [xm, ym] = a.mid 
            arc1 = Part.Edge(Part.Arc(Base.Vector(xs,-ys,0),Base.Vector(xm,-ym,0),Base.Vector(x1,-y1,0)))
            curve = arc1.Curve.AngleXU/pi*180
            #curve = arc1.AngleXU/pi*180
            #print(curve)
            if curve > 0:
                curve = -1*curve
                #print('inverting')
                #arc1.reverse();
            #Part.show(arc1);print(curve) #;stop
            [x2, y2] = rotPoint2([x1, y1], [xs, ys], curve)
        else:
            curve = a.angle
            [x2, y2] = rotPoint2([x1, y1], [xs, ys], curve)
            arc1 = Part.Edge(Part.Arc(Base.Vector(x2,-y2,0),mid_point(Base.Vector(x2,-y2,0),Base.Vector(x1,-y1,0),curve),Base.Vector(x1,-y1,0)))
        # if curve>0:
        #     arc = Part.makeCircle(r,center,Vector(0,0,1),a-angle,a)
        #     arc.reverse();
        # else:
        #     arc = Part.makeCircle(r,center,Vector(0,0,1),a,a-angle)
        Cntr = arc1.Curve.Center
        #Cntr = arc1.Center
        cx=Cntr.x;cy=Cntr.y
        #print cx,cy
        r = arc1.Curve.Radius
        #r = arc1.Radius
        #r=arcRadius(xs, ys, x1, y1, curve)
        #sa = arc1.Curve.FirstAngle
        #ea = arc1.Curve.LastAngle
        #sa,ea = arcAngles2(xs, ys, x1, y1, cx, cy, curve)
        sa,ea = arcAngles2(arc1,curve)
        #print sa,';',ea
        #print mid_point(Base.Vector(x2,-y2,0),Base.Vector(x1,-y1,0),curve)
        #[mx,my]=arcMidPoint([xs,ys], [x1,y1], curve)
        #c=arc1.Curve.Center
        #print c
        
        #App.ActiveDocument.PCB_SketchN.addGeometry(Part.Arc(Base.Vector(x2,-y2,0),mid_point(Base.Vector(x2,-y2,0),Base.Vector(x1,-y1,0),curve),Base.Vector(x1,-y1,0)))
        if load_sketch:
            if aux_orig ==1 or grid_orig ==1:
                #FreeCAD.ActiveDocument.PCB_Sketch_draft.addGeometry(Part.ArcOfCircle(Part.Circle(FreeCAD.Vector(cx-off_x,cy-off_y,0),FreeCAD.Vector(0,0,1),r),sa,ea),False)
                #PCB_Geo.append(Part.ArcOfCircle(Part.Circle(FreeCAD.Vector(cx-off_x,cy-off_y,0),FreeCAD.Vector(0,0,1),r),sa,ea))
                if hasattr (a, 'mid'):
                    PCB_Geo.append(Part.ArcOfCircle(kicad_parser.makeVect([a.start[0]-off_x,a.start[1]+off_y]),
                                                    kicad_parser.makeVect([a.mid[0]-off_x,a.mid[1]+off_y]),
                                                    kicad_parser.makeVect([a.end[0]-off_x,a.end[1]+off_y])))
                    # print('a.start=',a.start,'a.mid=',a.mid,'a.end=',a.end, 'off_x=',off_x, 'off_y=',off_y)
                    # Part.show(Part.ArcOfCircle(kicad_parser.makeVect([a.start[0]-off_x,a.start[1]+off_y]),
                    #                                 kicad_parser.makeVect([a.mid[0]-off_x,a.mid[1]+off_y]),
                    #                                 kicad_parser.makeVect([a.end[0]-off_x,a.end[1]+off_y])).toShape())
                else:
                    PCB_Geo.append(Part.ArcOfCircle(Part.Circle(FreeCAD.Vector(cx-off_x,cy-off_y,0),FreeCAD.Vector(0,0,1),r),sa,ea))
            else:
                if hasattr (a, 'mid'):
                    PCB_Geo.append(Part.ArcOfCircle(kicad_parser.makeVect(a.start),
                                                    kicad_parser.makeVect(a.mid),
                                                    kicad_parser.makeVect(a.end)))
                else:
                    #FreeCAD.ActiveDocument.PCB_Sketch_draft.addGeometry(Part.ArcOfCircle(Part.Circle(FreeCAD.Vector(cx,cy,0),FreeCAD.Vector(0,0,1),r),sa,ea),False)
                    PCB_Geo.append(Part.ArcOfCircle(Part.Circle(FreeCAD.Vector(cx,cy,0),FreeCAD.Vector(0,0,1),r),sa,ea))
        #mp=mid_point(Base.Vector(x2,-y2,0),Base.Vector(x1,-y1,0),curve)
        #msg1= "App.ActiveDocument.PCB_SketchN.addGeometry(Part.Arc(Base.Vector({0},-{1},0),{4},Base.Vector({2},-{3},0)))".format(x2,y2,x1,y1,mp)
        #print msg1
        #App.ActiveDocument.Sketch.addGeometry(Part.Arc(App.Vector(33.0,66.5,0.3),App.Vector(32.85857864376269,66.44142135623731,0.3),App.Vector(32.8,66.3,0.3)))
        edges.append(arc1)
        PCB.append(['Arc',x1, -y1, x2, -y2, curve])
        if show_border:
            Part.show(arc1)
        
    ## NB use always float() to guarantee number not string!!!
    for c in mypcb.gr_circle: #pcb circles
        # if c.layer != 'Edge.Cuts':
        if lyr not in c.layer:
            continue
        [xs, ys] = c.center
        [x1, y1] = c.end
        ys=-ys;y1=-y1
        #say(xs); say(ys)
        r = sqrt((xs - x1) ** 2 + (ys - y1) ** 2)
        circle1=Part.Edge(Part.Circle(Base.Vector(xs, ys,0), Base.Vector(0, 0, 1), r))
        if load_sketch:
            if aux_orig ==1 or grid_orig ==1:
                #FreeCAD.ActiveDocument.PCB_Sketch_draft.addGeometry(Part.Circle(Base.Vector(xs-off_x, ys-off_y,0), Base.Vector(0, 0, 1), r))
                PCB_Geo.append(Part.Circle(Base.Vector(xs-off_x, ys-off_y,0), Base.Vector(0, 0, 1), r))
            else:
                #FreeCAD.ActiveDocument.PCB_Sketch_draft.addGeometry(Part.Circle(Base.Vector(xs, ys,0), Base.Vector(0, 0, 1), r))
                PCB_Geo.append(Part.Circle(Base.Vector(xs, ys,0), Base.Vector(0, 0, 1), r))
        if show_border:
            Part.show(circle1)
        circle1=Part.Wire(circle1)
        circle1=Part.Face(circle1)
        if show_shapes:
            Part.show(circle1)
        say('2d circle closed path')
        PCBs.append(circle1)
        PCB.append(['Circle', xs, ys, r])

    #say(PCBs)
    get_time()
    say('parsing&building time ' +str(round(running_time-t0,3)))
    if 0:
        new_cpy_skt = FreeCAD.ActiveDocument.copyObject(FreeCAD.ActiveDocument.PCB_Sketch_draft, True)
        FreeCAD.ActiveDocument.addObject("Part::Face", "Face_PCB_Sketch_draft").Sources = (new_cpy_skt, )
        FreeCAD.ActiveDocument.recompute()
        s_PCB_Sketch_draft = FreeCAD.ActiveDocument.getObject("Face_PCB_Sketch_draft").Shape
        Part.show(s_PCB_Sketch_draft)
        FreeCAD.ActiveDocument.removeObject("Face_PCB_Sketch_draft")
        FreeCAD.ActiveDocument.recompute()
    
    make_face = True #getting PCB from Sketch
    use_PCB_Sketch_E = False #getting PCB from Sketch and Fp Edges
    dont_use_constraints = False
    create_pcb_from_edges = False
    create_pcb_basic = False
    fcv = getFCversion()
    if fcv[0]==0 and fcv[1] <17:
       make_face = False
       create_pcb_from_edges =True
    if edg_segms > max_edges_admitted:
        #sayerr('too many segments, skipping sketches & constraints')
        sayerr('too many segments, skipping ALL constraints')
        if FreeCAD.GuiUp:
            from PySide import QtGui
            QtGui.QApplication.restoreOverrideCursor()
            d = QtGui.QMessageBox()
            d.setText("""<b>Warning:</b> High number of entities to join (> """+str(max_edges_admitted)+""")<br><b>Constraints will not be applied to PCB Sketch</b>""")
            d.setInformativeText("This might take a long time or even freeze your computer. Are you sure?")
            d.setStandardButtons(QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel)
            d.setDefaultButton(QtGui.QMessageBox.Cancel)
            res = d.exec_()
            if res == QtGui.QMessageBox.Cancel:
                FreeCAD.Console.PrintMessage("Aborted\n")
                stop
        if 1:
            dont_use_constraints = True
            FreeCAD.ActiveDocument.PCB_Sketch_draft.Geometry=PCB_Geo
        else:
            make_face = False
            create_pcb_basic = True
    else:
        #say (PCB_Geo)
        #for g in PCB_Geo:
        #    FreeCAD.ActiveDocument.PCB_Sketch_draft.addGeometry(g)
        FreeCAD.ActiveDocument.PCB_Sketch_draft.Geometry=PCB_Geo
        #get_time()
        #say('adding Geo time ' +str(running_time-t0))
        #FreeCAD.ActiveDocument.addObject("Part::Face", "Face").Sources = (FreeCAD.ActiveDocument.getObject(new_skt.Name), )

    #FreeCADGui.SendMsgToActiveView("ViewFit")
    #stop
    HoleList=[]
    if lyr == 'Edge.Cuts':
        TopPadList=[]
        BotPadList=[]
        HoleList=[]
        THPList=[]
        ## NB use always float() to guarantee number not string!!!
        warn=""
        PCB_Models = []
        for m in mypcb.module:  #parsing modules  #check top/bottom for placing 3D models
            #print(m.tstamp);print(m.fp_text[0][1])
            #stop
            if len(m.at)==2:
                m_angle=0
            else:
                m_angle=m.at[2]
            m_at=[m.at[0],-m.at[1]] #y reversed
            #say(m.layer);stop
            #HoleList = getPads(board_elab,pcbThickness)
            # pad
            virtual=0
            # say(str(pcbv))
            if pcbv <= 5:
                if hasattr(m, 'attr'):
                    if 'virtual' in m.attr:
                        #say('virtual module')
                        virtual=1
                else:
                    virtual=0
            elif pcbv > 5:
                if hasattr(m, 'attr'):
                    if 'smd' not in str(m.attr) and 'through_hole' not in str(m.attr):
                        # 'exclude_from_pos_files' or 'exclude_from_bom'
                        # say('virtual module k>5')
                        virtual=1
                    else:
                        #say('non virtual module')
                        virtual=0
                else: # missing attribute (old 'virtual') -> 'other'
                    #say('virtual module')
                    virtual=1
            m_x = float(m.at[0])
            m_y = float(m.at[1]) * (-1)
            m_rot = float(m_angle)
            
            #sayw(m.layer);sayerr(LvlTopName)
            if m.layer == LvlTopName:  # top
                side = "Top"
                #sayw('top ' + m.layer)
            else:
                side = "Bottom"
                m_rot *= -1 ##bottom 3d model rotation
                #sayw('bot ' + m.layer)
    
            n_md=1
            for md in m.model: #parsing 3d model(s)
                #say (md[0]) #model name
                #say(md.at.xyz)
                #say(md.scale.xyz)
                #say(md.rotate.xyz)
                error_scale_module=False
                #say('scale ');sayw(scale_vrml)#;
                #error_scale_module=False
                xsc_vrml_val=md.scale.xyz[0]
                ysc_vrml_val=md.scale.xyz[1]
                zsc_vrml_val=md.scale.xyz[2]        
                # if scale_vrml!='1 1 1':
                if float(xsc_vrml_val)!=1 or float(ysc_vrml_val)!=1 or float(zsc_vrml_val)!=1:
                    if "box_mcad" not in md[0] and "cylV_mcad" not in md[0] and "cylH_mcad" not in md[0]:
                        sayw('wrong scale!!! set scale to (1 1 1)')
                    error_scale_module=True
                #model_list.append(mdl_name[0])
                #model=model_list[j]+'.wrl'
                #if py2:
                if sys.version_info[0] == 2: #py2
                    model=md[0].decode("utf-8")
                    #stop
                else: #py3
                    model=md[0] # py3 .decode("utf-8")
                #print (model, ' MODEL', type(model)) #maui test py3
                md_hide = False
                # print('md value',md, len(md))
                #hide attribute on 3d model kv6+
                try:
                    if len(md) >4: #hide attribute on 3d model
                        if md[1] == 'hide':
                            md_hide = True
                            #print(md[0],'hidden')
                except:
                    sayerr ('hide attribute on 3d model missing')
                    pass
                if (virtual==1 and addVirtual==0):
                    model_name='no3Dmodel'
                    side='noLayer'
                    if model:
                        sayw("virtual model "+model+" skipped") #virtual found warning
                else:
                    if model:
                        model_name=model
                        #sayw(model_name)
                        warn=""
                        if "box_mcad" not in model_name and "cylV_mcad" not in model_name and "cylH_mcad" not in model_name:
                            if error_scale_module:
                                sayw('wrong scale!!! for '+model_name+' Set scale to (1 1 1)')
                                msg="""<b>Error in '.kicad_pcb' model footprint</b><br>"""
                                msg+="<br>reset values of<br><b>"+model_name+"</b><br> to:<br>"
                                msg+="(scale (xyz 1 1 1))<br>"
                                #warn+=("reset values of scale to (xyz 1 1 1)")
                                warn=("reset values of scale to (xyz 1 1 1)")
                                ##reply = QtGui.QMessageBox.information(None,"info", msg)
                                #stop
                        #model_name=model_name[1:]
                        #say(model_name)
                        #sayw("here")
                    else:
                        model_name='no3Dmodel'  #to do how to manage no3Dmodel
                        side='noLayer'
                        sayerr('no3Dmodel')
                    mdl_name=model_name # re.findall(r'(.+?)\.wrl',params)
                    #if virtual == 1:
                    #    sayerr("virtual model(s)");sayw(mdl_name)
                    # sayw(mdl_name)
                    # sayerr(params)
                    if len(mdl_name) > 0:
                        # model_name, rot_comb, warn, pos_vrml, rotz_vrml, scale_vrml = get3DParams(mdl_name,params, rot, virtual)
                        #sayerr(md.at.xyz)
                        if conv_offs != 1: #pcb version >= 20171114 (offset wrl in mm)
                            if hasattr(md,'at'):
                                ofs=[md.at.xyz[0]/conv_offs,md.at.xyz[1]/conv_offs,md.at.xyz[2]/conv_offs]
                            if hasattr(md,'offset'):
                                ofs=[md.offset.xyz[0]/conv_offs,md.offset.xyz[1]/conv_offs,md.offset.xyz[2]/conv_offs]
                        else:
                            ofs=md.at.xyz
                        line = []
                        line.append(model_name)
                        line.append(m_x)
                        line.append(m_y)
                        line.append(m_rot-md.rotate.xyz[2])
                        line.append(side)
                        line.append(warn)
                        line.append(ofs) #(md.at.xyz) #pos_vrml)
                        line.append(md.rotate.xyz) #rotz_vrml)
                        #sayerr(rotz_vrml)
                        line.append(md.scale.xyz) #scale_vrml)
                        line.append(virtual)
                        if hasattr(m,'tstamp'):
                            line.append(m.tstamp) # fp tstamp
                        else:
                            sayw('missing \'TimeStamp\'')
                            line.append('null')
                        line.append(m.fp_text[0][1]) #fp reference
                        line.append(n_md) #number of models in module
                        line.append(md_hide)
                        PCB_Models.append(line)
                        n_md+=1
        
            pads = []
            for p in m.pad:
                if 'drill' not in p:
                    continue                    
                #say('drill present')
                #say (p.at)
                if len(p.at)>2:
                    #say ('angle '+str(p.at[2]))
                    p_angle=p.at[2]
                else:
                    p_angle=0.0
                #say('drill');say(p.drill)
                #say('drill size');
                if hasattr(p,'drill'):
                    if 'offset' in p.drill:
                        #say('offset');say(p.drill.offset)
                        offset=p.drill.offset
                    else:
                        offset=[0,0]
                else:
                    sayw('drill size missing');
                    #say('offset not present')
                    offset=[0,0]
                #print p.drill.oval
                #if p.drill.oval:
                #    if p.drill[0] < min_drill_size and p.drill[1] < min_drill_size:
                #        continue   
                #else:
                #    if p.drill[0] < min_drill_size:
                #        continue
                #say ( p)
                #if 'circle' in p[2]:
                ## NB use always float() to guarantee number not string!!!
                if hasattr(p,'drill'):
                    #sayerr(p.drill);
                    #sayw(p.drill.oval)
                    #if p.drill.oval is not None
                    #if len(p.drill)>1:
                    #    if p.drill[1] == 'oval':
                    #        drill_oval=True
                    # drill_oval=False
                    # myidx=0
                    # for dct in p.drill:
                    #     #print(dct,' ',myidx)
                    #     if dct == 'oval' and myidx == 0:
                    #         drill_oval=True
                    #     myidx+=1
                    # if drill_oval:
                    #print (p.drill);print(p.drill.oval);print(str(p.drill).split(',')[0])
                    #if p.drill.oval is not None:
                    if 'oval' in str(p.drill).split(',')[0]:  #py3 dict workaround
                    #if p.drill.oval:  #maui temp workaround errorchecking
                        #sayw(str(p.drill.oval))
                        #sayw('drill oval')
                        # print (str(p.drill).split(','))
                        try:
                            if p.drill[0] >= min_drill_size or p.drill[1] >= min_drill_size:
                                xs=p.at[0]+m.at[0];ys=-p.at[1]-m.at[1]
                                #x1=mc.end[0]+m.at[0];y1=-mc.end[1]-m.at[1]
                                #radius = float(p.drill[0])/2 #sqrt((xs - x1) ** 2 + (ys - y1) ** 2)
                                rx=float(p.drill[0])
                                #print (p.drill)
                                if len(p.drill)>2:
                                    try:
                                        #print (p.drill[1])
                                        #stop
                                        ry=float(p.drill[1])
                                    except:
                                        ry=rx
                                else:
                                    ry=rx
                                #print(p.at[0],p.at[1], p.drill[0])
                                [x1, y1] = rotPoint2([xs, ys], [m.at[0], -m.at[1]], m_angle)
                                #sayw('holes solid '+str(holes_solid))
                                if holes_solid:
                                    obj=createHole3(x1,y1,rx,ry,"oval",totalHeight) #need to be separated instructions   
                                else:
                                    obj=createHole4(x1,y1,rx,ry,"oval") #need to be separated instructions   
                                if p_angle!=0:
                                    rotateObj(obj, [x1, y1, p_angle])
                                HoleList.append(obj)
                        except:
                            sayw('missing drill value on pad for module '+str(m.fp_text[0][1])) 
                    #elif p.drill[0]!=0: #circle drill hole
                    else:
                        try: # [0] >= min_drill_size: #isinstance(p.drill,list):
                            # for t in m.fp_text:
                            #     print(t[1])
                            if p.drill[0] >= min_drill_size:
                                #xs=p.at[0]+offset[0]+m.at[0];ys=-p.at[1]-offset[1]-m.at[1]
                                xs=p.at[0]+m.at[0];ys=-p.at[1]-m.at[1]
                                #x1=mc.end[0]+m.at[0];y1=-mc.end[1]-m.at[1]
                                radius = float(p.drill[0])#/2 #sqrt((xs - x1) ** 2 + (ys - y1) ** 2)
                                rx=radius;ry=radius
                                #print(p.at[0],p.at[1], p.drill[0])
                                [x1, y1] = rotPoint2([xs, ys], [m.at[0], -m.at[1]], m_angle)
                                if holes_solid:
                                    obj=createHole3(x1,y1,rx,ry,"oval",totalHeight) #need to be separated instructions
                                else:
                                    obj=createHole4(x1,y1,rx,ry,"oval") #need to be separated instructions
                                #say(HoleList)
                                #if p_angle!=0:
                                #    rotateObj(obj, [x1, y1, p_angle])
                                #rotateObj(obj, [m.at[0], m.at[1], m_angle])
                                HoleList.append(obj)   
                        except:
                            sayw('missing drill value on pad for module '+str(m.fp_text[0][1])) 
                    ##pads.append({'x': x, 'y': y, 'rot': rot, 'padType': pType, 'padShape': pShape, 'rx': drill_x, 'ry': drill_y, 'dx': dx, 'dy': dy, 'holeType': hType, 'xOF': xOF, 'yOF': yOF, 'layers': layers})        
                    #stop
            if hasattr(m, 'fp_poly'):
                for lp in m.fp_poly:
                    #print(lp.layer)
                    if 'Edge.Cuts' not in lp.layer:
                        continue
                    # print(m.layer)
                    # if m.layer != 'Edge.Cuts':
                    # print(lp)
                    # print(lp.pts)
                    # print(lp.pts.xy)
                    # for p in lp.pts.xy:
                    #     print(p)
                    #if lp.layer != 'F.Cu':
                    if 'F.Cu' not in m.layer:
                        continue
                    #print ml.start,ml.end
                    ind = 0
                    l = len(lp.pts.xy)
                    #print(lp)
                    for p in lp.pts.xy:
                        #print('p',p)
                        if ind == 0:
                            line1=Part.Edge(PLine(Base.Vector(lp.pts.xy[l-1][0],-lp.pts.xy[l-1][1],0), Base.Vector(lp.pts.xy[0][0],-lp.pts.xy[0][1],0)))
                            edges.append(line1);
                        else:
                            line1=Part.Edge(PLine(Base.Vector(lp.pts.xy[ind-1][0],-lp.pts.xy[ind-1][1],0), Base.Vector(lp.pts.xy[ind][0],-lp.pts.xy[ind][1],0)))
                            edges.append(line1);
                        ind+=1
                        EdgeCuts.append(line1)
                        #print(line1.Vertexes[0].Point.x,line1.Vertexes[0].Point.y)
                        #line1.Vertexes[1].Point)
                        pt1 = (line1.Vertexes[0].Point.x,-line1.Vertexes[0].Point.y)
                        pt2 = (line1.Vertexes[1].Point.x,-line1.Vertexes[1].Point.y)
                        x1=pt1[0]+m.at[0];y1=-pt1[1]-m.at[1]
                        x2=pt2[0]+m.at[0];y2=-pt2[1]-m.at[1]
                        [x1, y1] = rotPoint2([x1,y1], [m.at[0], -m.at[1]], m_angle)
                        [x2, y2] = rotPoint2([x2,y2], [m.at[0], -m.at[1]], m_angle)            
                        if aux_orig ==1 or grid_orig ==1:
                            FpEdges_Geo.append(PLine(Base.Vector(x1-off_x,y1-off_y,0), Base.Vector(x2-off_x,y2-off_y,0)))
                        else:
                            FpEdges_Geo.append(PLine(Base.Vector(x1,y1,0), Base.Vector(x2,y2,0)))
                        PCB.append(['Line', x1, y1, x2, y2])
                    #closing edge
                        if  show_border: #0: #SHOW POLY BORDER
                            Part.show(line1)
                    #stop
            if min_drill_size == -1:
                for v in mypcb.via:
                    # based on code above for pads 
                    if 'drill' not in v:
                        continue
                    if hasattr(v,'drill'):
                    #if drill_present:
                        if v.drill >= min_drill_size:
                            x1=v.at[0];y1=-v.at[1]
                            radius = float(v.drill)
                            rx=radius;ry=radius
                            if holes_solid:
                                obj=createHole3(x1,y1,rx,ry,"oval",totalHeight) #need to be separated instructions
                            else:
                                obj=createHole4(x1,y1,rx,ry,"oval") #need to be separated instructions
                            HoleList.append(obj)
                    else:
                        sayw('drill size missing');
                    
            for ml in m.fp_line:
                # if ml.layer != 'Edge.Cuts':
                if lyr not in ml.layer:
                    continue
                #print ml.start,ml.end
                x1=ml.start[0]+m.at[0];y1=-ml.start[1]-m.at[1]
                x2=ml.end[0]+m.at[0];y2=-ml.end[1]-m.at[1]
                [x1, y1] = rotPoint2([x1,y1], [m.at[0], -m.at[1]], m_angle)
                [x2, y2] = rotPoint2([x2,y2], [m.at[0], -m.at[1]], m_angle)            
                if (Base.Vector(x1,y1,0)) != (Base.Vector(x2,y2,0)): #non coincident points
                    line1=Part.Edge(PLine(Base.Vector(x1,y1,0), Base.Vector(x2,y2,0)))
                    edges.append(line1);
                    EdgeCuts.append(line1)
                    if aux_orig ==1 or grid_orig ==1:
                        FpEdges_Geo.append(PLine(Base.Vector(x1-off_x,y1-off_y,0), Base.Vector(x2-off_x,y2-off_y,0)))
                    else:
                        FpEdges_Geo.append(PLine(Base.Vector(x1,y1,0), Base.Vector(x2,y2,0)))
                    PCB.append(['Line', x1, y1, x2, y2])
                    if show_border:
                        Part.show(line1)
            for mc in m.fp_circle:
                # if mc.layer != 'Edge.Cuts':
                if lyr not in mc.layer:
                    continue
                #print mc.center,mc.end
                xs=mc.center[0]+m.at[0];ys=-mc.center[1]-m.at[1]
                x1=mc.end[0]+m.at[0];y1=-mc.end[1]-m.at[1]
                radius = sqrt((xs - x1) ** 2 + (ys - y1) ** 2)
                [x1, y1] = rotPoint2([xs, ys], [m.at[0], -m.at[1]], m_angle)
                circle1=Part.Edge(Part.Circle(Base.Vector(x1, y1,0), Base.Vector(0, 0, 1), radius))
                circle2=circle1
                if show_border:
                    Part.show(circle1)
                circle1=Part.Wire(circle1)
                circle1=Part.Face(circle1)
                if show_shapes:
                    Part.show(circle1)
                say('2d circle closed path')
                PCBs.append(circle1)
                EdgeCuts.append(circle2)
                if aux_orig ==1 or grid_orig ==1:
                    FpEdges_Geo.append(Part.Circle(Base.Vector(xs-off_x, ys-off_y,0), Base.Vector(0, 0, 1), radius))
                else:
                    FpEdges_Geo.append(Part.Circle(Base.Vector(xs, ys,0), Base.Vector(0, 0, 1), radius))
                PCB.append(['Circle', x1, y1, radius])
                #mod_circles.append (['Circle', x1, y1, e[2]])
                #PCB.append(['Circle', x1, y1, radius])
            for ma in m.fp_arc:
                # if ma.layer != 'Edge.Cuts':
                if lyr not in ma.layer:
                    continue
                #print ma.start, ma.end, ma.angle           
                #xs=ma.start[0]+m.at[0];ys=-ma.start[1]-m.at[1]
                #x1=ma.end[0]+m.at[0];y1=-ma.end[1]-m.at[1]
                xs=ma.start[0];ys=ma.start[1]
                x1=ma.end[0];y1=ma.end[1]
                if hasattr (ma, 'mid'):
                    [xm, ym] = ma.mid 
                    #arc2 = Part.Edge(Part.Arc(Base.Vector(xs,-ys,0),Base.Vector(xm,-ym,0),Base.Vector(x1,-y1,0)))
                    arc1 = Part.Edge(Part.ArcOfCircle(kicad_parser.makeVect(ma.start), kicad_parser.makeVect(ma.mid), kicad_parser.makeVect(ma.end)).toShape())
                    arc1.rotate(Vector(),Vector(0,0,1),m_angle)
                    if aux_orig ==1 or grid_orig ==1:
                        mat_t=(m.at[0]-off_x,-m.at[1]-off_y,0)
                    else:
                        mat_t=(m.at[0],-m.at[1],0)
                    arc1.translate(mat_t)
                    edges.append(arc1)
                    EdgeCuts.append(arc1)
                    delta_angle=degrees(arc1.LastParameter-arc1.FirstParameter)
                    curve = delta_angle
                    [x2, y2] = [xs,ys] #rotPoint2([x1, y1], [xs, ys], curve)
                    sa,ea = arcAngles2(arc1,curve)
                    Cntr = arc1.Curve.Center
                    cx=Cntr.x;cy=Cntr.y
                    #print cx,cy
                    r = arc1.Curve.Radius
                    skt = Draft.makeSketch(arc1)
                    FpEdges_Geo.append(skt.Geometry[0])
                    FreeCAD.ActiveDocument.removeObject(skt.Name)
                else:
                    curve = ma.angle
                    [x2, y2] = rotPoint2([x1, y1], [xs, ys], curve)
                    y1=-y1-m.at[1]; y2=-y2-m.at[1]
                    x1+=m.at[0];x2+=m.at[0]
                    [x1, y1] = rotPoint2([x1, y1], [m.at[0], -m.at[1]], m_angle)
                    [x2, y2] = rotPoint2([x2, y2], [m.at[0], -m.at[1]], m_angle)
                    arc1=Part.Edge(Part.Arc(Base.Vector(x2,y2,0),mid_point(Base.Vector(x2,y2,0),Base.Vector(x1,y1,0),curve),Base.Vector(x1,y1,0)))
                    edges.append(arc1)
                    EdgeCuts.append(arc1)
                    sa,ea = arcAngles2(arc1,curve)
                    Cntr = arc1.Curve.Center
                    cx=Cntr.x;cy=Cntr.y
                    #print cx,cy
                    r = arc1.Curve.Radius
                    if aux_orig ==1 or grid_orig ==1:
                        FpEdges_Geo.append(Part.ArcOfCircle(Part.Circle(FreeCAD.Vector(cx-off_x,cy-off_y,0),FreeCAD.Vector(0,0,1),r),sa,ea))
                    else:
                        FpEdges_Geo.append(Part.ArcOfCircle(Part.Circle(FreeCAD.Vector(cx,cy,0),FreeCAD.Vector(0,0,1),r),sa,ea))
                if show_border:
                    Part.show(arc1)
                PCB.append(['Arc', x1, y1, x2, y2, curve])         

        if 0: #this is not needed anymoore because we have built a PCB_Sketch_draft from Edges
            if len(EdgeCuts) >0 and not create_pcb_from_edges:
                try:
                    s_PCB_Cuts = OSCD2Dg_edgestofaces(EdgeCuts,3 , edge_tolerance)
                    HoleList.append(s_PCB_Cuts)
                except:
                    sayerr('error in making footprint Edge Cuts')
            elif len(EdgeCuts) > 0:
                try:
                    s_PCB_Cuts = OSCD2Dg_edgestofaces(EdgeCuts,3 , edge_tolerance)
                    #Part.show(s_PCB_Cuts)
                except:
                    sayerr('error in making PCB from footprint Edge Cuts')
                    #creating a sketch with fp edges
        if len(EdgeCuts) > 0:
            PCB_Sketch_draft_E= FreeCAD.activeDocument().addObject('Sketcher::SketchObject','PCB_Sketch_draft_E')
            FreeCAD.activeDocument().PCB_Sketch_draft_E.Placement = FreeCAD.Placement(FreeCAD.Vector(0.000000,0.000000,0.000000),FreeCAD.Rotation(0.000000,0.000000,0.000000,1.000000))            
            FreeCAD.ActiveDocument.PCB_Sketch_draft_E.Geometry=PCB_Geo+FpEdges_Geo
            use_PCB_Sketch_E = True

    if lyr == 'Edge.Cuts':
        if make_face: #creation pcb from PCB sketch draft
            if use_PCB_Sketch_E:
                PCB2Sketch=FreeCAD.ActiveDocument.PCB_Sketch_draft_E
            else:
                PCB2Sketch=FreeCAD.ActiveDocument.PCB_Sketch_draft
            if len(PCB2Sketch.Geometry)>0:
                if addConstraints!='none' and not dont_use_constraints:
                    say('start adding constraints to pcb sketch')
                    get_time()
                    t0=(running_time)
                    if hasattr (FreeCAD.ActiveDocument.getObject(PCB2Sketch.Name), "autoconstraint"):
                        if addConstraints=='full':
                            FreeCAD.ActiveDocument.getObject("PCB_Sketch_draft").autoconstraint(edge_tolerance*5,0.01)
                            if use_PCB_Sketch_E:
                                FreeCAD.ActiveDocument.getObject("PCB_Sketch_draft_E").autoconstraint(edge_tolerance*5,0.01)
                        else:
                            add_constraints("PCB_Sketch_draft")
                            if use_PCB_Sketch_E:
                                add_constraints("PCB_Sketch_draft_E")
                    else:
                        add_constraints("PCB_Sketch_draft")
                        if use_PCB_Sketch_E:
                            add_constraints("PCB_Sketch_draft_E")
                    get_time()
                    #say('adding constraints time ' +str(running_time-t0))
                    say('adding constraints time ' + "{0:.3f}".format(running_time-t0))
                if 0: #dont_use_constraints:
                    sayw('adding missing geometry')
                    add_missing_geo("PCB_Sketch_draft")
                    #stop
                    
                make_face_mode = 1
                FreeCAD.ActiveDocument.recompute()
                if make_face_mode == 1:  ## face creation method
                    shsk = PCB2Sketch.Shape.copy()
                    #Part.show(shsk)
                    edgs = shsk.Edges
                    #print(edgs)
                    if len(edgs)== 0:
                        sayerr('No edges found for pcb!!!')
                        stop
                    if 1:
                        s_PCB_Sketch_draft = OSCD2Dg_edgestofaces(edgs,3 , edge_tolerance)
                    if 0:
                        import OpenSCAD2Dgeom
                        s_PCB_Sketch_draft = OpenSCAD2Dgeom.edgestofaces(Part.__sortEdges__(edgs))
                    Part.show(s_PCB_Sketch_draft)
                    Face_PCB_Sketch_draft = FreeCAD.ActiveDocument.ActiveObject
                    s_PCB_Sketch_draft = Face_PCB_Sketch_draft.Shape.copy()
                    ## OpenSCAD2Dgeom.edgestofaces(edgs)
                    
                else:
                    FreeCAD.ActiveDocument.addObject("Part::Face", "Face_PCB_Sketch_draft").Sources = (PCB2Sketch, ) #(FreeCAD.ActiveDocument.PCB_Sketch_draft, )
                    FreeCAD.ActiveDocument.recompute()
                    s_PCB_Sketch_draft = FreeCAD.ActiveDocument.getObject("Face_PCB_Sketch_draft").Shape.copy()
                    
                #s_PCB_Sketch_draft = s.copy()
                sayw ('created PCB face w/ edge tolerance -> '+str(edge_tolerance)+' mm')
                if aux_orig ==1 or grid_orig ==1:
                    s_PCB_Sketch_draft.translate((off_x, off_y,0))
                #else:
                #    s_PCB_Sketch_draft.translate(xs, ys,0)
                #if use_Links:
                #Part.show(s_PCB_Sketch_draft)
                if make_face_mode == 1:  ## face creation method
                    #if 0:
                    FreeCAD.ActiveDocument.removeObject(Face_PCB_Sketch_draft.Name)
                    if use_PCB_Sketch_E:
                        FreeCAD.ActiveDocument.removeObject(PCB_Sketch_draft_E.Name)
                    FreeCAD.ActiveDocument.recompute()
                else:
                    FreeCAD.ActiveDocument.removeObject("Face_PCB_Sketch_draft")
                    if use_PCB_Sketch_E:
                        FreeCAD.ActiveDocument.removeObject(PCB_Sketch_draft_E.Name)
                    FreeCAD.ActiveDocument.recompute()
                    
                #FreeCAD.ActiveDocument.addObject("Part::Face", "Face").Sources = (FreeCAD.ActiveDocument.PCB_Sketch_draft001, )
                if (zfit):
                    FreeCADGui.SendMsgToActiveView("ViewFit")
                cut_base = s_PCB_Sketch_draft
            else:
                sayerr('empty sketch; module edge board: creating PCB from Footprint Edge.Cuts')
                create_pcb_from_edges = True

    LCS = None
    #if aux_orig ==1 or grid_orig ==1:
    if origin is not None: #adding LCS only on aux or grid origin
        try:
            FreeCAD.ActiveDocument.addObject('PartDesign::CoordinateSystem','Local_CS'+fname_sfx)
            LCS = FreeCAD.ActiveDocument.ActiveObject
            FreeCADGui.ActiveDocument.getObject(LCS.Name).Visibility = False
            FreeCADGui.Selection.clearSelection()
            #FreeCADGui.Selection.addSelection(LCS)
            #FreeCADGui.runCommand('Std_HideSelection',0)
            #FreeCADGui.runCommand('Std_ToggleVisibility',0)
            #FreeCADGui.Selection.clearSelection()
        except:
            sayw('LCS not supported')
    
        if 0:
            Part.show(s_PCB_Cuts)
            fc_PCB_Cuts = FreeCAD.ActiveDocument.ActiveObject
            face_PCB_Cuts = fc_PCB_Cuts.Shape.copy()
            if aux_orig ==1 or grid_orig ==1:
                face_PCB_Cuts.translate((-off_x, -off_y,0))
            Part.show(face_PCB_Cuts)
        #obj = FreeCAD.ActiveDocument.ActiveObject
        #stop
        #HoleList.append(face_PCB_Cuts)
        #stop PCB_Cuts
        #sayw(len(HoleList))
        #say (PCB_Models)
        #stop
        
        #g = App.ActiveDocument.PCB_Sketch.Geometry
        #g = App.ActiveDocument.PCB_Sketch
        # For each sketch geometry type, map a list of points to move.
    
            
            # Direct access to sketch.Geometry[index] does not work. This would,
            # however prevent repeated recompute.
            #for point_index in point_indexes:
            #    point = PCB_Sketch.getPoint(geom_index, point_index)
            #    sayerr (point)
            #    sayw(point[0]);sayw(point[1])
            #    ## ckeck point coincidence for sketch constrains
            #    #sketch.movePoint(geom_index, point_index, point)
            #    
            #for i, pidx in enumerate(point_indexes):
            #    for pidx2 in point_indexes[(i + 1):]:
            #        point = PCB_Sketch.getPoint(geom_index, pidx)
            #        point2 = PCB_Sketch.getPoint(geom_index, pidx2)
            #        sayerr(pidx);sayw(pidx2)
            #        sayerr('points')
            #        sayw(point[0]);sayw(point[1]);sayw(point2[0]);sayw(point2[1])
            #        if point[0] == point2[0]:
            #            say('found 00')
            #            PCB_Sketch.addConstraint(Sketcher.Constraint('Coincident',idx,1,idx2,1)) 
            #        if point[1] == point2[0]:
            #            say('found 10')
            #            PCB_Sketch.addConstraint(Sketcher.Constraint('Coincident',idx,2,idx2,1)) 
            #        if point[0] == point2[1]:
            #            say('found 01')
            #            PCB_Sketch.addConstraint(Sketcher.Constraint('Coincident',idx,1,idx2,2)) 
            #        if point[1] == point2[1]:
            #            say('found 11')
            #            PCB_Sketch.addConstraint(Sketcher.Constraint('Coincident',idx,2,idx2,2)) 
            #        
    
        FreeCAD.ActiveDocument.recompute()
        
        #add_constraints(PCB_Sketch_draft.Name)    
        #t_name=cpy_sketch(PCB_Sketch_draft.Name)
        ##s_name=shift_sketch(PCB_Sketch_draft.Name, [-100,-100])
        ##add_constraints(s_name)   
        ##FreeCADGui.SendMsgToActiveView("ViewFit")
        ##stop
        #stop
        #Sketch.addConstraint(Sketcher.Constraint('Coincident',LineFixed,PointOfLineFixed,LineMoving,PointOfLineMoving))     
        
        #for geom in PCB_Sketch.Geometry:
        #    #if isinstance(geom, Part.Line):
        #    #    bbox.enlarge_line(geom)
        #    if isinstance(geom, Part.Circle):
        #        say("Circle")
        #    elif isinstance(geom, Part.ArcOfCircle):
        #        say("Arc")
            
        #for i, e1 in enumerate(g):
        #    for e2 in g[(i + 1):]:
        #        sayw(e2.SubObjects[0].Curve)
    
        #sort edges to form a single closed 2D shape
        loopcounter = 0
        #sayw((edges))
        #stop
        # for f in PCBs:
        #     Part.show(f)
        # stop
        if create_pcb_from_edges: 
        #if not test_face:
            #sayerr('doing')
            if (len(edges)==0) and (len(PCBs)==0):
                sayw("no PCBs found")
            else:
                sayerr('creating pcb from edges instead of sketch')
                newEdges = [];
                if (len(edges)>0):
                    newEdges.append(edges.pop(0))
                    #say(newEdges[0])
                    #print [newEdges[0].Vertexes[0].Point]
                    #print [newEdges[0].Vertexes[-1].Point]
                    #say(str(len(newEdges[0].Vertexes)))
                    nextCoordinate = newEdges[0].Vertexes[0].Point
                    firstCoordinate = newEdges[0].Vertexes[-1].Point
                #nextCoordinate = newEdges[0].Curve.EndPoint
                #firstCoordinate = newEdges[0].Curve.StartPoint
                if apply_edge_tolerance:
                    for e in edges:
                        for v in e.Vertexes: v.setTolerance(edge_tolerance)  #adding tolerance to vertex
                if show_data:
                    # print findWires(edges)
                    sayw(len(edges))
                    for e in edges:
                        sayw(e.Vertexes[0].Point);sayw(e.Vertexes[-1].Point)
                    for e in edges:
                        sayw("geomType")
                        say(DraftGeomUtils.geomType(e)) 
                #if show_data:
                #    sayw(enumerate(edges));
                while(len(edges)>0 and loopcounter < 2):
                    loopcounter = loopcounter + 1
                    #print "nextCoordinate: ", nextCoordinate
                    #if len(newEdges[0].Vertexes) > 1: # not circle
                    for j, edge in enumerate(edges):
                    #for j in range (len(edges)):
                        #print "compare to: ", edges[j].Curve.StartPoint, "/" , edges[j].Curve.EndPoint
                        #if edges[j].Curve.StartPoint == nextCoordinate:
                        if show_data:
                            say(distance(edges[j].Vertexes[-1].Point, nextCoordinate))
                            say(distance(edges[j].Vertexes[0].Point, nextCoordinate))
                        #if edges[j].Vertexes[-1].Point == nextCoordinate:
                        # sayw(distance(edges[j].Vertexes[-1].Point, nextCoordinate))
                        # sayw(distance(edges[j].Vertexes[0].Point, nextCoordinate))             
                        if distance(edges[j].Vertexes[-1].Point, nextCoordinate)<=edge_tolerance:
                            #if edges[j].Vertexes[-1].Point != nextCoordinate:
                            if distance(edges[j].Vertexes[-1].Point, nextCoordinate)>edge_tolerance_warning:
                                sayerr('non coincident edges:\n'+str(nextCoordinate)+';'+str(edges[j].Vertexes[-1].Point))
                            nextCoordinate = edges[j].Vertexes[0].Point
                            newEdges.append(edges.pop(j))
                            loopcounter = 0
                            break
                        #elif edges[j].Vertexes[0].Point == nextCoordinate:
                        elif distance(edges[j].Vertexes[0].Point, nextCoordinate)<=edge_tolerance:
                            #if edges[j].Vertexes[0].Point != nextCoordinate:
                            if distance(edges[j].Vertexes[0].Point, nextCoordinate)>edge_tolerance_warning:
                                sayerr('non coincident edges:\n'+str(nextCoordinate)+';'+str(edges[j].Vertexes[0].Point))
                            nextCoordinate = edges[j].Vertexes[-1].Point
                            newEdges.append(edges.pop(j))
                            loopcounter = 0
                            break
                    if show_data:
                        say ("first c" + str(firstCoordinate)); say(' '); say ("last c" + str(nextCoordinate))
                    #if nextCoordinate == firstCoordinate:
                    if distance(firstCoordinate, nextCoordinate)<=edge_tolerance:
                        say('2d closed path')
                        try: # maui
                            #say('\ntrying wire & face')
                            #newEdges_old=newEdges
                            ## newEdges = Part.Wire(newEdges)
                            #say('trying face')
                            ## newEdges = Part.Face(newEdges)
                            #newEdges = OpenSCAD2DgeomMau.edgestofaces(newEdges)
                            newEdges = OSCD2Dg_edgestofaces(newEdges,3 , edge_tolerance)
                            newEdges.check() # reports errors
                            newEdges.fix(0,0,0)
                            #say('done')
                            #newEdges.translate(Base.Vector(0,0,-totalHeight))
                            if show_shapes:
                                Part.show(newEdges)
                            #newEdges = newEdges.extrude(Base.Vector(0,0,totalHeight))
                            PCBs.append(newEdges)
                            if (len(edges)>0):
                                newEdges = [];
                                newEdges.append(edges.pop(0))
                                nextCoordinate = newEdges[0].Vertexes[0].Point
                                firstCoordinate = newEdges[0].Vertexes[-1].Point
                        except Part.OCCError: # Exception: #
                            say("error in creating PCB")
                            stop
                            
                if loopcounter == 2:
                    say("*** omitting PCBs because there was a not closed loop in your edge lines ***")
                    say("*** have a look at position x=" + str(nextCoordinate.x) + "mm, y=" + str(nextCoordinate.y) + "mm ***")
                    say('pcb edge not closed')
                    QtGui.QApplication.restoreOverrideCursor()
                    diag = QtGui.QMessageBox(QtGui.QMessageBox.Icon.Critical,
                                            'Error in creating Board Edge                                                                ."+"\r\n"',
                                            """<b>pcb edge not closed<br>review your Board Edges in Kicad!<br>position x=""" + str(nextCoordinate.x) + 'mm, y=' + str(-nextCoordinate.y) + 'mm')
                    diag.setWindowModality(QtCore.Qt.ApplicationModal)
                    diag.exec_()
                    FreeCADGui.activeDocument().activeView().viewTop()
                    if (zfit):
                        FreeCADGui.SendMsgToActiveView("ViewFit")
                    stop #maui
                if disable_cutting:
                    FreeCADGui.activeDocument().activeView().viewTop()
                    if (zfit):
                        FreeCADGui.SendMsgToActiveView("ViewFit")
                    stop #maui
                #say (PCBs)
                ## doc = FreeCAD.activeDocument()
                ## #outline = []
                ## for f in PCBs:
                ##     Part.show(f)
                ## PCB_Sketch= FreeCAD.activeDocument().addObject('Sketcher::SketchObject','Sketch')
                ## FreeCAD.activeDocument().Sketch.Placement = App.Placement(App.Vector(0.000000,0.000000,0.000000),App.Rotation(0.000000,0.000000,0.000000,1.000000))            
                ## for s in doc.Objects:
                ## #for f in PCBs:
                ##     if 'Part' in s.TypeId: #Part.show(s)
                ##         wires,_faces = Draft.downgrade(s,delete=False)
                ##         #Draft.downgrade(FreeCADGui.Selection.getSelection(),delete=True)
                ##         #sketch = Draft.makeSketch(wires[0:1])
                ##         #sketch.Label = "Sketch_pcb"
                ##         for wire in wires[0:1]:
                ##             Draft.makeSketch([wire],addTo=PCB_Sketch)
                ##         for wire in wires:
                ##             FreeCAD.ActiveDocument.removeObject(wire.Name)             
                ## FreeCAD.ActiveDocument.recompute()
                #for f in PCBs:
                #    Part.hide(f)
                ##FreeCADGui.SendMsgToActiveView("ViewFit")        
                ##stop
                
                maxLenght=0
                idx=0
                external_idx=idx
                for extruded in PCBs:
                    #search for orientation of each pcb in 3d space, save it (no transformation yet!)
                    angle = 0;
                    axis = Base.Vector(0,0,1)
                    position = Base.Vector(0,0,0)
                    if show_shapes:
                        Part.show(extruded)
                    #extrude_XLenght=FreeCAD.ActiveDocument.ActiveObject.Shape.BoundBox.XLength
                    # extrude_XLenght=extruded.Length #perimeter
                    extrude_XLenght=extruded.BoundBox.XLength
                    #extrude_XLenght=FreeCAD.ActiveDocument.ActiveObject.Shape.Edges.Length
                    if maxLenght < extrude_XLenght:
                        maxLenght = extrude_XLenght
                        external_idx=idx
                    #say('XLenght='+str(extrude_XLenght))
                    idx=idx+1
                say('max Length='+str(maxLenght)+' index='+str(external_idx))
                try:
                    cut_base=PCBs[external_idx]
                except:
                    say("*** omitting PCBs because there was a not closed loop in your edge lines ***")
                    say('pcb edge not closed')
                    QtGui.QApplication.restoreOverrideCursor()
                    diag = QtGui.QMessageBox(QtGui.QMessageBox.Icon.Critical,
                                            'Error in creating Board Edge                                                                ."+"\r\n"',
                                            """<b>pcb edge not closed<br>review your Board Edges in Kicad!<br>""")
                    diag.setWindowModality(QtCore.Qt.ApplicationModal)
                    diag.exec_()
                    FreeCADGui.activeDocument().activeView().viewTop()
                    if (zfit):
                        FreeCADGui.SendMsgToActiveView("ViewFit")
                    stop #maui
                i=0
                for i in range (len(PCBs)):
                    if i!=external_idx:
                        cutter=PCBs[i]
                        cut_base=cut_base.cut(cutter)
                if test_extrude:
                    cut_base = cut_base.extrude(Base.Vector(0,0,totalHeight))
                if show_shapes:
                    Part.show(cut_base)
                #cut_base_name=FreeCAD.ActiveDocument.ActiveObject.Name
                #say('Alive1')
            if len(PCBs)==1:
                cut_base = PCBs[0]
                if test_extrude:
                    cut_base = cut_base.extrude(Base.Vector(0,0,totalHeight))
                if show_shapes:
                    Part.show(cut_base)
                if show_shapes:
                    FreeCAD.activeDocument().removeObject("Shape")
                ###FreeCAD.ActiveDocument.recompute()
            
            if len(PCBs)==0:
                say('pcb edge not found')
                QtGui.QApplication.restoreOverrideCursor()
                diag = QtGui.QMessageBox(QtGui.QMessageBox.Icon.Critical,
                                        'Error in creating Board Edge                                                                ."+"\r\n"',
                                        """<b>pcb edge not closed<br>review your Board Edges in Kicad!<br>""")
                diag.setWindowModality(QtCore.Qt.ApplicationModal)
                diag.exec_()
                FreeCADGui.activeDocument().activeView().viewTop()
                if (zfit):
                    FreeCADGui.SendMsgToActiveView("ViewFit")
                stop #maui
            FreeCAD.ActiveDocument.recompute()
            FreeCADGui.activeDocument().activeView().viewTop()
        ##FreeCADGui.SendMsgToActiveView("ViewFit")
        if create_pcb_basic:
            ## experimental technique for getting the pcb edge in case of large quantity of segments
            ## To be completed
            if (len(edges)==0) and (len(PCBs)==0):
                sayw("no PCBs found")
                stop
            else:
                sayw('creating pcb from edges without constraints') 
                #N_edges = []
                #for s in edges:
                #    N_edges.extend(s.Edges)
                #if len(edges) > (100):
                #    FreeCAD.Console.PrintMessage(str(len(edges))+" edges to join\n")
                #    if FreeCAD.GuiUp:
                #        from PySide import QtGui
                #        d = QtGui.QMessageBox()
                #        d.setText("Warning: High number of entities to join (>100)")
                #        d.setInformativeText("This might take a long time or even freeze your computer. Are you sure? You can also disable the \"join geometry\" setting in DXF import preferences")
                #        d.setStandardButtons(QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel)
                #        d.setDefaultButton(QtGui.QMessageBox.Cancel)
                #        res = d.exec_()
                #        if res == QtGui.QMessageBox.Cancel:
                #            FreeCAD.Console.PrintMessage("Aborted\n")
                #            return
                
                if 0:
                    newEdges = OSCD2Dg_edgestofaces(edges,3 , edge_tolerance)
                    Part.show(newEdges)
                    stop
                if 0:
                    ## from importDXF
                    shapes = DraftGeomUtils.findWires(edges) #N_edges)
                    def addObject(shape,name="Shape",layer=None):
                        "adds a new object to the document with passed arguments"
                        if isinstance(shape,Part.Shape):
                            #say(doc.Name)
                            #stop
                            newob=doc.addObject("Part::Feature",name)
                            newob.Shape = shape
                        else:
                            newob = shape
                        #if layer:
                        #    lay=locateLayer(layer)
                        #    lay.addObject(newob)
                        #formatObject(newob)
                        return newob
                    shapes_list=[]
                    for s in shapes:
                        newob = addObject(s)
                        shapes_list.append(newob)
                    
                    WireSketch = FreeCAD.activeDocument().addObject('Sketcher::SketchObject','WireSketch')
                    shapes = Draft.makeSketch(shapes,autoconstraints=True,addTo=WireSketch)
                    FreeCAD.ActiveDocument.addObject("Part::Face", "Face_WireSketch").Sources = (FreeCAD.ActiveDocument.WireSketch, )
                    if 0:
                        FreeCAD.activeDocument().addObject("Part::Compound","ShapesCompound")
                        FreeCAD.activeDocument().ShapesCompound.Links = shapes_list
                        FreeCAD.ActiveDocument.addObject("Part::Face", "Face_Compound").Sources = (FreeCAD.ActiveDocument.ShapesCompound, )
                    FreeCAD.ActiveDocument.recompute()
                    if (zfit):
                        FreeCADGui.SendMsgToActiveView("ViewFit")
                    stop
                #fusion_wire = edges[0]
                #for no, e in enumerate(edges):
                #    no += 1
                #    if no > 1:
                #        fusion_wire = fusion_wire.fuse(e)
                # Part.show(fusion_wire)
                
                for e in edges:
                    Part.show(e)
                stop
                #w_pcb = Part.Wire(edges)
                #Part.show(w_pcb)
                
        say_time()
        
        #cut_base = cut_base.extrude(Base.Vector(0,0,totalHeight)) # test_face
        #Part.show(cut_base) #test Sketch
        #stop
        #PCB_Sketch= FreeCAD.activeDocument().addObject('Sketcher::SketchObject','PCB_Sketch')
        #FreeCAD.activeDocument().PCB_Sketch.Placement = App.Placement(App.Vector(0.000000,0.000000,0.000000),App.Rotation(0.000000,0.000000,0.000000,1.000000))            
        doc = FreeCAD.activeDocument()
        #wires,_faces = Draft.downgrade(cut_base,delete=False)
        #edges=[]
        #for f in cut_base.Faces:
        #    #print f.Edges
        #    edges.append(f.Edges)
        #for e in edges:
        #    print e
        #    print e.Vertexes.Point[0]
        #    print e.Vertexes.Point[-1]
        ##for w in cut_base.Wires:
        ##    print w
        ##    Draft.makeSketch([w], autoconstraints = True, addTo=PCB_Sketch)
        ##    PCB_Sketch.touch()
        #Part.Wire (edges)
        #print edges
        #for wire in wires:
        #    sayw(wire.Label)
        #    Draft.makeSketch([wire], autoconstraints = True, addTo=PCB_Sketch)
        #    #Draft.makeSketch([wire], autoconstraints = False, addTo=PCB_Sketch)
        #    PCB_Sketch.touch()
        if 0: #old Sketch method
            FreeCAD.ActiveDocument.recompute()
            wires,_faces = Draft.downgrade(FreeCAD.ActiveDocument.Shape,delete=False)
            FreeCAD.ActiveDocument.recompute()
            for wire in wires:
                Draft.makeSketch([wire],autoconstraints=True, addTo=PCB_Sketch)
                #makeSketch_FC_016([wire],autoconstraints=True, addTo=PCB_Sketch)
                PCB_Sketch.touch()
            #stop
            for wire in wires:
                FreeCAD.ActiveDocument.removeObject(wire.Name)             
                
            #Draft.makeSketch(FreeCAD.ActiveDocument.Wire,autoconstraints=False, addTo=PCB_Sketch)
            #FreeCAD.ActiveDocument.recompute()
            #FreeCAD.ActiveDocument.removeObject(FreeCAD.ActiveDocument.Wire.Name)
            FreeCAD.ActiveDocument.recompute()
        
        #s_name=shift_sketch(PCB_Sketch_draft.Name, [-100,-100])
        #add_constraints(s_name)   
        #stop
        #for s in doc.Objects:
        ##for f in PCBs:
        #    if 'Part' in s.TypeId: 
        #    #if cut_base.Name in s.Name: 
        #        #Part.show(s)
        #        wires,_faces = Draft.downgrade(s,delete=False)
        #        #wires,_faces = Draft.downgrade(s,delete=True)
        #        #Draft.downgrade(FreeCADGui.Selection.getSelection(),delete=True)
        #        #sketch = Draft.makeSketch(wires[0:1])
        #        #sketch.Label = "Sketch_pcb"
        #        #for f in _faces:
        #        #    print f.Edges
        #        for f in s.Faces:
        #            print f.Edges
        #            
        #        for wire in wires:
        #            #sayw(wire.Label)
        #            Draft.makeSketch([wire], autoconstraints = True, addTo=PCB_Sketch)
        #            #Draft.makeSketch([wire], autoconstraints = False, addTo=PCB_Sketch)
        #            PCB_Sketch.touch()
        #        stop
        #        for wire in wires:
        #            FreeCAD.ActiveDocument.removeObject(wire.Name)             
        # FreeCAD.ActiveDocument.recompute()
        #Part.show(cut_base)
        #stop #maui      
        ## to check to load models inside loop modules
        #if m.layer == 'F.Cu':  # top
        #    side = "Top"
        #else:
        #    side = "Bottom"
        #    m_angle *= -1 ##bottom 3d model rotation
        #    say(m_angle)    
        say("start cutting")
        get_time()
        t1=(running_time)
        if not use_AppPart:  #old method slower for FC016,015
            if holes_solid:
                #HoleList = getPads(board_elab,pcbThickness)
                say('generating solid holes')
            else:
                say('generating flat holes')
                ##HoleList = getPads_flat(board_elab)
            #say('alive-getting holes')
            #stop
            if len(HoleList)>0:
                #cut_base = FreeCAD.ActiveDocument.getObject(cut_base_name).Shape
                #cut_base_name=FreeCAD.ActiveDocument.ActiveObject
                #cut_base_name=FreeCAD.ActiveDocument.ActiveObject.Name
                #say(cut_base)
                for drill in HoleList:
                    #say("Cutting hole inside outline")
                    #Part.show(drill)
                    #say(drill)
                    if holes_solid:
                        drill = Part.makeSolid(drill)
                    if show_shapes:
                        Part.show(drill)
                    cut_base=cut_base.cut(drill)
            else:
                #face = cut_base
                cut_base = cut_base
        else:    
            sayw('using hierarchy container')
            if len(HoleList)>0:
                if holes_solid:
                    #HoleList = getPads(board_elab,pcbThickness)
                    say('generating solid holes')
                else:
                    say('generating flat holes')
                dlo=[]
                shapes=[];s_names=[]
                #for drill in HoleList:
                #    if holes_solid:
                #        drill = Part.makeSolid(drill)
                    #Part.show(drill)
                    #dlo.append(drill)
                #shapes=[];s_names=[]
                ##for o in FreeCAD.ActiveDocument.Objects:
                ##    if 'Shape' in o.Name:
                ##        dlo.append(FreeCAD.ActiveDocument.getObject(o.Name))
                ##        shapes.append(o.Shape)
                ##        s_names.append(o.Name)
                shapes=HoleList
                #stop
                ##https://forum.freecadweb.org/viewtopic.php?t=18179&start=30
                #multifuse
                shape_base=shapes[0]
                shapes=shapes[1:]
                #fc_016=True
                if len(HoleList)>1:  #more than one drill
                    shape = shape_base.fuse(shapes)
                else:   #one drill ONLY
                    shape = shape_base
                test_face_gen = False
                if test_face_gen:
                    Part.show(cut_base) #test_face
                    Part.show(shape) #test_face
                    stop
                try:
                    cut_base = cut_base.cut(shape)
                except:
                    say("*** omitting PCBs because there was a not closed loop in your edge lines ***")
                    say('pcb edge not closed')
                    QtGui.QApplication.restoreOverrideCursor()
                    diag = QtGui.QMessageBox(QtGui.QMessageBox.Icon.Critical,
                                            'Error in creating Board Edge                                                                ."+"\r\n"',
                                            """<b>pcb edge not closed<br>review your Board Edges in Kicad!<br>or try to fix it with Constrainator""")
                    diag.setWindowModality(QtCore.Qt.ApplicationModal)
                    diag.exec_()
                    FreeCADGui.activeDocument().activeView().viewTop()
                    if (zfit):
                        FreeCADGui.SendMsgToActiveView("ViewFit")
                    stop #maui                
                #Part.show(cut_base)
                #stop
                for s in s_names:
                    #Part.show(s)
                    FreeCAD.ActiveDocument.removeObject(s) #test_face
                FreeCAD.ActiveDocument.recompute()
                #stop
                #say_time()
            
            else:
                #face = cut_base
                sayw('pcb without holes')
                # Part.show(cut_base) #test_face
                # f0 = cut_base.Faces[0]
                # Part.show(f0)
                #cut_base = cut_base
                
            #else:
            #    #face = cut_base
            #    try:
            #        cut_base = cut_base
            #    except:
            #        cut_base = FreeCAD.ActiveDocument.getObject('PCB_Sketch_draft') #s_PCB_Sketch_draft
                    #if lyr != 'Edge.Cuts':
                    #    cut_base.Label=lyr+'-Sketch'
                        #FreeCADGui.SendMsgToActiveView("ViewFit")
        #    ##if len(HoleList)>0:
        #    ##    #face = cut_base.cut(Part.makeCompound(HoleList))
        #    ##    cut_base = cut_base.cut(Part.makeCompound(HoleList))   ###VERY fast but failing when overlapping of pads
        get_time()
        say('cutting time ' +str(round(running_time-t1,3)))
        
        if lyr == 'Edge.Cuts':
            pcb_name=u'Pcb'+fname_sfx
            #doc_outline=doc.addObject("Part::Feature","Pcb")
            doc_outline=doc.addObject("Part::Feature",pcb_name)
            pcb_name=FreeCAD.ActiveDocument.ActiveObject.Name
            pcb_board=FreeCAD.ActiveDocument.ActiveObject
            try:
                #doc_outline.Shape=cut_base.extrude(Base.Vector(0,0,-totalHeight))
                f0 = cut_base.Faces[0]
                s0 = f0.extrude(Base.Vector(0,0,-totalHeight))
                s = s0
                for f in cut_base.Faces[1:]:
                    #f0 = f0.union(f)
                    s1 = f.extrude(Base.Vector(0,0,-totalHeight))
                    s = s.fuse(s1)
                doc_outline.Shape=s
                #doc_outline.Shape=f0.extrude(Base.Vector(0,0,-totalHeight))
                #doc_outline.Shape=cut_base.Faces[0].extrude(Base.Vector(0,0,-totalHeight))
            except:
                #doc.removeObject("Pcb")
                doc.removeObject(pcb_name)
                say("*** omitting PCBs because there was a not closed loop in your edge lines ***")
                say('pcb edge not closed')
                QtGui.QApplication.restoreOverrideCursor()
                diag = QtGui.QMessageBox(QtGui.QMessageBox.Icon.Critical,
                                        'Error in creating Board Edge                                                                ."+"\r\n"',
                                        """<b>pcb edge not closed<br>review your Board Edges in Kicad!<br>or try to fix it with Constrainator""")
                diag.setWindowModality(QtCore.Qt.ApplicationModal)
                diag.exec_()
                FreeCADGui.activeDocument().activeView().viewTop()
                if (zfit):
                    FreeCADGui.SendMsgToActiveView("ViewFit")
                stop #maui                        
            #stop
            #tobechecked
            #try:
            #    FreeCAD.activeDocument().removeObject('Shape') #removing base shape
            #except:
            #    sayw('Shape already removed')
            #cut_base=cut_base.extrude(Base.Vector(0,0,-pcbThickness))
            #Part.show(cut_base)
            if simplifyComSolid:
                faces=[]
                for f in pcb_board.Shape.Faces:
                    faces.append(f) 
                try:
                    _ = Part.Shell(faces)
                    _=Part.Solid(_)
                    FreeCAD.ActiveDocument.removeObject(pcb_name)
                    #doc.addObject('Part::Feature','Pcb').Shape=_
                    doc.addObject('Part::Feature',pcb_name).Shape=_
                    pcb_name=FreeCAD.ActiveDocument.ActiveObject.Name
                    pcb_board=FreeCAD.ActiveDocument.ActiveObject
                except:
                    sayerr('error in simplifying compsolid')
            
            # simple_pcb=doc.addObject("Part::Feature","simple_Pcb")
            # simple_pcb.Shape=pcb_board.Shape
            # spcb=pcb_board.Shape
            # Part.show(spcb)
            
            #FreeCAD.ActiveDocument.ActiveObject.Label ="Pcb"
            FreeCADGui.ActiveDocument.ActiveObject.ShapeColor = (colr,colg,colb)
            #FreeCADGui.ActiveDocument.ActiveObject.Transparency = 20
            #if remove_pcbPad==True:
            #    FreeCAD.activeDocument().removeObject(cut_base_name)
                #FreeCAD.activeDocument().removeObject(Holes_name)
            boardG_name='Board_Geoms'+fname_sfx
            board_name='Board'+fname_sfx
            if use_AppPart and not force_oldGroups and not use_LinkGroups:
                ## to evaluate to add App::Part hierarchy
                #sayw("creating hierarchy")
                doc.Tip = doc.addObject('App::Part',boardG_name)
                boardG= doc.ActiveObject
                boardG.Label = boardG_name
                try:
                    boardG.License = ''
                    boardG.LicenseURL = ''
                except:
                    pass
                grp=boardG
                if rmv_container is None or rmv_container is False:
                    doc.Tip = doc.addObject('App::Part',board_name)
                    board= doc.ActiveObject
                    board.Label = board_name
                    #FreeCAD.ActiveDocument.getObject("Step_Virtual_Models").addObject(impPart)
                    # doc.getObject(board_name).addObject(doc.getObject(boardG_name))
                    try:
                        #doc.getObject(boardG_name).addObject(LCS)
                        doc.getObject(board_name).addObject(LCS)
                        LCS.MapMode = 'ObjectXY'
                        LCS.MapReversed = False
                        LCS.Support = [(doc.getObject(board_name).Origin.OriginFeatures[0],'')]
                    except:
                        pass
                    doc.getObject(board_name).addObject(doc.getObject(boardG_name))
                else:
                    try:
                        #doc.getObject(boardG_name).addObject(LCS)
                        doc.getObject(board_name).addObject(LCS)
                        LCS.MapMode = 'ObjectXY'
                        LCS.MapReversed = False
                        LCS.Support = [(doc.getObject(board_name).Origin.OriginFeatures[0],'')]
                    except:
                        pass
                doc.getObject(boardG_name).addObject(doc.getObject(pcb_name))
                #FreeCADGui.activeView().setActiveObject('Board_Geoms', doc.Board_Geoms)
                ## end hierarchy
            elif use_LinkGroups:
                doc.Tip = doc.addObject('App::LinkGroup',boardG_name)
                boardG= doc.ActiveObject
                boardG.Label = boardG_name
                grp=boardG_name
                if rmv_container is None or rmv_container is False:
                    doc.Tip = doc.addObject('App::LinkGroup',board_name)
                    board= doc.ActiveObject
                    board.Label = board_name
                    #FreeCAD.ActiveDocument.getObject("Step_Virtual_Models").addObject(impPart)
                    # doc.getObject("Board").addObject(doc.Board_Geoms)
                    #doc.getObject('Board_Geoms').adjustRelativeLinks(doc.getObject('Board'))
                    # doc.getObject(board_name).ViewObject.dropObject(doc.getObject(boardG_name),doc.getObject(boardG_name),'',[])
                    try:
                        #LCS.adjustRelativeLinks(doc.getObject('Board_Geoms'))
                        #doc.getObject(boardG_name).ViewObject.dropObject(LCS,LCS,'',[])
                        doc.getObject(board_name).ViewObject.dropObject(LCS,LCS,'',[])
                        # LinkGroups don't have 'Origin' Feature
                        # LCS.MapMode = 'ObjectXY'
                        # LCS.MapReversed = False
                        # LCS.Support = [(doc.getObject(board_name).Origin.OriginFeatures[0],'')]
                        FreeCADGui.Selection.clearSelection()
                        FreeCADGui.Selection.addSelection(LCS)
                        FreeCADGui.runCommand('Std_ToggleVisibility',0)
                        #stop
                    except:
                        pass
                    doc.getObject(board_name).ViewObject.dropObject(doc.getObject(boardG_name),doc.getObject(boardG_name),'',[])
                else:
                    try:
                        #LCS.adjustRelativeLinks(doc.getObject('Board_Geoms'))
                        #doc.getObject(boardG_name).ViewObject.dropObject(LCS,LCS,'',[])
                        doc.getObject(board_name).ViewObject.dropObject(LCS,LCS,'',[])
                        # LinkGroups don't have 'Origin' Feature
                        # LCS.MapMode = 'ObjectXY'
                        # LCS.MapReversed = False
                        # LCS.Support = [(doc.getObject(board_name).Origin.OriginFeatures[0],'')]
                        FreeCADGui.Selection.clearSelection()
                        FreeCADGui.Selection.addSelection(LCS)
                        FreeCADGui.runCommand('Std_ToggleVisibility',0)
                        #stop
                    except:
                        pass
                FreeCADGui.Selection.clearSelection()
                #grp.addObject(pcb_board)
                #doc.getObject('Pcb').adjustRelativeLinks(doc.getObject('Board_Geoms'))
                #doc.getObject('Board_Geoms').ViewObject.dropObject(doc.getObject('Pcb'),None,'',[])
                doc.getObject(boardG_name).ViewObject.dropObject(doc.getObject(pcb_name),doc.getObject(pcb_name),'',[])
                FreeCADGui.Selection.clearSelection()
                #FreeCADGui.activeView().setActiveObject('Board_Geoms', doc.Board_Geoms)
                ## end hierarchy        
            else:
                #sayw("creating flat groups")
                grp=doc.addObject("App::DocumentObjectGroup", boardG_name)
                grp.addObject(pcb_board)
            #pcb_sk=FreeCAD.ActiveDocument.PCB_Sketch
            #grp.addObject(pcb_sk)
            #grp.addObject(doc_outline)      
            pcb_bbx = doc.getObject(pcb_name).Shape.BoundBox
            say("pcb dimensions: ("+"{0:.2f}".format(pcb_bbx.XLength)+";"+"{0:.2f}".format(pcb_bbx.YLength)+";"+"{0:.2f}".format(pcb_bbx.ZLength)+")")          
    say_time()
    if k_index == 1:
        FreeCAD.ActiveDocument.removeObject(ndsk.Name)

    FreeCADGui.activeDocument().activeView().viewAxometric()
    if (zfit):
        FreeCADGui.SendMsgToActiveView("ViewFit")
    #FreeCADGui.SendMsgToActiveView("ViewFit")
    #pads_found=getPadsList(content)
    return PCB_Models, k_index
    
###    

###
#cmd open option
args=sys.argv
#say(args)
if len(args) >= 3:
#    #filename="./psu-fc-1.wrl"
    #path, fname = os.path.split(args[2])
    #export_board_2step=True
    ##sys.argv=""
    ext = os.path.splitext(os.path.basename(args[2]))[1]
    fullfname=args[2]
    fname=os.path.splitext(os.path.basename(args[2]))[0]
    #say(filePath+' ');say(fname+' ');say(ext);
    fullFileName=fullfname+".kicad_pcb"
    fullFileNamefp=fullfname+".kicad_mod"
    fileName=fname+".kicad_pcb"
    fileNamefp=fname+".kicad_mod"
    #filePath = os.path.dirname(os.path.abspath(__file__))
    filePath = os.path.dirname(os.path.abspath(fullFileName))
    filePathfp = os.path.dirname(os.path.abspath(fullFileName))
    #filePath = os.path.split(os.path.realpath(__file__))[0]
    say ('arg file path '+filePath)
    filefound=True
    if filePath == "":
        filePath = u"."
    last_pcb_path = filePath
    print (last_pcb_path)
    #say(fullFileName)
    if os.path.exists(fullFileName):
        #say("opening "+ fullFileName)
        #cfgParsWrite(configFilePath)
        #cfg_update_all()
        pg = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/kicadStepUp")
        pg.SetString("last_pcb_path", make_string(last_pcb_path))
        original_filename=fullFileName
        onLoadBoard(fullFileName)
    else:
        fullfilePath=filePath+os.sep+fname+".kicad_pcb"
        #say(fullfilePath)
        if os.path.exists(fullfilePath):
            #say("opening "+ fullfilePath)
            #cfgParsWrite(configFilePath)
            #cfg_update_all()
            pg = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/kicadStepUp")
            pg.SetString("last_pcb_path", make_string(last_pcb_path))
            original_filename=fullfilePath
            onLoadBoard(fullfilePath)
        else:
            filefound=False
        #    sayw("missing "+ fullfilePath)
        #    sayw("missing "+ fullFileName)
        #    #say("error missing "+ fullfilePath)
        #    QtGui.QApplication.restoreOverrideCursor()
        #    reply = QtGui.QMessageBox.information(None,"Error ...","... missing \r\n"+ fullfilePath+"\r\n... missing \r\n"+ fullFileName)
    if filefound ==False:
        if os.path.exists(fullFileNamefp):
            #say("opening "+ fullFileName)
            #cfgParsWrite(configFilePath)
            #cfg_update_all()
            onLoadFootprint(fullFileNamefp)
        else:
            fullfilePath=filePath+os.sep+fname+".kicad_mod"
            #say(fullfilePath)
            if os.path.exists(fullfilePath):
                fp_loaded= False
                doc = FreeCAD.ActiveDocument
                if doc is not None:
                    for o in doc.Objects:
                        if hasattr(o, 'Label'):
                            if o.Label.endswith('_fp'):
                                fp_loaded= True
                #say("opening "+ fullfilePath)
                #cfgParsWrite(configFilePath)
                #cfg_update_all()
                #print(fp_loaded)
                if not (fp_loaded):
                    onLoadFootprint(fullfilePath)
            else:
                sayw("missing "+ fullfilePath)
                sayw("missing "+ fullFileName)
                #say("error missing "+ fullfilePath)
                if 0:
                    QtGui.QApplication.restoreOverrideCursor()
                    reply = QtGui.QMessageBox.information(None,"Error ...","... missing \r\n"+ fullfilePath+"\r\n... missing \r\n"+ fullFileName)
        #

###

#QtGui.QDesktopServices.openUrl(QtCore.QUrl("t"))


# code ***********************************************************************************

#form = RotateXYZGuiClass()

#def singleInstance():
#    app = QtGui.qApp
#
#    for i in app.topLevelWidgets():
#        if i.objectName() == "kicadStepUp":
#            i.deleteLater()
#        else:
#            pass
#
#singleInstance()

#!# from Ui_DockWidget import Ui_DockWidget
#!# from Ui_DockWidget import KSUWidget

## sketch testing button

def Export3DStepF():
    global last_3d_path, last_pcb_path, stp_exp_mode, use_AppPart, use_Links, links_imp_mode, use_LinkGroups
    
    #say("export3DSTEP")
    sel = FreeCADGui.Selection.getSelection()
    if len (sel) > 0:
        #sayw(doc.Name)
        if "App::Part" in sel[0].TypeId and not use_AppPart:
            msg="""<b>App::Part hierarchy</b> cannot be exported ATM<br>use the buttons to <b>make a Union or Compound</b> before exporting it"""
            say_warning(msg)                
        else:
            cfg_read_all()
            pg = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/kicadStepUp")
            last_3d_path = pg.GetString("last_3d_path") 
            if len(last_3d_path) == 0:
                last_3d_path=last_pcb_path
                sayw(last_pcb_path)
            #getSaveFileName(self,"saveFlle","Result.txt",filter ="txt (*.txt *.)")
            Filter=""
            name, Filter = PySide.QtGui.QFileDialog.getSaveFileName(None, "Export 3D STEP ...",
                make_unicode(last_3d_path), "*.step *.stp")
            #say(name)
            if name:
                last_3d_path=os.path.dirname(name)
                pg = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/kicadStepUp")
                pg.SetString("last_3d_path",make_string(last_3d_path))
                #my_sk=FreeCAD.ActiveDocument.copyObject(FreeCAD.ActiveDocument.PCB_Sketch,False)
                #my_sk_name=FreeCAD.ActiveDocument.ActiveObject.Name
                #FreeCAD.ActiveDocument.removeObject(FreeCAD.ActiveDocument.PCB_Sketch.Name)
                #ImportGui.export(sel,name)
                ## PCB_Sketch=FreeCAD.ActiveDocument.copyObject(FreeCAD.ActiveDocument.getObject(my_sk_name),False)
                #cpy_sketch(my_sk_name,"PCB_Sketch")
                #FreeCAD.ActiveDocument.removeObject(my_sk_name)
                #FreeCAD.ActiveDocument.getObject("Board_Geoms").addObject(FreeCAD.ActiveDocument.getObject("PCB_Sketch"))
                sel = FreeCADGui.Selection.getSelection()
                selN=sel[0].Name
                doc = FreeCAD.ActiveDocument
                #sayw(stp_exp_mode)
                #stop
                #deselect Sketches
                if not use_AppPart:
                    for e in sel:
                        if 'Sketch' in e.TypeId:
                            FreeCADGui.Selection.removeSelection(FreeCAD.ActiveDocument.getObject(e.Name))
                            sel = FreeCADGui.Selection.getSelection()
                else:
                    #skl=[sk,grp]
                    skl=[]
                    skl=find_skt_in_Doc()
                    #print skl
                    #print sk_name,';',grp_name
                    for sk in skl:
                        say('moving sketch from grp')
                        #print sk
                        FreeCAD.ActiveDocument.getObject(sk[1]).removeObject(FreeCAD.ActiveDocument.getObject(sk[0]))
                            #FreeCAD.ActiveDocument.getObject(selN).removeObject(FreeCAD.ActiveDocument.getObject(sk_name))
                #stop
                fcv = getFCversion()
                fcb = checkFCbug(fcv)
                # sayerr('not fcb '+str(not fcb))
                # sayw(stp_exp_mode)
                # say(fcv[0])
                if (stp_exp_mode == 'hierarchy' and not fcb) or (fcv[0]==0 and fcv[1]<=16):  # FC not bugged or < 0.17
                    sayw('exporting hierarchy')
                    ImportGui.export(sel,name)
                elif (stp_exp_mode == 'onelevel') or (stp_exp_mode == 'hierarchy' and fcb):
                    sayw('exporting ONE level hierarchy')
                    try:
                        import kicadStepUpCMD
                    except:
                        sayerr('to export STEP it is necessary to use StepUp Workbench<br>instead of the single Macro<br>(because of '+str(fcv)+' FC bug)')
                        msg="""<font color='red'><b>to export STEP it is necessary to use StepUp Workbench<br>instead of the single Macro<br>(because of """+str(fcv)+""" FC bug</b></font>"""
                        say_warning(msg)
                        for sk in skl:
                            say('including sketch in grp')
                            FreeCAD.ActiveDocument.getObject(sk[1]).addObject(FreeCAD.ActiveDocument.getObject(sk[0]))
                        stop
                    if fcb:
                        cpmode='compound'
                    else:
                        cpmode='part'
                    suffix='_'
                    to_export_name=kicadStepUpCMD.deep_copy(doc,cpmode,suffix)
                    # to_export_name=FreeCAD.ActiveDocument.ActiveObject.Name
                    #sayw(FreeCAD.ActiveDocument.getObject(to_export_name).Label)
                    #say(sel[0])
                    __objs__=[]
                    __objs__.append(FreeCAD.ActiveDocument.getObject(to_export_name))
                    #import ImportGui
                    ImportGui.export(__objs__,name)
                    #FreeCAD.ActiveDocument.removeObject(to_export_nam)
                    removesubtree(__objs__)
                    del __objs__
                    if fcb: # bugged FC version
                        sayerr('exported a simplified STEP hierarchy because of '+str(fcv)+' FC bug')
                        msg="""<font color='red'><b>exported a simplified STEP hierarchy<br>because of """+str(fcv)+""" FC bug</b></font>"""
                        say_warning(msg)
                    #FreeCADGui.Selection.removeSelection(sel[0])
                    #FreeCADGui.Selection.addSelection(FreeCAD.ActiveDocument.getObject(to_export_name))
                    #sel1 = FreeCADGui.Selection.getSelection()
                    #say(sel1[0])
                    #ImportGui.export(sel1[0],name)
                    #stop
                elif stp_exp_mode == 'flat':
                    # need to deselect all 'Part' containers and select all simple objs
                    #say('flat')
                    if len(sel)==1 and 'App::Part' in sel[0].TypeId: ## flattening a Part hierarchy container
                        sayw('flattening Part container')
                        # FreeCADGui.Selection.removeSelection(sel[0])
                        __objs__=[]
                        # sayerr(FreeCAD.ActiveDocument.getObject(selN).Label)
                        # sayerr(FreeCAD.ActiveDocument.getObject(selN).OutListRecursive)
                        for o in FreeCAD.ActiveDocument.getObject(selN).OutListRecursive:
                            #sayw( o.TypeId )
                            #if 'Part::Feature' in o.TypeId:
                            if hasattr(o, 'Shape'):
                                # print o.Label
                                # say ('adding ') 
                                # FreeCADGui.Selection.addSelection(o)
                                __objs__.append(o)
                        ImportGui.export(__objs__,name)
                        del __objs__
                    else:
                        sayw('exporting selection')
                        ImportGui.export(sel,name)
                
                #print selN,'-',sk_name
                #FreeCAD.ActiveDocument.getObject(selN).removeObject(App.ActiveDocument.getObject(sk_name))
                if use_AppPart:
                    for sk in skl:
                        say('including sketch in grp')
                        FreeCAD.ActiveDocument.getObject(sk[1]).addObject(FreeCAD.ActiveDocument.getObject(sk[0]))
                # PCB_Sketch=FreeCAD.ActiveDocument.copyObject(FreeCAD.ActiveDocument.getObject(my_sk_name),False)
                #try:
                #    FreeCAD.ActiveDocument.getObject(selN).addObject(FreeCAD.ActiveDocument.getObject(sk_name))
                #except:
                #    sayw('no PCB_Sketch2')
                #    pass
    else:
        msg="""select something to be exported!"""
        sayerr(msg)
        say_warning(msg)
    
##           

def Import3DModelF():
    
    global last_3d_path, last_pcb_path
    global zfit
    
    say("import3DModel")
    #sayw(doc.Name)
    pg = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/kicadStepUp")
    last_3d_path = pg.GetString("last_3d_path") 
    cfg_read_all()
    if len(last_3d_path) == 0:
        last_3d_path=last_pcb_path
        sayw(last_pcb_path)
    Filter=""
    name, Filter = PySide.QtGui.QFileDialog.getOpenFileName(None, "Import 3D File...",
         make_unicode(last_3d_path), "*.step *.stp *.stpZ *.iges *.igs *.FCStd")
    #say(name)
    if name:
        ext = os.path.splitext(os.path.basename(name))[1]
        #sayw(ext.lower())
        if ext.lower() == ".fcstd":
            FreeCAD.open(name)
        else:
            if FreeCAD.ActiveDocument is None:
                #say("none")
                doc=FreeCAD.newDocument()
            else:
                doc=FreeCAD.ActiveDocument
            ##ReadShapeCompoundMode
            paramGetVS = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/Import/hSTEP")
            ReadShapeCompoundMode_status=paramGetVS.GetBool("ReadShapeCompoundMode")
            #sayerr("checking ReadShapeCompoundMode")
            sayw("ReadShapeCompoundMode status "+str(ReadShapeCompoundMode_status))
            enable_ReadShapeCompoundMode=False
            if ReadShapeCompoundMode_status:
                paramGetVS = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/Import/hSTEP")
                paramGetVS.SetBool("ReadShapeCompoundMode",False)
                sayw("disabling ReadShapeCompoundMode")
                enable_ReadShapeCompoundMode=True
            
            FreeCAD.setActiveDocument(doc.Name)
            FreeCAD.ActiveDocument=FreeCAD.getDocument(doc.Name)
            FreeCADGui.ActiveDocument=FreeCADGui.getDocument(doc.Name)
            if name.lower().endswith('stpz'):
                try:
                    import stepZ
                    stepZ.insert(name,doc.Name)
                except:
                    sayerr('.stpZ not supported!')
            else:
                ImportGui.insert(name, doc.Name)
            
            #enable_ReadShapeCompoundMode=False
            if enable_ReadShapeCompoundMode:
                paramGetVS = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/Import/hSTEP")
                paramGetVS.SetBool("ReadShapeCompoundMode",True)
                sayw("enabling ReadShapeCompoundMode")
        
        if (zfit):
            FreeCADGui.SendMsgToActiveView("ViewFit")
        last_3d_path=os.path.dirname(name)
        pg = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/kicadStepUp")
        pg.SetString("last_3d_path",make_string(last_3d_path))
    
##
#import PySide
#from PySide import QtCore, QtGui #, QtWidgets
##from PyQt5 import QtCore, QtGui, QtWidgets
QtWidgets = QtGui

class Ui_STEP_Preferences(object):
    def setupUi(self, STEP_Preferences):
        import os
        import kts_Locator
        ksuWBpath = os.path.dirname(kts_Locator.__file__)
        #sys.path.append(ksuWB + '/Gui')
        ksuWB_demo_path =  os.path.join( ksuWBpath, 'demo')
        STEP_Preferences.setObjectName("STEP_Preferences")
        STEP_Preferences.resize(860, 752)
        STEP_Preferences.setWindowTitle("STEP Suggested Preferences")
        STEP_Preferences.setToolTip("")
        self.verticalLayoutWidget = QtWidgets.QWidget(STEP_Preferences)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 847, 732))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label.setText("<b><font color='red'>Please set your preferences for STEP Import Export to:</font></b>")
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.label_2 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap(os.path.join(ksuWB_demo_path,"Import-Export-settings.png")))
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.label_3 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_3.setText("<b><font color='red'>(you can disable this warning on StepUp preferences)</font></b>")
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_2.addWidget(self.label_3)
        self.buttonBox = QtWidgets.QDialogButtonBox(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonBox.sizePolicy().hasHeightForWidth())
        self.buttonBox.setSizePolicy(sizePolicy)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_2.addWidget(self.buttonBox)
        self.verticalLayout.addLayout(self.verticalLayout_2)

        self.buttonBox.accepted.connect(STEP_Preferences.accept)
        self.retranslateUi(STEP_Preferences)
        QtCore.QMetaObject.connectSlotsByName(STEP_Preferences)

    def retranslateUi(self, STEP_Preferences):
        pass

##
class Ui_LayerSelection(object):
    def setupUi(self, LayerSelection):
        LayerSelection.setObjectName("LayerSelection")
        LayerSelection.resize(341, 232)
        LayerSelection.setWindowTitle("LayerSelection")
        LayerSelection.setToolTip("")
        self.buttonBoxLayer = QtWidgets.QDialogButtonBox(LayerSelection)
        self.buttonBoxLayer.setGeometry(QtCore.QRect(60, 190, 271, 32))
        self.buttonBoxLayer.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBoxLayer.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBoxLayer.setObjectName("buttonBoxLayer")
        self.verticalLayoutWidget = QtWidgets.QWidget(LayerSelection)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 325, 171))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label.setText("Select the layer to push the Sketch\n"
"Default \'Edge.Cuts\'")
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.verticalLayout.addLayout(self.verticalLayout_2)
        self.comboBoxLayerSel = QtWidgets.QComboBox(self.verticalLayoutWidget)
        self.comboBoxLayerSel.setObjectName("comboBoxLayerSel")
        self.verticalLayout.addWidget(self.comboBoxLayerSel)
        self.radioBtn_newdoc = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        self.radioBtn_newdoc.setToolTip("open in new FreeCAD document")
        self.radioBtn_newdoc.setText("open in new document")
        self.radioBtn_newdoc.setChecked(True)
        self.radioBtn_newdoc.setObjectName("radioBtn_newdoc")
        self.verticalLayout.addWidget(self.radioBtn_newdoc)
        self.radioBtn_replace_pcb = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        self.radioBtn_replace_pcb.setToolTip("<html><head/><body><p>replace PCB in current document</p><p><span style=\" font-weight:600; color:#aa0000;\">N.B.</span> Sketch constrains will be deleted!</p></body></html>")
        self.radioBtn_replace_pcb.setText("replace PCB and Sketch in current document")
        self.radioBtn_replace_pcb.setObjectName("radioBtn_replace_pcb")
        self.verticalLayout.addWidget(self.radioBtn_replace_pcb)
        self.radioBtn_keep_sketch = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        self.radioBtn_keep_sketch.setToolTip("<html><head/><body><p>keep Sketch in current document</p><p><span style=\" font-weight:600; color:#aa0000;\">N.B.</span> this option will keep Sketch &amp; constrains but replace the PCB</p><p>This could lead to a unsynced Sketch feature</p></body></html>")
        self.radioBtn_keep_sketch.setText("replace PCB and keep Sketch in curr. doc")
        self.radioBtn_keep_sketch.setObjectName("radioBtn_keep_sketch")
        self.verticalLayout.addWidget(self.radioBtn_keep_sketch)

        self.retranslateUi(LayerSelection)
        self.buttonBoxLayer.accepted.connect(LayerSelection.accept)
        self.buttonBoxLayer.rejected.connect(LayerSelection.reject)
        QtCore.QMetaObject.connectSlotsByName(LayerSelection)
#-------#-------------------------------------------------------------------------
        self.comboBoxLayerSel.currentTextChanged.connect(self.on_combobox_changed) #addition

    def retranslateUi(self, LayerSelection):
        pass
        
    def on_combobox_changed(self, value):
        print('combo change',value)
        if value != 'Edge.Cuts':
            self.radioBtn_newdoc.setChecked(True)
            self.radioBtn_replace_pcb.setEnabled(False)
            self.radioBtn_keep_sketch.setEnabled(False)
        else:
            self.radioBtn_replace_pcb.setEnabled(True)
            self.radioBtn_keep_sketch.setEnabled(True)
##
class Ui_LayerSelectionOut(object):
    def setupUi(self, LayerSelectionOut):
        LayerSelectionOut.setObjectName("LayerSelectionOut")
        LayerSelectionOut.resize(293, 249)
        LayerSelectionOut.setWindowTitle("LayerSelection")
        LayerSelectionOut.setToolTip("")
        self.buttonBoxLayer = QtWidgets.QDialogButtonBox(LayerSelectionOut)
        self.buttonBoxLayer.setGeometry(QtCore.QRect(10, 200, 271, 32))
        self.buttonBoxLayer.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBoxLayer.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBoxLayer.setObjectName("buttonBoxLayer")
        self.verticalLayoutWidget = QtWidgets.QWidget(LayerSelectionOut)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 271, 80))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label.setText("Select the layer to push the Sketch\nDefault \'Edge.Cuts\'")
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.verticalLayout.addLayout(self.verticalLayout_2)
        self.comboBoxLayerSel = QtWidgets.QComboBox(self.verticalLayoutWidget)
        self.comboBoxLayerSel.setObjectName("comboBoxLayerSel")
        self.verticalLayout.addWidget(self.comboBoxLayerSel)
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(LayerSelectionOut)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(10, 90, 271, 99))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.width_label = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.width_label.setMinimumSize(QtCore.QSize(150, 0))
        self.width_label.setToolTip("")
        self.width_label.setText("Line Width:")
        self.width_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.width_label.setObjectName("width_label")
        self.horizontalLayout.addWidget(self.width_label)
        self.lineEdit_width = QtWidgets.QLineEdit(self.verticalLayoutWidget_2)
        self.lineEdit_width.setToolTip("Line width for drawings")
        self.lineEdit_width.setText("0.16")
        self.lineEdit_width.setObjectName("lineEdit_width")
        self.horizontalLayout.addWidget(self.lineEdit_width)
        self.verticalLayout_3.addLayout(self.horizontalLayout)

        self.retranslateUi(LayerSelectionOut)
        self.buttonBoxLayer.accepted.connect(LayerSelectionOut.accept)
        self.buttonBoxLayer.rejected.connect(LayerSelectionOut.reject)
        QtCore.QMetaObject.connectSlotsByName(LayerSelectionOut)

#-------#-------------------------------------------------------------------------
        self.comboBoxLayerSel.currentTextChanged.connect(self.on_combobox_changed) #addition

    def retranslateUi(self, LayerSelectionOut):
        pass
        
    def on_combobox_changed(self, value):
        print('combo change',value)
        if 'Zone' in value:
            self.lineEdit_width.setEnabled(False)
            self.width_label.setEnabled(False)
            #self.width_label.setText("-----:")
        else:
            self.lineEdit_width.setEnabled(True)
            self.width_label.setEnabled(True)
##

def PushPCB():
#def onExport3DStep(self):
    global last_3d_path, start_time, load_sketch, last_pcb_path, edge_width
    #say("export3DSTEP")
    if load_sketch==False:
        msg="""<b>Edge editing NOT supported on FC0.15!</b><br>please upgrade your FC release"""
        say_warning(msg)
        msg="Edge editing NOT supported on FC0.15!"
        sayerr(msg)            
    #if 0:
    #if FreeCAD.ActiveDocument is None:
    #    FreeCAD.newDocument("PCB_Sketch")
    #    PCB_Sketch= FreeCAD.activeDocument().addObject('Sketcher::SketchObject','PCB_Sketch')
    #    offset=[0.0,0.0] #offset=[148.5,98.5]
    #    FreeCAD.activeDocument().PCB_Sketch.Placement = FreeCAD.Placement(FreeCAD.Vector(offset[0],offset[1]),FreeCAD.Rotation(0.000000,0.000000,0.000000,1.000000))
    #    FreeCAD.getDocument('PCB_Sketch').recompute()
    #    FreeCADGui.SendMsgToActiveView("ViewFit")
    else:
        sel = FreeCADGui.Selection.getSelection()
        if len (sel) == 1:
            #sayw(doc.Name)
            if "Sketch" in sel[0].TypeId:
                cfg_read_all()
                if len(last_pcb_path) == 0:
                    last_pcb_path = ""
                #    last_3d_path=last_pcb_path
                #    sayw(last_pcb_path)
                #getSaveFileName(self,"saveFlle","Result.txt",filter ="txt (*.txt *.)")
                layer_list = ['Edge.Cuts','Dwgs.User','Cmts.User','Eco1.User','Eco2.User','Margin', 'F.FillZone', 'F.KeepOutZone', 'F.MaskZone','B.FillZone', 'B.KeepOutZone', 'B.MaskZone',]
                LayerSelectionDlg = QtGui.QDialog()
                ui = Ui_LayerSelectionOut()
                ui.setupUi(LayerSelectionDlg)
                ui.comboBoxLayerSel.addItems(layer_list)
                reply=LayerSelectionDlg.exec_()
                if reply==1: # ok
                    SketchLayer=str(ui.comboBoxLayerSel.currentText())
                    if 1: #'Edge' not in SketchLayer:
                        edge_width=float(ui.lineEdit_width.text().replace(',','.'))
                    print(SketchLayer)
                    skname=sel[0].Name
                #else:  #canel
                #    print('Cancel')
                #    stop
                #    pass
                    testing=False
                    if not testing:
                        Filter=""
                        name, Filter = PySide.QtGui.QFileDialog.getSaveFileName(None, "Push Sketch PCB Edge to KiCad board ...",
                            make_unicode(last_pcb_path), "*.kicad_pcb")
                    else:
                        name='d:/Temp/e2.kicad_pcb'
                    #say(name)
                    if name:
                        if os.path.exists(name):
                            last_pcb_path=os.path.dirname(name)
                            pg = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/kicadStepUp")
                            pg.SetString("last_pcb_path",make_string(last_pcb_path))
                            start_time=current_milli_time()
                            export_pcb(name,SketchLayer,skname)
                        else:
                            msg="""Save to <b>an EXISTING KiCad pcb file</b> to update your Edge!"""
                            say_warning(msg)
                            msg="Save to an EXISTING KiCad pcb file to update your Edge!"
                            sayerr(msg)
                else:  #cancel
                    print('Cancel')
                    pass    
            else:
                msg="""select one Sketch to be pushed to kicad board!"""
                sayerr(msg)
                say_warning(msg)
        
        else:
            msg="""select one Sketch to be pushed to kicad board!"""
            sayerr(msg)
            say_warning(msg)
##
def Sync3DModel():
    global last_3d_path, start_time
    global last_fp_path, test_flag
    global configParser, configFilePath, last_pcb_path
    global ignore_utf8, ignore_utf8_incfg, disable_PoM_Observer
    global board_base_point_x, board_base_point_y, real_board_pos_x, real_board_pos_y
    global pcb_path, use_AppPart, force_oldGroups, use_Links, use_LinkGroups
    global original_filename, aux_orig, grid_orig
    global off_x, off_y, maxRadius, use_pypro

    import fcad_parser
    from fcad_parser import KicadPCB,SexpList
    import kicad_parser

    #say("export3DSTEP")
    if load_sketch==False:
        msg="""<b>Board editing NOT supported on FC0.15!</b><br>please upgrade your FC release"""
        say_warning(msg)
        msg="Board editing NOT supported on FC0.15!"
        sayerr(msg)            
    else:
        sel = FreeCADGui.Selection.getSelection()
        if len (sel) == 1:
            if hasattr(sel[0],"Shape") or "Link" in sel[0].TypeId:
                cfg_read_all()
                if len(last_pcb_path) == 0:
                    last_pcb_path = ""
                    #sayw(last_pcb_path)
                #getSaveFileName(self,"saveFlle","Result.txt",filter ="txt (*.txt *.)")
                testing=False
                if not testing:
                    Filter=""
                    fname, Filter = PySide.QtGui.QFileDialog.getOpenFileName(None, "Load KiCad PCB board data...",
                        make_unicode(last_pcb_path), "*.kicad_pcb")
                else:
                    fname='c:/Temp/demo/demo-test-mp.kicad_pcb'
                if fname is not None:
                    if os.path.exists(fname):
                        last_pcb_path=os.path.dirname(fname)
                        pg = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/kicadStepUp")
                        pg.SetString("last_pcb_path",make_string(last_pcb_path))
                        start_time=current_milli_time()
                        doc=FreeCAD.ActiveDocument
                        #filePath=last_pcb_path
                        #fpath=filePath+os.sep+doc.Label+'.kicad_pcb'
                        #sayerr('to '+fpath)
                        #print fname
                        if fname is None:
                            fpath=original_filename
                        else:
                            fpath=fname
                        sayerr('Loading from '+fpath)
                        #stop
                        if len(fpath) > 0:
                            #new_edge_list=getBoardOutline()
                            #say (new_edge_list)
                            cfg_read_all()
                            path, fname = os.path.split(fpath)
                            name=os.path.splitext(fname)[0]
                            ext=os.path.splitext(fname)[1]
                            fpth = os.path.dirname(os.path.abspath(fpath))
                            #filePath = os.path.split(os.path.realpath(__file__))[0]
                            say ('file path '+fpth); say('kicad board file: '+fname)
                            # stop
                            if fpth == "":
                                fpth = "."
                            last_pcb_path = fpth
                            last_pcb_path = re.sub("\\\\", "/", last_pcb_path)
                            ini_vars[10] = last_pcb_path
                            #cfg_update_all()
                            #sayerr(name+':'+ext)
                            pg = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/kicadStepUp")
                            pg.SetString("last_pcb_path", make_string(last_pcb_path))
                            mypcb = KicadPCB.load(fpath)
                            reply=False;ref_found=False;input_ref=''
                            #input_ref = QtGui.QInputDialog.getText(None, 'Sync Ref', 'Reference to be synced',QtGui.QLineEdit.EchoMode.Normal,'REF#',reply)
                            input_ref = QtGui.QInputDialog.getText(None, 'Sync Ref', 'Reference to be synced',QtGui.QLineEdit.EchoMode.Normal,'REF#') #,reply)
                            #print (reply);print('*');print input_ref
                            if len(input_ref) > 1:
                                if input_ref[1]:
                                    matching_Reference=input_ref[0] #'LD1'
                                    matching_TimeStamp='Null'
                                    for m in mypcb.module:
                                        Ref = m.fp_text[0][1]
                                        #print(Ref);print(len(Ref))
                                        if Ref.lstrip('"').rstrip('"') == matching_Reference:
                                            say ('found Reference:  '+Ref)
                                            ref_found=True
                                            if hasattr(m,'tstamp'):
                                                matching_TimeStamp=m.tstamp
                                                say ('linked TimeStamp: '+matching_TimeStamp)
                                                if sel[0].Label.rfind('_') < sel[0].Label.rfind('['):
                                                    ts = sel[0].Label[sel[0].Label.rfind('_')+1:sel[0].Label.rfind('[')]
                                                    nbrModel = sel[0].Label[sel[0].Label.rfind('['):]
                                                else:
                                                    ts = sel[0].Label[sel[0].Label.rfind('_')+1:]
                                                    nbrModel = ''
                                                #ts = sel[0].Label[sel[0].Label.rfind('_')+1:]
                                                #mmodel=m.model[0][0]
                                                #print (mmodel[mmodel.rfind('/')+1:mmodel.rfind('.')]);stop
                                                if len (m.model)>0:
                                                    if nbrModel == '':
                                                        mmodel=m.model[0][0]
                                                    else:
                                                        nMd=int(nbrModel.replace('[','').replace(']',''))-1
                                                        #print (nMd)
                                                        mmodel=m.model[nMd][0]
                                                    if mmodel.rfind('/') !=-1:
                                                        mmodel=mmodel[mmodel.rfind('/')+1:mmodel.rfind('.')]
                                                    else:
                                                        mmodel=mmodel[mmodel.rfind('\\')+1:mmodel.rfind('.')]
                                                else:
                                                    mmodel=''
                                                if ((len (ts) != 8) and (len (ts) != 12)) or sel[0].Label.rfind('_') == -1:
                                                    msg="TimeStamp not found!\nAdding & Syncing Ref & TimeStamp"
                                                    sayw(msg)
                                                    if len (mmodel)>0:
                                                        sel[0].Label=Ref+'_'+mmodel.replace('.','')+'_'+matching_TimeStamp+nbrModel
                                                    else:
                                                        sel[0].Label=Ref+'_'+sel[0].Label+'_'+matching_TimeStamp+nbrModel
                                                else:
                                                    if len(matching_TimeStamp) > 8:
                                                        matching_TimeStamp=matching_TimeStamp[-12:]
                                                    if len (mmodel)>0:
                                                        sel[0].Label=Ref.lstrip('"').rstrip('"')+'_'+mmodel.replace('.','')+'_'+matching_TimeStamp+nbrModel
                                                    else:
                                                        sel[0].Label=Ref.lstrip('"').rstrip('"')+sel[0].Label[sel[0].Label.find('_'):sel[0].Label.rfind('_')+1]+matching_TimeStamp+nbrModel
                                                    msg="Adding & Syncing Ref & TimeStamp"
                                                    say(msg)                                                    
                                                #sel[0].Label=Ref+sel[0].Label[sel[0].Label.index('_'):sel[0].Label.rindex('_')+1]+matching_TimeStamp
                                                msg="""<b>3D model Reference & TimeStamp synced<br>with the Reference """+Ref+""" of the kicad board!</b><br><br>"""
                                                msgr="3D model Reference & TimeStamp synced\nwith the Reference "+Ref+" of the kicad board!"
                                                say(msgr)
                                                say_info(msg)
                                            else:
                                                sayerr('Reference: '+Ref+' is missing TimeStamp field')
                                                msg="""<b>Reference: """+Ref+""" is missing TimeStamp field<b>"""
                                                say_warning(msg)
                                    if not ref_found:
                                        sayerr('Reference: '+matching_Reference+' not found!')
                                        msg="""<b>Reference: """+matching_Reference+""" not found!<b>"""
                                        say_warning(msg)
                                else:
                                    msg="""Operation aborted!"""
                                    sayerr(msg)
                                    say_info(msg)
                                    #model_data=re.findall('\s\(module(\s'+matching_Reference+'\s.+?)\(at',data, re.MULTILINE|re.DOTALL)
                                    #model_data=re.findall('\s\(fp_text\s(reference\s'+matching_Reference'+'\s.+?)\(at,data, re.MULTILINE|re.DOTALL)
                    else:
                        msg="""Load <b>an EXISTING KiCad pcb file</b> to sync your 3D model Reference & TimeStamp!"""
                        say_warning(msg)
                        msg="Load an EXISTING KiCad pcb file to sync your 3D model Reference & TimeStamp!"
                        sayerr(msg)
                else:
                    msg="""select one 3D model to sync its TimeStamp based on its Reference in the kicad board!"""
                    sayerr(msg)
                    say_warning(msg)
            else:
                msg="""Operation aborted!"""
                sayerr(msg)
                say_info(msg)
        else:
            msg="""select one 3D model to sync its TimeStamp based on its Reference in the kicad board!"""
            sayerr(msg)
            say_warning(msg)

###
def PushMoved():
    global last_3d_path, start_time
    global last_fp_path, test_flag
    global configParser, configFilePath, last_pcb_path
    global ignore_utf8, ignore_utf8_incfg, disable_PoM_Observer
    global board_base_point_x, board_base_point_y, real_board_pos_x, real_board_pos_y
    global pcb_path, use_AppPart, force_oldGroups, use_Links, use_LinkGroups
    global original_filename, aux_orig, grid_orig
    global off_x, off_y, maxRadius, use_pypro

    import fcad_parser
    from fcad_parser import KicadPCB,SexpList
    import kicad_parser

    ## to export to STEP an object and its links with a different placement and label
    ## two options must be set: 1) disable 'Reduce number of objects'; 2) disable 'Ignore instance names'
    ## NB the second one is not good for collaboration with different cads
    
    #say("export3DSTEP")
    if load_sketch==False:
        msg="""<b>Board editing NOT supported on FC0.15!</b><br>please upgrade your FC release"""
        say_warning(msg)
        msg="Board editing NOT supported on FC0.15!"
        sayerr(msg)            
    else:
        check_ok=False
        sel = FreeCADGui.Selection.getSelection()
        if len (sel) >= 1:
            for s in sel:
                if s.Label.rfind('_') < s.Label.rfind('['):
                    ts = s.Label[s.Label.rfind('_')+1:s.Label.rfind('[')]
                else:
                    ts = s.Label[s.Label.rfind('_')+1:]
                if len (ts) == 8 or len (ts) == 12:
                    #print(ts);stop
                    check_ok=True
                    #stop
                    break
            #else:
            #    msg="""select only 3D model(s) moved to be updated/pushed to kicad board!<br><b>a TimeSTamp is required!</b>"""
            #    sayerr(msg)
            #    say_warning(msg)
        if check_ok:
            cfg_read_all()
            #pg = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/kicadStepUp")
            #pg.GetString("last_3d_path")
            if len(last_pcb_path) == 0:
                last_pcb_path=u''
                #sayw(last_pcb_path)
            #getSaveFileName(self,"saveFlle","Result.txt",filter ="txt (*.txt *.)")
            testing=False #True
            if not testing:
                Filter=""
                fname, Filter = PySide.QtGui.QFileDialog.getSaveFileName(None, "Push 3D PCB position(s) to KiCad board ...",
                    make_unicode(last_pcb_path), "*.kicad_pcb")
            else:
                fname='c:/Temp/demo/test-rot.kicad_pcb'
            if fname:
                if os.path.exists(fname):
                    last_3d_path=os.path.dirname(fname)
                    pg = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/kicadStepUp")
                    pg.SetString("last_3d_path",make_string(last_3d_path))
                    start_time=current_milli_time()
                    doc=FreeCAD.ActiveDocument
                    #filePath=last_pcb_path
                    #fpath=filePath+os.sep+doc.Label+'.kicad_pcb'
                    #sayerr('to '+fpath)
                    #print fname
                    if fname is None:
                        fpath=original_filename
                    else:
                        fpath=fname
                    sayerr('saving to '+fpath)
                    #stop
                    if len(fpath) > 0:
                        #new_edge_list=getBoardOutline()
                        #say (new_edge_list)
                        cfg_read_all()
                        path, fname = os.path.split(fpath)
                        name=os.path.splitext(fname)[0]
                        ext=os.path.splitext(fname)[1]
                        fpth = os.path.dirname(os.path.abspath(fpath))
                        #filePath = os.path.split(os.path.realpath(__file__))[0]
                        say ('my file path '+fpth)
                        # stop
                        if fpth == "":
                            fpth = "."
                        last_pcb_path = fpth
                        last_pcb_path = re.sub("\\\\", "/", last_pcb_path)
                        ini_vars[10] = last_pcb_path
                        #cfg_update_all()
                        pg = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/kicadStepUp")
                        pg.SetString("last_pcb_path", make_string(last_pcb_path))
                        #sayerr(name+':'+ext)
                        #mypcb = KicadPCB.load(fpath)
                        with codecs.open(fpath,'r', encoding='utf-8') as txtFile:
                            content = txtFile.readlines() # problems?
                        content.append(u" ")
                        txtFile.close()
                        data=u''.join(content)
                        tml= time.localtime()
                        now=str(tml.tm_year)+'-'+str(tml.tm_mon)+'-'+str(tml.tm_mday)+'-'+str(tml.tm_hour)+'.'+str(tml.tm_min)+'.'+str(tml.tm_sec)
                        #foname=os.path.join(path, name+'-bkp-'+now+ext+'-bak')
                        foname=os.path.join(path, name+u'-bkp-'+make_unicode(now)+ext+u'-bak')
                        oft=None
                        if aux_orig == 1:
                            oft=getAuxOrigin(data)
                        elif grid_orig == 1:
                            oft=getGridOrigin(data)
                        #print oft
                        gof=False
                        origin_warn=False
                        if oft is not None:
                            if oft == [0.0,0.0]:
                                origin_warn=True
                            off_x=oft[0];off_y=-oft[1]
                            offset = oft
                            gof=True
                            pcb_push=True
                        else:
                            pcb_push=False
                        testing=False #True
                        if testing is not True:
                            try:
                                #with codecs.open(foname,'w', encoding='utf-8') as ofile:
                                #    ofile.write(data)
                                #    ofile.close()
                                copyfile(fpath, foname)
                                say('file copied')
                            except:
                                msg="""<b>problem in writing permissions to kicad board!</b><br><br>"""
                                msg+="<b>file saving aborted to<br>"+fpath+"</b><br><br>"
                                msgr="problem in writing permissions to kicad board!\n"
                                msgr+="file saving aborted to "+fpath+"\n"
                                pcb_push=False
                                say(msgr)
                                say_info(msg)
                    if pcb_push:
                        mdp = 0
                        for s in sel:
                            #sayw(doc.Name)
                            if use_pypro:
                                if hasattr(s,"TimeStamp"):
                                    ts=s.TimeStamp
                                    content = push3D2pcb(s,content,ts)
                                else:
                                    msg="""select only 3D model(s) moved to be updated/pushed to kicad board!"""
                                    sayerr(msg)
                                    say_warning(msg)
                            else:
                                if s.Label.rfind('_') < s.Label.rfind('['):
                                    ts = s.Label[s.Label.rfind('_')+1:s.Label.rfind('[')]
                                else:
                                    ts = s.Label[s.Label.rfind('_')+1:]
                                if len (ts) == 8 or len (ts) == 12:
                                    mdp+=1
                                    #print(ts);stop
                                    content = push3D2pcb(s,content,ts)
                                #else:
                                #    msg="""select only 3D model(s) moved to be updated/pushed to kicad board!<br><b>a TimeSTamp is required!</b>"""
                                #    sayerr(msg)
                                #    say_warning(msg)
                        newcontent=u''.join(content)
                        #pcbTracks=re.findall('\s\(tracks(\s.+?)\)',data, re.MULTILINE|re.DOTALL)
                        found_tracks=True
                        if 0: # forcing found tracks to true 'cause kicad 6 doesn't write it anymore inside the file
                            pcbTracks=re.findall('\s\(tracks(\s.+?)\)',data, re.MULTILINE|re.DOTALL)
                            found_tracks=False
                            if len(pcbTracks)>0:
                                try:
                                    if (float(pcbTracks[0])) > 0:
                                        found_tracks=True
                                except:
                                    found_tracks=True
                        with codecs.open(fpath,'w', encoding='utf-8') as ofile:
                            ofile.write(newcontent)
                            ofile.close()        
                        say_time()
                        say('pushed '+str(mdp)+' model(s)')
                        msg="""<b>3D model new position(s) pushed to kicad board!</b><br>["""+str(mdp)+""" model(s) updated]<br><br>"""
                        if found_tracks:
                            msg+="<font color='blue'><b>in case of tracks<br></b>you will need to fix your routing!</font><br><br>"
                        msg+="<b>file saved to<br>"+fpath+"</b><br><br>"
                        msg+="<i>backup file saved to<br>"+foname+"</i><br>"
                        msgr="3D model new position pushed to kicad board!\n"
                        msgr+="file saved to "+fpath+"\n"
                        msgr+="backup file saved to "+foname
                        say(msgr)
                        say_info(msg)
                        if origin_warn:
                            if aux_orig == 1:
                                origin_msg='AuxOrigin'
                            elif grid_orig == 1:
                                origin_msg='GridOrigin'
                            msg = origin_msg +' is set in FC Preferences but not set in KiCAD pcbnew file'
                            sayw(msg)
                            msg="""<b><font color='red'>"""+origin_msg+""" is set in FreeCAD Preferences<br>but not set in KiCAD pcbnew file</font></b>"""
                            msg+="""<br><br>Please assign """+origin_msg+""" to your KiCAD pcbnew board file"""
                            msg+="""<br>for a better Mechanical integration"""
                            say_warning(msg)
                    else:
                        msg="""To update 3D model Position(s) in <b>an EXISTING KiCad pcb file</b><br>the KiCAD pcbnew board file must have assigned \'Grid Origin\' or<br>\'Aux Origin\' (Drill and Place offset)!"""
                        msg+="""<br>Moreover in FC StepUP preferences you must have<br>\'PCB Settings\'->\'PCB Placement\'<br>set to \'Grid Origin\' or \'Aux Origin\'"""
                        say_warning(msg)
                        msg="To update 3D model Position(s) in an EXISTING KiCad pcb file\nthe KiCAD pcbnew board file must have assigned \'Grid Origin\' or \'Aux Origin\' (Drill and Place offset)!"
                        msg+="\nMoreover in FC StepUP preferences you must have\n\'PCB Settings\'->\'PCB Placement\'\nset to \'Grid Origin\' or \'Aux Origin\'"
                        sayerr(msg)
                else:
                    msg="""Save to <b>an EXISTING KiCad pcb file</b> to update your 3D model position!"""
                    say_warning(msg)
                    msg="Save to an EXISTING KiCad pcb file to update your 3D model position!"
                    sayerr(msg)
            else:
                msg="""Operation aborted!"""
                sayerr(msg)
                say_info(msg)
        else:
            msg="""select only 3D model(s) moved to be updated/pushed to kicad board!<br><b>a Time Stamp is required!</b>"""
            sayerr(msg)
            say_warning(msg)

###
def getModelsData(mypcb):
    """ mypcb = KicadPCB.load(file_pcb) """
    ## NB use always float() to guarantee number not string!!!
    import fcad_parser
    from fcad_parser import KicadPCB,SexpList
    import kicad_parser
    
    warn=""
    PCB_Models = []
    Edge_Cuts_lvl=44
    Top_lvl=0
    conv_offs=25.4
    if hasattr(mypcb, 'host'):
        print(mypcb.host)
    if hasattr(mypcb, 'version'):
        version = float(mypcb.version)
        if version <= 3:
            QtGui.QApplication.restoreOverrideCursor()
            reply = QtGui.QMessageBox.information(None,"Error ...","... KICAD pcb version "+ str(version)+" not supported \r\n"+"\r\nplease open and save your board with the latest kicad version")
            stop
        if version>=4:
            Edge_Cuts_lvl=44
            Top_lvl=0
        conv_offs=1.0
        if version >= 20171114:
            conv_offs=25.4
    
    for lynbr in mypcb.layers: #getting layers name
        if float(lynbr) == Top_lvl:
            LvlTopName=(mypcb.layers['{0}'.format(str(lynbr))][0])
        if float(lynbr) == Edge_Cuts_lvl:
            LvlEdgeName=(mypcb.layers['{0}'.format(str(lynbr))][0])

    for m in mypcb.module:  #parsing modules  #check top/bottom for placing 3D models
        #print(m.tstamp);print(m.fp_text[0][1])
        #stop
        if len(m.at)==2:
            m_angle=0
        else:
            m_angle=m.at[2]
        m_at=[m.at[0],-m.at[1]] #y reversed
        virtual=0
        if hasattr(m, 'attr'):
            if 'virtual' in m.attr:
                #say('virtual module')
                virtual=1
        else:
            virtual=0
        m_x = float(m.at[0])
        m_y = float(m.at[1]) * (-1)
        m_rot = float(m_angle)
        #sayw(m.layer);sayerr(LvlTopName)
        if m.layer == LvlTopName:  # top
            side = "Top"
            #sayw('top ' + m.layer)
        else:
            side = "Bottom"
            m_rot *= -1 ##bottom 3d model rotation
            #sayw('bot ' + m.layer)
        n_md=1
        for md in m.model:
            #say (md[0]) #model name
            #say(md.at.xyz)
            #say(md.scale.xyz)
            #say(md.rotate.xyz)
            error_scale_module=False
            #say('scale ');sayw(scale_vrml)#;
            #error_scale_module=False
            xsc_vrml_val=md.scale.xyz[0]
            ysc_vrml_val=md.scale.xyz[1]
            zsc_vrml_val=md.scale.xyz[2]        
            # if scale_vrml!='1 1 1':
            if float(xsc_vrml_val)!=1 or float(ysc_vrml_val)!=1 or float(zsc_vrml_val)!=1:
                if "box_mcad" not in md[0] and "cylV_mcad" not in md[0] and "cylH_mcad" not in md[0]:
                    sayw('wrong scale!!! set scale to (1 1 1)')
                error_scale_module=True
            #model_list.append(mdl_name[0])
            #model=model_list[j]+'.wrl'
            #if py2:
            if sys.version_info[0] == 2: #py2
                model=md[0].decode("utf-8")
                #stop
            else: #py3
                model=md[0] # py3 .decode("utf-8")
            #print (model, ' MODEL', type(model)) #maui test py3
            if (virtual==1 and addVirtual==0):
                model_name='no3Dmodel'
                side='noLayer'
                if model:
                    sayw("virtual model "+model+" skipped") #virtual found warning
            else:
                if model:
                    model_name=model
                    #sayw(model_name)
                    warn=""
                    if "box_mcad" not in model_name and "cylV_mcad" not in model_name and "cylH_mcad" not in model_name:
                        if error_scale_module:
                            sayw('wrong scale!!! for '+model_name+' Set scale to (1 1 1)')
                            msg="""<b>Error in '.kicad_pcb' model footprint</b><br>"""
                            msg+="<br>reset values of<br><b>"+model_name+"</b><br> to:<br>"
                            msg+="(scale (xyz 1 1 1))<br>"
                            #warn+=("reset values of scale to (xyz 1 1 1)")
                            warn=("reset values of scale to (xyz 1 1 1)")
                            ##reply = QtGui.QMessageBox.information(None,"info", msg)
                            #stop
                    #model_name=model_name[1:]
                    #say(model_name)
                    #sayw("here")
                else:
                    model_name='no3Dmodel'  #to do how to manage no3Dmodel
                    side='noLayer'
                    sayerr('no3Dmodel')
                mdl_name=model_name # re.findall(r'(.+?)\.wrl',params)
                #if virtual == 1:
                #    sayerr("virtual model(s)");sayw(mdl_name)
                # sayw(mdl_name)
                # sayerr(params)
                if len(mdl_name) > 0:
                    # model_name, rot_comb, warn, pos_vrml, rotz_vrml, scale_vrml = get3DParams(mdl_name,params, rot, virtual)
                    #sayerr(md.at.xyz)
                    if conv_offs != 1: #pcb version >= 20171114 (offset wrl in mm)
                        if hasattr(md,'at'):
                            ofs=[md.at.xyz[0]/conv_offs,md.at.xyz[1]/conv_offs,md.at.xyz[2]/conv_offs]
                        if hasattr(md,'offset'):
                            ofs=[md.offset.xyz[0]/conv_offs,md.offset.xyz[1]/conv_offs,md.offset.xyz[2]/conv_offs]
                    else:
                        ofs=md.at.xyz
                    line = []
                    line.append(model_name)
                    line.append(m_x)
                    line.append(m_y)
                    line.append(m_rot-md.rotate.xyz[2])
                    line.append(side)
                    line.append(warn)
                    line.append(ofs) #(md.at.xyz) #pos_vrml)
                    line.append(md.rotate.xyz) #rotz_vrml)
                    #sayerr(rotz_vrml)
                    line.append(md.scale.xyz) #scale_vrml)
                    line.append(virtual)
                    if hasattr(m,'tstamp'):
                        line.append(m.tstamp) # fp tstamp
                    else:
                        sayw('missing \'TimeStamp\'')
                        line.append('null')
                    line.append(m.fp_text[0][1]) #fp reference
                    line.append(n_md) #number of models in module
                    PCB_Models.append(line)
                    n_md+=1
    return PCB_Models
###

def PullMoved():
    global last_3d_path, start_time
    global last_fp_path, test_flag
    global configParser, configFilePath, last_pcb_path
    global ignore_utf8, ignore_utf8_incfg, disable_PoM_Observer
    global board_base_point_x, board_base_point_y, real_board_pos_x, real_board_pos_y
    global pcb_path, use_AppPart, force_oldGroups, use_Links, use_LinkGroups
    global original_filename, aux_orig, grid_orig
    global off_x, off_y, maxRadius, use_pypro
    
    import fcad_parser
    from fcad_parser import KicadPCB,SexpList
    import kicad_parser
    
    ## to export to STEP an object and its links with a different placement and label
    ## two options must be set: 1) disable 'Reduce number of objects'; 2) disable 'Ignore instance names'
    ## NB the second one is not good for collaboration with different cads
    
    #say("export3DSTEP")
    if load_sketch==False:
        msg="""<b>Board editing NOT supported on FC0.15!</b><br>please upgrade your FC release"""
        say_warning(msg)
        msg="Board editing NOT supported on FC0.15!"
        sayerr(msg)            
    else:
        check_ok=False
        sel = FreeCADGui.Selection.getSelection()
        if len (sel) >= 1:
            for s in sel:
                if s.Label.rfind('_') < s.Label.rfind('['):
                    ts = s.Label[s.Label.rfind('_')+1:s.Label.rfind('[')]
                else:
                    ts = s.Label[s.Label.rfind('_')+1:]
                if len (ts) == 8 or len (ts) == 12:
                    #print(ts);stop
                    check_ok=True
                    #stop
                    break
            #else:
            #    msg="""select only 3D model(s) moved to be updated/pushed to kicad board!<br><b>a TimeSTamp is required!</b>"""
            #    sayerr(msg)
            #    say_warning(msg)
        if check_ok:
            cfg_read_all()
            #pg = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/kicadStepUp")
            #pg.GetString("last_3d_path")
            if len(last_pcb_path) == 0:
                last_pcb_path=u''
                #sayw(last_pcb_path)
            #getSaveFileName(self,"saveFlle","Result.txt",filter ="txt (*.txt *.)")
            testing=False #True
            if not testing:
                Filter=""
                fname, Filter = PySide.QtGui.QFileDialog.getOpenFileName(None, "Pull 3D model position(s) from pcbnew File...",
                    make_unicode(last_pcb_path), "*.kicad_pcb")
            else:
                fname='c:/Temp/demo/test-rot.kicad_pcb'
            if fname:
                if os.path.exists(fname):
                    last_3d_path=os.path.dirname(fname)
                    pg = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/kicadStepUp")
                    pg.SetString("last_3d_path",make_string(last_3d_path))
                    start_time=current_milli_time()
                    doc=FreeCAD.ActiveDocument
                    #filePath=last_pcb_path
                    #fpath=filePath+os.sep+doc.Label+'.kicad_pcb'
                    #sayerr('to '+fpath)
                    #print fname
                    if fname is None:
                        fpath=original_filename
                    else:
                        fpath=fname
                    sayerr('loading from '+fpath)
                    #stop
                    if len(fpath) > 0:
                        #new_edge_list=getBoardOutline()
                        #say (new_edge_list)
                        cfg_read_all()
                        path, fname = os.path.split(fpath)
                        name=os.path.splitext(fname)[0]
                        ext=os.path.splitext(fname)[1]
                        fpth = os.path.dirname(os.path.abspath(fpath))
                        #filePath = os.path.split(os.path.realpath(__file__))[0]
                        say ('my file path '+fpth)
                        # stop
                        if fpth == "":
                            fpth = "."
                        last_pcb_path = fpth
                        last_pcb_path = re.sub("\\\\", "/", last_pcb_path)
                        ini_vars[10] = last_pcb_path
                        #cfg_update_all()
                        pg = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/kicadStepUp")
                        pg.SetString("last_pcb_path", make_string(last_pcb_path))
                        #sayerr(name+':'+ext)
                        mypcb = KicadPCB.load(fpath)
                        mymodels = getModelsData(mypcb)
                        pcbThickness=float(mypcb.general.thickness)
                        #print(mymodels)
                        #stop
                        #with codecs.open(fpath,'r', encoding='utf-8') as txtFile:
                        #    content = txtFile.readlines() # problems?
                        #content.append(u" ")
                        #txtFile.close()
                        #data=u''.join(content)
                        #oft=None
                        #if aux_orig == 1:
                        #    oft=getAuxOrigin(data)
                        #if grid_orig == 1:
                        #    oft=getGridOrigin(data)
                        #print oft
                        #gof=False
                        #if oft is not None:
                        #    off_x=oft[0];off_y=-oft[1]
                        #    offset = oft
                        #    gof=True
                        #    pcb_pull=True
                        #else:
                        #    pcb_pull=False
                        oft=None
                        if aux_orig == 1:
                            if hasattr(mypcb, 'setup'):
                                if hasattr(mypcb.setup, 'aux_axis_origin'):
                                    oft = mypcb.setup.aux_axis_origin 
                                    #oft=getAuxOrigin(data)
                                else:
                                    oft = [0.0,0.0]
                        elif grid_orig == 1:
                            if hasattr(mypcb, 'setup'):
                                if hasattr(mypcb.setup, 'grid_origin'):
                                    oft=mypcb.setup.grid_origin
                                else:
                                    oft = [0.0,0.0]
                            else:
                                oft = [0.0,0.0]
                                #oft=getGridOrigin(data)
                        #print ('oft ',oft)
                        gof=False
                        
                        origin_warn=False
                        if oft is not None:
                            if oft == [0.0,0.0]:
                                origin_warn=True
                            off_x=oft[0];off_y=-oft[1]
                            offset = oft
                            gof=True
                            pcb_pull=True
                        else:
                            pcb_pull=False
                        #print ('ofx,ofy reviewed ',off_x,' ',off_y)
                        testing=False #True
                    if pcb_pull:
                        for s in sel:
                            #sayw(doc.Name)
                            if 0: # use_pypro:
                                if hasattr(s,"TimeStamp"):
                                    ts=s.TimeStamp
                                    content = push3D2pcb(s,content,ts,pcbThickness)
                                else:
                                    msg="""select only 3D model(s) to be updated/pulled from kicad board!"""
                                    sayerr(msg)
                                    say_warning(msg)
                            else:
                                if s.Label.rfind('_') < s.Label.rfind('['):
                                    ts = s.Label[s.Label.rfind('_')+1:s.Label.rfind('[')]
                                else:
                                    ts = s.Label[s.Label.rfind('_')+1:]
                                if len (ts) == 8 or len (ts) == 12:
                                    #print (s.Label) #;stop
                                    nbrModel = None
                                    if s.Label.rfind('_') < s.Label.rfind('['):
                                        #ts = s.Label[s.Label.rfind('_')+1:s.Label.rfind('[')]
                                        nbrModel = s.Label[s.Label.rfind('['):]
                                        #print(nbrModel)
                                        nMd = int(nbrModel.replace('[','').replace(']',''))-1
                                    else:
                                        #ts = s.Label[s.Label.rfind('_')+1:]
                                        nMd = 0
                                        #print('nbrModel = 0')
                                    #print('timestamp',ts,'numModel',nMd)
                                    content = pull3D2dsn(s,mymodels,ts,nMd,gof,pcbThickness)
                                #else:
                                #    msg="""select only 3D model(s) to be updated/pulled from kicad board!<br><b>a TimeSTamp is required!</b>"""
                                #    sayerr(msg)
                                #    say_warning(msg)
                        say_time()
                        msg="""<b>3D model new position pulled from kicad board!</b><br><br>"""
                        msg+="<b>file loaded from<br>"+fpath+"</b><br><br>"
                        msgr="3D model new position pulled from kicad board!\n"
                        say(msgr)
                        say_info(msg)
                        if origin_warn:
                            if aux_orig == 1:
                                origin_msg='AuxOrigin'
                            elif grid_orig == 1:
                                origin_msg='GridOrigin'
                            msg = origin_msg +' is set in FC Preferences but not set in KiCAD pcbnew file'
                            sayw(msg)
                            msg="""<b><font color='red'>"""+origin_msg+""" is set in FreeCAD Preferences<br>but not set in KiCAD pcbnew file</font></b>"""
                            msg+="""<br><br>Please assign """+origin_msg+""" to your KiCAD pcbnew board file"""
                            msg+="""<br>for a better Mechanical integration"""
                            say_warning(msg)
                    else:
                        msg="""To update 3D model Position(s) from <b>an EXISTING KiCad pcb file</b><br>the KiCAD pcbnew board file must have assigned \'Grid Origin\' or<br>\'Aux Origin\' (Drill and Place offset)!"""
                        msg+="""<br>Moreover in FC StepUP preferences you must have<br>\'PCB Settings\'->\'PCB Placement\'<br>set to \'Grid Origin\' or \'Aux Origin\'"""
                        say_warning(msg)
                        msg="To update 3D model Position(s) from an EXISTING KiCad pcb file\nthe KiCAD pcbnew board file must have assigned \'Grid Origin\' or \'Aux Origin\' (Drill and Place offset)!"
                        msg+="\nMoreover in FC StepUP preferences you must have \n\'PCB Settings\'->\'PCB Placement\'\nset to \'Grid Origin\' or \'Aux Origin\'"
                        sayerr(msg)
                else:
                    msg="""Load from <b>an EXISTING KiCad pcb file</b> to update your 3D model position!"""
                    say_warning(msg)
                    msg="Load from an EXISTING KiCad pcb file to update your 3D model position!"
                    sayerr(msg)
            else:
                msg="""Operation aborted!"""
                sayerr(msg)
                say_info(msg)
        else:
            msg="""select only 3D model(s) to be updated/pulled from kicad board!<br><b>a Time Stamp is required!</b>"""
            sayerr(msg)
            say_warning(msg)

##

def PushFootprint():
#def onExport3DStep(self):
    global last_3d_path, start_time, load_sketch, last_pcb_path
    #say("export3DSTEP")
    if load_sketch==False:
        msg="""<b>Edge editing NOT supported on FC0.15!</b><br>please upgrade your FC release"""
        say_warning(msg)
        msg="Edge editing NOT supported on FC0.15!"
        sayerr(msg)            
    #if 0:
    #if FreeCAD.ActiveDocument is None:
    #    FreeCAD.newDocument("PCB_Sketch")
    #    PCB_Sketch= FreeCAD.activeDocument().addObject('Sketcher::SketchObject','PCB_Sketch')
    #    offset=[0.0,0.0] #offset=[148.5,98.5]
    #    FreeCAD.activeDocument().PCB_Sketch.Placement = FreeCAD.Placement(FreeCAD.Vector(offset[0],offset[1]),FreeCAD.Rotation(0.000000,0.000000,0.000000,1.000000))
    #    FreeCAD.getDocument('PCB_Sketch').recompute()
    #    FreeCADGui.SendMsgToActiveView("ViewFit")
    else:
        sel = FreeCADGui.Selection.getSelection()
        if len (sel) >= 1:
            #sayw(doc.Name)
            to_discretize=False;sk_to_discr=[];sk_temp=[];sk_to_convert=[];sk_to_reselect=[]
            fp_label=u''
            #annular=0.125
            if "Sketch" in sel[0].TypeId or "Group" in sel[0].TypeId:
                if "Group" in sel[0].TypeId:
                    #print(FreeCAD.ActiveDocument.getObject(sel[0].Name).OutList,'g.OutList')
                    #for o in FreeCAD.ActiveDocument.Objects:
                    #print((sel[0].Name))
                    fp_label=sel[0].Label.replace(' ','_')
                    for o in FreeCAD.ActiveDocument.getObject(sel[0].Name).OutList:
                        #if sel[0] in o.InList:
                        #print(o.Label)
                        if 'PTH_Drills' in o.Label:
                            centers=[];rads=[]
                            for idx,g in enumerate(o.Geometry):
                                #if 'ArcOfCircle' in str(g) and not isConstruction(g): #o.getConstruction(idx): #g.Construction:
                                if 'Circle' in str(g) and not isConstruction(g):
                                    if not (g.Center in centers and g.Radius in rads):
                                        centers.append(g.Center);rads.append(g.Radius)
                            #print(len(centers), centers)
                            if 'NPTH_Drills' not in o.Label:
                                if '_padNbr=' in o.Label:
                                    skLabel = 'Sketch_Pads_TH_SMD'+o.Label[o.Label.index('_padNbr='):]+'_tmp'
                                elif  '_padNum=' in o.Label:
                                    skLabel = 'Sketch_Pads_TH_SMD'+o.Label[o.Label.index('_padNum='):]+'_tmp'
                                else:
                                    skLabel = 'Sketch_Pads_TH_SMD_tmp'
                            else:
                                skLabel = 'Sketch_Pads_NPTH_tmp'
                            FreeCAD.ActiveDocument.addObject('Sketcher::SketchObject', skLabel)
                            skd_name=FreeCAD.ActiveDocument.ActiveObject.Name
                            FreeCAD.ActiveDocument.ActiveObject.Label = skLabel #workaround to keep '=' in Label
                            sk_temp.append(FreeCAD.ActiveDocument.ActiveObject)
                            #FreeCAD.ActiveDocument.getObject(skd_name).Placement = FreeCAD.Placement(FreeCAD.Vector(0.000000, 0.000000, 0.000000), FreeCAD.Rotation(0.000000, 0.000000, 0.000000, 1.000000))
                            #FreeCAD.ActiveDocument.getObject(skd_name).MapMode = "Deactivated"
                            #print(centers)
                            for i,c in enumerate(centers):
                                FreeCAD.ActiveDocument.getObject(skd_name).addGeometry(Part.Circle(FreeCAD.Vector(c[0], c[1]), FreeCAD.Vector(0, 0, 1), rads[i]))
                                if 'Pads_NPTH' not in FreeCAD.ActiveDocument.getObject(skd_name).Label:
                                    FreeCAD.ActiveDocument.getObject(skd_name).addGeometry(Part.Circle(FreeCAD.Vector(c[0], c[1]), FreeCAD.Vector(0, 0, 1), rads[i]*1.4)) # annular = 40% of radius
                            FreeCAD.ActiveDocument.recompute()
                            FreeCADGui.Selection.addSelection(FreeCAD.ActiveDocument.getObject(skd_name))
                            sk_to_convert.append(FreeCAD.ActiveDocument.getObject(skd_name))
                            sk_to_reselect.append(o)
                        if 'F_Silks' in o.Label or 'F_Fab' in o.Label or 'F_CrtYd' in o.Label \
                            or 'Pads_TH' in o.Label or 'Pads_NPTH' in o.Label or 'Edge_Cuts' in o.Label\
                            or 'Pads_Round_Rect' in o.Label or 'FZ_' in o.Label\
                            or 'Pads_Geom' in o.Label:
                            #or 'Pads_Round_Rect' in o.Label or 'Pads_Poly' in o.Label or 'NetTie_Poly' in o.Label or 'FZ_' in o.Label\
                            #print('adding selection ',o.Label)
                            FreeCADGui.Selection.addSelection(FreeCAD.ActiveDocument.getObject(o.Name))
                            sk_to_convert.append(o)
                            #print(o.Label,'sk added')
                        if hasattr(o,"LabelText"):
                            sayerr(o.LabelText)
                            if 'Ref' in o.Label or 'Val' in o.Label:
                                FreeCADGui.Selection.addSelection(FreeCAD.ActiveDocument.getObject(o.Name))
                                sk_to_convert.append(o)
                        ## checking Pads_Poly for ArcOfCircle to be discretized
                        to_discretize=False
                        if 'NetTie_Poly' in o.Label: 
                            if hasattr(o,"Geometry"):
                                for g in o.Geometry:
                                    if 'ArcOfCircle' in str(g) and not isConstruction(g):
                                        FreeCAD.Console.PrintWarning('need to discretize Arcs\n')
                                        to_discretize=True
                                if to_discretize:
                                    sk_to_discr.append(o)
                                    FreeCADGui.Selection.removeSelection(o)
                                else:
                                    #print(o.Label,'sk added')
                                    sk_to_convert.append(o)
                        to_discretize=False
                        if 'Pads_Poly' in o.Label: 
                            if hasattr(o,"Geometry"):
                                for g in o.Geometry:
                                    if 'ArcOfCircle' in str(g) and not isConstruction(g):
                                        FreeCAD.Console.PrintWarning('need to discretize Arcs\n')
                                        to_discretize=True
                                if to_discretize:
                                    sk_to_discr.append(o)
                                    FreeCADGui.Selection.removeSelection(o)
                                else:
                                    #print(o.Label,'sk added')
                                    sk_to_convert.append(o)
                else:
                    for o in sel:
                        to_discretize=False
                        if 'PTH_Drills' in o.Label:
                            #o= sel[0]
                            centers=[];rads=[]
                            for idx,g in enumerate(o.Geometry):
                                if 'Circle' in str(g) and not isConstruction(g):
                                    if not (g.Center in centers and g.Radius in rads):
                                        centers.append(g.Center);rads.append(g.Radius)
                            #print(len(centers), centers)
                            if 'NPTH_Drills' not in o.Label:
                                if '_padNbr=' in o.Label:
                                    skLabel = 'Sketch_Pads_TH_SMD'+o.Label[o.Label.index('_padNbr='):]+'_tmp'
                                elif  '_padNum=' in o.Label:
                                    skLabel = 'Sketch_Pads_TH_SMD'+o.Label[o.Label.index('_padNum='):]+'_tmp'
                                else:
                                    skLabel = 'Sketch_Pads_TH_SMD_tmp'
                            else:
                                skLabel = 'Sketch_Pads_NPTH_tmp'
                            FreeCAD.ActiveDocument.addObject('Sketcher::SketchObject', skLabel)
                            skd_name=FreeCAD.ActiveDocument.ActiveObject.Name
                            FreeCAD.ActiveDocument.ActiveObject.Label = skLabel #workaround to keep '=' in Label
                            sk_temp.append(FreeCAD.ActiveDocument.ActiveObject)
                            #FreeCAD.ActiveDocument.getObject(skd_name).Placement = FreeCAD.Placement(FreeCAD.Vector(0.000000, 0.000000, 0.000000), FreeCAD.Rotation(0.000000, 0.000000, 0.000000, 1.000000))
                            #FreeCAD.ActiveDocument.getObject(skd_name).MapMode = "Deactivated"
                            for i,c in enumerate(centers):
                                FreeCAD.ActiveDocument.getObject(skd_name).addGeometry(Part.Circle(FreeCAD.Vector(c[0], c[1]), FreeCAD.Vector(0, 0, 1), rads[i]))
                                if 'NPTH_Drills' not in o.Label:
                                    FreeCAD.ActiveDocument.getObject(skd_name).addGeometry(Part.Circle(FreeCAD.Vector(c[0], c[1]), FreeCAD.Vector(0, 0, 1), rads[i]*1.4)) # annular = 40% of radius # +annular))
                            FreeCAD.ActiveDocument.recompute()
                        elif 'NetTie_Poly' in o.Label: 
                            for g in sel[0].Geometry:
                                if 'ArcOfCircle' in str(g):
                                    FreeCAD.Console.PrintWarning('need to discretize Arcs\n')
                                    to_discretize=True
                            if to_discretize:
                                sk_to_discr.append(o)
                                FreeCADGui.Selection.removeSelection(o)
                            else:
                                #print(o.Label,'sk added')
                                sk_to_convert.append(o)
                        elif 'Pads_Poly' in o.Label: 
                            to_discretize=False
                            for g in o.Geometry:
                                if 'ArcOfCircle' in str(g):
                                    FreeCAD.Console.PrintWarning('need to discretize Arcs\n')
                                    to_discretize=True
                            if to_discretize:
                                sk_to_discr.append(o)
                                FreeCADGui.Selection.removeSelection(o)
                            else:
                                print(o.Label,'sk added')
                                sk_to_convert.append(o)
                for sk in sk_to_discr:
                    ws=sk.Shape.copy()
                    #Part.show(ws)    
                    wn=[]
                    q_deflection = 0.005 #0.02 ##0.005
                    wnc=[]
                    for e in ws.Edges:
                        if hasattr(e.Curve,'Radius'):
                            if not e.Closed:  # Arc and not Circle
                                wn.append(Part.makePolygon(e.discretize(QuasiDeflection=q_deflection)))
                            else:
                                #wn.append(Part.Wire(e))
                                wnc.append(Part.Wire(e))
                                sayw('added circle pad')
                        else:
                            wn.append(Part.Wire(e))
                    #sk_d=Draft.makeSketch(wn)
                    edgs=[]
                    for s in wn:
                        for e in s.Edges:
                            edgs.append(e)
                    wns = Part.Wire(Part.__sortEdges__(edgs))
                    #Part.show(wnc[0])
                    #print (wns);print(wnc[0])
                    sk_d=Draft.makeSketch([wns,wnc[0]], autoconstraints=True)
                    Connect = sk_d
                    
                    # for e in ws.Edges:
                    #     if hasattr(e.Curve,'Radius'):
                    #         if not e.Closed:  # Arc and not Circle
                    #             #print(e.discretize(QuasiDeflection=q_deflection))
                    #             sh=Part.makePolygon(e.discretize(QuasiDeflection=q_deflection))
                    #             for ed in sh.Edges:
                    #                 wn.append(ed)
                    #             #Part.show(sh)
                    #             sayw('added discretized polygon')
                    #         else:
                    #             #wn.append(Part.Wire(e))
                    #             wnc.append(Part.Wire(e))
                    #             sayw('added circle pad')
                    #     else:
                    #         wn.append(Part.Wire(e))
                    # #sk_d=Draft.makeSketch(wn)
                    # edgs=[]
                    # for s in wn:
                    #     for e in s.Edges:
                    #         edgs.append(e)
                    #         #print (e,e.TypeId)
                    # #wns = Part.Wire(Part.__sortEdges__(edgs))
                    
                    #lines = []
                    #points = []
                    #p_coords = []
                    #for wire in wn:
                    #    #points = []
                    #    for vert in wire.Vertexes:
                    #        points.append(vert.Point)
                    #        p_coords.append((vert.Point.x,vert.Point.y))
                    #print(points)
                    #print(p_coords)
                    # p=p_coords
                    # import functools
                    # import math
                    # center = functools.reduce(lambda a, b: (a[0] + b[0], a[1] + b[1]), p, (0, 0))
                    # center = (center[0] / len(p), (center[1] / len(p)))
                    # p.sort(key = lambda a: math.atan2(a[1] - center[1], a[0] - center[0]))
                    # contour=p
                    # #print(p)
                    # #print(sort_to_form_plist(p_coords))
                    # #stop
                    # #import numpy as np
                    # #vstack_ = np.vstack(p_coords)
                    # ##print(vstack_)
                    # ##contours = np.vstack(p_coords).squeeze()
                    # #contours = np.vstack(points).squeeze()
                    # ##contours= [ np.array(contours) ]
                    # #print(contours)
                    # v_contour=[]
                    # #for p in contours:
                    # #    print(Base.Vector(p[0],p[1],p[2]))
                    # #    v_contour.append(Base.Vector(p[0],p[1],p[2]))
                    # for p in contour:
                    #     print(Base.Vector(p[0],p[1],0.0))
                    #     v_contour.append(Base.Vector(p[0],p[1],0.0))
                    # sh1 = Part.makePolygon(v_contour)
                    # Part.show(sh1)
                    # stop

                    ## if len (wnc)>0:
                    ##     edgs.append(wnc[0].Edges[0])
                    ## sk_d=Draft.makeSketch(edgs, autoconstraints=True)
                    
                    ## FreeCAD.ActiveDocument.recompute()
                    ### creating an edge ordered sketch
                    del_sk_d = True
                    if 0:
                        try:
                            ### Begin command Part_CompJoinFeatures
                            say('importing BOPTools')
                            import PartGui
                            # from PartGui import BOPTools
                            import BOPTools
                            import BOPTools.JoinFeatures
                            say('trying makeConnect')
                            j = BOPTools.JoinFeatures.makeConnect(name='Connect')
                            j.Objects = [sk_d]
                            j.Proxy.execute(j)
                            j.purgeTouched()
                            for obj in j.ViewObject.Proxy.claimChildren():
                                obj.ViewObject.hide()
                            ### End command Part_CompJoinFeatures
                            say('makeConnect done')
                            Connect = FreeCAD.ActiveDocument.ActiveObject
                        except:
                            sayw('failed makeConnect')
                            FreeCAD.ActiveDocument.removeObject(FreeCAD.ActiveDocument.ActiveObject.Name)
                            Connect = sk_d
                            del_sk_d = False
                    sv0 = Draft.makeShape2DView(FreeCAD.ActiveDocument.getObject(Connect.Name), FreeCAD.Vector(-0.0, -0.0, 1.0))
                    FreeCAD.ActiveDocument.recompute()
                    FreeCAD.ActiveDocument.removeObject(Connect.Name)
                    if 0: #del_sk_d:
                        FreeCAD.ActiveDocument.removeObject(sk_d.Name)
                    #FreeCADGui.Selection.clearSelection()
                    #FreeCADGui.Selection.addSelection(FreeCAD.ActiveDocument.Name,sv0.Name)
                    sk_d = Draft.makeSketch(FreeCAD.ActiveDocument.getObject(sv0.Name), autoconstraints=True)
                    FreeCAD.ActiveDocument.removeObject(sv0.Name)
                    FreeCAD.ActiveDocument.recompute()
                    #stop
                    #ws=sk_d.Shape.copy()
                    #sk_do = Draft.makeSketch(ws)
                    #Part.makePolygon(ws.Edges)
                    #FreeCAD.ActiveDocument.removeObject(sk_d.Name)
                    sk_d.Label=sk.Label+'_'
                    FreeCADGui.Selection.addSelection(sk_d)
                    sk_to_convert.append(sk_d)
                    sk_temp.append(sk_d)
                #stop
                FreeCAD.ActiveDocument.recompute()
                #stop
                #if "Group" in sel[0].TypeId:
                #    for o in FreeCAD.ActiveDocument.Objects:
                #        FreeCADGui.Selection.addSelection(o)
                cfg_read_all()
                pg = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/kicadStepUp")
                last_fp_path = pg.GetString("last_fp_path")
                if len(last_fp_path) == 0:
                    last_fp_path=last_pcb_path
                    #sayw(last_pcb_path)
                #getSaveFileName(self,"saveFlle","Result.txt",filter ="txt (*.txt *.)")
                testing=False #False
                for s in sk_to_convert:
                    FreeCADGui.Selection.addSelection(s)
                    #print(s.Label,'added')
                for s in sk_to_discr:
                    FreeCADGui.Selection.removeSelection(s)
                if not testing:
                    Filter=""
                    name, Filter = PySide.QtGui.QFileDialog.getSaveFileName(None, "Push Footprint to KiCad module ...",
                        make_unicode(last_fp_path), "*.kicad_mod")
                else:
                    if os.path.isdir("d:/Temp/"):
                        name='d:/Temp/ex2.kicad_mod'
                    elif os.path.isdir("c:/Temp/"):
                        name='c:/Temp/ex2.kicad_mod'                        
                #say(name)
                if name:
                    #if os.path.exists(name):
                    last_fp_path=os.path.dirname(name)
                    pg = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/kicadStepUp")
                    pg.SetString("last_fp_path", make_string(last_fp_path)) # py3 .decode("utf-8")
                    start_time=current_milli_time()
                    if not name.endswith('.kicad_mod'):
                        name=name+u'.kicad_mod'
                    export_footprint(name,fp_label)
                    for s in sk_to_discr:
                        FreeCADGui.Selection.addSelection(s)
                    for s in sk_to_reselect:
                        FreeCADGui.Selection.addSelection(s)
                    #stop
                if not testing:
                    for s in sk_temp:
                        FreeCAD.ActiveDocument.removeObject(s.Name)
                    #else:
                    #    msg="""Save to <b>an EXISTING KiCad pcb file</b> to update your Edge!"""
                    #    say_warning(msg)
                    #    msg="Save to an EXISTING KiCad pcb file to update your Edge!"
                    #    sayerr(msg)
            else:
                msg="""Select Group or Sketch/Text elements to be converted to KiCad Footprint!"""
                sayerr(msg)
                say_warning(msg)
        else:
            msg="""Select Group or Sketch/Text elements to be converted to KiCad Footprint!"""
            sayerr(msg)
            say_warning(msg)
###

def simplify_sketch_old():
    ''' simplifying & sanitizing sketches '''
    global maxRadius, edge_tolerance
    
    doc = FreeCAD.ActiveDocument
    sel = FreeCADGui.Selection.getSelection()
    if len(sel)==1:
        if 'Sketcher' in sel[0].TypeId:
            sanitizeSketch(sel[0].Name)
        new_edge_list, not_supported, to_discretize, construction_geom = getBoardOutline()
        ## support for arcs, lines and bsplines in F_Silks
        sel = FreeCADGui.Selection.getSelection()
        sk_name=None
        sk_name=sel[0].Name
        sk_label=sel[0].Label
        if len(to_discretize)>0 and sk_name is not None:
            FreeCADGui.ActiveDocument.getObject(sk_name).Visibility=False # hidden Sketch
            #sel = FreeCADGui.Selection.getSelection()
            #for s in sel:
            #    if 'F_Silks' in s.Label:
            #        sk_name=s.Name
            #if len (sel)==1:
                #sk_name=sel[0].Name
            t_name=cpy_sketch(sk_name)
            ###t_sk=FreeCAD.ActiveDocument.copyObject(FreeCAD.ActiveDocument.getObject(sk_name))
            elist, to_dis=check_geom(t_name)
            #Draft.clone(FreeCAD.ActiveDocument.getObject(sk_name),copy=True)
            #clone_name=App.ActiveDocument.ActiveObject.Name
            geoBasic=[]
            geoBasic=split_basic_geom(t_name, to_dis)
            #print geoBasic
            #remove_basic_geom(t_name, to_dis)
            ## remove_basic_geom(t_name, to_dis)
            ##remove_basic_geom(t_sk.Name, to_discretize)
            ##elist, to_dis=check_geom(t_sk.Name)
            #print elist
            #stop
            obj_list_prev=[]
            for obj in doc.Objects:
                #print obj.TypeId
                if (obj.TypeId=="Part::Feature") or (obj.TypeId=="Sketcher::SketchObject"):
                    obj_list_prev.append(obj.Name)
            #Draft.draftify(FreeCAD.ActiveDocument.getObject(t_name),delete=True)
            #Draft.draftify(FreeCAD.ActiveDocument.getObject(t_name),delete=False)
            b=FreeCAD.ActiveDocument.getObject(t_name)
            shp1=b.Shape.copy()
            Part.show(shp1)
            FreeCAD.ActiveDocument.removeObject(t_name)
            FreeCAD.ActiveDocument.recompute()
            #stop
            obj_list_after=[]
            for obj in doc.Objects:
                if (obj.TypeId=="Part::Feature") or (obj.TypeId=="Sketcher::SketchObject")\
                   or (obj.TypeId=="Part::Part2DObjectPython"):
                    if obj.Name not in obj_list_prev:
                        obj_list_after.append(obj.Name)
            #print obj_list_after #, obj_list_prev
            sk_to_conv=[]
            for obj in doc.Objects:
                if obj.Name in obj_list_after:
                    if (obj.TypeId=="Part::Part2DObjectPython"):
                        FreeCAD.ActiveDocument.removeObject(obj.Name)
                        FreeCAD.ActiveDocument.recompute() 
                    else:
                       sk_to_conv.append(obj.Name)
            keep_sketch_converted=True #False
            for s in sk_to_conv:
                #sayerr(s) ## 
                ns=Discretize(s)
                for g in geoBasic:
                    FreeCAD.ActiveDocument.getObject(ns).addGeometry(g)
                offset1=[-FreeCAD.ActiveDocument.getObject(sk_name).Placement.Base[0],-FreeCAD.ActiveDocument.getObject(sk_name).Placement.Base[1]]
                elist, to_dis=check_geom(ns,offset1)
                for e in elist:
                    #print e[(len(e)-1):][0]
                    e[(len(e)-1)]=sk_label
                    #print e[(len(e)-1):][0]
                #stop
                new_edge_list=new_edge_list+elist
                if not keep_sketch_converted:
                    FreeCAD.ActiveDocument.removeObject(ns)
                else:
                    FreeCAD.ActiveDocument.getObject(ns).Label=sel[0].Label+'_simplified'
                FreeCAD.ActiveDocument.recompute()
            #############  end discretizing
        else:
            sayw('nothing to simplify')
        # to do: evaluate sanitize check
        ####stop

###
def simplify_sketch():
    ''' simplifying & sanitizing sketches '''
    global maxRadius, edge_tolerance, precision
    
    doc = FreeCAD.ActiveDocument
    sel = FreeCADGui.Selection.getSelection()
    if len(sel)==1:
        if 'Sketcher' in sel[0].TypeId:
            sanitizeSketch(sel[0].Name)
        # new_edge_list, not_supported, to_discretize, construction_geom = getBoardOutline()
        to_discretize = []
        new_edge_list = []
        if hasattr(sel[0],'GeometryFacadeList'):
            Gm = sel[0].GeometryFacadeList
            for g in Gm:
                if 'BSplineCurve object' in str(g.Geometry):
                    to_discretize.append(g.Geometry)
                elif 'Ellipse' in str(g.Geometry) or 'Parabola' in str(g.Geometry) or 'Hyperbola' in str(g.Geometry):
                    to_discretize.append(g.Geometry)
                else:
                    if not isConstruction(g): #g.Construction: # adding only non construction geo
                        new_edge_list.append(g.Geometry)
        else:
            Gm = sel[0].Geometry
            for g in Gm:
                if 'BSplineCurve object' in str(g):
                    to_discretize.append(g)
                elif 'Ellipse' in str(g) or 'Parabola' in str(g) or 'Hyperbola' in str(g):
                    to_discretize.append(g)
                else:
                    if not isConstruction(g): #g.Construction: # adding only non construction geo
                        new_edge_list.append(g)
        #for g in sel[0].Geometry:
        ## support for arcs, lines and bsplines in F_Silks
        sel = FreeCADGui.Selection.getSelection()
        sk_name=None
        sk_name=sel[0].Name
        sk_label=sel[0].Label
        
        if len(to_discretize)>0 and sk_name is not None:
            FreeCADGui.ActiveDocument.getObject(sk_name).Visibility=False # hidden Sketch
            #sel = FreeCADGui.Selection.getSelection()
            #for s in sel:
            #    if 'F_Silks' in s.Label:
            #        sk_name=s.Name
            #if len (sel)==1:
                #sk_name=sel[0].Name
            for g in to_discretize:
                if 'Ellipse' in str(g) or 'BSpline' in str(g) or 'Hyperbol' in str(g) or 'Parabol' in str(g):
                    bs = g.toBSpline() # (tolerance, maxSegments, maxDegree)
                    gds = bs.toBiArcs(precision)
                    for gd in gds:
                        new_edge_list.append(gd)
            if len(new_edge_list) > 0:
                doc.addObject('Sketcher::SketchObject','sSketch')
                ssk = doc.ActiveObject
                ssk_name = doc.ActiveObject.Name
                ssk.Geometry = new_edge_list
                # for i,g in enumerate (new_edge_list):
                #     if 'BSplineCurve object' in str(g):
                #         ssk.exposeInternalGeometry(i)
                doc.recompute()
                ssk.Label = sk_label + u'_simplified'
            
            # t_name=cpy_sketch(sk_name)
            # ###t_sk=FreeCAD.ActiveDocument.copyObject(FreeCAD.ActiveDocument.getObject(sk_name))
            # elist, to_dis=check_geom(t_name)
            # #Draft.clone(FreeCAD.ActiveDocument.getObject(sk_name),copy=True)
            # #clone_name=App.ActiveDocument.ActiveObject.Name
            # geoBasic=[]
            # geoBasic=split_basic_geom(t_name, to_dis)
            # #remove_basic_geom(t_name, to_dis)
            # ## remove_basic_geom(t_name, to_dis)
            # ##remove_basic_geom(t_sk.Name, to_discretize)
            # ##elist, to_dis=check_geom(t_sk.Name)
            # #print elist
            # #stop
            # obj_list_prev=[]
            # for obj in doc.Objects:
            #     #print obj.TypeId
            #     if (obj.TypeId=="Part::Feature") or (obj.TypeId=="Sketcher::SketchObject"):
            #         obj_list_prev.append(obj.Name)
            # #Draft.draftify(FreeCAD.ActiveDocument.getObject(t_name),delete=True)
            # #Draft.draftify(FreeCAD.ActiveDocument.getObject(t_name),delete=False)
            # b=FreeCAD.ActiveDocument.getObject(t_name)
            # shp1=b.Shape.copy()
            # Part.show(shp1)
            # #stop
            # FreeCAD.ActiveDocument.removeObject(t_name)
            # FreeCAD.ActiveDocument.recompute()
            # #stop
            # obj_list_after=[]
            # for obj in doc.Objects:
            #     if (obj.TypeId=="Part::Feature") or (obj.TypeId=="Sketcher::SketchObject")\
            #        or (obj.TypeId=="Part::Part2DObjectPython"):
            #         if obj.Name not in obj_list_prev:
            #             obj_list_after.append(obj.Name)
            # #print obj_list_after #, obj_list_prev
            # sk_to_conv=[]
            # for obj in doc.Objects:
            #     if obj.Name in obj_list_after:
            #         if (obj.TypeId=="Part::Part2DObjectPython"):
            #             FreeCAD.ActiveDocument.removeObject(obj.Name)
            #             FreeCAD.ActiveDocument.recompute() 
            #         else:
            #            sk_to_conv.append(obj.Name)
            # keep_sketch_converted=True #False
            # for s in sk_to_conv:
            #     #sayerr(s) ## 
            #     ns=Discretize(s)
            #     for g in geoBasic:
            #         FreeCAD.ActiveDocument.getObject(ns).addGeometry(g)
            #     offset1=[-FreeCAD.ActiveDocument.getObject(sk_name).Placement.Base[0],-FreeCAD.ActiveDocument.getObject(sk_name).Placement.Base[1]]
            #     elist, to_dis=check_geom(ns,offset1)
            #     for e in elist:
            #         #print e[(len(e)-1):][0]
            #         e[(len(e)-1)]=sk_label
            #         #print e[(len(e)-1):][0]
            #     #stop
            #     new_edge_list=new_edge_list+elist
            #     if not keep_sketch_converted:
            #         FreeCAD.ActiveDocument.removeObject(ns)
            #     else:
            #         FreeCAD.ActiveDocument.getObject(ns).Label=sel[0].Label+'_simplified'
            #     FreeCAD.ActiveDocument.recompute()
            #############  end discretizing
        else:
            sayw('nothing to simplify')
        # to do: evaluate sanitize check
        ####stop

###

def normalize_bsplines():
    ''' simplifying & sanitizing sketches '''
    global edge_tolerance, maxRadius, maxSegments, precision
    
    doc = FreeCAD.ActiveDocument
    docG = FreeCADGui.ActiveDocument
    sel = FreeCADGui.Selection.getSelection()
    if len(sel)==1:
        if 'Sketcher' in sel[0].TypeId:
            skGeo = sel[0].Geometry
            found_to_simplify = False
            kGeo = []
            #print(skGeo)
            maxDegree = 3 #kicad max degree of splines
            for g in skGeo:
                #if 'BSplineCurve object' in str(g):
                #    bs = g
                #    # Set degree
                #    #maxDegree = 3 #kicad max degree of splines
                #    if bs.Degree < maxDegree:
                #        bs.increaseDegree(maxDegree)
                #    elif bs.Degree > maxDegree:
                #        # degree too high. We need to approximate the curve
                #        bs = bs.approximateBSpline(edge_tolerance,maxSegment,maxDegree) # (tolerance, maxSegments, maxDegree)
                #        # Generate to a list of bezier curves
                #  import kicadStepUptools; import importlib; importlib.reload(kicadStepUptools)
                if 'Ellipse' in str(g) or 'Parabola' in str(g) or 'Hyperbola' in str(g):
                    # bs = g.approximateBSpline(edge_tolerance,maxSegments,maxDegree) # (tolerance, maxSegments, maxDegree) 
                    bs = g.toBSpline() # (tolerance, maxSegments, maxDegree)
                    bs = bs.toBiArcs(precision)
                    for b in bs:
                        kGeo.append(b)
                    found_to_simplify = True
                    #print(bs)
                    #stop
                else: #std geo like line, arcs, circles
                    bs = g
                    kGeo.append(bs)
            if found_to_simplify:
                doc.addObject('Sketcher::SketchObject','kBspSketch')
                kbsp = doc.ActiveObject
                kbsp_name = doc.ActiveObject.Name
                kbsp.Geometry = kGeo
                for i,g in enumerate (kGeo):
                    if 'BSplineCurve object' in str(g):
                        kbsp.exposeInternalGeometry(i)
                doc.recompute()
                docG.getObject(sel[0].Name).Visibility = False
                        # bezier_list = bs.toBezier()
                        # # Check the result
                        # for bc in bezier_list:
                        #     print("%s (degree : %d / nb poles : %d)"%(bc, bc.Degree, bc.NbPoles))
                        #     print(bc, bc.Degree, bc.NbPoles)
                        #     Part.show(bc.toShape())
                        #     Draft.makeSketch(FreeCAD.ActiveDocument.ActiveObject,autoconstraints=True)
                            # if not keep_sketch_converted:
                            #     FreeCAD.ActiveDocument.removeObject(ns)
                            # else:
                                #     FreeCAD.ActiveDocument.getObject(ns).Label=sel[0].Label+'_simplified'
                                # FreeCAD.ActiveDocument.recompute()
                                    #############  end discretizing
            else:
                sayw('nothing to simplify')
        else:
            sayw('nothing to simplify')
        # to do: evaluate sanitize check
        ####stop

###

###
def export_footprint(fname=None,flabel=None):
    global last_fp_path, test_flag, start_time
    global configParser, configFilePath, start_time
    global ignore_utf8, ignore_utf8_incfg, disable_PoM_Observer
    global board_base_point_x, board_base_point_y, real_board_pos_x, real_board_pos_y
    global pcb_path, use_AppPart, force_oldGroups, use_Links, use_LinkGroups
    global original_filename
    global off_x, off_y, maxRadius, pad_nbr
    
    sayw('exporting new footprint')
    doc=FreeCAD.ActiveDocument
    #print fname
    if fname is None:
        sayerr('missing fp file name') 
        stop
    #    fpath=original_filename
    else:
        fpath=fname
    
    sayerr('saving to '+fpath)
    #stop
    
    if len(fpath) > 0:
        #new_edge_list=getBoardOutline()
        #say (new_edge_list)
        cfg_read_all()
        path, fname = os.path.split(fpath)
        name=os.path.splitext(fname)[0]
        ext=os.path.splitext(fname)[1]
        fpth = os.path.dirname(os.path.abspath(fpath))
        #filePath = os.path.split(os.path.realpath(__file__))[0]
        #say ('my file path '+fpath)
        # stop
        if fpth == "":
            fpth = "."
        last_fp_path = fpth
        last_fp_path = re.sub("\\\\", "/", last_fp_path)
        ini_vars[11] = last_fp_path
        #cfg_update_all()
        pg = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/kicadStepUp")
        pg.SetString("last_fp_path", make_string(last_fp_path))
        #sayerr(name+':'+ext)
        new_edge_list, not_supported, to_discretize, construction_geom = getBoardOutline()
        #print (new_edge_list, to_discretize)
        #stop
        
        ## support for arcs, lines and bsplines in F_Silks
        sel = FreeCADGui.Selection.getSelection()
        sk_name=None
        NetTie_present = False
        fp_name='fc_footprint'
        if flabel == '' or flabel is None:
            fp_name = FreeCAD.ActiveDocument.Name
        else:
            fp_name = flabel
        #print(fp_name, 'fp_name1')
        
        for s in sel:
            if 'F_Silks' in s.Label:
                sk_name=s.Name
                sk_label=s.Label
            if 'NetTie' in s.Label:
                NetTie_present = True

        if len(to_discretize)>0 and sk_name is not None:
            #sel = FreeCADGui.Selection.getSelection()
            #for s in sel:
            #    if 'F_Silks' in s.Label:
            #        sk_name=s.Name
            #if len (sel)==1:
                #sk_name=sel[0].Name
            t_name=cpy_sketch(sk_name)
            ###t_sk=FreeCAD.ActiveDocument.copyObject(FreeCAD.ActiveDocument.getObject(sk_name))
            elist, to_dis=check_geom(t_name)
            #Draft.clone(FreeCAD.ActiveDocument.getObject(sk_name),copy=True)
            #clone_name=App.ActiveDocument.ActiveObject.Name
            remove_basic_geom(t_name, to_dis)
            ##remove_basic_geom(t_sk.Name, to_discretize)
            ##elist, to_dis=check_geom(t_sk.Name)
            #print elist
            #stop
            obj_list_prev=[]
            for obj in doc.Objects:
                #print obj.TypeId
                if (obj.TypeId=="Part::Feature") or (obj.TypeId=="Sketcher::SketchObject"):
                    obj_list_prev.append(obj.Name)
            #Draft.draftify(FreeCAD.ActiveDocument.getObject(t_name),delete=True)
            #Draft.draftify(FreeCAD.ActiveDocument.getObject(t_name),delete=False)
            b=FreeCAD.ActiveDocument.getObject(t_name)
            shp1=b.Shape.copy()
            Part.show(shp1)
            FreeCAD.ActiveDocument.removeObject(t_name)
            FreeCAD.ActiveDocument.recompute()
            #stop
            obj_list_after=[]
            for obj in doc.Objects:
                if (obj.TypeId=="Part::Feature") or (obj.TypeId=="Sketcher::SketchObject")\
                   or (obj.TypeId=="Part::Part2DObjectPython"):
                    if obj.Name not in obj_list_prev:
                        obj_list_after.append(obj.Name)
            #print obj_list_after #, obj_list_prev
            sk_to_conv=[]
            for obj in doc.Objects:
                if obj.Name in obj_list_after:
                    if (obj.TypeId=="Part::Part2DObjectPython"):
                        FreeCAD.ActiveDocument.removeObject(obj.Name)
                        FreeCAD.ActiveDocument.recompute() 
                    elif (obj.TypeId=="Sketcher::SketchObject"):
                       sk_to_conv.append(obj.Name)
            keep_sketch_converted=False #False
            for s in sk_to_conv:
                #sayerr(s) ## 
                ns=Discretize(s)
                offset1=[-FreeCAD.ActiveDocument.getObject(sk_name).Placement.Base[0],-FreeCAD.ActiveDocument.getObject(sk_name).Placement.Base[1]]
                elist, to_dis=check_geom(ns,offset1)
                for e in elist:
                    #print e[(len(e)-1):][0]
                    e[(len(e)-1)]=sk_label
                    #print e[(len(e)-1):][0]
                #stop
                new_edge_list=new_edge_list+elist
                if not keep_sketch_converted:
                    FreeCAD.ActiveDocument.removeObject(ns)
                FreeCAD.ActiveDocument.recompute()
            #############  end discretizing
  
        new_border=u''
        #print (new_edge_list)
        #stop
        ## maxRadius # 4000 = 4m max length for KiCad
        #edge_nbr=0
        sanitized_edge_list=[]
        for border in new_edge_list:
            #print border # [0]
            if 'arc' in border[0]:
                #print border[0]
                if abs(float(border[3])) > maxRadius:
                    #print 'too big radius= ',border[3]
                    #print 'border len= ', len(border)
                    #points=border [10].x
                    p1x = float("{0:.6f}".format(border [10].x));p1y=float("{0:.6f}".format(border [10].y))
                    #print p1x, ' ',p1y
                    p2x = float("{0:.6f}".format(border [11].x));p2y=float("{0:.6f}".format(border [11].y))
                    #print '1st point ', border [10],' 2nd point ', border [11]
                    sanitized_edge_list.append(['line',p1x,p1y,p2x,p2y,border[13]])
                else:
                    sanitized_edge_list.append(border)
            else:
                sanitized_edge_list.append(border)
            #edge_nbr=edge_nbr+1
        # print '------------------'
        #print (sanitized_edge_list)
        ####stop
        #for border in new_edge_list:
        reference=u"FC_"; value=u"Val_"; 
        xr= 0.0; yr=1.0;xv= 0.0; yv=-1.0
        #sel = FreeCADGui.Selection.getSelection()
        fsize='1.0 1.0'; fthick='0.15'
        ref_fsize='1.0 1.0'; ref_fthick='0.15'
        val_fsize='1.0 1.0'; val_fthick='0.15'
        for o in FreeCAD.ActiveDocument.Objects:
        #if sel[0].TypeId =='App::DocumentObjectGroup':
            #if o.TypeId =='App::DocumentObjectGroup':
            #    fp_name=o.Label
            #    print(fp_name, 'fp_name2')
        
            #else:
            #    fp_name = FreeCAD.ActiveDocument.Name
            if o.TypeId =='App::Annotation':
                if 'Ref' in o.Label:
                    reference=o.LabelText[0]
                    xr=o.Position.x;yr=-o.Position.y
                    fsize_list = o.Label.split('_')
                    l = len (fsize_list)
                    if l > 1:
                        fs = (fsize_list[l-1].rstrip('mm')); 
                        ref_fsize=(fs+' '+fs); ref_fthick="{0:.3f}".format((float(fs)*0.15))
                    else:
                        ref_fsize='1.0 1.0'; ref_fthick='0.15'
                elif 'Val' in o.Label:
                    value=o.LabelText[0]
                    xv=o.Position.x;yv=-o.Position.y
                    fsize_list = o.Label.split('_')
                    l = len (fsize_list)
                    if l > 1:
                        fs = (fsize_list[l-1].rstrip('mm')); 
                        val_fsize=(fs+' '+fs); val_fthick="{0:.3f}".format((float(fs)*0.15))
                    else:
                        val_fsize='1.0 1.0'; val_fthick='0.15'
        offset=[0,0]
        drills=[];psmd=[];pth=[];npth=[]
        pply=[];ntply=[];prrect=[];pgeom=[];pgeomG=[]
        pads_TH_SMD=[];pads_NPTH=[]
        fzply=[];edge_thick=0.
        #edge_thick=0.15 #; lyr='F.SilkS'
        # lyr=border[len(border-1):]
        ## header=u"(module "+fp_name+" (layer F.Cu) (tedit 5A74E519)"+os.linesep
        #header=header+fp_type
        #header=header+"  (descr \""+fp_name+" StepUp generated footprint\")"+os.linesep
        # print(fp_name, 'fp_name3')
        header="  (descr \""+fp_name.replace('-fp','')+" StepUp generated footprint\")"+os.linesep
        if NetTie_present:
            header=header+"  (tags \"net tie\")"+os.linesep
            # header=header+"  (attr virtual)"
        header=header+"  (fp_text reference \""+reference+u"\" (at "+str(xr)+" "+str(yr)+") (layer F.SilkS)"+os.linesep
        header=header+"  (effects (font (size "+ref_fsize+") (thickness "+ref_fthick+")))"+os.linesep
        header=header+"  )"+os.linesep
        header=header+"  (fp_text value \""+value+u"\" (at "+str(xv)+" "+str(yv)+") (layer F.SilkS)"+os.linesep
        header=header+"    (effects (font (size "+val_fsize+") (thickness "+val_fthick+")))"+os.linesep
        #header=header+"    (effects (font (size 1.0 1.0) (thickness 0.15)))"+os.linesep
        header=header+"  )"+os.linesep
        header=header+"  (fp_text user %R (at "+str(xr)+" "+str(yr)+") (layer F.Fab)"+os.linesep
        header=header+"    (effects (font (size "+ref_fsize+") (thickness "+ref_fthick+")))"+os.linesep
        #header=header+"    (effects (font (size 1 1) (thickness 0.15)))"+os.linesep
        header=header+"  )"+os.linesep
        header=header+"  (fp_text user \"EDIT PAD NUMBERS\" (at "+str(xv)+" "+str(yv-1)+") (layer Cmts.User)"+os.linesep
        header=header+"    (effects (font (size 1 1) (thickness 0.2) italic))"+os.linesep
        header=header+"  )"

        ## import kicadStepUptools; reload(kicadStepUptools)
        for border in sanitized_edge_list:
            #print (border)
            lyr=border[(len(border)-1):][0]
            lyr_splt = lyr.split('_')
            #print(lyr)
            if 'CrtYd' in lyr and len(lyr_splt)>=3:
                edge_thick=float(lyr.split('_')[len(lyr_splt)-1])
                lyr=u'F.CrtYd'
            elif 'Silks' in lyr:
                if len(lyr_splt)>=3:
                    edge_thick=float(lyr.split('_')[len(lyr_splt)-1])
                    lyr=u'F.SilkS'
                else:
                    lyr='skip'
            elif 'Fab' in lyr:
                if len(lyr_splt)>=3:
                    edge_thick=float(lyr.split('_')[len(lyr_splt)-1])
                    lyr=u'F.Fab'
                else:
                    lyr='skip'                
            elif 'Cuts' in lyr:
                if len(lyr_splt)>=3:
                    edge_thick=float(lyr.split('_')[len(lyr_splt)-1])
                    lyr=u'Edge.Cuts'
                else:
                    lyr='skip'
            #elif 'Pads_SMD' in lyr:
            #    edge_thick=0.
            #    lyr=u'Pads_SMD'
            #    psmd.append(border)
            #elif 'Pads_TH' in lyr and not 'SMD' in lyr:
            #    edge_thick=0.
            #    lyr=u'Pads_TH'
            #    pth.append(border)
            #elif 'Drills' in lyr:
            #    edge_thick=0.
            #    lyr=u'Drills'
            #    drills.append(border)
            elif 'NPTH' in lyr:
                edge_thick=0.
                lyr=u'NPTH'
                pads_NPTH.append(border)
            elif 'Pads_Poly' in lyr:
                edge_thick=0.
                if 0: #'B_Cu' in lyr:
                    lyr=u'Pad_Poly_B_Cu'
                else:
                    lyr=u'Pad_Poly'
                pply.append(border)
            elif 'NetTie_Poly' in lyr:
                edge_thick=0.
                if 0: #'B_Cu' in lyr:
                    lyr=u'NetTie_Poly_B_Cu'
                else:
                    lyr=u'NetTie_Poly'
                ntply.append(border)
            elif 'FZ_F_Mask' in lyr:
                edge_thick=0.
                lyr=u'FZ_Mask_Poly'
                fzply.append(border)
            elif 'Pads_Round_Rect' in lyr:
                edge_thick=0.
                if 0: #'B_Cu' in lyr:
                    lyr=u'Pads_Round_Rect_B_Cu'
                else:
                    lyr=u'Pads_Round_Rect'
                prrect.append(border)
            elif 'Pads_TH' in lyr and 'SMD' in lyr:
                edge_thick=0.
                if 0: #'B_Cu' in lyr:
                    lyr=u'PadsAll_B_Cu'
                else:
                    lyr=u'PadsAll'
                pads_TH_SMD.append(border)
            elif 'Pads_Geom' in lyr:
                #edge_thick=float(lyr.split('_')[2])
                edge_thick=float(lyr.split('_')[len(lyr_splt)-1])
                #print (lyr)
                sk = FreeCAD.ActiveDocument.getObjectsByLabel(lyr)[0]
                if hasattr(sk,'GeometryFacadeList'):
                    Gm = sk.GeometryFacadeList
                    for g in Gm:
                        if isConstruction(g): # g.Construction:
                            if 'Circle' in type(g.Geometry).__name__ and not 'ArcOfCircle' in type(g.Geometry).__name__:
                                sk_ge=g.Geometry.toShape()  #needed to fix some issue on sketch geometry building
                                pgeomG.append([
                                    'circle',
                                    sk_ge.Edges[0].Curve.Radius,
                                    sk_ge.Edges[0].Curve.Center.x,
                                    sk_ge.Edges[0].Curve.Center.y,
                                    sk.Label
                                ])
                else:
                    Gm = sk.Geometry
                    for g in Gm:
                        if isConstruction(g): #g.Construction:
                            if 'Circle' in type(g).__name__ and not 'ArcOfCircle' in type(g).__name__:
                                sk_ge=g.toShape()  #needed to fix some issue on sketch geometry building
                                pgeomG.append([
                                    'circle',
                                    sk_ge.Edges[0].Curve.Radius,
                                    sk_ge.Edges[0].Curve.Center.x,
                                    sk_ge.Edges[0].Curve.Center.y,
                                    sk.Label
                                ])
                #lyr=u'Pads_Geom'
                pgeom.append(border)
                #print (pgeom);print(pgeomG)
            #sayw(prrect); sayw(pply)
            #sayw(pth)
            
            #if (lyr != 'Pads_SMD' and lyr != 'Pads_TH' and lyr != 'Drills' and lyr != 'NPTH'\
            if ('Pads_SMD' not in lyr and 'Pads_TH' not in lyr and 'Drills' not in lyr and 'NPTH' not in lyr \
                                 and 'Pad_Poly' not in lyr and 'NetTie_Poly' not in lyr and 'Pads_Round_Rect' not in lyr and 'PadsAll' not in lyr)\
                                 and 'FZ_' not in lyr and 'Pads_Geom' not in lyr and 'skip' not in lyr:
                #print border, ' BORDER'                                                  #
                #if len (border)>0:
                new_border=new_border+os.linesep+createFp(border,offset, lyr, edge_thick)
            #sayw(createEdge(border))
        #stop
        
        #pth_ordered=collect_pads(psmd) #pads_all)  ## pads normalized with sequence of segments
        ## normalizing TH and SMD pads
        if len(pads_TH_SMD) >0:
            pth_ordered=collect_pads(pads_TH_SMD) #pads_all)  ## pads normalized with sequence of segments
            ## search for drills (pads inside pads)
            drl_found=collect_drl(pth_ordered)
            #sayerr (pth_ordered)
            #sayw(drl_found)
            ## impiling pads 
            pads_TH_SMD=[]
            for p in pth_ordered:
                for e in p:
                    pads_TH_SMD.append (e)
            # print len(pads_TH_SMD)
            pth=[]
            pth=pads_TH_SMD
            ## impiling pads 
            drills=[]
            for p in drl_found:
                for e in p:
                    drills.append (e)
            # print len(drills)
            #print psmd
            #stop
        
        ## normalizing NPTH pads
        if len(pads_NPTH) >0:
            pth_ordered=collect_pads(pads_NPTH) #pads_all)  ## pads normalized with sequence of segments
            ## search for drills (pads inside pads)
            drl_found=collect_drl(pth_ordered)
            #sayerr (pth_ordered)
            #sayw(drl_found)
            #stop
            ## impiling pads 
            pads_NPTH=[]
            for p in pth_ordered:
                for e in p:
                    pads_NPTH.append (e)
            # print len(pads_NPTH)
            npth=[]
            npth=pads_NPTH
            ## impiling pads 
            #drills=[]
            for p in drl_found:
                for e in p:
                    drills.append (e)
            # print len(drills)
            #print psmd
            #stop
        
        ## normalizing Round Rect pads
        if len(prrect) >0:
            pth_ordered=collect_pads(prrect) #pads_all)  ## pads normalized with sequence of segments
            ## search for drills (pads inside pads)
            drl_found=collect_drl(pth_ordered)
            #sayerr (pth_ordered)
            #sayw(drl_found)
            #stop
            ## impiling pads 
            prrect=[]
            for p in pth_ordered:
                for e in p:
                    prrect.append (e)
            #print len(prrect)
            if len (prrect)>0:
                sayw('normalized Round Rect')
            #print prrect
            #npth=[]
            #npth=pads_NPTH
            ## impiling pads 
            #drills=[]
            for p in drl_found:
                for e in p:
                    drills.append (e)
            #print len(drills)
            #print psmd
            #stop
        
        ## normalizing Poly pads
        if len(pply) >0:
            #print(pply)
            pth_ordered=collect_pads(pply) #pads_all)  ## pads normalized with sequence of segments
            #sayerr(pth_ordered);sayerr(len(pth_ordered))
            ## impiling pads 
            #drl_found=collect_drl(pth_ordered)
            
            pply=[]
            for p in pth_ordered:
                for e in p:
                    pply.append (e)
            #print len(prrect)
            if len (pply)>0:
                sayw('normalized Poly')
            # ## impiling pads 
            # for p in drl_found:
            #     for e in p:
            #         drills.append (e)
            #print prrect
            #npth=[]
            #npth=pads_NPTH
            #print len(drills)
            #print psmd
            #stop

        ## normalizing NetTie Poly
        if len(ntply) >0:
            #sayerr(ntply)
            pth_ordered=collect_pads(ntply) #pads_all)  ## pads normalized with sequence of segments
            #sayerr(pth_ordered)
            ## impiling pads 
            #drl_found=collect_drl(pth_ordered)
            
            ntply=[]
            for p in pth_ordered:
                for e in p:
                    ntply.append (e)
            #print len(prrect)
            if len (ntply)>0:
                sayw('normalized NetTie Poly')

        ## normalizing Geom pads
        pGm=[]
        if len(pgeomG) >0:
            pth_ordered=collect_pads(pgeomG) #pads_all)  ## pads normalized with sequence of segments
            #sayerr(pth_ordered)
            ## impiling pads 
            drl_found=collect_drl(pth_ordered)
            print(drl_found)
            pGm=[]
            for p in pth_ordered:
                for e in p:
                    pGm.append (e)
            #print len(prrect)
            if len (pGm)>0:
                sayw('normalized Geom')
                #print(pGm)
            # ## impiling pads 
            # for p in drl_found:
            #     for e in p:
            #         drills.append (e)
            #print prrect
            #npth=[]
            #npth=pads_NPTH
            #print len(drills)
            #print psmd
            #stop
        
        ## writing content
        newcontent=u''+header
        #new_edge=new_border+os.linesep+')'+os.linesep
        #newcontent=newcontent+new_edge+u' '
        if len (new_border)>0:
            newcontent=newcontent+new_border #+os.linesep
        #print newcontent
            
        #### ----------SMD-------------------------------
        #npad=u''
        #mpad=[]
        #nline=1
        #pad_nbr=1
        #found_arc=False
        #for pad in psmd:
        #    if pad[0]=='circle':
        #        npad=npad+os.linesep+createFpPad(pad,offset,u'SMD')
        #    elif pad[0]=='line' and not found_arc:
        #        mpad.append(pad)
        #        if nline>=4:
        #            npad=npad+os.linesep+createFpPad(mpad,offset,u'SMD')
        #            nline=0
        #            mpad=[]
        #        nline=nline+1
        #    elif pad[0]=='arc' or (pad[0]=='line' and found_arc):
        #        found_arc=True
        #        mpad.append(pad)
        #        if nline>=4:
        #            npad=npad+os.linesep+createFpPad(mpad,offset,u'SMD')
        #            nline=0
        #            mpad=[]
        #            found_arc=False
        #        nline=nline+1
        #if len (npad)>0:
        #    newcontent=newcontent+npad+os.linesep
        #    sayw('created SMD pads')
        ### ----------Drills-------------------------------
        #print psmd
        mdrills=[]
        pad_nbr=1
        nline=1
        drill_pos=[]
        found_arc=False
        #sayerr(drills)
        for drill in drills:
            #sayerr(drill)
            if drill[0]=='circle':
                #ret=createFpPad(drill,offset,u'Drills')
                #sayw(ret)
                drill_pos.append(createFpPad(drill,offset,u'Drills'))
            # elif drill[0]=='line' and not found_arc:
            #     mdrills.append(drill)
            #     if nline>=4:
            #         #ndrill=ndrill+os.linesep+createFpPad(mdrills,offset,u'Drills')
            #         drill_pos.append(createFpPad(mdrill,offset,u'Drills'))
            #         nline=0
            #         mdrills=[]
            #     nline=nline+1
            elif drill[0]=='arc' or (drill[0]=='line' and found_arc):
                found_arc=True
                mdrills.append(drill)
                #print('arc or line + '+str(nline))
                if nline>=4:
                    #ndrill=ndrill+os.linesep+createFpPad(mdrills,offset,u'Drills')
                    drill_pos.append(createFpPad(mdrills,offset,u'Drills'))
                    nline=0
                    mdrills=[]
                    found_arc=False
                nline=nline+1
        #sayw(drill_pos)
        ## drill_pos (cntX,cntY,sizeX,sizeY)
        fp_type='  (attr smd)'+os.linesep
        if len (drill_pos)>0:
            #newcontent=newcontent+os.linesep+')'+os.linesep+u' '       
            sayw ('collected drills centers and positions')
            fp_type=''
        #re.sub(r'^[^\n]*\n', '', s)
            newcontent=u"(module "+fp_name.replace('-fp','')+" (layer F.Cu) (tedit 61218795)"+os.linesep+newcontent
        else:
            newcontent=u"(module "+fp_name.replace('-fp','')+" (layer F.Cu) (tedit 61218795)"+os.linesep+fp_type+newcontent
        
        #header=header+fp_type
        ### ----------TH-------------------------------      
        npad=u''
        mpad=[]
        nline=1
        pad_nbr=1
        found_arc=False
        for pad in pth:
            if pad[0]=='circle':
                npad=npad+os.linesep+createFpPad(pad,offset,u'TH', drill_pos)
            elif pad[0]=='line' and not found_arc:
                mpad.append(pad)
                if nline>=4:
                    npad=npad+os.linesep+createFpPad(mpad,offset,u'TH', drill_pos)
                    nline=0
                    mpad=[]
                nline=nline+1
            elif pad[0]=='arc' or (pad[0]=='line' and found_arc):
                found_arc=True
                mpad.append(pad)
                if nline>=4:
                    npad=npad+os.linesep+createFpPad(mpad,offset,u'TH', drill_pos)
                    nline=0
                    mpad=[]
                    found_arc=False
                nline=nline+1
                
        #print 'len pad '+str(len(npad))
        
        #print newcontent
        if len (npad)>0:
            newcontent=newcontent+npad+os.linesep
            say('created TH pads')
        ### ----------NPTH-------------------------------
        npad=u''
        mpad=[]
        nline=1
        pad_nbr=1
        found_arc=False
        for pad in npth:
            if pad[0]=='circle':
                npad=npad+os.linesep+createFpPad(pad,offset,u'NPTH', drill_pos)
            elif pad[0]=='line' and not found_arc:
                mpad.append(pad)
                if nline>=4:
                    npad=npad+os.linesep+createFpPad(mpad,offset,u'NPTH', drill_pos)
                    nline=0
                    mpad=[]
                nline=nline+1
            elif pad[0]=='arc' or (pad[0]=='line' and found_arc):
                found_arc=True
                mpad.append(pad)
                if nline>=4:
                    npad=npad+os.linesep+createFpPad(mpad,offset,u'NPTH', drill_pos)
                    nline=0
                    mpad=[]
                    found_arc=False
                nline=nline+1
                
        #print 'len pad '+str(len(npad))
        #print newcontent
        if len (npad)>0:
            newcontent=newcontent+npad+os.linesep
            say('created NPTH pads')
        ### ----------Round Rect-------------------------------
        npad=u''
        mpad=[]
        nline=1
        pad_nbr=1
        found_arc=False
        #found_line=False
        for pad in prrect:
            #sayw('RRect type '+pad[0])
            #sayerr(pad)
            #if pad[0]=='circle':
            #    npad=npad+os.linesep+createFpPad(pad,offset,u'NPTH', drill_pos)
            #if pad[0]=='line' and not found_arc:
            if pad[0]=='arc' and not found_arc:
                mpad.append(pad)
                found_arc=True
                nline=nline+1
            #elif pad[0]=='arc' or (pad[0]=='line' and found_arc):
            elif (nline<=8 and found_arc):
                mpad.append(pad)
                #print mpad
                #print nline
                if nline>=8:
                    #print npad
                    #print 'd pos ',drill_pos
                    #print 'mpad';print mpad
                    #print 'offset ',offset
                    #stop
                    npad=npad+os.linesep+createFpPad(mpad,offset,u'RoundRect', drill_pos)
                    nline=0
                    mpad=[]
                    found_arc=False
                nline=nline+1
        #print npad        
        # ### ----------Round Rect-------------------------------
        # npad=u''
        # mpad=[]
        # nline=1
        # pad_nbr=1
        # found_arc=False
        # for pad in prrect:
        #     #sayerr(pad)
        #     #if pad[0]=='circle':
        #     #    npad=npad+os.linesep+createFpPad(pad,offset,u'NPTH', drill_pos)
        #     if pad[0]=='line' and not found_arc:
        #         mpad.append(pad)
        #         nline=nline+1
        #     elif pad[0]=='arc' or (pad[0]=='line' and found_arc):
        #         found_arc=True
        #         mpad.append(pad)
        #         if nline>=8:
        #             #print npad
        #             #print 'd pos ',drill_pos
        #             #print 'mpad';print mpad
        #             #print 'offset ',offset
        #             #stop
        #             npad=npad+os.linesep+createFpPad(mpad,offset,u'RoundRect', drill_pos)
        #             nline=0
        #             mpad=[]
        #             found_arc=False
        #         nline=nline+1
        # #print npad        
        
        #print 'len pad '+str(len(npad))
        #print newcontent
        if len (npad)>0:
            newcontent=newcontent+npad+os.linesep
            say('created Round Rect pads')
        ### ----------Poly reference Pad-------------------------------
        #print psmd
        polypad=[]
        polypad=pply
        pad_nbr=1
        nline=1
        polypad_pos=[]
        found_arc=False
        #sayerr(polypad)
        for circ_pad in polypad:
            #sayerr(drill)
            if circ_pad[0]=='circle':
                #ret=createFpPad(drill,offset,u'Drills')
                #sayw(circ_pad)
                polypad_pos.append(createFpPad(circ_pad,offset,u'Drills'))
            # elif drill[0]=='line' and not found_arc:
            #     mdrills.append(drill)
            #     if nline>=4:
            #         #ndrill=ndrill+os.linesep+createFpPad(mdrills,offset,u'Drills')
            #         drill_pos.append(createFpPad(mdrill,offset,u'Drills'))
            #         nline=0
            #         mdrills=[]
            #     nline=nline+1
            
        #sayw(drill_pos)
        ## drill_pos (cntX,cntY,sizeX,sizeY)
        if len (polypad_pos)>0:
            #newcontent=newcontent+os.linesep+')'+os.linesep+u' '       
            sayw ('collected poly pads centers and positions')
            #print(polypad_pos, 'poly pad pos')
            #print(pply,'pl geo')
        ### ----------Poly-------------------------------
        #polypad_pos=[]  ### TBC polypad inside poly sketch
        #sayerr(pply)
        #sayerr(polypad_pos)
        npad=u''
        mpad=[]
        nline=1
        pad_nbr=1
        poly_closed=False
        for pad in pply:
            #sayerr(pad)
            #print('pad',pad)
            #if pad[0]=='circle':
            #    npad=npad+os.linesep+createFpPad(pad,offset,u'NPTH', drill_pos)
            if pad[0]=='line':
                mpad.append(pad)
                if len(mpad)>1:
                    if abs(mpad[0][1]-pad[3])<edge_tolerance and abs(mpad[0][2]-pad[4])<edge_tolerance:
                        #print(mpad[0][1],pad[3],mpad[0][2],pad[4])
                        sayerr('poly closed')
                        poly_closed=True
                        nline=1
                        #pad_nbr=pad_nbr+1
                else:
                    nline=nline+1
            if poly_closed:
                #print npad
                #print ('mpad', mpad)
                #print ('polypad_pos', polypad_pos)
                poly_closed=False
                if 0: #'B_Cu' in lyr:
                    npad=npad+os.linesep+createFpPad(mpad,offset,u'Poly_B_Cu', polypad_pos)
                else:
                    npad=npad+os.linesep+createFpPad(mpad,offset,u'Poly', polypad_pos)
                nline=1
                mpad=[]
            #nline=nline+1
        #print npad        
        
        #print 'len pad '+str(len(npad))
        #print newcontent
        if len (npad)>0:
            newcontent=newcontent+npad+os.linesep
            say('created Poly pads')

        ### ----------NetTie Poly reference pad -------------------------------
        #print psmd
        polypad=[]
        polypad=ntply
        pad_nbr=1
        nline=1
        polypad_pos=[]
        found_arc=False
        #sayerr(polypad)
        for circ_pad in polypad:
            #sayerr(drill)
            if circ_pad[0]=='circle':
                #ret=createFpPad(drill,offset,u'Drills')
                #sayw(circ_pad)
                polypad_pos.append(createFpPad(circ_pad,offset,u'Drills'))
            # elif drill[0]=='line' and not found_arc:
            #     mdrills.append(drill)
            #     if nline>=4:
            #         #ndrill=ndrill+os.linesep+createFpPad(mdrills,offset,u'Drills')
            #         drill_pos.append(createFpPad(mdrill,offset,u'Drills'))
            #         nline=0
            #         mdrills=[]
            #     nline=nline+1
            
        #sayw(drill_pos)
        ## drill_pos (cntX,cntY,sizeX,sizeY)
        if len (polypad_pos)>0:
            #newcontent=newcontent+os.linesep+')'+os.linesep+u' '       
            sayw ('collected net tie poly pads centers and positions')
            #print(polypad_pos, 'poly pad pos')
            #print(ntply,'nt geo')
        ### ----------Poly-------------------------------
        #polypad_pos=[]  ### TBC polypad inside poly sketch
        #sayerr(pply)
        #sayerr(polypad_pos)
        npad=u''
        mpad=[]
        nline=1
        pad_nbr=1
        poly_closed=False
        for pad in ntply:
            #sayerr(pad)
            #if pad[0]=='circle':
            #    npad=npad+os.linesep+createFpPad(pad,offset,u'NPTH', drill_pos)
            if pad[0]=='line':
                mpad.append(pad)
                if len(mpad)>1:
                    if abs(mpad[0][1]-pad[3])<edge_tolerance and abs(mpad[0][2]-pad[4])<edge_tolerance:
                        sayerr('poly closed')
                        poly_closed=True
                        nline=1
                        #pad_nbr=pad_nbr+1
                else:
                    nline=nline+1
            if poly_closed:
                #print npad
                #print 'mpad';print mpad
                poly_closed=False
                if 0: #'B_Cu' in lyr:
                    npad=npad+os.linesep+createFpPad(mpad,offset,u'NetTie_Poly_B_Cu', polypad_pos)
                else:
                    npad=npad+os.linesep+createFpPad(mpad,offset,u'NetTie_Poly', polypad_pos)
                nline=1
                mpad=[]
            #nline=nline+1
        #print npad        
        
        #print 'len pad '+str(len(npad))
        #print newcontent
        if len (npad)>0:
            newcontent=newcontent+npad+os.linesep
            say('created NetTie Poly pads')

        ### ----------FZ Poly-------------------------------
        #polypad_pos=[]  ### TBC polypad inside poly sketch
        #sayerr(pply)
        #sayerr(polypad_pos)
        npad=u''
        mpad=[]
        nline=1
        pad_nbr=1
        poly_closed=False
        polypad_pos=None
        for pad in fzply:
            #sayerr(pad)
            #if pad[0]=='circle':
            #    npad=npad+os.linesep+createFpPad(pad,offset,u'NPTH', drill_pos)
            if pad[0]=='line':
                mpad.append(pad)
                if len(mpad)>1:
                    if abs(mpad[0][1]-pad[3])<edge_tolerance and abs(mpad[0][2]-pad[4])<edge_tolerance:
                        sayerr('poly closed')
                        poly_closed=True
                        nline=1
                        #pad_nbr=pad_nbr+1
                else:
                    nline=nline+1
            if poly_closed:
                #print npad
                #print 'mpad';print mpad
                poly_closed=False
                npad=npad+os.linesep+createFpPad(mpad,offset,u'FZ_Mask_Poly', polypad_pos)
                nline=1
                mpad=[]
            #nline=nline+1
        #print npad        
        
        #print 'len pad '+str(len(npad))
        #print newcontent
        if len (npad)>0:
            newcontent=newcontent+npad+os.linesep
            say('created FZ Poly pads')
        ### ----------Geom reference Pad-------------------------------
        #print psmd
        pgeompad=[]
        pgeompad=pGm
        pad_nbr=1
        nline=1
        pgeompad_pos=[]
        found_arc=False
        #sayerr(polypad)
        for circ_pad in pgeompad:
            #sayerr(drill)
            if circ_pad[0]=='circle':
                #ret=createFpPad(drill,offset,u'Drills')
                #sayw(circ_pad)
                pgeompad_pos.append(createFpPad(circ_pad,offset,u'Drills'))
            # elif drill[0]=='line' and not found_arc:
            #     mdrills.append(drill)
            #     if nline>=4:
            #         #ndrill=ndrill+os.linesep+createFpPad(mdrills,offset,u'Drills')
            #         drill_pos.append(createFpPad(mdrill,offset,u'Drills'))
            #         nline=0
            #         mdrills=[]
            #     nline=nline+1
            
        #sayw(drill_pos)
        ## drill_pos (cntX,cntY,sizeX,sizeY)
        if len (pgeompad_pos)>0:
            #newcontent=newcontent+os.linesep+')'+os.linesep+u' '       
            sayw ('collected geometry pads centers and positions')
            sayw(pgeompad_pos)
        ### ----------Primitive Geometry-------------------------------
        ## only Circle supported ATM
        #polypad_pos=[]  ### TBC polypad inside poly sketch
        #sayerr(pply)
        #sayerr(polypad_pos)
        npad=u''
        mpad=[]
        nline=1
        pad_nbr=1
        #say (pgeom)
        #stop
        i=0
        for pad in pgeom:
            #sayerr(pad)
            #if pad[0]=='circle':
            #    npad=npad+os.linesep+createFpPad(pad,offset,u'NPTH', drill_pos)
            if pad[0]=='line':
                sayw('line not suported')
            if pad[0]=='circle':
                #print npad
                #print 'mpad';print mpad
                mpad.append(pad)
                npad=npad+os.linesep+createFpPad(mpad,offset,u'Pads_Geom', [pgeompad_pos[i]])
                nline=1
                mpad=[]
            i+=1
            #nline=nline+1
        #print npad        
        
        #print 'len pad '+str(len(npad))
        #print newcontent
        if len (npad)>0:
            newcontent=newcontent+npad+os.linesep
            say('created Geom pads')
            
        ## adding 3D model preset
        newcontent+=os.linesep+u"   (model \""+str(fpth)+os.sep+fp_name.rstrip('-fp')+u'.wrl\"'+os.linesep
        newcontent+=u"    (at (xyz 0 0 0))"+os.linesep
        newcontent+=u"    (scale (xyz 1 1 1))"+os.linesep
        newcontent+=u"    (rotate (xyz 0 0 0))"+os.linesep
        newcontent+=u"  )"+os.linesep
        ### ---------- wrtiting file --------------------
        newcontent=newcontent+')'+os.linesep+u' '       
        with codecs.open(fpath,'w', encoding='utf-8') as ofile:
            ofile.write(newcontent)
            ofile.close()        
        say_time()
        msg="""<b>new Footprint pushed to kicad footprint!</b><br><br>"""
        msg+="<b>file saved to<br>"+fpath+"</b><br><br>"
        msgr="new Footprint pushed to kicad footprint!\n"
        msgr+="file saved to "+fpath+"\n"
        lns=len (not_supported) 
        #print lns
        if lns > 2:
            if lns < 103: # writing only some geometry not supported
                msg+="<br><b>found downgraded Geometry:<br>"+not_supported[:-2]+"!</b>"
                msgr+="\nfound downgraded Geometry: "+not_supported[:-2]+"!"
            else:
                nss=not_supported[:-2]
                nss=nss[:101]+'... <br> ...'
                msg+="<br><b>found downgraded Geometry:<br>"+nss+"</b>"
                msgr+="\nfound downgraded Geometry: "+not_supported[:-2]+"!"
            
        say(msgr)
        say_info(msg)
        #if not edge_pcb_exists:
        #    msg="<b>close your FC Sketch<br>and reload the kicad_pcb file</b>"
        #    say_warning(msg)
        
            
###
def collect_drl(pads):

    pad_shps=[] #pad,center,shape
    if pads is not None:
        for p in pads:
            #sayw(p)
            #print p[0][0] ;print p[0][2] 
            if p[0][0]=='circle': 
                p_center=(p[0][2],p[0][3],0)
                p_radius=p[0][1]
                #print p_center
                wr=Part.Wire(Part.makeCircle(p_radius, Base.Vector(p_center)))
                ps=Part.Wire(wr)
                face = Part.Face(ps)
                Part.show(face)
                shpName=FreeCAD.ActiveDocument.ActiveObject.Name
                #say( FreeCAD.ActiveDocument.ActiveObject.Label)
                shape= FreeCAD.ActiveDocument.ActiveObject.Shape
                pad_shps.append([p,p_center,shpName])
            elif p[0][0] =='arc' and 'Pads_Round_Rect' in p[0][len(p[0])-1]:
                sayw('round rect')
                #print p
                r1=p[0][1]; cx1=p[0][2]; cy1=p[0][3]
                #print 'r1 ', r1, ' c1 ', cx1,',',cy1
                r2=p[2][1]; cx2=p[2][2]; cy2=p[2][3]
                #print 'r2 ', r2, ' c2 ', cx2,',',cy2
                #stop
                if abs(cx1-cx2)>edge_tolerance: # horizontal
                    sayerr('horizontal')
                    #print p
                    px=(p[0][10].x+p[2][10].x)/2;
                    py=(p[0][10].y+p[2][10].y)/2;
                    sx=2*r1+abs(p[1][1]-p[3][1]); 
                    sy=2*r1+abs(p[1][2]-p[1][4])
                    #print r1,' ',sx-2*r1
                else: #vertical
                    sayerr('vertical')
                    #print p[0][10].x
                    #print p[2][10].x
                    px=(p[0][10].x+p[2][10].x)/2;
                    py=(p[0][10].y+p[2][10].y)/2;
                    sx=2*r1+abs(p[3][1]-p[3][3]); 
                    sy=2*r1+abs(p[1][2]-p[1][4])
                p_center=(px,py,0)
                #Draft.makePoint(px,py, 0)
                wr=[]
                #print p 
                #arc -> approximate shape with rectangle
                wr.append(Part.makeLine((px-sx/2, py-sy/2,0.0),(px-sx/2, py+sy/2,0.0)))
                wr.append(Part.makeLine((px-sx/2, py+sy/2,0.0),(px+sx/2, py+sy/2,0.0)))
                wr.append(Part.makeLine((px+sx/2, py+sy/2,0.0),(px+sx/2, py-sy/2,0.0)))
                wr.append(Part.makeLine((px+sx/2, py-sy/2,0.0),(px-sx/2, py-sy/2,0.0)))

                ps=Part.Wire(wr)
                face = Part.Face(ps)
                Part.show(face)
                #stop
                shpName=FreeCAD.ActiveDocument.ActiveObject.Name
                #say( FreeCAD.ActiveDocument.ActiveObject.Label)
                shape= FreeCAD.ActiveDocument.ActiveObject.Shape
                pad_shps.append([p,p_center,shpName])   
            elif p[0][0]=='line':
                #print p
                px=(p[0][1]+p[0][3])/2;py=(p[1][2]+p[1][4])/2;
                if abs(p[0][1]-p[0][3]) >0:
                    sx=abs(p[0][1]-p[0][3])
                    px=(p[0][1]+p[0][3])/2
                else:
                    sx=abs(p[1][1]-p[1][3])
                    px=(p[1][1]+p[1][3])/2
                if abs(p[1][2]-p[1][4]) >0:
                    sy=abs(p[1][2]-p[1][4])
                    py=(p[1][2]+p[1][4])/2;
                else:
                    sy=abs(p[0][2]-p[0][4])
                    py=(p[0][2]+p[0][4])/2;
                # Draft.makePoint(px,py, 0)
                #print p[0];print p[1]
                #stop
                p_center=(px,py,0)
                wr=[]
                for lines in p:
                    wr.append(Part.makeLine((lines[1], lines[2],0.0),(lines[3], lines[4],0.0)))
                ps=Part.Wire(wr)
                face = Part.Face(ps)
                Part.show(face)
                #stop
                shpName=FreeCAD.ActiveDocument.ActiveObject.Name
                #say( FreeCAD.ActiveDocument.ActiveObject.Label)
                shape= FreeCAD.ActiveDocument.ActiveObject.Shape
                pad_shps.append([p,p_center,shpName])            
            elif p[0][0]=='arc':
                #print pad
                r1=p[0][1]; cx1=p[0][2]; cy1=p[0][3]
                #print 'r1 ', r1, ' c1 ', cx1,',',cy1
                r2=p[2][1]; cx2=p[2][2]; cy2=p[2][3]
                #print 'r2 ', r2, ' c2 ', cx2,',',cy2
                #stop
                if abs(cx1-cx2)>edge_tolerance: # horizontal
                    sayerr('horizontal')
                    px=(p[0][10].x+p[2][11].x)/2;py=(p[0][11].y+p[2][11].y)/2;
                    sx=2*r1+abs((p[0][10].x-p[2][11].x)); sy=2*r1
                else: #vertical
                    sayerr('vertical')
                    px=(p[0][10].x+p[0][11].x)/2;py=(p[0][10].y+p[2][10].y)/2;
                    sx=2*r1; sy=2*r1+abs((p[0][10].y-p[2][10].y))
                p_center=(px,py,0)
                # Draft.makePoint(px,py, 0)
                wr=[]
                #print p 
                #arc -> approximate shape with rectangle
                wr.append(Part.makeLine((px-sx/2, py-sy/2,0.0),(px-sx/2, py+sy/2,0.0)))
                wr.append(Part.makeLine((px-sx/2, py+sy/2,0.0),(px+sx/2, py+sy/2,0.0)))
                wr.append(Part.makeLine((px+sx/2, py+sy/2,0.0),(px+sx/2, py-sy/2,0.0)))
                wr.append(Part.makeLine((px+sx/2, py-sy/2,0.0),(px-sx/2, py-sy/2,0.0)))

                ps=Part.Wire(wr)
                face = Part.Face(ps)
                Part.show(face)
                #stop
                shpName=FreeCAD.ActiveDocument.ActiveObject.Name
                #say( FreeCAD.ActiveDocument.ActiveObject.Label)
                shape= FreeCAD.ActiveDocument.ActiveObject.Shape
                pad_shps.append([p,p_center,shpName])   
        i=1
        drl=[]
        for p in pad_shps:
            #print d
            point1=FreeCAD.Vector(p[1])
            #Draft.makePoint(p[1][0],p[1][1],p[1][2])
            shp=FreeCAD.ActiveDocument.getObject(p[2]).Shape
            for p2 in pad_shps[i:]:
                shp2=FreeCAD.ActiveDocument.getObject(p2[2]).Shape
                #sayw(point);say(shp2.BoundBox.YLength);sayw(shp.BoundBox.YLength)
                #print shp2.isInside(point,0,True)
                point2=FreeCAD.Vector(p2[1])
                if shp2.isInside(point1,0,True):
                    sayerr('pad in pad found! ')#+str(p[0]))
                    #checking who is inside
                    if shp2.BoundBox.YLength > shp.BoundBox.YLength:
                        drl.append(p[0])
                    else:
                        drl.append(p2[0])
                elif shp.isInside(point2,0,True):
                    sayerr('pad in pad found! ')#+str(p2[0]))
                    #checking who is inside
                    if shp2.BoundBox.YLength > shp.BoundBox.YLength:
                        drl.append(p[0])
                    else:
                        drl.append(p2[0])
            i=i+1    
        #print pad_shps
        #sayw(drl)
        testing=False #True
        if not testing:
            for p in pad_shps:
                FreeCAD.ActiveDocument.removeObject(p[2])
        for d in drl:
            pads.remove(d) ## remove drls from pads
        #say(pads)
        return drl
    else:
        drl=[]
        return  drl
    ## return drls and pads without drls
##

def collect_pads(pad_list):

    #print pad_list
    
    #sort edges to form a single closed 2D shape
    loopcounter = 0
    normalized_pads = []
    #sayw((edges))
    #stop
    if (len(pad_list)==0):
        sayw("no Pads found")
    else:
        newPads = [];
        #sayerr(pad_list)
        for pad in (pad_list):
            #print pad
            if pad[0]=='circle':
                normalized_pads.append([pad])
                #pad_list.pop(i)
        npd=[]
        for pad in (pad_list):
            if pad[0]!='circle':
                npd.append(pad)
        pad_list=[]
        pad_list=npd
        #sayw(pad_list)
        #sayerr (len(pad_list))
        #stop        
        if (len(pad_list)>0):
            #print pad_list
            #newPads.append(pad_list.pop(0))
            #print 'HERE'
            #print pad_list[0]
            ## print pad_list[1][9].Radius, ' ',pad_list[1][9].Center.x,' ',pad_list[1][9].Center.y
            ## print pad_list[1][10].x, ' ',pad_list[1][10].y  # p1.x,p1.y
            ## print pad_list[1][11].x, ' ',pad_list[1][11].y  # p2.x,p2.y
            newPads.append(pad_list[0])
            pad_list.pop(0)
            #print pad_list
            if newPads[0][0]=='line':
                #print newPads,' line'#;stop
                nextCoordinate = (newPads[0][3],newPads[0][4])
                firstCoordinate = (newPads[0][1],newPads[0][2])
            elif newPads[0][0]=='arc':
                nextCoordinate = (newPads[0][10].x,newPads[0][10].y)
                firstCoordinate = (newPads[0][11].x,newPads[0][11].y)
            #elif newPads[0][0]=='circle':
            #    normalized_pads.append(newPads)
            #    ## TDB!!!
        #print 'nextCoordinate1 ',nextCoordinate
        #print pad_list;stop           
        while(len(pad_list)>0 and loopcounter < 2):
            loopcounter = loopcounter + 1
            #print "nextCoordinate: ", nextCoordinate
            #if len(newEdges[0].Vertexes) > 1: # not circle
            for j, pad in enumerate(pad_list):
                #print j
                #sayerr(pad_list[j][0])
                #say(pad)
                #print pad_list[j],' line1'#;stop
                if pad_list[j][0]=='line':
                    #print pad_list[j],' line2'#;stop
                    #print 'nextCoordinate ',nextCoordinate
                    if distance((pad_list[j][3],pad_list[j][4]), nextCoordinate)<=edge_tolerance:
                        #if edges[j].Vertexes[-1].Point != nextCoordinate:
                        ## if distance((pad_list[j][3],pad_list[j][4]), nextCoordinate)>edge_tolerance_warning:
                        ##     sayerr('non coincident edges:\n'+str(nextCoordinate)+';'+str((pad_list[j][1],pad_list[j][2])))
                        nextCoordinate = (pad_list[j][1],pad_list[j][2])
                        newPads.append(pad_list.pop(j))
                        loopcounter = 0
                        break
                    elif distance((pad_list[j][1],pad_list[j][2]), nextCoordinate)<=edge_tolerance:
                        #if edges[j].Vertexes[0].Point != nextCoordinate:
                        ## if distance((pad_list[j][1],pad_list[j][2]), nextCoordinate)>edge_tolerance_warning:
                        ##     sayerr('non coincident edges:\n'+str(nextCoordinate)+';'+str((pad_list[j][3],pad_list[j][4])))
                        nextCoordinate = (pad_list[j][3],pad_list[j][4])
                        newPads.append(pad_list.pop(j))
                        loopcounter = 0
                        break
                elif pad_list[j][0]=='arc':
                    #print pad_list[j],' line2'#;stop
                    #print 'nextCoordinate ',nextCoordinate
                    if distance((pad_list[j][11].x,pad_list[j][11].y), nextCoordinate)<=edge_tolerance:
                        #if edges[j].Vertexes[-1].Point != nextCoordinate:
                        ## if distance((pad_list[j][3],pad_list[j][4]), nextCoordinate)>edge_tolerance_warning:
                        ##     sayerr('non coincident edges:\n'+str(nextCoordinate)+';'+str((pad_list[j][1],pad_list[j][2])))
                        nextCoordinate = (pad_list[j][10].x,pad_list[j][10].y)
                        newPads.append(pad_list.pop(j))
                        loopcounter = 0
                        break
                    elif distance((pad_list[j][10].x,pad_list[j][10].y), nextCoordinate)<=edge_tolerance:
                        #if edges[j].Vertexes[0].Point != nextCoordinate:
                        ## if distance((pad_list[j][1],pad_list[j][2]), nextCoordinate)>edge_tolerance_warning:
                        ##     sayerr('non coincident edges:\n'+str(nextCoordinate)+';'+str((pad_list[j][3],pad_list[j][4])))
                        nextCoordinate = (pad_list[j][11].x,pad_list[j][11].y)
                        newPads.append(pad_list.pop(j))
                        loopcounter = 0
                        break
                #elif pad_list[j][0]=='circle':
                #    nextCoordinate=firstCoordinate
                #    normalized_pads.append(newPads)
                #    loopcounter = 0
                #    break
                #    #print pad_list[j]
                #    #stop
            #sayw(len(pad_list))
            #sayw(pad_list)
            if distance(firstCoordinate, nextCoordinate)<=edge_tolerance:# or pad_list[j-1][0]=='circle':
                say('2d closed path')
                normalized_pads.append(newPads)
                if (len(pad_list)>0):
                    newPads = [];
                    newPads.append(pad_list.pop(0))
                    if newPads[0][0]=='line':
                        nextCoordinate = (newPads[0][3],newPads[0][4])
                        firstCoordinate = (newPads[0][1],newPads[0][2])
                    elif newPads[0][0]=='arc':
                        nextCoordinate = (newPads[0][11].x,newPads[0][11].y)
                        firstCoordinate = (newPads[0][10].x,newPads[0][10].y)
                        #stop
                    #elif newPads[0][0]=='circle':
                        
                #else:
                #    say("error in creating Pads")
                #    stop                    
        #print normalized_pads, 'pads NBR ', len(normalized_pads), 'loopcounter ', loopcounter
        #sayw('pads NBR '+str(len(normalized_pads)))
        #sayw('normalized_pads '+str((normalized_pads)))
        norm_pads=[];n_pads=[]
        #print normalized_pads
        #stop
        for pads in normalized_pads:
            #sayw (pads)
            if pads[0][0]=='line':
                #stop
                first_elm = pads[0]
                n_pads=[];i=1
                for elm in pads:
                    if i>1:
                        n_pads.append(elm)
                    i=i+1
                n_pads.append(first_elm)
                    #stop
                norm_pads.append(n_pads)
            else:
                norm_pads.append(pads)
        #sayerr(norm_pads);stop

        if len (norm_pads)>0:
            #sayw(norm_pads)
            return norm_pads
        else:
            return normalized_pads
        
##

def createFpPad(pad,offset,tp, _drills=None):
    global pad_nbr, edge_tolerance
    
    #if tp=='SMD':
    #    if pad[0]=='circle':
    #        sayerr('circle pad nbr.'+str(pad_nbr))
    #        px=pad[2];py=pad[3]*-1;sx=2*pad[1];sy=2*pad[1]
    #        pdl ="  (pad "+str(pad_nbr)+" smd circle (at "+str(px)+" "+str(py)+") (size "+str(sx)+" "+str(sy)+") (layers F.Cu F.Paste F.Mask))"
    #        pad_nbr=pad_nbr+1
    #        #say(pad)
    #        return pdl
    #    elif pad[0][0]=='line':
    #        sayerr('rect pad nbr.'+str(pad_nbr))
    #        px=(pad[0][1]+pad[0][3])/2;py=(pad[1][2]+pad[1][4])/-2;
    #        if abs(pad[0][1]-pad[0][3]) >0:
    #            sx=abs(pad[0][1]-pad[0][3])
    #            px=(pad[0][1]+pad[0][3])/2
    #        else:
    #            sx=abs(pad[1][1]-pad[1][3])
    #            px=(pad[1][1]+pad[1][3])/2
    #        if abs(pad[1][2]-pad[1][4]) >0:
    #            sy=abs(pad[1][2]-pad[1][4])
    #            py=(pad[1][2]+pad[1][4])/-2;
    #        else:
    #            sy=abs(pad[0][2]-pad[0][4])
    #            py=(pad[0][2]+pad[0][4])/-2;
    #            #print pad[0];print pad[1]
    #            #stop
    #        pdl ="  (pad "+str(pad_nbr)+" smd rect (at "+str(px)+" "+str(py)+") (size "+str(sx)+" "+str(sy)+") (layers F.Cu F.Paste F.Mask))"
    #        pad_nbr=pad_nbr+1
    #        #say(pad);sayw(pdl)
    #        return pdl
    #    elif pad[0][0]=='arc':
    #        sayerr('arc pad nbr.'+str(pad_nbr))
    #        #print pad[0]
    #        r1=pad[0][1]; cx1=pad[0][2]; cy1=pad[0][3]
    #        #print 'r1 ', r1, ' c1 ', cx1,',',cy1
    #        r2=pad[2][1]; cx2=pad[2][2]; cy2=pad[2][3]
    #        #print 'r2 ', r2, ' c2 ', cx2,',',cy2
    #        #stop
    #        ## px=((cx1-r1)+(cx2+r2))/2;py=((cy1-r1)+(cy2+r2))/-2;sx=abs((cx1-r1)-(cx2+r2));sy=abs((cy1-r1)-(cy2+r2))
    #        #print pad[0]
    #        #print pad[1]
    #        if abs(cx1-cx2)>edge_tolerance: # horizontal
    #            sayerr('horizontal')
    #            px=(pad[0][10].x+pad[2][11].x)/2;py=(pad[0][11].y+pad[2][11].y)/-2;
    #            sx=2*r1+abs((pad[0][10].x-pad[2][11].x)); sy=2*r1
    #        else: #vertical
    #            sayerr('vertical')
    #            px=(pad[0][10].x+pad[0][11].x)/2;py=(pad[0][10].y+pad[2][10].y)/-2;
    #            sx=2*r1; sy=2*r1+abs((pad[0][10].y-pad[2][10].y))
    #        pdl ="  (pad "+str(pad_nbr)+" smd oval (at "+str(px)+" "+str(py)+") (size "+str(sx)+" "+str(sy)+") (layers F.Cu F.Paste F.Mask))"
    #        pad_nbr=pad_nbr+1
    #        #say(pad);sayw(pdl)
    #        return pdl
    #    else:
    #        return u''
    if tp=='Drills':  #getting center and size
        if pad[0]=='circle':
            sayerr('circle drill')
            px=pad[2];py=pad[3]*-1;sx=2*pad[1];sy=2*pad[1]
            drl =[px,py,sx,sy]
            pad_nbr=pad_nbr+1
            #say(drl)
            return drl
        elif pad[0][0]=='arc':
            sayerr('oval drill')
            #print pad
            r1=pad[0][1]; cx1=pad[0][2]; cy1=pad[0][3]
            #print 'r1 ', r1, ' c1 ', cx1,',',cy1
            r2=pad[2][1]; cx2=pad[2][2]; cy2=pad[2][3]
            # print 'r2 ', r2, ' c2 ', cx2,',',cy2
            #stop
            ## different method for horizontal and vertical
            if abs(cx1-cx2)>edge_tolerance: # horizontal
                px=((cx1-r1)+(cx2+r2))/2;py=((cy1-r1)+(cy2+r2))/-2;sx=abs(cx1-cx2)+2*r2;sy=2*r2
            else: #vertical
                px=((cx1-r1)+(cx2+r2))/2;py=((cy1-r1)+(cy2+r2))/-2;sx=2*r2;sy=abs(cy1-cy2)+2*r2
            drl =[px,py,sx,sy]
            pad_nbr=pad_nbr+1
            #say(pad);sayw(drl)
            return drl
        else:
            return u''
    #elif tp == 'PadsAll' or tp=='TH' or tp=='NPTH':  #getting center and size
    elif 'PadsAll' in tp or tp=='TH' or tp=='NPTH':  #getting center and size
        pad_layers=" (layers *.Cu *.Mask))"
        if tp=='PadsAll':
            tp='TH';ptp='thru_hole'
        if tp=='TH':
            ptp='thru_hole'
        else:
            ptp='np_thru_hole'
        #sayw (pad)
        found_drill=False
        if pad[0]=='circle':
            if '_padNbr=' in pad[-1]:
                padNbr='"'+pad[-1][pad[-1].index('_padNbr='):].replace('_padNbr=','').replace('_tmp','').replace('_','')+'"'
            elif '_padNum=' in pad[-1]:
                padNbr='"'+pad[-1][pad[-1].index('_padNum='):].replace('_padNum=','').replace('_tmp','').replace('_','')+'"'
            else:
                padNbr='"#"'
            sayerr('circle pad nbr.'+str(pad_nbr))
            cx=pad[2];cy=pad[3]*-1;sx=2*pad[1];sy=2*pad[1]
            if len(_drills)>0:
                #print _drills
                for d in _drills:
                    # print d
                    if d[0] > cx-sx/2 and d[0] < cx+sx/2 and d[1] > cy-sy/2 and d[1] < cy+sy/2:
                        sayw('drill in pad found!')
                        found_drill=True
                        break
                #drl_size=[d[2],d[3]]
                ### OFFSET
                if found_drill:
                    if d[2]!=d[3]:
                        drill_str="(drill oval "+"{0:.3f}".format(d[2])+" "+"{0:.3f}".format(d[3]) #+")"
                    else:
                        drill_str="(drill "+"{0:.3f}".format(d[2]) #+")"
                    if abs(d[0]-cx)>edge_tolerance or abs(d[1]-cy)>edge_tolerance:
                    #if d[0] != cx or d[1] != cy:
                        drill_str=drill_str+" (offset "+"{0:.3f}".format(cx-d[0])+" "+"{0:.3f}".format(cy-d[1])+"))" #+")"
                        cx=d[0];cy=d[1]
                    else:
                        drill_str=drill_str+")"
                else:
                    drill_str="" #"(drill 0)"
                    if tp=='NPTH':
                        ptp="np_thru_hole"; pad_layers=" (layers *.Cu *.Mask))"
                        drill_str="(drill "+"{0:.3f}".format(sx) +")"
                        #drill_str="(drill oval "+str(d[2])+" "+str(d[3]) #"(drill 0)"
                    else:
                        #print('pad[-1]',pad[-1])
                        pattern = '_In+([0-9]*?).Cu'
                        result = re.search(pattern, pad[-1])
                        if 'B_Cu' in pad[-1]:
                            pdLr='B.Cu'
                            ptp="smd"; pad_layers=" (layers B.Cu B.Paste B.Mask))"
                        elif result is not None:
                            pdLr=result.group().replace('_','.')[1:]
                            ptp="smd"; pad_layers=" (layers "+pdLr+"))"
                        else:
                            pdLr='F.Cu'
                            ptp="smd"; pad_layers=" (layers F.Cu F.Paste F.Mask))"
                        drill_str="" #"(drill 0)"
            else:
                if tp=='NPTH':
                    ptp="np_thru_hole"; pad_layers=" (layers *.Cu *.Mask))"
                    drill_str="(drill "+"{0:.3f}".format(sx) +")"
                    #drill_str="(drill oval "+str(d[2])+" "+str(d[3]) #"(drill 0)"
                else:
                    if 0: #'B_Cu' in tp:
                        ptp="smd"; pad_layers=" (layers B.Cu B.Paste B.Mask))"
                    else:
                        ptp="smd"; pad_layers=" (layers F.Cu F.Paste F.Mask))"
                    drill_str="" #"(drill 0)"
            if sx==sy:
                pshp='circle'
            else:
                pshp='oval'
            #pdl ="  (pad "+str(pad_nbr)+" "+ptp+" "+pshp+" (at "+str(cx)+" "+str(cy)+") (size "+str(sx)+" "+str(sy)+") "+drill_str+pad_layers
            pdl ="  (pad "+padNbr+" "+ptp+" "+pshp+" (at "+"{0:.3f}".format(cx)+" "+"{0:.3f}".format(cy)+") (size "+"{0:.3f}".format(sx)+" "+"{0:.3f}".format(sy)+") "+drill_str+pad_layers
            pad_nbr=pad_nbr+1
            #say(pad)
            return pdl
        elif pad[0][0]=='line':
            if '_padNbr=' in pad[0][-1]:
                padNbr='"'+pad[0][-1][pad[0][-1].index('_padNbr='):].replace('_padNbr=','').replace('_tmp','').replace('_','')+'"'
            elif '_padNum=' in pad[0][-1]:
                padNbr='"'+pad[0][-1][pad[0][-1].index('_padNum='):].replace('_padNum=','').replace('_tmp','').replace('_','')+'"'
            else:
                padNbr='"#"'
            #say(_drills)
            #sayerr('rect pad nbr.'+str(pad_nbr))
            #sayw(str(pad))
            #cx=(pad[0][1]+pad[0][3])/2;cy=(pad[1][2]+pad[1][4])/-2;sx=abs(pad[0][1]-pad[0][3]);sy=abs(pad[1][2]-pad[1][4])
            ptype="rect"
            sayerr('rect pad nbr.'+str(pad_nbr))
            px=(pad[0][1]+pad[0][3])/2;py=(pad[1][2]+pad[1][4])/-2;
            if abs(pad[0][1]-pad[0][3]) > edge_tolerance:
                sx=abs(pad[0][1]-pad[0][3])
                px=(pad[0][1]+pad[0][3])/2
            else:
                sx=abs(pad[1][1]-pad[1][3])
                px=(pad[1][1]+pad[1][3])/2
            if abs(pad[1][2]-pad[1][4]) > edge_tolerance:
                sy=abs(pad[1][2]-pad[1][4])
                py=(pad[1][2]+pad[1][4])/-2;
            else:
                sy=abs(pad[0][2]-pad[0][4])
                py=(pad[0][2]+pad[0][4])/-2;
                #print pad[0];print pad[1]
                #stop
            found_drill=False
            if len(_drills)>0:
                for d in _drills:
                    if d[0] > px-sx/2 and d[0] < px+sx/2 and d[1] > py-sy/2 and d[1] < py+sy/2:
                        sayw('drill in pad found! '+str(d[0])+','+str(d[1])+'/'+str(px)+','+str(py)+':'+str(sx)+','+str(sy))
                        found_drill=True
                        break
                #drl_size=[d[2],d[3]]
                ### OFFSET
                if found_drill:
                    if d[2]!=d[3]:
                        drill_str="(drill oval "+"{0:.3f}".format(d[2])+" "+"{0:.3f}".format(d[3]) #+")"
                    else:
                        drill_str="(drill "+"{0:.3f}".format(d[2]) #+")"
                    if abs(d[0]-px)>edge_tolerance or abs(d[1]-py)>edge_tolerance:
                        drill_str=drill_str+" (offset "+"{0:.3f}".format(px-d[0])+" "+"{0:.3f}".format(py-d[1])+"))" #+")"
                        px=d[0];py=d[1]
                    else:
                        drill_str=drill_str+")"
                else:
                    drill_str="" #"(drill 0)"
                    if tp=='NPTH':
                        sayerr('Error: NPTH rectangular pad WITHOUT drill -> correcting to oval/circle pad')
                        ptp="np_thru_hole"; pad_layers=" (layers *.Cu *.Mask))"
                        if sx==sy:
                            drill_str="(drill "+"{0:.3f}".format(sx) +")"
                            ptype="circle"
                        else:
                            drill_str="(drill oval "+"{0:.3f}".format(sx)+" "+"{0:.3f}".format(sy)+")" #"(drill 0)"
                            ptype="oval"
                    else:
                        #print('pad[-1] Rect',pad[-1])
                        pattern = '_In+([0-9]*?).Cu'
                        result = re.search(pattern, pad[0][-1])
                        if 'B_Cu' in pad[0][-1]:
                            pdLr='B.Cu'
                            ptp="smd"; pad_layers=" (layers B.Cu B.Paste B.Mask))"
                        elif result is not None:
                            pdLr=result.group().replace('_','.')[1:]
                            ptp="smd"; pad_layers=" (layers "+pdLr+"))"
                        else:
                            pdLr='F.Cu'
                            ptp="smd"; pad_layers=" (layers F.Cu F.Paste F.Mask))"
                        #ptp="smd"; pad_layers=" (layers F.Cu F.Paste F.Mask))"
                        #drill_str="" #"(drill 0)"
            else:
                if tp=='NPTH':
                    ptp="np_thru_hole"; pad_layers=" (layers *.Cu *.Mask))"
                    if sx==sy:
                        drill_str="(drill "+"{0:.3f}".format(sx) +")"
                        ptype="circle"
                    else:
                        drill_str="(drill oval "+"{0:.3f}".format(sx)+" "+"{0:.3f}".format(sy)+")" #"(drill 0)"
                        ptype="oval"
                else:
                    #print('pad[-1] Rect 2',pad[-1])
                    pattern = '_In+([0-9]*?).Cu'
                    result = re.search(pattern, pad[0][-1])
                    if 'B_Cu' in pad[0][-1]:
                        pdLr='B.Cu'
                        ptp="smd"; pad_layers=" (layers B.Cu B.Paste B.Mask))"
                    elif result is not None:
                        pdLr=result.group().replace('_','.')[1:]
                        ptp="smd"; pad_layers=" (layers "+pdLr+"))"
                    else:
                        pdLr='F.Cu'
                        ptp="smd"; pad_layers=" (layers F.Cu F.Paste F.Mask))"
                    #ptp="smd"; pad_layers=" (layers F.Cu F.Paste F.Mask))"
                    drill_str="" #"(drill 0)"

                #pdl ="  (pad "+str(pad_nbr)+" "+ptp+" rect (at "+str(px)+" "+str(py)+") (size "+str(sx)+" "+str(sy)+") "+drill_str+pad_layers
            pdl ="  (pad "+padNbr+" "+ptp+" "+ptype+" (at "+"{0:.3f}".format(px)+" "+"{0:.3f}".format(py)+") (size "+"{0:.3f}".format(sx)+" "+"{0:.3f}".format(sy)+") "+drill_str+pad_layers
            #pdl ="  (pad "+str(pad_nbr)+" thru_hole rect (at "+str(px)+" "+str(py)+") (size "+str(sx)+" "+str(sy)+") (layers F.Cu F.Paste F.Mask))"
            pad_nbr=pad_nbr+1
            #say(pad);sayw(pdl)
            return pdl
        elif pad[0][0]=='arc':
            if '_padNbr=' in pad[0][-1]:
                padNbr='"'+pad[0][-1][pad[0][-1].index('_padNbr='):].replace('_padNbr=','').replace('_tmp','').replace('_','')+'"'
            elif '_padNum=' in pad[0][-1]:
                padNbr='"'+pad[0][-1][pad[0][-1].index('_padNum='):].replace('_padNum=','').replace('_tmp','').replace('_','')+'"'
            else:
                padNbr='"#"'
            sayerr('arc pad nbr.'+str(pad_nbr))
            #print pad
            r1=pad[0][1]; cx1=pad[0][2]; cy1=pad[0][3]
            #print 'r1 ', r1, ' c1 ', cx1,',',cy1
            r2=pad[2][1]; cx2=pad[2][2]; cy2=pad[2][3]
            #print 'r2 ', r2, ' c2 ', cx2,',',cy2
            #stop
            if abs(cx1-cx2)>edge_tolerance: # horizontal
                sayerr('horizontal')
                px=(pad[0][10].x+pad[2][11].x)/2;py=(pad[0][11].y+pad[2][11].y)/-2;
                sx=2*r1+abs((pad[0][10].x-pad[2][11].x)); sy=2*r1
            else: #vertical
                sayerr('vertical')
                px=(pad[0][10].x+pad[0][11].x)/2;py=(pad[0][10].y+pad[2][10].y)/-2;
                sx=2*r1; sy=2*r1+abs((pad[0][10].y-pad[2][10].y))
 
            found_drill=False
            if len(_drills)>0:
                for d in _drills:
                    if d[0] > px-sx/2 and d[0] < px+sx/2 and d[1] > py-sy/2 and d[1] < py+sy/2:
                        sayw('drill in pad found! '+str(d[0])+','+str(d[1])+'/'+str(px)+','+str(py)+':'+str(sx)+','+str(sy))
                    #if d[0] > cx-sx/2 and d[0] < cx+sx/2 and d[1] > cy-sy/2 and d[1] < cy+sy/2:
                    #    sayw('drill in pad found!')
                        found_drill=True
                        break
                #drl_size=[d[2],d[3]]
                ### OFFSET
                if found_drill:
                    if d[2]!=d[3]:
                        drill_str="(drill oval "+"{0:.3f}".format(d[2])+" "+"{0:.3f}".format(d[3]) #+")"
                    else:
                        drill_str="(drill "+"{0:.3f}".format(d[2]) #+")"
                    if abs(d[0]-px)>edge_tolerance or abs(d[1]-py)>edge_tolerance:
                        drill_str=drill_str+" (offset "+"{0:.3f}".format(px-d[0])+" "+"{0:.3f}".format(py-d[1])+"))" #+")"
                        px=d[0];py=d[1]
                    else:
                        drill_str=drill_str+")"
                else:
                    if tp=='NPTH':
                        ptp="np_thru_hole"; pad_layers=" (layers *.Cu *.Mask))"
                        if sx==sy:
                            drill_str="(drill "+"{0:.3f}".format(sx) +")"
                        else:
                            drill_str="(drill oval "+"{0:.3f}".format(sx)+" "+"{0:.3f}".format(sy)+")" #"(drill 0)"
                        #drill_str="(drill oval "+str(d[2])+" "+str(d[3]) #"(drill 0)"
                    else:
                        pattern = '_In+([0-9]*?).Cu'
                        result = re.search(pattern, pad[0][-1])
                        if 'B_Cu' in pad[0][-1]:
                            pdLr='B.Cu'
                            ptp="smd"; pad_layers=" (layers B.Cu B.Paste B.Mask))"
                        elif result is not None:
                            pdLr=result.group().replace('_','.')[1:]
                            ptp="smd"; pad_layers=" (layers "+pdLr+"))"
                        else:
                            pdLr='F.Cu'
                            ptp="smd"; pad_layers=" (layers F.Cu F.Paste F.Mask))"
                        if '_padNbr=' in pad[0][-1]:
                            padNbr='"'+pad[0][-1][pad[0][-1].index('_padNbr='):].replace('_padNbr=','')+'"'
                        elif '_padNum=' in pad[0][-1]:
                            padNbr='"'+pad[0][-1][pad[0][-1].index('_padNum='):].replace('_padNum=','')+'"'
                        else:
                            padNbr='"#"'
                        #ptp="smd"; pad_layers=" (layers F.Cu F.Paste F.Mask))"
                        drill_str="" #"(drill 0)"
            else:
                if tp=='NPTH':
                    ptp="np_thru_hole"; pad_layers=" (layers *.Cu *.Mask))"
                    if sx==sy:
                        drill_str="(drill "+"{0:.3f}".format(sx) +")"
                    else:
                        drill_str="(drill oval "+"{0:.3f}".format(sx)+" "+"{0:.3f}".format(sy)+")" #"(drill 0)"
                    #drill_str="(drill oval "+str(d[2])+" "+str(d[3]) #"(drill 0)"
                else:
                    pattern = '_In+([0-9]*?).Cu'
                    result = re.search(pattern, pad[0][-1])
                    if 'B_Cu' in pad[0][-1]:
                        pdLr='B.Cu'
                        ptp="smd"; pad_layers=" (layers B.Cu B.Paste B.Mask))"
                    elif result is not None:
                        pdLr=result.group().replace('_','.')[1:]
                        ptp="smd"; pad_layers=" (layers "+pdLr+"))"
                    else:
                        pdLr='F.Cu'
                        ptp="smd"; pad_layers=" (layers F.Cu F.Paste F.Mask))"
                    #ptp="smd"; pad_layers=" (layers F.Cu F.Paste F.Mask))"
                    drill_str="" #"(drill 0)"

            #pdl ="  (pad "+str(pad_nbr)+" "+ptp+" oval (at "+str(px)+" "+str(py)+") (size "+str(sx)+" "+str(sy)+") "+drill_str+pad_layers
            pdl ="  (pad "+padNbr+" "+ptp+" oval (at "+"{0:.3f}".format(px)+" "+"{0:.3f}".format(py)+") (size "+"{0:.3f}".format(sx)+" "+"{0:.3f}".format(sy)+") "+drill_str+pad_layers
            #pdl ="  (pad "+str(pad_nbr)+" "+ptp+" oval (at "+str(cx)+" "+str(cy)+") (size "+str(sx)+" "+str(sy)+") (layers F.Cu F.Paste F.Mask))"
            pad_nbr=pad_nbr+1
            #say(pad);sayw(pdl)
            return pdl
        else:
            return u''
    ##--------------------------------------------##
    #elif tp=='RoundRect':
    elif 'RoundRect' in tp:
        if '_padNbr=' in pad[0][-1]:
            padNbr='"'+pad[0][-1][pad[0][-1].index('_padNbr='):].replace('_padNbr=','').replace('_tmp','').replace('_','')+'"'
        elif '_padNum=' in pad[0][-1]:
            padNbr='"'+pad[0][-1][pad[0][-1].index('_padNum='):].replace('_padNum=','').replace('_tmp','').replace('_','')+'"'
        else:
            padNbr='"#"'
        found_drill=False
        #sayw(pad)
        #stop
        ptp='thru_hole'
        pad_layers=" (layers *.Cu *.Mask)"
        if pad[0][0]=='arc':
            #say(_drills)
            sayerr('round rect pad nbr.'+str(pad_nbr))
            #print p
            r1=pad[0][1]; cx1=pad[0][2]; cy1=pad[0][3]
            #print 'r1 ', r1, ' c1 ', cx1,',',cy1
            r2=pad[4][1]; cx2=pad[4][2]; cy2=pad[2][3]
            #print 'r2 ', r2, ' c2 ', cx2,',',cy2
            #stop
            if abs(cx1-cx2)>edge_tolerance: # horizontal
                sayerr('horizontal')
                #print pad
                px=(pad[0][10].x+pad[4][10].x)/2;
                py=(pad[0][10].y+pad[4][10].y)/2;
                sx=abs(pad[5][1]-pad[1][1])
                sy=abs(pad[7][2]-pad[3][2])
                #print r1,' ',sx-2*r1
            else: #vertical
                stop
                # sayerr('vertical')
                # #print pad[0][10].x
                # #print pad[2][10].x
                # px=(pad[0][10].x+pad[4][10].x)/2;
                # py=(pad[0][10].y+pad[4][10].y)/2;
                # sx=2*r1+abs(pad[3][1]-pad[3][3]); 
                # sy=2*r1+abs(pad[1][2]-pad[1][4])
            p_center=(px,py,0)
            #print px,' ',py
            #print sx,' ',sy
            rratio=r1/min(sx,sy)
            #Draft.makePoint(px,py, 0)
            # cx=(pad[0][1]+pad[0][3])/2;cy=(pad[1][2]+pad[1][4])/-2;sx=abs(pad[0][1]-pad[0][3])+2*pad[4][1];sy=abs(pad[1][2]-pad[1][4])+2*pad[4][1]
            # r=pad[4][1]
            # rratio=r/min(sx,sy)
            # #sayerr('center='+str(cx)+','+str(cy)+' size='+str(sx)+','+str(sy))
            # found_drill=False
            # r1=pad[0][1]; cx1=pad[0][2]; cy1=pad[0][3]
            # #print 'r1 ', r1, ' c1 ', cx1,',',cy1
            # r2=pad[2][1]; cx2=pad[2][2]; cy2=pad[2][3]
            # #print 'r2 ', r2, ' c2 ', cx2,',',cy2
            # #stop
            # if abs(cx1-cx2)>edge_tolerance: # horizontal
            #     sayerr('horizontal')
            #     px=(pad[0][10].x+pad[2][11].x)/2;py=(pad[0][11].y+pad[2][11].y)/-2;
            #     sx=2*r1+abs((pad[0][10].x-pad[2][11].x)); sy=2*r1
            # else: #vertical
            #     sayerr('vertical')
            #     px=(pad[0][10].x+pad[0][11].x)/2;py=(pad[0][10].y+pad[2][10].y)/-2;
            #     sx=2*r1; sy=2*r1+abs((pad[0][10].y-pad[2][10].y))
 
            found_drill=False
            if len(_drills)>0:
                for d in _drills:
                    #sayw(d)
                    if d[0] > px-sx/2 and d[0] < px+sx/2 and -d[1] > py-sy/2 and -d[1] < py+sy/2:
                        sayw('drill in pad found! '+str(d[0])+','+str(-d[1])+'/'+str(px)+','+str(py)+':'+str(sx)+','+str(sy))
                    #if d[0] > cx-sx/2 and d[0] < cx+sx/2 and d[1] > cy-sy/2 and d[1] < cy+sy/2:
                    #    sayw('drill in pad found!')
                        found_drill=True
                        break
                #drl_size=[d[2],d[3]]
                ### OFFSET
                if found_drill:
                    if d[2]!=d[3]:
                        drill_str="(drill oval "+"{0:.3f}".format(abs(d[2]))+" "+"{0:.3f}".format(abs(d[3])) #+")"
                    else:
                        drill_str="(drill "+"{0:.3f}".format(abs(d[2])) #+")"
                    if abs(d[0]-px)>edge_tolerance or abs(-d[1]-py)>edge_tolerance:
                        drill_str=drill_str+" (offset "+"{0:.3f}".format(px-d[0])+" "+"{0:.3f}".format(-py-d[1])+"))" #+")"
                        px=d[0];py=d[1]
                    else:
                        drill_str=drill_str+")"
                else:
                    pattern = '_In+([0-9]*?).Cu'
                    result = re.search(pattern, pad[0][-1])
                    if 'B_Cu' in pad[0][-1]:
                        pdLr='B.Cu'
                        ptp="smd"; pad_layers=" (layers B.Cu B.Paste B.Mask)"
                    elif result is not None:
                        pdLr=result.group().replace('_','.')[1:]
                        ptp="smd"; pad_layers=" (layers "+pdLr+")"
                    else:
                        pdLr='F.Cu'
                        ptp="smd"; pad_layers=" (layers F.Cu F.Paste F.Mask)"
                    #ptp="smd"; pad_layers=" (layers F.Cu F.Paste F.Mask)"
                    py=-py
                    drill_str="" #"(drill 0)"
            else:
                pattern = '_In+([0-9]*?).Cu'
                result = re.search(pattern, pad[0][-1])
                if 'B_Cu' in pad[0][-1]:
                    pdLr='B.Cu'
                    ptp="smd"; pad_layers=" (layers B.Cu B.Paste B.Mask)"
                elif result is not None:
                    pdLr=result.group().replace('_','.')[1:]
                    ptp="smd"; pad_layers=" (layers "+pdLr+")"
                else:
                    pdLr='F.Cu'
                    ptp="smd"; pad_layers=" (layers F.Cu F.Paste F.Mask)"
                #ptp="smd"; pad_layers=" (layers F.Cu F.Paste F.Mask)"
                py=-py
                drill_str="" #"(drill 0)"

            # if len(_drills)>0:
            #     for d in _drills:
            #         sayw(d)
            #         if d[0] > cx-sx/2 and d[0] < cx+sx/2 and d[1] > cy-sy/2 and d[1] < cy+sy/2:
            #             sayw('drill in pad found! '+str(d[0])+','+str(d[1])+'/'+str(cx)+','+str(cy)+':'+str(sx)+','+str(sy))
            #             found_drill=True
            #             ptp='thru_hole'
            #             p_layers='(layers *.Cu *.Mask)'
            #             break
            #     #drl_size=[d[2],d[3]]
            #     ### OFFSET
            #     if found_drill:
            #         if d[2]!=d[3]:
            #             drill_str="(drill oval "+str(d[2])+" "+str(d[3]) #+")"
            #         else:
            #             drill_str="(drill "+str(d[2]) #+")"
            #         if abs(d[0]-cx)>edge_tolerance or abs(d[1]-cy)>edge_tolerance:
            #             drill_str=drill_str+"(offset "+str(cx-d[0])+" "+str(cy-d[1])+"))" #+")"
            #             cx=d[0];cy=d[1]
            #         else:
            #             drill_str=drill_str+")"
            #     else:
            #         #drill_str="(drill 0)"
            #         ptp='smd'
            #         drill_str=""
            #         p_layers='(layers F.Cu F.Paste F.Mask)'
            # else:
            #     drill_str=""
            #     ptp='smd'
            #     p_layers='(layers F.Cu F.Paste F.Mask)'
            #rratio=0.25  ### TBD
            #pdl ="  (pad "+str(pad_nbr)+" "+ptp+" roundrect (at "+str(cx)+" "+str(cy)+") (size "+\
            pdl ="  (pad "+padNbr+" "+ptp+" roundrect (at "+"{0:.3f}".format(px)+" "+"{0:.3f}".format(py)+") (size "+\
                 "{0:.3f}".format(sx)+" "+"{0:.3f}".format(sy)+") "+drill_str+" "+pad_layers+" (roundrect_rratio "+"{0:.3f}".format(rratio)+"))" #+str(rratio)+"))"
            #pdl ="  (pad "+str(pad_nbr)+" thru_hole rect (at "+str(px)+" "+str(py)+") (size "+str(sx)+" "+str(sy)+") (layers F.Cu F.Paste F.Mask))"
            pad_nbr=pad_nbr+1
            #say(pad);sayw(pdl)
            return pdl
    ##--------------------------------------------##
    #elif tp=='RoundRect':
    #    found_drill=False
    #    if pad[0][0]=='line':
    #        #say(_drills)
    #        sayerr('round rect pad nbr.'+str(pad_nbr))
    #        cx=(pad[0][1]+pad[0][3])/2;cy=(pad[1][2]+pad[1][4])/-2;sx=abs(pad[0][1]-pad[0][3])+2*pad[4][1];sy=abs(pad[1][2]-pad[1][4])+2*pad[4][1]
    #        r=pad[4][1]
    #        rratio=r/min(sx,sy)
    #        #sayerr('center='+str(cx)+','+str(cy)+' size='+str(sx)+','+str(sy))
    #        found_drill=False
    #        if len(_drills)>0:
    #            for d in _drills:
    #                if d[0] > cx-sx/2 and d[0] < cx+sx/2 and d[1] > cy-sy/2 and d[1] < cy+sy/2:
    #                    sayw('drill in pad found! '+str(d[0])+','+str(d[1])+'/'+str(cx)+','+str(cy)+':'+str(sx)+','+str(sy))
    #                    found_drill=True
    #                    ptp='thru_hole'
    #                    p_layers='(layers *.Cu *.Mask)'
    #                    break
    #            #drl_size=[d[2],d[3]]
    #            ### OFFSET
    #            if found_drill:
    #                if d[2]!=d[3]:
    #                    drill_str="(drill oval "+str(d[2])+" "+str(d[3]) #+")"
    #                else:
    #                    drill_str="(drill "+str(d[2]) #+")"
    #                if abs(d[0]-cx)>edge_tolerance or abs(d[1]-cy)>edge_tolerance:
    #                    drill_str=drill_str+" (offset "+str(cx-d[0])+" "+str(cy-d[1])+"))" #+")"
    #                    cx=d[0];cy=d[1]
    #                else:
    #                    drill_str=drill_str+")"
    #            else:
    #                #drill_str="(drill 0)"
    #                ptp='smd'
    #                drill_str=""
    #                p_layers='(layers F.Cu F.Paste F.Mask)'
    #        else:
    #            drill_str=""
    #            ptp='smd'
    #            p_layers='(layers F.Cu F.Paste F.Mask)'
    #        #rratio=0.25  ### TBD
    #        #pdl ="  (pad "+str(pad_nbr)+" "+ptp+" roundrect (at "+str(cx)+" "+str(cy)+") (size "+\
    #        pdl ="  (pad # "+ptp+" roundrect (at "+str(cx)+" "+str(cy)+") (size "+\
    #             str(sx)+" "+str(sy)+") "+drill_str+" "+p_layers+"(roundrect_rratio "+str(rratio)+"))"
    #        #pdl ="  (pad "+str(pad_nbr)+" thru_hole rect (at "+str(px)+" "+str(py)+") (size "+str(sx)+" "+str(sy)+") (layers F.Cu F.Paste F.Mask))"
    #        pad_nbr=pad_nbr+1
    #        #say(pad);sayw(pdl)
    #        return pdl
    ##--------------------------------------------##
    elif tp=='FZ_Mask_Poly':
        found_drill=False
        wr=[]
        pad_ref="  (pad # smd custom (at 0 0 ) (size 0.1 0.1) (layers F.Mask)"+os.linesep
        pad_ref=pad_ref+"    (zone_connect 0)"+os.linesep
        pad_ref=pad_ref+"    (options (clearance outline) (anchor circle))"+os.linesep
        pad_ref=pad_ref+"    (primitives"+os.linesep
        #pad_ref=pad_ref+"      (gr_poly"
       
        if pad[0][0]=='line':
            #sayw(pad)
            pts="      (gr_poly (pts"+os.linesep
            segments_nbr=len(pad)
            i=1
            #for lines in pad:
            #    #if i<segments_nbr:
            #    #    pts=pts+"         (xy "+str(lines[1])+" "+str(-1*lines[2])+") (xy "+str(lines[3])+" "+str(-1*lines[4])+")"+os.linesep
            #    #else:
            #    #    pts=pts+"         (xy "+str(lines[1])+" "+str(-1*lines[2])+")) (width 0))"+os.linesep
            #    #wr.append(Part.makeLine((lines[1], lines[2],0.0),(lines[3], lines[4],0.0)))
            #    i=i+1
            #ant=Part.Wire(wr)
            ##sayw( ant.isClosed() )
            ##Part.show(ant)
            #face = Part.Face(ant)
            #Part.show(face)
            #shpName=FreeCAD.ActiveDocument.ActiveObject.Name
            ##say( FreeCAD.ActiveDocument.ActiveObject.Label)
            #shape= FreeCAD.ActiveDocument.ActiveObject.Shape
            i=1
            for lines in pad:
                if i<segments_nbr:
                    pts=pts+"         (xy "+"{0:.3f}".format(lines[1])+" "+"{0:.3f}".format(-1*lines[2])+") (xy "+"{0:.3f}".format(lines[3])+" "+"{0:.3f}".format(-1*lines[4])+")"+os.linesep
                else:
                    pts=pts+"         (xy "+"{0:.3f}".format(lines[1])+" "+"{0:.3f}".format(-1*lines[2])+")) (width 0))"+os.linesep
                i=i+1
            #pad_ref="  (pad "+str(pad_nbr)+" smd custom (at "+str(d[0])+" "+str(d[1])+" ) (size "+str(d[2])+" "+str(d[2])+") (layers F.Cu F.Paste F.Mask)"+os.linesep
            # pad_ref="  (pad # smd custom (at "+str(0.0)+" "+str(0.0)+" ) (size "+str(0)+" "+str(0)+") (layers F.Cu F.Paste F.Mask)"+os.linesep
            # pad_ref=pad_ref+"    (zone_connect 0)"+os.linesep
            # pad_ref=pad_ref+"    (options (clearance outline) (anchor circle))"+os.linesep
            # pad_ref=pad_ref+"    (primitives"+os.linesep
            #pad_ref=pad_ref+"    (gr_poly (pts"+os.linesep
            pad_ref=pad_ref+pts
            pad_ref=pad_ref+"    ))"+os.linesep
            #sayerr(pad_ref)
            pad_nbr=pad_nbr+1
            found_drill=False
            #Part.show(face)
              #(pad 1 smd custom (at 1 2) (size 0.2 0.2) (layers F.Cu F.Paste F.Mask)
              #(zone_connect 0)
              #(options (clearance outline) (anchor circle))
              #(primitives
              #(gr_poly (pts
              #    (xy -3.0 1.0) (xy -4.0 1.0) (xy -3.0 -2.0) (xy -0.5 -2.0) (xy 1.0 -4.0)
              #    (xy 4.0 -2.0) (xy 5.0 2.0) (xy 1.0 3.0)) (width 0))
              #))
            #sayerr(pts)
            
            #say(_drills)
            # sayerr('poly rect pad nbr.'+str(pad_nbr))
            # p1=(pad[0][1],pad[0][2]);p2=(pad[0][3]+pad[0][4])
            # sayerr('segment='+p1+','+p2
            # found_drill=False
            # if len(_drills)>0:
            #     for d in _drills:
            #         if d[0] > cx-sx/2 and d[0] < cx+sx/2 and d[1] > cy-sy/2 and d[1] < cy+sy/2:
            #             sayw('drill in pad found! '+str(d[0])+','+str(d[1])+'/'+str(cx)+','+str(cy)+':'+str(sx)+','+str(sy))
            #             found_drill=True
            #             ptp='thru_hole'
            #             p_layers='(layers *.Cu *.Mask)'
            #             break
            #     #drl_size=[d[2],d[3]]
            #     ### OFFSET
            #     if found_drill:
            #         if d[2]!=d[3]:
            #             drill_str="(drill oval "+str(d[2])+" "+str(d[3]) #+")"
            #         else:
            #             drill_str="(drill "+str(d[2]) #+")"
            #         if abs(d[0]-cx)>edge_tolerance or abs(d[1]-cy)>edge_tolerance:
            #             drill_str=drill_str+" (offset "+str(cx-d[0])+" "+str(cy-d[1])+"))" #+")"
            #             cx=d[0];cy=d[1]
            #         else:
            #             drill_str=drill_str+")"
            #     else:
            #         #drill_str="(drill 0)"
            #         ptp='smd'
            #         drill_str=""
            #         p_layers='(layers F.Cu F.Paste F.Mask)'
            # else:
            #     drill_str=""
            #     ptp='smd'
            #     p_layers='(layers F.Cu F.Paste F.Mask)'
            # #rratio=0.25  ### TBD
            # pdl ="  (pad "+str(pad_nbr)+" "+ptp+" roundrect (at "+str(cx)+" "+str(cy)+") (size "+\
            #      str(sx)+" "+str(sy)+") "+drill_str+" "+p_layers+"(roundrect_rratio "+str(rratio)+"))"
            # #pdl ="  (pad "+str(pad_nbr)+" thru_hole rect (at "+str(px)+" "+str(py)+") (size "+str(sx)+" "+str(sy)+") (layers F.Cu F.Paste F.Mask))"
            # pad_nbr=pad_nbr+1
            # say(pad);sayw(pdl)
            # return pdl
            return pad_ref
###
    elif 'NetTie_Poly' in tp: #accepting with or without reference pad
        found_drill=False
        wr=[]
        if pad[0][0]=='line':
            #sayw(pad)
            pts="      (fp_poly (pts"+os.linesep
            segments_nbr=len(pad)
            i=1
            layers = []
            #print(len(pad))
            padNbr='"#"'
            for lines in pad:
                #if i<segments_nbr:
                #    pts=pts+"         (xy "+str(lines[1])+" "+str(-1*lines[2])+") (xy "+str(lines[3])+" "+str(-1*lines[4])+")"+os.linesep
                #else:
                #    pts=pts+"         (xy "+str(lines[1])+" "+str(-1*lines[2])+")) (width 0))"+os.linesep
                wr.append(Part.makeLine((lines[1], lines[2],0.0),(lines[3], lines[4],0.0)))
                pattern = '_In+([0-9]*?).Cu'
                result = re.search(pattern, lines[5])
                if 'B_Cu' in lines[5]:
                    layers.append('Poly_B_Cu')
                elif result is not None:
                    layers.append('Poly'+result.group())
                else:
                    layers.append('Poly_F_Cu')
                if '_padNbr=' in lines[5]:
                    padNbr='"'+lines[5][lines[5].index('_padNbr='):].replace('_padNbr=','').replace('_','')+'"'
                elif '_padNum=' in lines[5]:
                    padNbr='"'+lines[5][lines[5].index('_padNum='):].replace('_padNum=','').replace('_','')+'"'
                else:
                    padNbr='"#"'
                i=i+1
            ant=Part.Wire(wr)
            #sayw( ant.isClosed() )
            #Part.show(ant)
            
            face = Part.Face(ant)
            Part.show(face)
            shpName=FreeCAD.ActiveDocument.ActiveObject.Name
            #say( FreeCAD.ActiveDocument.ActiveObject.Label)
            shape= FreeCAD.ActiveDocument.ActiveObject.Shape
            if len(_drills)>0:
                for d in _drills:
                    #print d
                    point=FreeCAD.Vector(d[0],-1*d[1],0)
                    if shape.isInside(point,0,True):
                        sayw('pad in poly found! '+str(d[0])+','+str(-1*d[1]))
                        found_drill=True
                        break
            #stop
            #if 1:
            FreeCAD.ActiveDocument.removeObject(shpName)
            if 1: #if found_drill:
                #print(len(ant.Wires))
                i=1
                for w in ant.Wires:
                    pattern = '_In+([0-9]*?)_Cu'
                    result = re.search(pattern, layers[i])
                    add_maskLayer = True
                    if 'B_Cu' in layers[i]:
                        padLayer = 'B.Cu'
                    elif result is not None:
                        padLayer = result.group().replace('_Cu','.Cu')[1:]
                        # print(padLayer)
                        add_maskLayer = False
                    else:
                        padLayer = 'F.Cu'
                    i=i+1
                    clusters = Part.sortEdges(w.Edges) #[0] 
                    #print(len(clusters))
                    for cluster in clusters:
                        #print(len(cluster))
                        for i,e in enumerate(cluster): #w.Edges):
                            if i < len(cluster)-1: 
                                #if (e.Vertexes[0].X == clusters[i-1].Vertexes[0].X) and (e.Vertexes[0].Y == clusters[i-1].Vertexes[0].Y):
                                    #pts=pts+"         (xy "+str(e.Vertexes[0].X)+" "+str(-1*(e.Vertexes[0].Y))+") (xy "+str(e.Vertexes[1].X)+" "+str(-1*(e.Vertexes[1].Y))+")"+os.linesep
                                    pts=pts+"         (xy "+"{0:.3f}".format(e.Vertexes[0].X)+" "+"{0:.3f}".format(-1*(e.Vertexes[0].Y))+") (xy "+"{0:.3f}".format(e.Vertexes[1].X)+" "+"{0:.3f}".format(-1*(e.Vertexes[1].Y))+")"+os.linesep
                                    #float("{0:.3f}".format(value))
                                #else:
                                #   pts=pts+"         (xy "+str(e.Vertexes[1].X)+" "+str(-1*(e.Vertexes[1].Y))+") (xy "+str(e.Vertexes[0].X)+" "+str(-1*(e.Vertexes[0].Y))+")"+os.linesep
                            else:
                                #"{0:.3f}".format(
                                pts=pts+"         (xy "+"{0:.3f}".format(e.Vertexes[0].X)+" "+"{0:.3f}".format(-1*(e.Vertexes[0].Y))+")) (layer "+padLayer+") (width 0))"+os.linesep
                                #pts=pts+"         (xy "+str(e.Vertexes[0].X)+" "+str(-1*(e.Vertexes[0].Y))+")) (layer "+padLayer+") (width 0))"+os.linesep
                #i=1
                #for lines in pad:
                #    if i<segments_nbr:
                #        #pts=pts+"         (xy "+str(lines[1]-d[0])+" "+str(-1*lines[2]-d[1])+") (xy "+str(lines[3]-d[0])+" "+str(-1*lines[4]-d[1])+")"+os.linesep
                #        pts=pts+"         (xy "+str(lines[1])+" "+str(-1*lines[2])+") (xy "+str(lines[3])+" "+str(-1*lines[4])+")"+os.linesep
                #    else:
                #        #pts=pts+"         (xy "+str(lines[1]-d[0])+" "+str(-1*lines[2]-d[1])+")) (width 0))"+os.linesep
                #        pts=pts+"         (xy "+str(lines[1])+" "+str(-1*lines[2])+")) (layer F.Cu) (width 0))"+os.linesep
                #    i=i+1
                #sh=sketch.Shape
                #ws=sh.Wires 
                #for e in w.Edges:
                #    print (e.Vertexes[0].X,e.Vertexes[0].Y)
                ##for i,w in enumerate(ant):
                ##    if i< len(ant)-1: #segments_nbr-1:
                ##        #pts=pts+"         (xy "+str(lines[1]-d[0])+" "+str(-1*lines[2]-d[1])+") (xy "+str(lines[3]-d[0])+" "+str(-1*lines[4]-d[1])+")"+os.linesep
                ##        if i>1:
                ##            if (lines[1] == pad[i-1][1]) and (lines[2] == pad[i-1][2]):
                ##                pts=pts+"         (xy "+str(lines[1])+" "+str(-1*lines[2])+") (xy "+str(lines[3])+" "+str(-1*lines[4])+")"+os.linesep
                ##            else:
                ##                pts=pts+"         (xy "+str(lines[3])+" "+str(-1*lines[4])+") (xy "+str(lines[1])+" "+str(-1*lines[2])+")"+os.linesep
                ##        else:
                ##            pts=pts+"         (xy "+str(lines[1])+" "+str(-1*lines[2])+") (xy "+str(lines[3])+" "+str(-1*lines[4])+")"+os.linesep
                ##    else:
                ##        #pts=pts+"         (xy "+str(lines[1]-d[0])+" "+str(-1*lines[2]-d[1])+")) (width 0))"+os.linesep
                ##        pts=pts+"         (xy "+str(lines[1])+" "+str(-1*lines[2])+")) (layer F.Cu) (width 0))"+os.linesep
                    #i=i+1
                
                #for i,lines in enumerate(pad):
                #    if i<segments_nbr-1:
                #        #pts=pts+"         (xy "+str(lines[1]-d[0])+" "+str(-1*lines[2]-d[1])+") (xy "+str(lines[3]-d[0])+" "+str(-1*lines[4]-d[1])+")"+os.linesep
                #        if i>1:
                #            if (lines[1] == pad[i-1][1]) and (lines[2] == pad[i-1][2]):
                #                pts=pts+"         (xy "+str(lines[1])+" "+str(-1*lines[2])+") (xy "+str(lines[3])+" "+str(-1*lines[4])+")"+os.linesep
                #            else:
                #                pts=pts+"         (xy "+str(lines[3])+" "+str(-1*lines[4])+") (xy "+str(lines[1])+" "+str(-1*lines[2])+")"+os.linesep
                #        else:
                #            pts=pts+"         (xy "+str(lines[1])+" "+str(-1*lines[2])+") (xy "+str(lines[3])+" "+str(-1*lines[4])+")"+os.linesep
                #    else:
                #        #pts=pts+"         (xy "+str(lines[1]-d[0])+" "+str(-1*lines[2]-d[1])+")) (width 0))"+os.linesep
                #        pts=pts+"         (xy "+str(lines[1])+" "+str(-1*lines[2])+")) (layer F.Cu) (width 0))"+os.linesep
                #    #i=i+1
                if add_maskLayer:
                    pts = pts + pts.replace('.Cu','.Mask')
                #pad_ref="  (pad "+str(pad_nbr)+" smd custom (at "+str(d[0])+" "+str(d[1])+" ) (size "+str(d[2])+" "+str(d[2])+") (layers F.Cu F.Paste F.Mask)"+os.linesep
                if found_drill:
                    if add_maskLayer:
                        pad_ref="  (pad "+padNbr+" smd circle (at "+"{0:.3f}".format(d[0])+" "+"{0:.3f}".format(d[1])+" ) (size "+"{0:.3f}".format(d[2])+" "+"{0:.3f}".format(d[2])+") (layers "+padLayer+" "+padLayer.rstrip('Cu')+"Mask))"+os.linesep
                    else:
                        pad_ref="  (pad "+padNbr+" smd circle (at "+"{0:.3f}".format(d[0])+" "+"{0:.3f}".format(d[1])+" ) (size "+"{0:.3f}".format(d[2])+" "+"{0:.3f}".format(d[2])+") (layers "+padLayer+"))"+os.linesep
                    #if 0: #'B_Cu' in tp:
                    #    #pad_ref="  (pad # smd custom (at "+str("{0:.3f}".format(d[0]))+" "+str("{0:.3f}".format(d[1]))+" ) (size "+str("{0:.3f}".format(d[2]))+" "+str("{0:.3f}".format(d[2]))+") (layers B.Cu B.Paste B.Mask)"+os.linesep
                    #    pad_ref="  (pad # smd circle (at "+str("{0:.3f}".format(d[0]))+" "+str("{0:.3f}".format(d[1]))+" ) (size "+str("{0:.3f}".format(d[2]))+" "+str("{0:.3f}".format(d[2]))+") (layers B.Cu B.Mask))"+os.linesep
                    #else:
                    #    #pad_ref="  (pad # smd custom (at "+str("{0:.3f}".format(d[0]))+" "+str("{0:.3f}".format(d[1]))+" ) (size "+str("{0:.3f}".format(d[2]))+" "+str("{0:.3f}".format(d[2]))+") (layers F.Cu F.Paste F.Mask)"+os.linesep
                    #    pad_ref="  (pad # smd circle (at "+str("{0:.3f}".format(d[0]))+" "+str("{0:.3f}".format(d[1]))+" ) (size "+str("{0:.3f}".format(d[2]))+" "+str("{0:.3f}".format(d[2]))+") (layers F.Cu F.Mask))"+os.linesep
                else:
                    pad_ref=""
                # #pad_ref="  (pad # smd custom (at "+str("{0:.3f}".format(d[0]))+" "+str("{0:.3f}".format(d[1]))+" ) (size "+str("{0:.3f}".format(d[2]))+" "+str("{0:.3f}".format(d[2]))+") (layers F.Cu F.Paste F.Mask)"+os.linesep
                # pad_ref=pad_ref+"    (zone_connect 0)"+os.linesep
                # pad_ref=pad_ref+"    (options (clearance outline) (anchor circle))"+os.linesep
                # pad_ref=pad_ref+"    (primitives"+os.linesep
                # #pad_ref=pad_ref+"    (gr_poly (pts"+os.linesep
                #if pad_ref!="":
                #    pad_ref=pad_ref+pts
                #    pad_ref=pad_ref+"    ))"+os.linesep
                #else:
                #    pad_ref=pad_ref+pts+os.linesep
                pad_ref=pad_ref+pts+os.linesep
                    #sayerr(pad_ref)
                pad_nbr=pad_nbr+1
                found_drill=False
            else:
                sayw("missing reference pad for polyline pad")
                #stop
            return pad_ref
###
    #elif tp=='Poly':
    elif 'Poly' in tp: #NB after NetTie_Poly
        found_drill=False
        wr=[]
        if pad[0][0]=='line':
            #sayw(pad)
            pts="      (gr_poly (pts"+os.linesep
            segments_nbr=len(pad)
            i=1
            layers = []
            for lines in pad:
                #if i<segments_nbr:
                #    pts=pts+"         (xy "+str(lines[1])+" "+str(-1*lines[2])+") (xy "+str(lines[3])+" "+str(-1*lines[4])+")"+os.linesep
                #else:
                #    pts=pts+"         (xy "+str(lines[1])+" "+str(-1*lines[2])+")) (width 0))"+os.linesep
                wr.append(Part.makeLine((lines[1], lines[2],0.0),(lines[3], lines[4],0.0)))
                pattern = '_In+([0-9]*?).Cu'
                result = re.search(pattern, lines[5])
                if 'B_Cu' in lines[5]:
                    layers.append('Poly_B_Cu')
                elif result is not None:
                    layers.append('Poly'+result.group())
                else:
                    layers.append('Poly_F_Cu')
                if '_padNbr=' in lines[5]:
                    padNbr='"'+lines[5][lines[5].index('_padNbr='):].replace('_padNbr=','').replace('_','')+'"'
                elif '_padNum=' in lines[5]:
                    padNbr='"'+lines[5][lines[5].index('_padNum='):].replace('_padNum=','').replace('_','')+'"'
                else:
                    padNbr='"#"'
                i=i+1
            ant=Part.Wire(wr)
            #sayw( ant.isClosed() )
            #Part.show(ant)
            face = Part.Face(ant)
            Part.show(face)
            shpName=FreeCAD.ActiveDocument.ActiveObject.Name
            #say( FreeCAD.ActiveDocument.ActiveObject.Label)
            shape= FreeCAD.ActiveDocument.ActiveObject.Shape
            if len(_drills)>0:
                for d in _drills:
                    #print (d)
                    point=FreeCAD.Vector(d[0],-1*d[1],0)
                    if shape.isInside(point,0,True):
                        sayw('pad in poly found! '+str(d[0])+','+str(-1*d[1]))
                        found_drill=True
                        break
            FreeCAD.ActiveDocument.removeObject(shpName)
            #stop
            #if 1:
            if found_drill:
                i=1
                for w in ant.Wires:
                    pattern = '_In+([0-9]*?)_Cu'
                    result = re.search(pattern, layers[i])
                    clusters = Part.sortEdges(w.Edges) #[0] 
                    internalLayer = False
                    print(layers[i])
                    if 'B_Cu' in layers[i]:
                        padLayer = 'B.Cu'
                    elif result is not None:
                        padLayer = result.group().replace('_Cu','.Cu')[1:]
                        internalLayer = True
                    else:
                        padLayer = 'F.Cu'
                    i=i+1
                    #print(len(clusters))
                    for cluster in clusters:
                        #print(len(cluster))
                        for i,e in enumerate(cluster): #w.Edges):
                            if i < len(cluster)-1: 
                                #if (e.Vertexes[0].X == clusters[i-1].Vertexes[0].X) and (e.Vertexes[0].Y == clusters[i-1].Vertexes[0].Y):
                                    pts=pts+"         (xy "+"{0:.3f}".format(e.Vertexes[0].X-d[0])+" "+"{0:.3f}".format(-1*(e.Vertexes[0].Y)-d[1])+") (xy "+"{0:.3f}".format(e.Vertexes[1].X-d[0])+" "+"{0:.3f}".format(-1*(e.Vertexes[1].Y)-d[1])+")"+os.linesep
                                #else:
                                #   pts=pts+"         (xy "+str(e.Vertexes[1].X)+" "+str(-1*(e.Vertexes[1].Y))+") (xy "+str(e.Vertexes[0].X)+" "+str(-1*(e.Vertexes[0].Y))+")"+os.linesep
                            else:
                                pts=pts+"         (xy "+"{0:.3f}".format(e.Vertexes[0].X-d[0])+" "+"{0:.3f}".format(-1*(e.Vertexes[0].Y)-d[1])+")) (layer "+padLayer+") (width 0))"+os.linesep
                #pts = pts + pts.replace('F.Cu','F.Mask')
                #pad_ref="  (pad "+str(pad_nbr)+" smd custom (at "+str(d[0])+" "+str(d[1])+" ) (size "+str(d[2])+" "+str(d[2])+") (layers F.Cu F.Paste F.Mask)"+os.linesep
                if found_drill: #ref pad found
                    if internalLayer:
                        pad_ref="  (pad "+padNbr+" smd custom (at "+"{0:.3f}".format(d[0])+" "+"{0:.3f}".format(d[1])+" ) (size "+"{0:.3f}".format(d[2])+" "+"{0:.3f}".format(d[2])+") (layers "+padLayer+")"+os.linesep
                    else:
                        pad_ref="  (pad "+padNbr+" smd custom (at "+"{0:.3f}".format(d[0])+" "+"{0:.3f}".format(d[1])+" ) (size "+"{0:.3f}".format(d[2])+" "+"{0:.3f}".format(d[2])+") (layers "+padLayer+" "+padLayer.rstrip('Cu')+"Mask)"+os.linesep
                    
                    #if 'B_Cu' in lyr:
                    #    pad_ref="  (pad # smd custom (at "+str("{0:.3f}".format(d[0]))+" "+str("{0:.3f}".format(d[1]))+" ) (size "+str("{0:.3f}".format(d[2]))+" "+str("{0:.3f}".format(d[2]))+") (layers B.Cu B.Paste B.Mask)"+os.linesep
                    #    #pad_ref="  (pad # smd custom (at "+str("{0:.3f}".format(d[0]))+" "+str("{0:.3f}".format(d[1]))+" ) (size "+str("{0:.3f}".format(d[2]))+" "+str("{0:.3f}".format(d[2]))+") (layers B.Cu B.Mask)"+os.linesep
                    #else:
                    #    #pad_ref="  (pad # smd custom (at "+str("{0:.3f}".format(d[0]))+" "+str("{0:.3f}".format(d[1]))+" ) (size "+str("{0:.3f}".format(d[2]))+" "+str("{0:.3f}".format(d[2]))+") (layers F.Cu F.Paste F.Mask)"+os.linesep
                    #    pad_ref="  (pad # smd custom (at "+str("{0:.3f}".format(d[0]))+" "+str("{0:.3f}".format(d[1]))+" ) (size "+str("{0:.3f}".format(d[2]))+" "+str("{0:.3f}".format(d[2]))+") (layers F.Cu F.Mask)"+os.linesep
                #else:
                #    pad_ref=""
                # pad_ref=pad_ref+pts+os.linesep
                # #pad_ref="  (pad # smd custom (at "+str("{0:.3f}".format(d[0]))+" "+str("{0:.3f}".format(d[1]))+" ) (size "+str("{0:.3f}".format(d[2]))+" "+str("{0:.3f}".format(d[2]))+") (layers F.Cu F.Paste F.Mask)"+os.linesep
                pad_ref=pad_ref+"    (zone_connect 0)"+os.linesep
                pad_ref=pad_ref+"    (options (clearance outline) (anchor circle))"+os.linesep
                pad_ref=pad_ref+"    (primitives"+os.linesep
                # #pad_ref=pad_ref+"    (gr_poly (pts"+os.linesep
                #if pad_ref!="":
                pad_ref=pad_ref+pts
                pad_ref=pad_ref+"    ))"+os.linesep
                #pad_ref=pad_ref+pts+"    ))"+os.linesep
                    #sayerr(pad_ref)
                pad_nbr=pad_nbr+1
                found_drill=False
            else:
                sayw("missing reference pad for polyline pad")
                stop
            return pad_ref

            
            # if found_drill:
            #     i=1
            #     for lines in pad:
            #         if i<segments_nbr:
            #             pts=pts+"         (xy "+str(lines[1]-d[0])+" "+str(-1*lines[2]-d[1])+") (xy "+str(lines[3]-d[0])+" "+str(-1*lines[4]-d[1])+")"+os.linesep
            #         else:
            #             pts=pts+"         (xy "+str(lines[1]-d[0])+" "+str(-1*lines[2]-d[1])+")) (width 0))"+os.linesep
            #         i=i+1
            #     #pad_ref="  (pad "+str(pad_nbr)+" smd custom (at "+str(d[0])+" "+str(d[1])+" ) (size "+str(d[2])+" "+str(d[2])+") (layers F.Cu F.Paste F.Mask)"+os.linesep
            #     if 0: #'B_Cu' in tp:
            #         pad_ref="  (pad # smd custom (at "+str("{0:.3f}".format(d[0]))+" "+str("{0:.3f}".format(d[1]))+" ) (size "+str("{0:.3f}".format(d[2]))+" "+str("{0:.3f}".format(d[2]))+") (layers B.Cu B.Paste B.Mask)"+os.linesep
            #     else:
            #         pad_ref="  (pad # smd custom (at "+str("{0:.3f}".format(d[0]))+" "+str("{0:.3f}".format(d[1]))+" ) (size "+str("{0:.3f}".format(d[2]))+" "+str("{0:.3f}".format(d[2]))+") (layers F.Cu F.Paste F.Mask)"+os.linesep
            #     #pad_ref="  (pad # smd custom (at "+str("{0:.3f}".format(d[0]))+" "+str("{0:.3f}".format(d[1]))+" ) (size "+str("{0:.3f}".format(d[2]))+" "+str("{0:.3f}".format(d[2]))+") (layers F.Cu F.Paste F.Mask)"+os.linesep
            #     pad_ref=pad_ref+"    (zone_connect 0)"+os.linesep
            #     pad_ref=pad_ref+"    (options (clearance outline) (anchor circle))"+os.linesep
            #     pad_ref=pad_ref+"    (primitives"+os.linesep
            #     #pad_ref=pad_ref+"    (gr_poly (pts"+os.linesep
            #     pad_ref=pad_ref+pts
            #     pad_ref=pad_ref+"    ))"+os.linesep
            #     #sayerr(pad_ref)
            #     pad_nbr=pad_nbr+1
            #     found_drill=False
            # else:
            #     sayerr("missing reference pad for polyline pad")
            #     stop
            #Part.show(face)
              #(pad 1 smd custom (at 1 2) (size 0.2 0.2) (layers F.Cu F.Paste F.Mask)
              #(zone_connect 0)
              #(options (clearance outline) (anchor circle))
              #(primitives
              #(gr_poly (pts
              #    (xy -3.0 1.0) (xy -4.0 1.0) (xy -3.0 -2.0) (xy -0.5 -2.0) (xy 1.0 -4.0)
              #    (xy 4.0 -2.0) (xy 5.0 2.0) (xy 1.0 3.0)) (width 0))
              #))
            #sayerr(pts)
            
            #say(_drills)
            # sayerr('poly rect pad nbr.'+str(pad_nbr))
            # p1=(pad[0][1],pad[0][2]);p2=(pad[0][3]+pad[0][4])
            # sayerr('segment='+p1+','+p2
            # found_drill=False
            # if len(_drills)>0:
            #     for d in _drills:
            #         if d[0] > cx-sx/2 and d[0] < cx+sx/2 and d[1] > cy-sy/2 and d[1] < cy+sy/2:
            #             sayw('drill in pad found! '+str(d[0])+','+str(d[1])+'/'+str(cx)+','+str(cy)+':'+str(sx)+','+str(sy))
            #             found_drill=True
            #             ptp='thru_hole'
            #             p_layers='(layers *.Cu *.Mask)'
            #             break
            #     #drl_size=[d[2],d[3]]
            #     ### OFFSET
            #     if found_drill:
            #         if d[2]!=d[3]:
            #             drill_str="(drill oval "+str(d[2])+" "+str(d[3]) #+")"
            #         else:
            #             drill_str="(drill "+str(d[2]) #+")"
            #         if abs(d[0]-cx)>edge_tolerance or abs(d[1]-cy)>edge_tolerance:
            #             drill_str=drill_str+" (offset "+str(cx-d[0])+" "+str(cy-d[1])+"))" #+")"
            #             cx=d[0];cy=d[1]
            #         else:
            #             drill_str=drill_str+")"
            #     else:
            #         #drill_str="(drill 0)"
            #         ptp='smd'
            #         drill_str=""
            #         p_layers='(layers F.Cu F.Paste F.Mask)'
            # else:
            #     drill_str=""
            #     ptp='smd'
            #     p_layers='(layers F.Cu F.Paste F.Mask)'
            # #rratio=0.25  ### TBD
            # pdl ="  (pad "+str(pad_nbr)+" "+ptp+" roundrect (at "+str(cx)+" "+str(cy)+") (size "+\
            #      str(sx)+" "+str(sy)+") "+drill_str+" "+p_layers+"(roundrect_rratio "+str(rratio)+"))"
            # #pdl ="  (pad "+str(pad_nbr)+" thru_hole rect (at "+str(px)+" "+str(py)+") (size "+str(sx)+" "+str(sy)+") (layers F.Cu F.Paste F.Mask))"
            # pad_nbr=pad_nbr+1
            # say(pad);sayw(pdl)
            # return pdl
            #return pad_ref
##
    elif tp=='Pads_Geom':
        found_drill=False
        wr=[]
        if len(_drills)>0:
            for d in _drills:
                #print d
                sayw('drill found! '+str(d[0])+','+str(-1*d[1]))
                found_drill=True
                break
        if pad[0][0]=='line':
            sayw('line is not supported')
        elif pad[0][0]=='circle':
            print (pad)
            wd_=float(pad[0][4].split('_')[2])
            pts="      (gr_circle (center "+"{0:.3f}".format(pad[0][2]-d[0])+" "+"{0:.3f}".format(-1*pad[0][3]-d[1])+") (end "+"{0:.3f}".format(pad[0][2]-d[0]+pad[0][1])+" "+"{0:.3f}".format(-1*pad[0][3]-d[1])+") (width "+"{0:.3f}".format(wd_)+"))"+os.linesep
            say(pts)
            if found_drill:
                #pad_ref="  (pad "+str(pad_nbr)+" smd custom (at "+str(d[0])+" "+str(d[1])+" ) (size "+str(d[2])+" "+str(d[2])+") (layers F.Cu F.Paste F.Mask)"+os.linesep
                if 0: #'B_Cu' in tp:
                    pad_ref="  (pad # smd custom (at "+str("{0:.3f}".format(d[0]))+" "+str("{0:.3f}".format(d[1]))+" ) (size "+str(d[2])+" "+str(d[2])+") (layers B.Cu B.Paste B.Mask)"+os.linesep
                else:
                    pad_ref="  (pad # smd custom (at "+str("{0:.3f}".format(d[0]))+" "+str("{0:.3f}".format(d[1]))+" ) (size "+str(d[2])+" "+str(d[2])+") (layers F.Cu F.Paste F.Mask)"+os.linesep
                pad_ref=pad_ref+"    (zone_connect 0)"+os.linesep
                pad_ref=pad_ref+"    (options (clearance outline) (anchor circle))"+os.linesep
                pad_ref=pad_ref+"    (primitives"+os.linesep
                #pad_ref=pad_ref+"    (gr_poly (pts"+os.linesep
                pad_ref=pad_ref+pts
                pad_ref=pad_ref+"    ))"+os.linesep
                #sayerr(pad_ref)
                pad_nbr=pad_nbr+1
                found_drill=False
            else:
                sayerr("missing reference pad for polyline pad")
                stop
            return pad_ref
    else:
        return u''
    pass


###

def getBoardOutline():
    global edge_tolerance, maxRadius, maxSegments
    global dvm, dqd, precision
    
    use_discretize = False # discretize or toBiArc method for Ellipses and parabola and Hyperbola
    
    if not FreeCAD.activeDocument():
        return False
    #
    doc = FreeCAD.activeDocument()
    outline = []
    #to_discretize=[[]] * 2 #[[][]]
    to_discretize=[]
    construction_geom=[]
    not_supported = ''
    
    sel = FreeCADGui.Selection.getSelection()
    if len (sel) >0:
        #sayw(doc.Name)
        for j in sel:
        #for j in doc.Objects:
            sayerr(j.Name)
            #sayw(j.Geometry)
            
            #if hasattr(j, "Proxy") and hasattr(j.Proxy, "Type") and j.Proxy.Type == "PCBboard":
            ##if hasattr(j, "Geometry"):
            if "Sketch" in j.TypeId:
                try:
                    #print j.Geometry
                    for k in range(len(j.Geometry)):
                        #print(type(j.Geometry[k]).__name__)
                        bezier_list  = []
                        bezier_list_tmp  = []
                        if hasattr(j,'GeometryFacadeList'):
                            Gm = j.GeometryFacadeList
                        else:
                            Gm = j.Geometry
                        #if hasattr(Gm[k],'Construction'):
                        if isConstruction(Gm[k]):
                            #if Gm[k].Construction:
                            construction_geom.append(k)
                            sayw('construction skipped')
                            continue
                        if 'Point' in type(j.Geometry[k]).__name__:  #skipping points
                            sayw('point skipped')
                            #sayerr('point')
                            continue
                        #if type(j.Geometry[k]).__name__ == 'LineSegment':
                        if 'LineSegment' in type(j.Geometry[k]).__name__:
                        #if 'Line' in type(j.Geometry[k]).__name__:
                            sk_ge=j.Geometry[k].toShape() #needed to fix some issue on sketch geometry building
                            outline.append([
                                'line',
                                sk_ge.Edges[0].Vertexes[0].Point.x,
                                sk_ge.Edges[0].Vertexes[0].Point.y,
                                sk_ge.Edges[0].Vertexes[1].Point.x,
                                sk_ge.Edges[0].Vertexes[1].Point.y,
                                j.Label
                            ])
                            # outline.append([
                            #     'line',
                            #     j.Geometry[k].StartPoint.x,
                            #     j.Geometry[k].StartPoint.y,
                            #     j.Geometry[k].EndPoint.x,
                            #     j.Geometry[k].EndPoint.y
                            # ])
                        #elif type(j.Geometry[k]).__name__ == 'Circle':
                        elif 'Circle' in type(j.Geometry[k]).__name__ and not 'ArcOfCircle' in type(j.Geometry[k]).__name__:
                            sk_ge=j.Geometry[k].toShape()  #needed to fix some issue on sketch geometry building
                            outline.append([
                                'circle',
                                sk_ge.Edges[0].Curve.Radius,
                                sk_ge.Edges[0].Curve.Center.x,
                                sk_ge.Edges[0].Curve.Center.y,
                                j.Label
                            ])
                            # outline.append([
                            #     'circle',
                            #     j.Geometry[k].Radius,
                            #     j.Geometry[k].Center.x, 
                            #     j.Geometry[k].Center.y
                            # ])
                        #elif type(j.Geometry[k]).__name__ == 'ArcOfCircle':
                        #elif isinstance(j.Geometry[k].Curve,Part.Circle)
                        elif 'ArcOfCircle' in type(j.Geometry[k]).__name__:
                            #if isinstance(j.Shape.Edges[k].Curve,Part.Circle):
                            #sayw(type(j.Geometry[k]))
                            #sayerr(j.Shape.Edges[k].Curve)
                            sk_ge=j.Geometry[k].toShape() #needed to fix some issue on sketch geometry building
                            outline.append([
                                'arc',
                                j.Geometry[k].Radius, 
                                sk_ge.Edges[0].Curve.Center.x,
                                sk_ge.Edges[0].Curve.Center.y,
                                j.Geometry[k].FirstParameter, 
                                j.Geometry[k].LastParameter,
                                j.Geometry[k].Axis[0],
                                j.Geometry[k].Axis[1],
                                j.Geometry[k].Axis[2],
                                j.Geometry[k],
                                sk_ge.Edges[0].Vertexes[0].Point,
                                sk_ge.Edges[0].Vertexes[1].Point,
                                sk_ge.Edges[0].Orientation,
                                j.Label
                            ])
                            
                            ##j.Geometry[k].Center.x, 
                            ##j.Geometry[k].Center.y, 
                                
                            # i=j.Geometry[k]
                            # sayerr('Xaxis1a')
                            # if 0: #i.XAxis.x < 0:   ## da cambiare this is not available on FC0.16
                            #     sayerr('Xaxis1b')
                            #     outline.append([
                            #         'arc',
                            #         i.Radius, 
                            #         i.Center.x, 
                            #         i.Center.y, 
                            #         i.LastParameter+pi,
                            #         i.FirstParameter+pi, 
                            #         -i.Axis[0],
                            #         i.Axis[1],
                            #         i.Axis[2],
                            #         i
                            #     ])
                            # else:
                            #     outline.append([
                            #         'arc',
                            #         i.Radius, 
                            #         i.Center.x, 
                            #         i.Center.y, 
                            #         i.LastParameter,
                            #         i.FirstParameter+pi, 
                            #         i.Axis[0],
                            #         i.Axis[1],
                            #         i.Axis[2],
                            #         i
                            #     ])
                        elif (accept_spline) and ('BSplineCurve' in type(j.Geometry[k]).__name__):
                            bs = j.Geometry[k]
                            # Set degree
                            #maxDegree = 3 #kicad max degree of splines
                            if bs.Degree < maxDegree:
                                bs.increaseDegree(maxDegree)
                            elif bs.Degree > maxDegree:
                                # degree too high. We need to approximate the curve
                                bs = bs.approximateBSpline(edge_tolerance,maxSegments,maxDegree) # (tolerance, maxSegments, maxDegree)
                                # Generate to a list of bezier curves
                            bezier_list.extend(bs.toBezier())  # Generate to a list of bezier curves, these are of 4 poles
                            for bc in bezier_list:
                                print("%s (degree : %d / nb poles : %d)"%(bc, bc.Degree, bc.NbPoles))
                                # poles = bc.getPoles()
                                # spline=Part.BSplineCurve()
                                # spline.buildFromPoles(poles, False, 3)
                                #kicadGeo.append(spline)
                                #print(poles)
                                outline.append([
                                    'spline',
                                    bc.getPole(1).x,
                                    bc.getPole(1).y,
                                    bc.getPole(2).x,
                                    bc.getPole(2).y,
                                    bc.getPole(3).x,
                                    bc.getPole(3).y,
                                    bc.getPole(4).x,
                                    bc.getPole(4).y,
                                    j.Label
                                ])
                                #print(outline)
                        # elif (use_discretize) and (accept_spline) and ('Parabola' in type(j.Geometry[k]).__name__ or 'Hyperbola' in type(j.Geometry[k]).__name__\
                        #      or 'Ellipse' in type(j.Geometry[k]).__name__): 
                        elif (accept_spline) and ('Parabol' in type(j.Geometry[k]).__name__ or 'Hyperbol' in type(j.Geometry[k]).__name__): 
                        ## discretizing
                         # or 'Ellipse' in type(j.Geometry[k]).__name__  ## Ellipses are not well approximated by Splines
                            gd = j.Geometry[k]
                            gds = gd.toShape()
                            pl = gds.discretize(QuasiDeflection=dqd)
                            #pl = gds.discretize(QuasiDeflection=1.0)
                            w = Part.makePolygon(pl)
                            wv = w.Vertexes
                            for i in range(0,len(wv), 1):
                            #for v in wv:
                                if i < len(wv)-1:
                                    v1x = wv[i].Point.x
                                    v1y = wv[i].Point.y
                                    v2x = wv[i+1].Point.x
                                    v2y = wv[i+1].Point.y
                                elif 'Arc' not in str(gd):
                                    v1x = wv[i].Point.x
                                    v1y = wv[i].Point.y
                                    v2x = wv[0].Point.x
                                    v2y = wv[0].Point.y
                                    #print('last point',v1x,v1y,v2x,v2y)
                                #i+=2
                                outline.append([
                                    'line',
                                    v1x,
                                    v1y,
                                    v2x,
                                    v2y,
                                    j.Label,
                                ])    
                                #print(v1x,v1y,v2x,v2y,i)
                        # elif (not use_discretize) and (accept_spline) and ('Parabola' in type(j.Geometry[k]).__name__ or 'Hyperbola' in type(j.Geometry[k]).__name__\
                        #      or 'Ellipse' in type(j.Geometry[k]).__name__): 
                        elif (not use_discretize) and (accept_spline) and ('Ellipse' in type(j.Geometry[k]).__name__): 
                        ## toBiArcs 
                         # or 'Ellipse' in type(j.Geometry[k]).__name__  ## Ellipses are not well approximated by Splines
                            gk = j.Geometry[k]
                            bs = gk.toBSpline() # (tolerance, maxSegments, maxDegree)
                            gds = bs.toBiArcs(precision)
                            # import kicadStepUptools; import importlib; importlib.reload(kicadStepUptools) 
                            #;kicadStepUptools.open(u"C:/Temp/bspline.kicad_pcb")
                            #for g in gds:
                            #    print(str(g))
                            #stop
                            for g in gds:
                                # s = g.toShape() #needed to fix some issue on sketch geometry building
                                # outline.append([
                                #     'arc',
                                #     g.Radius, 
                                #     s.Edges[0].Curve.Center.x,
                                #     s.Edges[0].Curve.Center.y,
                                #     g.FirstParameter, 
                                #     g.LastParameter,
                                #     g.Axis[0],
                                #     g.Axis[1],
                                #     g.Axis[2],
                                #     g,
                                #     s.Edges[0].Vertexes[0].Point,
                                #     s.Edges[0].Vertexes[1].Point,
                                #     s.Edges[0].Orientation,
                                #     j.Label
                                # ])                                
                                # #Part.show(s)
                                outline.append([
                                    'arc',
                                    g.Radius, 
                                    g.Center.x,
                                    g.Center.y,
                                    g.FirstParameter, 
                                    g.LastParameter,
                                    g.Axis[0],
                                    g.Axis[1],
                                    g.Axis[2],
                                    g,
                                    g.StartPoint,
                                    g.EndPoint,
                                    'Forward',
                                    j.Label
                                ])

                        #elif (accept_spline) and ('Parabola' in type(j.Geometry[k]).__name__ or 'Hyperbola' in type(j.Geometry[k]).__name__): 
                        # # or 'Ellipse' in type(j.Geometry[k]).__name__  ## Ellipses are not well approximated by Splines
                        #    bs = j.Geometry[k]
                        #    bs = bs.approximateBSpline(edge_tolerance,maxSegment,maxDegree) # (tolerance, maxSegments, maxDegree) 
                        #    bezier_list_tmp.extend(bs.toBezier()) 
                        #    tmpGeo = []
                        #    for bc in bezier_list_tmp:
                        #        print("%s (degree : %d / nb poles : %d)"%(bc, bc.Degree, bc.NbPoles))
                        #        poles = bc.getPoles()
                        #        spline=Part.BSplineCurve()
                        #        spline.buildFromPoles(poles, False, 3)
                        #        tmpGeo.append(spline)
                        #    print('double rework for Ellipses and Parabola and Hyperbola')
                        #    bezier_list_tmp = []
                        #    for g in tmpGeo:
                        #        if 'BSplineCurve object' in str(g):
                        #            bs = g
                        #            if bs.Degree < maxDegree:
                        #                bs.increaseDegree(maxDegree)
                        #            elif bs.Degree > maxDegree:
                        #                # degree too high. We need to approximate the curve
                        #                bs = bs.approximateBSpline(edge_tolerance,maxSegments,maxDegree) # (tolerance, maxSegments, maxDegree)
                        #            bezier_list_tmp.extend(bs.toBezier())  # Generate to a list of bezier curves, these are of 4 poles
                        #    for bc in bezier_list_tmp:
                        #        print("%s (degree : %d / nb poles : %d)"%(bc, bc.Degree, bc.NbPoles))
                        #        poles = bc.getPoles()
                        #        #spline=Part.BSplineCurve()
                        #        #spline.buildFromPoles(poles, False, 3)
                        #        outline.append([
                        #            'spline',
                        #            bc.getPole(1).x,
                        #            bc.getPole(1).y,
                        #            bc.getPole(2).x,
                        #            bc.getPole(2).y,
                        #            bc.getPole(3).x,
                        #            bc.getPole(3).y,
                        #            bc.getPole(4).x,
                        #            bc.getPole(4).y,
                        #            j.Label
                        #        ])
                        else:  ## dropped ... it shouldn't arrive here
                            #print j.Geometry[k],'; not supported'
                            to_discretize.append(k)  #to_discretize.append(k, j.Label)
                            str_geom=str(j.Geometry[k])
                            if 'ArcOfEllipse' in str_geom:
                                str_geom='ArcOfEllipse'
                            elif 'ArcOfParabola' in str_geom:
                                str_geom='ArcOfParabola'
                            elif 'ArcOfHyperbola' in str_geom:
                                str_geom='ArcOfHyperbola'
                            if str_geom not in not_supported:
                                if 'Vector' not in str_geom:
                                    not_supported=not_supported + str_geom.strip('<').strip('>').strip(' object')+'; '
                            #continue
                    ##break
                except Exception as e:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    FreeCAD.Console.PrintWarning('1. ' + str(e) + "\n")
                    FreeCAD.Console.PrintWarning('error class: '+str(exc_type)+'\nfile name: '+str(fname)+'\nerror @line: '+str(exc_tb.tb_lineno)+'\nerror value: '+str(e.args[0])+'\n')
    # print (to_discretize)
    # stop
    return outline, not_supported, to_discretize, construction_geom
##


def createEdge(edg,ofs,sklayer=None,pcb_ver=None):
    global edge_width, maxRadius
    
    #print edg
    k_edg=''
    if edge_width is None:
        edge_width=0.16
    #def getMinX(self, x):
    #    if x < self.minX:
    #        self.minX = x
    #        
    #def getMinY(self, y):
    #    if y < self.minY:
    #        self.minY = y

    if sklayer is None:
        layer='Edge.Cuts'
    else:
        layer = sklayer
    if edg[0] == 'line':
        if pcb_ver is None or pcb_ver < 20211014:
            k_edg = "  (gr_line (start {0:.6f} {1:.6f}) (end {2:.6f} {3:.6f}) (angle 90) (layer {5}) (width {4}))"\
                        .format(edg[1]+ofs[0], -edg[2]+ofs[1], edg[3]+ofs[0], -edg[4]+ofs[1], edge_width, layer)
            #k_edg +=os.linesep
            #.format('{0:.10f}').format(edg[1] + abs(0), '{0:.10f}').format(edg[2] + abs(0), '{0:.10f}').format(edg[3] + abs(0), '{0:.10f}').format(edg[4] + abs(0), 'Edge.Cuts', edge_width)
        else:
            k_edg = "  (gr_line (start {0:.6f} {1:.6f}) (end {2:.6f} {3:.6f}) (layer {5}) (width {4}))"\
                        .format(edg[1]+ofs[0], -edg[2]+ofs[1], edg[3]+ofs[0], -edg[4]+ofs[1], edge_width, layer)
    elif edg[0] == 'circle':
        k_edg = "  (gr_circle (center {0:.6f} {1:.6f}) (end {2:.6f} {1:.6f}) (layer {4}) (width {3}))".format(edg[2]+ofs[0], -edg[3]+ofs[1], edg[2]+ofs[0]-edg[1], edge_width, layer)
        #k_edg +=os.linesep
                    #.format(
                    #'{0:.10f}'.format(i[1] + abs(self.minX)), '{0:.10f}'.format(i[2] + abs(self.minY)), '{0:.10f}'.format(
    #    self.addCircle(edg[1:], 'Edge.Cuts', 0.01)
    elif edg[0] == 'arc':
        #print edg
        #print 2*pi
        #use_rotation=False
        #if abs(abs(edg[5])-2*pi) <= edge_tolerance:
        #    print '2PI'
        #    use_rotation=True
        radius = edg[1]         #radius
        xs = edg[2]             #center x
        ys = (edg[3]) * (-1)    #center y
        #mp = DraftGeomUtils.findMidpoint(self.circle.Edges[0])
        #if 0: #use_rotation:
        #    sayerr('2PI')
        #    sayerr('check edge orientation!!!')
        #    #eA = edg[4]+pi
        #    #sA = edg[5]+pi
        #    eA = edg[4]-pi/2
        #    sA = edg[5]-pi/2
        #else:
        sA = edg[4]
        eA = edg[5]
        axisX = edg[6]
        axisY = edg[7]
        axisZ = edg[8]
        
        angle = degrees(sA - eA) # * (-1)
        # sayerr(angle)
        
        ##x1 = radius * cos(sA) + xs
        ##y1 = (radius * sin(sA)) * (-1) + ys
        #xs = edg[11][0] 
        #ys = (edg[11][1]) * (-1) 
        ## sA = atan2(edg[10][1]-edg[3], edg[10][0]-edg[2])
        ## eA = atan2(edg[11][1]-edg[3], edg[11][0]-edg[2])
        # sayerr(edg[12])
        
        x1 = edg[10][0] 
        y1 = (edg[10][1]) * (-1) 
        x2 = edg[11][0] 
        y2 = (edg[11][1]) * (-1) 
        
        #y1 = (radius * sin(sA)) * + ys
        #print axisX, axisY,axisZ
        #print ('coord     xs, ys, x1, y1 ', xs,';', ys,';', x1,';', y1,';',angle)
        #for i,e in enumerate(edg):
        #    print ('param edg['+str(i)+']='+str(edg[i]))
        #if angle > 180:
        #    angle = 360 - angle
        #self.getMinX(xs)
        #self.getMinY(ys)
        #self.getMinX(x1)
        #self.getMinY(y1)
        # Draft.makePoint(xs, -ys, 0)
        # Draft.makePoint(x1, -y1, 0)
        # #Draft.makePoint(mp[0],mp[1],mp[2])
        # Draft.makePoint(x2, -y2, 0)
        
        if abs(xs) > maxRadius or abs(ys) > maxRadius:
            if pcb_ver is None or pcb_ver < 20211014:
                k_edg = "  (gr_line (start {0:.6f} {1:.6f}) (end {2:.6f} {3:.6f}) (angle 0) (layer {5}) (width {4}))"\
                            .format(x1+ofs[0], y1+ofs[1], x2+ofs[0], y2+ofs[1], edge_width, layer)
                #k_edg = "  (gr_line (start {0} {1}) (end {2} {3}) (angle 90) (layer {5}) (width {4}))"\
                #            .format(edg[1]+ofs[0], -edg[2]+ofs[1], edg[3]+ofs[0], -edg[4]+ofs[1], edge_width, 'Edge.Cuts')
                #print xs + ofs[0]
                #stop
            else:
                k_edg = "  (gr_line (start {0:.6f} {1:.6f}) (end {2:.6f} {3:.6f}) (layer {5}) (width {4}))"\
                            .format(x1+ofs[0], y1+ofs[1], x2+ofs[0], y2+ofs[1], edge_width, layer)
        else:
            if pcb_ver is None or pcb_ver < 20211014:
                #self.pcbElem.append(['gr_arc', xs, ys, x1, y1, curve, width, layer])
                k_edg = "  (gr_arc (start {0:.6f} {1:.6f}) (end {2:.6f} {3:.6f}) (angle {4:.6f}) (layer {6}) (width {5}))"\
                        .format(xs+ofs[0], ys+ofs[1], x1+ofs[0], y1+ofs[1], angle, edge_width, layer)
            else:
                #stop
                # print(angle)
                # ep = rotatePoint(radius,sA,angle,[x1,y1])
                # print(ep[0],ep[1])
                mp = mid_point(Base.Vector(x1,y1,0),Base.Vector(x2,y2,0),angle)
                # Draft.makePoint(x1,y1,0)
                # FreeCAD.ActiveDocument.ActiveObject.ViewObject.PointColor=(1.0,0.0,0.0,0.0)
                # Draft.makePoint(x2,y2,0)
                # FreeCAD.ActiveDocument.ActiveObject.ViewObject.PointColor=(0.0,1.0,0.0,0.0)
                # Draft.makePoint(mp[0],mp[1],0)
                # FreeCAD.ActiveDocument.ActiveObject.ViewObject.PointColor=(0.0,0.0,1.0,0.0)
                # Part.show(Part.Edge(Part.Arc(FreeCAD.Base.Vector(x1, y1, 0), FreeCAD.Base.Vector(mp[0],mp[1], 0), FreeCAD.Base.Vector(x2, y2, 0))))
                # print(mp[0],mp[1])
                k_edg = "  (gr_arc (start {0:.6f} {1:.6f}) (mid {2:.6f} {3:.6f}) (end {4:.6f} {5:.6f}) (layer {7}) (width {6}))"\
                        .format(x2+ofs[0], y2+ofs[1], mp[0]+ofs[0], mp[1]+ofs[1], x1+ofs[0], y1+ofs[1], edge_width, layer)
                        #.format(xs+ofs[0], ys+ofs[1], mp[0]+ofs[0], mp[1]+ofs[1], x1+ofs[0], y1+ofs[1], edge_width, layer)
                #print(k_edg)
                #stop
    #    self.addArc(edg[1:], 'Edge.Cuts', 0.01)
    elif edg[0] == 'spline':
        k_edg = "  (gr_curve (pts (xy {0:.6f} {1:.6f}) (xy {2:.6f} {3:.6f}) (xy {4:.6f} {5:.6f}) (xy {6:.6f} {7:.6f})) (layer {9}) (width {8}))"\
        .format(edg[1]+ofs[0], -edg[2]+ofs[1], edg[3]+ofs[0], -edg[4]+ofs[1], edg[5]+ofs[0], -edg[6]+ofs[1], edg[7]+ofs[0], -edg[8]+ofs[1], edge_width, layer)
        # (pts (xy 151.983691 88.782809) (xy 152.805595 84.674685) (xy 148.40623 80.726614) (xy 144.40069 81.955321)) (layer Edge.Cuts) (width 0.2))
        
    return k_edg
##
def createFp(edg,ofs,layer, edge_thick):
    global edge_width, maxRadius
    
    #print edg
    k_edg=''
    #if edge_width is None:
    #    edge_width=0.16
    #def getMinX(self, x):
    #    if x < self.minX:
    #        self.minX = x
    #        
    #def getMinY(self, y):
    #    if y < self.minY:
    #        self.minY = y
    ## writing fp
    ln='fp_line'
    ac='fp_arc'
    cr='fp_circle'
    if edg[0] == 'line':
        if 0: #abs(edg[1]+ofs[0])>500 or abs(edg[2]+ofs[1])>500:
            #print edg
            stop
            k_edg = "  ("+ln+" (start {0:.6f} {1:.6f}) (end {2:.6f} {3:.6f}) (angle 90) (layer {5}) (width {4}))"\
                        .format(edg[1]+ofs[0], -edg[2]+ofs[1], edg[3]+ofs[0], -edg[4]+ofs[1], edge_thick, layer)
        else:
            k_edg = "  ("+ln+" (start {0:.6f} {1:.6f}) (end {2:.6f} {3:.6f}) (layer {5}) (width {4}))"\
                        .format(edg[1]+ofs[0], -edg[2]+ofs[1], edg[3]+ofs[0], -edg[4]+ofs[1], edge_thick, layer)
        #k_edg +=os.linesep
        #.format('{0:.10f}').format(edg[1] + abs(0), '{0:.10f}').format(edg[2] + abs(0), '{0:.10f}').format(edg[3] + abs(0), '{0:.10f}').format(edg[4] + abs(0), 'Edge.Cuts', edge_width)
    elif edg[0] == 'circle':
        k_edg = "  ("+cr+" (center {0:.6f} {1:.6f}) (end {2:.6f} {1:.6f}) (layer {4}) (width {3}))".format(edg[2]+ofs[0], -edg[3]+ofs[1], edg[2]+ofs[0]-edg[1], edge_thick, layer)
        #k_edg +=os.linesep
                    #.format(
                    #'{0:.10f}'.format(i[1] + abs(self.minX)), '{0:.10f}'.format(i[2] + abs(self.minY)), '{0:.10f}'.format(
    #    self.addCircle(edg[1:], 'Edge.Cuts', 0.01)
    elif edg[0] == 'arc':
        #print edg
        #print 2*pi
        #use_rotation=False
        #if abs(abs(edg[5])-2*pi) <= edge_tolerance:
        #    print '2PI'
        #    use_rotation=True
        radius = edg[1]
        xs = edg[2]
        ys = (edg[3]) * (-1)
        #if 0: #use_rotation:
        #    sayerr('2PI')
        #    sayerr('check edge orientation!!!')
        #    #eA = edg[4]+pi
        #    #sA = edg[5]+pi
        #    eA = edg[4]-pi/2
        #    sA = edg[5]-pi/2
        #else:
        sA = edg[4]
        eA = edg[5]
        axisX = edg[6]
        axisY = edg[7]
        axisZ = edg[8]
        
        angle = degrees(sA - eA) # * (-1)
        # sayerr(angle)
        
        ##x1 = radius * cos(sA) + xs
        ##y1 = (radius * sin(sA)) * (-1) + ys
        #xs = edg[11][0] 
        #ys = (edg[11][1]) * (-1) 
        ## sA = atan2(edg[10][1]-edg[3], edg[10][0]-edg[2])
        ## eA = atan2(edg[11][1]-edg[3], edg[11][0]-edg[2])
        # sayerr(edg[12])
        
        if  1: #angle ==< 0:
            x1 = edg[10][0] 
            y1 = (edg[10][1]) * (-1) 
            x2 = edg[11][0] 
            y2 = (edg[11][1]) * (-1) 
        else:
            x1 = edg[11][0] 
            y1 = (edg[11][1]) * (-1) 
        
        #y1 = (radius * sin(sA)) * + ys
        #print axisX, axisY,axisZ
        #print 'coord     xs, ys, x1, y1 ', xs,';', ys,';', x1,';', y1,';',angle
        
        #if angle > 180:
        #    angle = 360 - angle
                        
        #self.getMinX(xs)
        #self.getMinY(ys)
        #self.getMinX(x1)
        #self.getMinY(y1)
        # Draft.makePoint(xs, -ys, 0)
        # Draft.makePoint(x1, -y1, 0)
        # #Draft.makePoint(mp[0],mp[1],mp[2])
        # Draft.makePoint(x2, -y2, 0)
        
        if abs(xs) > maxRadius or abs(ys) > maxRadius:
            k_edg = "  ("+ln+" (start {0:.6f} {1:.6f}) (end {2:.6f} {3:.6f}) (layer {5}) (width {4}))"\
                        .format(x1+ofs[0], y1+ofs[1], x2+ofs[0], y2+ofs[1], edge_thick, layer)
            #k_edg = "  (gr_line (start {0} {1}) (end {2} {3}) (angle 90) (layer {5}) (width {4}))"\
            #            .format(edg[1]+ofs[0], -edg[2]+ofs[1], edg[3]+ofs[0], -edg[4]+ofs[1], edge_width, 'Edge.Cuts')
            #print xs + ofs[0]
            #stop
        else:
            #self.pcbElem.append(['gr_arc', xs, ys, x1, y1, curve, width, layer])
            k_edg = "  ("+ac+" (start {0:.6f} {1:.6f}) (end {2:.6f} {3:.6f}) (angle {4:.6f}) (layer {6}) (width {5}))"\
                    .format(xs+ofs[0], ys+ofs[1], x1+ofs[0], y1+ofs[1], angle, edge_thick, layer)
            #.format(
            #            '{0:.10f}'.format(i[1] + abs(self.minX)), '{0:.10f}'.format(i[2] + abs(self.minY)), '{0:.10f}'.format(i[3] + abs(self.minX)), '{0:.10f}'.format(i[4] + abs(self.minY)), i[5], i[6], i[7]))
    #    self.addArc(edg[1:], 'Edge.Cuts', 0.01)
    return k_edg
##

def Discretize(skt_name):
    ##http://forum.freecadweb.org/viewtopic.php?f=12&t=16336#p129468
    ##Discretizes the edge and returns a list of points.
    ##The function accepts keywords as argument:
    ##discretize(Number=n) => gives a list of 'n' equidistant points
    ##discretize(QuasiNumber=n) => gives a list of 'n' quasi equidistant points (is faster than the method above)
    ##discretize(Distance=d) => gives a list of equidistant points with distance 'd'
    ##discretize(Deflection=d) => gives a list of points with a maximum deflection 'd' to the edge
    ##discretize(QuasiDeflection=d) => gives a list of points with a maximum deflection 'd' to the edge (faster)
    ##discretize(Angular=a,Curvature=c,[Minimum=m]) => gives a list of points with an angular deflection of 'a'
    ##and a curvature deflection of 'c'. Optionally a minimum number of points
    ##can be set which by default is set to 2. 

    global dvm, dqd, precision

    # lng=(abs(FreeCAD.ActiveDocument.getObject(skt_name).Shape.BoundBox.XLength)+abs(FreeCAD.ActiveDocument.getObject(skt_name).Shape.BoundBox.YLength))
    # dv=int(dvm*lng) #discretize auto setting
    # #dv=int(0.5*lng) #discretize auto setting COARSE for testing
    # #print dv
    # if dv < 20:
    #     dv=20
    b=FreeCAD.ActiveDocument.getObject(skt_name)
    shp1=b.Shape.copy()
    #e = shp1.Edges[0].Curve
    #skList=[]
    newShapeList = []
    newShapes = []
    for e in shp1.Edges:
    ##e = shp1.Edges[0] #.Curve
    #sayerr(e.Curve)
    #print DraftGeomUtils.geomType(e)
    #if isinstance(e.Curve,Part.BSplineCurve):
    #    sayerr('geomType BSP')
    #Part.show(shp1)
        if isinstance(e.Curve,Part.BSplineCurve):
            say('found BSpline')
            edges = []
            arcs = e.Curve.toBiArcs(precision)
            #print arcs
            for i in arcs:
                edges.append(Part.Edge(i))
            w = Part.Wire([Part.Edge(i) for i in edges])
            Part.show(w)
            w_name=FreeCAD.ActiveDocument.ActiveObject.Name
            newShapeList.append(w_name)
            wn=FreeCAD.ActiveDocument.getObject(w_name)
            newShapes.append(wn)
        else: #ellipses
            #l=b.Shape.copy().discretize(dv)
            #l=b.Shape.copy().discretize(QuasiDeflection=0.02)
            w = Part.Wire(e)
            Part.show(w)
            w_name=FreeCAD.ActiveDocument.ActiveObject.Name
            #newShapeList.append(w_name)
            wn=FreeCAD.ActiveDocument.getObject(w_name)
            #newShapes.append(wn)
            l=wn.Shape.copy().discretize(QuasiDeflection=dqd)
            #l=b.Shape.copy().discretize(QuasiDeflection=dqd)
            f=Part.makePolygon(l)
            Part.show(f)
            sh_name=FreeCAD.ActiveDocument.ActiveObject.Name
            newShapeList.append(sh_name)
            newShapes.append(f)
            FreeCAD.ActiveDocument.removeObject(w_name)
            FreeCAD.ActiveDocument.recompute() 
        
    ## sketch = Draft.makeSketch(newShapes[0],autoconstraints=True)
    sketch = Draft.makeSketch(FreeCAD.ActiveDocument.getObject(newShapeList[0]),autoconstraints=True)
    
    #FreeCAD.ActiveDocument.ActiveObject.Label="Sketch_dxf"
    sname=FreeCAD.ActiveDocument.ActiveObject.Name
    for w in newShapes[1:]:
        Draft.makeSketch([w],addTo=sketch)    
    geom=[]
    ## recreating a correct geometry
    for i in sketch.Geometry:
        if isinstance(i,Part.ArcOfCircle) and i.XAxis.x < 0:
            arc=Part.ArcOfCircle(i.Circle,i.FirstParameter+pi,i.LastParameter+pi)
            arc.XAxis.x = -arc.XAxis.x
            geom.append(arc)
        else:
            geom.append(i)                
    tsk= FreeCAD.activeDocument().addObject('Sketcher::SketchObject','Sketch_result')
    tsk.addGeometry(geom)
    tsk.Placement=FreeCAD.ActiveDocument.getObject(sname).Placement
    FreeCAD.ActiveDocument.removeObject(sname)
    #print tsk.Geometry
    ##for w in newShapes[1:]:
    ##    Draft.makeSketch([w],addTo=sketch)    
    #stop
    #for wire in wires:
    #    FreeCAD.ActiveDocument.removeObject(wire.Name)
    for wnm in newShapeList:
        FreeCAD.ActiveDocument.removeObject(wnm)
    FreeCAD.ActiveDocument.removeObject(skt_name)
    FreeCAD.ActiveDocument.recompute() 
    s_name=tsk.Name
        
        #else: #ellipses
        #    #l=b.Shape.copy().discretize(dv)
        #    #l=b.Shape.copy().discretize(QuasiDeflection=0.02)
        #    l=b.Shape.copy().discretize(QuasiDeflection=dqd)
        #    f=Part.makePolygon(l)
        #    Part.show(f)
        #    sh_name=FreeCAD.ActiveDocument.ActiveObject.Name
        #    FreeCAD.ActiveDocument.recompute() 
        #    Draft.makeSketch(FreeCAD.ActiveDocument.getObject(sh_name),autoconstraints=True)
        #    s_name=FreeCAD.ActiveDocument.ActiveObject.Name
        #    FreeCAD.ActiveDocument.removeObject(sh_name)
        #    FreeCAD.ActiveDocument.removeObject(skt_name)
        #    FreeCAD.ActiveDocument.recompute() 
    
    
    return s_name
    #stop

##
def remove_basic_geom(c_name, to_disc):
    
    s=FreeCAD.ActiveDocument.getObject(c_name)
    geoL=len(FreeCAD.ActiveDocument.getObject(c_name).Geometry)
    #print 'to discretize'
    #print to_disc
    to_disc_str=[]
    for j in range (len(to_disc)):
        to_disc_str.append(str(to_disc[j]))
    #print to_disc_str
    #print 'geo',' ', App.ActiveDocument.getObject(c_name).Geometry
    #print 'oldgeo',' ', App.ActiveDocument.getObject("PCB_Sketch").Geometry
    #stop
    #print 'removing'
    #for i in range (geoL-1,0,-1):
    for i in range (geoL-1,-1,-1):
        #print 's.geom'
        #if str(s.Geometry[i-1]) in to_disc_str:
        #    print 'found geo to disc'
        #else:
        #print str(s.Geometry[i]), ';;' 
        if str(s.Geometry[i]) not in to_disc_str:
            if hasattr(s,'GeometryFacadeList'):
                Gm = s.GeometryFacadeList
            else:
                Gm = s.Geometry
            #if hasattr(Gm[i],'Construction'):
            #    if not Gm[i].Construction:
            if isConstruction(Gm[i]):
                #print FreeCAD.ActiveDocument.getObject(c_name).Geometry[i]
                FreeCAD.ActiveDocument.getObject(c_name).delGeometry(i)
    FreeCAD.ActiveDocument.recompute()
    #stop
    #if i not in 
    #App.ActiveDocument.getObject("PCB_Sketch").delGeometry(0, 3, 4, 10, 11, 12)
##
def split_basic_geom(c_name, to_disc):
    
    s=FreeCAD.ActiveDocument.getObject(c_name)
    geoL=len(FreeCAD.ActiveDocument.getObject(c_name).Geometry)
    geoB = []
    #print 'to discretize'
    #print to_disc
    to_disc_str=[]
    for j in range (len(to_disc)):
        to_disc_str.append(str(to_disc[j]))
    #print to_disc_str
    #print 'geo',' ', App.ActiveDocument.getObject(c_name).Geometry
    #print 'oldgeo',' ', App.ActiveDocument.getObject("PCB_Sketch").Geometry
    #stop
    #print 'removing'
    #for i in range (geoL-1,0,-1):
    for i in range (geoL-1,-1,-1):
        #print 's.geom'
        #if str(s.Geometry[i-1]) in to_disc_str:
        #    print 'found geo to disc'
        #else:
        #print str(s.Geometry[i]), ';;' 
        if str(s.Geometry[i]) not in to_disc_str:
            if hasattr(s,'GeometryFacadeList'):
                Gm = s.GeometryFacadeList
            else:
                Gm = s.Geometry
            #if hasattr(Gm[i],'Construction'):
            #    if not Gm[i].Construction:
            if isConstruction(Gm[i]):
                #print FreeCAD.ActiveDocument.getObject(c_name).Geometry[i]
                geoB.append(FreeCAD.ActiveDocument.getObject(c_name).Geometry[i])
                FreeCAD.ActiveDocument.getObject(c_name).delGeometry(i)
    FreeCAD.ActiveDocument.recompute()
    #stop
    #if i not in 
    #App.ActiveDocument.getObject("PCB_Sketch").delGeometry(0, 3, 4, 10, 11, 12)
    return geoB
##
def check_geom(sk_name, ofs=None):
    
    if ofs is None:
        ofs=[0,0]
    j=FreeCAD.ActiveDocument.getObject(sk_name)
    to_discretize=[]
    outline=[]
    foundBSP=False
    foundElly=False
    geo_all=''
    for k in range(len(j.Geometry)):
        foundGeo=False
        #print(type(j.Geometry[k]).__name__)
        if hasattr(j,'GeometryFacadeList'):
            Gm = j.GeometryFacadeList
        else:
            Gm = j.Geometry
        #if hasattr(Gm[k],'Construction'):
        if isConstruction(Gm[k]):
            sayw('construnction skipped')
        #if Gm[k].Construction:
            #sayerr('construction skipped')
            continue
        if 'Point' in type(j.Geometry[k]).__name__:  #skipping points
            sayw('point skipped')
            continue
        if 'LineSegment' in type(j.Geometry[k]).__name__:
        #if 'Line' in type(j.Geometry[k]).__name__:
            sk_ge=j.Geometry[k].toShape() #needed to fix some issue on sketch geometry building
            outline.append([
                'line',
                sk_ge.Edges[0].Vertexes[0].Point.x+ofs[0],
                sk_ge.Edges[0].Vertexes[0].Point.y+ofs[1],
                sk_ge.Edges[0].Vertexes[1].Point.x+ofs[0],
                sk_ge.Edges[0].Vertexes[1].Point.y+ofs[1],
                j.Label
            ])
            # outline.append([
            #     'line',
            #     j.Geometry[k].StartPoint.x+ofs[0],
            #     j.Geometry[k].StartPoint.y+ofs[1],
            #     j.Geometry[k].EndPoint.x+ofs[0],
            #     j.Geometry[k].EndPoint.y+ofs[1]
            # ])
        #elif type(j.Geometry[k]).__name__ == 'Circle':
        elif 'Circle' in type(j.Geometry[k]).__name__ and not 'ArcOfCircle' in type(j.Geometry[k]).__name__:
            sk_ge=j.Geometry[k].toShape() #needed to fix some issue on sketch geometry building
            outline.append([
                'circle',
                sk_ge.Edges[0].Curve.Radius,
                sk_ge.Edges[0].Curve.Center.x+ofs[0], 
                sk_ge.Edges[0].Curve.Center.y+ofs[1],
                j.Label 
            ])
            #outline.append([
            #    'circle',
            #    j.Geometry[k].Radius,
            #    j.Geometry[k].Center.x+ofs[0], 
            #    j.Geometry[k].Center.y+ofs[1]
            #])
        #elif type(j.Geometry[k]).__name__ == 'ArcOfCircle':
        elif 'ArcOfCircle' in type(j.Geometry[k]).__name__:
            #outline.append([
            #    'arc',
            #    j.Geometry[k].Radius, 
            #    j.Geometry[k].Center.x+ofs[0], 
            #    j.Geometry[k].Center.y+ofs[1], 
            #    j.Geometry[k].FirstParameter+ofs[0], 
            #    j.Geometry[k].LastParameter+ofs[1],
            #    j.Geometry[k].Axis[0],
            #    j.Geometry[k].Axis[1],
            #    j.Geometry[k].Axis[2],
            #    j.Geometry[k],
            #    j.Shape.Edges[k].Vertexes[0].Point,
            #    j.Shape.Edges[k].Vertexes[1].Point,
            #    j.Shape.Edges[k].Orientation
            #])
            sk_ge=j.Geometry[k].toShape() #needed to fix some issue on sketch geometry building
            outline.append([
                'arc',
                j.Geometry[k].Radius, 
                sk_ge.Edges[0].Curve.Center.x+ofs[0],
                sk_ge.Edges[0].Curve.Center.y+ofs[1],
                j.Geometry[k].FirstParameter+ofs[0],
                j.Geometry[k].LastParameter+ofs[1],
                j.Geometry[k].Axis[0],
                j.Geometry[k].Axis[1],
                j.Geometry[k].Axis[2],
                j.Geometry[k],
                sk_ge.Edges[0].Vertexes[0].Point,
                sk_ge.Edges[0].Vertexes[1].Point,
                sk_ge.Edges[0].Orientation,
                j.Label
            ])
            ## maxRadius=3500
            ## sayerr(j.Geometry[k].Radius)
            ## stop
            ##if j.Geometry[k].Radius > maxRadius:
            ##    sayerr(j.Geometry[k].Radius)
            # i=j.Geometry[k]
            # sayerr('Xaxis2a')
            # if 0: #i.XAxis.x < 0:  #da cambiare  this is not available on FC0.16
            #     sayerr('Xaxis2b')
            #     outline.append([
            #         'arc',
            #         i.Radius, 
            #         i.Center.x, 
            #         i.Center.y, 
            #         i.LastParameter+pi,
            #         i.FirstParameter+pi, 
            #         -i.Axis[0],
            #         i.Axis[1],
            #         i.Axis[2],
            #         i
            #     ])
            # else:
            #     outline.append([
            #         'arc',
            #         i.Radius, 
            #         i.Center.x, 
            #         i.Center.y, 
            #         i.LastParameter,
            #         i.FirstParameter+pi, 
            #         i.Axis[0],
            #         i.Axis[1],
            #         i.Axis[2],
            #         i
            #     ])
        else:
            #print j.Geometry[k],'; not supported'
            to_discretize.append(j.Geometry[k])
            #to_discretize.append(k)
            str_geom=str(j.Geometry[k])
            if 'ArcOfEllipse' in str_geom:
                str_geom='ArcOfEllipse'
            elif 'ArcOfParabola' in str_geom:
                str_geom='ArcOfParabola'
            elif 'ArcOfHyperbola' in str_geom:
                str_geom='ArcOfHyperbola'
            #continue
                    ##break            
                    #print j.Geometry[k],'; not supported'
        #else:
        #    str_geom=str(j.Geometry[k])
        #    if 'ArcOfEllipse' in str_geom:
        #        str_geom='ArcOfEllipse'
        #        foundGeom=True;foundBSP==False;foundElly==False
        #    elif 'ArcOfParabola' in str_geom:
        #        str_geom='ArcOfParabola'
        #        foundGeom=True;foundBSP==False;foundElly==False
        #    elif 'ArcOfHyperbola' in str_geom:
        #        str_geom='ArcOfHyperbola'
        #        foundGeom=True;foundBSP==False;foundElly==False
        #    elif 'Circle' in str_geom:
        #        foundGeom=True;foundBSP==False;foundElly==False
        #    elif 'Line' in str_geom:
        #        foundGeom=True;foundBSP==False;foundElly==False
        #    if 'Vector' in str_geom:
        #        if foundBSP==True and foundGeom==False or foundElly==True and foundGeom==False:
        #            to_discretize.append(j.Geometry[k])   
        #    #continue
    ##break
    #print to_discretize
    #stop
    
    return outline, to_discretize


##

##  getGridOrigin
def getGridOrigin(dt):
    match = re.search(r'\(grid_origin (.+?) (.+?)\)', dt, re.MULTILINE|re.DOTALL)
    if match is not None:
        return [float(match.group(1)), float(match.group(2))];
    else:
        #returning default top left corner value
        return [0.0,0.0]
##
##  getAuxOrigin
def getAuxOrigin(dt):
    match = re.search(r'\(aux_axis_origin (.+?) (.+?)\)', dt, re.MULTILINE|re.DOTALL)
    if match is not None:
        return [float(match.group(1)), float(match.group(2))];
    else:
        # #returning default top left corner value
        # return [0.0,0.0]
        return None
##
def export_pcb(fname=None,sklayer=None,skname=None):
    global last_fp_path, test_flag, start_time
    global configParser, configFilePath, start_time
    global ignore_utf8, ignore_utf8_incfg, disable_PoM_Observer
    global board_base_point_x, board_base_point_y, real_board_pos_x, real_board_pos_y
    global pcb_path, use_AppPart, force_oldGroups, use_Links, use_LinkGroups
    global original_filename, aux_orig, grid_orig
    global off_x, off_y, maxRadius
    global zfit, edge_width
    
    import fcad_parser
    from fcad_parser import KicadPCB,SexpList
    import kicad_parser
    
    sayw('exporting new pcb edges')
    doc=FreeCAD.ActiveDocument
    #filePath=last_pcb_path
    #fpath=filePath+os.sep+doc.Label+'.kicad_pcb'
    #sayerr('to '+fpath)
    
    #print fname
    if fname is None:
        fpath=original_filename
    else:
        fpath=fname
    
    sayerr('saving to '+fpath)
    #stop
    
    if len(fpath) > 0:
        #new_edge_list=getBoardOutline()
        #say (new_edge_list)
        cfg_read_all()
        path, fname = os.path.split(fpath)
        name=os.path.splitext(fname)[0]
        ext=os.path.splitext(fname)[1]
        fpth = os.path.dirname(os.path.abspath(fpath))
        #filePath = os.path.split(os.path.realpath(__file__))[0]
        say ('my file path '+fpth)
        # stop
        if fpth == "":
            fpth = "."
        last_pcb_path = fpth
        last_pcb_path = re.sub("\\\\", "/", last_pcb_path)
        ini_vars[10] = last_pcb_path
        #cfg_update_all()
        pg = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/kicadStepUp")
        pg.SetString("last_pcb_path", make_string(last_pcb_path))
        #sayerr(name+':'+ext)
        with codecs.open(fpath,'r', encoding='utf-8') as txtFile:
            content = txtFile.readlines() # problems?
        content.append(u" ")
        txtFile.close()
        data=u''.join(content)
        tml= time.localtime()
        now=str(tml.tm_year)+'-'+str(tml.tm_mon)+'-'+str(tml.tm_mday)+'-'+str(tml.tm_hour)+'.'+str(tml.tm_min)+'.'+str(tml.tm_sec)
        #foname=os.path.join(path, name+'-bkp-'+now+ext+'-bak')
        foname=os.path.join(path, name+u'-bkp-'+make_unicode(now)+ext+u'-bak')
        pcb_push=True
        testing=False
        if testing is not True:
            try:
                #with codecs.open(foname,'w', encoding='utf-8') as ofile:
                #    ofile.write(data)
                #    ofile.close()
                copyfile(fpath, foname)
                say('file copied')
            except:
                msg="""<b>problem in writing permissions to kicad board!</b><br><br>"""
                msg+="<b>file saving aborted to<br>"+fpath+"</b><br><br>"
                msgr="problem in writing permissions to kicad board!\n"
                msgr+="file saving aborted to "+fpath+"\n"
                pcb_push=False
                say(msgr)
                say_info(msg)
        if pcb_push==True:    
            if sklayer is None:
                ssklayer = 'Edge'
            else:
                ssklayer = sklayer.split('.')[0]
                if 'KeepOutZone' in sklayer:
                    ssklayer = 'KeepOutZone'
                elif 'FillZone' in sklayer:
                    ssklayer = 'FillZone'
                elif 'MaskZone' in sklayer:
                    ssklayer = 'MaskZone'
                print (ssklayer)
            edge_pcb_exists=False
            mypcb = KicadPCB.load(fpath)
            pcb_version = mypcb.version
            sayw('parsing, pcb v='+str(pcb_version))
            edg_segms = 0
            for ln in mypcb.gr_line:
                if ssklayer in ln.layer:
                    #say(ln.layer)
                    edg_segms+=1
                    break
            if edg_segms == 0:
                for ar in mypcb.gr_arc:
                    if ssklayer in ar.layer:
                        #say(ln.layer)
                        edg_segms+=1
                        break
            if edg_segms == 0:
                for cr in mypcb.gr_circle:
                    if ssklayer in cr.layer:
                        #say(ln.layer)
                        edg_segms+=1
                        break
            if edg_segms == 0:
                for lp in mypcb.gr_poly:
                    #print(lp)
                    #print(lp.layer)
                    #print(lp.pts)
                    if ssklayer in lp.layer:
                        #sayerr(lp.layer)
                        for p in lp.pts.xy:
                            edg_segms+=1
                            break
                            #sayerr(p)
                    #stop
                    #edg_segms+=1
            if edg_segms == 0:
                for bs in mypcb.gr_curve:
                    if ssklayer in bs.layer:
                        #sayerr(bs.layer)
                        for p in bs.pts.xy:
                            edg_segms+=1
                            break
                        #edg_segms+=1
            #sayw(str(edg_segms)+' '+ssklayer+' segments')
            if (edg_segms)>0:
                edge_pcb_exists=True
                sayw('found '+ssklayer+' element(s)')
            #stop
            if ssklayer == 'Edge':
                if hasattr(mypcb, 'setup'):
                    if hasattr(mypcb.setup, 'edge_width'): #maui edge width
                        edge_width=mypcb.setup.edge_width
                    elif hasattr(mypcb.setup, 'edge_cuts_line_width'): #maui edge cuts new width k 5.99
                        edge_width=mypcb.setup.edge_cuts_line_width
                #else:
                #    edge_width=0.16
            oft=None
            origin_warn = False
            #skip = False
            if aux_orig == 1:
                oft=getAuxOrigin(data)
                if oft is None:
                    msg="""StepUp is configured for \'aux origin\' reference<br>but \'aux origin\' is not placed/set on kicad destination board"""
                    say_warning(msg)
                    stop
                else:
                    print ('aux_origin found',oft)
            elif grid_orig == 1:
                oft=getGridOrigin(data)
                if oft is None:
                    msg="""StepUp is configured for \'grid origin\' reference<br>but \'grid origin\' is not placed/set on kicad destination board"""
                    say_warning(msg)
                    stop
                else:
                    if oft == [0.0,0.0]:
                        origin_warn = True
                    print ('grid_origin found',oft)
            else:
                print('using an approximate PCB center as sketch reference point')
            #print oft
            gof=False
            if oft is not None:
                off_x=oft[0];off_y=-oft[1]
                offset = oft
                gof=True
  
            if edge_pcb_exists and ssklayer != 'FillZone' and ssklayer != 'KeepOutZone':
                #offset=[0,0]
                doc=FreeCAD.ActiveDocument
                ksu_found=False;skt_name='';pcb_found=False
                for obj in doc.Objects:
                    if ("PCB_Sketch" in obj.Name) or ("PCB_Sketch" in obj.Label) or\
                       ("Edge_Sketch" in obj.Name) or ("Edge.Cuts" in obj.Label) or \
                       ("Dwgs_Sketch" in obj.Name) or ("Dwgs.User" in obj.Label) or \
                       ("Eco1_Sketch" in obj.Name) or ("Eco1.User" in obj.Label) or \
                       ("Eco2_Sketch" in obj.Name) or ("Eco2.User" in obj.Label) or \
                       ("Cmts_Sketch" in obj.Name) or ("Cmts.User" in obj.Label) or \
                       ("Margin_Sketch" in obj.Name) or ("Margin" in obj.Label):
                        ksu_found=True
                        skt_name=obj.Name
                    if ("Pcb" in obj.Name):
                        ksu_found=True
                        pcb_found=True
                testing=False
                if testing is True:
                    off_x=0;off_y=0
                if ksu_found==True or testing==True:
                    if pcb_found==True:
                        #bbpx=-FreeCAD.ActiveDocument.getObject('Pcb').Placement.Base[0]+FreeCAD.ActiveDocument.getObject(skt_name).Placement.Base[0]
                        #bbpy=FreeCAD.ActiveDocument.getObject('Pcb').Placement.Base[1]-FreeCAD.ActiveDocument.getObject(skt_name).Placement.Base[1]
                        bbpx=-FreeCAD.ActiveDocument.getObject(skname).Placement.Base[0]+FreeCAD.ActiveDocument.getObject(skt_name).Placement.Base[0]
                        bbpy=FreeCAD.ActiveDocument.getObject(skname).Placement.Base[1]-FreeCAD.ActiveDocument.getObject(skt_name).Placement.Base[1]
                        offset=[bbpx,bbpy]
                    else:
                        off_x=0;off_y=0
                        offset=[off_x,-off_y]
                    if gof and grid_orig==1:
                        offset=[off_x,-off_y]
                        offset = (getGridOrigin(data)[0],getGridOrigin(data)[1])
                    elif gof and aux_orig==1:
                        offset=[off_x,-off_y]
                        offset = (getAuxOrigin(data)[0],getAuxOrigin(data)[1])
                    #if gof and not pcb_found:
                    #    offset=[0,0]
                    ## maui to test position
                    #print offset
                    #say(offset)
                    #stop
                    if ssklayer == 'Edge':
                        say('pcb edge exists')
                        sayw('removing old Edge '+ssklayer)
                    else:
                        sayw('removing existing drawings '+ssklayer)
                    ## removing old Edge
                    repl = re.sub('\s\(gr_line(.+?)'+ssklayer+'(.+?)\)\)\r\n|\s\(gr_line(.+?)'+ssklayer+'(.+?)\)\)\r|\s\(gr_line(.+?)'+ssklayer+'(.+?)\)\)\n','',data, flags=re.MULTILINE)
                    repl = re.sub('\s\(gr_curve(.+?)'+ssklayer+'(.+?)\)\)\r\n|\s\(gr_curve(.+?)'+ssklayer+'(.+?)\)\)\r|\s\(gr_curve(.+?)'+ssklayer+'(.+?)\)\)\n','',repl, flags=re.MULTILINE)
                    repl = re.sub('\s\(gr_arc(.+?)'+ssklayer+'(.+?)\)\)\r\n|\s\(gr_arc(.+?)'+ssklayer+'(.+?)\)\)\r|\s\(gr_arc(.+?)'+ssklayer+'(.+?)\)\)\n','',repl, flags=re.MULTILINE)
                    repl = re.sub('\s\(gr_circle(.+?)'+ssklayer+'(.+?)\)\)\r\n|\s\(gr_circle(.+?)'+ssklayer+'(.+?)\)\)\r|\s\(gr_circle(.+?)'+ssklayer+'(.+?)\)\)\n','',repl, flags=re.MULTILINE)
                    repl = re.sub('\s\(gr_rect(.+?)'+ssklayer+'(.+?)\)\)\r\n|\s\(gr_rect(.+?)'+ssklayer+'(.+?)\)\)\r|\s\(gr_rect(.+?)'+ssklayer+'(.+?)\)\)\n','',repl, flags=re.MULTILINE)
                    repl = re.sub('\s\(gr_poly(.+?)'+ssklayer+'(.+?)\)\)\r\n|\s\(gr_poly(.+?)'+ssklayer+'(.+?)\)\)\r|\s\(gr_poly(.+?)'+ssklayer+'(.+?)\)\)\n','',repl, flags=re.MULTILINE|re. DOTALL)
                    #sayerr(replace)
                    k = repl.rfind(")")  #removing latest ')'
                    newcontent = repl[:k]
                else:
                    sayerr('to push a new release of Edge to a kicad board with an existing Edge\nyou need to load the board with StepUp first')
                    say_warning("""<b>to push a new release of Edge to a kicad board<br>with an existing Edge<br>you need to load the board with StepUp first<br><br>""")
                    stop
            else:
                #[148.5, -98.5] center of A4 page
                if gof and grid_orig==1:
                    sayw('pcb edge does not exist, aligning sketch to Grid Origin')
                    offset=[off_x,-off_y]
                elif gof and aux_orig==1:
                    sayw('pcb edge does not exist, aligning sketch to Aux Origin')
                    offset=[off_x,-off_y]
                else:
                    sayw('pcb edge does not exist, aligning sketch to center of A4 page')
                    offset=[148.5,98.5]
                ##sel = FreeCADGui.Selection.getSelection()
                ##if len (sel) >0:
                ##    #sayw(doc.Name)
                ##    for j in sel:
                ##        if "Sketch" in j.TypeId:
                ##            #FreeCAD.ActiveDocument.getObject(j.Name).Placement = FreeCAD.Placement(FreeCAD.Vector(148.5, -98.5,0),FreeCAD.Rotation(FreeCAD.Vector(0,0,1),0))
                ##            if FreeCAD.ActiveDocument.getObject(j.Name).Placement.Base[0]==0: #sketch created at FC origin
                ##                FreeCAD.ActiveDocument.getObject(j.Name).Placement = FreeCAD.Placement(FreeCAD.Vector(148.5,-98.5,0), App.Rotation(0,0,0), App.Vector(0,0,0)) #[Pos=(-148.5,98,5), Yaw-Pitch-Roll=(0,0,0)]
                            
                            #shift_sketch(j.Name,offset)
                FreeCAD.ActiveDocument.recompute()
                if (zfit):
                    FreeCADGui.SendMsgToActiveView("ViewFit")
                k = data.rfind(")")  #removing latest ')'
                newcontent = data[:k] 
            
            to_discretize = []; not_supported = []
            if ssklayer != 'FillZone' and ssklayer != 'MaskZone' and ssklayer != 'KeepOutZone':
                new_edge_list, not_supported, to_discretize, construction_geom = getBoardOutline()
                #print (new_edge_list)
                #stop
                
                #geoL=len(App.ActiveDocument.getObject("PCB_Sketch").Geometry)
                if len(to_discretize)>0:
                    #stop
                    sel = FreeCADGui.Selection.getSelection()
                    if len (sel)==1:
                        sk_name=sel[0].Name
                        t_name=cpy_sketch(sk_name)
                        ###t_sk=FreeCAD.ActiveDocument.copyObject(FreeCAD.ActiveDocument.getObject(sk_name))
                        elist, to_dis=check_geom(t_name)
                        #Draft.clone(FreeCAD.ActiveDocument.getObject(sk_name),copy=True)
                        #clone_name=App.ActiveDocument.ActiveObject.Name
                        remove_basic_geom(t_name, to_dis)
                        ##remove_basic_geom(t_sk.Name, to_discretize)
                        ##elist, to_dis=check_geom(t_sk.Name)
                        #print elist
                        #stop
                    obj_list_prev=[]
                    for obj in doc.Objects:
                        #print obj.TypeId
                        if (obj.TypeId=="Part::Feature") or (obj.TypeId=="Sketcher::SketchObject"):
                            obj_list_prev.append(obj.Name)
                    #Draft.draftify(FreeCAD.ActiveDocument.getObject(t_name),delete=True)
                    #Draft.draftify(FreeCAD.ActiveDocument.getObject(t_name),delete=False)
                    b=FreeCAD.ActiveDocument.getObject(t_name)
                    shp1=b.Shape.copy()
                    Part.show(shp1)
                    FreeCAD.ActiveDocument.removeObject(t_name)
                    FreeCAD.ActiveDocument.recompute()
                    #stop
                    obj_list_after=[]
                    for obj in doc.Objects:
                        if (obj.TypeId=="Part::Feature") or (obj.TypeId=="Sketcher::SketchObject")\
                            or (obj.TypeId=="Part::Part2DObjectPython"):
                                if obj.Name not in obj_list_prev:
                                    obj_list_after.append(obj.Name)
                    #print obj_list_after #, obj_list_prev
                    sk_to_conv=[]
                    for obj in doc.Objects:
                        if obj.Name in obj_list_after:
                            if (obj.TypeId=="Part::Part2DObjectPython"):
                                FreeCAD.ActiveDocument.removeObject(obj.Name)
                                FreeCAD.ActiveDocument.recompute() 
                            else:
                                sk_to_conv.append(obj.Name)
                    keep_sketch_converted=False #False
                    for s in sk_to_conv:
                        #sayerr(s) ## 
                        ns=Discretize(s)
                        offset1=[-FreeCAD.ActiveDocument.getObject(sk_name).Placement.Base[0],-FreeCAD.ActiveDocument.getObject(sk_name).Placement.Base[1]]
                        elist, to_dis=check_geom(ns,offset1)
                        new_edge_list=new_edge_list+elist
                        if not keep_sketch_converted:
                            FreeCAD.ActiveDocument.removeObject(ns)
                        FreeCAD.ActiveDocument.recompute()
                        #print new_edge_list
                    #stop
                #if len (not_supported)>0:
                #    Draft.downgrade(FreeCADGui.Selection.getSelection(),delete=False)
                #    stop
                #say (new_edge_list)
                #stop
                #sayerr(replace)
                #replace = re.sub('\s\(gr_arc(.+?Edge)\)\)\r\n|\(gr_line(.+?Edge)\)\)\r|\(gr_line(.+?Edge)\)\)\n','',replace, flags=re.MULTILINE)
                #replace = re.sub('\s\(gr_circle(.+?Edge)\)\)\r\n|\(gr_line(.+?Edge)\)\)\r|\(gr_line(.+?Edge)\)\)\n','',replace, flags=re.MULTILINE)
                #newcontent = re.sub('^\)','ENDOFFILE',replace, flags=re.MULTILINE)
                
                #newcontent = re.sub('^\)','',replace, flags=re.MULTILINE) #end of file
                #newcontent = re.sub('/\.(?=[^\(]*$)/','',replace, flags=re.MULTILINE) #end of file
                #newcontent = newcontent.replace(/\((?=[^.]*$)/, "")
                #newcontent = re.sub(r'(.*)\)', r'', replace, flags=re.MULTILINE)
                new_border=''
                #print new_edge_list
                ## maxRadius # 4000 = 4m max length for KiCad
                #edge_nbr=0
                sanitized_edge_list=[]
                for border in new_edge_list:
                    #print border # [0]
                    if 'arc' in border[0]:
                        #print border[0]
                        if abs(float(border[3])) > maxRadius:
                            #stop
                            #print 'too big radius= ',border[3]
                            #print 'border len= ', len(border)
                            #points=border [10].x
                            #p1x = float(border [10].x);p1y=float(border [10].y)
                            p1x = float("{0:.6f}".format(border [10].x));p1y=float("{0:.6f}".format(border [10].y))
                            #print p1x, ' ',p1y
                            #p2x = float(border [11].x);p2y=float(border [11].y)
                            p2x = float("{0:.6f}".format(border [11].x));p2y=float("{0:.6f}".format(border [11].y))
                            #print '1st point ', border [10],' 2nd point ', border [11]
                            sanitized_edge_list.append(['line',p1x,p1y,p2x,p2y])
                        else:
                            sanitized_edge_list.append(border)
                    else:
                        sanitized_edge_list.append(border)
                    #edge_nbr=edge_nbr+1
                #print sanitized_edge_list
                #stop
                #for border in new_edge_list:
                for border in sanitized_edge_list:
                    new_border=new_border+os.linesep+createEdge(border,offset,sklayer,pcb_version)
                    #sayw(createEdge(border))
                #stop
                new_edge=new_border+os.linesep+')'+os.linesep
                newcontent=newcontent+new_edge+u' '
            elif ssklayer == 'FillZone' or ssklayer == 'MaskZone':
                newcontent=newcontent+pushFillZone(skname,offset,sklayer)+os.linesep+')'+os.linesep+u' '
            else:
                newcontent=newcontent+pushFillZone(skname,offset,sklayer)+os.linesep+')'+os.linesep+u' '
            #print newcontent
            with codecs.open(fpath,'w', encoding='utf-8') as ofile:
                ofile.write(newcontent)
                ofile.close()        
            say_time()
            if ssklayer != 'FillZone' and ssklayer != 'MaskZone' and ssklayer != 'KeepOutZone':
                msg="""<b>new Edge pushed to kicad board!</b><br><br><br>"""
            elif ssklayer == 'FillZone':
                msg="""<b>new FillZone pushed to kicad board!</b><br>Edit the properties of the new FillZone in pcbnew<br>"""
            elif ssklayer == 'MaskZone':
                msg="""<b>new MaskZone pushed to kicad board!</b><br>Edit the properties of the new FillZone in pcbnew<br>"""
            elif ssklayer == 'KeepOutZone':
                msg="""<b>new KeepOutZone pushed to kicad board!</b><br>Edit the properties of the new KeepOutZone in pcbnew<br>"""
            msg+="<b>file saved to<br>"+fpath+"</b><br><br>"
            msg+="<i>backup file saved to<br>"+foname+"</i><br>"
            if ssklayer == 'Edge':
                msgr="new Edge pushed to kicad board!\n"
            else:
                msgr="new "+ssklayer+" pushed to kicad board!\n"
            msgr+="file saved to "+fpath+"\n"
            msgr+="backup file saved to "+foname
            lns=len (not_supported) 
            #print lns
            if lns > 2:
                if lns < 103: # writing only some geometry not supported
                    msg+="<br><b>found downgraded Geometry:<br>"+not_supported[:-2]+"!</b>"
                    msgr+="\nfound downgraded Geometry: "+not_supported[:-2]+"!"
                else:
                    nss=not_supported[:-2]
                    nss=nss[:101]+'... <br> ...'
                    msg+="<br><b>found downgraded Geometry:<br>"+nss+"</b>"
                    msgr+="\nfound downgraded Geometry: "+not_supported[:-2]+"!"
                
            say(msgr)
            say_info(msg)
            if not edge_pcb_exists and ssklayer != 'FillZone' and ssklayer != 'KeepOutZone':
                msg="<b>close your FC Sketch<br>and reload the kicad_pcb file</b>"
                say_warning(msg)
            if origin_warn:
                if aux_orig == 1:
                    origin_msg='AuxOrigin'
                elif grid_orig == 1:
                    origin_msg='GridOrigin'
                msg = origin_msg +' is set in FC Preferences but not set in KiCAD pcbnew file'
                sayw(msg)
                msg="""<b><font color='red'>"""+origin_msg+""" is set in FreeCAD Preferences<br>but not set in KiCAD pcbnew file</font></b>"""
                msg+="""<br><br>Please assign """+origin_msg+""" to your KiCAD pcbnew board file"""
                msg+="""<br>for a better Mechanical integration"""
                say_warning(msg)

    #def precision(self, value):
    #    return "%.2f" % float(value)
    
##
def find_sequence (elist,idx, min_dist):
    """find point sequence in two edges"""
    ep0 = elist[idx].Vertexes[0].Point
    ep1 = elist[idx].Vertexes[1].Point
    ep2 = elist[idx+1].Vertexes[0].Point
    ep3 = elist[idx+1].Vertexes[1].Point
    if distance(ep0,ep2) < min_dist:
        first_pnt = ep1
        common_pnt = ep0
        last_pnt = ep3
    elif distance(ep0,ep3) < min_dist:
        first_pnt = ep1
        common_pnt = ep3
        last_pnt = ep2
    elif distance(ep1,ep3) < min_dist:
        first_pnt = ep0
        common_pnt = ep1
        last_pnt = ep2
    elif distance(ep1,ep2) < min_dist:
        first_pnt = ep0
        common_pnt = ep1
        last_pnt = ep3
    else:
        msg="""<b><font color='red'>to push a FillZone or a KeepOutZone<br>you need a single closed Sketch!</font></b>"""
        say_warning(msg)
        stop
    return first_pnt, common_pnt, last_pnt
##
def pushFillZone(skn, ofs, keepout=None):
    shapes = []
    q_deflection = 0.005 #0.02 ##0.005
    tol = 0.01
    constr = 'coincident' #'all'
    if skn is None:
        sel = FreeCADGui.Selection.getSelection()
        for selobj in sel:
            for e in selobj.Shape.Edges:
                shapes.append(Part.makePolygon(e.discretize(QuasiDeflection=q_deflection)))
    else:
        selobj = FreeCAD.ActiveDocument.getObject(skn)
        for e in selobj.Shape.Edges:
            shapes.append(Part.makePolygon(e.discretize(QuasiDeflection=q_deflection)))
    Draft.makeSketch(shapes)
    sk_d = FreeCAD.ActiveDocument.ActiveObject
    if sk_d is not None:
        FreeCADGui.ActiveDocument.getObject(sk_d.Name).LineColor = (1.00,1.00,1.00)
        FreeCADGui.ActiveDocument.getObject(sk_d.Name).PointColor = (1.00,1.00,1.00)
        max_geo_admitted = 1500 # after this number, no recompute is applied
        if len (sk_d.Geometry) < max_geo_admitted:
            FreeCAD.ActiveDocument.recompute()
    import constrainator
    constrainator.add_constraints(sk_d.Name, tol, constr)
    skt = FreeCAD.ActiveDocument.getObject(sk_d.Name)
    if hasattr(skt, 'OpenVertices'):
        openVtxs = skt.OpenVertices
        if len(openVtxs) >0:
            FreeCAD.Console.PrintError("Open Vertexes found.\n")
            FreeCAD.Console.PrintWarning(str(openVtxs)+'\n')
            msg = """Open Vertexes found.<br>"""+str(openVtxs)
            reply = QtGui.QMessageBox.information(None,"info", msg)
            add_points=True
            if add_points:
                for v in openVtxs:
                    FreeCAD.ActiveDocument.addObject('PartDesign::Point','DatumPoint')
                    dp = FreeCAD.ActiveDocument.ActiveObject
                    dp.Placement = FreeCAD.Placement (FreeCAD.Vector(v[0],v[1],0), FreeCAD.Rotation(0,0,0), FreeCAD.Vector(0,0,0))
                    dp.Label = 'OpenVertexPointer'
    #FreeCADGui.ActiveDocument.getObject(sel[0].Name).Visibility=False
    shp = skt.Shape
    #ofs=[0.0,0.0]
    edge_width = 0.1 
    edges = shp.Edges
    segments_nbr=len(edges)
    if segments_nbr<3:
        stop
    if 'Fill' in keepout:
        fillzone = """  (zone (net 0) (net_name "") (layer """+keepout[:1]+""".Cu) (tstamp 0) (hatch edge 0.508)"""+os.linesep
        fillzone+="""    (connect_pads (clearance 0.508))"""+os.linesep
        fillzone+="""    (min_thickness 0.254)"""+os.linesep
        fillzone+="""    (fill yes (arc_segments 32) (thermal_gap 0.508) (thermal_bridge_width 0.508))"""+os.linesep
        fillzone+="""    (polygon"""+os.linesep
    elif 'Mask' in keepout:
        fillzone = """  (gr_poly"""+os.linesep
    elif 'KeepOut' in keepout: #keepout zone
        fillzone = """  (zone (net 0) (net_name "") (layers """+keepout[:1]+""".Cu) (tstamp 0) (hatch edge 0.508)"""+os.linesep
        fillzone+="""    (connect_pads (clearance 0.508))"""+os.linesep
        fillzone+="""    (min_thickness 0.254)"""+os.linesep
        fillzone+="""    (keepout (tracks not_allowed) (vias not_allowed) (copperpour not_allowed))"""+os.linesep
        fillzone+="""    (fill (arc_segments 32) (thermal_gap 0.508) (thermal_bridge_width 0.508))"""+os.linesep
        fillzone+="""    (polygon"""+os.linesep
    i=0
    pts = "      (pts "+os.linesep
    first_pnt, common_pnt, last_pnt = find_sequence (edges,i,tol)
    i+=1
    for e in edges[1:-1]:
        if 'Line' not in str(e.Curve):
            stop
        first_pnt, common_pnt, last_pnt = find_sequence (edges,i,tol)
        if i < segments_nbr:
            pts=pts+"         (xy {0:.3f} {1:.3f}) (xy {2:.3f} {3:.3f})".format(first_pnt.x+ofs[0], -first_pnt.y+ofs[1], common_pnt.x+ofs[0], -common_pnt.y+ofs[1])+os.linesep
        i=i+1
    pts=pts+"         (xy {0:.3f} {1:.3f})".format(last_pnt.x+ofs[0], -last_pnt.y+ofs[1])+os.linesep
    fillzone += pts
    if 'Mask' in keepout:
        fillzone+="      )"+os.linesep+"  (layer "+keepout[:6]+") (width 0.0))"+os.linesep
    else:
        fillzone+="      )"+os.linesep+"    )"+os.linesep+"  )"+os.linesep #+")"+os.linesep
    if sk_d is not None:
        FreeCAD.ActiveDocument.removeObject(sk_d.Name)
    #print(fillzone)
    #FreeCAD.ActiveDocument.commitTransaction()
    #with open(filename, "wb") as f:
    #    f.write(fillzone.encode('utf-8'))
    return fillzone
##
def pull3D2dsn(s,mdls,tsp,nMd,gof,pcbThickness):
    global start_time, aux_orig, grid_orig
    global board_base_point_x, board_base_point_y, real_board_pos_x, real_board_pos_y
    global off_x, off_y, maxRadius
    
    #sayw('pulling 3D model placement from pcb')
    doc=FreeCAD.ActiveDocument
    if gof and grid_orig==1:
        offset=[off_x,-off_y]
    #print(offset)
    if 0:
        model_3d_name = s.Label[s.Label.find('_')+1:s.Label.rfind('_')]
        model_3d_name = model_3d_name.replace('.','')
        #print (model_3d_name);stop
        nbrModel = None
        if s.Label.rfind('_') < s.Label.rfind('['):
            #ts = s.Label[s.Label.rfind('_')+1:s.Label.rfind('[')]
            nbrModel = s.Label[s.Label.rfind('['):]
            #print(nbrModel)
            nMd = int(nbrModel.replace('[','').replace(']',''))-1
        else:
            #ts = s.Label[s.Label.rfind('_')+1:]
            nMd = 0
            #print('nbrModel = 0')
    idxF=-1
    for i,mdl in enumerate (mdls):
        #print (mdl,nMd)
        #print(mdl[10],':', mdl[12]-1,':',nMd)
        if tsp in str(mdl[10]) and mdl[12]-1 == nMd:
            #print('FOUND',mdl[10],':', mdl[12],':',nMd)
            #if nMd == mdl[12]:
            idxF=i
            FLayer=1.
            #print(mdl[4])
            pos_x=mdl[1]-off_x
            pos_y=mdl[2]-off_y
            rot=mdl[3]
            mdl_layer=mdl[4]
            wrl_pos=mdl[6]
            wrl_rot=mdl[7]
            #print(mdl[10])
            #print(mdl[12])
            #print(wrl_pos)
            #print(wrl_rot)
            dummyshape = Part.Shape()
            print(s.Label,': model found! Placing it!')
            if 'Top' not in mdl_layer:
                FLayer=-1.
            if FLayer==1.:
                #ang = float(rot)
                #dummyshape.Placement = FreeCAD.Placement(FreeCAD.Vector(pos_x,pos_y,-pcbThickness),FreeCAD.Rotation(FreeCAD.Vector(0,1,0),180))
                ##FreeCAD.ActiveDocument.getObject(s.Name).Placement.Rotation=FreeCAD.Rotation(FreeCAD.Vector(0,0,1),ang)
                dummyshape.Placement=FreeCAD.Placement(FreeCAD.Vector(pos_x+float(wrl_pos[0])*25.4,pos_y+float(wrl_pos[1])*25.4,0+float(wrl_pos[2])*25.4),FreeCAD.Rotation(-float(wrl_rot[2]),-float(wrl_rot[1]),-float(wrl_rot[0]))) #rot is already rot fp -rot wrl
                dummyshape.rotate((pos_x,pos_y,0),(0,0,1),rot+float(wrl_rot[2]))
                FreeCAD.ActiveDocument.getObject(s.Name).Placement=dummyshape.Placement
                #bbpa=degrees(FreeCAD.ActiveDocument.getObject(s.Name).Placement.Rotation.Angle)
                #print(bbpa);#stop
                #if FreeCAD.ActiveDocument.getObject(s.Name).Placement.Rotation.Axis.z == -1:
                #    bbpa=-bbpa
                #new_angle=bbpa+z_rot
            else:
                #print('bottom')
                dummyshape.Placement=FreeCAD.Placement(FreeCAD.Vector(pos_x+float(wrl_pos[0])*25.4,pos_y+float(wrl_pos[1])*25.4,+pcbThickness+float(wrl_pos[2])*25.4),FreeCAD.Rotation(-float(wrl_rot[2]),-float(wrl_rot[1]),-float(wrl_rot[0]))) #rot is already rot fp -rot wrl
                dummyshape.rotate((pos_x,pos_y,0),(0,0,1),180+rot+float(wrl_rot[2]))
                dummyshape.rotate((pos_x,pos_y,0),(0,1,0),180)
                FreeCAD.ActiveDocument.getObject(s.Name).Placement=dummyshape.Placement
            #   bbpa=round(FreeCAD.ActiveDocument.getObject(s.Name).Placement.Rotation.toEuler()[0],1)
            break
#
##
def push3D2pcb(s,cnt,tsp):
    #global last_fp_path, test_flag, start_time
    #global configParser, configFilePath, start_time
    #global ignore_utf8, ignore_utf8_incfg, disable_PoM_Observer
    global start_time, aux_orig, grid_orig
    global board_base_point_x, board_base_point_y, real_board_pos_x, real_board_pos_y
    #global pcb_path, use_AppPart, force_oldGroups, use_Links
    #global original_filename, aux_orig, grid_orig
    global off_x, off_y, maxRadius
    
    #sayw('pushing 3D model moved to pcb')
    doc=FreeCAD.ActiveDocument
    data=u''.join(cnt)
    tstamp_found=False
    #if len(re.findall('\s\(tstamp(.+?)\)',data, re.MULTILINE|re.DOTALL))>0:
    #if len(re.findall('\s\(tstamp(\s'+s.TimeStamp+'.+?)\)',data, re.MULTILINE|re.DOTALL))>0:
    #if len(re.findall('\s\(tstamp(\s'+tsp+'.+?)\)',data, re.MULTILINE|re.DOTALL))>0:
    if len(re.findall('\s\(tstamp(\s.*'+tsp.lower()+'+\))',data,  re.MULTILINE|re.DOTALL))>0 or \
        len(re.findall('\s\(tstamp(\s.*'+tsp.upper()+'+\))',data,  re.MULTILINE|re.DOTALL))>0:  #kv6 puts tstamp in lower case
    #if len(re.findall('\s\(tstamp(\s'+tsp+'.+?)\)',data, re.MULTILINE|re.DOTALL))>0:
        tstamp_found=True
        #old_pos=re.findall('\s\(tstamp(\s'+sel[0].TimeStamp+'.+?'+'\(at'+'\s.+?)\)',data, re.MULTILINE|re.DOTALL)[0]
        #print (old_pos)
        # new_pos=old_pos.split('(at')[0]+'(at 1.23 5.67 890'
    if tstamp_found:
        oft=None
        if aux_orig == 1:
            oft=getAuxOrigin(data)
        if grid_orig == 1:
            oft=getGridOrigin(data)
        #print oft
        gof=False
        if oft is not None:
            off_x=oft[0];off_y=-oft[1]
            offset = oft
            gof=True
        bbpx=FreeCAD.ActiveDocument.getObject(s.Name).Placement.Base[0]
        bbpy=FreeCAD.ActiveDocument.getObject(s.Name).Placement.Base[1]
        offset=[bbpx,bbpy]
        #print(bbpx);print(bbpy);print(bbpa)
        if gof and grid_orig==1:
            offset=[off_x,-off_y]
        #print(offset)
        #print (bbpx+off_x);print (-1*(bbpy+off_y))
        model_3d_name = s.Label[s.Label.find('_')+1:s.Label.rfind('_')]
        model_3d_name = model_3d_name.replace('.','')
        #print (model_3d_name);stop
        if s.Label.rfind('_') < s.Label.rfind('['):
            #ts = s.Label[s.Label.rfind('_')+1:s.Label.rfind('[')]
            nbrModel = s.Label[s.Label.rfind('['):]
            nMd = int(nbrModel.replace('[','').replace(']',''))-1
        else:
            #ts = s.Label[s.Label.rfind('_')+1:]
            nMd = 0
        idxF=-1
        for i,ln in enumerate (cnt):
            #if '(tstamp '+s.TimeStamp in ln:
            #if '(tstamp '+tsp in ln:
            if '(tstamp ' in ln:
                if tsp in ln:
                    idxF=i
                    #print(ln)
        FLayer=1.
        if idxF>=0:
            print(s.Label)
            sayw('pushing 3D model moved to pcb')
            if 'Front' not in cnt[idxF]:
                FLayer=-1.
            if FLayer==1.:
                bbpa=degrees(FreeCAD.ActiveDocument.getObject(s.Name).Placement.Rotation.Angle)
                #print(bbpa);#stop
                if FreeCAD.ActiveDocument.getObject(s.Name).Placement.Rotation.Axis.z == -1:
                    bbpa=-bbpa
                #new_angle=bbpa+z_rot
            else:
                bbpa=round(FreeCAD.ActiveDocument.getObject(s.Name).Placement.Rotation.toEuler()[0],1)
                #new_angle=bbpa+z_rot
            #say (content[idxF+1])
            #if 'Front' not in cnt[idxF]:
            #    FLayer=-1.
            mod_old_angle = 0
            mod_old_values = cnt[idxF+1].split('(at ')[1].split(' ')
            #sayw(mod_old_values)
            if len(mod_old_values) == 3:
                mod_old_angle= (mod_old_values[2].split(')'))[0]
                mod_old_angle = mod_old_angle.replace(' ','')
                #print (mod_old_angle)
                if len(mod_old_angle) > 0:
                    mod_old_angle=float("{0:.3f}".format(float(mod_old_angle)))
                else:
                    mod_old_angle = 0
            #say ('module old angle '+str(mod_old_angle))
            nbr_spaces = len(cnt[idxF+1]) - len(cnt[idxF+1].lstrip())
            #new_pos="{0:.3f}".format(bbpx+off_x)+" "+"{0:.3f}".format(-1*(bbpy+off_y))+\
            #        " "+"{0:.3f}".format(bbpa)+")"
#                    " "+"{0:.3f}".format(bbpa-mod_old_angle)+")"
            #print(new_pos)
            ##cnt[idxF+1]=" " * nbr_spaces + '(at '+new_pos+os.linesep
            #say (content[idxF+1])
            looping=True;ik=0
            pads_2rot=[];old_ref_angle=None;old_val_angle=None;old_usr_angle=None
            nMdCnt = 0
            while looping and (idxF+ik) < len(cnt):
            #for ln in content[idxF+1:]:
                ik+=1
                ln = cnt[idxF+ik]
                if '(model' in ln:
                    if nMdCnt==nMd:
                        #looping=False
                        ##if model_3d_name in ln.replace('.',''): #removing '.' not imported by STEP
                            #print(ln);print(cnt[idxF+ik+3]);stop
                        #print(ln);print(cnt[idxF+ik+3]);print(nMdCnt)#;stop
                        ln_r=cnt[idxF+ik+1]
                        #      (offset (xyz -1.27 0 0)) mm
                        #      (at (xyz -1.27/25.4 0 0)) decimils
                        if 'at' in ln_r: 
                            k=25.40
                        else:
                            k=1.0
                        ido = ln_r.find('xyz');ofs=ln_r[ido+3:] #lstrip('xyz')
                        ido = ofs.find('))');ofs=ofs[:ido] 
                        ofs = ofs.lstrip(' ').split(' ')
                        #sayerr(ofs)
                        if len(ofs)==3:
                            x_o=float(ofs[0])*k
                            y_o=float(ofs[1])*k
                            z_o=float(ofs[2])*k
                        else:
                            x_o=0;y_o=0;z_o=0
                        #sayw(ofs)
                        ln_r=cnt[idxF+ik+3]
                        #      (rotate (xyz 0 0 0))
                        #print(ln_r)#;stop
                        idz = ln_r.find('xyz');z_rot=ln_r[idz+3:] #lstrip('xyz')
                        idz = z_rot.find('))');z_rot=z_rot[:idz] 
                        #z_rot = z_rot.rstrip('))')
                        z_rot = z_rot.lstrip(' ').split(' ')
                        #sayerr(z_rot)
                        if len(z_rot)==3:
                            z_rot=float(z_rot[2])
                        else:
                            z_rot=0
                        #print(z_rot);stop
                        #sayw(z_rot)
                        looping=False
                    else:
                        nMdCnt+=1
                if '(pad' in ln:
                    #print (ln)
                    #print (ln.split('(at ')[1].split(')')[0].split(' '))
                    pad_values=ln.split('(at ')[1].split(')')[0].split(' ')
                    if len(pad_values) == 3:
                        #print(pad_values[2])
                        old_pad_angle = (float(pad_values[2]))
                    else:
                        old_pad_angle = 0
                    base_pad_angle = old_pad_angle - mod_old_angle
                    id_pad = idxF+ik
                    pads_2rot.append([base_pad_angle,id_pad,pad_values])
                    #print(content[idxF+ik])
                if '(fp_text reference' in ln:
                    #print (ln)
                    #print (ln.split('(at ')[1].split(')')[0].split(' '))
                    ref_values=ln.split('(at ')[1].split(')')[0].split(' ')
                    old_ref_angle = 0
                    if len(ref_values) == 3:
                        #print(pad_values[2])
                        print(ref_values[2])
                        if ref_values[2] != 'unlocked':
                            old_ref_angle = (float(ref_values[2]))
                    #else:
                    #    old_ref_angle = 0
                    #print (pad_values);print(ln.split('(at '))
                    idx_ref=idxF+ik
                if '(fp_text value' in ln:
                    #print (ln)
                    #print (ln.split('(at ')[1].split(')')[0].split(' '))
                    val_values=ln.split('(at ')[1].split(')')[0].split(' ')
                    old_val_angle = 0
                    if len(val_values) == 3:
                        #print(pad_values[2])
                        if val_values[2] != 'unlocked':
                            old_val_angle = (float(val_values[2]))
                    #else:
                    #    old_val_angle = 0
                    base_val_angle = old_val_angle - mod_old_angle
                    new_val_angle = ' '+("{0:.3f}".format(base_val_angle + bbpa))
                    if float(new_val_angle) == 0:
                        new_val_angle=''
                    #print (pad_values);print(ln.split('(at '))
                    idx_val=idxF+ik
                    cnt[idxF+ik] = ln.split('(at ')[0]+'(at ' + val_values[0] +' '+ val_values[1]+new_val_angle+ln[ln.index(')'):]
                if '(fp_text user' in ln:
                    #print (ln)
                    #print (ln.split('(at ')[1].split(')')[0].split(' '))
                    usr_values=ln.split('(at ')[1].split(')')[0].split(' ')
                    old_usr_angle = 0
                    if len(usr_values) == 3:
                        #print(pad_values[2])
                        if usr_values[2] != 'unlocked':
                            old_usr_angle = (float(usr_values[2]))
                    #else:
                    #    old_usr_angle = 0
                    base_usr_angle = old_usr_angle - mod_old_angle
                    new_usr_angle = ' '+("{0:.3f}".format(base_usr_angle + bbpa))
                    if float(new_usr_angle) == 0:
                        new_usr_angle=''
                    #print (pad_values);print(ln.split('(at '))
                    idx_usr=idxF+ik
                    cnt[idxF+ik] = ln.split('(at ')[0]+'(at ' + usr_values[0] +' '+ usr_values[1]+new_usr_angle+ln[ln.index(')'):]
            #adjusting footprint
            if FLayer==1.:
                new_angle=bbpa+z_rot
            else:
                new_angle=(bbpa-z_rot) # 180+(bbpa+z_rot)
            #new_angle=bbpa+z_rot
            if "{0:.3f}".format(new_angle) == '-0.00' or "{0:.3f}".format(new_angle) == '0.00':
                new_angle_str=''
            else:
                new_angle_str = ' '+"{0:.3f}".format(new_angle)
            new_pos="{0:.3f}".format(bbpx+off_x-x_o*FLayer)+" "+"{0:.3f}".format(-1*(bbpy+off_y-y_o*FLayer))\
                    +new_angle_str+")"
             #print(new_pos)
            cnt[idxF+1]=" " * nbr_spaces + '(at '+new_pos+os.linesep
            #adjusting reference
            if old_ref_angle is not None:
                base_ref_angle = old_ref_angle - mod_old_angle # - z_rot
                new_ref_angle = ' '+("{0:.3f}".format(base_ref_angle + bbpa + z_rot))
                if float(new_ref_angle) == 0:
                    new_ref_angle=''
                ln=cnt[idx_ref]
                cnt[idx_ref] = ln.split('(at ')[0]+'(at ' + ref_values[0] +' '+ ref_values[1]+new_ref_angle+ln[ln.index(')'):]
            if old_val_angle is not None:
                base_val_angle = old_ref_angle - mod_old_angle # 
                new_val_angle = ' '+("{0:.3f}".format(base_val_angle + bbpa + z_rot))
                if float(new_val_angle) == 0:
                    new_val_angle=''
                ln=cnt[idx_val]
                cnt[idx_val] = ln.split('(at ')[0]+'(at ' + val_values[0] +' '+ val_values[1]+new_val_angle+ln[ln.index(')'):]
            if old_usr_angle is not None:
                base_usr_angle = old_usr_angle - mod_old_angle # 
                new_usr_angle = ' '+("{0:.3f}".format(base_usr_angle + bbpa + z_rot))
                if float(new_usr_angle) == 0:
                    new_usr_angle=''
                ln=cnt[idx_usr]
                cnt[idx_usr] = ln.split('(at ')[0]+'(at ' + usr_values[0] +' '+ usr_values[1]+new_usr_angle+ln[ln.index(')'):]
                #print(new_ref_angle);print(old_ref_angle);print(z_rot);print(bbpa);print(base_ref_angle+bbpa);stop
            for p2r in pads_2rot:
                new_pad_angle = ' '+("{0:.3f}".format(p2r[0] + bbpa + z_rot))
                if float(new_pad_angle) == 0:
                    new_pad_angle=''
                #print (pad_values);print(ln.split('(at '))
                ln  = cnt[p2r[1]]
                pad_val = p2r[2]
                cnt[p2r[1]] = ln.split('(at ')[0]+'(at ' + pad_val[0] +' '+ pad_val[1]+new_pad_angle+ln[ln.index(')'):]                    
            #stop # 'we need to search for pads in module and add rotation angle each'
        #stop
        #newdata=u''.join(content)
        newcontent=cnt
        #print newcontent
    else:
        msg="<b>footprint TimeStamp not found!<br>Please reload the kicad_pcb file</b>"
        say_warning(msg)
        newcontent=cnt
    # with codecs.open(fpath,'w', encoding='utf-8') as ofile:
    #     ofile.write(newcontent)
    #     ofile.close()        
    # say_time()
    # msg="""<b>3D model new position pushed to kicad board!</b><br><br>"""
    # if found_tracks:
    #     msg+="<font color='red'><b>tracks found!<br></b>you will need to fix your routing!</font><br><br>"
    # msg+="<b>file saved to<br>"+fpath+"</b><br><br>"
    # msg+="<i>backup file saved to<br>"+foname+"</i><br>"
    # msgr="3D model new position pushed to kicad board!\n"
    # msgr+="file saved to "+fpath+"\n"
    # msgr+="backup file saved to "+foname
    # say(msgr)
    # #say_info(msg)
    return newcontent        
##


#!# KSUWidget.activateWindow()
#!# KSUWidget.raise_()
#!# KSUWidget.hide()

def getComboView(self,window):
    """ Returns the main Tab.
    """
    dw=window.findChildren(QtGui.QDockWidget)
    for i in dw:
        if str(i.objectName()) == "Combo View":
            return i.findChild(QtGui.QTabWidget)
    raise Exception("No tab widget found")

# QDockWidget::setFloating (false)
# KSUWidget.setFloating(True)  #undock
#KSUWidget.setFloating(False)  #dock

#KSUWidget.setStyleSheet('QPushButton { border: 1px solid #5a5a5a;border-radius: 0px;min-width: 50px;min-height: 20px;padding: 1px 2px;}')
#KSUWidget.setStyleSheet('QPushButton:hover,QPushButton:focus { color: white; border-color: #3874f2; background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #5e90fa, stop:1 #3874f2);}')

# print QtGui.QApplication.style().metaObject().className()    # 
# print KSUWidget.style().metaObject().className()    # 
# print QtGui.QApplication.instance().styleSheet()    # list all applied styles    

# try:
#     if KSUWidget.style().metaObject().className()== "QStyleSheetStyle":
#         KSUWidget.setStyleSheet('QPushButton {border-radius: 0px; padding: 1px 2px;}')
# except:
#     pass
## QtGui.QFont().setPointSize(font_size) ???? to evaluate if still is necessary
   
#Ui_DockWidget().destroyed.connect(onDestroy())
## KSUWidget.installEventFilter(KSUWidget)

## form = RotateXYZGuiClass()
## #rotate = rotate_gui()
## form.setObjectName("kicadStepUp")
## 
## if QtGui.QApplication.style().metaObject().className() == "QStyleSheetStyle":
##     form.setStyleSheet('QPushButton {border-radius: 0px; padding: 1px 2px;}')


