import math
from config import DECK_HALF_WIDTH_M,HANGER_LOWER_OFFSET_M
def area(d):return math.pi*d*d/4
def perimeter(d):return math.pi*d
def section_factor(d):return perimeter(d)/area(d)
def nearest_section(p,sections):return min(sections,key=lambda s:abs(s.x_m-p.x_m))
def receiver_xyz(s,name):return (s.x_m,DECK_HALF_WIDTH_M,s.intrados_m+HANGER_LOWER_OFFSET_M if 'Suspente' in name else s.cable_m)
def distance3d(a,b):return math.sqrt(sum((x-y)**2 for x,y in zip(a,b)))
