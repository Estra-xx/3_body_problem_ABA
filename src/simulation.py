import numpy as np
from scipy.integrate import solve_ivp

from himmelskoerper_klassen import CelestialBody, G

#constants
AE = 1.495978707e11

#hardcoded planets
HARDCODED_PLANETS = [
    {'name': 'Merkur', 'mass': 3.3e23,  'r0': AE * np.array([0.39, 0.0]), 'v0': np.array([0.0, 47.9e3]), 'color': 'gray'},
    {'name': 'Venus',  'mass': 4.9e24,  'r0': AE * np.array([0.72, 0.0]), 'v0': np.array([0.0, 35.0e3]), 'color': 'orange'},
    {'name': 'Erde',   'mass': 5.97e24, 'r0': AE * np.array([1.00, 0.0]), 'v0': np.array([0.0, 29.8e3]), 'color': 'blue'},
    {'name': 'Mars',   'mass': 6.4e23,  'r0': AE * np.array([1.52, 0.0]), 'v0': np.array([0.0, 24.1e3]), 'color': 'red'},
]

def build_default_planets(): 
    return [
        CelestialBody(p['name'], p['mass'], p['r0'], p['v0'], p['color']) 
        for p in HARDCODED_PLANETS
    ]
def differential_equation(t, u, bodies, masses):
    #rechte seite von der dgl
    #u steht für alle posotionen (x, y, je körper)
    #v für alle geschwindigkeiten (vx, vy, je körper)
    n = len(bodies)
    positions = u[:2 * n].reshape(n, 2)
    velocities = u[2 * n:].reshape(n, 2)

    #aktuelle position von körper beschreiben, für total acceleration benötigt
    for body, r in zip(bodies, positions):
        body.r = r 

    accelerations = np.array([body.total_acceleration(bodies) for body in bodies])

    return np.concatenate([velocities.flatten(), accelerations.flatten()])


def start_nbody_simulation(bodies, t_end= 60* 60 * 24 * 365 * 25, steps= 10000, simulation_name = None):
    n = len(bodies)
    masses = np.array([b.mass for b in bodies])

    r0 = np.array([b.r for b in bodies]).flatten()
    v0 = np.array([b.v for b in bodies]).flatten()
    u0 = np.concatenate([r0, v0])

    t_eval = np.linspace(0, t_end, steps)

    #DOP853 statt RK45 - besser für größere SI einheiten, standard-fehlertoleranz für RK45
    result = solve_ivp(
        differential_equation, (0, t_end), u0, 
        t_eval = t_eval, args = (bodies, masses),
        method='DOP853', rtol=1e-9, atol=1e-6
    )

    if not result.success: 
        raise RuntimeError(f"Integration fehlgeschlagen: {result.message}")

    t = result.t
    u = result.y

    positions = u[:2 * n].reshape(n, 2, -1)
    velocities = u[2 * n:].reshape(n, 2, -1)

    #Verlauf für Körper (je Zeiteinheit) 
    for i, body in enumerate(bodies): 
        body.r_history = positions[i].T
        body.v_history = velocities[i].T

        body.r = body.r_history[-1]
        body.v = body.v_history[-1]

    return {'t': t, 'bodies': bodies, 'masses': masses, 'name': simulation_name}

def build_star(params, name= 'Stern', color= 'gold'):
    r0 = (params.get('position_x', 0.0) * AE, params.get('position_y', 0.0) * AE)
    v0 = (params['velocity_x'], params['velocity_y'])
    return CelestialBody(name, params['mass'], r0, v0, color)


def simulate_single_star(star_params, planet_params, simulation_name = None):
    star = CelestialBody('Stern', star_params['mass'], (0.0, 0.0),
        (star_params['velocity_x'], star_params['velocity_y']), 'gold')

    planets = build_default_planets()
    for i, p in enumerate(planet_params): 
        planets.append(build_star(p, name= f'Planet {len(HARDCODED_PLANETS) + i + 1}', color= 'blue'))

    bodies = [star] + planets
    return start_nbody_simulation(bodies, simulation_name= simulation_name)

def simulate_multiple_stars(star_param_list, simulation_name= None):
    stars = [
        build_star(p, name= f'Stern {i + 1}', color= 'gold')
        for i, p in enumerate(star_param_list)
    ]

    return start_nbody_simulation(stars, simulation_name= simulation_name)
