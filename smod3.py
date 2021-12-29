import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/System'))
from System.Core import Interface
if __name__ == "__main__":
    try:
        Interface.init()
        Interface.mainLoop()
    except:
        exit(0)
