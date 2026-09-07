import math 

class CelestialBody:
    def __init__(self, name, mass, x, y, vx, vy, radius, color):
        self.name = name
        self.mass = mass
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.radius = radius
        self.color = color

    def distance_to(self, other):
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)
    
    def apply_force(self, other, dt, G=6.67e-11):
        d = self.distance_to(other)
        if d == 0:
            return
        
        f = G * self.mass * other.mass / (d**2)
        fx = f * (other.x - self.x) / d
        fy = f * (other.y - self.y) / d
        
        self.vx += fx / self.mass * dt
        self.vy += fy / self.mass * dt
    
    def update_position(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt
