"""
    INITIAL BUILD OF MINI CAMELOT GAME - TO RUN IN CONSOLE 

    DANIEL RICHARD CLARKE
    May 6th, 2015
    CS 6613 - Artificial Intelligence - Spring 2015
    Professor Edward Wong
"""

import operator, calendar, time

class Board:
    def __init__(self, white=None, black=None):
        self.board = []
        for i in range (0,112):
            self.board.append("-")

        self.emptys = ['A1','A2','A3','B1','B2','C1','F1','G1','G2','H1','H2','H3','A12','A13','A14','B13','B14','C14','F14','G13','G14','H12','H13','H14']
        if white == None:
            self.white = ['C5','D5','E5','F5','D6','E6']
        else:
            self.white = white
        if black == None:
            self.black = ['D9','E9','C10','D10','E10','F10']
        else:
            self.black = black

    def print_board(self):
        for i in range(0,len(self.board)-1):
            self.board[i] = '-'
        
        for coord in self.white:
            ind = coord_decode(coord)
            self.board[ind] = 'X'

        for coord in self.black:
            ind = coord_decode(coord)
            self.board[ind] = 'O'

        for coord in self.emptys:
            ind = coord_decode(coord)
            self.board[ind] = ' '
        
        print("\tA\tB\tC\tD\tE\tF\tG\tH")
        row = 1
        prntstr = ""
        for i in range(0,len(self.board)):
            if i%8 == 0:
                if i != 0:
                    prntstr += '\t' + str(row) + '\n\n'
                    row += 1
                prntstr += str(row)
            prntstr += '\t' + self.board[i]            
        print(prntstr + '\t' + str(row))



def gen_possible_moves(board,player=None):
    possible_moves = []
    flag = False

    if player == None:
        all_pieces = board.white + board.black
    elif player == 1:
        all_pieces = board.white
    elif player == -1:
        all_pieces = board.black
    
    for coord in all_pieces:
        if coord[0] == 'A':
            int_moves = [-8,-7,1,8,9]
        elif coord[0] == 'H':
            int_moves = [-9,-8,-1,7,8]
        else:
            int_moves = [-9,-8,-7,-1,1,7,8,9]
        ind = coord_decode(coord)
        for ints in int_moves:
           if player == 1 and coord_encode(ind+ints) in board.black: ##capturing move
               if (not (coord_encode(ind+ints)[0] == 'A' and coord[0] == 'B')) and (not(coord_encode(ind+ints)[0] == 'H' and coord[0] == 'G')):
                   new_finish = ind+ints+ints
                   if new_finish in range(0,112) and coord_encode(new_finish) not in board.black and coord_encode(new_finish) not in board.white and coord_encode(new_finish) not in board.emptys:
                       possible_moves.append([coord,coord_encode(new_finish),coord_encode(ind+ints)])
                       flag = True
           if player == -1 and coord_encode(ind+ints) in board.white: ##capturing move
               if (not (coord_encode(ind+ints)[0] == 'A' and coord[0] == 'B')) and (not(coord_encode(ind+ints)[0] == 'H' and coord[0] == 'G')):
                   new_finish = ind+ints+ints
                   if new_finish in range(0,112) and coord_encode(new_finish) not in board.black and coord_encode(new_finish) not in board.white and coord_encode(new_finish) not in board.emptys:
                       possible_moves.append([coord,coord_encode(new_finish),coord_encode(ind+ints)])
                       flag = True
           if player == 1 and coord_encode(ind+ints) in board.white: ##cantering move
               if (not (coord_encode(ind+ints)[0] == 'A' and coord[0] == 'B')) and (not(coord_encode(ind+ints)[0] == 'H' and coord[0] == 'G')):
                   new_finish = ind+ints+ints
                   if new_finish in range(0,112) and coord_encode(new_finish) not in board.black and coord_encode(new_finish) not in board.white and coord_encode(new_finish) not in board.emptys:
                       possible_moves.append([coord,coord_encode(new_finish)])
           if player == -1 and coord_encode(ind+ints) in board.black: ##cantering move
               if (not (coord_encode(ind+ints)[0] == 'A' and coord[0] == 'B')) and (not(coord_encode(ind+ints)[0] == 'H' and coord[0] == 'G')):
                   new_finish = ind+ints+ints
                   if new_finish in range(0,112) and coord_encode(new_finish) not in board.black and coord_encode(new_finish) not in board.white and coord_encode(new_finish) not in board.emptys:
                       possible_moves.append([coord,coord_encode(new_finish)])
           ##plain move
           if ind+ints in range(0,112) and coord_encode(ind+ints) not in board.emptys and coord_encode(ind+ints) not in board.white and coord_encode(ind+ints) not in board.black:
               possible_moves.append([coord,coord_encode(ind+ints)])

    if flag:
        pm_temp = []
        for move in possible_moves:
            if len(move) == 3:
                pm_temp.append(move)
        possible_moves = list(pm_temp)

    return possible_moves
       

def coord_decode(coord):
    coord_dict = {'A':0,'B':1,'C':2,'D':3,'E':4,'F':5,'G':6,'H':7}

    if len(coord) > 3 or coord[0] not in coord_dict.keys():
        print("ERROR - Coord provided is not correct")
    else:
        ##print(coord_dict[coord[0]])
        ##print(int(coord[1:]))
        ind = (int(coord[1:])*8) + coord_dict[coord[0]]
        return ind-8
    
def coord_encode(ind):
    ind_dict = {0:'A',1:'B',2:'C',3:'D',4:'E',5:'F',6:'G',7:'H'}

    row = int(ind/8) + 1
    col = ind_dict[ind%8]

    return str(col) + str(row)

def accept_input(board,player_num):
    print("Please enter the coordinate of the piece you wish to move, a comma, and the coordinate of where to place it. If you are taking an enemy piece, add another comma, and the coordinate of the piece you are taking.")
    move = input().split(",")
    if player_num == 1:
        if move in gen_possible_moves(board,player_num):
            for i in range(0,len(board.white)):
                if board.white[i] == move[0]:
                    board.white[i] = move[1]
            if len(move) == 3:           
                board.black.remove(move[2])
        else:
            print("That is not an acceptable move, please try again...")
            accept_input(board,player_num)
    else:
        if move in gen_possible_moves(board,player_num):
            for i in range(0,len(board.black)):
                if board.black[i] == move[0]:
                    board.black[i] = move[1]
            if len(move) == 3:           
                board.white.remove(move[2])        
        else:
            print("That is not an acceptable move, please try again...")
            accept_input(board,player_num)

def cpu_move(board,move,player_num):
    if player_num == -1:
        if move in gen_possible_moves(board,player_num):
            for i in range(0,len(board.black)):
                if board.black[i] == move[0]:
                    board.black[i] = move[1]
            if len(move) == 3:           
                board.white.remove(move[2])
        else:
            print("ERROR1 - Black")
    else:
        if move in gen_possible_moves(board,player_num):
            for i in range(0,len(board.white)):
                if board.white[i] == move[0]:
                    board.white[i] = move[1]
            if len(move) == 3:           
                board.black.remove(move[2])        
        else:
            print("ERROR1 - White")

def alpha_beta_search(state, depth, player):
    global max_depth
    global num_nodes
    global max_node_prunes
    global min_node_prunes
    global start_time
    global depth_limit

    start_time = float(time.time())

    num_nodes += 1
    
    alpha = -100
    beta = 100
    flag = None

    possible_moves = gen_possible_moves(state,player)
##    print(possible_moves)
    moves_and_val = {}

    if player == -1:
        for j in range(0,len(possible_moves)):
            move = possible_moves[j]
            new_board = Board(list(state.white), list(state.black))
            for i in range(0,len(new_board.black)):
                if new_board.black[i] == move[0]:
                    new_board.black[i] = move[1]
            if len(move) == 3:
                flag = move
    ##            print(new_board.white)
    ##            print("attempt remove",move[2])            
                new_board.white.remove(move[2])
            v = max_value(new_board,alpha,beta,depth+1)
            moves_and_val[j] = v
    else:
        for j in range(0,len(possible_moves)):
            move = possible_moves[j]
            new_board = Board(list(state.white), list(state.black))
            for i in range(0,len(new_board.white)):
                if new_board.white[i] == move[0]:
                    new_board.white[i] = move[1]
            if len(move) == 3:
                flag = move
    ##            print(new_board.white)
    ##            print("attempt remove",move[2])            
                new_board.black.remove(move[2])
            v = min_value(new_board,alpha,beta,depth+1)
            moves_and_val[j] = v       

##    print("Max depth: ", depth)
##    print("Nodes-generated: ",nodes_gen)
##    print("Max-Val Prunes: ",max_val_prunes)
##    print("Min-Val Prunes: ",min_val_prunes)
    if player == -1: best = min(moves_and_val, key = moves_and_val.get)
    if player == 1: best = max(moves_and_val, key = moves_and_val.get)
    finish_time = float(time.time())
    if (finish_time - start_time) < 5.0 and max_depth == depth_limit:
        depth_limit += 1
        print("DLS")
        return alpha_beta_search(state,0,player)
    else:
        print("T:",finish_time-start_time)
        print(moves_and_val[best])
##        print(best)
        if flag == None:
            return possible_moves[best]
        else:
            return flag

def max_value(state, alpha, beta, depth):
    global max_depth
    global num_nodes
    global max_node_prunes
    global min_node_prunes

    num_nodes += 1
    max_depth = max(max_depth,depth)
    
    if terminal_test(state, depth):
        return eval(state)
    v = -100
    possible_moves = gen_possible_moves(state,1)
    for move in possible_moves:
        new_board = Board(list(state.white), list(state.black))
        for i in range(0,len(new_board.white)):
            if new_board.white[i] == move[0]:
                new_board.white[i] = move[1]
        if len(move) == 3:
##            print(new_board.black)
##            print("attempt remove",move[2])
            new_board.black.remove(move[2])
        v = max(v,min_value(new_board, alpha, beta, depth+1))
        if v >= beta:
##            print("prune")
            max_node_prunes += 1
            return v
        alpha = max(alpha,v)
    return v

def min_value(state, alpha, beta, depth):
    global max_depth
    global num_nodes
    global max_node_prunes
    global min_node_prunes

    num_nodes += 1
    max_depth = max(max_depth,depth)
    
    if terminal_test(state, depth):
        return eval(state)
    v = 100
    possible_moves = gen_possible_moves(state,-1)
    for move in possible_moves:
        new_board = Board(list(state.white), list(state.black))
        for i in range(0,len(new_board.black)):
            if new_board.black[i] == move[0]:
                new_board.black[i] = move[1]
        if len(move) == 3:
##            print(new_board.white)
##            print("attempt remove",move[2])
            new_board.white.remove(move[2])
        v = min(v,max_value(new_board,alpha,beta,depth+1))
        if v <= alpha:
##            print("prune")
            min_node_prunes += 1
            return v
        beta = min(beta,v)
    return v

def terminal_test(board, depth):
    global start_time
    global depth_limit

    current_time = float(time.time())

    if depth != 0 and (current_time - start_time) >= 9.9:
        return True
    
    if depth >= depth_limit: ##Set max depth here!
        return True
    
    white_winners = ['D14','E14']
    black_winners = ['D1','E1']

    if len(board.white) == 0 or len(board.black) == 0:
        return True

    for coord in board.white:
        if coord in white_winners:
            return True
    for coord in board.black:
        if coord in black_winners:
            return True

    return False

def eval(board):
    white_winners = ['D14','E14']
    black_winners = ['D1','E1']

    min_white_dist = 13
    min_black_dist = 13

    for coord in board.white:
        if coord in white_winners:
            return 100
        min_white_dist = min(min_white_dist,13-int(coord_decode(coord)/8))
##        print(min_white_dist)
    for coord in board.black:
        if coord in black_winners:
            return -100
        min_black_dist = min(min_black_dist,int(coord_decode(coord)/8))
##        print(min_black_dist)

    eval_num = 100 * ((0.2 * ((len(board.white) - len(board.black))/5)) + (0.4 * (-1/min_black_dist)) + (0.4 * (1/min_white_dist)))
##    if min_white_dist <= 2:
##        print(min_black_dist, min_white_dist, eval_num)
    
    return eval_num

def print_absearch_stats():
    print("Max Depth: ",max_depth)
    print("Nodes Generated: ",num_nodes)
    print("MaxNode Prunes: ",max_node_prunes)
    print("MinNode Prunes: ",min_node_prunes)

def win_check(board):
    white_winners = ['D14','E14']
    black_winners = ['D1','E1']

    if len(board.white) == 0:
        return -1

    if len(board.black) == 0:
        return 1

    for coord in board.white:
        if coord in white_winners:
            return 1
    for coord in board.black:
        if coord in black_winners:
            return -1

    return 0    

c = Board()
c.print_board()

print("Would you like to to be White (X) or Black (O)? (X/O)")
char = input()
if char == 'X':
    human_num = 1
elif char == 'O':
    human_num = -1
else:
    print("Thats not a valid selection... You can be White(X)")
    human_num = 1

while True:
    max_depth = 0
    num_nodes = 0
    max_node_prunes = 0
    min_node_prunes = 0
    start_time = 0
    depth_limit = 4
##    ##cpu run
##    cpu_move(c,alpha_beta_search(c,0,1),1)
##    print_absearch_stats()
##    c.print_board()
##    if terminal_test(c,0) : break
##    
##    max_depth = 0
##    num_nodes = 0
##    max_node_prunes = 0
##    min_node_prunes = 0
##    start_time = 0
##    depth_limit = 4
##    cpu_move(c,alpha_beta_search(c,0,-1),-1)
##    print_absearch_stats()
##    c.print_board()
##    if terminal_test(c,0) : break
    
    if human_num == 1:
        accept_input(c,human_num)
        c.print_board()
        if win_check(c) != 0 : break
        cpu_move(c,alpha_beta_search(c,0,-human_num),-human_num)
        print_absearch_stats()
        c.print_board()
        if win_check(c) != 0 : break
    else:
        cpu_move(c,alpha_beta_search(c,0,-human_num),-human_num)
        print_absearch_stats()
        c.print_board()
        if win_check(c) != 0 : break
        accept_input(c,human_num)
        c.print_board()
        if win_check(c) != 0 : break
        
if win_check(c) == 1:
    print("GAME OVER. White has won the game!")
elif win_check(c) == -1:
    print("GAME OVER. Black has won the game!")
