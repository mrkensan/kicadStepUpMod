# -*- coding: utf-8 -*-
#****************************************************************************
#*                                                                          *
#*  Kicad STEPUP (TM) (3D kicad board and models to STEP) for FreeCAD       *
#*  3D exporter for FreeCAD                                                 *
#*  Kicad STEPUP TOOLS (TM) (3D kicad board and models to STEP) for FreeCAD *
#*  Copyright (c) 2015                                                      *
#*  Maurice easyw@katamail.com                                              *
#*                                                                          *
#*  Kicad STEPUP (TM) is a TradeMark and cannot be freely useable           *
#*                                                                          *

#class ColorLib:

# ***************************************************
# Convert color into FreeCAD color style
#
def ColorToFreeCad(*color):
    from past.builtins import basestring

    if len(color)==1:
        if isinstance(color[0],basestring):
            if color[0].startswith('#'):
                #color = color[0].replace('#','0x')
                #color = int(color,0)
                #print (color)
                #r = float((color>>24)&0xFF)
                #g = float((color>>16)&0xFF)
                #b = float((color>>8)&0xFF)
                color = color[0] #[1:]
                #print(color[1:3])
                r = int((color[1:3]), 16) #/255
                g = int((color[3:5]), 16) #/255
                b = int((color[5:7]), 16) #/255
                #print(r,g,b);stop
                #print(r,g,b)
                #stop
            else:
                color = int(color[0],0)
                r = float((color>>24)&0xFF)
                g = float((color>>16)&0xFF)
                b = float((color>>8)&0xFF)
        else:
            color = color[0]
            r = float((color>>24)&0xFF)
            g = float((color>>16)&0xFF)
            b = float((color>>8)&0xFF)
    else:
        r,g,b = color
    return (r/255.0,g/255.0,b/255.0)


# *************************************************************************
# Return Copper Thickness & Name for Prefs Setting
# https://www.pcbuniverse.com/pcbu-tech-tips.php?a=4
# https://www.smta.org/chapters/files/UMW_Viasystems_Surface_Finishes.pdf
def GetCuWeight(n):
    return {
        0 : (0.001, "Face Only"),   # 0 oz Render Face only
        1 : (0.017, "0.5 oz"),
        2 : (0.035, "1.0 oz"),
        3 : (0.052, "1.5 oz"),
        4 : (0.070, "2.0 oz"),
        5 : (0.087, "2.5 oz"),
        6 : (0.104, "3.0 oz")
    }.get(n, (-1, "Error"))   # -1 is default if n not found


# *************************************************************************
# Return Pad Surface Finish Thickness, Color & Name for Prefs Setting
# https://www.epectec.com/downloads/Surface-Finishes.pdf
def GetPadFinish(n):
    return {
        0 : (0.005, "#FCC9AC", "Bare Copper"),
        1 : (0.004, "#D0B062", "ENIG (Gold)"),
        2 : (0.005, "#DBDCDC", "RoHS (Lead-Free)"),
        3 : (0.007, "#ADA89E", "HASL (63Pb / 37Sn)"),
        4 : (0.001, "#CBC9C6", "Immersion Silver"),
        5 : (0.002, "#BABDA0", "Immersion Tin")
    }.get(n, (-1, "FFFFFF", "Error"))   # -1 is default if n not found


# *************************************************************************
# Return PCB Color, Track Color, Silk Color, and Board Color Name
#   Silkscreen color is "White" except for white boards, then "Black"
def GetPcbColors(n):
    return {
        0 : ("#A2161E", "#1CAA46", "#F8F8F0", "Light Green"),  # "#068631", "#1CAA46"
        1 : ("#164191", "#0861BD", "#F8F8F0", "Blue"),
        2 : ("#068631", "#1CAA46", "#F8F8F0", "Red"),          # "#A2161E", "#D42634"
        3 : ("#542D70", "#8C4ba0", "#F8F8F0", "Purple"),
        4 : ("#073825", "#1B6F49", "#F8F8F0", "Dark Green"),
        5 : ("#1D355C", "#065391", "#F8F8F0", "Dark Blue"),
        6 : ("#0078B5", "#0091C8", "#F8F8F0", "Light Blue"),
        7 : ("#b19600", "#d39d1a", "#F8F8F0", "Yellow"),
        8 : ("#1A2127", "#a17961", "#F8F8F0", "Black"),
        9 : ("#EDF0F5", "#E1E2E5", "#2D2D2D", "White")
    }.get(n,("#FFFFFF", "#FFFFFF", "Error"))   # if n not found


