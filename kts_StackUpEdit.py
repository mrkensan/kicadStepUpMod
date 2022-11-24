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

__KTS_FILE_VER__  = "1.0.0"
__KTS_FILE_NAME__ = "KTS_STACKUPEDIT"

from kts_PrefsMgmt import prefs_set_file_version
prefs_set_file_version(__KTS_FILE_NAME__, __KTS_FILE_VER__)

from kts_KiCadPCB import *

def _getComboView(main_window):
    from PySide import QtGui

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
    import FreeCADGui
    from PySide import QtGui

    combo_view_tabs = _getComboView(FreeCADGui.getMainWindow())

    if (combo_view_tabs == None):
        print("Combo View Not Found")
        return None

    our_new_tab = StackUpEditDialog(stackup)
    tab_index = combo_view_tabs.addTab(our_new_tab,"Stackup Editor")
    print("Tab Index = "+str(tab_index))
    print("Index of 'our_new_tab' = "+str(combo_view_tabs.indexOf(our_new_tab)))
    print("Text of 'our_new_tab' = "+str(combo_view_tabs.tabText(tab_index)))

    dw=combo_view_tabs.findChildren(QtGui.QDialog)
    for i in dw:
       print(str(i.objectName()))

    return combo_view_tabs, tab_index;
# END - kts_make_stack_edit_tab()


from PySide.QtGui import QComboBox

class CutOutlineSelector(QComboBox):
    this_layer = ""

    def __init__(self, layer):
        super().__init__()
        self.this_layer = layer

    def PopulateList(self, selected, outline_layers):
        print("Making a combo layer: ", self.this_layer.content, ". Defaulting to: ", selected)
        self.addItems(outline_layers)
        self.setCurrentText(selected)
        self.currentTextChanged.connect(self._user_selection)

    def _user_selection(self, selected):
        print("Outline drawing for:", self.this_layer.content, " is :", selected)
        return 
# END - class CutOutlineSelector


# We subclass QDialog here in order override some
# built-in methods like accept() & cancel(), etc..
from PySide.QtGui import QDialog

class StackUpEditDialog(QDialog):
    """Create the 'Stackup Editor' tab in \nthe 'Combo View' Panel of the UI."""

    item_vert_ht = 13
    item_box_ht  = 15
    item_horz_wd = 70
    item_horz_spc = 10
    header_vert_ht  = 2 * item_vert_ht
    header_horz_wd = item_horz_wd
    header_horz_spc = item_horz_spc
    drop_down_ht = item_vert_ht + 3
    layer_spacing = 4


    def __init__(self, stackup: KTS_Stackup):
        from PySide.QtGui import QDialogButtonBox, QVBoxLayout

        super().__init__()

        # Create buttons to accept or reject the changes
        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        # Build row of col titles
        stackup_header_row = self._build_stackup_row_header()

        self.layout = QVBoxLayout()                 # We use a Vertical Box layout to stack the layers
        self.layout.setSpacing(self.layer_spacing)
        #self.layout.setMargin(0)                   # No vertical space between elements
        #self.layout.setContentsMargins(0,0,0,0)

        # Add header first, then content row for each physical stackup-layer
        self.layout.addLayout(stackup_header_row)
        for lyr in stackup:
            self.layout.addLayout(self._build_stackup_row(lyr))

        self.layout.addStretch()                    # Required to allow rows above to "relax" to assigned spacing
        self.layout.addWidget(self.buttonBox)       # These will be stuck to the lower right corner
        self.setLayout(self.layout)                 # Commit the layout to our new tab in the "Combo View"

        return None
    # END - __init__()


    def _build_stackup_row_header(self): # Returns a QHBoxLayout element
        from PySide.QtGui  import QLabel, QHBoxLayout
        from PySide.QtCore import Qt

        headers = []
        column_labels = ["Stack Up", "Cut\nOutline", "Content", "Type", "Thickness", 
                         "Material", "Region", "Stack Up\nColor", "Cu Finish", "Function"]

        for col in column_labels:
            # Construct text elements for Row
            headers.append(QLabel())
            headers[-1].setText(col)
            headers[-1].setAlignment(Qt.AlignCenter | Qt.AlignBottom)
            headers[-1].setContentsMargins(0, 0, 0, 0)
            #headers[-1].setAlignment(Qt.AlignBottom)
            headers[-1].setStyleSheet("font-weight: bold; padding :0px; ")
            headers[-1].setFixedHeight(self.header_vert_ht)
            headers[-1].setFixedWidth(self.header_horz_wd)

            headers[-1].setStyleSheet(headers[-1].styleSheet() + "background-color: #EDF0F5; ")
        
        # Create row object
        row_layout = QHBoxLayout()
        row_layout.setSpacing(self.header_horz_spc)     # Horiz space between elements

        # Add elements, in order left-to-right, to the new row
        for col in headers:
            row_layout.addWidget(col)

        row_layout.addStretch()         # Required to allow colums to respect their fixed spacing

        return (row_layout)
    # END - _build_stackup_row_header()


    def _build_stackup_row(self, layer: KTS_StackUpRecord): # Returns a QHBoxLayout element
        from PySide.QtGui import QLabel, QHBoxLayout, QGraphicsScene, QGraphicsView, QFrame
        from PySide.QtCore import Qt

        items = []

        # These are the columns we want to iteratively render, in order
        layer_col_vals = []
        layer_col_vals.append(layer.content)
        layer_col_vals.append(layer.lyr_type)
        layer_col_vals.append(str(layer.thkness))
        layer_col_vals.append(layer.material)
        layer_col_vals.append(layer.region)
        layer_col_vals.append(layer.color)
        layer_col_vals.append(layer.finish)
        layer_col_vals.append(layer.lyr_func)

        # Colored rectangle representing the material of layer
        rect = QGraphicsScene(self)                     # Create container (scene) for graphics element
        rect.addRect(0, 0, self.item_horz_wd,           # Add a rectangle to the scene
                     self.item_box_ht, Qt.NoPen,
                     KtsColor.to_QColor(layer.color))  

        # Create view object for rectangle and set display params 
        rect_view = QGraphicsView(rect)             # Add view containing rectangle
        rect_view.setFrameStyle(QFrame.NoFrame)     # Remove "frame" around view
        rect_view.setFixedHeight(self.item_box_ht)  # Adjust Height...
        rect_view.setFixedWidth(self.item_horz_wd)  # ... and width to absolute
        items.append(rect_view)                     # Add column for view containing rectangle

        # Drop-down list for user selection of drawing-layer to associate with stackup-layer
        if (('Dielec' in layer.content) or ('Polyimide' in layer.material)):
            outline_menu = CutOutlineSelector(layer)    # Init object for this particular stackup layer
        
            outline_menu.PopulateList("Three", KiCAD_Layers.get_outline_items())

            font = outline_menu.font()
            font.setPointSize(7)                            # Set font to fit in our row without clipping
            outline_menu.setFont(font)
            outline_menu.setFixedHeight(self.drop_down_ht)  # Adjust Height...
            outline_menu.setFixedWidth(self.item_horz_wd)   # ... and width to absolute
            items.append(outline_menu)                      # Add column for view containing Drop-down list
        else:
            # Add a "Blank Spot" instead of the drop-down for this stackup-layer
            items.append(QLabel())
            items[-1].setFixedHeight(self.item_vert_ht)
            items[-1].setFixedWidth(self.item_horz_wd)

        # Iterate through the remaining columns, rendering the text into QLabel objects
        for col in layer_col_vals:
            # Construct text elements for Row
            items.append(QLabel())                  # Add column for field text
            items[-1].setText(col)
            items[-1].setAlignment(Qt.AlignCenter)
            # Highlight potential errors for the user to resolve
            # ToDo: Add a "hover tip" to help the user know how to resolve it
            if (col == '???') or (col == '0'):
                items[-1].setStyleSheet("background-color: #FFEC22; font-weight: bold; ")
            items[-1].setFixedHeight(self.item_vert_ht)
            items[-1].setFixedWidth(self.item_horz_wd)
            #items[-1].setStyleSheet(items[-1].styleSheet() + "background-color: #EDF0F5; ")    # Just for debugging use to check alignments

        # Create an empty row object
        row_layout = QHBoxLayout()
        row_layout.setSpacing(self.item_horz_spc)   # Horiz space between elements
                                                    # We may want to set a minimum width for the row
                                                    # (if this is possible) to prevent smooshing stuff

        # Probably don't need this...
        #row_layout.setAlignment(Qt.AlignCenter)     # Align placement of ELEMENT inside cell
        #row_layout.setMargin(0)                     # No Horiz margin inside elements
        #row_layout.setContentsMargins(0, 0, 0, 0)   # or? No Horiz margin inside elements

        # Add elements, in order left-to-right, to the new row
        for col in items:
            row_layout.addWidget(col)
        
        row_layout.addStretch()         # Required to allow colums to respect their fixed spacing

        return (row_layout)
    # END - _build_stackup_row()


    # Overrides the builtin accept() method
    def accept(stuff):
        print("Accepted", stuff)
        pprint.pprint(stuff)

# END - class StackUpEditDialog

# END_MODULE - kts_StackUpEdit
