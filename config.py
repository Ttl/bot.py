"""Contains origin for screen and mouse functions."""
ox, oy = (0,0)

def setOrigin(coordinates):
	global ox,oy
	ox,oy = coordinates
	
def getOrigin():
	global ox,oy
	return ox,oy
