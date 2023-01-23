import pygame as pg
from board_funcs import *
from checkbox import Checkbox
from minimax import  minimax_alpha_beta

w = 800
h = 800

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (153,153,153)
LIGHT = (254,254,254)
DARK = (90, 90, 90)

def main():
    pg.init()
    screen = pg.display.set_mode((w, h))
    pg.display.set_caption('Domineering')
   
    
    boxes =[]
    button = Checkbox(screen, 20, 50, 0, caption='Player')
    button2 = Checkbox(screen, 120, 50, 1, caption='Computer')
    button2.checked = True
    checkedBox = button2
    boxes.append(button)
    boxes.append(button2)


    
    size_box_1 = pg.Rect(500,50,40,30)
    size_box_2 = pg.Rect(565,50,40,30)

    font = pg.font.Font(None, 32)
    
    size_box_1_active = False
    size_box_2_active = False
    size_box_color_active = pg.Color('dodgerblue2')
    size_box_color_inactive = pg.Color('lightskyblue3')

    size_box_1_color = size_box_color_inactive
    size_box_2_color = size_box_color_inactive

    text_X = font.render("X",True,BLACK,None)
    size_box_1_text = '2'       #pocetna velicina table
    size_box_2_text = '5'
    new_sbx_1_text=size_box_1_text
    new_sbx_2_text=size_box_2_text

    board = init_board(size_box_1_text,size_box_2_text) # inicijalizacija ploce (pocetno stanje)

    running = True      # game loop uslov

    turn = 'X'          # pocetni potez
    humanOnMove = False  # proverava da li prvi igra covek


    

    while running:

        for event in pg.event.get():

            # event handler za prekid igre
            if event.type == pg.QUIT:
                running = False

            # event handler za klik misem
       
            if event.type == pg.MOUSEBUTTONDOWN:
            
                for box in boxes:
                    # oldChecked = box.checked
                    box.update_checkbox(event)
                    if box.checked is True and box is not checkedBox:
                        if box.caption == "Player":
                            humanOnMove = True
                        else:
                            humanOnMove = False
                        for b in boxes:
                            if b != box:
                                b.checked = False
                        checkedBox = box
                        # if not oldChecked:
                        board = init_board(size_box_1_text,size_box_2_text)
                        turn = "X"

                if event.button != 3: # razlicito od 3 da ne bi kliktali desnim klikom

                    # provera da li je kliknuto na size_box_1
                    if size_box_1.collidepoint(event.pos):
                        size_box_1_active = not size_box_1_active
                    else:
                        size_box_1_active = False
                    size_box_1_color = size_box_color_active if size_box_1_active else size_box_color_inactive
                    
                    # provera da li je kliknuto na size_box_2
                    if size_box_2.collidepoint(event.pos):
                        size_box_2_active = not size_box_2_active
                    else:
                        size_box_2_active = False
                    size_box_2_color = size_box_color_active if size_box_2_active else size_box_color_inactive

                    # pozicija na koju je stvarno kliknuto (jedan kvadrat)
                    true_target = find_square(event.pos[0], event.pos[1], int(size_box_1_text), int(size_box_2_text))

                    if humanOnMove:
                    # odredjivanje dva kvadrata koja treba popuniti na osnovu toga 
                    # koji igrac je na potezu (kvadrat na koji je stvarno kliknuto i njegov susedni)
                        target = check_if_valid(turn,true_target,size_box_1_text,size_box_2_text)
                        if(not target): break

                        newTurn = change_state(board,target,turn)

                        if newTurn != turn:
                            turn = newTurn
                            humanOnMove = not humanOnMove

                        if(not check_end(board,turn)):
                            print("Pobednik je ", "O" if turn == "X" else "X")
 
            if not humanOnMove and check_end(board,turn):
                new_state = ai_play_move(board,turn)
                if new_state is not None:
                    board = new_state
                    turn = "O" if turn == "X" else "X"
                    humanOnMove = not humanOnMove

                

                if(not check_end(board,turn)):
                    print("Pobednik je ", "O" if turn == "X" else "X") 
                    # running = False         
                    #koriscenje funkcije za nalazenje sledecih stanja (svih mogucih poteza)

                    # states = find_all_possible_states(turn,board)
                    # for state in states:
                    #     for i in range(len(state)):
                    #         print(*state[i])
                    #     print("------------------")

            # event handler za pisanje po size boxovima
            if event.type == pg.KEYDOWN:
                if size_box_1_active:                    
                    if event.key == pg.K_BACKSPACE:
                        new_sbx_1_text = size_box_1_text[:-1]
                    else:                        
                        new_sbx_1_text += event.unicode
                        new_board = resize_board(
                                                new_sbx_1_text,
                                                size_box_2_text,
                                                size_box_1_text,
                                                size_box_2_text
                                                )
                        if(new_board != False):
                            size_box_1_text = new_sbx_1_text
                            
                            if checkedBox.caption == "Player":
                                humanOnMove = True
                            else: humanOnMove = False

                   
                            turn = "X"
                            board=new_board
                            
                        
                elif size_box_2_active:
                    if event.key == pg.K_RETURN:
                        new_sbx_2_text = ''
                    elif event.key == pg.K_BACKSPACE:
                        new_sbx_2_text = size_box_2_text[:-1]
                    else:
                        new_sbx_2_text += event.unicode
                        new_board = resize_board(
                                                size_box_1_text,
                                                new_sbx_2_text,
                                                size_box_1_text,
                                                size_box_2_text
                                                )
                        if(new_board!= False):
                            size_box_2_text = new_sbx_2_text
                            
                            if checkedBox.caption == "Player":
                                humanOnMove = True
                            else: humanOnMove = False

                            turn = "X"
                            board=new_board

        # crtanje pozadine, ploce, koordinata i domina
        screen.fill(DARK)
        draw_squares(screen , board , LIGHT , GREY)
        draw_coords(screen,font,int(size_box_2_text), int(size_box_1_text))
        draw_domine(board,screen, int(size_box_2_text),int(size_box_1_text))

        # crtanje size boxova
        txt_surface = font.render(new_sbx_1_text, True, size_box_1_color)
        screen.blit(txt_surface, (size_box_1.x+8, size_box_1.y+5))
        pg.draw.rect(screen, size_box_1_color, size_box_1, 2)

        screen.blit(text_X,(545,55))
        
        txt_surface2 = font.render(new_sbx_2_text, True, size_box_2_color)
        screen.blit(txt_surface2, (size_box_2.x+8, size_box_2.y+5))
        pg.draw.rect(screen, size_box_2_color, size_box_2, 2)

        # iscrtavanje checkbox-ova i teksta
        for box in boxes:
            box.render_checkbox()

        text_first_plays = font.render("Select first player: ",True,BLACK,None)
        screen.blit(text_first_plays,(20,20))

        # clock    
        clock = pg.time.Clock()
        clock.tick(60)
        pg.display.update()
        

def ai_play_move(state , turn):
    next_board = minimax_alpha_beta(state,1,True,turn)[0]

    if next_board is not None and is_equal(next_board,state):
        change_state(state,((0,0),(1,0)) if turn =="X" else ((0,0),(0,1)),turn)
        return state

    return next_board
    


if __name__ == '__main__':
    main()