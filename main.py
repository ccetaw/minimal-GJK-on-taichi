import numpy as np
import taichi as ti
from shapes import Circle, Polygon, Simplex
from gjk import gjk

res = 800
COLLISION = 0xFF0000
SIMPLEX = 0x00FFFF
NO_COLLISION = 0xFFFFFF

square = Polygon([np.array([-0.5, -0.5]),
                  np.array([-0.5, 0.2]),
                  np.array([0.2, 0.2]),
                  np.array([0.2, -0.5])])

circle = Circle(np.array([0.24, 0.24]), 0.4)

def draw_polygon(gui, vertices, c=0xFFFFFF):
    begin = (np.array(vertices) + 1.0) / 2.0
    indices = np.arange(1, len(begin)+1)
    indices[len(begin)-1] = 0
    end = begin[indices]
    gui.lines(begin = begin, end = end, radius = 0.001*res, color=c)

def draw_circle(gui, center, radius, c=0xFFFFFF):
    ticks = np.arange(1000) * 2.0 * np.pi / 1000
    x = radius * np.cos(ticks)
    y = radius * np.sin(ticks)
    begin = (np.array([x, y]).transpose() + center + 1.0) / 2.0
    indices = np.arange(1, len(begin)+1)
    indices[len(begin)-1] = 0
    end = begin[indices]
    gui.lines(begin = begin, end = end, radius = 0.001*res, color=c)

def draw_arrow(gui, d, c=0xFFFFFF):
    gui.arrow([0.5, 0.5], d, radius = 0.001*res, color=c)

def draw_point(gui, p, c=0xFFFFFF):
    gui.circle(pos= (p + 1)/2, radius=0.003*res, color=c)


gui = ti.GUI("GJK demo", res=(res,res))
iterations = 0

for iterations in range(100):
    # Move the shapes
    square.rotate(1/100)
    circle.translate(np.array([np.sin(iterations/10) * 0.01, np.sin(iterations/10) * 0.01]))

    # Inintialize the simplex
    d = np.array([1, 0]) # Support
    simplex = Simplex([square.furthest_point(d) - circle.furthest_point(-d)])
    
    # Draw shapes
    if gjk(square, circle, simplex):
        draw_polygon(gui, square.vertices, COLLISION)
        draw_circle(gui, circle.center, circle.radius, COLLISION)
    else:
        draw_polygon(gui, square.vertices, NO_COLLISION)
        draw_circle(gui, circle.center, circle.radius, NO_COLLISION)

    # Draw origin
    draw_point(gui, np.array([0, 0]), 0xFF00FF)

    # Draw simplex
    draw_polygon(gui, simplex.vertices, SIMPLEX)

    # Output files
    iterations += 1
    filename = f'frame_{iterations:05d}.png'
    gui.show("./output/"+filename)