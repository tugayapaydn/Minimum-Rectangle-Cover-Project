from Point import *
from Chord import *
import sys

class FlowNetwork:
    def __init__(self, vert_chords, horiz_chords):
        self.__UNIT_EDGE_CAPACITY = 1
        self.__INF_EDGE_CAPACITY = float('inf')
        self.__vert_chords = vert_chords
        self.__horiz_chords = horiz_chords
        self.create_bipartite_graph()

    def create_bipartite_graph(self):
        vert_len = len(self.__vert_chords)
        horiz_len = len(self.__horiz_chords)
        self.__num =  vert_len + horiz_len + 2
        
        self.__vertices = [(sPoint(sys.maxsize, sys.maxsize), sPoint(sys.maxsize, sys.maxsize))] + self.__horiz_chords + self.__vert_chords + [(sPoint(sys.maxsize-1, sys.maxsize-1), sPoint(sys.maxsize-1, sys.maxsize-1))]
        self.__graph = {}
        self.__graph_cap = {}
        self.__reversed_graph = {}

        self.__graph[self.__vertices[0]] = [x for x in self.__horiz_chords]
        self.__graph_cap[self.__vertices[0]] = [self.__UNIT_EDGE_CAPACITY for i in range(horiz_len)]
        self.__graph[self.__vertices[self.__num-1]] = []

        #Add edges from horizontal chords → vertical chords
        
        ch = Chord((None, None), (None, None))
        for h in self.__horiz_chords:
            self.__graph[h] = [v for v in self.__vert_chords if ch.intersect(h[0], h[1], v[0], v[1])]
            self.__graph_cap[h] = [self.__INF_EDGE_CAPACITY for i in range(len(self.__graph[h]))]
        
        for v in self.__vert_chords:
            self.__graph[v] = [self.__vertices[self.__num-1]]
            self.__graph_cap[v] = [self.__UNIT_EDGE_CAPACITY]
            self.__reversed_graph[v] = [h for h in self.__horiz_chords if ch.intersect(h[0], h[1], v[0], v[1])]

    def intersects(self, c1, c2):
        if not (c1[0] == c2[0] and c1[1] == c2[1]): 
            if  (c1[0] == c2[0]) or (c1[0] == c2[1]) or (c1[1] == c2[0]) or (c1[1] == c2[1]):
                return True
        return False
    
    def find_in_graph(self, ch_s, ch_des):
        i = 0
        for s in self.__graph[ch_s]:
            if s == ch_des:
                return i
            i += 1
        return -1

    def BFS_HASH(self, s, t, parent):
        visited = {}
        queue = []
        queue.append(s)

        while queue:
            u = queue.pop(0)

            for i in range(len(self.__graph[u])):
                neighbour = self.__graph[u][i]
                if (((neighbour in visited) and (visited[neighbour] == False)) or (neighbour not in visited)) and self.__graph_cap[u][i] > 0:
                    queue.append(neighbour)
                    parent[neighbour] = u
                    visited[neighbour] = True

        return True if ((t in visited) and (visited[t])) else False

    def max_flow(self):
        source = self.__vertices[0]
        sink = self.__vertices[self.__num-1]
        parent = {}
        v_list = []

        k = 0
        while self.BFS_HASH(source, sink, parent):
            v_list.append([])

            path = float("Inf")
            
            s = sink
            while s != source:
                i = self.find_in_graph(parent[s], s)
                path = min(path, self.__graph_cap[parent[s]][i])
                s = parent[s]

            v = sink
            while v != source:
                i = self.find_in_graph(parent[v], v)
                self.__graph_cap[parent[v]][i] -= path
                v_list[k].append((parent[v], v))
                v = parent[v]
            k = k+1

        max_match = []
        for m in v_list:
            max_match.append((m[1][0], m[1][1]))

        return max_match
        
    
    #Removes edges between chords(vertices) of the bipartite graph
    def remove_edge(self, e):
        if e[0] in self.__graph:
            g = self.__graph[e[0]]
            i = 0
            j = len(g)
            while i < j:
                if g[i] == e[1]:
                    g.pop(i)
                    j -= 1
                i += 1
                    
        if e[1] in self.__reversed_graph:
            g = self.__reversed_graph[e[1]]
            i = 0
            j = len(g)
            while i < j:
                if g[i] == e[0]:
                    g.pop(i)
                    j -= 1
                i += 1
        
    def maxInd(self):
        m = self.max_flow()
        
        s = []
        f = []
        
        for c in self.__vert_chords:
            flag = False
            for i in m:
                for j in i:
                    if j == c:
                        flag = True
            if flag == False:
                f.append(c)
        
        for c in self.__horiz_chords:
            flag = False
            for i in m:
                for j in i:
                    if j == c:
                        flag = True
            if flag == False:
                f.append(c)

        while f or m:
            if f:
                u = f.pop(0)
                s.append(u)
            else:
                e = m.pop(0)
                self.remove_edge(e)
                u = e[0]
                s.append(u)

            if u in self.__graph:
                size = len(self.__graph[u])
                for i in range(size):
                    v = self.__graph[u].pop(0)
                    self.remove_edge((u, v))
                    size -= 1
                    
                    if v in self.__reversed_graph:
                        for h in self.__reversed_graph[v]:
                            for j in range(len(m)):
                                if m[j] == (v, h):
                                    m.remove(j)
                                    f.append(h)
        return s
    