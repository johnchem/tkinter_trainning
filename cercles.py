import tkinter as tk


def cercle(x, y, r, coul='black'):
    """tracé d'un cercle de centre (x,y) et de rayon r"""
    can.create_oval(x - r, y - r, x + r, y + r, outline=coul)


def figure_1():
    """dessiner une cible"""
    # effacer l'ecran
    can.delete('all')

    # tracer les lignes verticales et horizontal :
    can.create_line(100, 0, 100, 200, fill='blue')
    can.create_line(0, 100, 200, 100, fill='blue')
    # tracer plusieurs cercles concentriques:
    rayon = 15
    while rayon < 100:
        cercle(100, 100, rayon)
        rayon += 15


def figure_2():
    """dessiner une visage simplifié"""
    # effacer l'ecran
    can.delete('all')
    # liste de propriété des cercles
    cc = [[100, 100, 80, 'red'],
          [70, 70, 15, 'blue'],
          [130, 70, 15, 'blue'],
          [70, 70, 5, 'black'],
          [130, 70, 5, 'black'],
          [44, 115, 20, 'red'],
          [156, 115, 20, 'red'],
          [100, 95, 15, 'purple'],
          [100, 145, 30, 'purple']]

    for el in cc:
        cercle(el[0], el[1], el[2], el[3])


# programme principal
root = tk.Tk()
can = tk.Canvas(root, width=200, height=200, bg='ivory')
can.pack(side='top', padx=5, pady=5)

b1 = tk.Button(root, text="dessin 1", command=figure_1)
b1.pack(side='left', padx=3, pady=3)

b2 = tk.Button(root, text="dessin 2", command=figure_2)
b2.pack(side='right', padx=3, pady=3)

root.mainloop()
