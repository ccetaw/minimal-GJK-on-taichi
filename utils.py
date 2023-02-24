import numpy as np

def nearest_point_on_line(p, l):
    """
    Given a point and a line, determine the nearest point on the line to the point
    ----
    Input:
    - point p: np array
    - line l: list of np array
    Output:
    - nearest point: np array
    """
    if np.dot(p - l[0], l[1]-l[0]) < 0:
        return l[0]
    elif np.dot(p-l[1], l[0]-l[1]) < 0:
        return l[1]
    elif np.array_equal(l[1], l[0]):
        return l[0]
    else:
        return l[0] + np.dot(p - l[0], l[1] - l[0]) * (l[1] - l[0]) / (np.linalg.norm(l[1] - l[0]) ** 2)
    

def is_in_convex_hull(p, vertices):
    """
    Given a point and a convex shape (simplex here), determine if the point is inside the convex hull
    https://inginious.org/course/competitive-programming/geometry-pointinconvex#:~:text=A%20convex%20polygon%20is%20a,of%20each%20of%20the%20segments.
    ----
    Input:
    - Point p: np array
    - Convex hull c: Simplex
    Output:
    - True / False
    """
    z = [0, 0]
    for i in range(len(vertices)):
        z[0] = z[1]
        AB = vertices[(i+1)%len(vertices)] - vertices[i]
        AP = p - vertices[i]
        z[1] = AB[0] * AP[1] - AB[1] * AP[0]
        if z[0] * z[1] < 0:
            return False
    return True