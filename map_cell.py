import pygame
from enum import IntEnum

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED=(255,0,0)
BLUE=(0,0,255)
PURPLE=(128,0,128)
class Ctype(IntEnum):
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
        self.innerRect=pygame.Rect(self.x+2,self.y+2,self.size-1,self.size-1)
        #self.font = pygame.font.SysFont(NONE, 12)


    def contains_piece(self,other):
        return self.ctype<7

    def __str__(self):
        return f'({self.col},{self.row}),{self.get_type_text()}'
    #Called when a cell is clicked on,
    def set_selected(self,tf):
        self.selected=tf

    def set_ctype(self,ctype):
        self.ctype=ctype


    #-------------------------------------------------------
    # Does not change selected (boolean) or the ctype in the cell.
    # Have to do that in grid to store information on how many of each type of piece are left
    # Returns:
    # 0 if no piece dies,
    # -1 if self piece dies,
    # 1 if cell2 dies,
    # -2 if both pieces die
    # -3 if move is not allowed
    # -4 Means that the first piece selected was not a player or cpu piece, so probably a bug with the program
    #-------------------------------------------------------
    def fight(self,cell2):
        if not (self.row in range(cell2.row-1,cell2.row+2) and self.col in range(cell2.col-1,cell2.col+2)):
            print('Invalid Move cell range')
            return -3
        #Self piece is a player piece
        if(1<=self.ctype<=3):
            if cell2.ctype==Ctype.EMPTY:
                return 0
            elif cell2.ctype==Ctype.HOLE:
                return -1
            elif (1<=cell2.ctype<=3):
                print('Invalid Move pvp')
                return -3
            else:
                id=self.ctype+3-cell2.ctype
                if(id==0):
                    print('Both die')
                    return -2
                #cell2 piece dies
                elif(id==1 or id==-2):
                    return 1
                #cell1 piece dies
                else:
                    return -1

        # Self piece is a cpu piece
        elif 4<self.ctype<=6:
            if cell2.ctype==Ctype.EMPTY:
                return 0
            elif cell2.ctype==Ctype.HOLE:
                return -1
            elif (4<=cell2.ctype<=6):
                print('Invalid Move cpu v.cpu')
                return -3
            else:
                id=self.ctype-3-cell2.ctype
                if(id==0):
                    print('Both die')
                    return -2
                #cell2 piece dies
                elif(id==1 or id==-2):
                    return 1
                #cell1 piece dies
                else:
                    return -1
        # Probably a bug
        else:
            print('BUG?')
            return -4
    def get_type_text(self):
        t=self.ctype
        if(t==Ctype.CPUKNIGHT):
            return 'CPUH'
        elif(t==Ctype.CPUMAGE):
            return 'CPUM'
        elif(t==Ctype.CPUWUMPUS):
            return 'CPUW'
        elif(t==Ctype.MAGE):
            return "PM"
        elif(t==Ctype.KNIGHT):
            return "PH"
        elif(t==Ctype.WUMPUS):
            return 'PW'
        elif(t==Ctype.HOLE):
            return 'HOLE'
        else:
            return ''
    def draw(self,win):

        font=pygame.font.SysFont(None,20)
        if(self.ctype in range(4,7)):
            mainColor=BLUE
        elif self.ctype in range(1,4):
            mainColor=RED
        else:
            mainColor=BLACK
        if(self.selected):
            mainColor=PURPLE
        text=font.render(f'{self.get_type_text()}',True,mainColor)
        innerRect=text.get_rect(center=self.innerRect.center)
        #innerRect.fill(WHITE)
        win.fill(WHITE,self.innerRect)
        win.blit(text,innerRect)
        # pygame.draw.rect(win,,(self.x,self.y,self.size,self.size))
