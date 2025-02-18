#-*-coding:utf-8

"""
exercice pratique de création d'un programme d'affichage et de calcul 
de la graviation entre plusieurs astres 

source et ennonce du probleme :
https://python.developpez.com/cours/TutoSwinnen/?page=Chapitre8#L8.7

- Les planetes sont represente par des ronds de couleur
- elles sont selectionnable par un clic et on peut modifier leurs positions 
avec les fleches directionnel ou les boutons en haut a gauche de l'interface
- la taille (rayon) des planetes est modifiable via le slider
- la densite est aussi modifiable avec un slider

- lors de la modification des propritees d'une planete, les calculs sont remis a jours
- on calcul la masse de chaque planetes et la distance entre elles pour le calcul de la force de gravite
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
UNITE_DISTANCE = 1 #distance unitaire en m
SCREENWIDTH = 500
SCREENHEIGHT = 700


class planet:
    """
    objet planet:
    .canvas : nom de la variable de canvas pour la gestion de l'affichage dans tkinter
    .coords[3] : coords (x, y, r) caracterisant le cercle
    .densite : valeur de densite
    .nom : nom utilisateur de la planete
    .masse : masse calcule a partir du rayon et de la densite
    .planet : objet oval representant la planet dans le User Interface (UI)
    .listePlanet[] : bibliotheque stockant les objets planet avec leur nom usuel (gestion collision)

    ._collision() : retour True si collision detecte avec bordure ou objet planet
    ._masse() : calcul de la masse de self
    ._update() : mise a jour des parametres calcules (masse)
    .centre_masse() : calcule la position du centre du cercle d'apres la position de l'objet tk.oval
    .change_gravite() : gestion de la modification de la variable .gravite
    .deplacement() : gestion du mouvement dans l'affichage
    .deselect() : desactive l'effet visuel de selection
    .select() : active l'effet visuel de selection
    .size_update() : gestion de la modification de taille de l'objet
    """
    listePlanet = {}
    
    def __init__(self, canvas, x, y, r, coul, NomPlanet):
        logging.info("planet init {name} : ({x}, {y}, {r}) {coul}". format(
            name= NomPlanet, 
            x= x, y= y, r= r,
            coul= coul))

        self.canvas = canvas
        self.coords = (x, y, r)
        self.densite = 1
        self.nom = NomPlanet

        self.masse = self._masse()
        
        self.planet = canvas.create_oval((x-r, y-r, x+r, y+r), fill=coul)
        self.listePlanet[NomPlanet] = self
        

    def _collision(self, newx, newy, newr):
        """prends les nouvelles coordonnées de l'objets et renvoie
        un booleen TRUE si il rentre en contact avec un autre object
        """
        maxWidth = self.canvas.winfo_width()
        maxHeight = self.canvas.winfo_height()

        logging.info("test collision => nouvelle coord {x}, {y}, {r}". format(
            x= newx, y= newy, r= newr
        ))

        #variable booléenne
        collision = False
        OutOfBorder = False

        #gestion des out of border
        if (newx-newr)<0 or (newx+newr)>maxWidth or \
           (newy-newr)<0 or (newy+newr)>maxHeight:
            OutOfBorder = True

        #gestion des colisions avec les autres planets
        for nomPlanet, ObjPlanet in planet.listePlanet.items():
            x2, y2, r2 = ObjPlanet.coords
            
            if nomPlanet == self.nom:
                continue
            else:
                #calcule de la distance entre les centres APRES mvt
                distance = sqrt((newx-x2)**2 + (newy-y2)**2)
                
                #log debugage
                logging.debug("{} ({}, {}) r= {}".format( \
                    self.nom, newx, newy, newr))
                logging.debug("{} ({}, {}) r= {}".format( \
                    nomPlanet, x2, y2, r2))
                logging.debug("distance= {:.2f} somme rayon = {}".format( \
                     distance, newr+r2))
                
                if distance <= (newr+r2):
                    collision = True

        logging.debug("collision resultat : Border = {}, planet = {}".format(OutOfBorder, collision))

        if OutOfBorder:
            print("mouvement interdit")
            return True
        elif collision:
            print("collision des planets")
            return True
        else:
            print("pas de collisions")
            return False

    def deplacement(self, hb, gd):
        """ gestion du mouvement de l'objets dans le canvas et 
        gestion des colisions avec les bordures 
        tmpCoords = coordonnées de la boite concentant l'objet
        maxWidth, maxHeight : taille du canevas
        distance : distance entre les centres de 2 objets
        """
        #log pour debugging
        logging.info("deplacement horiz = {} verti = {}".format(gd, hb))

        #màj des coord et mvt si les tests sont OK
        old_x, old_y, r = self.coords
        new_x = old_x+gd
        new_y = old_y+hb

        if self._collision(new_x, new_y, r):
            return
        else:
            self.coords = new_x, new_y, r
            self.canvas.move(self.planet, gd, hb)

    def centre_masse(self):
        """ retrouve la position du centre de masse 
        dans les coord du canvas"""
        position = self.canvas.coords(self.planet)
        x = (position[0]+position[2])//2
        y = (position[1]+position[3])//2

        logging.info("centre de masse {} = ({}, {})".format(
            self.nom, x, y
        ))

        return (x, y)

    def _masse(self):
        """ volumne de la sphere (m3) 
        puis calcul de la masse (kg) avec la densite """
        r = self.coords[2]
        volume = (4/3)*pi*r**3
        masse = self.densite*1000*volume
        return masse

    def _update(self):
        """ update des propritées de l'objet lors de la modification
        de la taille ou de la densité
        """
        logging.debug("update {}".format(self.nom))

        self.masse = self._masse()
     
    def select(self):
        "active l'aspect selectionner de l'objet"
        logging.debug("{} select".format(self.nom))

        self.canvas.itemconfig(self.planet, outline = "black", width=2)
        
    def deselect(self):
        "desactive l'aspect selectionne de l'objet"
        logging.debug("{} deselect".format(self.nom))

        color = self.canvas.itemcget(self.planet, "fill")
        self.canvas.itemconfig(self.planet, outline = color, width=1)
    
    def change_densité(self, value):
        "modification de la densité et màj de la masse"
        logging.debug("modification densité {} => {}".format(self.nom, value))
        self.densite = value
        self._update()
        
    def size_update(self, value):
        """ modification de la taille de l'objet aprés test collision
        si collision, renvoie False sinon modifie les coords de l'objet
        """
        x, y, r = self.coords
        if self._collision(x, y, value):
            logging.debug("{} collision detecté aug taille annulé".format(self.nom))
            return False
        else:
            logging.debug("{} aug. taille autorisé r={}".format(self.nom, value))

            self.coords = x, y, value
            self._update()
            self.canvas.coords(self.planet, (x-value, y-value, x+value, y+value))


def cercle(x, y, r, coul="black"):
	""" fonction graphique pour l'affichage simplifié d'un cercle"""
	can.create_oval(x-r, y-r, x+r, y+r, fill=coul)

def pointeur(event):
    """ gere la selection ou deselection des planetes lors de l'event clic droit"""
    global selected_planet
    Xp, Yp = event.x, event.y
    selected_planet = None

    for nomPlanet, ObjPlanet in planet.listePlanet.items():
        X1, Y1, R1 = ObjPlanet.coords
        distance = sqrt((Xp-X1)**2+(Yp-Y1)**2)
        
        if distance <= R1:
            selected_planet = ObjPlanet
            ObjPlanet.select()

            logging.debug("modification curseur objet")
            
            densityScale.set(ObjPlanet.densite)
            sizeScale.set(ObjPlanet.coords[2])
        else:
            ObjPlanet.deselect()

    if selected_planet == None:
        logging.debug("raz des curseur objet")
        
        densityScale.set(0)
        sizeScale.set(0)

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
	par la norme du vecteur entre leurs centres de masses
	"""
	global UNITE_DISTANCE
	coord1 = obj1.centre_masse()
	coord2 = obj2.centre_masse()
	distance = sqrt((coord2[0]-coord1[0])**2 + (coord2[1]-coord1[1])**2)*UNITE_DISTANCE
	return distance


def force_gravitation(obj1, obj2):
	""" calcul de la force de gravitation de l'obj2 sur l'obj1"""
	return G*(obj1.masse*obj2.masse)/get_distance(obj1,obj2)**2

# --- fonction de modification d'object ---

def increase_size(planet, value):
    """ handler externe pour la modification de la taille des planetes"""

    if not planet == None:
        logging.debug("modification de la taille de {}: {}".format(planet.nom, value))

        #si la modification de la taille echoue => reinitialisation de la position du curseur de taille
        if planet.size_update(value) == False:
            sizeScale.set(planet.coords[2])
        else:
            label_update()
    else:
        print("selectionner une planete")

def increase_density(planet, value):
    """ handler externe pour la modification de la densite des planetes"""

    if not planet == None:
        logging.debug("modification de la densite de {}: {}".format(planet.nom, value))

        planet.change_densité(value)
        label_update()
    else:
        print("selectionner une planete")

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
    """ mise en forme de l'affichage de la force """
    force = force_gravitation(obj1, obj2)
    i=0
    if force//1>1:
        while force//10**i > 1:
            i+=1
        return "{:.2f}x1e{} N".format(force/10**(i-1), (i-1))
    else:
        while force*10**i < 1:
            i+=1
        return "{:.2f}x1e-{} N".format(force*10**(i), i)

def display_masse(masse):
    """ mise en forme de l'affichage de la masse """
    i=0
    while masse//10**i > 1:
        i+=1
    return "{:.2f}x1e{} kg".format(masse/10**(i-1), (i-1))


def label_update():
    """ mise a jours des l'ensembles des valeurs de l'UI """

    liste_planets = list(planet.listePlanet.keys())
    
    FirstPlanet = planet.listePlanet[liste_planets[0]]
    SecondPlanet = planet.listePlanet[liste_planets[1]]
    
    force_1_2 = display_force(FirstPlanet, SecondPlanet)
    force_2_1 = display_force(SecondPlanet, FirstPlanet)
    
    labName1.configure(text=FirstPlanet.nom)
    labForce1.configure(text=force_1_2)
    labMass1.configure(text=display_masse(FirstPlanet.masse))
    labDensity1.configure(text=FirstPlanet.densite)
    labRadius1.configure(text=FirstPlanet.coords[2])
    
    labName2.configure(text=SecondPlanet.nom)
    labForce2.configure(text=force_2_1)
    labMass2.configure(text=display_masse(SecondPlanet.masse))
    labDensity2.configure(text=SecondPlanet.densite)
    labRadius2.configure(text=SecondPlanet.coords[2])
    
    labDistance.configure(text=display_distance(FirstPlanet, SecondPlanet))
    

### programme principal ###

#global variable
selected_planet = None

# affichage racine tkinter
root = tk.Tk()
 
# Gets both half the screen width/height and window width/height
positionRight = int(root.winfo_screenwidth()/2 - SCREENWIDTH/2)
positionDown = int(root.winfo_screenheight()/2 - SCREENHEIGHT/2)

#fenetre principale
root.title("gravitation")
root.geometry("+{posR}+{posD}".format( \
    posR=positionRight, posD=positionDown))

"""
root.geometry("{w}x{h}+{posR}+{posD}".format( \
    w=SCREENWIDTH, h=SCREENHEIGHT, \
    posR=positionRight, posD=positionDown))
"""

#canevas pour l'affichage des planetes
can = tk.Canvas(root, width=500, height=500, bg="blue4")
can.grid(row=0, column=0, sticky="NSEW")

#affichage des infos numérique
frame=tk.Frame(root, bg="black")
frame.grid(row=1, column= 0, columnspan=1, sticky="NSEW")

#affichage des controles
control_box=tk.Frame(root, bg="ivory")
control_box.grid(row=0, column=1, sticky="NEW")

#reglage grid frame
frame.grid_columnconfigure(0, weight=1)
frame.grid_columnconfigure(1, weight=2)
frame.grid_columnconfigure(2, weight=2)

#planete 1 label init
labName1 = tk.Label(frame, bg="ivory")
labForce1= tk.Label(frame, bg="ivory")
labMass1 = tk.Label(frame, bg="ivory")
labDensity1 = tk.Label(frame, bg="ivory")
labRadius1 = tk.Label(frame, bg="ivory")

#planete 2 labels init
labName2 = tk.Label(frame, bg="ivory")
labForce2 = tk.Label(frame, bg="ivory")
labMass2 = tk.Label(frame, bg="ivory")
labDensity2 = tk.Label(frame, bg="ivory")
labRadius2 = tk.Label(frame, bg="ivory")

#etiquettes
tk.Label(frame, bg="grey").grid(row=0, column=0, sticky="NSEW")
tk.Label(frame, bg="ivory", text="force").grid(row=1, column=0, sticky="NSEW", padx=1, pady=1)
tk.Label(frame, bg="ivory", text="masse").grid(row=2, column=0, sticky="NSEW", padx=1, pady=1)
tk.Label(frame, bg="ivory", text="densité").grid(row=3, column=0, sticky="NSEW", padx=1, pady=1)
tk.Label(frame, bg="ivory", text="rayon").grid(row=4, column=0, sticky="NSEW", padx=1, pady=1)
tk.Label(frame, bg="ivory", text="distance").grid(row=5, column=0, sticky="NSEW", padx=1, pady=1)

#planet 1 label layout
labName1.grid(row=0, column=1, sticky="NSEW", padx=1, pady=1)
labForce1.grid(row=1, column=1, sticky="NSEW", padx=1, pady=1)
labMass1.grid(row=2, column=1, sticky="NSEW", padx=1, pady=1)
labDensity1.grid(row=3, column=1, sticky="NSEW", padx=1, pady=1)
labRadius1.grid(row=4, column=1, sticky="NSEW", padx=1, pady=1)

#planet 2 labels layout
labName2.grid(row=0, column=2, sticky="NSEW", padx=1, pady=1)
labForce2.grid(row=1, column=2, sticky="NSEW", padx=1, pady=1)
labMass2.grid(row=2, column=2, sticky="NSEW", padx=1, pady=1)
labDensity2.grid(row=3, column=2, sticky="NSEW", padx=1, pady=1)
labRadius2.grid(row=4, column=2, sticky="NSEW", padx=1, pady=1)

#distance
labDistance = tk.Label(frame, bg="ivory")
labDistance.grid(row=5, column=1, columnspan=2, sticky="NSEW", padx=1, pady=1)

#------initialisation des planetes-----
#coord initiales
maxWidth = 500 #can.winfo_width()
maxHeight = 500 #can.winfo_height()
print(maxWidth)
print(maxHeight)

#parametres des planetes
r1 = 5 
x1, y1 = randrange(r1, maxWidth-r1), randrange(r1, maxHeight-r1)

r2 = 10
x2, y2 = randrange(r2, maxWidth-r2), randrange(r2, maxHeight-r2)

#planet init
planet1=planet(can, x1, y1, r1, "red", NomPlanet="planet1")
planet2=planet(can, x2, y2, r2, "green", NomPlanet="planet2")

# --- boutons controles ---

#vitesse de deplacement des planetes dans la fenetres
vitesse = 5

#button creation
UpButton = tk.Button(control_box, text="haut", \
    command= lambda: move(selected_planet, "Up", vitesse))
DownButton = tk.Button(control_box, text="bas", \
    command= lambda: move(selected_planet, "Down", vitesse))
RightButton = tk.Button(control_box, text="droite", \
    command= lambda: move(selected_planet, "Right", vitesse))
LeftButton = tk.Button(control_box, text="gauche", \
    command= lambda: move(selected_planet, "Left", vitesse))

#scrollbar creation
densityScale = tk.Scale(control_box, orient="vertical", from_=1, to=10, resolution = 0.1, \
    command= lambda e: increase_density(selected_planet, float(e)))
labDensityScale = tk.Label(control_box, text="Densité")

sizeScale = tk.Scale(control_box, orient="vertical", from_=1, \
    command= lambda e: increase_size(selected_planet, int(e)))
labSizeScale = tk.Label(control_box, text="Rayon")

#Buttons layouts
UpButton.grid(row=1, column=2, columnspan=2, rowspan=2, sticky="NSEW")
DownButton.grid(row=3, column=2, columnspan=2, rowspan=2, sticky="NSEW")
RightButton.grid(row=2, column=4, columnspan=2, rowspan=2, sticky="NSEW")
LeftButton.grid(row=2, column=0, columnspan=2, rowspan=2, sticky="NSEW")

#scroll bar layout
control_box.rowconfigure(6, minsize=30)
control_box.rowconfigure(8, minsize=300)
labDensityScale.grid(row=7, column=1, columnspan=2, sticky="NSEW")
densityScale.grid(row=8, column=1, columnspan = 2, sticky = "NS")
labSizeScale.grid(row=7, column=3, columnspan=2, sticky="NSEW")
sizeScale.grid(row=8, column=3, columnspan = 2, sticky = "NS")

#evenements claviers
can.bind("<Button-1>", pointeur)
root.bind("<Up>", lambda e: move(selected_planet, e.keysym, vitesse))
root.bind("<Down>", lambda e: move(selected_planet, e.keysym, vitesse))
root.bind("<Right>", lambda e: move(selected_planet, e.keysym, vitesse))
root.bind("<Left>", lambda e: move(selected_planet, e.keysym, vitesse))

#setup initial des etiquettes
label_update()

#boucle principale pour la gestion des events
root.mainloop()
