import pickle
from math import pi , acos , sin , cos

edges = open("rrEdges.txt")
dists = open("rrNodes.txt")

nested = {}
distdict = {}

def calcd(y1,x1, y2,x2):
   y1  = float(y1)
   x1  = float(x1)
   y2  = float(y2)
   x2  = float(x2)
   R   = 3958.76
   y1 *= pi/180.0
   x1 *= pi/180.0
   y2 *= pi/180.0
   x2 *= pi/180.0
   return acos( sin(y1)*sin(y2) + cos(y1)*cos(y2)*cos(x2-x1) ) * R

for line in dists:
    name = line.split(" ")[0].strip()
    lat = line.split(" ")[1].strip()
    long = line.split(" ")[2].strip()
    distdict[name] = (lat, long)

for line in edges:
    one = line.split(" ")[0].strip()
    two = line.split(" ")[1].strip()
    if one not in nested:
        nested[one] = {}
    if two not in nested:
        nested[two] = {}
    dist = calcd(distdict[one][0], distdict[one][1], distdict[two][0], distdict[two][1])
    nested[one][two] = dist
    nested[two][one] = dist

pickle.dump(nested, open("nestedDict.pk", "wb"))

print(nested["4800332"]["4800260"])