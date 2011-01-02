import sys

if sys.platform == 'darwin':
    raise NotImplementedError

if sys.platform == 'win32':
    raise NotImplementedError

else:
    from linux import *

