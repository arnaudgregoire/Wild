# -*- coding: utf-8 -*-
"""
Created on Wed Apr  6 14:03:41 2016

@author: Coline, Régis, Arnaud
"""
from terrain import Terrain

class Plaine(Terrain):
    """
    Inherit from the superclass Terrain
    :param nature: integer which establish nature of the case  (0:Eau, 1:Plaine, 2:Forêt, 3:Forêt_morte, 4:Forêt_malade )
    :param nature_suivant:integer qwhich establish nature of the case for the next round
    :param couleur:integer useful for the graphic interface
    :param germe: boolean which indicates if there is any sylviculteur on the case
    """
    def __init__(self,x,y,presence):
        self.nature=1
        self.nature_suivant=9
        self.germe=False
        self.couleur=2
    #appel du constructeur de la classe parente
        super(Plaine,self).__init__(x,y,presence)
    
    def maj(self,field):
        """
        Method for the class Plaine which modify nature_suivant :
        Here, the value will always be 1 except if there is a forester on the case (germe=True) : nature_suivant=3
        or if the method maj in the class Foret makes nature_suivant=3
        """
        if self.nature_suivant==9:
            self.nature_suivant=1
        if self.germe==True:
            self.nature_suivant=2