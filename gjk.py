import numpy as np

def gjk(a, b, simplex):
    """
    GJK algorithm.
    Input:
    - Shape a, b
    Output
    - Weather a and b collide
    """
    # Inintialize the simplex
    d = np.array([1, 0]) # Support
    iter = 0
    
    
    while True:
        npoint, iedge = simplex.nearest_point()
        d = np.array(-npoint) / np.linalg.norm(-npoint)
        
        minkow_point = a.furthest_point(d) - b.furthest_point(-d)
        
        # Return false if the line connecting the two points don't pass by the origin
        if minkow_point[0] * npoint[0] > 0 and minkow_point[1] * npoint[1] > 0:
            return False

        simplex.update(minkow_point, iedge)
        if simplex.is_origin_inside():
            # print(simplex.vertices)
            return True
        elif iter > 10:
            # print(simplex.vertices)
            return False
        iter += 1


