"""Helps creating DTMs.

Press <Ctrl>+A to add pixel to dtm,
<Ctrl>S to clear DTM
and <Ctrl>D to print color under cursor"""

from bot import *
import gtk
import keybinder

dmt = {}

def printdmt():
    global dmt
    print dmt 

def dmtAdd():
    global ox,oy
    pos = mousePos()
    if dmt == {}:
        ox,oy = pos
    dmt[(pos[0]-ox,pos[1]-oy)]= getPixel(pos[0],pos[1])
    printdmt()

def dmtClear():
    global dmt
    dmt = {}
    print "Cleared"

def printColor():
    t = mousePos()
    print getPixel(t[0],t[1])

add = "<Ctrl>A"
clear = "<Ctrl>S"
color = "<Ctrl>D"

keybinder.bind(add,dmtAdd)
keybinder.bind(clear,dmtClear)
keybinder.bind(color,printColor)
gtk.main()
