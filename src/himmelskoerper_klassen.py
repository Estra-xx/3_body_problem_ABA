import numpy as np

G = 6.6743e-11


class CelestialBody:
    def __init__(self, name, mass, r0, v0, color = 'gray'):
        self.name = name
        self.mass = mass
        self.r = np.array(r0, dtype = float)
        self.v = np.array(v0, dtype = float)
        self.color = color 

        self.r_history = None
        self.v_history = None

    def distance_to(self, other):
        #Euklidischer Abstand
        return np.linalg.norm(self.r - other.r)
    
    def apply_force(self, other):
        difference = other.r - self.r #Vektor pointing to other body
        distance = np.linalg.norm(difference)
        if distance == 0:
            return np.zeros(2)
        return G * self.mass * other.mass / distance**2 * (difference / distance)

    def acceleration(self, other): 
        #Beschleunigung m/s^2 - von anderen auf sich selbst 
        return self.apply_force(other) / self.mass

    def total_acceleration(self, all_bodies): 
        a = np.zeros(2)
        for other in all_bodies: 
            if other is self: 
                continue 
            a += self.acceleration(other)
        return a
    
    def __repr__(self): 
        return f"CelestialBody({self.name!r}, masse={self.mass:.2e})"