import string
import pygame as pg

OFFSET_X = 50
OFFSET_Y = 100
OFFSET_DOMINE = 5


def draw_squares(screen , board , LIGHT, GREY):
    colour_dict = {True: LIGHT, False: GREY}
    current_colour = True
    for row in range(len(board)):
        for square in range(len(board[0])):
            # print(square)
            pg.draw.rect(screen, colour_dict[current_colour], ((OFFSET_X + (square * 50)), OFFSET_Y + (row * 50), 50, 50))
            current_colour = not current_colour
        if(len(board[0]) % 2 == 0):
            current_colour = not current_colour

def draw_o(screen,color , x,y):
    pg.draw.rect(screen, color, (OFFSET_X + OFFSET_DOMINE + (y * 50), OFFSET_Y + OFFSET_DOMINE + (x * 50), 90, 40),0,15)

def draw_x(screen,color , x,y):
    pg.draw.rect(screen, color, ((OFFSET_X + OFFSET_DOMINE + (y * 50)), OFFSET_Y + OFFSET_DOMINE + (x * 50), 40, 90),0,15)

def draw_domine(board, screen ,w, h):
    X = (211,100,59)     #boje domina
    O = (64,59,51,255)

    for i in range(w):
        count = 0
        for j in range(h):
            if(board[i][j] == "O"):
                count+=1
                if(count==2):
                    draw_o(screen,O,i,j-1)
                    count = 0
                    
    for i in range(h):
        count = 0
        for j in range(w):
            if(board[j][i] == 'X'):
                count+=1
                if(count==2):
                    draw_x(screen,X,j-1,i)
                    count = 0
               
def draw_coords(screen, font, w, h):
    BLACK = (0, 0, 0)
    for row in range(w):
        text = str( w - row)
        text_surface = font.render(text,True,BLACK)
        screen.blit(text_surface,(OFFSET_X - 25,OFFSET_Y + 18+(row*50)))

    letters = list(string.ascii_uppercase)
    for col in range(h):
        text = letters[col]
        text_surface = font.render(text,True,BLACK)
        screen.blit(text_surface,(OFFSET_X + 18 + (col*50),OFFSET_Y+ 18 +w*50))
   
def resize_board(new_w, new_h,w,h):
    try:
        
        int1 = int(new_w)
        int2 = int(new_h)
        if(new_w != '' and new_w!=w and int1<= 10 ):
            w = new_w
            b = init_board(w,h)
        
        elif(new_h != '' and new_h!=h and int2<= 10):
            h=new_h
            b = init_board(w,h)
        else: return False
        return b       
    except:
        print("Nevalidan znak")

def init_board(x, y):
    a = int(x)
    b = int(y)
    board = [["-" for x in range(a)] for x in range(b)]
    return board

def find_square(x, y , board_width , board_height):
    true_target = int((y - OFFSET_Y) // 50) if int((y - OFFSET_Y) // 50) < board_height else -1  , int((x - OFFSET_X) // 50) if int((x - OFFSET_X) // 50) < board_width else -1
    return true_target

def check_end(board, player): # vraca true ako postoji mogucnost da player odigra potez
    counter = 0
    match player:
            case 'O':
                for j in range(len(board)):
                    for i in range(len(board[0])):
                        if(board[j][i]=='-'):
                            counter+=1
                        else: counter=0

                        if(counter==2):
                            return True    
                    counter=0
            case 'X':
                 for j in range(len(board[0])):
                    for i in range(len(board)):
                        if(board[i][j]=='-'):
                            counter+=1
                        else: counter=0

                        if(counter==2):
                            return True    
                    counter=0
    return False


def check_if_valid(turn, true_target, board_width , board_height):
    match turn:
        case 'O':
            #provera da O plocica ne strci van table 
            if true_target[0]>=int(board_height) or true_target[0] < 0 or true_target[1] < 0 or  true_target[1]>=int(board_width)-1:
                return False
            target = true_target , (true_target[0], true_target[1]+1)

        case 'X': 
            #provera da X plocica ne strci van table
            if true_target[1]>=int(board_width) or true_target[1] < 0 or true_target[0] < 0 or  true_target[0]>=int(board_height)-1:
                return False
            target = true_target , (true_target[0]+1, true_target[1])
    return target           

def change_state(board,target,turn):
    slobodno = True
    for x in target:
        if board[x[0]][x[1]] != "-":
            slobodno = False
            break
    if(slobodno):
        for x in target:
            board[x[0]][x[1]]= turn
        turn = "O" if turn == "X" else "X"
    return turn


def find_all_possible_states(turn,board):
    states = []
   
    match turn:
        case 'O':
            for i in range(len(board)):
                for j in range(len(board[0])-1):
                    target = check_if_valid(turn,(i,j),len(board[0]),len(board))
                    if target:
                        # state = copy.deepcopy(board)
                        state = list(map(list,board))
                        new_turn = change_state(state,target,turn)
                        if new_turn != turn:
                            states.append(state)
                        
        case 'X':
           for i in range(len(board)-1):
                for j in range(len(board[0])):
                    target = check_if_valid(turn,(i,j),len(board[0]),len(board))
                    if target:
                        # state = copy.deepcopy(board)
                        state = list(map(list,board))
                        new_turn = change_state(state,target,turn)
                        if new_turn != turn:
                            states.append(state)     

    return states

def find_all_possible_moves(turn,board):
    board_h = len(board)
    board_w = len(board[0])
    turns = []
    match turn:
        case 'O':
            for i in range(board_h):
                for j in range(board_w-1):
                    target = check_if_valid(turn,(i,j),board_w,board_h)
                    if target:
                        slobodno = True
                        for x in target:
                            if board[x[0]][x[1]] != "-":
                                slobodno = False
                        if(slobodno):
                            turns.append((i,j))

            
        case 'X':
            for i in range(board_h -1):
                for j in range(board_w):
                    target = check_if_valid(turn,(i,j),board_w,board_h)
                    if target:
                        slobodno = True
                        for x in target:
                            if board[x[0]][x[1]] != "-":
                                slobodno = False
                        if(slobodno):
                            turns.append((i,j))
    return turns



def is_equal(state1, state2):
    if len(state1) != len(state2):
        return False

    if len(state1[0]) != len(state2[0]):
        return False

    for i in range(len(state1)):
        for j in range(len(state1[0])):
            if state1[i][j] != state2[i][j]:
                return False
    
    return True