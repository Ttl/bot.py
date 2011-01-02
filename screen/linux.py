import gtk.gdk
import PIL.Image

#Global congiguration
import config

def getArea(x1,y1,x2,y2):
    """Return image of desktop.
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

"""Sets up some global variables.
size is tuple of screen size.
root is handle to accessing display.""" 
root = gtk.gdk.get_default_root_window()
size = gtk.gdk.get_default_root_window().get_size()
colormap = gtk.gdk.colormap_get_system()
