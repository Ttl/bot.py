"""Program for picking colors from screen."""
from mouse import *
from screen import *
import sys

ox,oy = (0,0)
if len(sys.argv)>=3:
    ox = int(sys.argv[1])
    oy = int(sys.argv[2])

prev=(-1,-1)
while True:
    temp = mousePos()
    if temp != prev:
        print temp[0]-ox,temp[1]-oy, getPixel(temp[0],temp[1])
        prev = temp
