import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox, Button

fig = plt.figure(figsize=(6, 3))
box = TextBox(fig.add_axes([0.2, 0.6, 0.5, 0.2]), "", initial="0.0")
btn = Button(fig.add_axes([0.2, 0.2, 0.3, 0.2]), "Test")
btn.on_clicked(lambda e: print("Klick OK, Text =", box.text))
plt.show()