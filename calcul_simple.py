import tkinter as tk
from math import *

""" definition de l'action à effectuer si l'utilisateur actionne
la touche "enter" alors qu'il edite le champ d'entrée"""

def evaluer(event):
    chaine.configure(text='Resultat = ' + str(eval(entree.get())))

### programme prinipal ####
root=tk.Tk()
entree=tk.Entry(root)

#lie l'event "appuie touche entree" a l'action evaluer
entree.bind("<Return>", evaluer) 
chaine=tk.Label(root)
entree.pack()
chaine.pack()

root.mainloop()