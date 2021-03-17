
class sPoint:
    def __init__(self, x, y):
        self.__coord = (x, y)
        #self.__neighbour : Vertex = []
    
    #Return coordinates of the vertex
    def getCoord(self):
        return self.__coord
    
    #Returns coordinate and neighbours of the vertex
    def __str__(self):
        return str(self.__coord)

    def __eq__(self, c):
        return self.__coord == c

    def __ne__(self, c):
        return self.__coord != c
    
    def __hash__(self):
        return hash(self.__coord)
