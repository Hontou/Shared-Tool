#Common imports on others, presume needed
import os
import uuid
from Tool import *
#Date/Time imports
from datetime import *

#Gets the current date and then turns into usable vars
def getTDate():
    tD = str(date.today())
    y1,y2,y3,y4,h1,m1,m2,h2,d1,d2 = tD
    tDList = [d1,d2,m1,m2]
    return tDList

def getDM():
    DMT = getTDate()
    DM = DMT[0] + DMT[1] + DMT[2] + DMT[3]
    return DM

print(getDM())
