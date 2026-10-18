import math as m

class Es_param_find():
    R=6371 #km
    GM= 3.986005*10**14 #m3/s2
    M= 5.9742*10**24 #kg
    
    def __init__(self,alt):
        if isinstance(alt,(int,float))and m.isfinite(alt)  and not isinstance(alt,bool):
                if alt>0:
                        self.h=alt
                        self.orbit_rad= Es_param_find.R+self.h
                        self.velocity=(Es_param_find.GM*10**-9/self.orbit_rad)**0.5#km/s
                        self.orbit_period=(2*m.pi*((self.orbit_rad*10**3)**3/Es_param_find.GM)**0.5)#seconds
                        self.a_velocity=(m.pi*2)/self.orbit_period
                        self.now_t=0
                        self.elaps_t=0
                        self.a_pos=0
                        self.coor_pos=(self.orbit_rad,0)
                                                
                else :
                    raise ValueError("Invlaid Altitude")
        else :
            raise ValueError("Invalid Altitude")
    
    def simulate(self,t):
        if isinstance(t,(int,float))and m.isfinite(t)  and not isinstance(t,bool):
                if t>=0:
                        self.now_t=t
                        self.elaps_t=self.now_t%self.orbit_period
                        self.a_pos=self.a_velocity*self.elaps_t
                        self.coor_pos=(self.orbit_rad*m.cos(self.a_pos),self.orbit_rad*m.sin(self.a_pos))
                        return self.coor_pos
                                                
                else :
                    raise ValueError("Invlaid Time")
        else :
            raise ValueError("Invalid Time")
        

sat = Es_param_find(400)
print(sat.simulate(0))
print(sat.simulate(sat.orbit_period / 4))
x, y = sat.simulate(100)
print(m.hypot(x, y))
