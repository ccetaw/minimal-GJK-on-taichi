import numpy as np
from utils import (
    nearest_point_on_line,
    is_in_convex_hull)

class Circle():

    def __init__(self, c, r) -> None:
        """
        Init the circle
        ----
        Input:
        - Circle center c: listlike
        - Radius r: float
        """
        self.center = np.array(c)
        self.radius = r

    def furthest_point(self, d):
        """
        Furthest point on the shape along direction d
        -----
        Input:
        - Direction d: numpy array
        Output:
        - Furthest point: numpy array
        """
        return self.center + self.radius * d

    def translate(self, v):
        self.center = self.center + v

class Polygon():

    def __init__(self, v) -> None:
        """
        Init the polygon by a list of vertices. The edges are connected 
        the same order as the list.
        ----
        Input:
        - A list of vertices

        """
        self.vertices = v
        self.center = np.zeros(2)
        for i in range(len(self.vertices)):
            self.center += self.vertices[i]
        self.center /= len(self.vertices)

    def furthest_point(self, d):
        """
        Furthest point on the shape along direction d
        -----
        Input:
        - Direction d: numpy array
        Output:
        - Furthest point: numpy array
        """
        imax = 0
        dmax = np.dot(self.vertices[0], d)
        for i in range(len(self.vertices)):
            pd = np.dot(self.vertices[i], d) # projected distance on d
            if pd > dmax:
                dmax = pd
                imax = i

        return self.vertices[imax]

    def translate(self, v):
        for i in range(len(self.vertices)):
            self.vertices[i] = self.vertices[i] + v
        for i in range(len(self.vertices)):
            self.center += self.vertices[i]
        self.center /= len(self.vertices)

    def rotate(self, angle):
        rot_mat = np.array([[np.sin(angle), -np.cos(angle)], [np.cos(angle), np.sin(angle)]])
        for i in range(len(self.vertices)):
            self.vertices[i] = self.center + rot_mat @ (self.vertices[i] - self.center)

    
                
class Simplex():

    def __init__(self, v) -> None:
        """
        Init the polygon by a list of vertices. The edges are connected 
        the same order as the list.
        ----
        Input:
        - A list of vertices

        """
        self.vertices = v
    
    def nearest_point(self):
        """
        Nearest point in the simplex to origin
        ----
        Output:
        - Nearest point: numpy array
        - edge vertices
        """
        ndist = np.inf
        npoint = np.array([0,0])
        iedge = [0, 0] # index of the edge

        if len(self.vertices) == 1:
            npoint = self.vertices[0]
            iedge = [0, 0]
        elif len(self.vertices) == 2:
            edge = [self.vertices[0], self.vertices[1]]
            npoint = nearest_point_on_line(np.array([0, 0]), edge)
            iedge = [0, 1]
        else:
            for i in range(len(self.vertices)):
                edge = [self.vertices[i], self.vertices[(i+1)%len(self.vertices)]]
                point = nearest_point_on_line(np.array([0, 0]), edge)
                if np.linalg.norm(point) < ndist:
                    ndist = np.linalg.norm(point)
                    npoint = point
                    iedge = [i, (i+1)%len(self.vertices)]
        
        return npoint, iedge
        
    def is_origin_inside(self):
        """
        Test if the origin is inside the simplex
        """
        if len(self.vertices) == 3:
            return is_in_convex_hull(np.array([0, 0]), self.vertices)
        else:
            return False

    def update(self, p, iedge):
        if len(self.vertices) == 1:
            self.vertices.append(p)
        elif np.array_equal(self.vertices[-1], p):
            self.vertices = [self.vertices[iedge[0]], self.vertices[iedge[1]]]
        else:
            self.vertices = [self.vertices[iedge[0]], self.vertices[iedge[1]]]
            self.vertices.append(p)