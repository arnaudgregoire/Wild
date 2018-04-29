# -*- coding: utf-8 -*-
"""
Created on Wed Apr  6 14:05:31 2016

@author: Coline, Régis, Arnaud
"""
from terrain import Terrain

class Foret_morte(Terrain):
    """
    Inherit from the superclass Terrain
    :param nature: integer which establish nature of the case  (0:Eau, 1:Plaine, 2:Forêt, 3:Forêt_morte, 4:Forêt_malade )
    :param nature_suivant:integer qwhich establish nature of the case for the next round
    :param couleur:integer useful for the graphic interface     
    :param taille:integer in the range [0,30]
    :param coupe: boolean which indicate if a lumberjack is on the case, which mean he can cut the forest
    """
    def __init__(self,x,y,taille):
        """
        Constructor in the class : Foret_morte
        """
        self.nature=3
        self.nature_suivant=9
        self.taille=taille
        self.coupe=False
        self.couleur=1.2
        super(Foret_morte,self).__init__(x,y)
    
    def maj(self,field):
        """
        Every round, the attribute taille decreases of one.
        If taille=0 or if coupe=True, nature_suivant=1(plaine)
        """
        if self.taille==0 or self.coupe==True:
            self.nature_suivant=1
        else:
            self.taille=self.taille-1
            self.nature_suivant=3