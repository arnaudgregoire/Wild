# -*- coding: utf-8 -*-
"""
Created on Wed Apr  6 14:38:54 2016

@author: Coline, Régis, Arnaud
"""
#import os
#os.chdir('C:\\Users\\Ariane\\Projet_info')
import random as rd
import matplotlib
matplotlib.use('Qt4Agg')
import matplotlib.pyplot as plt
import time
from humain import Sylviculteur, Bucheron
from terrain import Terrain
from eau import Eau
from foret import Foret
from foret_morte import Foret_morte
from foret_malade import Foret_malade
from plaine import Plaine
import numpy as np
import math

def generation_hum(nb_humains,type_classe,taille_x,taille_y,field):
    """
    method which create a list containing the human objects. They are randomly distributed on the map, except on the water.
    :param taille_x/y: integer which referts to the size of the map
    """
    humains=[]
    for i in range(nb_humains):
        x=rd.randint(0,taille_x-1)
        y=rd.randint(0,taille_y-1)
        while field[x][y].nature==0:
            x=rd.randint(0,taille_x-1)
            y=rd.randint(0,taille_y-1)
        humains=humains+[type_classe(x,y)]
    return(humains)

def tour(field,sylviculteurs,bucherons):
    """
    Method which runs a round, like a simulation with probabilities calculated in each method "maj" belonging to every class. 
    It updates the matrice which contains the objects (plaine ,eau , foret etc...)
    
    """
    #on met à jour tous les sylviculteurs
    for sylviculteur in sylviculteurs:
        sylviculteur.maj(field,4)
      #on met à jour tous les bucherons
    for bucheron in bucherons:
        bucheron.maj(field, 3)
        
    #on met à jour tous les objets du terrains
    for x in range(field.shape[0]):
        for y in range(field.shape[1]):
            field[x,y].maj(field)
    

    #La valeur des attributs nature_suivant détermine quelle classe s'applique à la case.        
    for x in range(field.shape[0]):
        for y in range(field.shape[1]):
            if field[x,y].nature!=field[x,y].nature_suivant:
                if field[x,y].nature_suivant==1:
                    field[x,y]=Plaine(x,y,field[x,y].presence)
                if field[x,y].nature_suivant==2 and field[x,y].nature==1:
                    field[x,y]=Foret(x,y,0,False)
                if field[x,y].nature_suivant==2 and field[x,y].nature==4:
                    field[x,y]=Foret(x,y,field[x,y].taille,field[x,y].presence)
                if field[x,y].nature_suivant==4:
                    field[x,y]=Foret_malade(x,y,field[x,y].taille,field[x,y].presence)
                if field[x,y].nature_suivant==3:
                    field[x,y]=Foret_morte(x,y,field[x,y].taille,field[x,y].presence) 
    #Nature_suivant reprend la valeur 9, qui sert de valeur tampon                
    for x in range(field.shape[0]):
        for y in range(field.shape[1]):
            if field[x,y].nature_suivant!=9:
                field[x,y].nature=field[x,y].nature_suivant
                field[x,y].nature_suivant=9


def ihm(field,sylviculteurs,bucherons,tours):
    """
    return a graphic showing the shape of the simulation 
    """
    ihm=np.zeros(field.shape)
    for x in range(field.shape[0]):
        for y in range(field.shape[1]):
            ihm[x,y]=field[x,y].couleur
    fig=plt.figure()
    plt.pcolormesh(ihm,cmap='brg')
    for sylviculteur in sylviculteurs:
        plt.plot(sylviculteur.y,sylviculteur.x,'o')
    for bucheron in bucherons:
        plt.plot(bucheron.y,bucheron.x,'*')
    return(fig)
    


        
        
def generation_terrain(taille_x,taille_y,nb_sylviculteurs,nb_bucherons):
    """
    Method which create a matrice with field objects (eau, plaine, etc...) 
    and uses two lists created by the method generation_hum (sylviculteur and bucheron).
    To create a coherent field, it uses noise.
    The shapes created are smoothed by bilinear interpolation, 
    then each case is discretised to make them correspond at each object
    """
    print('starting Map creation')
    start_gen=time.time()
    imgx = taille_x
    imgy = taille_y 
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
    mat_obj=np.array([[Plaine(x,y,False) for x in range(imgx)]for y in range(imgy)])
    #Les 3 valeurs de la matrice intermédiaire sont associés aux 3 classes terrains de départ (Eau, Plaine, Forêt)
    for y in range(imgy):
        for x in range(imgx):  
            if imgAr[y][x]==0:
                mat_obj[x][y]=Eau(x,y,False)
            if imgAr[y][x]==1.6:
                mat_obj[x][y]=Foret(x,y,0,False)
            if imgAr[y][x]==2:
                mat_obj[x][y]=Plaine(x,y,False)
    
    sylviculteurs=generation_hum(nb_sylviculteurs,Sylviculteur,taille_x,taille_y,mat_obj)
    bucherons=generation_hum(nb_bucherons,Bucheron,taille_x,taille_y,mat_obj)
    
    end_gen=time.time()
    print('Map created in ' +str(end_gen-start_gen)+'seconds')
    
    return(mat_obj,sylviculteurs,bucherons)
       
#
#def film(Map,nb_tours):
#    """
#    Méthode permettant de générer un film
#    """
#    fig=plt.figure()
#    plt.xlim(0,10)
#    plt.ylim(0,10)
#    FFMpegWriter = manimation.writers['ffmpeg']
#    metadata = dict(title='Movie Test', artist='Matplotlib',
#                    comment='Movie support!')
#    writer = FFMpegWriter(fps=15, metadata=metadata)
#    with writer.saving(fig, "wild.mp4", 100):
#        for i in range(nb_tours):
#            tour(Map, sylviculteurs, bucherons, nature_case)
#            ihm=np.zeros(Map.shape)
#            for x in range(Map.shape[0]):
#                for y in range(Map.shape[1]):
#                    ihm[x,y]=Map[x,y].nature
#            plt.pcolor(ihm, cmap='brg')
#            writer.grab_frame()
#
#def dessin(field,nb_tours):
#    """
#    Renvoie l'état de la simulation après nb_tours
#    """
#    tic=time.time()
#    ihm(field,sylviculteurs,bucherons,tour)
#    for i in range(nb_tours):
#        print('start Round '+str(i))
#        start_tour=time.time()
#        tour(field, sylviculteurs, bucherons)
#        end_tour=time.time()
#        print('End Round ' +str(i))
#        print('Round done in '+str(end_tour-start_tour)+' seconds')
#        if i>nb_tours-10:
#            ihm(field,sylviculteurs, bucherons, i)
#    ihm(field,sylviculteurs, bucherons, nb_tours)
#    toc=time.time()
#    print('la simulation a mis ' +str(toc-tic)+ ' secondes')
    
#Generation=generation_terrain(100,100,10,10)
#field=Generation[0]
#sylviculteurs=Generation[1]
#bucherons=Generation[2]
#dessin(field,10)