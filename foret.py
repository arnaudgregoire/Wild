# -*- coding: utf-8 -*-
"""
Created on Wed Apr  6 14:15:14 2016

@author: Coline, Régis, Arnaud
"""
from terrain import Terrain
import random as rd

class Foret(Terrain):
    """
    Inherit from the superclass Terrain
    :param nature: integer which establish nature of the case  (0:Eau, 1:Plaine, 2:Forêt, 3:Forêt_morte, 4:Forêt_malade )
    :param nature_suivant:integer qwhich establish nature of the case for the next round
    :param taille:integer in the range [0,30]
    :param couleur:integer useful for the graphic interface
    """
    def __init__(self,x,y,taille):
        """
        Constructor in the class : Eau
        """
        self.nature=2
        self.nature_suivant=9
        self.taille=0
        self.couleur=1.8
        #Constructor call of the super class 
        super(Foret,self).__init__(x,y)
        
    def maj(self, field):
        """
        Method which modify the attribute taille, by making it growth by one every round until taille=30.
        If forest is next to a case water ( where the attribute nature=0), its attribute taille growth by 2 every round.
        From the attribut taille of 15, forest can settle one case by round around if their attribute nature=1 (plaines) 
        Forest has 0,01% of hazard to develop desease every round.
        """
        A=True
        eau_voisin=False
        for i in [self.x-2,self.x-1,self.x,self.x+1,self.x+2]:
            for j in [self.y-2,self.y-1,self.y,self.y+1,self.y+2]:
                if i>=0 and i<field.shape[0] and j>=0 and j<field.shape[1]:
                    if field[i,j].nature==0:
                        eau_voisin=True
        if eau_voisin==True and self.taille<30:
            self.taille=self.taille+1
        a=0
        if self.taille<30:
            self.taille=self.taille+1
        if self.taille>15:
            for i in [self.x-1,self.x,self.x+1]:
                for j in [self.y-1,self.y,self.y+1]:
                    if i>=0 and i<field.shape[0] and j>=0 and j<field.shape[1] and a<=1:
                        if field[i,j].nature==1:
                            if rd.randint(0,100)>20:
                                field[i,j].nature_suivant=2
        while A==True:
            if rd.uniform(0,100)>99.99:
                self.nature_suivant=4
            if self.nature_suivant==9:
                self.nature_suivant=2
            A=False
        self.couleur=1.8-(0.2/30)*self.taille