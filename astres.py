#-*-coding:utf-8

"""
exercice pratique de création d'un programme d'affichage et de calcul 
de la graviation entre plusieurs astres 

source et ennonce du probleme :
https://python.developpez.com/cours/TutoSwinnen/?page=Chapitre8#L8.7
"""
import tkinter as tk
from math import *
import logging

logging.basicConfig(filename='planet.log', filemode='w', \
                    format='%(name)s - %(levelname)s - %(message)s', \
                    level=logging.DEBUG)

logging.debug('--------------- Start new session ------------------')


ANNEE_LUMIERE = 9.5*10**15  
UNITE_ASTRO = 149597870700
G = 6.67*10**-11 #N.m2.kg-2
DENSITE = 1
UNITE_DISTANCE = 1 #distance unitaire en 

def labelTest():
    labMass1.configure(text="masse 1")
    labMass2.configure(text="masse 2")
    #labDistance.configure(text="distance")
    labForce1.configure(text="Force 2-1")
    labForce2.configure(text="Force 1-2")

class planet:
    listePlanet = {}
    def __init__(self, canvas, x, y, r, coul, NomPlanet):
        self.canvas = canvas
        self.coords = (x, y, r)
        self.planet = canvas.create_oval((x-r, y-r, x+r, y+r), fill=coul)
        self.masse = self._masse(r)
        self.nom = NomPlanet
        self.listePlanet[NomPlanet] = self
        
    def move(self, direction, vitesse=10):
        """ detection de la direction du mouvement"""
        if direction == "haut":
            self.choisir_direc(hb=-vitesse, gd=0)
        elif direction == "bas":
            self.choisir_direc(hb=+vitesse, gd=0)
        elif direction == "droite":
            self.choisir_direc(hb=0, gd=+vitesse)
        elif direction == "gauche":
            self.choisir_direc(hb=0, gd=-vitesse)
        else:
            self.choisir_direc(0, 0)
        label_update()

    def choisir_direc(self, hb, gd):
        """ gestion du mouvement de l'objets dans le canvas et 
        gestion des colisions avec les bordures """
        tmpCoords = self.canvas.coords(self.planet)
        """
        logging.info("intial coord ({}, {}) r= {}".format(tmpCoords[0], \
        tmpCoords[1], \
        tmpCoords[2]))
        
        logging.info("deplacement horiz = {} verti = {}".format(gd, hb))
        """
        colisions = False
        OutOfBorder = False
        #gestion des out of border
        if tmpCoords[0]+gd<0 or tmpCoords[2]+gd>200 or \
            tmpCoords[1]+hb<0 or tmpCoords[3]+hb>200:
            OutOfBorder = True

        #gestion des colisions avec les autres planets
        for nomPlanet, ObjPlanet in planet.listePlanet.items():
            x1, y1, r1 = self.coords
            x2, y2, r2 = ObjPlanet.coords
            
            if nomPlanet == self.nom:
                continue
            else:
                distance = sqrt(((x1+gd)-x2)**2 + ((y1+hb)-y2)**2)
                
                logging.debug("{} ({}, {}) r= {} => ({}, {})".format( \
                    self.nom, x1, y1, r1, (x1+gd), (y1+hb)))
                logging.debug("{} ({}, {}) r= {}".format( \
                    nomPlanet, x2, y2, r2))
                logging.debug("deplacement x= {}, y= {}".format(gd, hb))
                logging.debug("distance= {:.2f} somme rayon = {}".format( \
                     distance, r1+r2))
                
                #print("distance de {:.2f} m avec la planet {}".format(
                #    distance, ObjPlanet.nom))
                if distance <= (r1+r2):
                    colisions = True

        if OutOfBorder:
            print("mouvement interdit")
            return
        elif colisions:
            print("collision des planets")
            return
        else:
            old_x, old_y, old_r = self.coords
            self.coords = (old_x+gd, old_y+hb, old_r)
            self.canvas.move(self.planet, gd, hb)

    def centre_masse(self):
        """ retrouve la position du centre de masse 
        dans les coord du canvas"""
        position = self.canvas.coords(self.planet)
        x = (position[0]+position[2])//2
        y = (position[1]+position[3])//2
        return (x, y)

    def _masse(self, r):
        """ volumne de la sphere (m3) 
        puis calcul de la masse (kg) avec la densite """
        volume = (4/3)*pi*r**3
        return DENSITE*1000*volume


def cercle(x, y, r, coul="black"):
	""" function graphique pour l'affichage simplifié d'un cercle"""
	can.create_oval(x-r, y-r, x+r, y+r, fill=coul)

# --- fonction de calcul ---

def get_distance(obj1, obj2):
	""" calcul la distance entre 2 objets 'planet' 
	par la norme du vecteur entre leurs centre de masse
	"""
	global UNITE_DISTANCE
	coord1 = obj1.centre_masse()
	coord2 = obj2.centre_masse()
	distance = sqrt((coord2[0]-coord1[0])**2 + (coord2[1]-coord1[1])**2)*UNITE_DISTANCE
	return distance


def force_gravitation(obj1, obj2):
	""" calcul de la force de gravitation de l'obj2 sur l'obj1"""
	return G*(obj1.masse*obj2.masse)/get_distance(obj1,obj2)**2

# --- fonction d'affichage des labels ---

def display_distance(obj1, obj2):
    """ affichage de la distance entre 2 objects avec 4 unitees de distance :
    - année lumiére a.l.
    - unité astronomique u.a
    - le km- le m
    """
    distance = get_distance(obj1, obj2)
    if distance//ANNEE_LUMIERE > 1:
        return "{:.2f} a.l.".format(distance/ANNEE_LUMIERE)
    elif distance//UNITE_ASTRO > 1:
        return "{:.2f} ua".format(distance/UNITE_ASTRO)
    elif distance//10**3:
        return "{:.2f} km".format(distance/10*3)
    else:
        return "{:.2f} m".format(distance)


def display_force(obj1, obj2):
    force = force_gravitation(obj1, obj2)
    i=0
    if force//1>1:
        while force//10**i > 1:
            i+=1
        return "{:.2f}x1e{}".format(force/10**(i-1), (i-1))
    else:
        while force*10**i < 1:
            i+=1
        return "{:.2f}x1e-{}".format(force*10**(i), i)

def display_masse(masse):
    i=0
    while masse//10**i > 1:
        i+=1
    return "{:.2f}x1e{} kg".format(masse/10**(i-1), (i-1))


def label_update():
    labMass1.configure(text=display_masse(planet1.masse))
    labMass2.configure(text=display_masse(planet2.masse))
    labDistance.configure(text=display_distance(planet1, planet2))
    labForce1.configure(text=display_force(planet1, planet2))
    labForce2.configure(text=display_force(planet2, planet1))


### programme principal ###

# position initial
x1, y1 = 50, 100
x2, y2 = 150, 100

# affichage
root = tk.Tk()
root.title("gravitation")

labMass1 = tk.Label(root, bg="ivory")
labMass1.grid(row=0, column=0, columnspan=2)

labDistance = tk.Label(root, bg="green")
labDistance.grid(row=0, column=2, columnspan=2)

labMass2 = tk.Label(root, bg="red")
labMass2.grid(row=0, column=4, columnspan=2)

can = tk.Canvas(root, width=200, height=200, bg="blue4")
can.grid(row=1, columnspan=6)

tk.Label(root, text="astre 1").grid(row=2, column=0, columnspan=2)
tk.Label(root, text="astre 2").grid(row=2, column=4, columnspan=2)

labForce1=tk.Label(root, bg="gold")
labForce1.grid(row=3, column=0, columnspan=2)

labForce2 = tk.Label(root, bg="brown")
labForce2.grid(row=3, column=4, columnspan=2)

frame=tk.Frame(root)
frame.grid(row=4, columnspan=6)

planet1=planet(can, x1, y1, 5, "red", NomPlanet="planet1")
planet2=planet(can, x2, y2, 10, "green", NomPlanet="planet2")

vitesse = 5

# --- astre 1 ---
tk.Button(root, text="haut", command= lambda: planet1.move("haut", vitesse))\
    .grid(row=4, column=0)
tk.Button(root, text="bas", command=lambda: planet1.move("bas", vitesse))\
    .grid(row=4, column=1)
tk.Button(root, text="droite", command=lambda: planet1.move("droite", vitesse))\
    .grid(row=5, column=1)
tk.Button(root, text="gauche", command=lambda: planet1.move("gauche", vitesse))\
    .grid(row=5, column=0)

# --- astre 2 ---
tk.Button(root, text="haut", command= lambda: planet2.move("haut", vitesse))\
    .grid(row=4, column=4)
tk.Button(root, text="bas", command= lambda: planet2.move("bas", vitesse))\
    .grid(row=4, column=5)
tk.Button(root, text="droite", command= lambda: planet2.move("droite", vitesse))\
    .grid(row=5, column=5)
tk.Button(root, text="gauche", command= lambda: planet2.move("gauche", vitesse))\
    .grid(row=5, column=4)

label_update()
root.mainloop()
