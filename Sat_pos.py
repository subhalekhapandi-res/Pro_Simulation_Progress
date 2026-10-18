import Orbit_math as om
import math 
r,v,T=om.Satellite_param(400)
T=T*60#seconds
def angular_velocity(t):
    return (math.pi*2)/T 

def angular_position(t):
    elaps_t=t%T
    return angular_velocity(t)*elaps_t

def coor_pos(t):
    a=angular_position(t)
    return (r*math.cos(a),r*math.sin(a))
