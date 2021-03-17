
#%%
import math
from Point import *
from FlowNetwork import FlowNetwork
from Chord import *
import copy

class RectilinearPolygon:
    def __init__(self, file):
        self._vertices = [] 
        self._vert_chords = []
        self._horiz_chords = []
        self._graph = {}
        
        #Read the vertices from file into a list
        with open(file) as f:
            lines = f.readlines()
            for i in range(len(lines)):
                x, y = map(int, lines[i].strip('\n').split(','))
                self._vertices.append(sPoint(x, y))

        self._V = len(self._vertices)
        if self._V < 4:
            raise ValueError
        
        for i in range(self._V-1):
            self._graph[self._vertices[i]] = [self._vertices[i-1], self._vertices[i+1]]
        self._graph[self._vertices[self._V-1]] = [self._vertices[self._V-2], self._vertices[0]]

        #Find cohorizontal and covertical chords
        self._chordset()
        

    def is_concave(self, vertex: sPoint):
        v1 = self._graph[vertex][0].getCoord()
        v2 = self._graph[vertex][1].getCoord()
        v = vertex.getCoord()
        
        x1, y1 = v1[0] - v[0], v1[1] - v[1]
        x2, y2 = v2[0] - v[0], v2[1] - v[1]

        numerator = (x1 * x2 + y1 * y2)
        denom = math.sqrt((x1 ** 2 + y1 ** 2) * (x2 ** 2 + y2 ** 2))
        angle = (math.acos(numerator / denom) * 180 / (math.pi))
        sign = (x1 * y2) > (x2 * y1)
        
        if (sign == True and angle == 90.0) or (sign == False and angle == 270.0):
            return True
                
        return False

    #Creates horizontal and vertical chordset lists stored as tuples (vertex1, vertex2)
    def _chordset(self):
        covert_set = sorted(self._vertices, key=lambda k: [k.getCoord()[0], k.getCoord()[1]])

        i = 0
        while i < len(covert_set)-1:
            v1 = covert_set[i]
            v2 = covert_set[i+1]

            if v1.getCoord()[0] == v2.getCoord()[0]:
                if not self.is_edge(v1, v2):
                    if self.is_concave(v1) and self.is_concave(v2):
                        self._vert_chords.append((v1,v2))
            i += 1

        cohoriz_set = sorted(self._vertices, key=lambda k: [k.getCoord()[1], k.getCoord()[0]])        
        i = 0
        while i < len(cohoriz_set)-1:
            v1 = cohoriz_set[i]
            v2 = cohoriz_set[i+1]

            if v1.getCoord()[1] == v2.getCoord()[1]:
                if not self.is_edge(v1, v2):
                    if self.is_concave(v1) and self.is_concave(v2):
                        self._horiz_chords.append((v1,v2))
            i += 1

    def is_edge(self, v1: sPoint, v2: sPoint):
        if v1 == None or v2 == None:
            return False

        if (v1 in self._graph) and (v2 in self._graph[v1]):
            return True
        
        return False
    
    def find_edge(self, p):
        cohoriz_set = sorted(self._vertices, key=lambda k: [k.getCoord()[1], k.getCoord()[0]])

        ind = cohoriz_set.index(p)
        p = p.getCoord()
        
        up = 0
        for e in self._graph[p]:
            e = e.getCoord()
            if e[0] == p[0]:
                up = p[1] - e[1]

        if up < 0:
            for i in range(ind-1, 0, -1):
                c = cohoriz_set[i].getCoord()
                if c[1] != p[1]:
                    for e in self._graph[c]:
                        e = e.getCoord()
                        if c[1] == e[1] and (p[0] in range(c[0], e[0]+1)):
                            return sPoint(p[0], c[1])
        
        if up > 0:
            for i in range(ind+1, len(cohoriz_set), +1):
                c = cohoriz_set[i].getCoord()
                if c[1] != p[1]:
                    for e in self._graph[c]:
                        e = e.getCoord()
                        if c[1] == e[1] and (p[0] in range(c[0], e[0]+1)):
                            return sPoint(p[0], c[1])
        return None

    #cv = vertex that a vertical line will be drawn from
    def _draw_horiz(self, cv):
        for x in cv:
            end = self.find_edge(x)
            if end != None:
                self._graph[x].append(end)
                self._vertices.append(end)
            

    def minimum_cover(self):
        network = FlowNetwork(self._vert_chords, self._horiz_chords)
        polygon_covering = [copy.deepcopy(self._graph)]

        max_ind_set = network.maxInd()
        for x in max_ind_set:         
            self._graph[x[0]].append(x[1])
            self._graph[x[1]].append(x[0])

        
        concave_set = []
        for v in self._vertices:
            if len(self._graph[v]) == 2 and self.is_concave(v):
                concave_set.append(v)
        
        self._draw_horiz(concave_set)
        polygon_covering.append(copy.deepcopy(self._graph))
        return polygon_covering
# %%
