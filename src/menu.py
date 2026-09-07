
# ! textboxen werden falsch übergeben (überlappen sich) 
#TODO auswahlmenü entfernen sobald man ausgewählt hat und einen zurück button hinzufügen 
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
        status['mode'] = 'singular'
        status['star_amount'] = 1
        build_menu(fig)

    def multiple_mode(event): 
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

    fig.canvas.draw_idle()
    return fig 

def build_singular(fig): 
    return fig  # TODO Missing functionalities = placeholder 

def build_multiple(fig): 
    amount = status['star_amount']

    first_row_y = 0.75 

    textbox = {} 

    for i in range(amount): 
        y = first_row_y - i * row_height
        fig.text(0.05, y + 0.02, f"Stern {i + 1}", fontsize = 12)

    # Params for stars (initial velocity, mass, position on x/y axis)   
    ax_mass = fig.add_axes([0.15, y, 0.15, 0.05])
    box_mass = TextBox(ax_mass, "", initial = "1.0e30kg") #1.0e30kg = 0.2-0.5 SM (solar masses)

    ax_x_positon = fig.add_axes([0.15, y, 0.15, 0.05])
    box_x_position = TextBox(ax_x_positon, "", initial = "0.0")

    ax_y_position = fig.add_axes([0.15, y, 0.15, 0.05])
    box_y_position = TextBox(ax_y_position, "", initial = "0.0")

    ax_x_velocity = fig.add_axes([0.15, y, 0.15, 0.05])
    box_x_velocity = TextBox(ax_x_velocity, "", initial = "0.0")

    ax_y_velocity = fig.add_axes([0.15, y, 0.15, 0.05])
    box_y_velocity = TextBox(ax_y_velocity, "", initial = "0.0")

    #ax_x_acceleration = fig.add_axes([0.15, y, 0.15, 0.05])
    #box_x_acceleration = TextBox(ax_x_acceleration, "ax",initial = "0,.0") 

    #ax_y_acceleration = fig.add_axes([0.15, y, 0.15, 0.05])
    #box_y_acceleration = TextBox(ax_y_acceleration, "ay", initial = "1.0e30kg")

    textbox[i] = {
        'Masse': box_mass,
        'Position X-Achse': box_x_position,
        'Position Y-Achse': box_y_position,
        'Initialgeschwindigkeit y': box_x_velocity,
        'Initialgeschwindigkeit x': box_y_velocity,
        #'Beschleunigung x': box_x_acceleration,
        #'Beschleunigung y': box_y_acceleration
    }

    status['references'] += list(textbox[i].values())

    #Row-Descriptors & Units
    fig.text(0.15, y + 0.02, "Masse in kg", fontsize = 10)
    fig.text(0.15, y + 0.02, "Position X-Achse [AE]", fontsize = 10)
    fig.text(0.15, y + 0.02, "Position Y-Achse [AE]", fontsize = 10)
    fig.text(0.15, y + 0.02, "Initialgeschwindigkeit x [m/s]", fontsize = 10)
    fig.text(0.15, y + 0.02, "Initialgeschwindigkeit y [m/s]", fontsize = 10)
    #fig.text(0.15, y + 0.02, "Beschleunigung x [m/s^2]", fontsize = 10)
    #fig.text(0.15, y + 0.02, "Beschleunigung y [m/s^2]", fontsize = 10)

    y_assignedToButton = y - amount * row_height

    # Button to add star
    if amount < max_amount_stars: 
        button_add_star = Button(fig.add_axes([0.15, y_assignedToButton - 0.02, 0.05, 0.05]), 'Stern hinzufügen')

        def add_star(event): 
            status['star_amount'] += 1
            build_menu(fig)

        button_add_star.on_clicked(add_star)
        status['references'] += [button_add_star]

    else : 
        fig.text(0.15, y_assignedToButton - 0.02, "Maximale Anzahl von Sternen erreicht", fontsize = 10)

    ax_start = fig.add_axes([0.4, 0.05, 0.02, 0.05])
    btn_start = Button(ax_start, 'Starten')

    def start(event): 
        params = []
        for i in range(amount):
            b = textbox[i]
            params.append({
                'Masse': b['Masse'].text,
                'Position X-Achse': b['Position X-Achse'].text,
                'Position Y-Achse': b['Position Y-Achse'].text,
                'Initialgeschwindigkeit y': b['Initialgeschwindigkeit y'].text,
                'Initialgeschwindigkeit x': b['Initialgeschwindigkeit x'].text,
                #'Beschleunigung x': b['Beschleunigung x'].text,
                #'Beschleunigung y': b['Beschleunigung y'].text
            })

        from simulation import simulate_multiple_stars #TODO ADD AMOUNT OF STARS AS PARAM TO SIMULATION FILE (make sure its codependent)
        from graphen_plotting import show_multiple_plot 

        data = simulate_multiple_stars(params)
        show_multiple_plot(fig, data)

    btn_start.on_clicked(start)
    status['references'] += [btn_start]

    fig.canvas.draw_idle()
    return fig
def main_menu(fig): 
    
    return build_menu(fig)