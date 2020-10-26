import pygame
import pygame_gui
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
    def draw_grid_lines(self, window, axis_dim, size_x, size_y):
        # gap = size_y // cols
        gap = size_x // axis_dim
        for i in range(axis_dim):
            # DRAWS HORIZONTAL LINES:
            pygame.draw.line(window, GREY, (0, i * gap), (size_y, i * gap))
            for j in range(axis_dim):
                # DRAWS VERTICAL LINES:
                pygame.draw.line(window, GREY, (j * gap, 0), (j * gap, size_x))
#------------------------------------------------------------------------------
    def draw_map(self):
        gap=GAME_X//self.axis_dim
        print(gap)
        win = WINDOW
        cell=Cell(0,0,gap,1,Ctype.EMPTY)
        cell2=Cell(0,1,gap,1,Ctype.EMPTY)
        win = WINDOW
        cell.draw(background)
        cell2.draw(background)
        #grid = self
        #win.fill(WHITE)
        # for row in grid.grid:
        #     for cell in row:
        #         cell.draw(win)
        #grid.draw_grid_lines(win, self.axis_dim, WIN_X, )
        pygame.display.update()


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------
        # ***** GAME LOOP ******
        # For testing purposes mainly
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------
clock = pygame.time.Clock()
is_running = True
grid=Grid(2)
grid.draw_map()
while is_running:
 time_delta = clock.tick(60)/1000.0
 for event in pygame.event.get():
     if event.type == pygame.QUIT:
         is_running = False
     elif event.type == pygame.MOUSEBUTTONDOWN:
        location = pygame.mouse.get_pos()
        col = location[0]
        row = location[1]
        print("testing clicking")
        print(f"X-axis Location : {col}")
        print(f"Y-axis Location : {row}")


     manager.process_events(event)

 manager.update(time_delta)

 WINDOW.blit(background, (0, 0))
 manager.draw_ui(WINDOW)

 pygame.display.update()
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------
