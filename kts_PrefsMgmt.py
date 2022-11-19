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

"""Preferences Management Module\nMethods related to reading, writing, updating Workbench settings."""

# These names are different than for all other files so we
# don't overwrite generic names when including this file
__KTS_PREFS_VER__  = "1.0.2"
__KTS_PREFS_NAME__ = "KTS_PREFSMGMT"

'''
import os
def _get_my_file():
    try:
        my_file = os.path.dirname(os.path.basename(__file__))
        print("PrefsMgmt)__file__ = " + my_file)
    except NameError:  # We are the main py2exe script, not a module
        import sys
        my_file = os.path.dirname(os.path.basename(sys.argv[0]))
        print("(PrefsMgmt) No __file__: " + my_file)
    return(my_file)

print("get_my_file = " + _get_my_file())
'''

# This is the signature of the parameter store for our
# workbench, within the FreeCAD "user param" store
def _workbench_prefs_folder():
    return "User parameter:BaseApp/Preferences/Mod/KiCAD_2STEP"


def check_for_updates(url, commit_nbr):
    import re, sys

    resp_ok = False
    if (sys.version_info > (3, 0)):  #py3
        import urllib
        from urllib import request, error #URLError, HTTPError
        req = request.Request(url)
        try:
            response = request.urlopen(req)
            resp_ok = True
            the_page = response.read().decode("utf-8") 
        except error.HTTPError as e:
            FreeCAD.Console.PrintWarning('The server couldn\'t fulfill the request.')
            FreeCAD.Console.PrintWarning('Error code: ' + str(e.code)+'\n')
        except error.URLError as e:
            FreeCAD.Console.PrintWarning('We failed to reach a server.\n')
            FreeCAD.Console.PrintWarning('Reason: '+ str(e.reason)+'\n')
                
    else:  #py2
        import urllib2
        from urllib2 import Request, urlopen, URLError, HTTPError
        req = Request(url)
        try:
            response = urlopen(req)
            resp_ok = True
            the_page = response.read()
        except HTTPError as e:
            FreeCAD.Console.PrintWarning('The server couldn\'t fulfill the request.')
            FreeCAD.Console.PrintWarning('Error code: ' + str(e.code)+'\n')
        except URLError as e:
            FreeCAD.Console.PrintWarning('We failed to reach a server.\n')
            FreeCAD.Console.PrintWarning('Reason: '+ str(e.reason)+'\n')          
                
    if resp_ok:            
        # everything is fine
        #the_page = response.read()
        # print the_page
        if 0: #old method to get commits nbr
            str2='<li class=\"commits\">'
            pos=the_page.find(str2)
            str_commits=(the_page[pos:pos+600])
            # print str_commits
            pos=str_commits.find('<span class=\"num text-emphasized\">')
            commits=(str_commits[pos:pos+200])
            commits=commits.replace('<span class=\"num text-emphasized\">','')
            #commits=commits.strip(" ")
            #exp = re.compile("\s-[^\S\r\n]")
            #print exp
            #nbr_commits=''
            my_commits=re.sub('[\s+]', '', commits)
            pos=my_commits.find('</span>')
            #print my_commits
            nbr_commits=my_commits[:pos]
            nbr_commits=nbr_commits.replace(',','')
            nbr_commits=nbr_commits.replace('.','')
        else:
            pos=the_page.find("Commits on master")
            page=the_page[:pos]
            pos1=page.rfind('<strong>')
            pos2=page.rfind('</strong>')
            nbr_commits=''
            if pos1 < pos2:
                nbr_commits=page[pos1+8:pos2]
                nbr_commits=nbr_commits.replace(',','')
                nbr_commits=nbr_commits.replace('.','')
            if len(nbr_commits) == 0:
                nbr_commits = '0'
                
        FreeCAD.Console.PrintMessage(url+'-> commits:'+str(nbr_commits)+'\n')
        if int(nbr_commits) == 0:
            FreeCAD.Console.PrintWarning('We failed to get the commit numbers from github.\n')
        else:
            delta = int(nbr_commits) - commit_nbr
            if delta > 0:
                s = ""
                if delta >1:
                    s="s"
                FreeCAD.Console.PrintError('PLEASE UPDATE "kicadStepUpMod" WB.\n')
                msg="""
                <font color=red>PLEASE UPDATE "kicadStepUpMod" WB.</font>
                <br>through \"Tools\" \"Addon manager\" Menu
                <br><br><b>your release is """+str(delta)+""" commit"""+s+""" behind</b><br>
                <br><a href=\""""+myurlKWB+"""\">KiCad StepUp Wb</a>
                <br>
                <br>set \'checkUpdates\' to \'False\' to avoid this checking
                <br>in \"Tools\", \"Edit Parameters\",<br>\"Preferences\"->\"Mod\"->\"kicadStepUp\"
                """
                QtGui.QApplication.restoreOverrideCursor()
                reply = QtGui.QMessageBox.information(None,"Warning", msg)
            else:
                FreeCAD.Console.PrintMessage('the WB is Up to Date\n')

### END - check_for_updates()


def _prefs_first_time_init(prefs):
    """Initialize user preferences for KiCAD to STEP Workbench"""

    import FreeCAD
    import time
    import os, re
    from sys import platform as _platform

    FreeCAD.Console.PrintWarning('Creating first time KiCAD to STEP preferences\n')

    # Determine Platform to define default model path
    if _platform == "linux" or _platform == "linux2":
        # linux
        default_prefix3d = '/usr/share/kicad/modules/packages3d'
    elif _platform == "darwin":
        # OSX / MacOS
        default_prefix3d = '/Library/Application Support/kicad/packages3d' 
    else:
        # Windows
        default_prefix3d = (os.environ["ProgramFiles"]+u'\\KiCad\\share\\kicad\\modules\\packages3d')
        default_prefix3d = re.sub("\\\\", "/", default_prefix3d)

    # Set Workbench general prefs
    prefs.SetBool("updateChecking", 1)
    prefs.SetInt("updateCheckInterval", 1)   # days
    prefs.SetInt("updateLastChecked", int(time.time())) # seconds

    # ToDo: Install Prefs in these files and remove from here
    prefs.SetString("versionTracks", '')
    prefs.SetString("versionKicadParser", '')
    
    prefs.SetString("last_pcb_path", '')
    prefs.SetString("last_3d_path", '')
    prefs.SetString("lastUserPath", '')

    # Set Import/Export Settings
    #prefs.SetString('prefix3d_1',make_string(default_prefix3d))
    prefs.SetInt('pcb_color',0)
    prefs.SetString('drill_size',u'0.0')
    prefs.SetBool('make_union',0)
    prefs.SetBool('exp_step',0)
    prefs.SetBool('turntable',0)
    prefs.SetBool('generate_sketch',1)
    prefs.SetBool('vrml_materials',1)
    prefs.SetBool('mode_virtual',1)
    prefs.SetInt('pcb_placement',0)
    prefs.SetInt('step_exp_mode',0)
    prefs.SetInt('3D_loading_mode',0)
    prefs.SetInt('sketch_constraints',0)
    prefs.SetString('blacklist',u'')
    prefs.SetString('prefix3d_1',default_prefix3d)
    prefs.SetString('prefix3d_2',u'')
    prefs.SetString('prefix3d_3',u'')
    prefs.SetString('prefix3d_4',u'')
    prefs.SetString('bbox_list',u'')
    prefs.SetString('edge_tolerance',u'0.01')
    prefs.SetBool('asm3_links',1)
    prefs.SetBool('asm3_linkGroups',0)
    prefs.SetBool('stpz_export_enabled',0)
    prefs.SetBool('wrz_export_enabled',0)
    prefs.SetBool('help_warning_enabled',1)
    prefs.SetBool('transparency_material_glass_enabled',0)
    prefs.SetBool('transparency_material_led_enabled',0)
    prefs.SetBool('skip_import_zones',0)

    # Enhanced Prefs
    prefs.SetInt('Tracks_Cu_Weight',0)
    prefs.SetInt('Tracks_Cu_Finish',0)
    prefs.SetInt('PCB_Part_Placement',0)
    prefs.SetInt('Tracks_Pad_Drills',0)
    prefs.SetInt('PCBA_Import_Mode',0)
    prefs.SetString('name_3d_macro',u'')
    prefs.SetString('path_3d_macro',u'')

    #stack_up = prefs.GetGroup("StackUp")
    #stack_up.SetString('ColorToQColor',u'')

    FreeCAD.saveParameter()     # Immediately save the new prefs to user.cfg

### END - _prefs_first_time_init()


def prefs_get():
    """Retrieve/init KiCAD to STEP prefs from FreeCAD Paramter store"""
    import FreeCAD

    prefs = FreeCAD.ParamGet(_workbench_prefs_folder())
    if prefs.IsEmpty():
        _prefs_first_time_init(prefs)
        # Set version of PrefMgmt for first-time
        vers = prefs.GetGroup("Versions")
        vers.SetString(__KTS_PREFS_NAME__, __KTS_PREFS_VER__)
    else:
        # Check to see if we need update stored prefs
        _prefs_check_version(prefs)

    '''
        tnow = int(time.time())
        if prefs.IsEmpty():
            upd=True
            prefs.SetInt("updateDaysInterval",1)
            prefs.SetInt("lastCheck",tnow-2*ONE_DAY)
            prefs.SetInt("dockingMode",0)
            interval=True
            FreeCAD.Console.PrintError('new \'check for updates\' feature added!!!\n')
            msg="""
            <font color=red>new \'check for updates\' feature added!!!</font>
            <br>
            <br>set \'checkUpdates\' to \'False\' to avoid this checking
            <br>in \"Tools\", \"Edit Parameters\",<br>\"Preferences\"->\"Mod\"->\"kicadStepUp\"
            """
            QtGui.QApplication.restoreOverrideCursor()
            reply = QtGui.QMessageBox.information(None,"Warning", msg)
        else:
            upd=prefs.GetBool("checkUpdates")
    '''

    return (prefs)

### END - check_prefs()


def prefs_set_file_version(filename: str, version: str):
    """Add current version of named file to user preferences store."""
 
    import FreeCAD

    prefs = prefs_get()                 # Get the root preferences store for our Workbench
    vers = prefs.GetGroup("Versions")   # Get the "group" for file versions
    vers.SetString(filename, version)
    FreeCAD.saveParameter()             # Immediately save the new prefs to user.cfg
    return None

### END - prefs_set_file_version()


def prefs_get_file_version(filename: str):
    """Add current version of named file to user preferences store."""
 
    prefs = prefs_get()                 # Get the root preferences store for our Workbench
    vers = prefs.GetGroup("Versions")   # Get the "group" for file versions
    return (vers.GetString(filename))

### END - prefs_get_file_version()


def _prefs_check_version(prefs):
    """Check version of prefs stored vs. kts_PrefsMgmt version"""

    vers = prefs.GetGroup("Versions")   # Get the "group" for file versions
    if (vers.GetString(__KTS_PREFS_NAME__) < __KTS_PREFS_VER__):
        vers.SetString("PREFS_IS", "OLD")
        # Here we update it
    elif (vers.GetString(__KTS_PREFS_NAME__) > __KTS_PREFS_VER__):
        # This should never happen, but it's an error
        vers.SetString("PREFS_IS", "TOO NEW")
    else:
        # Just overwrite with the version of this file. 
        vers.SetString(__KTS_PREFS_NAME__, __KTS_PREFS_VER__)
        vers.RemString("PREFS_IS")
    return None

### END - _prefs_check_version()


'''
    time_interval = pg.GetInt("updateDaysInterval")
    if time_interval <= 0:
        time_interval = 1
        pg.SetInt("updateDaysInterval",1)
    nowTimeCheck = int(time.time())
    lastTimeCheck = pg.GetInt("lastCheck")
    #print (nowTimeCheck - lastTimeCheck)/(ONE_DAY*time_interval)
    if time_interval <= 0 or ((nowTimeCheck - lastTimeCheck)/(ONE_DAY*time_interval) >= 1):
        interval = True
        pg.SetInt("lastCheck",tnow)
    else:
        interval = False
                #<li class="commits">
    ##
    if upd and interval:
        check_updates(myurlKWB, mycommitsKWB)
'''
