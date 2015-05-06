"""
    FINAL BULID OF MINI CAMELOT GAME - TO RUN ON LOCALHOST SERVER

    DANIEL RICHARD CLARKE
    May 6th, 2015
    CS 6613 - Artificial Intelligence - Spring 2015
    Professor Edward Wong
"""

from flask import *
import json
import operator, calendar, time
app = Flask(__name__)

##GLOBALS
max_depth = 0
num_nodes = 0
max_node_prunes = 0
min_node_prunes = 0
start_time = 0
depth_limit = 4

##APPLICATION FLASK VIEWS
@app.route('/')
def main_page(name=None):
    return render_template('index.html',name=name)

@app.route('/poss_move', methods=['GET'])
def gen_possible_moves():
    data = json.loads(request.args.get('payload',''))
    
    board = data['board']
    player = data['player']
    
    possible_moves = []
    flag = False

    if player == 1:
        all_pieces = board['white']
    elif player == -1:
        all_pieces = board['black']
    

    ## MODIFIED POSSIBLE MOVE GENERATOR TO DEAL WITH BOARD ARRAY INDEX RATHER THAN APLPHANUMERIC COORDINADTES
    for ind in all_pieces:
        if ind%8 == 0:
            int_moves = [-8,-7,1,8,9]
        elif ind%8 == 7:
            int_moves = [-9,-8,-1,7,8]
        else:
            int_moves = [-9,-8,-7,-1,1,7,8,9]
        for ints in int_moves:
           if player == 1 and ind+ints in board['black']: ##capturing move
               if (not (coord_encode(ind+ints)[0] == 'A' and coord_encode(ind)[0] == 'B')) and (not(coord_encode(ind+ints)[0] == 'H' and coord_encode(ind)[0] == 'G')):
                   new_finish = ind+ints+ints
                   if new_finish in range(0,112) and new_finish not in board['black'] and new_finish not in board['white'] and new_finish not in board['emptys']:
                       possible_moves.append([ind,new_finish,ind+ints])
                       flag = True
           if player == -1 and ind+ints in board['white']: ##capturing move
               if (not (coord_encode(ind+ints)[0] == 'A' and coord_encode(ind)[0] == 'B')) and (not(coord_encode(ind+ints)[0] == 'H' and coord_encode(ind)[0] == 'G')):
                   new_finish = ind+ints+ints
                   if new_finish in range(0,112) and new_finish not in board['black'] and new_finish not in board['white'] and new_finish not in board['emptys']:
                       possible_moves.append([ind,new_finish,ind+ints])
                       flag = True
           if player == 1 and ind+ints in board['white']: ##cantering move
               if (not (coord_encode(ind+ints)[0] == 'A' and coord_encode(ind)[0] == 'B')) and (not(coord_encode(ind+ints)[0] == 'H' and coord_encode(ind)[0] == 'G')):
                   new_finish = ind+ints+ints
                   if new_finish in range(0,112) and new_finish not in board['black'] and new_finish not in board['white'] and new_finish not in board['emptys']:
                       possible_moves.append([ind,new_finish])
           if player == -1 and ind+ints in board['black']: ##cantering move
               if (not (coord_encode(ind+ints)[0] == 'A' and coord_encode(ind)[0] == 'B')) and (not(coord_encode(ind+ints)[0] == 'H' and coord_encode(ind)[0] == 'G')):
                   new_finish = ind+ints+ints
                   if new_finish in range(0,112) and new_finish not in board['black'] and new_finish not in board['white'] and new_finish not in board['emptys']:
                       possible_moves.append([ind,new_finish])
           ##plain move
           if ind+ints in range(0,112) and ind+ints not in board['emptys'] and ind+ints not in board['white'] and ind+ints not in board['black']:
               possible_moves.append([ind,ind+ints])

    if flag:
        pm_temp = []
        for move in possible_moves:
            if len(move) == 3:
                pm_temp.append(move)
        possible_moves = list(pm_temp)

    return json.dumps(possible_moves)

@app.route('/cpu_move', methods=['GET'])
def cpu_move():
    data = json.loads(request.args.get('payload',''))
    
    js_board = data['board']
    player = data['player']

    board_w = []
    board_b = []

    for num in js_board['black']:
      board_b.append(coord_encode(num))

    for num in js_board['white']:
      board_w.append(coord_encode(num))

    board = Board(board_w,board_b)

    init_new_search()

    move_en = alpha_beta_search(board,0,player)

    move = []
    for m in move_en:
      move.append(coord_decode(m))

    data = {'move':move,'max_d':max_depth,'num_nodes':num_nodes,'max_node_prunes':max_node_prunes,'min_node_prunes':min_node_prunes}

    return json.dumps(data)


##METHODS AND CLASSES - FROM ORIGINAL IMPLEMENTATION
class Board:
    def __init__(self, white=None, black=None):
        ## BOARD IS ENCODED AS A SINGLE DIMENSION ARRAY
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

## FUNCTION TO GENERATE POSSIBLE MOVES A PLAYER CAN MAKE GIVEN THE STATE OF THE BOARD
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
       
## DECODE ALPHANUMERIC COORDINATES TO INDEX OF BOARD
def coord_decode(coord):
    coord_dict = {'A':0,'B':1,'C':2,'D':3,'E':4,'F':5,'G':6,'H':7}

    if len(coord) > 3 or coord[0] not in coord_dict.keys():
        print("ERROR - Coord provided is not correct")
    else:
        ind = (int(coord[1:])*8) + coord_dict[coord[0]]
        return ind-8

## ENCODE INDEX OF BOARD TO APLHANUMERIC COORDINATE  
def coord_encode(ind):
    ind_dict = {0:'A',1:'B',2:'C',3:'D',4:'E',5:'F',6:'G',7:'H'}

    row = int(ind/8) + 1
    col = ind_dict[ind%8]

    return str(col) + str(row)

## REST GLOBALS BEFORE NEW ALPHA BETA SEARCH
def init_new_search():
    global max_depth
    global num_nodes
    global max_node_prunes
    global min_node_prunes
    global start_time
    global depth_limit

    max_depth = 0
    num_nodes = 0
    max_node_prunes = 0
    min_node_prunes = 0
    start_time = 0
    depth_limit = 4 

## ALPHA BETA SEARCH
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
                new_board.black.remove(move[2])
            v = min_value(new_board,alpha,beta,depth+1)
            moves_and_val[j] = v       

    if player == -1: best = min(moves_and_val, key = moves_and_val.get)
    if player == 1: best = max(moves_and_val, key = moves_and_val.get)
    finish_time = float(time.time())

    ## IMPLETMENT A DEPTH LIMITED SEARCH. IF ABLE TO SEARCH ENTIRE TREE IN LESS THAN 5 SECS, INCREMENT MAX DEPTH AND REDO
    if (finish_time - start_time) < 5.0 and max_depth == depth_limit:
        depth_limit += 1
        print("DLS")
        return alpha_beta_search(state,0,player)
    else:
        print("T:",finish_time-start_time) ##PRINT TOTAL TIME TAKEN ON AB SEARCH
        print(moves_and_val[best]) ##PRINTS BEST EVAL NUMBER
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
            new_board.black.remove(move[2])
        v = max(v,min_value(new_board, alpha, beta, depth+1))
        if v >= beta:
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
            new_board.white.remove(move[2])
        v = min(v,max_value(new_board,alpha,beta,depth+1))
        if v <= alpha:
            min_node_prunes += 1
            return v
        beta = min(beta,v)
    return v

## TEST IS LEAVE IS TERMINAL. ALSO IMPLETEMENTS CUTOFF BASED ON TREE DEPTH AND/OR TIME LIMIT REACHED
def terminal_test(board, depth):
    global start_time
    global depth_limit

    current_time = float(time.time())

    if depth != 0 and (current_time - start_time) >= 9.9:
        return True
    
    if depth >= depth_limit:
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

## EVALUATION FUNCTION
def eval(board):
    white_winners = ['D14','E14']
    black_winners = ['D1','E1']

    min_white_dist = 13
    min_black_dist = 13

    for coord in board.white:
        if coord in white_winners:
            return 100
        min_white_dist = min(min_white_dist,13-int(coord_decode(coord)/8))
    for coord in board.black:
        if coord in black_winners:
            return -100
        min_black_dist = min(min_black_dist,int(coord_decode(coord)/8))

    ## actual function. 20% weight to difference in number of pieces on board (attempt to capture). 80% total weight to distance to castle (attempt to reach castle)
    eval_num = 100 * ((0.2 * ((len(board.white) - len(board.black))/5)) + (0.4 * (-1/min_black_dist)) + (0.4 * (1/min_white_dist)))
    
    return eval_num

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

if __name__ == '__main__':
    app.debug = True
    app.run()
