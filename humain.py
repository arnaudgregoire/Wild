# -*- coding: utf-8 -*-
"""
Created on Wed Apr  6 09:57:39 2016

@author: Coline, Régis, Arnaud
"""

import numpy as np
#import matplotlib
#matplotlib.use("Agg")
#import matplotlib.pyplot as plt
#import matplotlib.animation as manimation
import random as rd
import math
import time



def distance(x1,x2,y1,y2):
    """
    Method which return the cartesian distance between 2 points
    """
    return(np.sqrt((x2-x1)**2+(y2-y1)**2))
    

        
class Humain(object):
    """
    superclass which contains the AI moving on the map
    :param x,y : position of the case where is the element
    """
    def __init__(self,x,y):
        self.x=x
        self.y=y
        
    def maj(self, field, nature_case):
        """
        method which makes moving the AI and allows them to interact with the cases they are on
        :param nature_case:integer wich indicate if the case is Foret_malade or Foret_morte
        """
        Lx=[]
        Ly=[]
        L_krank=[]
        min=[]
        min_choix=[]
        dist_min=0
        for i in [self.x-2,self.x-1,self.x,self.x+1,self.x+2]:
            for j in [self.y-2,self.y-1,self.y,self.y+1,self.y+2]:
                if i>=0 and i<field.shape[0] and j>=0 and j<field.shape[1] and field[i,j].nature!=0 and [i,j]!=[self.x,self.y] and field[self.x,self.y].presence==False:
                    Lx=Lx+[i]
                    Ly=Ly+[j]
        for i in [self.x-1,self.x,self.x+1]:
            for j in [self.y-1,self.y,self.y+1]:
                if i>=0 and i<field.shape[0] and j>=0 and j<field.shape[1] and field[i,j].nature==0 and field[self.x,self.y].presence==False:
                    Lx=Lx+[i]
                    Ly=Ly+[j]
        #on trouve les cases forêts malades/mortes
        for x in range(field.shape[0]):
            for y in range(field.shape[1]):
                if field[x,y].nature==nature_case:
                    L_krank=L_krank+[[x,y]]
        
        #on trouve la plus proche de notre humain
        if L_krank==[]:
            pass
        else:
            min=L_krank[0]
            dist_min=distance(L_krank[0][0],self.x,L_krank[0][1],self.y)
            for i in range(len(L_krank)-1):
                if distance(L_krank[i][0],self.x,L_krank[i][1],self.y)<dist_min:
                    min=L_krank[i]
                    dist_min=distance(L_krank[i][0],self.x,L_krank[i][1],self.y)
        #on regarde quel déplacement le rapproche le plus de la case malade/morte
            min_choix=[Lx[0],Ly[0]]
            dist_min=distance(Lx[0],min[0],Ly[0],min[1])
            for x in Lx:
                for y in Ly:
                    if distance(x,min[0],y,min[1])<dist_min:
                        min_choix=[x,y]
                        dist_min=distance(min_choix[0],min[0],min_choix[1],min[1])
            # on déplace le sylviculteur en changeant ses coordonnées
            field[self.x,self.y].presence=False
            self.x=min_choix[0]
            self.y=min_choix[1]
            field[self.x,self.y].presence=True
        
        
class Sylviculteur(Humain):
    """
    Subclass of the class "Humain". Can cure diseases and make forest grows on "plaine" case. Move by one case each round
    only if there is some illness to cure.
    
    """
    
    def __init__(self,x,y):
        self.identif=5
        super(Sylviculteur,self).__init__(x,y)
        
                
    def maj(self, field, nature_case):
        """
        Method which allows the AI to plant forests and cure ill forests. Inherits from the method maj in the class "Humain".
        """
        #on regroupe dans Lx et Ly les cases où le sylviculteur peut potentiellement se déplacer
        #L_krank : liste des forêts malades sur la carte
        super(Sylviculteur,self).maj(field, nature_case)
        # S'il est sur une case Plaine, il fait germer une forêt
        if field[self.x,self.y].nature==1:
            field[self.x,self.y].germe=True
        #S'il est sur une case forêt malade, il la soigne
        if field[self.x,self.y].nature==4:
            field[self.x,self.y].soin=True
            
class Bucheron(Humain):
    """
    Subclass of the class "Humain". Can cut dead forests, which means transform "foret morte" cases in "plaine" cases.
    Move by one case each round only if there is some dead forest to cut. 
    """
    
    def __init__(self,x,y):
        self.identif=6
        super(Bucheron,self).__init__(x,y)
        
                
    def maj(self, field, nature_case):
        """
        Method which allows the AI to cut dead forests. Inherits from the method maj in the class "Humain"
        
        """
        #on regroupe dans Lx et Ly les cases où le sylviculteur peut potentiellement se déplacer
        #L_krank : liste des forêts malades sur la carte
        super(Bucheron,self).maj(field,nature_case)
        
        # S'il est sur une case forêt morte, il La coupe
        if field[self.x,self.y].nature==3:
            field[self.x,self.y].coupe=True
            
