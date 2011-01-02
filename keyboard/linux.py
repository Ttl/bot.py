from pyatspi import Registry as registry
from pyatspi import (KEY_SYM, KEY_PRESS, KEY_PRESSRELEASE, KEY_RELEASE)

def pressKey(key):
    registry.generateKeyboardEvent(key, None, KEY_SYM)
