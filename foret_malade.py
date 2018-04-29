# -*- coding: utf-8 -*-
"""
Created on Wed Apr  6 14:09:58 2016

@author: Coline, Régis, Arnaud
"""

from terrain import Terrain
import random as rd

class Foret_malade(Terrain): 
    """
    Inherit from the superclass Terrain
    :param nature: integer which establish nature of the case  (0:Eau, 1:Plaine, 2:Forêt, 3:Forêt_morte, 4:Forêt_malade )
    :param nature_suivant:integer qwhich establish nature of the case for the next round
    :param couleur:integer useful for the graphic interface
    :param taille:integer in the range [0,30]
    :param duree: integer in the range [0,3]
    :param soin: boolean which indicate if a forester is on the case, which mean he can heal the disease
    """
    def __init__(self,x,y,taille,presence):
         """
         Constructor in the class : Foret_malade
         """
         self.nature=4
         self.nature_suivant=9
         self.taille=taille
         self.duree=3
         self.soin=False
         self.couleur=1.4
         #Constructor call of the super class 
         super(Foret_malade,self).__init__(x,y,presence)

    def maj(self,field):
        """
        If duree=0, the sick forest dies and become dead forest.
        As long as forest is sick (durée !=0) it can contaminate other cases if their nature=2 
        with a chance of 50% every round.
        If there is a forester on the case (soin=True), nature_suivant=2.
        """
        if self.duree==0:
            self.nature_suivant=3
        else:
            self.nature_suivant=4
        
        if self.duree>0:
            for i in [self.x-1,self.x,self.x+1]:
                for j in [self.y-1,self.y,self.y+1]:
                    if i>=0 and i<field.shape[0] and j>=0 and j<field.shape[1]:
                        if field[i,j].nature==2:
                            if rd.randint(0,100)>50:
                                field[i,j].nature_suivant=4

            self.nature_suivant=4
            self.duree=self.duree-1
        else:
            self.nature_suivant=3
        if self.soin==True:
            self.nature_suivant=2
