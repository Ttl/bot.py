"""Program for picking colors from screen."""
from main import *

def init():
    global ox,oy
    #Set origin
    sx, sy = getScreenSize()
    ox,oy = findColor(0,0,sx,sy,(232,64,207))
    mouseMove(0,0)

#init()
ox,oy = (0,0)
prev=(-1,-1)
while True:
    temp = mousePos()
    if temp != prev:
        print temp[0]-ox,temp[1]-oy, getPixel(temp[0],temp[1])
        prev = temp
