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
#*  Schema                                                                  *
#*    kts_StackUp - Definition of actual PCBA Stackup                       *
#*      layer_posn: int (top=1, etc...) # this is just be list order
#*      layer_data: PCB file drawing num contianing layer "content" 
#*      layer_outline: PCB file drawing num contianing layer outlines 
#*      layer_type: from kts_LayerTypes enum {Silk, Adhes, SolMask, etc.}
#*      layer_thk:  Finished thickness of layer in microns (um)
#*      layer_matl: material type of layer (FR4, Polyimide, Prepreg, etc.)
#*      layer_region: region of PCB project layer is used on {flex, rigid}
#*                                                                          *
#*    KiCAD_Layers - KTS layer definition & purpose for PCBA                *
#*      kicad_num:  Absolute numeric ID of layer from kicad app
#*      kicad_enum: Symbolic enum used for each layer
#*      kicad_dscr: User-defined name from KiCAD PCB file
#*
#*  Dictionaries
#*      kts_dscr:   User-defined name from KTS domain

#*      kts_LayerTypes: enum {Silk, Adhes, SolMask, etc.}
#*                                                                          *
#*      kts_Materials:  enum {FR4, Polyimide, Prepreg, etc.}
#*          This will probably also have names/types to allow for later
#*          generating fab docs... so {{PrePreg, "PrePreg 3080"}, {...}}
#*                                                                          *
#*      kts_Regions:    enum {flex, rigid, stiffner, prepreg, etc.}
#*                                                                          *
#****************************************************************************


__KTS_FILE_VER__  = "1.0.0"
__KTS_FILE_NAME__ = "KTS_STACKUPEDIT"

from kts_PrefsMgmt import prefs_set_file_version
prefs_set_file_version(__KTS_FILE_NAME__, __KTS_FILE_VER__)


class KiCAD_Layers():
    """Create and maintain a dictionary of the activated layers
       in the selected PCB. Methods to look up layer info by
       either KiCAD layer number or layer Mnemonic."""
    from fcad_parser import KicadPCB
    layer_dict = dict()

    def init(kicad_pcb):
        if not hasattr(kicad_pcb, 'layers'):
            # Make this into an "Alert"
            print("KiCAD_Layers: No Layers found in PCB file." )
        else:
            print("KiCAD_Layers: Found: ", len(kicad_pcb.layers), " layers." )

            for lyr in kicad_pcb.layers:
                # Add mnemonic->number mapping
                KiCAD_Layers.layer_dict[(kicad_pcb.layers[lyr])[0].replace('"', '')] = lyr

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


def kts_make_stack_edit_tab():
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
    our_new_tab = StackUpEditDialog()
    
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
from PySide.QtGui import QPen, QColor, QBrush, QFrame, QComboBox, QLineEdit, QFont
from PySide.QtCore import QRectF

class StackUpEditDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setFixedHeight(300)

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
        my_rect = QRectF(0,0,50,layer_height)

        scene = QGraphicsScene(self)
        scene.addRect(my_rect, Qt.NoPen, Qt.red)
        
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


        row_layout = QHBoxLayout()
        row_layout.setSpacing(0)   # No Horiz space between elements
        row_layout.setMargin(0)   # No Horiz space between elements
        row_layout.setContentsMargins(0, 0, 0, 0)

        row_layout.addStretch()
        row_layout.addWidget(entry)
        row_layout.addWidget(view)
        row_layout.addWidget(combobox)
        row_layout.addStretch()

        
        row_layout2 = QHBoxLayout()
        row_layout2.addWidget(view2)

        #row_layout.setMaximumHeight(100)

        self.layout = QVBoxLayout() # We use a Vertical Box layout to stack the layers
        self.layout.setSpacing(layer_spacing)   # No vertical space between elements

        message = QLabel("Something happened, is that OK?")
        message.setFixedHeight(20)

        message2 = QLabel("Something happened, is that OK?")

        self.layout.addWidget(message)
        self.layout.addLayout(row_layout)
        self.layout.addLayout(row_layout2)
        self.layout.addWidget(message2)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

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