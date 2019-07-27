import tkinter as tk
from random import randrange

# --- definition des fonctions gestionnaires d'événement ---
def drawline():
    global x1, y1, x2, y2, coul
    can1.create_line(x1, y1, x2, y2, width=2, fill=coul)

    #modification des coordonnées pour la lignes suivante :
    y2, y1 = y2+10, y1-10

def changecolor():
    global coul
    pal=['purple', 'cyan', 'maroon', 'green', 'red', 'blue', 'orange', 'yellow']
    c=randrange(8)
    coul=pal[c]

# --- programme principal ----

#variable utilisées de maniére global :
x1, y1, x2, y2 = 10, 190, 190, 10
coul = 'dark green'

#création du widget principal ("maitre")
root = tk.Tk()

#création des widgets "esclaves" :
can1=tk.Canvas(root, bg='dark grey', height=200, width=200)
can1.pack(side="left")

bou1=tk.Button(root, text="Quitter", command=root.quit)
bou1.pack(side='bottom')

bou2=tk.Button(root,text="Tracer une ligne", command=drawline)
bou2.pack()

bou3=tk.Button(root, text="Autre couleur", command=changecolor)
bou3.pack()

root.mainloop()     #demarrage du receptionnaire d'évenements
root.destroy()      #destruction de la fenêtre