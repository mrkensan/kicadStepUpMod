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
#*  KiCAD_2STEP - Render KiCAD PCB Models as STEP (No Round Trip, etc...)   *
#*                                                                          *
#****************************************************************************

from kts_versions import *

class kSU_MainPrefPage:

    def selectDirectory(self):
        from PySide import QtGui, QtCore
        selected_directory = QtGui.QFileDialog.getExistingDirectory()
        # Use the selected directory...
        print ('selected_directory:', selected_directory)

    def __init__(self, parent=None):
        from PySide import QtGui, QtCore
#!#        import os, hlp
        # Text for 'Help Tips' Pref Panel
        import hlp
        global ksuWBpath
        print ("Created kSU 'Help Tips' Pref panel")
        header_txt="""<font color=GoldenRod><b>kicad StepUp version """+verKSU+"""</font></b><br>"""
        help_t = header_txt+hlp.help_txt

        self.form = QtGui.QWidget()
        self.form.setWindowTitle("kSU \'Help Tips\'")
        self.form.verticalLayoutWidget = QtGui.QWidget(self.form)
        self.form.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 530, 650)) #top corner, width, height
        self.form.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.form.verticalLayout = QtGui.QVBoxLayout(self.form.verticalLayoutWidget)
        self.form.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.form.verticalLayout.setObjectName("verticalLayout")
        #self.form.label = QtGui.QLabel(self.form.verticalLayoutWidget)
        #self.form.label.setObjectName("label")
        #self.form.label.setText("Hello world!")
        #self.form.verticalLayout.addWidget(self.form.label)
        self.form.textEdit = QtGui.QTextBrowser(self.form.verticalLayoutWidget)
        self.form.textEdit.setGeometry(QtCore.QRect(00, 10, 530, 640)) #top corner, width, height
        self.form.textEdit.setOpenExternalLinks(True)
        self.form.textEdit.setObjectName("textEdit")
        self.form.textEdit.setText(help_t)        
# Button UI
        add_button=False
        if add_button:
            self.form.btn = QtGui.QPushButton('Create Folder', self.form.verticalLayoutWidget)
            self.form.btn.setToolTip('This creates the folders.')
            self.form.btn.resize(self.form.btn.sizeHint())
            self.form.btn.move(5, 60)       
            self.form.btn.clicked.connect(self.selectDirectory)   
            self.form.verticalLayout.addWidget(self.form.btn)        
        
#!#   def saveSettings(self):
#!#       print ("saveSettings Helper")
#!#       import SaveSettings
#!#       SaveSettings.update_ksuGui()
#!#       
#!#   def loadSettings(self):
#!#       print ("loadSettings Helper")
#!#       prefs = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/kicadStepUpGui").GetString('prefix3d_1')+'/'
#!#       print('KISYS3DMOD assigned to: ', prefs)
#!#       prefs = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/kicadStepUpGui")
#!#       #if prefs.GetContents() is not None:
#!#       #    for p in prefs.GetContents():
#!#       #        print (p)
#!#       print(FreeCAD.getUserAppDataDir())

### END - class kSU_MainPrefPage



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


def prefs_first_time_init(prefs):
    """Initialize user preferences for KiCAD to STEP Workbench"""

    import time, FreeCAD
    import os, re
    from sys import platform as _platform
   # from kts_versions import KTS_WORKBENCH_VER, KTS_PREFS_VER


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
        default_prefix3d = re.sub("\\\\", "/", default_prefix3d) #default_prefix3d.replace('\\','/')


    # Set Workbench general prefs
    prefs.SetBool("updateChecking", 1)
    prefs.SetInt("updateCheckInterval", 1)   # days
    prefs.SetInt("updateLastChecked", int(time.time())) # seconds
    #!# prefs.SetInt("dockingMode", 0)
    prefs.SetString("versionWorkbench", KTS_WORKBENCH_VER)
    prefs.SetString("versionPrefs", KTS_PREFS_VER)
    prefs.SetString("versionTracks", '')
    prefs.SetString("versionKicadParser", '')

    prefs.SetString("last_pcb_path", '')
    prefs.SetString("last_3d_path", '')
    prefs.SetString("lastUserPath", '')
    prefs.SetString("versionPrefs", KTS_PREFS_VER)
    prefs.SetString("versionPrefs", KTS_PREFS_VER)
    prefs.SetString("versionPrefs", KTS_PREFS_VER)
    prefs.SetString("versionPrefs", KTS_PREFS_VER)
    prefs.SetString("versionPrefs", KTS_PREFS_VER)

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

    FreeCAD.saveParameter()     # Immediately save the new prefs to user.cfg

### END - prefs_first_time_init()


def check_prefs():
    """Retrieve/init KiCAD to STEP preferences\nCheck for workbench updates"""
    import FreeCAD, time

    ONE_DAY = 86400

    prefs = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/KiCAD_2STEP")
    if prefs.IsEmpty():
        prefs_first_time_init(prefs)

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

    return(prefs)

### END - check_prefs()



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
