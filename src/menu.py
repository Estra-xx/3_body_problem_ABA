#TODO hardcoded planets data' should be visible from the getgo in the menu but should still be editable by user - the data s 

from matplotlib.widgets import Button, TextBox
import matplotlib.pyplot as plt
import numpy as np

from simulation import HARDCODED_PLANETS, AE 
import param_config

#active status, shows selected mode (singular or multiple star system) and amount of stars & planets
status = {
    'mode': None, 
    'star_amount': 1,
    'planet_amount': 0,
    'references': [] #holds references to previous settings
}

min_amount_stars = 1
max_amount_stars = 7
max_amount_planets = 6
row_height = 0.05 

def build_menu(fig): 
    fig.clear()
    fig.suptitle("Simulationsmenü", fontsize = 20)
    status['references'] = [] #reset previous references

    if status['mode'] is None: 
        # mode: singular, multiple
        axes_button1 = fig.add_axes([0.15, 0.85, 0.3, 0.08])
        button_singular = Button(axes_button1, "Einfachsternsystem")

        axes_button2 = fig.add_axes([0.55, 0.85, 0.3, 0.08])
        button_multiple = Button(axes_button2, "Mehrfachsternsystem") 

        axes_button3 = fig.add_axes([0.35, 0.72, 0.3, 0.08])
        button_listing = Button(axes_button3, "Verlauf")

        def singular_mode(event): 
            fig.canvas.release_mouse(event.inaxes) #Mausgriff freigeben, sonst funktioniert fig.clear() nicht
            status['mode'] = 'singular'
            status['star_amount'] = 1
            status['planet_amount'] = 0
            build_menu(fig)

        def multiple_mode(event): 
            fig.canvas.release_mouse(event.inaxes)
            status['mode'] = 'multiple'
            status['star_amount'] = 2 
            build_menu(fig)

        def verlauf_mode(event):
            fig.canvas.release_mouse(event.inaxes)
            status['mode'] = 'listing'
            build_menu(fig)
            
        button_singular.on_clicked(singular_mode)
        button_multiple.on_clicked(multiple_mode)
        button_listing.on_clicked(verlauf_mode)
        status['references'] += [button_singular, button_multiple, button_listing]

    if status['mode'] == 'singular': 
        build_singular(fig)
    elif status['mode'] == 'multiple': 
        build_multiple(fig)
    elif status['mode'] == 'verlauf':
        build_verlauf(fig)

    def return_menu(event):
            fig.canvas.release_mouse(event.inaxes)
            status['mode'] = None
            status['star_amount'] = 1
            status['planet_amount'] = 0 
            build_menu(fig)

    
    if status['mode'] is not None:
        return_button = Button(fig.add_axes([0.35, 0.05, 0.2, 0.06]), 'Zurück')
        return_button.on_clicked(return_menu)
        status['references'] += [return_button]

    fig.canvas.draw_idle()
    return fig 

def build_celestial_body(fig, y, position_changable = True): 

    ax_mass = fig.add_axes([0.15, y, 0.12, 0.04])
    box_mass = TextBox(ax_mass, "", initial="1.0e30")
    fields = {'mass': box_mass}

    if position_changable:
            ax_x = fig.add_axes([0.29, y, 0.09, 0.04])
            box_x = TextBox(ax_x, "", initial="0.0")
            ax_y = fig.add_axes([0.40, y, 0.09, 0.04])
            box_y = TextBox(ax_y, "", initial="0.0")
            fields['position_x'] = box_x
            fields['position_y'] = box_y

    ax_vx = fig.add_axes([0.53, y, 0.09, 0.04])
    box_vx = TextBox(ax_vx, "", initial="0.0")
    ax_vy = fig.add_axes([0.64, y, 0.09, 0.04])
    box_vy = TextBox(ax_vy, "", initial="0.0")
    fields['velocity_x'] = box_vx
    fields['velocity_y'] = box_vy

    status['references'] += list(fields.values())
    return fields

def read_fields(fields):
    return {key: float(box.text) for key, box in fields.items()}
def row_headers(fig, y, position_changable = True):
    fig.text(0.15, y + 0.03, "Masse [kg]", fontsize = 10)
    if position_changable:
        fig.text(0.29, y + 0.03, "Position X-Achse [AE]", fontsize = 10)
        fig.text(0.40, y + 0.03, "Position Y-Achse [AE]", fontsize = 10)
    
    fig.text(0.53, y + 0.03, "Initialgeschwindigkeit x [m/s]", fontsize = 10)
    fig.text(0.64, y + 0.03, "Initialgeschwindigkeit y [m/s]", fontsize = 10)
    

def build_name(fig, y=0.16):
    fig.text(0.15, y + 0.045, "Simulationsname:", fontsize = 10)
    ax_name = fig.add_axes([0.15, y, 0.4, 0.04])
    box_name = TextBox(ax_name, "", initial=param_config.next_standardname())
    status['references'] += [box_name]
    return box_name

    
def build_singular(fig):
    star_row_y = 0.72
    row_headers(fig, star_row_y, position_changable=False)
    fig.text(0.02, star_row_y + 0.01, "Stern", fontsize = 10) #position fix bei 0/0 bei einzelsternsystem
    star_fields = build_celestial_body(fig, star_row_y, position_changable=False)

    #mind. 4 Planeten - Referenz: unser Sonnensystem
    standard_header_y = star_row_y - row_height - 0.03
    fig.text(0.02, standard_header_y + 0.03, "Planet: min. 4 Planeten\n nicht änderbar", fontsize = 10, style = 'italic') #position fix bei 0/0 bei einzelsternsystem

    for i, p in enumerate(HARDCODED_PLANETS):
        y = standard_header_y - i * 0.035
        x_ae = p['r0'][0] / AE
        y_ae = p['r0'][1] / AE
        fig.text(0.002, y, 
                 f"{p['name']}: Masse={p['mass']:.2e} kg, "
                 f"x={x_ae:.2f} AE, y={y_ae:.2f} AE, "
                 f"vx={p['v0'][0]:.2f} m/s, vy={p['v0'][1]:.2f} m/s",
                 fontsize = 10, style = 'italic', color='gray')
        
    planet_header_y = standard_header_y - len(HARDCODED_PLANETS) * 0.035 - 0.03
    fig.text(0.02, planet_header_y + 0.03, "Zusätzliche Planeten hinzufügen:", fontsize = 10, style = 'italic') #position fix bei 0/0 bei einzelsternsystem

    planet_row_y = planet_header_y - 0.02
    if status['planet_amount'] > 0:
        row_headers(fig, planet_row_y, position_changable=True)

    planet_fields = {}
    for i in range(status['planet_amount']):
        y = planet_row_y - (i + 1) * row_height
        fig.text(0.02, y + 0.01, f"Planet {i + 1}", fontsize = 10)
        planet_fields[i] = build_celestial_body(fig, y, position_changable=True)

    y_planets = planet_row_y - (status['planet_amount'] + 1) * row_height

    if status['planet_amount'] < max_amount_planets:
        button_add_planet = Button(
            fig.add_axes([0.15, y_planets - 0.02, 0.2, 0.05]),
            "Planet hinzufügen"
        )

        def add_planet(event):
            fig.canvas.release_mouse(event.inaxes) #Mausgriff freigeben, sonst funktioniert fig.clear() nicht
            status['planet_amount'] += 1
            build_menu(fig)

        button_add_planet.on_clicked(add_planet)
        status['references'] += [button_add_planet]
        y_name = y_planets - 0.09
    else:
        fig.text(0.15, y_planets - 0.01, "Maximale Anzahl an Planeten erreicht", fontsize = 10) 
        y_name = y_planets - 0.09

    name_field = build_name(fig, y_name)

    ax_start = fig.add_axes([0.55, 0.05, 0.2, 0.06])
    button_start = Button(ax_start, "Starten")

    def start(event): 
        fig.canvas.release_mouse(event.inaxes) #Mausgriff freigeben, sonst funktioniert fig.clear() nicht

        star_params = read_fields(star_fields)
        planet_params = [read_fields(planet_fields[i]) for i in range(status['planet_amount'])]
        simulation_name = name_field.text.strip() or param_config.next_standardname()

        from simulation import simulate_single_star
        from graphen_plotting import show_simulation_plot

        param_config.save_simulation(simulation_name, 'singular', star_params, planet_params)
        
        data = simulate_single_star(star_params, planet_params, simulation_name)
        show_simulation_plot(data)

    button_start.on_clicked(start)
    status['references'] += [button_start]

    fig.canvas.draw_idle()
    return fig
   
def build_multiple(fig): 
    amount = status['star_amount']
    star_row_y = 0.72
    row_headers(fig, star_row_y, position_changable=True)

    star_fields = {}
    for i in range(amount):
        y = star_row_y - i * row_height
        fig.text(0.02, y + 0.01, f"Stern {i + 1}", fontsize = 10)
        star_fields[i] = build_celestial_body(fig, y, position_changable=True)

    y_star = star_row_y - amount * row_height

    #Button Add Star
    if amount < max_amount_stars:
        button_add_star = Button(
            fig.add_axes([0.15, y_star - 0.03, 0.2, 0.05]),
            'Stern hinzufügen'
        )

        def add_star(event): 
            fig.canvas.release_mouse(event.inaxes)
            status['star_amount'] += 1
            build_menu(fig)

        button_add_star.on_clicked(add_star)
        status['references'] += [button_add_star]
        y_name = y_star - 0.11

    else : 
        fig.text(0.15, y_star - 0.02, "Maximale Anzahl an Sternen erreicht", fontsize = 10)
        y_name = y_star - 0.09

    name_field = build_name(fig, y_name)

    ax_start = fig.add_axes([0.55, 0.05, 0.2, 0.06])
    button_start = Button(ax_start, 'Starten')

    def start(event): 
        fig.canvas.release_mouse(event.inaxes) 
        star_params = [read_fields(star_fields[i]) for i in range(amount)]
        simulation_name = name_field.text.strip() or param_config.next_standardname()

        positions = [(p['position_x'], p['position_y']) for p in star_params]
        if len (set(positions)) < len(positions):
            print("Startwerte von den Sternen sollen unterschiedlich sein - sonst läuft Epot gegen die Unendlichkeit.")
            return

        from simulation import simulate_multiple_stars
        from graphen_plotting import show_simulation_plot

        param_config.save_simulation(simulation_name, 'multiple', star_params)

        try: 
            data = simulate_multiple_stars(star_params, simulation_name)
        except RuntimeError as e: 
            print("Simulation konnte nicht gestartet werden - kollabiert sofort. Sterne brauchen Startgeschwindigkeiten.")
            return
        
        show_simulation_plot(data)

    button_start.on_clicked(start)
    status['references'] += [button_start]
    fig.canvas.draw_idle()
    return fig

def replay_simulation(fig, listing): 
    from simulation import simulate_single_star, simulate_multiple_stars
    from graphen_plotting import show_simulation_plot

    if listing['mode'] == 'singular': 
        data = simulate_single_star(listing['star_params'][0], listing['planet_params'], listing['name'])
    else: 
        data = simulate_multiple_stars(listing['star_params'], listing['name'])

    show_simulation_plot(data)

def build_verlauf(fig):
    fig.text(0.02, 0.8, "Gespeicherte Simulationen:", fontsize = 10, style = 'italic')
    listings = param_config.load_simulation()
    if not listing: 
        fig.text(0.15, 0.7, "Keine gespeicherten Simulationen gefunden.", fontsize = 10, style = 'italic')
        fig.canvas.draw_idle()
        return fig

    row_y = 0.7

    #show newest on top 
    for listing in listings: 
        fig.text(0.02, row_y + 0.01, f"{listing['name']}, {listing['mode']}, {listing['timestamp']}", fontsize = 10)

        ax_show = fig.add_axes([0.60, row_y, 0.12, 0.04])
        button_show = Button(ax_show, 'Anzeigen')

        ax_delete = fig.add_axes([0.75, row_y, 0.12, 0.04])
        button_delete = Button(ax_delete, 'Löschen')

        def show(event, listing=listing):
            fig.canvas.release_mouse(event.inaxes)
            replay_simulation(fig, listing)

        def delete(event, listing=listing):
            fig.canvas.release_mouse(event.inaxes)
            param_config.delete_simulation(listing['name'])
            build_menu(fig)

        button_show.on_clicked(show)
        button_delete.on_clicked(delete)
        status['references'] += [button_show, button_delete]

        row_y -= row_height
        if row_y < 0.1: 
            break

    fig.canvas.draw_idle()
    return fig

def main_menu(fig): 
    return build_menu(fig)