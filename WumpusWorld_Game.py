import pygame
import pygame_gui
import random
from map_cell import *
import queue

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
NUM_SELECTED = 0
PLAYER_SELECTIONS = queue.Queue(3) # QUEUE TO KEEP TRACK OF CONSECUTIVE SELECTS







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
                #CHANGE THIS BASED ON WHAT THE PROFESSOR SAYS FOR NUMBER OF PITS
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

def clear_selected():
    global PLAYER_SELECTIONS
    global NUM_SELECTED
    while not PLAYER_SELECTIONS.empty():
        cell = PLAYER_SELECTIONS.get()
        print(f"Removing: '{cell.get_type_text()}' from list")
        cell.selected = False
        cell.draw(background)
    NUM_SELECTED = 0

def update_selected(cell):
    global NUM_SELECTED
    cell.selected = True
    cell.draw(background)
    NUM_SELECTED +=1
    PLAYER_SELECTIONS.put(cell)
    print(f"SELECTED CELL :: {CLICKED_POS}  {cell.get_type_text()})")

def player_move_unit(grid, event):
    global LAST_CLICKED
    global CLICKED_POS
    global NUM_SELECTED
    global PLAYER_SELECTIONS
    # Get the row and column of the clicked positin on game board
    if event.type == pygame.MOUSEBUTTONUP:
        pos = pygame.mouse.get_pos()
        col, row = get_clicked_pos(grid, pos)
        # Excludes positions outside of board dimensions
        if col < grid.axis_dim and row < grid.axis_dim:
             CLICKED_POS = (col,row)
             cell = grid.grid[col][row]
             # SELECT & DESELECT A CELL
             #  -- MAX 2 SELECTED
             if cell.selected == True:
                 cell.selected = False
                 cell.draw(background)
                 NUM_SELECTED -= 1
                 PLAYER_SELECTIONS.get()
             elif cell.selected == False and NUM_SELECTED < 2:
                 if NUM_SELECTED == 0 and (1 <= cell.ctype <= 3):
                     update_selected(cell)
                 elif NUM_SELECTED == 0 and (4 <= cell.ctype <= 8):
                     print("Please select a friendly piece first!")
                 elif NUM_SELECTED > 0 and (4 <= cell.ctype <= 8):
                     update_selected(cell)
             print(f"Num selected = {NUM_SELECTED}")
    # CLICK ENTER TO CONFIRM YOUR MOVE
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RETURN and NUM_SELECTED == 2:
            print("CONFIRMED MOVE")
            # Get the two cells from the queue
            p_piece = PLAYER_SELECTIONS.get()
            p_piece.selected = False
            NUM_SELECTED -=1

            t_piece = PLAYER_SELECTIONS.get()
            t_piece.selected = False
            NUM_SELECTED -=1

            code=p_piece.fight(t_piece)
            print(f'Code:{code}')
            #No battle, swap swap cells
            if code==0:
                temp_type = t_piece.ctype
                t_piece.ctype = p_piece.ctype
                p_piece.ctype = temp_type
            #Invalid move
            if code==-3:
                pass
            #both pieces die
            elif code==-2:
                t_piece.ctype=Ctype.EMPTY
                p_piece.ctype=Ctype.EMPTY
            #t_piece dies
            elif code==1:
                #code to subtract from total pieces here
                t_piece.ctype=p_piece.ctype
                p_piece.ctype=Ctype.EMPTY
            #p_piece dies
            elif code==-1:
                print('here')
                p_piece.ctype=Ctype.EMPTY
                print(p_piece)
            elif code==-4:
                print('Probably a bug?')

            t_piece.draw(background)
            p_piece.draw(background)
            


            #A method to check if the player or the cpu won should go here
            return

        else:
            print("Invalid keypress or not enough selected")




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
grid=Grid(2)
grid.init_grid()
#print(grid.grid[5][1].ctype)
grid.draw_map()
while is_running:
    time_delta = clock.tick(60)/1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        player_move_unit(grid, event)

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
