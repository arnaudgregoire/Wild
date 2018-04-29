
"""
@author: Arnaud,Coline,Régis
"""

import numpy as np
#import matplotlib
#matplotlib.use("Agg")
import matplotlib.pyplot as plt
#import matplotlib.animation as manimation
import random as rd
import math
import time




def distance(x1,x2,y1,y2):
    """
    Retourne la distance cartésienne entre le point (x1,y1) et le point(x2,y2)
    """
    return(np.sqrt((x2-x1)**2+(y2-y1)**2))
    
class Bucheron():
    """
    Le bucheron est un humain qui se déplace d'une case par tour en :
    
    -coupant des arbres si il se trouve sur de la forêt morte
    
    Actuellement, il se déplace aléatoirement.
    """
    
    def __init__(self,x,y):
        """
        Un bucheron est défini par ses coordonnées sur la grille
        """
        self.x=x
        self.y=y
        self.choix=False
        
                
    def maj(self):
        """
        Un bucheron peut se déplacer sur une case :
        
        -autour de lui
        -qui ne contient pas d'eau
        
         Il peut :
         
        -couper des arbres si il se trouve sur de la forêt morte
        
        """
        #on regroupe dans Lx et Ly les cases où le bucheron peut potentiellement se déplacer
        Lx=[]
        Ly=[]
        for i in [self.x-1,self.x,self.x+1]:
            for j in [self.y-1,self.y,self.y+1]:
                if i>=0 and i<Terrain.shape[0] and j>=0 and j<Terrain.shape[1] and Terrain[i,j].Etat!=0:
                    Lx=Lx+[i]
                    Ly=Ly+[j]
        #on choisit aléatoirement dans Lx et Ly le déplacement que va faire le sylviculteur
        self.x=Lx[rd.randint(0,len(Lx)-1)]
        self.y=Ly[rd.randint(0,len(Ly)-1)]
        
        # S'il est sur une forêt morte, il la coupe et la fait devenir de la plaine
        if Terrain[self.x,self.y].Etat==3:
            Terrain[self.x,self.y].coupe=True
        
        
        
class Sylviculteur():
    """
    Le sylviculteur est un humain qui se déplace d'une case par tour en :
    
    -soignant une forêt malade s'il est sur une case foret malade
    -plantant des arbres s'il est sur une case plaine
    
    Actuellement, il se déplace aléatoirement.
    """
    
    def __init__(self,x,y):
        """
        Un sylviculteur est défini par ses coordonnées sur la grille
        """
        self.x=x
        self.y=y
        self.choix=False
        
                
    def maj(self):
        """
        Un sylviculteur peut se déplacer sur une case :
        
        -autour de lui
        -qui ne contient pas d'eau
        
        S'il est sur une case forêt malade, il la soigne
        
        S'il est sur une case Plaine, il fait germer une forêt
        """
        #on regroupe dans Lx et Ly les cases où le sylviculteur peut potentiellement se déplacer
        Lx=[]
        Ly=[]
        L_krank=[]
        min=[]
        min_choix=[]
        dist_min=0
        for i in [self.x-1,self.x,self.x+1]:
            for j in [self.y-1,self.y,self.y+1]:
                if i>=0 and i<Terrain.shape[0] and j>=0 and j<Terrain.shape[1] and Terrain[i,j].Etat!=0:
                    Lx=Lx+[i]
                    Ly=Ly+[j]
        #on trouve les cases forêt malade 
        for x in range(Terrain.shape[0]):
            for y in range(Terrain.shape[1]):
                if Terrain[x,y].Etat==4:
                    L_krank=L_krank+[[x,y]]
        
        #on trouve la plus proche de notre sylviculteur
        if L_krank==[]:
            pass
        else:
            min=L_krank[0]
            dist_min=distance(L_krank[0][0],self.x,L_krank[0][1],self.y)
            for i in range(len(L_krank)):
                if distance(L_krank[i][0],self.x,L_krank[i][1],self.y)<dist_min:
                    min=L_krank[i]
                    distmin=distance(L_krank[i][0],self.x,L_krank[i][1],self.y)
        #on regarde quelle déplacement le rapproche le plus de la case malade
            min_choix=[Lx[0],Ly[0]]
            dist_min=distance(Lx[0],min[0],Ly[0],min[1])
            for x in Lx:
                for y in Ly:
                    if distance(x,min[0],y,min[1])<dist_min:
                        min_choix=[x,y]
                        dist_min=distance(Lx[0],min[0],Ly[0],min[1])
            # on déplace le sylviculteur en changeant ses coordonnées
            self.x=min_choix[0]
            self.y=min_choix[1]
        
        # S'il est sur une case Plaine, il fait germer une forêt
        if Terrain[self.x,self.y].Etat==1:
            Terrain[self.x,self.y].germe=True
        #S'il est sur une case forêt malade, il la soigne
        if Terrain[self.x,self.y].Etat==4:
            Terrain[self.x,self.y].soin=True

        
    
class Eau():
    """
    L'eau est un terrain qui ne change jamais
    
    Le sylviculteur ne peut pas se déplacer sur l'eau
    
    Si il y a de l'eau à 2 cases d'une case forêt la forêt grandit plus rapidemment
    """
    
    def __init__(self,x,y):
        """
        L'eau est défini par :
        
        -ses coordonnées (x,y)
        -son Etat, l'état 0 correspond à l'état Eau
        -sa nature, la nature est utilisé pour avoir une joli couleur sur la colormap
        """
        self.x=x
        self.y=y
        self.Etat=0
        self.Etat_suivant=9
        self.nature=0     
        
    def maj(self):
        """
        A chaque tour,l'eau reste de l'eau
        """
        self.Etat_suivant=0
        
class Plaine():
    """
    La Plaine peut être :
    
    -colonisé par de la forêt si il y a de la forêt à proximité
    -
    """
    
    def __init__(self,x,y):
        """
        La plaine est défini par :
        
        -ses coordonnées (x,y)
        -son Etat, l'état 1 correspond à l'état Eau
        -sa nature, la nature est utilisé pour avoir une joli couleur sur la colormap
        """
        self.x=x
        self.y=y
        self.Etat=1
        self.Etat_suivant=9
        self.nature=2
        self.germe=False
        
    def maj(self):
        if self.Etat_suivant==9:
            self.Etat_suivant=1
        if self.germe==True:
            self.Etat_suivant=2
            
class Foret_morte():
    """
    La forêt morte est un état où à chaque tour :
    
    -la taille de la forêt diminue de 1
    - si la taille de la forêt morte passe à 0, la forêt devient au tour suivant de la plaine
    """
    def __init__(self,x,y,taille):
        """
        La forêt morte est défini par :
        
        -ses coordonnées (x,y)
        -son état (l'état "forêt morte" est caracérisé par l'entier 3)
        -sa nature : la nature sert à définir une couleur pour la représentation
        """
        self.x=x
        self.y=y
        self.taille=taille
        self.Etat=3
        self.Etat_suivant=9
        self.nature=1.2
        self.coupe=False
        
    def maj(self):
        """
        Si la taille de la forêt est nulle, elle devient de la plaine,
        sinon elle devient de la forêt morte avec une taille n-1
        """
        if self.taille ==0 or self.coupe==True:
            self.Etat_suivant=1
        else:
            self.taille=self.taille-1
            self.Etat_suivant=3
            
class Foret_malade():
    """
    La forêt malade est un état où à chaque tour :
    
    - une fois que la forêt tombe malade, elle va survivre 5 tour avant de devenir de la forêt morte
    - la forêt malade peut contaminer les cases forêt voisines
    -la durée de la forêt malade diminue de 1 à chaque tour
    - la forêt malade peut être soigné si  un sylviculteur est présent
    """
    
    def __init__(self,x,y,taille):
        """	
        La forêt malade est défini par:
        
        -ses  coordonnées (x,y)
        -sa taille ( entier entre 0 et 30 qui sera transmis à la forêt morte )
        -son état ( l'état 'forêt malade' est caractérisé par l'entier 4
        -sa durée ( le nombre de tours qui reste à la forêt malade à vivre )
        """
        self.x=x
        self.y=y
        self.taille=taille
        self.Etat=4
        self.Etat_suivant=9
        self.nature=1.4
        self.duree=5
        self.soin=False
        
    def maj(self):
        """
        la forêt malade va:
        
        -essayer d'infecter les cases forêts voisines
        -si la durée de la forêt malade atteint 0, elle se transforme en forêt morte 
        -Sinon, elle passe en forêt malade de durée n-1
        -Si un sylviculteur est présent sur cette case, il active le booléen Soin
        -Si le booléen Soin est activé, la forêt malade devient de la forêt
        """
        if self.duree>0:
            for i in [self.x-1,self.x,self.x+1]:
                for j in [self.y-1,self.y,self.y+1]:
                    if i>=0 and i<Terrain.shape[0] and j>=0 and j<Terrain.shape[1]:
                        if Terrain[i,j].Etat==2:
                            if rd.randint(0,100)>50:
                                Terrain[i,j].Etat_suivant=4

            self.Etat_suivant=4
            self.duree=self.duree-1
        else:
            self.Etat_suivant=3
        if self.soin==True:
            self.Etat_suivant=2
        
class Foret():
    """
    La forêt est un état où à chaque tour:
    
    -elle peut s'étendre sur une des cases plaine voisines si sa taille est supérieur à 15
    -elle peut devenir de la forêt malade avec 0,1% de chance	
    """
    def __init__(self,x,y,taille):
        """	
        La forêt est défini par:
        
        -ses  coordonnées (x,y)
        -sa taille ( entier entre 0 et 30 qui sera transmis à la forêt malade)
        -son état ( l'état 'forêt' est caractérisé par l'entier 2
        -sa nature ( utilisé pour la représentation graphique )
        """
        self.x=x
        self.y=y
        self.taille=taille
        self.Etat=2
        self.Etat_suivant=9
        self.nature=1.8
        
    def maj(self):
        """
        La forêt va:
        
        -grandir de 1 si la taille de la forêt est inférieur à 30
        -essayer d'infecter une des cases plaine voisines si sa taille est supérieur à 15
        -devenir malade avec une probabilité de 0.01% de chance
        """
        A=True
        Eau_voisin=False
        for i in [self.x-2,self.x-1,self.x,self.x+1,self.x+2]:
            for j in [self.y-2,self.y-1,self.y,self.y+1,self.y+2]:
                if i>=0 and i<Terrain.shape[0] and j>=0 and j<Terrain.shape[1]:
                    if Terrain[i,j].Etat==0:
                        Eau_voisin=True
        if Eau_voisin==True and self.taille<30:
            self.taille=self.taille+1
        a=0
        if self.taille<30:
            self.taille=self.taille+1
        if self.taille>15:
            for i in [self.x-1,self.x,self.x+1]:
                for j in [self.y-1,self.y,self.y+1]:
                    if i>=0 and i<Terrain.shape[0] and j>=0 and j<Terrain.shape[1] and a<=1:
                        if Terrain[i,j].Etat==1:
                            if rd.randint(0,100)>20:
                                Terrain[i,j].Etat_suivant=2
        while A==True:
            if rd.uniform(0,100)>99.99:
                self.Etat_suivant=4
            else:
                self.Etat_suivant=2
            A=False
        self.nature=1.8-(0.2/30)*self.taille

        
def tour(Terrain):
    """
    Un tour consiste en une simulation, c'est à dire la mise à jour de la matrice de nos objets (Plaine ,eau , foret etc...)
    
    """
    #on met à jour tous les objets du terrains
    for x in range(Terrain.shape[0]):
        for y in range(Terrain.shape[1]):
            Terrain[x,y].maj()
    #on met à jour tous les sylviculteurs
    for sylviculteur in sylviculteurs:
        sylviculteur.maj()
      #on met à jour tous les bucherons
    for bucheron in bucherons:
        bucheron.maj()
            
    for x in range(Terrain.shape[0]):
        for y in range(Terrain.shape[1]):
            if Terrain[x,y].Etat!=Terrain[x,y].Etat_suivant:
                if Terrain[x,y].Etat_suivant==1:
                    Terrain[x,y]=Plaine(x,y)
                if Terrain[x,y].Etat_suivant==2 and Terrain[x,y].Etat==1:
                    Terrain[x,y]=Foret(x,y,0)
                if Terrain[x,y].Etat_suivant==2 and Terrain[x,y].Etat==4:
                    Terrain[x,y]=Foret(x,y,Terrain[x,y].taille)
                if Terrain[x,y].Etat_suivant==4:
                    Terrain[x,y]=Foret_malade(x,y,Terrain[x,y].taille)
                if Terrain[x,y].Etat_suivant==3:
                    Terrain[x,y]=Foret_morte(x,y,Terrain[x,y].taille) 
                    

    for x in range(Terrain.shape[0]):
        for y in range(Terrain.shape[1]):
            if Terrain[x,y].Etat_suivant!=9:
                Terrain[x,y].Etat=Terrain[x,y].Etat_suivant
                Terrain[x,y].Etat_suivant=9



 
def generation_terrain(taille_x,taille_y,nb_sylviculteurs,nb_bucherons):
    """
    Génère une matrice d'objets terrain (Eau,Plaine,etc...) et une liste d'objets sylviculteurs.
    Pour créer un terrain cohérent, la fonction utilise un bruit de valeur.
    Le bruit de valeur permet la génération aléatoire de formes cohérentes
    Ces formes sont ensuite lissés par une interpolation bilinéaire
    On discrétise ensuite la matrice obtenue pour faire corresspondre chaque case à un état(Eau,Plaine,Forêt)
    On peut jouer sur la persistence du bruit de Perlin pour varier la forme du terrain généré
     
    """
    imgx = taille_x; imgy = taille_y 
    octaves = int(math.log(max(imgx, imgy), 2.0))
    persistence =0.8
    imgAr = [[0.0 for i in range(imgx)] for j in range(imgy)] # matrice intermédiaire
    totAmp = 0.0
    for k in range(octaves):
        freq = 2**k
        amp = persistence ** k
        totAmp += amp
        # création d'une matrice de taille n*m (*amplitude)
        n = freq + 1; m = freq + 1 # taille de la matrice
        ar = [[rd.random() * amp for i in range(n)] for j in range(m)]
        nx = imgx / (n - 1.0); ny = imgy / (m - 1.0)
        for ky in range(imgy):
            for kx in range(imgx):
                #création du bruit de valeur
                #avec une interpolation bilinéaire
                i = int(kx / nx); j = int(ky / ny)
                dx0 = kx - i * nx; dx1 = nx - dx0
                dy0 = ky - j * ny; dy1 = ny - dy0
                z = ar[j][i] * dx1 * dy1
                z += ar[j][i + 1] * dx0 * dy1
                z += ar[j + 1][i] * dx1 * dy0
                z += ar[j + 1][i + 1] * dx0 * dy0
                z /= nx * ny
                imgAr[ky][kx] += z # Rassemblement dans la matrice intermédiaire
    
    # on cherche les propriétés statistiques de la matrice        
    somme=0
    ecart_carre=0
    for y in range(imgy):
        for x in range(imgx):
            somme=somme+imgAr[y][x]
    
    moyenne=somme/(imgx*imgy)
    
    for y in range(imgy):
        for x in range(imgx):
            ecart_carre=ecart_carre+(imgAr[y][x]-moyenne)**2
            
    ecart_type=np.sqrt(ecart_carre/(imgx*imgy))
    
    # on regroupe toutes les valeurs de la matrice pour n'avoir plus que 3 valeurs
    for y in range(imgy):
        for x in range(imgx):
            if imgAr[y][x]<moyenne-ecart_type:
                imgAr[y][x]=0
            if imgAr[y][x]>moyenne+ecart_type:
                imgAr[y][x]=1.6
            if imgAr[y][x]>=moyenne-ecart_type and imgAr[y][x]<=moyenne+ecart_type:
                imgAr[y][x]=2
    # Création matrice objet ( elle sera modifié par la suite)
    mat_obj=np.array([[Plaine(x,y) for x in range(imgx)]for y in range(imgy)])
    #Les 3 valeurs de la matrice intermédiaire sont associés aux 3 classes terrains de départ (Eau, Plaine, Forêt)
    for y in range(imgy):
        for x in range(imgx):  
            if imgAr[y][x]==0:
                mat_obj[x][y]=Eau(x,y)
            if imgAr[y][x]==1.6:
                mat_obj[x][y]=Foret(x,y,0)
            if imgAr[y][x]==2:
                mat_obj[x][y]=Plaine(x,y)
    # Création d'une liste contenant n objets sylviculteurs (n:paramètre de la fonction)
    sylviculteurs=[]
    # les sylviculteurs sont répartis aléatoirement sur le terrain, ils ne peuvent pas apparaître dans l'eau
    for i in range(nb_sylviculteurs):
        x=rd.randint(0,imgx-1)
        y=rd.randint(0,imgy-1)
        while mat_obj[x][y].Etat==0:
            x=rd.randint(0,imgx-1)
            y=rd.randint(0,imgy-1)
        sylviculteurs=sylviculteurs+[Sylviculteur(x,y)]
    
    bucherons=[]
    # les bucherons sont répartis aléatoirement sur le terrain, ils ne peuvent pas apparaître dans l'eau
    for i in range(nb_bucherons):
        x=rd.randint(0,imgx-1)
        y=rd.randint(0,imgy-1)
        while mat_obj[x][y].Etat==0:
            x=rd.randint(0,imgx-1)
            y=rd.randint(0,imgy-1)
        bucherons=bucherons+[Bucheron(x,y)]
    
    return(mat_obj,sylviculteurs,bucherons)
    
    
def film(Terrain,nb_tours):
    """
    Renvoie un .mp4 qui contient la compilation de chaque repésentation graphique de la simulation.
    Pour que la fonction marche, il faut installer le module ffmpeg
    """
    fig=plt.figure()
    plt.xlim(0,10)
    plt.ylim(0,10)
    FFMpegWriter = manimation.writers['ffmpeg']
    metadata = dict(title='Into the Wild', artist='Arnaud Studio',
                    comment='Movie support!')
    writer = FFMpegWriter(fps=10, metadata=metadata)
    with writer.saving(fig, "wild.mp4", 100):
        for i in range(nb_tours):
            tour(Terrain)
            ihm=np.zeros(Terrain.shape)
            for x in range(Terrain.shape[0]):
                for y in range(Terrain.shape[1]):
                    ihm[x,y]=Terrain[x,y].nature
            plt.imshow(ihm,cmap='brg', interpolation='none')
            for sylviculteur in sylviculteurs:
                plt.plot(sylviculteur.y,sylviculteur.x,'o')
            writer.grab_frame()
            plt.clf()

def ihm(Terrain,tours):
    """
    Renvoie une représentation graphique de l'état de la simulation
    """
    ihm=np.zeros(Terrain.shape)
    for x in range(Terrain.shape[0]):
        for y in range(Terrain.shape[1]):
            ihm[x,y]=Terrain[x,y].nature
    plt.figure()
    plt.pcolormesh(ihm,cmap='brg')
    for sylviculteur in sylviculteurs:
        plt.plot(sylviculteur.y,sylviculteur.x,'o')
    for bucheron in bucherons:
        plt.plot(bucheron.y,bucheron.x,'*')
    plt.colorbar()
    plt.title('Etat du terrain après '+str(tours)+' simulations')
    plt.show()

def dessin(Terrain,nb_tours):
    """
    Renvoie l'état de la simulation après nb_tours
    """
    tic=time.time()
    ihm(Terrain,0)
    for i in range(nb_tours):
        tour(Terrain)
    ihm(Terrain,nb_tours)
    toc=time.time()
    print('la simulation a mis ' +str(toc-tic)+ ' secondes')
    
Generation=generation_terrain(100,100,10,10)
Terrain=Generation[0]
sylviculteurs=Generation[1]
bucherons=Generation[2]
#film(Terrain,800)
dessin(Terrain, 50)
