import numpy as np
import matplotlib.pyplot as plt
import math
from dataclasses import dataclass
import create_shapes

@dataclass
class circle:
    radius: float = 0
    center: float = 0
    points: float = 0

    points_span:  float = 0  #Number of points in the arc inside the circle
    advancement:  float = 0  #Advancement of the external conference w.r.t the inner one
    distance_ext: float = 0 #Distance of the center external conference. It's proportional to the radius of the external conf
    number_ext:   float = 0  #Number of external conferences, they will be uniformly distributed around 2pi

radius_main = 1
center_main = [0,0]
points_main = 200

distance_ext    = 1.2 *radius_main
points_ext      = 100
advancement_ext =  0.5 * (2*(distance_ext-radius_main))
points_span     = 50
number_ext      = 2

main_circle = circle(radius=radius_main,
                     center=center_main,
                     points=points_main)

external_circle = circle(points=points_ext,
                         distance_ext=distance_ext,
                         advancement=advancement_ext,
                         points_span=points_span,
                         number_ext=number_ext)


Create_shape = create_shapes.create_shapes(main_circle,external_circle)


Create_shape.plotting_circles("after")