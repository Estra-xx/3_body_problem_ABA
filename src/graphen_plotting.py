from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl

from himmelskoerper_klassen import G 

#references of all active animations, making it able to continue running in the background
active_animations = []

def show_simulation_plot(data): #receives data from all simulations - aufgeteilt in zwei: Hauptsimulation, Graphen mit ausgewerteten Daten
    bodies = data['bodies']
    masses = data['masses']
    t = data['t']
    name = data.get('name')

    n = len(bodies)
    n_steps = len(t)
    title = f"Simulation: {name}" if name else "Simulation"

    #Fenster 1 
    fig_orbit = plt.figure(figsize=(12, 8))
    fig_orbit.suptitle(title, fontsize=16)
    ax_orbit = fig_orbit.add_subplot(1, 1, 1)

     # Bahnkurven Achse
    ax_orbit.set_title('Bahnkurven', fontsize=12)
    ax_orbit.set_xlabel('x [m]', fontsize=12)
    ax_orbit.set_ylabel('y [m]', fontsize=12)
    ax_orbit.set_aspect('equal')

    all_positions = np.concatenate([body.r_history for body in bodies], axis=0)
    margin = 0.1 * (all_positions.max() - all_positions.min() + 1)
    ax_orbit.set_xlim(all_positions[:, 0].min() - margin, all_positions[:, 0].max() + margin)
    ax_orbit.set_ylim(all_positions[:, 1].min() - margin, all_positions[:, 1].max() + margin)

    trail_lines = []
    points = []
    accel_arrows = []
    for b in bodies: 
        trail, = ax_orbit.plot([], [], '-', color = b.color, linewidth = 1.5, alpha = 0.7)
        point, = ax_orbit.plot([], [], 'o', color = b.color, markersize = 9, label = b.name)
        arrow = ax_orbit.annotate('', xy=(0, 0), xytext=(0, 0), 
                                  arrowprops=dict(arrowstyle='->', color=b.color, lw=2), fontsize=12)
        trail_lines.append(trail)
        points.append(point)
        accel_arrows.append(arrow)
    ax_orbit.legend(loc='upper left', fontsize=8)

    #Fenster 2 
    fig_graphs = plt.figure(figsize=(12, 8))
    fig_graphs.suptitle(f"{title} - Erhaltungsgrößen", fontsize=16)
    gs = fig_graphs.add_gridspec(2, 2)

    ax_energy = fig_graphs.add_subplot(gs[0, 0])
    ax_angular = fig_graphs.add_subplot(gs[0, 1])
    ax_com = fig_graphs.add_subplot(gs[1, 0])
    ax_momentum = fig_graphs.add_subplot(gs[1, 1])

    #Energie 
    ax_energy.set_title("Gesamtenergie", fontsize=12)
    ax_energy.set_xlabel("t [s]", fontsize=12)
    ax_energy.set_ylabel("E [J]", fontsize=12)

    E_kin = np.zeros_like(t)
    E_pot = np.zeros_like(t)

    for i, b in enumerate(bodies):
        E_kin += 0.5 * masses[i] * np.sum(b.v_history**2, axis=1)
    for i in range(n): 
        for j in range(i + 1, n): 
            dist = np.linalg.norm(bodies[j].r_history - bodies[i].r_history, axis = 1)
            E_pot -= G * masses[i] * masses[j] / dist
    E_total = E_kin + E_pot

    ax_energy.plot(t, E_total, '-b')
    line_t_energy, = ax_energy.plot([], [], '-k')

    # Drehimpuls
    ax_angular.set_title('Drehimpuls (z-Komponente)', fontsize=12)
    ax_angular.set_xlabel('t [s]', fontsize=12)
    ax_angular.set_ylabel('L [kg m^2/s]', fontsize=12)

    L = np.zeros_like(t)
    for i, b in enumerate(bodies): 
        r = b.r_history
        v = b.v_history
        L += masses[i] * (r[:, 0] * v[:, 1] - r[:, 1] * v[:, 0])

    ax_angular.plot(t, L, '-g')
    line_t_angular, = ax_angular.plot([], [], '-k')

    # Schwerpunkt
    ax_com.set_title('Schwerpunkt', fontsize=12)
    ax_com.set_xlabel('x [m]', fontsize=12)
    ax_com.set_ylabel('y [m]', fontsize=12)

    com = np.zeros((n_steps, 2)) # com = centre of mass
    for i, b in enumerate(bodies):
        com += masses[i] * b.r_history
    
    com /= masses.sum()

    ax_com.plot(com[:, 0], com[:, 1], '-m', alpha=0.5)
    com_point, = ax_com.plot([], [], 'mo', markersize=6) 

    # Impuls
    ax_momentum.set_title('Gesamtimpuls', fontsize=12)
    ax_momentum.set_xlabel('t [s]', fontsize=12)
    ax_momentum.set_ylabel('P [kg m/s]', fontsize=12)

    p_total = np.zeros((n_steps, 2))
    for i, b in enumerate(bodies):
        p_total += masses[i] * b.v_history
    p_mag = np.linalg.norm(p_total, axis=1)

    ax_momentum.plot(t, p_mag, '-r')
    line_t_momentum, = ax_momentum.plot([], [], '-k')

    fig_graphs.tight_layout()

    #Animation
    def update_orbit(frame):
        for body in bodies:
            body.r = body.r_history[frame]

        for i, b in enumerate(bodies):
            r = b.r_history
            trail_lines[i].set_data(r[:frame + 1, 0], r[:frame + 1, 1])
            points[i].set_data([r[frame, 0]], [r[frame, 1]])


            a = b.total_acceleration(bodies)
            a_norm = np.linalg.norm(a)
            if a_norm > 0: 
                scale = margin / a_norm * 0.3
                x0, y0 = r[frame, 0], r[frame, 1]
                accel_arrows[i].set_position((x0, y0))
                accel_arrows[i].xy = (x0 + a[0] * scale, y0 + a[1] * scale)

        return trail_lines + points + accel_arrows

    def update_graphs(frame): 
        x_pos = t[frame]
        line_t_energy.set_data([x_pos, x_pos], ax_energy.get_ylim())
        line_t_angular.set_data([x_pos, x_pos], ax_angular.get_ylim())
        line_t_momentum.set_data([x_pos, x_pos], ax_momentum.get_ylim())
        com_point.set_data([com[frame, 0]], [com[frame, 1]])
        return [line_t_energy, line_t_angular, line_t_momentum, com_point]

    anim_orbit = FuncAnimation(fig_orbit, update_orbit, frames=n_steps, interval=100, blit=False, repeat=True)
    anim_graphs = FuncAnimation(fig_graphs, update_graphs, frames=n_steps, interval=100, blit=False, repeat=True)
    active_animations.extend([anim_orbit, anim_graphs])

    fig_orbit.show()
    fig_graphs.show()

    return fig_orbit, fig_graphs