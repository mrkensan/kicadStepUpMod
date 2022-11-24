# -*- coding: utf-8 -*-
#****************************************************************************
#*                                                                          *
#*   This program is free software; you can redistribute it and/or modify   *
#*   it under the terms of the GNU Affero General Public License            *
#*   as published by the Free Software Foundation to ensure cooperation     *
#*   with the community in the case of network server software;             *
#*   for detail see the LICENSE text file.                                  *
#*   http://www.gnu.org/licenses/agpl-3.0.en.html                           *
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
#*   The purpose of this workbench is to provide a single-function tool     *
#*   for rendering KiCAD PCBs into STEP models for use in non-FreeCAD MCAD  *
#*   packages. We also add support for Rigid-Flex stackups, and rendering   *
#*   of these boards into STEP files which can be usefully manipulated in   *
#*   the MCAD domain (e.g. flexing the flexible portions of the PCBA).      *
#*                                                                          *
#*   Because our use-case does not require manipulation of the rendered     *
#*   model in FreeCAD, this tool focuses only on PCB rendering.             *
#*   Functions such as PCB round-tipping between MCAD-ECAD apps are         *
#*   supported by other FreeCAD workbenches.                                *
#*                                                                          *
#*   We hope that this workbench is useful to the community!                *
#*                                                                          *
#****************************************************************************



class KtsState:
    internal_count = 1  # call counter
    WbState = dict()    # State Storage

    def myState(self, item_name=None, item_value=None):
        if (item_name == None):    # Don't try to look up "None"
            return None

        if (item_value != None):
            self.WbState[item_name] = item_value        # Add/update this item
            return None
        else:
            return (self.WbState.get(item_name, None))  # Try to find item, 'None' if not present


    def delStateItem(self, item_name):
        if (item_name != None):    # Don't try to Delete "None"
            self.WbState.pop(item_name, None)
        return None





