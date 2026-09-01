import math
from config import DECK_HALF_WIDTH_M,HANGER_LOWER_OFFSET_M
def area(d): return math.pi*d*d/4.
def perimeter(d,f=1.): return f*math.pi*d
def section_factor(d,f=1.):
    """A_m/V selon NF EN 1993-1-2 §4.2.5.1; pour un cercle: η_exp·4/D."""
    return perimeter(d,f)/area(d)
def intrados_rise(y):
    """Approximation en deux segments: (0;0), (1,91;0,19), (3,70;0,61)."""
    y=abs(y)
    if y>3.70: raise ValueError('Point hors tablier')
    return .19*y/1.91 if y<=1.91 else .19+(.61-.19)*(y-1.91)/(3.70-1.91)
def nearest_section(position,sections): return min(sections,key=lambda s:abs(s.x_m-position.x_m))
def receiver_xyz(section,element_name):
    z=section.intrados_m+HANGER_LOWER_OFFSET_M if 'Suspente' in element_name else section.cable_m
    return (section.x_m,DECK_HALF_WIDTH_M,z)
def distance3d(a,b): return math.sqrt(sum((x-y)**2 for x,y in zip(a,b)))
