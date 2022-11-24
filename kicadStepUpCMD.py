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

#****************************************************************************
#*                                                                          *
#*  kicadStepUpCMD.py - FreeCAD Workbench "Command" classes                 *
#*                                                                          *
#*   Each command definition here follows the structure described by:       *
#*      https://wiki.freecadweb.org/Workbench_creation                      *
#*                                                                          *
#*                                                                          *
#*                                                                          *
#*                                                                          *
#*                                                                          *
#****************************************************************************


__KTS_FILE_VER__  = "2.2.9"
__KTS_FILE_NAME__ = "KICADSTEPUPCMD"

from kts_PrefsMgmt import prefs_set_file_version
prefs_set_file_version(__KTS_FILE_NAME__, __KTS_FILE_VER__)



import FreeCAD, FreeCADGui, Part
from FreeCAD import Base
import imp, os, sys, tempfile, re
import Draft, DraftGeomUtils  #, OpenSCAD2Dgeom
from PySide import QtGui, QtCore
QtWidgets = QtGui

from pivy import coin
from threading import Timer

import kts_Locator
# from kicadStepUptools import onLoadBoard, onLoadFootprint
import math
from math import sqrt

import constrainator
from constrainator import add_constraints, sanitizeSkBsp

ksuCMD_version__='2.2.9'


precision = 0.1 # precision in spline or bezier conversion
q_deflection = 0.02 # quasi deflection parameter for discretization

hide_compound = True

reload_Gui=False#True

a3 = False
try:
    from freecad.asm3 import assembly as asm
    FreeCAD.Console.PrintWarning('A3 available\n')
    a3 = True
except:
    # FreeCAD.Console.PrintWarning('A3 not available\n')
    a3 = False

try:
    from PathScripts.PathUtils import horizontalEdgeLoop
    from PathScripts.PathUtils import horizontalFaceLoop
    from PathScripts.PathUtils import loopdetect
    import PathCommands
except:
    FreeCAD.Console.PrintError('Path WB not found\n')

def reload_lib(lib):
    if (sys.version_info > (3, 0)):
        import importlib
        importlib.reload(lib)
    else:
        reload (lib)

use_outerwire = False #False #True
remove_shapes = True #False #True 
hide_objects = True #False # True
use_draft = True #False  # use Draft.makesketch
attach_sketch = False #True
create_plane = False# True #False

conv_started = False

global max_geo_admitted
max_geo_admitted = 1500 # after this number, no recompute is applied


def P_Line(prm1,prm2):
    if hasattr(Part,"LineSegment"):
        return Part.LineSegment(prm1, prm2)
    else:
        return Part.Line(prm1, prm2)

def fuse_objs(GuiObjSel):
    objList= []
    for s in GuiObjSel:
        objList.append(s.Object)
    FreeCAD.ActiveDocument.addObject("Part::MultiFuse","MultiFuse")
    MultiFuseName = FreeCAD.ActiveDocument.ActiveObject.Name
    FreeCAD.ActiveDocument.getObject(MultiFuseName).Shapes = objList
    # [App.activeDocument().Part__Feature002,App.activeDocument().Part__Feature003,App.activeDocument().Part__Feature004,App.activeDocument().Part__Feature005,App.activeDocument().Part__Feature006,App.activeDocument().Part__Feature007,App.activeDocument().Part__Feature008,App.activeDocument().Part__Feature009,App.activeDocument().Part__Feature010,App.activeDocument().Part__Feature011,]
    FreeCAD.ActiveDocument.recompute()
    return MultiFuseName
#

def rmvsubtree(objs):
    def addsubobjs(obj,toremoveset):
        toremove.add(obj)
        if hasattr(obj,'OutList'):
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
                toremove.remove(obj)
                break
        else:
            checkinlistcomplete = True
    for obj in toremove:
        try:
            obj.Document.removeObject(obj.Name)
        except:
            pass
###
def info_msg(msg):
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
##

ksuWBpath = os.path.dirname(kts_Locator.__file__)
#sys.path.append(ksuWB + '/Gui')
ksuWB_icons_path =  os.path.join( ksuWBpath, 'Resources', 'icons')

#__dir__ = os.path.dirname(__file__)
#iconPath = os.path.join( __dir__, 'Resources', 'icons' )


def ksu_edges2sketch():
    global conv_started, max_geo_admitted
    
    cp_edges = [];cp_edges_names = []
    cp_edges_shapes = []; cp_edges_obj = []
    cp_obj = []; cp_obj_name = []
    cp_points = []; cp_faces = []
    wires = []
    doc=FreeCAD.ActiveDocument
    docG = FreeCADGui.ActiveDocument
    en = None
    selEx=FreeCADGui.Selection.getSelectionEx()
    import Draft
    if len (selEx) > 0:
        for selEdge in selEx:
            if not (conv_started):
                doc.openTransaction('e2sk')
                conv_started = True
            for i,e in enumerate(selEdge.SubObjects):
                if 'Edge' in selEdge.SubElementNames[i]:
                    cp_edges.append(e)
                    #cp_edges_shapes.append(e.toShape())
                    Part.show(Part.Wire(e))
                    cp = doc.ActiveObject
                    cp_edges_obj.append(cp)
                    #print(cp)
                    cp_edges_names.append(selEdge.ObjectName+'.'+selEdge.SubElementNames[i])
                    cp_obj.append(selEdge.Object)
                    cp_edges_shapes.append(selEdge.Object.Shape)
                    cp_obj_name.append(selEdge.ObjectName)
                    if create_plane:
                        for v in cp.Shape.Vertexes[:3]: #selEdge.Object.Shape.Vertexes[:3]:
                            if v.Point not in cp_points:
                                cp_points.append(v.Point)
                            if len (cp_points) > 2:
                                    break
                    #FreeCAD.Console.PrintMessage(selEdge.ObjectName);FreeCAD.Console.PrintMessage('\n')
                    FreeCAD.Console.PrintMessage(selEdge.ObjectName+'.'+selEdge.SubElementNames[i])
                    FreeCAD.Console.PrintMessage('\n')
                    if hide_objects:
                        docG.getObject(selEdge.ObjectName).Visibility = False
                    #FreeCAD.Console.PrintMessage(e);FreeCAD.Console.PrintMessage('\n')
                    #cp_e = Part.show(Part.Wire(e))
                    wire = Part.Wire(e)
                    #cp_edges_shapes.append(wire.toShape())
                    wires.append (wire)
                elif 'Face'  in selEdge.SubElementNames[i]:
                    #o.Shape.Faces
                    cp_faces.append(e)
                    if use_outerwire:
                        ow=e.OuterWire
                        wires.append (ow)
                        #es = ow.Edges
                        for _e in ow.Edges:
                            cp_edges.append(_e)
                        Part.show(ow)
                        cp = doc.ActiveObject
                        cp_edges_obj.append(cp)
                        if create_plane:
                            for v in cp.Vertexes[:3]: #selEdge.Object.Shape.Vertexes[:3]:
                                print('point')
                                if v.Point not in cp_points:
                                    cp_points.append(v.Point)
                                if len (cp_points) > 2:
                                    break
                    else:    
                        ws=e.Wires
                        wires.append (ws)
                        #es=e.Edges
                        if create_plane:
                            for v in e.Vertexes[:3]: #selEdge.Object.Shape.Vertexes[:3]:
                                print(v.Point)
                                if len (cp_points) > 2:
                                    break
                                if v.Point not in cp_points:
                                    cp_points.append(v.Point)
                        for w in ws:
                            for _e in w.Edges:
                                cp_edges.append(_e)
                            Part.show(w)
                            cp = doc.ActiveObject
                            cp_edges_obj.append(cp)
                    if hide_objects:
                        docG.getObject(selEdge.ObjectName).Visibility = False
                    #for ed in es:
                    #    Part.show(ed)
                elif 'Vertex'  in selEdge.SubElementNames[i]:
                    #print(selEdge.SubElementNames[i])
                    #print(selEdge.Object.Shape.Volume)
                    if selEdge.Object.Shape.Volume == 0:
                        print('outline selected')
                        #for _e in selEdge.Object.Shape.Edges:
                        #    Part.show(_e.Curve.toShape())
                        #    cp_edges.append(_e)
                        #    cp_edges_shapes.append(e.toShape())
                        #    Part.show(Part.Wire(_e))
                        #    cp = doc.ActiveObject
                        #    cp_edges_obj.append(cp)
                        cp_edges_obj.append(selEdge.Object.Shape.copy())
                        if hide_objects:
                            docG.getObject(selEdge.ObjectName).Visibility = False
                    
        if len (cp_edges_obj) >0: # (wires) >0:
            if not (use_draft):
                FreeCAD.activeDocument().addObject('Sketcher::SketchObject','Sketch')
                #FreeCAD.activeDocument().Sketch.MapMode = "ObjectXY"
                #doc.recompute()
                sketch = doc.ActiveObject
                sketch.Label = "Sketch_converted"
            if len (cp_edges_obj) > 1:
                doc.addObject("Part::MultiFuse","union")
                union = doc.ActiveObject
                doc.union.Shapes = cp_edges_obj #cp_obj # [doc.Shape005,doc.Shape006]
                if len (cp_edges_obj) < max_geo_admitted:
                    doc.recompute()
            else:
                union = cp_edges_obj[0]
            #sketch.MapMode = "ObjectXZ"
            #sketch.Support = [(doc.Cut,'Face2')]
            #sketch.MapMode = 'FlatFace'
            # doc.recompute()
            #Draft.makeSketch([wire],addTo=sketch)
            # points = 
            #print(cp_points)
            triple = []
            if len (cp_points) > 2:
                for p in cp_points:
                    if p not in triple:
                        triple.append(p)
                face= Part.Face(Part.makePolygon([p for p in triple], True))
            else:
                for _e in cp_edges:
                    if _e.isClosed():
                        face = Part.Face(Part.Wire(_e))
            #print (triple)
            #plane = Part.Plane(*[p for p in triple])
            #print([p for p in triple])
            if create_plane:
                doc.addObject('Part::Feature','Face').Shape=face
                newface = doc.ActiveObject
            #[App.ActiveDocument.union.Shape.Vertex2.Point, App.ActiveDocument.union.Shape.Vertex5.Point, App.ActiveDocument.union.Shape.Vertex1.Point, ], True))
            #print(plane)
            ## _makeSketch(plane,wires,addTo=sketch)
            #Draft.makeSketch(wires,addTo=sketch)
            _objs_ = []
            use_workaround_1 = False
            use_workaround_2 = False
            active_view = FreeCADGui.ActiveDocument.activeView()
            rotation_view = active_view.getCameraOrientation()
            top_rotation = FreeCAD.Rotation(0.0,0.0,0.0,1.0)
            if rotation_view != top_rotation and len(union.Shape.Edges) < max_geo_admitted:
                use_workaround_1 = True
                use_workaround_2 = True
            if use_workaround_1:
                FreeCAD.Console.PrintWarning('workaround to avoid issues in Draft.makeSketch from Bottom\n')
                _objs_ = Draft.downgrade(FreeCAD.ActiveDocument.getObject('union'), delete=False)
                FreeCAD.ActiveDocument.recompute()
                _objs_ = []
                _objs_ = Draft.upgrade(FreeCADGui.Selection.getSelection(), delete=True)
                _objs_ = []
                FreeCAD.ActiveDocument.recompute()
                _objs_ = Draft.downgrade(FreeCADGui.Selection.getSelection(), delete=True)
                sel_objs = FreeCADGui.Selection.getSelection()
            if use_draft:
                #Draft.makeSketch(union,addTo=sketch)
                if use_workaround_1:
                    Draft.makeSketch(FreeCADGui.Selection.getSelection(),autoconstraints=True) #,addTo=sketch)
                else:
                    Draft.makeSketch(union,autoconstraints=True) #,addTo=sketch)
                sketch = doc.ActiveObject
                p = sketch.Placement
                # print(p)
                # print(p.Rotation.Axis)
                if use_workaround_2 and p.Rotation.Axis.z != 1:
                    FreeCAD.Console.PrintWarning('workaround on Axis to avoid issues in Draft.makeSketch\n')
                    p.Rotation.Axis.x = 0
                    p.Rotation.Axis.y = 0
                    p.Rotation.Axis.z = 1
                    p.Base.x = 0
                    p.Base.y = 0
                    p.Base.z = 1
                    # print(p)
                sketch.Label = "Sketch_converted"
            else:
                for _e in union.Shape.Edges:
                    if isinstance(_e.Curve,Part.Line) or isinstance(_e.Curve,Part.LineSegment):
                        sketch.addGeometry(P_Line(Base.Vector(_e.firstVertex().Point), Base.Vector(_e.lastVertex().Point)))
                    #sketch.addGeometry(_e.Curve)
            sk = doc.ActiveObject
            if attach_sketch:
                sketch.Support = [newface, 'Face1']
                sketch.MapMode = 'FlatFace'
            #sk.Placement = union.Placement
            if remove_shapes:
                rmvsubtree([union])
                if use_workaround_1:
                    for o in sel_objs:
                        FreeCAD.ActiveDocument.removeObject(o.Name)
                if create_plane:
                    rmvsubtree([newface])
            sketch.MapMode = 'Deactivated'
            # for e in cp_edges:
            #     sketch.addGeometry(e.Curve, False)
            #     print ('e added')
            for i in range(0, len(sketch.Geometry)):
                try: 
                    g = str(sketch.Geometry[i])
                    if 'BSpline' in g or 'Ellipse' in g:
                        sketch.exposeInternalGeometry(i)
                except:
                    #print 'error'
                    pass
            docG.getObject(sketch.Name).LineColor = (1.00,1.00,1.00)
            docG.getObject(sketch.Name).PointColor = (1.00,1.00,1.00)
            #print(docG.getObject(sketch.Name).PointColor)
            lg = len(sketch.Geometry)
            if lg == 0:
                doc.removeObject(sketch.Name)
                docG.getObject(selEdge.ObjectName).Visibility = True
                QtGui.QApplication.restoreOverrideCursor()
                reply = QtGui.QMessageBox.information(None,"info", "All Shapes must be co-planar")
                doc.abortTransaction()
            else:
                for s in FreeCADGui.Selection.getSelection():
                    FreeCADGui.Selection.removeSelection(s)
                FreeCADGui.Selection.addSelection(sketch)
                doc.commitTransaction()
            conv_started = False
            if lg < max_geo_admitted:
                doc.recompute()
    # for ob in FreeCAD.ActiveDocument.Objects:
    #     FreeCADGui.Selection.removeSelection(ob)
##
class Ui_Offset_value(object):
    def setupUi(self, Offset_value):
        Offset_value.setObjectName("Offset_value")
        Offset_value.resize(292, 177)
        Offset_value.setWindowTitle("Offset value")
        Offset_value.setToolTip("")
        self.buttonBoxLayer = QtWidgets.QDialogButtonBox(Offset_value)
        self.buttonBoxLayer.setGeometry(QtCore.QRect(10, 130, 271, 32))
        self.buttonBoxLayer.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBoxLayer.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBoxLayer.setObjectName("buttonBoxLayer")
        self.gridLayoutWidget = QtWidgets.QWidget(Offset_value)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 10, 271, 101))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.offset_label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.offset_label.setMinimumSize(QtCore.QSize(0, 0))
        self.offset_label.setToolTip("")
        self.offset_label.setText("Offset [+/- mm]:")
        self.offset_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.offset_label.setObjectName("offset_label")
        self.gridLayout.addWidget(self.offset_label, 0, 0, 1, 1)
        self.lineEdit_offset = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.lineEdit_offset.setToolTip("Offset value [+/- mm]")
        self.lineEdit_offset.setText("0.16")
        self.lineEdit_offset.setObjectName("lineEdit_offset")
        self.gridLayout.addWidget(self.lineEdit_offset, 0, 1, 1, 1)
        self.checkBox = QtWidgets.QCheckBox(self.gridLayoutWidget)
        self.checkBox.setToolTip("Arc or Intersection Offset method")
        self.checkBox.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.checkBox.setText("Arc")
        self.checkBox.setChecked(True)
        self.checkBox.setObjectName("checkBox")
        self.gridLayout.addWidget(self.checkBox, 2, 0, 1, 1)
        
        self.offset_label_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.offset_label_2.setMinimumSize(QtCore.QSize(0, 0))
        self.offset_label_2.setToolTip("")
        self.offset_label_2.setText("Offset Y [mm]:")
        self.offset_label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.offset_label_2.setObjectName("offset_label_2")
        self.gridLayout.addWidget(self.offset_label_2, 1, 0, 1, 1)
        self.lineEdit_offset_2 = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.lineEdit_offset_2.setToolTip("Offset Y value [+/- mm]")
        self.lineEdit_offset_2.setText("5.0")
        self.lineEdit_offset_2.setObjectName("lineEdit_offset_2")
        self.gridLayout.addWidget(self.lineEdit_offset_2, 1, 1, 1, 1)

        self.retranslateUi(Offset_value)
        self.buttonBoxLayer.accepted.connect(Offset_value.accept)
        self.buttonBoxLayer.rejected.connect(Offset_value.reject)
        QtCore.QMetaObject.connectSlotsByName(Offset_value)

    def retranslateUi(self, Offset_value):
        pass

##
#
# class SMExtrudeCommandClass():
#   """Extrude face"""
# 
#   def GetResources(self):
#     return {'Pixmap'  : os.path.join( iconPath , 'SMExtrude.svg') , # the name of a svg file available in the resources
#             'MenuText': "Extend Face" ,
#             'ToolTip' : "Extend a face along normal"}
class Ui_CDialog(object):
    def setupUi(self, CDialog):
        CDialog.setObjectName("CDialog")
        CDialog.resize(317, 302)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Sketcher_LockAll.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        CDialog.setWindowIcon(icon)
        CDialog.setToolTip("")
        CDialog.setStatusTip("")
        CDialog.setWhatsThis("")
        self.buttonBox = QtGui.QDialogButtonBox(CDialog)
        self.buttonBox.setGeometry(QtCore.QRect(8, 255, 207, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.Label_howto = QtGui.QLabel(CDialog)
        self.Label_howto.setGeometry(QtCore.QRect(20, 5, 265, 61))
        self.Label_howto.setToolTip("Select a Sketch and Parameters\n"
"to constraint the sketch\n"
"NB the Sketch will be modified!")
        self.Label_howto.setStatusTip("")
        self.Label_howto.setWhatsThis("")
        self.Label_howto.setText("<b>Select a Sketch and Parameters to<br>constrain the sketch.<br>NB the Sketch will be modified!</b>")
        self.Label_howto.setObjectName("Label_howto")
        self.Constraints = QtGui.QGroupBox(CDialog)
        self.Constraints.setGeometry(QtCore.QRect(10, 70, 145, 166))
        self.Constraints.setToolTip("")
        self.Constraints.setStatusTip("")
        self.Constraints.setWhatsThis("")
        self.Constraints.setTitle("Constraints")
        self.Constraints.setObjectName("Constraints")
        self.verticalLayoutWidget = QtGui.QWidget(self.Constraints)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(12, 20, 125, 137))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.all_constraints = QtGui.QRadioButton(self.verticalLayoutWidget)
        self.all_constraints.setMinimumSize(QtCore.QSize(92, 64))
        self.all_constraints.setToolTip("Lock Coincident, Horizontal\n"
"and Vertical")
        self.all_constraints.setText("")
        self.all_constraints.setIcon(icon)
        self.all_constraints.setIconSize(QtCore.QSize(48, 48))
        self.all_constraints.setChecked(True)
        self.all_constraints.setObjectName("all_constraints")
        self.verticalLayout.addWidget(self.all_constraints)
        self.coincident = QtGui.QRadioButton(self.verticalLayoutWidget)
        self.coincident.setMinimumSize(QtCore.QSize(92, 64))
        self.coincident.setToolTip("Lock Coincident")
        self.coincident.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("Sketcher_LockCoincident.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.coincident.setIcon(icon1)
        self.coincident.setIconSize(QtCore.QSize(48, 48))
        self.coincident.setChecked(False)
        self.coincident.setObjectName("coincident")
        self.verticalLayout.addWidget(self.coincident)
        self.Tolerance = QtGui.QGroupBox(CDialog)
        self.Tolerance.setGeometry(QtCore.QRect(166, 70, 141, 91))
        self.Tolerance.setToolTip("")
        self.Tolerance.setStatusTip("")
        self.Tolerance.setWhatsThis("")
        self.Tolerance.setTitle("Tolerance")
        self.Tolerance.setObjectName("Tolerance")
        self.verticalLayoutWidget_2 = QtGui.QWidget(self.Tolerance)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(8, 20, 125, 57))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtGui.QLabel(self.verticalLayoutWidget_2)
        self.label.setToolTip("mm")
        self.label.setStatusTip("")
        self.label.setWhatsThis("")
        self.label.setText("tolerance in mm")
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.tolerance = QtGui.QLineEdit(self.verticalLayoutWidget_2)
        self.tolerance.setMinimumSize(QtCore.QSize(64, 22))
        self.tolerance.setMaximumSize(QtCore.QSize(64, 22))
        self.tolerance.setToolTip("Tolerance on Constraints")
        self.tolerance.setStatusTip("")
        self.tolerance.setWhatsThis("")
        self.tolerance.setInputMethodHints(QtCore.Qt.ImhPreferNumbers)
        self.tolerance.setInputMask("")
        self.tolerance.setText("0.1")
        self.tolerance.setPlaceholderText("")
        self.tolerance.setObjectName("tolerance")
        self.verticalLayout_2.addWidget(self.tolerance)
        self.rmvXGeo = QtGui.QCheckBox(CDialog)
        self.rmvXGeo.setGeometry(QtCore.QRect(170, 180, 141, 20))
        self.rmvXGeo.setToolTip("remove duplicated geometries")
        self.rmvXGeo.setStatusTip("")
        self.rmvXGeo.setText("rmv xtr geo")
        self.rmvXGeo.setObjectName("rmvXGeo")

        #self.retranslateUi(CDialog)
        ###  --------------------------------------------------------
        #self.checkBox.setText("rmv xtr geo")
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), CDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), CDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(CDialog)
        
        
        myiconsize=48
        icon = QtGui.QIcon()
        myicon=os.path.join( ksuWB_icons_path , 'Sketcher_LockCoincident.svg')
        icon.addPixmap(QtGui.QPixmap(myicon), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.coincident.setIcon(icon)
        self.coincident.setIconSize(QtCore.QSize(myiconsize, myiconsize))
        self.coincident.setChecked(True)
        icon1 = QtGui.QIcon()
        myicon=os.path.join( ksuWB_icons_path , 'Sketcher_LockAll.svg')
        icon1.addPixmap(QtGui.QPixmap(myicon), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.all_constraints.setIcon(icon1)
        self.all_constraints.setIconSize(QtCore.QSize(myiconsize, myiconsize))
        icond = QtGui.QIcon()
        myicon=os.path.join( ksuWB_icons_path , 'Sketcher_LockAll.svg')
        icond.addPixmap(QtGui.QPixmap(myicon), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        CDialog.setWindowIcon(icon)
    

        # remove question mark from the title bar
        CDialog.setWindowFlags(CDialog.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        #self.Label_howto.setText("<b>Select a Sketch and Parameters<br>to constraint the sketch<br>NB the Sketch will be modified!</b>")

    def return_strings(self):
    #   Return list of values. It need map with str (self.lineedit.text() will return QString)
        return map(str, [self.tolerance.text(), self.all_constraints.isChecked(), self.rmvXGeo.isChecked()])
        
    # @staticmethod
    # def get_data(parent=None):
    #     #dialog = Ui_CDialog()
    #     dialog = Ui_CDialog(parent)
    #     #dialog = QtGui.QDialog()
    #     dialog.exec_()
    #     return dialog.return_strings()
        
################ ------------------- end CD-ui #############################


class ksuToolsOpenBoard:
    "ksu tools Open Board object"
 
    def GetResources(self):
        return {'Pixmap'  : os.path.join( ksuWB_icons_path , 'importBoard.svg') , # the name of a svg file available in the resources
                     'MenuText': "Load Board" ,
                     'ToolTip' : "ksu Load KiCad PCB Board and Parts"}
 
    def IsActive(self):
        #if FreeCAD.ActiveDocument == None:
        #    return False
        #else:
        #    return True
        #import kicadStepUptools
        return True
 
    def Activated(self):
        # do something here...
        import kicadStepUptools
        #if not kicadStepUptools.checkInstance():
        #    reload( kicadStepUptools )
        if reload_Gui:
            reload_lib( kicadStepUptools )
        #from kicadStepUptools import onPushPCB
        #FreeCAD.Console.PrintWarning( 'active :)\n' )
        kicadStepUptools.onLoadBoard()
        # ppcb=kicadStepUptools.KSUWidget
        # ppcb.onPushPCB()
    
        #onPushPCB()
        #import kicadStepUptools


FreeCADGui.addCommand('ksuToolsOpenBoard',ksuToolsOpenBoard())
##


class ksuToolsExportModel:
    "ksu tools Export Model to KiCad object"
 
    def GetResources(self):
        return {'Pixmap'  : os.path.join( ksuWB_icons_path , 'export3DModel.svg') , # the name of a svg file available in the resources
                     'MenuText': "Export 3D Model" ,
                     'ToolTip' : "ksu Export 3D Model to KiCad"}
 
    def IsActive(self):
        #if FreeCAD.ActiveDocument == None:
        #    return False
        #else:
        #    return True
        #import kicadStepUptools
        return True
 
    def Activated(self):
        # do something here...
        # import kicadStepUptools
        #if not kicadStepUptools.checkInstance():
        #    reload( kicadStepUptools )
        #if reload_Gui:
        #    reload_lib( kicadStepUptools )
        #from kicadStepUptools import onPushPCB
        #FreeCAD.Console.PrintWarning( 'active :)\n' )
      ##evaluate to read cfg and get materials value???
      ##or made something as in load board
        #ini_content=kicadStepUptools.cfg_read_all()
        if FreeCAD.ActiveDocument.FileName == "":
            msg="""please <b>save</b> your job file before exporting."""
            QtGui.QApplication.restoreOverrideCursor()
            QtGui.QMessageBox.information(None,"Info ...",msg)
            FreeCADGui.SendMsgToActiveView("Save")
        
        from kicadStepUptools import routineScaleVRML
        if reload_Gui:
            reload_lib( kicadStepUptools )
        routineScaleVRML()
        ## kicadStepUptools.routineScaleVRML()
        #kicadStepUptools.Ui_DockWidget.onCfg()
        # ppcb=kicadStepUptools.KSUWidget
        # ppcb.onPushPCB()
 
        #onPushPCB()
        #import kicadStepUptools

FreeCADGui.addCommand('ksuToolsExportModel',ksuToolsExportModel())
##

class ksuToolsImport3DStep:
    "ksu tools Import 3D Step object"
 
    def GetResources(self):
        return {'Pixmap'  : os.path.join( ksuWB_icons_path , 'add_block_y.svg') , # the name of a svg file available in the resources
                     'MenuText': "Import 3D Step" ,
                     'ToolTip' : "ksu Import 3D Step Model"}
 
    def IsActive(self):
        #if FreeCAD.ActiveDocument == None:
        #    return False
        #else:
        #    return True
        #import kicadStepUptools
        return True
 
    def Activated(self):
        # do something here...
        import kicadStepUptools
        #if not kicadStepUptools.checkInstance():
        #    reload( kicadStepUptools )
        if reload_Gui:
            reload_lib( kicadStepUptools )
        #from kicadStepUptools import onPushPCB
        #FreeCAD.Console.PrintWarning( 'active :)\n' )
        kicadStepUptools.Import3DModelF()

FreeCADGui.addCommand('ksuToolsImport3DStep',ksuToolsImport3DStep())
##

class ksuToolsExport3DStep:
    "ksu tools Export 3D to Step object"
 
    def GetResources(self):
        return {'Pixmap'  : os.path.join( ksuWB_icons_path , 'export3DStep.svg') , # the name of a svg file available in the resources
                     'MenuText': "Export 3D to Step" ,
                     'ToolTip' : "ksu Export selected objects to Step Model"}
 
    def IsActive(self):
        #if FreeCAD.ActiveDocument == None:
        #    return False
        #else:
        #    return True
        #import kicadStepUptools
        return True
 
    def Activated(self):
        # do something here...
        import kicadStepUptools
        #if not kicadStepUptools.checkInstance():
        #    reload( kicadStepUptools )
        if reload_Gui:
            reload_lib( kicadStepUptools )
        #from kicadStepUptools import onPushPCB
        #FreeCAD.Console.PrintWarning( 'active :)\n' )
        kicadStepUptools.Export3DStepF()

FreeCADGui.addCommand('ksuToolsExport3DStep',ksuToolsExport3DStep())
##


class ksuToolsPullPCB:
    "Pull layer from KiCAD PCB into Sketch object"
 
    def GetResources(self):
        return {'Pixmap'  : os.path.join( ksuWB_icons_path , 'Sketcher_Pull.svg') , # the name of a svg file available in the resources
                'MenuText': "Pull Sketch Layer from PCB" ,
                'ToolTip' : "Pull KiCAD PCB layer into a Sketch"}
 
    def IsActive(self):
        return True     # Command is always active
 
    def Activated(self):
        import kicadStepUptools
        #if not kicadStepUptools.checkInstance():
        #    reload( kicadStepUptools )
        if reload_Gui:
            reload_lib( kicadStepUptools )

        kicadStepUptools.PullPCB()

FreeCADGui.addCommand('ksuToolsPullPCB',ksuToolsPullPCB())
# END Command - ksuToolsPullPCB


#####
def mk_str_u(input):
    if (sys.version_info > (3, 0)):  #py3
        if isinstance(input, str):
            return input
        else:
            input =  input.encode('utf-8')
            return input
    else:  #py2
        if type(input) == unicode:
            input =  input.encode('utf-8')
            return input
        else:
            return input
###
make_compound = False

##
def toggle_highlight_subtree(objs):
    def addsubobjs(obj,totoggleset):
        totoggle.add(obj)
        for subobj in obj.OutList:
            addsubobjs(subobj,totoggleset)

    import FreeCAD
    totoggle=set()
    for obj in objs:
        addsubobjs(obj,totoggle)
    checkinlistcomplete =False
    while not checkinlistcomplete:
        for obj in totoggle:
            if (obj not in objs):
                if (frozenset(obj.InList) - totoggle):
                    if hasattr (set, 'totoggle'):
                        totoggle.toggle(obj)
                        break
        else:
            checkinlistcomplete = True
    obj_tree=objs[1:len(objs)]
    for obj in totoggle:
        if 'Compound' not in FreeCADGui.ActiveDocument.getObject(obj.Name).TypeId: # and 'App::Part' not in Gui.ActiveDocument.getObject(obj.Name).TypeId:
            if 'Part' in obj.TypeId or 'App::Link' in obj.TypeId:
                if obj not in obj_tree:
                    FreeCADGui.Selection.addSelection(obj)
                else:
                    FreeCADGui.Selection.removeSelection(obj)
        else:
            if hide_compound==True:
                FreeCADGui.ActiveDocument.getObject(obj.Name).Visibility=False

#####
def toggle_visibility_subtree(objs):
    def addsubobjs(obj,totoggleset):
        totoggle.add(obj)
        for subobj in obj.OutList:
            addsubobjs(subobj,totoggleset)

    import FreeCAD
    totoggle=set()
    for obj in objs:
        addsubobjs(obj,totoggle)
    checkinlistcomplete =False
    while not checkinlistcomplete:
        for obj in totoggle:
            if (obj not in objs) and (frozenset(obj.InList) - totoggle):
                totoggle.toggle(obj)
                break
        else:
            checkinlistcomplete = True
    for obj in totoggle:
        if 'Compound' not in FreeCADGui.ActiveDocument.getObject(obj.Name).TypeId:
            if 'Part' in obj.TypeId or 'Sketch' in obj.TypeId:
            #if 'Part::Feature' in obj.TypeId or 'App::Part' in obj.TypeId:
                #if obj.Visibility==True:
                if FreeCADGui.ActiveDocument.getObject(obj.Name).Visibility==True:
                    #obj.Document.getObject(obj.Name).Visibility=False
                    FreeCADGui.ActiveDocument.getObject(obj.Name).Visibility=False
                else:
                    FreeCADGui.ActiveDocument.getObject(obj.Name).Visibility=True
        else:
            if hide_compound==True:
                FreeCADGui.ActiveDocument.getObject(obj.Name).Visibility=False

#####

#####
def toggle_transparency_subtree(objs):
    def addsubobjs(obj,totoggleset):
        totoggle.add(obj)
        for subobj in obj.OutList:
            addsubobjs(subobj,totoggleset)

    import FreeCAD
    doc=FreeCADGui.ActiveDocument
    totoggle=set()
    for obj in objs:
        addsubobjs(obj,totoggle)
    checkinlistcomplete =False
    while not checkinlistcomplete:
        for obj in totoggle:
            if (obj not in objs) and (frozenset(obj.InList) - totoggle):
                try:
                    totoggle.toggle(obj)
                    break
                except:
                    FreeCAD.Console.PrintWarning('totoggle not allowed\n')
        else:
            checkinlistcomplete = True
    for obj in totoggle:
        #FreeCAD.Console.PrintMessage(obj.Label)
        #if 'App::Part' not in obj.TypeId and 'Part::Feature' in obj.TypeId:
        if 'App::Part' not in obj.TypeId and 'Part' in obj.TypeId:
            #if obj.Visibility==True:
            #FreeCAD.Console.PrintMessage(obj.Label)
            if doc.getObject(obj.Name).Transparency == 0:
                #obj.Document.getObject(obj.Name).Visibility=False
                doc.getObject(obj.Name).Transparency = 70
            else:
                doc.getObject(obj.Name).Transparency = 0
##

#####
def toggleAlly(tree, item, collapse):
    if collapse == False:
        tree.expandItem(item)
    elif collapse == True:  
        tree.collapseItem(item)
    for i in range(item.childCount()):
        print(item.child(i).text(0))
        if 'Origin' not in item.child(i).text(0):
            toggleAlly(tree, item.child(i), collapse)
##



#####
class ksuToolsAligner:
    "ksu tools Aligner"
    
    def GetResources(self):
        mybtn_tooltip ="Manipulator tools \'Aligner\'"
        return {'Pixmap'  : os.path.join( ksuWB_icons_path , 'Align.svg') , # the name of a svg file available in the resources
                     'MenuText': mybtn_tooltip ,
                     'ToolTip' : mybtn_tooltip}
 
    def IsActive(self):
        combined_path = '\t'.join(sys.path)
        if 'Manipulator' in combined_path:
            return True
        #else:
        #    self.setToolTip("Grayed Tooltip!")
        #    print(self.ObjectName)
        #    grayed_tooltip="Grayed Tooltip!"
        #    mybtn_tooltip=grayed_tooltip
 
    def Activated(self):
        # do something here...
        combined_path = '\t'.join(sys.path)
        if 'Manipulator' in combined_path:
            import Aligner;reload_lib(Aligner)

FreeCADGui.addCommand('ksuToolsAligner',ksuToolsAligner())

#####
class ksuToolsMover:
    "ksu tools Mover"
    
    def GetResources(self):
        mybtn_tooltip ="Manipulator tools \'Mover\'"
        return {'Pixmap'  : os.path.join( ksuWB_icons_path , 'Mover.svg') , # the name of a svg file available in the resources
                     'MenuText': mybtn_tooltip ,
                     'ToolTip' : mybtn_tooltip}
 
    def IsActive(self):
        combined_path = '\t'.join(sys.path)
        if 'Manipulator' in combined_path:
            return True
        #else:
        #    self.setToolTip("Grayed Tooltip!")
        #    print(self.ObjectName)
        #    grayed_tooltip="Grayed Tooltip!"
        #    mybtn_tooltip=grayed_tooltip
 
    def Activated(self):
        # do something here...
        combined_path = '\t'.join(sys.path)
        if 'Manipulator' in combined_path:
            import Mover;reload_lib(Mover)

FreeCADGui.addCommand('ksuToolsMover',ksuToolsMover())
#####
class ksuToolsCaliper:
    "ksu tools Caliper"
    
    def GetResources(self):
        mybtn_tooltip ="Manipulator tools \'Caliper\'"
        return {'Pixmap'  : os.path.join( ksuWB_icons_path , 'Caliper.svg') , # the name of a svg file available in the resources
                     'MenuText': mybtn_tooltip ,
                     'ToolTip' : mybtn_tooltip}
 
    def IsActive(self):
        combined_path = '\t'.join(sys.path)
        if 'Manipulator' in combined_path:
            return True
        #else:
        #    self.setToolTip("Grayed Tooltip!")
        #    print(self.ObjectName)
        #    grayed_tooltip="Grayed Tooltip!"
        #    mybtn_tooltip=grayed_tooltip
 
    def Activated(self):
        # do something here...
        combined_path = '\t'.join(sys.path)
        if 'Manipulator' in combined_path:
            import Caliper;reload_lib(Caliper)

FreeCADGui.addCommand('ksuToolsCaliper',ksuToolsCaliper())
#####
###
class ksuToolsEditPrefs:
    "ksu tools Edit Preferences"
    
    def GetResources(self):
        mybtn_tooltip ="Edit Preferences"
        return {'Pixmap'  : os.path.join( ksuWB_icons_path , 'Preferences-Edit.svg') , # the name of a svg file available in the resources
                'MenuText': mybtn_tooltip ,
                'ToolTip' : mybtn_tooltip}
 
    def IsActive(self):
        return True
        #else:
        #    self.setToolTip("Grayed Tooltip!")
        #    print(self.ObjectName)
        #    grayed_tooltip="Grayed Tooltip!"
        #    mybtn_tooltip=grayed_tooltip
 
    def Activated(self):
        # do something here...
        #import kicadStepUptools
        FreeCADGui.runCommand("Std_DlgPreferences")
        
FreeCADGui.addCommand('ksuToolsEditPrefs',ksuToolsEditPrefs())

#####
#####
class ksuToolsDefeaturingTools:
    "ksu tools DefeaturingTools"
    
    def GetResources(self):
        mybtn_tooltip ="Defeaturing Tools from Defeaturing WorkBench"
        return {'Pixmap'  : os.path.join( ksuWB_icons_path , 'DefeaturingTools.svg') , # the name of a svg file available in the resources
                     'MenuText': mybtn_tooltip ,
                     'ToolTip' : mybtn_tooltip}
 
    def IsActive(self):
        combined_path = '\t'.join(sys.path)
        if 'Defeaturing' in combined_path:
            return True
        #else:
        #    self.setToolTip("Grayed Tooltip!")
        #    print(self.ObjectName)
        #    grayed_tooltip="Grayed Tooltip!"
        #    mybtn_tooltip=grayed_tooltip
 
    def Activated(self):
        # do something here...
        combined_path = '\t'.join(sys.path)
        if 'Defeaturing' in combined_path:
            import DefeaturingTools;reload_lib(DefeaturingTools)

FreeCADGui.addCommand('ksuToolsDefeaturingTools',ksuToolsDefeaturingTools())
#####
####
class ksuToolsAddTracks:
    "ksu tools Add Tracks"
    
    def GetResources(self):
        mybtn_tooltip ="ksu tools Add Tracks\nNB: it could be a very intensive loading!"
        return {'Pixmap'  : os.path.join( ksuWB_icons_path , 'tracks.svg') , # the name of a svg file available in the resources
                     'MenuText': mybtn_tooltip ,
                     'ToolTip' : mybtn_tooltip}
 


    def IsActive(self):
        return True
        #else:
        #    self.setToolTip("Grayed Tooltip!")
        #    print(self.ObjectName)
        #    grayed_tooltip="Grayed Tooltip!"
        #    mybtn_tooltip=grayed_tooltip
 
    def Activated(self):
        # do something here...
        import tracks
        #!#from kicadStepUptools import removesubtree
        from kicadStepUptools import ZoomFitThread
        from PySide import QtGui, QtCore
        from sys import platform as _platform
        
        pt_lnx=False
        if _platform == "linux" or _platform == "linux2":
            pt_lnx=True

        if FreeCAD.ActiveDocument is not None:
            doc = FreeCAD.ActiveDocument
        else:
            doc = FreeCAD.newDocument()
        #doc.commitTransaction()
        #doc.UndoMode = 1
        doc.openTransaction('add_tracks_kicad')
        add_toberemoved = tracks.addtracks()
        # print(add_toberemoved)
        doc.commitTransaction()
        doc.recompute()
        def removing_objs():
            ''' removing objects after delay ''' 
            from kicadStepUptools import removesubtree
            doc.openTransaction('rmv_tracks_kicad')
            for tbr in add_toberemoved:
                removesubtree(tbr)
            doc.commitTransaction()
            # doc.undo()
            # doc.undo()
        # adding a timer to allow double transactions during the python code
        QtCore.QTimer.singleShot(0.2,removing_objs)
        if (not pt_lnx): # and (not pt_osx): issue on AppImages hanging on loading 
            FreeCADGui.SendMsgToActiveView("ViewFit")
        else:
            zf= Timer (0.25,ZoomFitThread)
            zf.start()        

    ##

FreeCADGui.addCommand('ksuToolsAddTracks',ksuToolsAddTracks())
#####
class ksuToolsAddSilks:
    "ksu tools Add Silks"
    
    def GetResources(self):
        mybtn_tooltip ="ksu tools Add Silks from kicad exported DXF\nNB: it could be a very intensive loading!"
        return {'Pixmap'  : os.path.join( ksuWB_icons_path , 'Silks.svg') , # the name of a svg file available in the resources
                     'MenuText': mybtn_tooltip ,
                     'ToolTip' : mybtn_tooltip}
 
    def IsActive(self):
        return True
        #else:
        #    self.setToolTip("Grayed Tooltip!")
        #    print(self.ObjectName)
        #    grayed_tooltip="Grayed Tooltip!"
        #    mybtn_tooltip=grayed_tooltip
 
    def Activated(self):
        # do something here...
        import makefacedxf
        if makefacedxf.checkDXFsettings():
            makefacedxf.makeFaceDXF()
        else:
            msg = """<b>DXF import setting NOT as required.</b><br>Please check to have selected:<br>
            - DXF Legacy Importer<br>
            - DXF Join Geometries<br>
            - DXF Create Simple Part Shapes<br>
            in DXF Preferences Import options"""
            reply = QtGui.QMessageBox.information(None,"Warning", msg)

FreeCADGui.addCommand('ksuToolsAddSilks',ksuToolsAddSilks())
#####
