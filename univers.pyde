#Projet : coder un algorithme de sélection pour retirer les objets trop éloignés d'un objet dont on étudie la position.
#Projet : mettre tout ça en 3 dimensions
#Projet : faire spawn les objets en cercle
#Projet : réduire le pas de temps
#Projet : donner une vitesse circulaire initiale
#Projet : faire spawn les objets selon une sphère
#Projet : installer un système de matrice 3x3 tel que position, vitesse, accélération
#Projet : diviser l'espace en plusieurs secteurs avec un poids en fonction de la distance par raport à l'étoile étudiée
#Projet : importer fichiers pythons

from random import *
from math import *
import copy
add_library('peasycam')

width = 1920
height = 1080

#Initialisation de la fenêtre
def setup():
    fullScreen(1)
    size(width,height,P3D)
    cam = PeasyCam(this, 2000)
    fill(255)
    noStroke()
        
al = 9.461*10**15         # Valeur d'une année lumière
facteur = 10**(-2)        # Facteur d'échelle
    
# Convertisseurs unités -> mètres
def u_to_m(d, f=facteur):
    return (d*al)/f

# Convertisseurs mètres -> unités
def m_to_u(d, f=facteur):
    return (d*f)/al
        
#Création d'un corps
class Body():
    
    def __init__(self, distance, speed, inclination, mass):
        self.posx = distance*cos(inclination)
        self.posy = distance*sin(inclination)
        self.posz = 0
        self.vx = 0
        self.vy = speed
        self.vz = 0
        self.ax = 0
        self.ay = 0
        self.az = 0
        self.m = mass
        
    def getX(self):
        return self.posx
    
    def getY(self):
        return self.posy
    
    def getZ(self):
        return self.posz
    
    def getVx(self):
        return self.vx
    
    def getVy(self):
        return self.vy
    
    def getVz(self):
        return self.vz
    
    def getAx(self):
        return self.ax
    
    def getAy(self):
        return self.ay
    
    def getAz(self):
        return self.az
    
    def getM(self):
        return self.m
    
    def setX(self, dx):
        self.posx = dx
        
    def setY(self, dy):
        self.posy = dy
        
    def setZ(self, dz):
        self.posz = dz
        
    def setVx(self, vx):
        self.vx = vx
        
    def setVy(self, vy):
        self.vy = vy
    
    def setVz(self, vz):
        self.vz = vz
    
    def setAx(self, ax):
        self.ax = ax
        
    def setAy(self, ay):
        self.ay = ay
        
    def setAz(self, az):
        self.az = az
        
    def setM(self, dm):
        self.m = dm
        
    def getDistance(self, object):
        return sqrt((self.getX()-object.getX())**2 + (self.getY()-object.getY())**2 + (self.getZ()-object.getZ())**2 + 30000)
    
    def calculNewPos(self, objects, t, G = 6.67*10**(-11)):
        
        Ax, Ay, Az = 0, 0, 0

        for object in objects:
            champ = object.getM()*G/u_to_m(self.getDistance(object))**3
            Ax += champ*(object.getX()-self.getX())
            Ay += champ*(object.getY()-self.getY())
            Az += champ*(object.getZ()-self.getZ())
            
        self.setX((1/2)*Ax*(t**2) + self.getVx()*t + self.getX())
        self.setY((1/2)*Ay*(t**2) + self.getVy()*t + self.getY())
        self.setZ((1/2)*Az*(t**2) + self.getVz()*t + self.getZ())
        
        self.setVx(Ax*t + self.getVx())
        self.setVy(Ay*t + self.getVy())
        self.setVz(Az*t + self.getVz())
        
        self.setAx(Ax)
        self.setAy(Ay)
        self.setAz(Az)   
        
def getAngle(x, y):
        
    if x > 0 and y > 0:
        return atan(y/x)
    elif x < 0 and y > 0:
        return atan(-x/y)+PI/2
    elif x < 0 and y < 0:
        return atan(-y/-x)+PI
    elif x > 0 and y < 0:
        return atan(x/-y)+3*PI/2
    else:
        return 0

objects_ = []
v_value = 0.45
dmax = m_to_u(52850*al)
imax = PI

for i in range(10):
    
    r = uniform(0, dmax)
    inclination = uniform(-imax, imax)
    speed = 0
    mass = randint(1, 3000)*2**29
    
    objects_.append(Body(r, speed, inclination, mass))
    
"""
    r = uniform(0, dmax)
    alpha = uniform(0, 2*PI)
    beta = uniform(0, 2*PI)
    #x, y, z = r*cos(alpha)*cos(beta), r*cos(alpha)*sin(beta), r*sin(alpha)
    x, y, z = r*cos(alpha), r*sin(alpha), randint(-5, 5)
    
    theta = float(getAngle(x, y)+v_angle)
    speed = v_value*(r/dmax)
    
    vx, vy, vz = speed*cos(theta), speed*sin(theta), 0
    #vx, vy, vz = 0, 0, 0
    objects_.append(Body(x, y, z, vx, vy, vz))
"""

#Temps
step = 3600*24*365*100000
increase_step_value = 1.5

points_ = [[] for i in range(len(objects_))]
showmiddle = False
showpath = False

def draw():
    global points_
    background(0)
    lights()
    
    for object in objects_:
        list_ = copy.copy(objects_)
        list_.remove(object)
        object.calculNewPos(list_, step)
                
    """
    i = 0
    newstep = step/1
    while i <= step:

        for object in objects_:
            list_ = copy.copy(objects_)
            list_.remove(object)
            object.calculNewPos(list_, newstep)
            
        i+=newstep
    """
    for object in objects_:
        stroke(255)
        point(object.getX(), object.getY(), object.getZ())
        #push()
        #translate(object.getX(), object.getY(), object.getZ())
        #sphere(0.5)
        #pop()
    
        points_[objects_.index(object)].append((object.posx, object.posy, object.posz))
        
    if showpath:
        showpaths(points_)
        
def keyPressed():
    global showpath, step

    if key == 'p':
        showpath = False if showpath else True
    if key == 'o':
        step = 0
    if keyCode == UP:
        step += increase_step_value
    if keyCode == DOWN:
        if step-increase_step_value > 0:
            step -= increase_step_value
        else:
            step = 0
    if keyCode == RIGHT:
        for object in objects_:
            object.setM(object.getM()*10)
    if keyCode == LEFT:
        for object in objects_:
            object.setM(object.getM()/10)
    
def showpaths(listpoints_):
    stroke(255)
    noFill()
    for i in range(len(listpoints_)):
        beginShape()
        for o in range(len(listpoints_[i])):
            vertex(listpoints_[i][o][0], listpoints_[i][o][1], listpoints_[i][o][2])
        endShape()
