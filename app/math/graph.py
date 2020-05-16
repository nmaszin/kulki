import pygame
import pygame.gfxdraw
import math
from app.simulation.simulation import Simulation
from app.math.point import Point
from app.math.vector import Vector
from app.math.rectangle import Rectangle
from app.math.matrix import TransformationMatrix
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style

def average(tab_of_coordinates):
    sum_distance=0
    for id in range(len(tab_of_coordinates)-1):
        sum_distance+=Math.sqrt(((tab_of_coordinates[id][0]-tab_of_coordinates[id+1][0])**2+(tab_of_coordinates[id+1][1]-tab_of_coordinates[id+1][1])**2))
    return sum_distance/(len(tab_of_coordinates-1))

class Graph:
    # obecnie tylko wykres sredniej drogi miedzy zderzeniami
    def __init__(self,start,stop):
        self.start=start
        self.stop=stop
        self.coordinates=[]
        self.x_axis=[]
        self.y_axis=[]
    
    def update_graph(self,index, tab_of_coordinates):
        self.coordinates[index].append(tab_of_coordinates)
        self.x_axis.append(index)
        self.y_axis.append(average(tab_of_coordinates))