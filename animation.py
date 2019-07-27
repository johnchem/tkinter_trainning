import tkinter as tk 
# procédure générale de déplacement : 
def avance(gd, hb): 
    global x1, y1 
    x1, y1 = x1+gd, y1+hb 
    can1.coords(oval1, x1, y1, x1+30, y1+30) 
    
# gestionnaires d'événements : 
def depl_gauche(): 
    avance(-10, 0) 

def depl_droite(): 
    avance(10, 0) 

def depl_haut(): 
    avance(0, -10) 

def depl_bas(): 
    avance(0, 10) 
    
#------ Programme principal ------- 
# les variables suivantes seront utilisées de manière globale : 
x1, y1 = 10, 10 

# coordonnées initiales 
# Création du widget principal ("maître") : 
root = tk.Tk() 
root.title("Exercice d'animation avec Tkinter") 

# création des widgets "esclaves" : 
can1 = tk.Canvas(root,bg='dark grey',height=300,width=300) 
oval1 = can1.create_oval(x1,y1,x1+30,y1+30,width=2,fill='red') 
can1.pack(side="left") 

tk.Button(root, text='Quitter', command=root.quit).pack(side="bottom") 
tk.Button(root, text='Gauche', command=depl_gauche).pack() 
tk.Button(root, text='Droite', command=depl_droite).pack() 
tk.Button(root, text='Haut', command=depl_haut).pack() 
tk.Button(root, text='Bas', command=depl_bas).pack() 

# démarrage du réceptionnaire d'évènements (boucle principale) : 
root.mainloop() 