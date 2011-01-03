import PIL.Image
import config
import gtk.gdk

"""Sets up some global variables.
size is tuple of screen size.
root is handle to accessing display.""" 
root = gtk.gdk.get_default_root_window()
size = gtk.gdk.get_default_root_window().get_size()
colormap = gtk.gdk.colormap_get_system()
    
class DTM():
    """DTM is array of pixel locations and colors
    pixels format { (0,0):(r,g,b), (x,y):(r1,g1,b1), ... }
    """
    def __init__(self,pixels):
        self.pixels = pixels
        self.len = len(self.pixels.keys())
        topx,topy = (0,0)
        botx,boty = (0,0)
        for i in pixels.keys():
            if i[0]<topx:
                topx = i[0]
            if i[0]>botx:
                botx = i[0]
            if i[1]<topy:
                topy = i[1]
            if i[1]>boty:
                boty = i[1]
        self.bounds = (topx,topy,botx,boty)
    def __str__(self):
        return str(pixels)
    def iterPixels(self):
        for i,j in self.pixels.items():
            yield i,j
            
            
def getArea(x1,y1,x2,y2):
    """Return area from desktop.
    Thanks to FionaSarah for the code."""
    global root, colormap
    x1+=config.ox
    y1+=config.oy
    x2+=config.ox
    y2+=config.oy
    x,y=x2-x1,y2-y1
    screengrab = gtk.gdk.Pixbuf(
        gtk.gdk.COLORSPACE_RGB,
        False,
        8,
        x,
        y
      )

    screengrab.get_from_drawable(
        root, 
        colormap,
        x1, y1, 0, 0,
        x,
        y
      )

    final_screengrab = PIL.Image.frombuffer(
      "RGB",
      (x, y),
      screengrab.get_pixels(),
      "raw",
      "RGB",
      screengrab.get_rowstride(),
      1
    )
    return final_screengrab

def getScreenSize():
    return size
    
def toleranceEqual(color1,color2,tolerance):
    """Function for checking if two colors are equal within tolerance"""
    for i in (0,1,2):
        if not color1[i]-tolerance<=color2[i]<=color1[i]+tolerance:
            return False
    return True

def similarity(color1,color2):
    """Return how similar colors are. Similarity of black and white is 0.0 and
    two same colors is 1.0"""
    out = 0.0
    for i in (0,1,2):
        out += abs(color1[i]-color2[i])
    return 1.0 - out/765
    
        
def getPixel(x, y):
    """Returns pixel color of screen"""
    return getArea(x,y,x+1,y+1).getpixel((0,0))

def findColor(x1,y1,x2,y2,color,tolerance=0):
    """Tries to find color in an area of screen. Returns False if not found"""
    image = getArea(x1,y1,x2,y2)
    equal = (lambda x,y,z: x==y) if tolerance==0 else toleranceEqual
    for i in xrange(x2-x1):
        for j in xrange(y2-y1):
            if equal(image.getpixel( (i,j) ), color, tolerance):
                return (x1+i,y1+j)
    return False

def findDTM(dtm, x1, y1, x2, y2, tolerance=0):
    """Tries to find array of pixels from image"""
    image = getArea(x1,y1,x2,y2)
    topx, topy, botx, boty = dtm.bounds
    sx,sy = x2-x1,y2-y1
    equal = lambda x,y,z:x==y
    if tolerance==0:
        equal = (lambda x,y,z: x==y)
    else:
        equal = toleranceEqual
    for x in xrange(-topx,sx-botx):
        for y in xrange(-topy,sy-boty):
            for (i,j) in dtm.iterPixels():
                if not equal(image.getpixel((x+i[0],y+i[1])),j,tolerance):
                    break
            else:
                return x+x1,y+y1

    return False

def findDTMi(dtm, image, x1, y1, x2, y2, tolerance=0):
    """Tries to find array of pixels from image"""
    topx, topy, botx, boty = dtm.bounds
    sx,sy = x2-x1,y2-y1
    if tolerance==0:
        equal = (lambda x,y,z: x==y)
    else:
        equal = toleranceEqual
    for x in xrange(-topx,sx-botx):
        for y in xrange(-topy,sy-boty):
            for (i,j) in dtm.iterPixels():
                if not equal(image.getpixel((x+i[0],y+i[1])),j,tolerance):
                    break
            else:
                return x+x1,y+y1
    return False

def similarityDTMi(dtm, image, x1, y1, x2, y2):
    """Returns float in range 0.0-1.0 indicating how well dtm fits in image"""
    topx, topy, botx, boty = dtm.bounds
    sx,sy = x2-x1,y2-y1
    length = dtm.len
    maxsim = 0.0
    for x in xrange(-topx,sx-botx):
        for y in xrange(-topy,sy-boty):
            result = 0.0
            for (i,j) in dtm.iterPixels():
                result+=similarity(image.getpixel((x+i[0],y+i[1])),j)
            temp = result / length
            if temp==1.0:#Can't get higher than this
                return 1.0
            if temp>maxsim:
                maxsim = temp           
    return maxsim
