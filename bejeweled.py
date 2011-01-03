#http://www.digbejeweled.com/
"""Instructions:

1. Goto http://www.digbejeweled.com/
2. Make sure game is visible
3. Run this script
4. Watch the computer play the game for you.
"""

from config import *
from screen import *
from mouse import *
from time import sleep

try:
    import psyco
    psyco.full()
except:
    print 'Psyco not found'

sx, sy = getScreenSize()
w = 36                      #Width between cells in pixels
gx,gy = (151,5)             #Top left corner of play area

def gameOver():
    return getPixel(436,289)==(0,49,99) and getPixel(142,313)==(147,139,72)

def findPlay():
    c = getPixel(342,279)
    if c in ((65,171,199),(5, 54, 126)):#Button changes color on mouse over
        mouseClick(342,279) #Double click just to be sure
        mouseClick(342,279)
        sleep(1)

def init():
    #Set origin
    originDTM = DTM({(0, 0): (232, 64, 207), (450, 323): (150, 137, 46)})
    origin = findDTM(originDTM,0,0,sx,sy)
    if origin==False:
        print "Couldn't find the game!"
        quit(0)
    setOrigin(origin)
    #setOrigin(findColor(0,0,sx,sy,(232,64,207)))#Alternative way using colors
    mouseClick(0,0,True)#Focus window
    sleep(0.2)
    findPlay()

def readSquares():
    global board,w,gx,gy
    area = getArea(gx,gy,gx+8*w,gy+8*w)
    for x in xrange(8):
        for y in xrange(8):
            board[x][y]=area.getpixel((x*w+10,y*w+14))    


def checkMove(x,y,x1,y1):
    gem1 = board[x][y]
    gem2 = board[x1][y1]

    board[x][y]=gem2
    board[x1][y1]=gem1
    bestmatch1 = 0 

    prev = -1
    matched = 0
    for i in xrange(max(0,x-3),min(8,x+3)):
        if board[i][y]==prev:
            matched+=1
        else:
            matched=0
        if matched>1 and matched>bestmatch1:
            bestmatch1 = matched
        prev=board[i][y]

    prev=-1
    matched=0
    bestmatch2=0
    for i in xrange(max(0,y-3),min(8,y+3)):
        if board[x][i]==prev:
            matched+=1
        else:
            matched=0
        if matched>1 and matched>bestmatch2:
            bestmatch2 = matched
        prev=board[x][i]

    #Undo move
    board[x1][y1]=gem2
    board[x][y]=gem1
    return bestmatch1+bestmatch2 

def tryMoves():
    global board
    bestMove = [-1,0,0,False]#score,x,y,move right
    for y in xrange(7,-1,-1):#Test moves from bottom to up
        for x in xrange(8):
            if (x-1>=0):
                t = checkMove(x,y,x-1,y)
                if t > bestMove[0]:
                    bestMove = [t,x-1,y,True]
            if (x+1<=7):
                t = checkMove(x,y,x+1,y)
                if t > bestMove[0]:
                    bestMove = [t,x,y,True]
            if (y-1>=0):
                t = checkMove(x,y,x,y-1)
                if t > bestMove[0]:
                    bestMove = [t,x,y-1,False]
            if (y+1<=7):
                t = checkMove(x,y,x,y+1)
                if t > bestMove[0]:
                    bestMove = [t,x,y,False]
    if bestMove[0]>1:
        makeMove(bestMove[1],bestMove[2],bestMove[3])
    return None

def makeMove(x1,y1,right):
    global board,w,gx,gy
    #Save mouse position and move mouse back where it was after clicking
    pos = mousePos()
    if right:
        mouseClick(gx+w*x1+18,gy+w*y1+18, True)
        mouseClick(gx+w*(x1+1)+18,gy+w*y1+18, True)
    else:
        mouseClick(gx+w*x1+18,gy+w*y1+18, True)
        mouseClick(gx+w*x1+18,gy+w*(y1+1)+18, True)
    mouseMove(pos[0],pos[1])

board=[ [0 for i in xrange(8)] for c in xrange(8) ]
init()
while not gameOver(): 
    readSquares()
    tryMoves()
    sleep(0.2)
print 'Game Over'
