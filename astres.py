#-*-coding:utf-8

"""
exercice pratique de création d'un programme d'affichage et de calcul 
de la graviation entre plusieurs astres 

source et ennonce du probleme :
https://python.developpez.com/cours/TutoSwinnen/?page=Chapitre8#L8.7
"""

import tkinter as tk
from math import *
from random import randrange
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
SCREENWIDTH = 500
SCREENHEIGHT = 650


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

    def deplacement(self, hb, gd):
        """ gestion du mouvement de l'objets dans le canvas et 
        gestion des colisions avec les bordures 
        tmpCoords = coordonnées de la boite concentant l'objet
        maxWidth, maxHeight : taille du canevas
        distance : distance entre les centres de 2 objets
        """
        tmpCoords = self.canvas.coords(self.planet)
        maxWidth = self.canvas.winfo_width()
        maxHeight = self.canvas.winfo_height()
        
        #log pour debugging
        logging.info("intial coord ({}, {}) r= {}".format(tmpCoords[0], \
        tmpCoords[1], \
        tmpCoords[2]))
        logging.info("deplacement horiz = {} verti = {}".format(gd, hb))
        
        #variable booléenne
        colisions = False
        OutOfBorder = False
        
        #gestion des out of border
        if tmpCoords[0]+gd<0 or tmpCoords[2]+gd>maxWidth or \
            tmpCoords[1]+hb<0 or tmpCoords[3]+hb>maxHeight:
            OutOfBorder = True

        #gestion des colisions avec les autres planets
        for nomPlanet, ObjPlanet in planet.listePlanet.items():
            x1, y1, r1 = self.coords
            x2, y2, r2 = ObjPlanet.coords
            
            if nomPlanet == self.nom:
                continue
            else:
                #calcule de la distance entre les centres APRES mvt
                distance = sqrt(((x1+gd)-x2)**2 + ((y1+hb)-y2)**2)
                
                #log debugage
                logging.debug("{} ({}, {}) r= {} => ({}, {})".format( \
                    self.nom, x1, y1, r1, (x1+gd), (y1+hb)))
                logging.debug("{} ({}, {}) r= {}".format( \
                    nomPlanet, x2, y2, r2))
                logging.debug("deplacement x= {}, y= {}".format(gd, hb))
                logging.debug("distance= {:.2f} somme rayon = {}".format( \
                     distance, r1+r2))
                
                if distance <= (r1+r2):
                    colisions = True

        if OutOfBorder:
            print("mouvement interdit")
            return
        elif colisions:
            print("collision des planets")
            return
        else:
            #màj des coord et mvt si les tests sont OK
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
     
    def select(self):
        self.canvas.itemconfig(self.planet, outline = "black", width=2)
        
    def deselect(self):
        color = self.canvas.itemcget(self.planet, "fill")
        self.canvas.itemconfig(self.planet, outline = color, width=1)


def cercle(x, y, r, coul="black"):
	""" function graphique pour l'affichage simplifié d'un cercle"""
	can.create_oval(x-r, y-r, x+r, y+r, fill=coul)

def pointeur(event):
    global selected_planet
    Xp, Yp = event.x, event.y
    selected_planet = None

    for nomPlanet, ObjPlanet in planet.listePlanet.items():
        X1, Y1, R1 = ObjPlanet.coords
        distance = sqrt((Xp-X1)**2+(Yp-Y1)**2)
        
        if distance <= R1:
            selected_planet = ObjPlanet
            ObjPlanet.select()
        else:
            ObjPlanet.deselect()

def move(planet, direction, vitesse=10):
	""" gestion externe du deplacement des objets"""
	if planet == None:
		print("pas de planete selectionnée")
	else:
		#detection de la direction du mouvement
		if direction == "Up":
			planet.deplacement(hb=-vitesse, gd=0)
		elif direction == "Down":
			planet.deplacement(hb=+vitesse, gd=0)
		elif direction == "Right":
			planet.deplacement(hb=0, gd=+vitesse)
		elif direction == "Left":
			planet.deplacement(hb=0, gd=-vitesse)
		else:
			planet.deplacement(0, 0)
	label_update()

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



#global variable
selected_planet = None

# affichage
root = tk.Tk()
 
# Gets both half the screen width/height and window width/height
positionRight = int(root.winfo_screenwidth()/2 - SCREENWIDTH/2)
positionDown = int(root.winfo_screenheight()/2 - SCREENHEIGHT/2)

root.title("gravitation")
root.geometry("{w}x{h}+{posR}+{posD}".format( \
    w=SCREENWIDTH, h=SCREENHEIGHT, \
    posR=positionRight, posD=positionDown))

labMass1 = tk.Label(root, bg="ivory")
labMass1.grid(row=0, column=0, columnspan=2, sticky="NSEW")

labDistance = tk.Label(root, bg="green")
labDistance.grid(row=0, column=2, columnspan=2, sticky="NSEW")

labMass2 = tk.Label(root, bg="red")
labMass2.grid(row=0, column=4, columnspan=2, sticky="NSEW")

can = tk.Canvas(root, width=500, height=500, bg="blue4")
can.grid(row=1, columnspan=6, sticky="NSEW")

tk.Label(root, text="astre 1").grid(row=2, column=0, columnspan=2, sticky="NSEW")
tk.Label(root, text="astre 2").grid(row=2, column=4, columnspan=2, sticky="NSEW")

labForce1=tk.Label(root, bg="gold")
labForce1.grid(row=3, column=0, columnspan=2, sticky="NSEW")

labForce2 = tk.Label(root, bg="brown")
labForce2.grid(row=3, column=4, columnspan=2, sticky="NSEW")

frame=tk.Frame(root)
frame.grid(row=4, columnspan=6, sticky="NSEW")

x1, y1 = randrange(0, 500), randrange(0, 500)
x2, y2 = randrange(0, 500), randrange(0, 500)
 
planet1=planet(can, x1, y1, 5, "red", NomPlanet="planet1")
planet2=planet(can, x2, y2, 10, "green", NomPlanet="planet2")

vitesse = 5

# --- boutons controles ---
#tk.Button(root, text="haut", command= lambda: planet1.move("haut", vitesse))\
#    .grid(row=4, column=0, sticky="NSEW")
tk.Button(root, text="haut", command= lambda e: move(selected_planet, "Up", vitesse))\
    .grid(row=4, column=0, sticky="NSEW")
tk.Button(root, text="bas", command= lambda e: move(selected_planet, "Down", vitesse))\
    .grid(row=4, column=1, sticky="NSEW")
tk.Button(root, text="droite", command=lambda e: move(selected_planet, "Right", vitesse))\
    .grid(row=5, column=1, sticky="NSEW")
tk.Button(root, text="gauche", command=lambda e: move(selected_planet, "Left", vitesse))\
    .grid(row=5, column=0, sticky="NSEW")

#evenements claviers
can.bind("<Button-1>", pointeur)
root.bind("<Up>", lambda e: move(selected_planet, e.keysym, vitesse))
root.bind("<Down>", lambda e: move(selected_planet, e.keysym, vitesse))
root.bind("<Right>", lambda e: move(selected_planet, e.keysym, vitesse))
root.bind("<Left>", lambda e: move(selected_planet, e.keysym, vitesse))

label_update()
root.mainloop()
