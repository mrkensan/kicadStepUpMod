# Template Commands showing the possible options...




class FC_std_CMD:
    """Standard Command Template"""

    def __init__(self):
 
    def GetResources(self):     # Resources icon for this tool (Icon, menu text, tool tip, etc...)

        return {'Pixmap'   : '/full/path/to/icon.svg'),                 # Icon shown a Button
                'MenuText' : "Text of Menu Item/Button w/ Mouse Hover", # Text shown when added as Menu
                'ToolTip'  : "Subtext telling more about the Button",   # Tooltip (shown on hover & status bar in UI)
                'Checkable': True | False,                              # Included for On/Off Buttons, T/F is initial state (optional)
                                                                        # param btn_status req'd in Activated to control "on/off"
                "Accel"    : "Shift+S",                                 # a default shortcut (optional)

                }


    def IsActive(self):
        print(">>>>>>>> ktsPcbImportOutline: IsActive Checked [", self.check_count ,"] <<<<<<<<")
        self.check_count += 1
        if (self.check_count < 6):
            return True     # Command is always active
        else:
            return False

    def Activated(self, btn_status):
        import kicadStepUptools
        kicadStepUptools.PullPCB()

# END class - ktsPcbImportOutline




# https://forum.freecadweb.org/viewtopic.php?f=10&t=12208

# Python command group

class TemplatePyGrp_1:
    def Activated(self):
        import FreeCAD
        FreeCAD.Console.PrintMessage("TemplatePyGrp_1\n")

    def GetResources(self):
        return {'Pixmap'  : 'Part_JoinConnect', 'MenuText': 'TemplatePyGrp_1', 'ToolTip': 'Print a message'}

class TemplatePyGrp_2:
    def Activated(self):
        import FreeCAD
        FreeCAD.Console.PrintMessage("TemplatePyGrp_2\n")

    def GetResources(self):
        return {'Pixmap'  : 'Part_JoinEmbed', 'MenuText': 'TemplatePyGrp_2', 'ToolTip': 'Print a message'}

class TemplatePyGrp_3:
    def Activated(self):
        import FreeCAD
        FreeCAD.Console.PrintMessage("TemplatePyGrp_3\n")

    def GetResources(self):
        return {'Pixmap'  : 'Part_JoinCutout', 'MenuText': 'TemplatePyGrp_3', 'ToolTip': 'Print a message'}

class TemplatePyGroup:
    "Example group command class"
    #def Activated(self, index):
    #    print "TemplatePyGroup activated ;-) "

    def GetCommands(self):
        return ("TemplatePyGrp_1", "TemplatePyGrp_2", "TemplatePyGrp_3", "Std_New")

    def GetDefaultCommand(self):
        return 2

    def GetResources(self):
        return {'Pixmap'  : 'python', 'MenuText': 'Group command', 'ToolTip': 'Example group command'}

FreeCADGui.addCommand('TemplatePyGrp_1',TemplatePyGrp_1())
FreeCADGui.addCommand('TemplatePyGrp_2',TemplatePyGrp_2())
FreeCADGui.addCommand('TemplatePyGrp_3',TemplatePyGrp_3())
FreeCADGui.addCommand('TemplatePyGroup',TemplatePyGroup())



# With git commit 27dc80c84 toggle commands are supported now. 
# In Qt terminology this is called 'checkable', not 'toggle'.

# Note:
#   1. The changes compared to a normal command is that
#      'Activated' has a second parameter of type int which is 0 for off and 1 for on.
#   2. The dict returned by GetResources must have the key 'Checkable'. 
#      If this key is present the command becomes a toggle command.
#        If the value is True the command is set to on by default, 
#        if it's False it is set to off. 
#      If the value cannot be interpreted as a boolean an exception is raised.

class TemplatePyCheckable:
    "Example toggle command class"
    def Activated(self, index):
        if index == 0:
            print "Toggle is off"
        else:
            print "Toggle is on"

    def GetResources(self):
        return {'Pixmap'  : 'python', 'MenuText': 'Toggle command', 'ToolTip': 'Example toggle command', 'Checkable': True}

FreeCADGui.addCommand('TemplatePyCheckable',TemplatePyCheckable())


##################################################################################################

# The individual command must set the Checkable key to True. 
# The command must set the Exclusive key to True and it's recommended to set DropDownMenu to False.

# If GetDefaultCommand is not there the first command is toggled, 
# otherwise you can control which other command to toggle. 
# And if you want to have an exclusive group but no toggled command,
# then GetDefaultCommand must be implemented to return a number out of range, e.g. -1.


class Cmd1:
    def Activated(self, index):
        pass

    def GetResources(self):
        return { 'MenuText': 'Command 1', 'Checkable': True}


class Cmd2:
    def Activated(self, index):
        pass

    def GetResources(self):
        return { 'MenuText': 'Command 2', 'Checkable': True}

class Cmd3:
    def Activated(self, index):
        pass

    def GetResources(self):
        return { 'MenuText': 'Command 3', 'Checkable': True}


class Cmd4:
    def Activated(self, index):
        pass

    def GetResources(self):
        return { 'MenuText': 'Command 4'}

class MyGroupCommand:
    def GetCommands(self):
        return ("Cmd1", "Cmd2", "Cmd3", "Cmd4") # a tuple of command names that you want to group

    def Activated(self, index):
        pass

    def GetDefaultCommand(self): # return the index of the tuple of the default command. This method is optional and when not implemented '0' is used  
        return 2

    def GetResources(self):
        return { 'MenuText': 'Group command', 'ToolTip': 'Example group command', 'DropDownMenu': False, 'Exclusive' : True, }
        
    def IsActive(self): # optional
        return True

FreeCADGui.addCommand('Cmd1',Cmd1())
FreeCADGui.addCommand('Cmd2',Cmd2())
FreeCADGui.addCommand('Cmd3',Cmd3())
FreeCADGui.addCommand('Cmd4',Cmd4())
FreeCADGui.addCommand('MyGroupCommand',MyGroupCommand())