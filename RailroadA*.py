import heapq
import pickle
from math import pi , acos , sin , cos
from tkinter import *
graph = pickle.load(open("nestedDict.pk", "rb"))

dists = open("rrNodes.txt")
names = open("rrNodeCity.txt")
coords = {}
for line in dists:
    name = line.split(" ")[0].strip()
    lat = line.split(" ")[1].strip()
    long = line.split(" ")[2].strip()
    coords[name] = (lat, long)

coded = {}
for line in names:
    split = line.split(" ", 1)
    coded[split[1].strip()] = split[0].strip()

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

class Node:
    def __init__(self, data, parent, goal):
        global coords
        self.data = data
        self.parent = parent
        self.goal = goal
        self.g = 0
        self.h = calcd(coords[goal][0], coords[goal][1], coords[data][0], coords[data][1])
        nested = Graph(graph)
        self.neighbors = nested.getNeighbors(data)
        if parent is not None:
            self.g = nested.getEdgeLength(parent, data) + parent.g
        self.f = self.g + self.h

    def __lt__(self, other):
        return 1

class Graph:
    def __init__(self, data):
        self.data = data
    def getNeighbors(self, name):
        neighbors = set()
        for key in self.data[name].keys():
            neighbors.add(key)
        return neighbors
    def getEdgeLength(self, parent, kid):
        return self.data[parent.data][kid]

def A_star(start_node):
    fringe = []
    visited = set()
    heapq.heappush(fringe, (start_node.f, start_node))
    while not (len(fringe) == 0):
        v = heapq.heappop(fringe)
        v = v[1]
        if v.data == v.goal:
            createMap(visited, v)
            return v
        visited.add(v.data)
        for neigh in v.neighbors:
            if neigh not in visited:
                n = Node(neigh, v, v.goal)
                heapq.heappush(fringe, (n.f, n))
    return None


def main():
    fro = input("From?\t")
    to = input("To?\t")
    ans = A_star(Node(coded[fro.strip()], None, coded[to.strip()]))
    print("Shortest Length:", ans.g)


def createMap(visited, goal):
    root = Tk()
    canvas = Canvas(root, width=1200, height=1200)
    canvas.pack()
    root.update()

    scaled = {}
    for key in coords:
        k = 15
        x = (float(coords[key][1]) - -130.35722) * k
        y = (60.84682 - float(coords[key][0])) * k
        scaled[key] = (x, y)


    pointer = goal
    while pointer.parent is not None:
        canvas.create_line(scaled[pointer.parent.data][0], scaled[pointer.parent.data][1], scaled[pointer.data][0],
                           scaled[pointer.data][1], width=2, fill="blue")
        pointer = pointer.parent

    for key in scaled:
        k = 15
        x = scaled[key][0]
        y = scaled[key][1]
        dot = canvas.create_oval(x, y, x, y, fill='black')
        if key in visited:
            canvas.itemconfig(dot, outline="red", fill="red")
        if key == goal.data:
            canvas.itemconfig(dot, outline="#AB12D5", fill="#AB12D5")
            canvas.create_text(scaled[key][0], scaled[key][1], text="Goal", font="Times 20 italic bold", fill="#AB12D5")
        if key == pointer.data:
            canvas.itemconfig(dot, outline = "#AB12D5", fill="#AB12D5")
            canvas.create_text(scaled[key][0], scaled[key][1], text="Start", font="Times 20 italic bold", fill="#AB12D5")

    root.mainloop()

if __name__ == "__main__":
    main()

#14.68673, 60.84682
#-130.35722, -60.02403