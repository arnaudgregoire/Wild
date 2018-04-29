#import os
#os.chdir('C:\\Users\\Ariane\\Desktop\\Projet_info2')
import sys
from PyQt4 import QtGui, QtCore
from main import generation_terrain,ihm,tour
import numpy as np
import matplotlib
matplotlib.use('Qt4Agg')
#import pylab
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt



class Example(QtGui.QWidget):
    
    def __init__(self):
        super(Example, self).__init__()
        self.initUI()
        
    def initUI(self): 
        self.setWindowIcon(QtGui.QIcon('icon.png'))
        self.icon=QtGui.QLabel()
        self.icon.setPixmap(QtGui.QPixmap('icon.png'))

        btn_gen = QtGui.QPushButton('Generate Map', self)
        btn_gen.resize(btn_gen.sizeHint())
        btn_gen.clicked.connect(self.clic_gen)
        
        start_gen = QtGui.QPushButton('Start Simulation !', self)
        start_gen.resize(btn_gen.sizeHint())
        start_gen.clicked.connect(self.start_gen)
        
        self.lcd_taille = QtGui.QLCDNumber(self)
        self.sld_taille = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        self.sld_taille.valueChanged.connect(self.lcd_taille.display)
        self.sld_taille.setRange(10,200)
        self.label_taille = QtGui.QLabel('Taille de la simulation', self)

        self.lcd_sylv = QtGui.QLCDNumber(self)
        self.sld_sylv = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        self.sld_sylv.valueChanged.connect(self.lcd_sylv.display)
        self.sld_sylv.setRange(0,5)
        self.label_sylv = QtGui.QLabel('nombre de sylviculteurs', self)
        
        self.lcd_buch = QtGui.QLCDNumber(self)
        self.sld_buch = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        self.sld_buch.valueChanged.connect(self.lcd_buch.display)
        self.sld_buch.setRange(0,5)
        self.label_buch = QtGui.QLabel('nombre de bucherons', self)
        
        self.hbox = QtGui.QHBoxLayout(self)
        self.hbox.addStretch(1)
        self.fig = Figure(figsize=(100,100))
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvas(self.fig)
        self.hbox.addWidget(self.canvas)
        self.splitter1=QtGui.QSplitter(QtCore.Qt.Vertical)
        self.splitter1.addWidget(self.icon)
        self.splitter1.addWidget(btn_gen)
        self.splitter1.addWidget(start_gen)
        self.hbox.addWidget(self.splitter1)
        self.vbox = QtGui.QVBoxLayout()
        self.vbox.addWidget(self.label_taille)
        self.vbox.addWidget(self.lcd_taille)
        self.vbox.addWidget(self.sld_taille)
        self.vbox.addWidget(self.label_sylv)
        self.vbox.addWidget(self.lcd_sylv)
        self.vbox.addWidget(self.sld_sylv)
        self.vbox.addWidget(self.label_buch)
        self.vbox.addWidget(self.lcd_buch)
        self.vbox.addWidget(self.sld_buch)
        self.hbox.addLayout(self.vbox)
        self.setLayout(self.hbox)
        
        self.setGeometry(50, 50, 900, 500)
        self.setWindowTitle('GUI Project The Wild')
        self.show()        
 
    def clic_gen(self):
        self.ax.clear()
        self.fig = Figure(figsize=(100,100))
        Generation=generation_terrain(int(self.lcd_taille.value()),int(self.lcd_taille.value()),int(self.lcd_sylv.value()),int(self.lcd_buch.value()))
        self.Map=Generation[0]
        self.sylviculteurs=Generation[1]
        self.bucherons=Generation[2]
        ihm=np.zeros(self.Map.shape)
        for x in range(self.Map.shape[0]):
            for y in range(self.Map.shape[1]):
                ihm[x,y]=self.Map[x,y].couleur
        self.ax.pcolormesh(ihm,cmap='brg')
        for sylviculteur in self.sylviculteurs:
            self.ax.plot(sylviculteur.y,sylviculteur.x,'o')
        for bucheron in self.bucherons:
            self.ax.plot(bucheron.y,bucheron.x,'*')
        self.canvas.draw()

    def start_gen(self):
        clearLayout(self.hbox)
        self.hbox.addStretch(1)
        self.fig = Figure(figsize=(100,100))
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvas(self.fig)
        ihm=np.zeros(self.Map.shape)
        for x in range(self.Map.shape[0]):
            for y in range(self.Map.shape[1]):
                ihm[x,y]=self.Map[x,y].couleur
        self.ax.pcolormesh(ihm,cmap='brg')
        for sylviculteur in self.sylviculteurs:
            self.ax.plot(sylviculteur.y,sylviculteur.x,'o')
        for bucheron in self.bucherons:
            self.ax.plot(bucheron.y,bucheron.x,'*')
        self.canvas.draw()
        
        btn_tour = QtGui.QPushButton('Start Round', self)
        btn_tour.resize(btn_tour.sizeHint())
        btn_tour.clicked.connect(self.start_round)
        
        self.hbox.addWidget(self.canvas)
        self.icon=QtGui.QLabel()
        self.icon.setPixmap(QtGui.QPixmap('icon.png'))
        self.splitter1=QtGui.QSplitter(QtCore.Qt.Vertical)
        self.splitter1.addWidget(self.icon)
        self.splitter1.addWidget(btn_tour)
        self.hbox.addWidget(self.splitter1)

        
    def start_round(self):
        self.ax.clear()
        print('début tour')
        tour(self.Map,self.sylviculteurs,self.bucherons)
        print('fin tour')
        ihm=np.zeros(self.Map.shape)
        for x in range(self.Map.shape[0]):
            for y in range(self.Map.shape[1]):
                ihm[x,y]=self.Map[x,y].couleur
        self.ax.pcolormesh(ihm,cmap='brg')
        for sylviculteur in self.sylviculteurs:
            self.ax.plot(sylviculteur.y,sylviculteur.x,'o')
        for bucheron in self.bucherons:
            self.ax.plot(bucheron.y,bucheron.x,'*')
        self.canvas.draw()
                
        

def clearLayout(layout):
    if layout != None:
        while layout.count():
            child = layout.takeAt(0)
            if child.widget() is not None:
                child.widget().deleteLater()
            elif child.layout() is not None:
                clearLayout(child.layout())        
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()