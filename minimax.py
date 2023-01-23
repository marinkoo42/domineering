from board_funcs import check_end, find_all_possible_states



def minimax_alpha_beta(stanje, dubina, moj_potez, player,alpha=(None, -1000), beta=(None, 1000) ):
    if moj_potez:
        return max_value(stanje, dubina, alpha, beta,player,stanje,moj_potez)
    else:
        return min_value(stanje, dubina, alpha, beta,player,stanje,moj_potez)


def max_value(stanje, dubina, alpha, beta, player, old_state,cpu_on_move,next_state =None):

    # ako hocemo da ubrzamo algoritam treba ukljuciti zakomentarisani kod,
    # algoritam bi onda prvo odigravao sve DD poteze (koji najvise ogranicavaju protivnika)
    # ali bez ulazenja u min i max funkcije
    ##################################################


    # if len(stanje)>5 or len(stanje[0])>5:

    #     states= find_all_possible_states(player,stanje)
    #     op = "X" if player=="O" else "O"
    #     opStates = find_all_possible_states(op,stanje)
    #     for state in states:
    #         if DD(state,op,len(opStates)):
    #             return state,oceni(state,player)
    
    ############################################################
    if not check_end(stanje,player) :
        return (next_state , -999)

    lista_stanja = find_all_possible_states(player,stanje)

    if dubina == 0 or lista_stanja is None or len(lista_stanja) == 0:
        return (next_state, oceni(stanje,player,old_state,cpu_on_move))
    else:
        for novo_stanje in lista_stanja:
            alpha = max(
            alpha, 
            min_value(novo_stanje, dubina - 1, alpha, beta, "O" if player == "X" else "X", stanje,not cpu_on_move,novo_stanje if next_state is None else next_state),
            key=lambda x: x[1])
            if alpha[1] >= beta[1]:
                break
    return alpha


def min_value(stanje, dubina, alpha, beta, player , old_state,cpu_on_move, next_state=None):
   
    if not check_end(stanje,player) :
        return (next_state , 999)

    lista_stanja = find_all_possible_states(player,stanje)
    if dubina == 0 or lista_stanja is None or len(lista_stanja) == 0:
        return (next_state, oceni(stanje,player,old_state,cpu_on_move))
    else:
        for novo_stanje in lista_stanja:
            beta = min(beta, max_value(novo_stanje, dubina - 1,
                alpha, beta, "O" if player == "X" else "X", stanje,not cpu_on_move,novo_stanje if next_state is None else next_state), key=lambda x: x[1])
            if beta[1] <= alpha[1]:
                break
    return beta



def oceni(stanje,turn,prevState,cpu_on_move):

    if not cpu_on_move:
        old_num_of_moves = find_all_possible_states(turn,prevState)
        cpu_move = "X" if turn=="O" else "O"
        if DD(stanje,turn,len(old_num_of_moves)):
            if cpu_move == "X":
                return 999
            else: return -999

        cpuStates = find_all_possible_states(cpu_move,stanje)
        moves = find_all_possible_states(turn,stanje)

        return len(cpuStates) - len(moves)


    else:
        cpu_move = turn
        op = "X" if turn=="O" else "O"
        cpuStates = find_all_possible_states(cpu_move,stanje)
        moves = find_all_possible_states(op,stanje)

        return len(cpuStates) - len(moves)
        



def DD(state,oponent,oldNumOfOpStates):
	OpStates = find_all_possible_states(oponent,state)
	if(oldNumOfOpStates - len(OpStates)) < 4: return False
	else: return True	


# def count_moves_played(state):
#     count = 0
#     for i in range(len(state)):
#         for j in range(len(state[0])):
#             if state[i][j] != "-":
#                 count += 1
#     return count//2
    