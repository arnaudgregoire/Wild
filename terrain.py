# -*- coding: utf-8 -*-
"""
Created on Wed Mar 30 09:37:10 2016

@author: Coline, Régis, Arnaud
"""
import numpy as np
import time
import math 
#matplotlib.use("Agg")
#import matplotlib
#import matplotlib.animation as manimation
import matplotlib.pyplot as plt
import random as rd


class Terrain(object):
    """ 
    Superclass of all the ground types (Eau, plaine, foret, foret_morte,  foret_malade)
    """
    def __init__(self,x,y):
        """
        :param x/y: give the coodonates x/y of one case
        """
        self.x=x
        self.y=y
        self.presence=False
    
    def __repr__(self):
        return(str(self.nature)+str(self.nature_suivant))

    @property
    def id(self):
        return self.nature
        
    def __str__(self):
        coordonnées="({},{})".format(self.x,self.y)
        return coordonnées

    def maj(self):
        NotImplementedError
    
