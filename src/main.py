#menu.py IMPORTS
import matplotlib.pyplot as plt
from menu import main_menu

if __name__ == "__main__":
    fig_menu  = plt.figure(figsize=(14, 8))
    main_menu(fig_menu)  
    plt.show()

