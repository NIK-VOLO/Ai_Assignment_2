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
        # ***** GLOBAL VARIABLES  ******
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------
CLICKED_POS = (-1,-1)
LAST_CLICKED = CLICKED_POS








# ------------------------------------------------------------------------------------------------------------------------------------------------------------------
        # ***** GAME GRID FUNCTIONS  ******
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------
class Grid:
    def __init__(self, dimension_mod):
        self.axis_dim = 3*dimension_mod
        self.grid = x = [[None for _ in range(self.axis_dim)] for _ in range(self.axis_dim)]

#--------------------------------------------------------------------
    def init_grid(self):
        gap = GAME_X // self.axis_dim
        print(self.axis_dim/3-1)
        total_spots=list(range(0, self.axis_dim))
        hole_locations=[]
        #row
        for i in range(self.axis_dim):
            self.grid.append([])

            if(i!=0 and i!=self.axis_dim-1):
                hole_locations=random.sample(total_spots,int(self.axis_dim/3-1))
            #column
            for j in range(self.axis_dim):
                if(i==0):
                    cell=Cell(j,i,gap,self.axis_dim,Ctype((j%3)+4))
                elif(i==self.axis_dim-1):
                    cell = Cell(j,i, gap,self.axis_dim, Ctype((j%3)+1))
                else:
                    cell=Cell(j,i,gap,self.axis_dim,Ctype.EMPTY)
                self.grid[j][i]=cell
            for k in hole_locations:
                if(i!=0 and i!=self.axis_dim-1):
                    self.grid[k][i].set_ctype(Ctype.HOLE)
        return self.grid
#--------------------------------------------------------------------
    def draw_map(self):
        gap=GAME_X//self.axis_dim
        #print(gap)
        win = background
        for row in self.grid:
            for cell in row:
                cell.draw(win)
        pygame.display.update()
#--------------------------------------------------------------------

    # SET COLOR OF A PARTICULAR CELL IN GRID
    # def set_cell_color(self, col, row, color):
    #     self.grid[col][row].set_color(color)
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------
        # ***** END GRID FUNCTIONS  ******
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------




# ------------------------------------------------------------------------------------------------------------------------------------------------------------------
        # ***** GLOBAL FUNCTIONS  ******
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_clicked_pos(grid, position):
    gap = GAME_X // grid.axis_dim
    x, y = position
    row = y // gap
    col = x // gap
    return col, row

def player_move_unit(grid):
    print("Player makes a move!")




# ------------------------------------------------------------------------------------------------------------------------------------------------------------------
        # ***** BUTTONS  ******
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------
button_layout_rect = pygame.Rect(0, 0, 100, 50)
button_layout_rect.topright = (-30,20)
hello_button = pygame_gui.elements.UIButton(relative_rect=button_layout_rect, text='Say Hello', manager=manager,
                                             anchors={'left': 'right',
                                             'right': 'right',
                                             'top': 'top',
                                             'bottom': 'top'})

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------
        # ***** GAME LOOP ******
        # For testing purposes mainly
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------
clock = pygame.time.Clock()
is_running = True
grid=Grid(3)
grid.init_grid()
#print(grid.grid[5][1].ctype)
grid.draw_map()
while is_running:
    time_delta = clock.tick(60)/1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        # Get the row and column of the clicked positin on game board
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            col, row = get_clicked_pos(grid, pos)
            if col < grid.axis_dim and row < grid.axis_dim: # Excludes positions outside of board dimensions
                CLICKED_POS = (col,row)
                if(CLICKED_POS == LAST_CLICKED): # Check if the cell has already been selected
                    #print("Cell already selected...")
                    pass
                else:
                    LAST_CLICKED = CLICKED_POS
                    print(f"SELECTED CELL :: {CLICKED_POS}  {grid.grid[col][row].get_type_text()})")

        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == hello_button:
                    print('Hello World!')

    manager.process_events(event)

    manager.update(time_delta)

    WINDOW.blit(background, (0, 0))
    manager.draw_ui(WINDOW)

    pygame.display.update()
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------
