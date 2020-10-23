import pygame
from enum import Enum

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class Ctype(Enum):
    MAGE=1
    WUMPUS=2
    KNIGHT=3
    CPUMAGE=4
    CPUWUMPUS=5
    CPUKNIGHT=6
    HOLE=7
    EMPTY=8

class Cell:
    def __init__(self, col,row,size, totalDimensions,ctype):
        self.col=col
        self.row=row
        self.size=size
        self.x=col*size
        self.y=row*size
        self.ctype=ctype
        self.selected=False


    #Called when a cell is clicked on, 
    def set_selected(self,tf):
        self.selected=tf

    def set_ctype(self,ctype):
        self.ctype=ctype


    def draw(self,win):
        print('draw')
        #Edit this based on what the cell currently contains
        #pygame.draw.rect(win,BLACK,(self.x,self.y,self.size,self.size))
        pygame.draw.rect(win,WHITE,(self.x+(self.size/10),self.y+(self.size/10),self.size-(self.size/5),self.size-(self.size/5)))
        # pygame.draw.rect(win,,(self.x,self.y,self.size,self.size))
        