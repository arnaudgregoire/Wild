# -*- coding: utf-8 -*-
"""

@author: Coline, Régis, Arnaud
"""
from terrain import Terrain

class Eau(Terrain):
    """
    Inherit from the superclass Terrain
    :param nature: integer which establish nature of the case  (0:Eau, 1:Plaine, 2:Forêt, 3:Forêt_morte, 4:Forêt_malade )
    :param nature_suivant:integer qwhich establish nature of the case for the next round
    :param couleur:integer useful for the graphic interface
    """
    def __init__(self,x,y): 
        """
        Constructor in the class : Eau
        """
        self.nature=0
        self.nature_suivant=9
        self.couleur=0
    #Constructor call of the super class  
        super(Eau,self).__init__(x,y)
    
    def maj(self,field):
        """
        Method for the class Eau which modify nature_suivant :
        Here, the value will always be 0.
        """
        self.nature_suivant=0