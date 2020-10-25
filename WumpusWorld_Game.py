import pygame
import pygame_gui
import random
from map_cell import *

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------
        # ***** GAME WINDOW INITIALIZATION  ******
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------
WHITE = (255,255,255)
GREY = (128, 128, 128)
WIN_X = 800
WIN_Y = 600
GAME_X = WIN_Y
pygame.init()
pygame.display.set_caption('WUMPUS WORLD GAME')
WINDOW = pygame.display.set_mode((WIN_X, WIN_Y))
background = pygame.Surface((WIN_X, WIN_Y))
#background.fill(WHITE)
manager = pygame_gui.UIManager((WIN_X, WIN_Y))
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------
        # ***** GAME GRID FUNCTIONS  ******
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------
class Grid:
    def __init__(self, dimension_mod):
        self.grid = []
        self.axis_dim = 3*dimension_mod

#--------------------------------------------------------------------
    def init_grid(self):
        gap = GAME_X // self.axis_dim
        print(self.axis_dim/3-1)
        #row
        total_spots=list(range(0, self.axis_dim))
        hole_locations=None
        for i in range(self.axis_dim):
            self.grid.append([])
            #column
            if(i!=0 and i!=self.axis_dim-1):
                hole_locations=random.sample(total_spots,int(self.axis_dim/3-1))
            for j in range(self.axis_dim):

                
                if(i==0):
                    cell=Cell(j,i,gap,self.axis_dim,Ctype((j%3)+4))
                elif(i==self.axis_dim-1):
                    cell = Cell(j,i, gap,self.axis_dim, Ctype((j%3)+1))
                else:
                    cell=Cell(j,i,gap,self.axis_dim,Ctype.EMPTY)
                self.grid[i].append(cell)
            
        return self.grid
#--------------------------------------------------------------------
#------------------------------------------------------------------------------
    def draw_map(self):
        gap=GAME_X//self.axis_dim
        #print(gap)
        win = background
        for row in self.grid:
            for cell in row:
                cell.draw(win)
        pygame.display.update()




# ------------------------------------------------------------------------------------------------------------------------------------------------------------------
        # ***** GAME LOOP ******
        # For testing purposes mainly
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------
clock = pygame.time.Clock()
is_running = True
grid=Grid(2)
grid.init_grid()
#print(grid.grid[5][1].ctype)
grid.draw_map()
while is_running:
 time_delta = clock.tick(60)/1000.0
 for event in pygame.event.get():
     if event.type == pygame.QUIT:
         is_running = False

     manager.process_events(event)

 manager.update(time_delta)

 WINDOW.blit(background, (0, 0))
 manager.draw_ui(WINDOW)

 pygame.display.update()
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------
