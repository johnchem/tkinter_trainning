import tkinter as tk
from numpy import arange
from random import choice


def rectangle(x, y, a, coul):
    x1, y1, x2, y2 = x, y, x + a, y + a
    can.create_rectangle(x1, y1, x2, y2, fill=coul)


def cercle(x, y, r, coul='red'):
    can.create_oval(x - r, y - r, x + r, y + r, fill=coul)


def damier():
    """dessiner un damier"""
    # effacer l'ecran
    can.delete('all')

    # dessiner le damier
    coord = arange(0, 200, 200 // 5)
    coul = 'blue'

    for x in coord:
        for y in coord:
            for ecart in (0, 20):
                rectangle(x + ecart, y + ecart, 20, coul)


def pion():
    coord = arange(10, 210, 20)
    x = choice(coord)
    y = choice(coord)
    cercle(x, y, 8)


def pointeur(event):
    cadre.configure(text="clic détecté en X={}, Y={}".format(
        event.x, event.y))

    coord = arange(0, 220, 200 // 10)

    i = 0
    while not event.x < coord[i + 1] and i < len(coord) - 1:
        i += 1
    posx = coord[i]

    i = 0
    while not event.y < coord[i + 1] and i < len(coord) - 1:
        i += 1
    posy = coord[i]

    cercle(posx + 10, posy + 10, 8, "black")


# programme principal

root = tk.Tk()
root.title('damier')

can = tk.Canvas(root, width=200, height=200, bg='white')
can.pack(side='top', padx=5, pady=5)

cadre = tk.Label(root)
cadre.pack()

b1 = tk.Button(root, text="reset", command=damier)
b1.pack(side='left', padx=3, pady=3)

b2 = tk.Button(root, text="pions", command=pion)
b2.pack(side='right', padx=3, pady=3)

can.bind("<Button-1>", pointeur)

damier()
root.mainloop()
