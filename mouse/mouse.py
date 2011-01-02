import config
from pymouse import *
from time import sleep
mouse = PyMouse()

def mouseClick(x,y,left=True,delay=0.0):
    x+=config.ox
    y+=config.oy
    mouse.press(x,y,left)
    sleep(delay)
    mouse.release(x,y,left)
    
def mouseDoubleClick(x,y,left=True,delay=0.0,delay2=0.3):
    x+=config.ox
    y+=config.oy
    mouse.press(x,y,left)
    sleep(delay)
    mouse.release(x,y,left)
    sleep(delay2)
    mouse.press(x,y,left)
    sleep(delay)
    mouse.release(x,y,left)
    
def mouseMove(x,y):
    mouse.move(config.ox+x,config.oy+y)

def mousePress(x,y):
    mouse.press(config.ox+x,config.oy+y)

def mouseRelease(x,y):
    mouse.release(config.ox+x,config.oy+y)

def mouseDrag(x1,y1,x2,y2):
    mouse.press(config.ox+x1,config.oy+y1)
    mouse.move(config.ox+x2,config.oy+y2)
    mouse.release(config.ox+x2,config.oy+y2)

def mousePos():
    t = mouse.position()
    return t[0]-config.ox,t[1]-config.oy
