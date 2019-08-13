from math import *

ANNEE_LUMIERE = 9.5 * 10 ** 15
UNITE_ASTRO = 149597870700
G = 6.67 * 10 ** -11  # N.m2.kg-2
DENSITE = 1
UNITE_DISTANCE = 1  # distance unitaire en m


class Planet:
    listePlanet = {}

    def __init__(self, canvas, x, y, r, coul, nom_planet):
        self.canvas = canvas
        self.coords = (x, y, r)
        self.planet = canvas.create_oval((x - r, y - r, x + r, y + r), fill=coul)
        self.masse = self._masse(r)
        self.nom = nom_planet
        self.listePlanet[nom_planet] = self

    def choisir_direc(self, hb, gd):
        """ gestion du mouvement de l'objets dans le canvas et 
        gestion des colisions avec les bordures """
        tmp_coords = self.canvas.coords(self.planet)

        colisions = False
        out_of_border = False
        if tmp_coords[0] + gd < 0 or tmp_coords[2] + gd > 200 or \
                tmp_coords[1] + hb < 0 or tmp_coords[3] + hb > 200:
            out_of_border = True

        for nomPlanet, ObjPlanet in Planet.listePlanet.items():
            x1, y1, r1 = ObjPlanet.coords
            x2, y2, r2 = self.coords

            if nomPlanet == self.nom:
                continue
            else:
                distance = sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
                if distance < (r1 + r2):
                    colisions = True

        if out_of_border:
            print("mouvement interdit")
            return
        elif colisions:
            print("collision des planets")
        else:
            self.canvas.move(self.planet, gd, hb)

    def move(self, direction):
        """ detection de la direction du mouvement"""
        if direction == "haut":
            self.choisir_direc(hb=-10, gd=0)
        elif direction == "bas":
            self.choisir_direc(hb=+10, gd=0)
        elif direction == "droite":
            self.choisir_direc(hb=0, gd=+10)
        elif direction == "gauche":
            self.choisir_direc(hb=0, gd=-10)
        else:
            self.choisir_direc(0, 0)
        label_update()

    def centre_masse(self):
        """ retrouve la position du centre de masse 
        dans les coord du canvas"""
        position = self.canvas.coords(self.planet)
        x = (position[0] + position[2]) // 2
        y = (position[1] + position[3]) // 2
        return (x, y)

    def _masse(self, r):
        """ volumne de la sphere (m3) 
        puis calcul de la masse (kg) avec la densite """
        volume = (4 / 3) * pi * r ** 3
        return DENSITE * 1000 * volume
