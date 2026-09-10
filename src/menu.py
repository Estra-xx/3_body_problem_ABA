
#TODO auswahlmöglichkeit zwischen einfach und mehrfachsternsystem entfernen wenn man im system drinnen is 
from matplotlib.widgets import Button, TextBox
import matplotlib.pyplot as plt
import numpy as np

#active status, shows selected mode (singular or multiple star system)
status = {
    'mode': None, 
    'star_amount': 1,
    'references': [] #holds references to previous settings
}

min_amount_stars = 1
max_amount_stars = 7
row_height = 0.05 


def build_menu(fig): 
    fig.clear()
    fig.suptitle("Simulationsmenü", fontsize = 20)
    status['references'] = [] #reset previous references

    # mode: singular, multiple
    axes_button1 = fig.add_axes([0.15, 0.85, 0.3, 0.08])
    button_singular = Button(axes_button1, "Einfachsternsystem")

    axes_button2 = fig.add_axes([0.55, 0.85, 0.3, 0.08])
    button_multiple = Button(axes_button2, "Mehrfachsternsystem")#

    def singular_mode(event): 
        fig.canvas.release_mouse(event.inaxes) #Mausgriff freigeben, sonst funktioniert fig.clear() nicht
        status['mode'] = 'singular'
        status['star_amount'] = 1
        build_menu(fig)

    def multiple_mode(event): 
        fig.canvas.release_mouse(event.inaxes)
        status['mode'] = 'multiple'
        status['star_amount'] = 2 
        build_menu(fig)

    button_singular.on_clicked(singular_mode)
    button_multiple.on_clicked(multiple_mode)
    status['references'] += [button_singular, button_multiple]

    if status['mode'] == 'singular': 
        build_singular(fig)
    elif status['mode'] == 'multiple': 
        build_multiple(fig)

    def return_menu(event):
            fig.canvas.release_mouse(event.inaxes)
            status['mode'] = None
            status['star_amount'] = 1
            build_menu(fig)

    #return button
    return_button = Button(fig.add_axes([0.35, 0.05, 0.2, 0.06]), 'Zurück')
    return_button.on_clicked(return_menu)

    status['references'] += [return_button]
    fig.canvas.draw_idle()
    return fig 


def build_star(fig, amount): 
    star_row_y = 0.75
    textbox = {}

    fig.text(0.15, star_row_y + 0.06, "Masse [kg]", fontsize = 10)
    fig.text(0.32, star_row_y + 0.06, "Position X-Achse [AE]", fontsize = 10)
    fig.text(0.44, star_row_y + 0.06, "Position Y-Achse [AE]", fontsize = 10)
    fig.text(0.56, star_row_y + 0.06, "Initialgeschwindigkeit x [m/s]", fontsize = 10)
    fig.text(0.68, star_row_y + 0.06, "Initialgeschwindigkeit y [m/s]", fontsize = 10)

    for i in range(amount): 
        y = star_row_y - i * row_height
        fig.text(0.02, y + 0.02, f"Stern {i +1}", fontsize = 10)

        # Params for stars (initial velocity, mass, position on x/y axis)   
        ax_mass = fig.add_axes([0.15, y, 0.15, 0.05])
        box_mass = TextBox(ax_mass, "", initial = "1.0e30") #1.0e30kg = 0.2-0.5 SM (solar masses)
    
        ax_x_positon = fig.add_axes([0.32, y , 0.10, 0.05])
        box_x_position = TextBox(ax_x_positon, "", initial = "0.0")
    
        ax_y_position = fig.add_axes([0.44, y, 0.10, 0.05])
        box_y_position = TextBox(ax_y_position, "", initial = "0.0")
    
        ax_x_velocity = fig.add_axes([0.56, y, 0.10, 0.05])
        box_x_velocity = TextBox(ax_x_velocity, "", initial = "0.0")
    
        ax_y_velocity = fig.add_axes([0.68, y, 0.10, 0.05])
        box_y_velocity = TextBox(ax_y_velocity, "", initial = "0.0")
    
        textbox[i] = {
            'Masse': box_mass,
            'Position X-Achse': box_x_position,
            'Position Y-Achse': box_y_position,
            'Initialgeschwindigkeit x': box_x_velocity,
            'Initialgeschwindigkeit y': box_y_velocity,
        }

        status['references'] += list(textbox[i].values())

    return textbox, star_row_y
def build_singular(fig): 
    amount = status['star_amount']
    textbox, star_row_y = build_star(fig, amount)

    ax_start = fig.add_axes([0.55, 0.05, 0.2, 0.06])
    button_start = Button(ax_start, "Starten")

    def start(event): 
        fig.canvas.release_mouse(event.inaxes) #Mausgriff freigeben, sonst funktioniert fig.clear() nicht
        params = []
        for i in range(amount):
            b = textbox[i]
            params.append({
                #Data being submitted as a float to simulation to avoid type errors
                'Masse': float(b['Masse'].text),
                'Position X-Achse': b['Position X-Achse'].text,
                'Position Y-Achse': b['Position Y-Achse'].text,
                'Initialgeschwindigkeit y': b['Initialgeschwindigkeit y'].text,
                'Initialgeschwindigkeit x': b['Initialgeschwindigkeit x'].text,
            })

        from simulation import simulate_single_star #TODO ADD AMOUNT OF STARS AS PARAM TO SIMULATION FILE (make sure its codependent)
        from graphen_plotting import show_single_plot 

        data = simulate_single_star(params)
        show_single_plot(fig, data)

    button_start.on_clicked(start)
    status['references'] += [button_start]

    fig.canvas.draw_idle()
    return fig 
def build_multiple(fig): 
    amount = status['star_amount']
    textbox, star_row_y = build_star(fig, amount)

    y_assignedToButton = star_row_y - amount * row_height

    #Button Add Star
    if amount < max_amount_stars:
        button_add_star = Button(
            fig.add_axes([0.15, y_assignedToButton - 0.3, 0.15, 0.05]),
            'Stern hinzufügen'
        )

        def add_star(event): 
            fig.canvas.release_mouse(event.inaxes)
            status['star_amount'] += 1
            build_menu(fig)

        button_add_star.on_clicked(add_star)
        status['references'] += [button_add_star]

    else : 
        fig.text(0.15, y_assignedToButton - 0.02, "Maximale Anzahl an Sternen erreicht", fontsize = 10)

    ax_start = fig.add_axes([0.55, 0.05, 0.2, 0.06])
    button_start = Button(ax_start, 'Starten')

    def start(event): 
        fig.canvas.release_mouse(event.inaxes) 
        params = []
        for i in range(amount):
            b = textbox[i]
            params.append({
                'Masse': b['Masse'].text,
                'Position X-Achse': b['Position X-Achse'].text,
                'Position Y-Achse': b['Position Y-Achse'].text,
                'Initialgeschwindigkeit y': b['Initialgeschwindigkeit y'].text,
                'Initialgeschwindigkeit x': b['Initialgeschwindigkeit x'].text,
            })

        from simulation import simulate_multiple_stars #TODO ADD AMOUNT OF STARS AS PARAM TO SIMULATION FILE (make sure its codependent)
        from graphen_plotting import show_multiple_plot 

        data = simulate_multiple_stars(params)
        show_multiple_plot(fig, data)

    button_start.on_clicked(start)
    status['references'] += [button_start]

    fig.canvas.draw_idle()
    return fig
def main_menu(fig): 
    return build_menu(fig)