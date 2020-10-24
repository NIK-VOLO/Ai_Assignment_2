import pygame
from enum import Enum

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED=(255,0,0)
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
        self.outerRect=pygame.Rect(self.x,self.y,self.size,self.size)
        self.innerRect=pygame.Rect(self.x+(self.size/12),self.y+(self.size/12),self.size-(self.size/6),self.size-(self.size/6))
        #self.font = pygame.font.SysFont(NONE, 12)


    #Called when a cell is clicked on, 
    def set_selected(self,tf):
        self.selected=tf

    def set_ctype(self,ctype):
        self.ctype=ctype

    def get_type_text(self):
        t=self.ctype
        if(t==Ctype.CPUKNIGHT):
            return 'CPUK'
        elif(t==Ctype.CPUMAGE):
            return 'CPUM'
        elif(t==Ctype.CPUWUMPUS):
            return 'CPUW'
        elif(t==Ctype.MAGE):
            return "PM"
        elif(t==Ctype.KNIGHT):
            return "PK"
        elif(t==Ctype.WUMPUS):
            return 'PW'
        elif(t==Ctype.HOLE):
            return 'HOLE'
        else:
            return ''
    def draw(self,win):
        print('draw')
        font=pygame.font.SysFont(None,20)
        text=font.render(f'Test{self.get_type_text()}',True,RED)
        innerRect = text.get_rect(center=self.innerRect.center)
        #Edit this based on what the cell currently contains
        pygame.draw.rect(win,BLACK,(self.x,self.y,self.size,self.size))
        pygame.draw.rect(win,WHITE,(self.x+(self.size/12),self.y+(self.size/12),self.size-(self.size/6),self.size-(self.size/6)))
        win.blit(text,innerRect)
        # pygame.draw.rect(win,,(self.x,self.y,self.size,self.size))
        