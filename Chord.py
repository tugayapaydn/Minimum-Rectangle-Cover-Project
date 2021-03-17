from Point import *

class Chord:
    def __init__(self, p: sPoint, q: sPoint):
        self._points = (p, q)
        
    def points(self):
        return self._points
        
    def __str__(self):
            return str(self._points[0].getCoord())+","+str(self.__vertices[1].getCoord())
    
    def __eq__(self,  v):
        return self._points == v

    def __ne__(self, v):
        return self._points != v

    def _onSegment(self, p: sPoint, q: sPoint, r: sPoint):
        p, q, r = p.getCoord(), q.getCoord(), r.getCoord()

        if (q[0] <= max(p[0], r[0])) and (q[0] >= min(p[0], r[0])) and (q[1] <= max(p[1], r[1])) and (q[1] >= min(p[1], r[1])):
            return True
        return False
    
    def _orientation(self, p: sPoint, q: sPoint, r: sPoint):
        p, q, r = p.getCoord(), q.getCoord(), r.getCoord()

        val = (float(q[1] - p[1]) * (r[0] - q[0])) - (float(q[0] - p[0]) * (r[1] - q[1]))

        if val > 0:
            return 1
        elif val < 0:
            return 2
        else:
            return 0

    def intersect(self, p1, q1, p2, q2):

        o1 = self._orientation(p1, q1, p2) 
        o2 = self._orientation(p1, q1, q2) 
        o3 = self._orientation(p2, q2, p1) 
        o4 = self._orientation(p2, q2, q1) 
    
        # General case 
        if ((o1 != o2) and (o3 != o4)): 
            return True
    
        # Special Cases 
    
        # p1 , q1 and p2 are colinear and p2 lies on segment p1q1 
        if ((o1 == 0) and self._onSegment(p1, p2, q1)): 
            return True
    
        # p1 , q1 and q2 are colinear and q2 lies on segment p1q1 
        if ((o2 == 0) and self._onSegment(p1, q2, q1)): 
            return True
    
        # p2 , q2 and p1 are colinear and p1 lies on segment p2q2 
        if ((o3 == 0) and self._onSegment(p2, p1, q2)): 
            return True
    
        # p2 , q2 and q1 are colinear and q1 lies on segment p2q2 
        if ((o4 == 0) and self._onSegment(p2, q1, q2)): 
            return True
    
        # If none of the cases 
        return False