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
<<<<<<< Updated upstream
        cell2.draw(background)
        #grid = self
        #win.fill(WHITE)
        # for row in grid.grid:
        #     for cell in row:
        #         cell.draw(win)
        #grid.draw_grid_lines(win, self.axis_dim, WIN_X, )
        pygame.display.update()
=======
    NUM_SELECTED = 0


def update_selected(cell):
    global NUM_SELECTED
    cell.selected = True
    cell.draw(background)
    NUM_SELECTED += 1
    PLAYER_SELECTIONS.put(cell)
    print(f"SELECTED CELL :: {CLICKED_POS}  {cell.get_type_text()})")


def player_move_unit(grid, event):
    global LAST_CLICKED
    global CLICKED_POS
    global NUM_SELECTED
    global PLAYER_SELECTIONS
    global PLAYER_NUM_UNITS
    global CPU_NUM_UNITS
    global VICTORY_TEXT
    # Get the row and column of the clicked positin on game board
    if event.type == pygame.MOUSEBUTTONUP:
        pos = pygame.mouse.get_pos()
        col, row = get_clicked_pos(grid, pos)
        # Excludes positions outside of board dimensions
        if col < grid.axis_dim and row < grid.axis_dim:
            CLICKED_POS = (col, row)
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
                    #get_neighbors(cell,grid, True)
                elif NUM_SELECTED == 0 and (4 <= cell.ctype <= 8):
                    print("Please select a friendly piece first!")
                elif NUM_SELECTED > 0 and (4 <= cell.ctype <= 8):
                    update_selected(cell)
            print(f"Num selected = {NUM_SELECTED}")

            if NUM_SELECTED == 2:
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
                # No battle, swap swap cells
                if code==0:
                    temp_type = t_piece.ctype
                    t_piece.ctype = p_piece.ctype
                    p_piece.ctype = temp_type
                # Invalid move
                if code==-3:
                    pass
                # both pieces die
                elif code==-2:
                    t_piece.ctype=Ctype.EMPTY
                    p_piece.ctype=Ctype.EMPTY
                    PLAYER_NUM_UNITS -= 1
                    CPU_NUM_UNITS -= 1
                # t_piece dies
                elif code==1:
                    # code to subtract from total pieces here
                    CPU_NUM_UNITS -= 1
                    t_piece.ctype=p_piece.ctype
                    p_piece.ctype=Ctype.EMPTY
                # p_piece dies
                elif code==-1:
                    print('here')
                    p_piece.ctype=Ctype.EMPTY
                    print(p_piece)
                    PLAYER_NUM_UNITS -= 1
                elif code==-4:
                    print('Probably a bug?')

                t_piece.draw(background)
                p_piece.draw(background)

                print(f'cpu pieces:{PLAYER_NUM_UNITS}')
                print(f'player pieces:{CPU_NUM_UNITS}')


                print(f"PLAYER PIECES ({PLAYER_NUM_UNITS}) ---- CPU PIECES ({CPU_NUM_UNITS})")
                VICTORY_TEXT = check_win()

                 # A method to check if the player or the cpu won should go here
                str_board=grid.gen_string_board()
                x=alphabeta((str_board,CPU_NUM_UNITS,PLAYER_NUM_UNITS),2,float('inf'),float('-inf'),True)
                PLAYER_NUM_UNITS=x[1][2]
                CPU_NUM_UNITS=x[1][1]
                #print('end')
                #print(h_val(x[1],True))

                #print(x)
                #print_string_state(x)

                grid.convert_string_board(x[1][0])
                VICTORY_TEXT = check_win()
                
                
                return
            else:
                print("select another to move")

def is_terminal(node):
    if(node[1]==0):
        return True
    elif(node[2]==0):
        return True
    return False


# Returns the heuristic value that is used to sort the board states in the priority queue
def h_val(node,maximizingPlayer):
    if node[2]==0:
        return 10000
    return h_val1(node,maximizingPlayer)*10+h_val2(node,maximizingPlayer)*.5+h_val3(node,maximizingPlayer)*.5+h_val4(node,maximizingPlayer)*.5
    #return h_val3(node,maximizingPlayer)
    # if maximizingPlayer:
    #     return node[2]-node[1]
    # else:
    #     return node[1]-node[2]
    # return node[1]-node[2]

#difference in # of pieces, makes it more aggressive
def h_val1(node,maximizingPlayer):
    return (node[1]-node[2])

#number of different neighbor enemy pieces
def h_val2(node,maximizingPlayer):

    p_list=get_piece_list(node[0],True)
    vals=[0]*len(p_list)
    for i in range(len(p_list)):
        current=p_list[i]
        neighbors=get_neighbors_string(current,node[0],True)
        for j in neighbors:
            if node[0][j[0]][j[1]][0]!='-':
                f=string_fight(node[0][current[0]][current[1]],node[0][j[0]][j[1]])
                if(f==1):
                    vals[i]+=1
                elif(f==-1):
                    vals[i]-=1
    return sum(vals)

# Number of friendly neighbor pieces, makes it cluster more
def h_val3(node,maximizingPlayer):
    p_list=get_piece_list(node[0],True)
    vals=[1]*len(p_list)
    for i in range(len(p_list)):
        current=p_list[i]
        neighbors=get_neighbors_string(current,node[0],True)
        friendlyNeighbors=get_neighbors_string(current,node[0],not True)
        for j in neighbors:
            if node[0][j[0]][j[1]][0]!='-':
                f=string_fight(node[0][current[0]][current[1]],node[0][j[0]][j[1]])
                if(f==1):
                    vals[i]+=1
                elif(f==-1):
                    vals[i]-=1
        for k in friendlyNeighbors:
            if node[0][k[0]][k[1]][0]!='-':
                vals[i]+=1
    return sum(vals)

#Row #,makes it more aggressive
def h_val4(node,maximizingPlayer):
    global D_MOD
    p_list=get_piece_list(node[0],True)
    total=0
    for i in p_list:
        print(i[1])
        if(not True):
            total+=i[1]
        else:
            total+=(3*D_MOD)-1+i[1]
    return total




# Reads the string board and returns the  coordinate pairs of the pieces of the current player
def get_piece_list(str_grid, maximizingPlayer):
    pieces=list()
    #col
    for i in range(grid.axis_dim):
        #range
        for j in range(grid.axis_dim):
            if(maximizingPlayer):
                if str_grid[i][j][0]=='C':
                    pieces.append([i,j])
            else:
                if str_grid[i][j][0]=='P':
                    pieces.append((i,j))
    return pieces

# Gets the cells around the piece that have valid moves
# --> If the cell has a pit, we assume that it's a bad move and don't add it to the list
# --> Depending on if the turn is maximizingPlayer or not, add cells containing enemy units but ignore friendly units
def get_neighbors(cell, grid, maximizingPlayer):
    global D_MOD
    neighbors = []
    board_size = D_MOD * 3
    for j in range(3):
        for i in range(3):
            #print(f'{cell.col-1+i}, {cell.row-1+j}')
            if(i == 1 and j == 1): # the current cell is self, don't check
                continue
            if(cell.col-1+i > board_size -1 or cell.col-1+i < 0 or cell.row-1+j > board_size -1 or cell.row-1+j < 0):
                #print(f"({i},{j}) OUT OF BOUNDS")
                continue
            if(grid.grid[cell.col-1+i][cell.row-1+j].ctype == Ctype.HOLE):
                #print(f"({i},{j}) IS A HOLE")                                        #------------- THIS MIGHT NEED OPTIZING ------------------
                continue
            #Check maximizingPlayer:
            # Assume player is maximizingPlayer
            if not maximizingPlayer:
                if 1 <= grid.grid[cell.col-1+i][cell.row-1+j].ctype <= 3:
                    #print(f"({i},{j}) IS A MAXimizingPlayer FRIENDLY PIECE (ignore)")
                    continue
            else:
                if 4 <= grid.grid[cell.col-1+i][cell.row-1+j].ctype <= 6:
                    #print(f"({i},{j}) IS A MINImizingPlayer FRIENDLY PIECE (ignore)")
                    continue
            #print(f"({i},{j}) is VALID")
            neighbors.append(grid.grid[cell.col-1+i][cell.row-1+j])
    return neighbors


def get_neighbors_string(pair, array, maximizingPlayer):
    global D_MOD
    col = pair[0]
    row = pair[1]
    neighbors = []
    board_size = D_MOD * 3
    for j in range(3):
        for i in range(3):
            #print(f'{cell.col-1+i}, {cell.row-1+j}')
            if(i == 1 and j == 1): # the current cell is self, don't check
                continue
            if(col-1+i > board_size -1 or col-1+i < 0 or row-1+j > board_size -1 or row-1+j < 0):
                #print(f"({i},{j}) OUT OF BOUNDS")
                continue
            if(array[col-1+i][row-1+j] == 'H'):
                #print(f"({i},{j}) IS A HOLE")                                        #------------- THIS MIGHT NEED OPTIZING ------------------
                continue
            #Check maximizingPlayer:
            # Assume player is maximizingPlayer
            if not maximizingPlayer:
                #if 1 <= array[cell.col-1+i][cell.row-1+j].ctype <= 3:
                if array[col-1+i][row-1+j][0] == 'P':
                    #print(f"({i},{j}) IS A MAXimizingPlayer FRIENDLY PIECE (ignore)")
                    continue
            else:
                #if 4 <= grid.grid[cell.col-1+i][cell.row-1+j].ctype <= 6:
                if array[col-1+i][row-1+j][0] == 'C':
                    #print(f"({i},{j}) IS A MINImizingPlayer FRIENDLY PIECE (ignore)")
                    continue
            #print(f"({i},{j}) is VALID")
            #neighbors.append((array[col-1+i][row-1+j],col-1+i,row-1+j))
            neighbors.append((col-1+i,row-1+j))
    return neighbors


# Performs a swap on the pieces for the scenario where coord1 moves to coord2 and beats the unit at coord2
def win_swap(coord1,coord2,array):
    array[coord2[0]][coord2[1]]=array[coord1[0]][coord1[1]]
    array[coord1[0]][coord1[1]]='-'
    return array

# Performs a swap on the pieces for the scenario where coord1 moves to coord2 and loses to the unit at coord2
def loss_swap(coord1,coord2,array):
    array[coord1[0]][coord1[1]]='-'
    return array

# Swaps coord1 and coord2
def swap(coord1,coord2,array):
    temp=array[coord1[0]][coord1[1]]
    array[coord1[0]][coord1[1]]=array[coord2[0]][coord2[1]]
    array[coord2[0]][coord2[1]]=temp
    return array

#returns the board state created by moving the piece at coord1 to coord2
def get_child_state(coord1,coord2,node,maximizingPlayer):
    array=copy.deepcopy(node[0])
    cpu_pieces=node[1]
    p_pieces=node[2]
    c1_type=array[coord1[0]][coord1[1]]
    c2_type=array[coord2[0]][coord2[1]]
    if(c2_type[0]=='-'):
        array=swap(coord1,coord2,array)
    else:
        winner=string_fight(c1_type,c2_type)
        if winner==-2:
            cpu_pieces-=1
            p_pieces-=1
            array[coord2[0]][coord2[1]]='-'
            array[coord1[0]][coord1[1]]='-'
        elif maximizingPlayer:
            if winner==1:
                p_pieces-=1
                array=win_swap(coord1,coord2,array)
            elif winner==-1:
                array=loss_swap(coord1,coord2,array)
                cpu_pieces-=1
        elif not maximizingPlayer:
            if winner==1:
                cpu_pieces-=1
                array=win_swap(coord1,coord2,array)
            elif winner==-1:
                array=loss_swap(coord1,coord2,array)
                p_pieces-=1
        else:
            print('error?')
    return (array,cpu_pieces,p_pieces)



# Simulates piece 1 landing on top of piece 2 on the string_grid
# returns 1 if piece1 wins and -1 piece 2 wins, and -2 if both die
# Returns 0 if there is an error, probably
def string_fight(piece1,piece2):
    p1_type=piece1[1]
    p2_type=piece2[1]
    if p1_type==p2_type:
        return -2
    if p1_type=='M':
        if p2_type=='K':
            return 1
        elif p2_type=='W':
            return -1
    if p1_type=='K':
        if(p2_type=='M'):
            return -1
        elif p2_type=='W':
            return 1
    if p1_type=='W':
        if p2_type=='M':
            return 1
        elif p2_type=='K':
            return -1
    print('ERROR IN STRING_FIGHT')
    return 0

def print_string_board(board):
    global D_MOD
    #print("-----------------------------------")
    #print("BOARD STATE:")
    for i in range(3 * D_MOD):
        print('\n')
        for j in range(3 * D_MOD):
            print(board[j][i], end = '\t')
    print("\n")

def print_string_state(state):
    print("-----------------------------------\nBOARD STATE:")
    print(f"HVAL: {state[0]}")
    print(f"PIECES: {state[1][1]},{state[1][2]}")
    print_string_board(state[1][0])
    print("-----------------------------------")

def alphabeta(node,depth,alpha,beta,maximizingPlayer):
    #return #TEMPORARY
    #global p_queue
    #p_queue=[]
    if depth==0 or is_terminal(node):
        return (h_val(node,maximizingPlayer),node)
    str_grid=node[0]
    best_move=None #this will be used to return the string_grid of the best move that the computer calculated
    if maximizingPlayer:
        value=float('-inf')
        p_queue=[]
        heapq.heapify(p_queue)
        #------------------------------------------------
        #create the childs of the current board state
        pieces = get_piece_list(str_grid, maximizingPlayer)
        game_states=list()
        for i in pieces:
            neighbors=get_neighbors_string(i,node[0],True)
            for size in range(len(neighbors)):
                game_states.append(get_child_state(i,neighbors[size],node,maximizingPlayer))
        #------------------------------------------------
        # Get neighbors of
        for child in game_states:
            heapq.heappush(p_queue,(h_val(child,maximizingPlayer),child))
        print('length')
        print(len(p_queue))
        while len(p_queue)>0:
            child=heapq.heappop(p_queue)
            print_string_state(child)
            alphabeta_results=alphabeta((child[1][0],child[1][1],child[1][2]),depth-1,alpha,beta,False)
            if alphabeta_results[0]>value:
                value=alphabeta_results[0]
                best_move=(child[1][0],child[1][1],child[1][2])
            #I don't know if the next line should be part of the above if statement
                alpha=max(alpha,value)
            if(alpha>=beta):
                print('quit cpu')
                continue
        return (value,best_move)
    else:
        value=float('inf')

        p_queue=[]
        heapq.heapify(p_queue)
        #------------------------------------------------
        #create the childs of the current board state
        pieces=get_piece_list(str_grid,maximizingPlayer)
        game_states=list()
        for i in pieces:
            neighbors=get_neighbors_string(i,node[0],False)
            for size in range(len(neighbors)):
                game_states.append(get_child_state(i,neighbors[size],node,maximizingPlayer))
        #------------------------------------------------
        for child in game_states:
            heapq.heappush(p_queue,(0-h_val(child,maximizingPlayer),child))
            #add child to queue
        while len(p_queue)>0:
            child=heapq.heappop(p_queue)
            alphabeta_results=alphabeta((child[1][0],child[1][1],child[1][2]),depth-1,alpha,beta,True)
            if alphabeta_results[0]<value:
                value=alphabeta_results[0]
                best_move=(child[1][0],child[1][1],child[1][2])
                beta=min(beta,value)
            if(alpha>=beta):
                #print('quit player')
                continue
        return (value,best_move)
#structure of node: (cell, grid,cpunumpieices,playernumpieces)



# Check if the game has ended
# Returns:
# 0 if tie
# 1 if player wins
# -1 if cpu wins
# 2 if game is still on
def check_win():
    if(PLAYER_NUM_UNITS==CPU_NUM_UNITS==0):
        print('Tie')
        return 'Tie'
    elif(PLAYER_NUM_UNITS==0):
        print('CPU Wins')
        return 'CPU Wins'
    elif(CPU_NUM_UNITS==0):
        print('Player Wins')
        return 'Player Wins'
    return "Game In Progress..."


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------
        # ***** UI ELEMENTS  ******
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------
# button_layout_rect = pygame.Rect(0, 0, 100, 50)
# button_layout_rect.topright = (-30,70)
# hello_button = pygame_gui.elements.UIButton(relative_rect=button_layout_rect, text='Say Hello', manager=manager,
#                                              anchors={'left': 'right',
#                                              'right': 'right',
#                                              'top': 'top',
#                                              'bottom': 'top'})

cpu_score_layout = pygame.Rect(0,0,150,40)
cpu_score_layout.topright = (-138, 70)
cpu_score_text = pygame_gui.elements.UILabel(relative_rect = cpu_score_layout, text = "CPU Pieces: " + str(CPU_NUM_UNITS), manager = manager,
                                                anchors={'left': 'right',
                                                'right': 'right',
                                                'top': 'top',
                                                'bottom': 'top'})

player_score_layout = pygame.Rect(0,0,150,40)
player_score_layout.bottomright = (-138, -20)
player_score_text = pygame_gui.elements.UILabel(relative_rect = player_score_layout, text = "Player Pieces: " + str(PLAYER_NUM_UNITS), manager = manager,
                                                anchors={'left': 'right',
                                                'right': 'right',
                                                'top': 'bottom',
                                                'bottom': 'bottom'})

game_status_layout = pygame.Rect(0,0,200,40)
game_status_layout.center = (-138,30)
game_status_text = pygame_gui.elements.UILabel(relative_rect = game_status_layout, text = VICTORY_TEXT, manager = manager,
                                                anchors={'left': 'right',
                                                'right': 'right',
                                                'top': 'top',
                                                'bottom': 'bottom'})

reset_layout = pygame.Rect(0,0,150,40)
reset_layout.topright = (-70, 140)
reset_grid_button = pygame_gui.elements.UIButton(relative_rect =reset_layout, text = "Reset Board", manager = manager,
                                                anchors={'left': 'right',
                                                'right': 'right',
                                                'top': 'top',
                                                'bottom': 'top'})
>>>>>>> Stashed changes


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
