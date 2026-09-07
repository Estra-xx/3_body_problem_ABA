import math
from matplotlib.animation import FuncAnimation

import matplotlib.pyplot as plt

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

# Create celestial bodies (binary star system + planets)
G = 6.67430e-11
# Binary star parameters
m1 = 1.989e30
m2 = 1.989e30
separation = 1.0e11  # meters between the two suns
# distances from center of mass
r1 = separation * m2 / (m1 + m2)
r2 = separation * m1 / (m1 + m2)
# angular velocity for circular orbit
omega = math.sqrt(G * (m1 + m2) / separation**3)
v1 = omega * r1
v2 = omega * r2

sun1 = CelestialBody("Sun A", m1, -r1, 0, 0, v1, 20, "yellow")
sun2 = CelestialBody("Sun B", m2, r2, 0, 0, -v2, 20, "orange")

planet1 = CelestialBody("Planet 1", 5.972e24, 150e9, 0, 0, 30000, 10, "blue")
planet2 = CelestialBody("Planet 2", 6.417e23, -230e9, 0, 0, -24000, 8, "red")

bodies = [sun1, sun2, planet1, planet2]

# Simulation
fig, ax = plt.subplots(figsize=(10, 10))
ax.set_xlim(-3e11, 3e11)
ax.set_ylim(-3e11, 3e11)
ax.set_aspect("equal")

def animate(frame):
    dt = 86400 * 10  # 10 days
    
    for body in bodies:
        for other in bodies:
            if body != other:
                body.apply_force(other, dt)
    
    for body in bodies:
        body.update_position(dt)
    
    ax.clear()
    ax.set_xlim(-3e11, 3e11)
    ax.set_ylim(-3e11, 3e11)
    ax.set_aspect("equal")
    
    for body in bodies:
        ax.plot(body.x, body.y, "o", color=body.color, markersize=body.radius/5, label=body.name)
    
    ax.legend()
    ax.set_title(f"Star System Simulation - Day {frame * 10}")
    ax.grid()

anim = FuncAnimation(fig, animate, frames=500, interval=50, repeat=True)
plt.show()