import math
from config import DECK_HALF_WIDTH_M,HANGER_LOWER_OFFSET_M
def area(d):return math.pi*d*d/4
def section_factor(d):return 4./d
def nearest_section(p,S):return min(S,key=lambda s:abs(s.x_m-p.x_m))
def receiver_xyz(s,n):return (s.x_m,DECK_HALF_WIDTH_M,s.intrados_m+HANGER_LOWER_OFFSET_M if 'secondaire' in n else s.cable_m)
def distance3d(a,b):return math.sqrt(sum((x-y)**2 for x,y in zip(a,b)))
