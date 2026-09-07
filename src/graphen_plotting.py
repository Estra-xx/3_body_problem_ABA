from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import scipy.integrate

fig = plt.figure(figsize=(14, 8))
fig.set_tight_layout(True)

#GridSpec, 2 Zeilen, 3 Spalten
gs = fig.add_gridspec(2, 3, width_ratios=[1.5, 1, 1])

# Erzeuge eine Axes für die Bahnkurve der Sterne.
ax_bahn = fig.add_subplot(gs[:, 0])
ax_bahn.set_xlabel('$x$ [AE]')
ax_bahn.set_ylabel('$y$ [AE]')
ax_bahn.set_aspect('equal')
ax_bahn.grid()

# Plotte die Bahnkurven der Sterne.
ax_bahn.plot(r1[0] / AE, r1[1] / AE, '-r')
ax_bahn.plot(r2[0] / AE, r2[1] / AE, '-b')

# Erzeuge Punktplots für die Positionen der Himmelskörper.
plot_stern1, = ax_bahn.plot([], [], 'o', color='red')
plot_stern2, = ax_bahn.plot([], [], 'o', color='blue')

# Erzeuge zwei Pfeile für die Beschleunigungsvektoren.
style = mpl.patches.ArrowStyle.Simple(head_length=6, head_width=3)
pfeil_a1 = mpl.patches.FancyArrowPatch((0, 0), (0, 0), color='red',
                                       arrowstyle=style)
pfeil_a2 = mpl.patches.FancyArrowPatch((0, 0), (0, 0), color='blue',
                                       arrowstyle=style)

# Füge die Pfeile zur Axes hinzu.
ax_bahn.add_patch(pfeil_a1)
ax_bahn.add_patch(pfeil_a2)

# Erzeuge eine Axes und plotte die Energie.
ax_energ = fig.add_subplot(gs[0, 1])
ax_energ.set_title('Energie')
ax_energ.set_xlabel('$t$ [d]')
ax_energ.set_ylabel('$E$ [J]')
ax_energ.grid()
ax_energ.plot(t / tag, E_kin1, '-r', label='$E_{kin,1}$')
ax_energ.plot(t / tag, E_kin2, '-b', label='$E_{kin,2}$')
ax_energ.plot(t / tag, E_pot, '-c', label='$E_{pot}$')
ax_energ.plot(t / tag, E_pot + E_kin1 + E_kin2,
              '-k', label='$E_{ges}$')
ax_energ.legend()

# Erzeuge eine Axes und plotte den Drehimpuls.
ax_drehimpuls = fig.add_subplot(gs[0, 2])
ax_drehimpuls.set_title('Drehimpuls')
ax_drehimpuls.set_xlabel('$t$ [d]')
ax_drehimpuls.set_ylabel('$L$ [kg m² / s]')
ax_drehimpuls.grid()
ax_drehimpuls.plot(t / tag, drehimpuls)

# Erzeuge eine Axes und plotte den Schwerpunkt.
ax_schwerpunkt = fig.add_subplot(gs[1, 1])
ax_schwerpunkt.set_title('Schwerpunkt')
ax_schwerpunkt.set_xlabel('$t$ [d]')
ax_schwerpunkt.set_ylabel('$r_s$ [mm]')
ax_schwerpunkt.grid()
ax_schwerpunkt.plot(t / tag, 1e3 * rs[0, :], label='$r_{s,x}$')
ax_schwerpunkt.plot(t / tag, 1e3 * rs[1, :], label='$r_{s,y}$')
ax_schwerpunkt.legend()

# Erzeuge eine Axes und plotte den Impuls.
ax_impuls = fig.add_subplot(gs[1, 2])
ax_impuls.set_title('Impuls')
ax_impuls.set_xlabel('$t$ [d]')
ax_impuls.set_ylabel('$p$ [kg m / s]')
ax_impuls.grid()
ax_impuls.plot(t / tag, impuls[0, :], label='$p_x$')
ax_impuls.plot(t / tag, impuls[1, :], label='$p_y$')
ax_impuls.legend()

# Sorge dafür, dass die nachfolgenden Linien nicht mehr die
# y-Skalierung verändern.
ax_energ.set_ylim(auto=False)
ax_drehimpuls.set_ylim(auto=False)
ax_schwerpunkt.set_ylim(auto=False)

# Erzeuge drei schwarze Linien, die die aktuelle Zeit in den
# Plots für Energie, Impuls und Drehimpuls darstellen.
linie_t_energ, = ax_energ.plot([], [], '-k')
linie_t_drehimp, = ax_drehimpuls.plot([], [], '-k')
linie_t_schwerpunkt, = ax_schwerpunkt.plot([], [], '-k')


def update(n):
    """Aktualisiere die Grafik zum n-ten Zeitschritt."""
    # Aktualisiere die Positionen der Sterne.
    plot_stern1.set_data(r1[:, n].reshape(-1, 1) / AE)
    plot_stern2.set_data(r2[:, n].reshape(-1, 1) / AE)

    # Berechne die Momentanbeschleunigung und aktualisiere die
    # Vektorpfeile.
    u = np.concatenate([r1[:, n], r2[:, n], v1[:, n], v2[:, n]])
    a_1, a_2 = np.split(dgl(t[n], u), 4)[2:]
    pfeil_a1.set_positions(r1[:, n] / AE,
                           r1[:, n] / AE + scal_a * a_1)
    pfeil_a2.set_positions(r2[:, n] / AE,
                           r2[:, n] / AE + scal_a * a_2)

    # Stelle die Zeit in den drei anderen Diagrammen dar.
    x_pos = t[n] / tag
    linien = [linie_t_energ, linie_t_drehimp, linie_t_schwerpunkt]
    for linie in linien:
        linie.set_data([[x_pos, x_pos], linie.axes.get_ylim()])

    return linien + [plot_stern1, plot_stern2, pfeil_a1, pfeil_a2]


# Erzeuge das Animationsobjekt und starte die Animation.
ani = mpl.animation.FuncAnimation(fig, update, frames=t.size,
                                  interval=30, blit=True)
plt.show()