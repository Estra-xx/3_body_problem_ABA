#params for stars (velocity, mass, position)

import json
import os
from datetime import datetime

SAVE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "simulations.json")

def load_all(): 
    if not os.path.exists(SAVE_FILE):
        return []
    with open(SAVE_FILE, "r", encoding="utf-8") as f:
        try: 
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_all(listings): 
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(listings, f, indent=2, ensure_ascii=False)

def next_standardname():
    listings = load_all()
    return f"Simulation_{len(listings) + 1}"

def save_simulation(name, mode, star_params, planet_params = None):
    
    listings = load_all()

    listings.append({
        'name': name or next_standardname(),
        'timestamp': datetime.now().isoformat(timespec = 'seconds'),
        'modus': mode,
        'star_params': star_params,
        'planet_params': planet_params or []
    })

    save_all(listings)

def load_simulation():
    return load_all()

def find_simulation(name):
    for listing in load_all():
        if listing['name'] == name:
            return listing
    return None

def delete_simulation(name):
    listings = load_all()
    listings = [listing for listing in listings if listing['name'] != name]
    save_all(listings)