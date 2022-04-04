"""
An AI player for Othello. 
"""

import random
import sys
import time


# You can use the functions in othello_shared to write your AI
from othello_shared import find_lines, get_possible_moves, get_score, play_move

# define a gloabal dictionary of states
dicstate = {}

def eprint(*args, **kwargs): #you can use this for debugging, as it will print to sterr and not stdout
    print(*args, file=sys.stderr, **kwargs)
    
# Method to compute utility value of terminal state
def compute_utility(board, color):
    '''
    Calculates number of disks of player's colour - number of disks of opponent's colour
    '''
    scores = get_score(board)
    value = 0
    # 1 = Dark
    if color == 1:
        value = scores[0]-scores[1]
    else:
        value = scores[1] - scores[0]
    return value

def nodeorderer(board, children, color):
    '''
    Orders the nodes
    '''
    if color == 2:
        Newcolor = 1

    if color == 1:
        Newcolor = 2

    moves = {}
    result = []
    
    for child in children:
        newboard = play_move(board, Newcolor, child[0], child[1])
        cost = compute_utility(newboard, color)
        if cost in moves and moves[cost] != [child]:
            moves[cost].append(move)
        else:
            moves[cost] = [child]

    ordlist = sorted(list(moves.keys()), reverse=True)
    for orde in ordlist:
        result += moves[orde]
    return result
        
# Better heuristic value of board
def compute_heuristic(board, color): #not implemented, optional
    '''
    Calculates number of disks of player's colour - number of disks of opponent's colour
    '''
    scores = get_score(board)
    value = 0
    numedge = 0
    i = 0
    while i < len(board):
        if board[0][i] == color:
            numedge += 1
        if board[i][0] == color:
            numedge += 1
        if board[-1][i] == color:
            numedge += 1
        if board[i][-1] == color:
            numedge += 1
            
        i+1
        
    numcorner = 0

    if board[0][0] == color:
        numcorner += 1

    if board[-1][0] == color:
        numcorner += 1

    if board[0][-1] == color:
        numcorner += 1

    if board[-1][-1] == color:
        numcorner += 1
    # 1 = Dark
    if color == 1:
        numdif = scores[0]-scores[1]


        
    if color == 2:
        numdif = scores[1] - scores[0]

    value = 6*len(board)*numcorner + 2*numedge + numdiff
    return value

############ MINIMAX ###############################
def minimax_min_node(board, color, limit, caching = 0):
    '''
    This function will compute the min-players belief
    '''
    # This computes the colour of the other player
    if color == 2:
        Newcolor = 1

    if color == 1:
        Newcolor = 2
        
    #IMPLEMENT (and replace
    if len(get_possible_moves(board, Newcolor)) != 0:
        bestmove = get_possible_moves(board, Newcolor)[0]

    else:
        bestmove =(None, None)
        
    if get_possible_moves(board, Newcolor) == () or limit == 0 :
        return ((None, None), compute_utility(board, Newcolor))

    MinEval = float('inf')
    strbor = str(board)
    posmoves = get_possible_moves(board, Newcolor)
                               
    for child in posmoves:
        newboard1 = play_move(board, Newcolor, child[0], child[1])
        strboard = str(newboard1)
        if caching and strboard in dicstate:
            Min = dicstate[strboard]
            
        else:
            x, Min = minimax_max_node(newboard1, color, limit - 1, caching)
            if caching:
                dicstate[strboard] = Min
                
        if Min < MinEval:
            bestmove = child
            MinEval = Min

    return (bestmove, MinEval)


def minimax_max_node(board, color, limit, caching = 0): #returns highest possible utility
    '''
    This function represents tha Maximizing part of the mini-max algorithm
'   '''
        
    #IMPLEMENT (and replace
    if len(get_possible_moves(board, color)) != 0:
        bestmove = get_possible_moves(board, color)[0]

    else:
        bestmove =(None, None)
        
    if len(get_possible_moves(board, color))== 0 or limit == 0 :
        return ((None, None), compute_utility(board, color))

    MaxEval = -float('inf')
    strbor = str(board)
    posmoves = get_possible_moves(board, color)

    for child in posmoves:
        newboard1 = play_move(board, color, child[0], child[1])
        strboard = str(newboard1)
        if caching and strboard in dicstate:
            Max = dicstate[strboard]
            
        else:
            x, Max = minimax_min_node(newboard1, color, limit - 1, caching)
            if caching:
                dicstate[strboard] =  Max
        if Max > MaxEval:
            bestmove = child
            MaxEval = Max
    return (bestmove, MaxEval)

def select_move_minimax(board, color, limit, caching = 0):
    """
    Given a board and a player color, decide on a move. 
    The return value is a tuple of integers (i,j), where
    i is the column and j is the row on the board.  

    Note that other parameters are accepted by this function:
    If limit is a positive integer, your code should enfoce a depth limit that is equal to the value of the parameter.
    Search only to nodes at a depth-limit equal to the limit.  If nodes at this level are non-terminal return a heuristic 
    value (see compute_utility)
    If caching is ON (i.e. 1), use state caching to reduce the number of state evaluations.
    If caching is OFF (i.e. 0), do NOT use state caching to reduce the number of state evaluations.    
    """
    value = minimax_max_node(board, color, limit, caching )
    return value[0][0], value[0][1] 

############ ALPHA-BETA PRUNING #####################
def alphabeta_min_node(board, color, alpha, beta, limit, caching = 0, ordering = 0):
   # This computes the colour of the other player
    if color == 2:
        Newcolor = 1

    if color == 1:
        Newcolor = 2
        
    #IMPLEMENT (and replace 
    if get_possible_moves(board, color) == () or limit == 0:
        return ((None, None), compute_utility(board, color))

    bestmove = (None, None)
    MinEval = 2**31
    posmoves = get_possible_moves(board, color)

    if ordering:
        posmoves = nodeorderer(board, posmoves, color)
                               
    for child in posmoves:
        newboard = play_move(board, Newcolor, child[0], child[1])
        value1 = alphabeta_max_node(newboard, color, alpha, beta, limit - 1, caching)
        strboard = str(newboard)
        if caching and strboard in dicstate:
            Min = dicstate[strboard]
        else:
            _, Min = alphabeta_max_node(newboard, color, alpha, beta, limit-1, caching)
            if caching:
                dicstate[strboard] = Min
                
        if Min < MinEval:
            bestmove = child
            MinEval = Min
            
        beta = min(beta, Min)
        if beta <= alpha:
            break
        
    return (bestmove, MinEval)

def alphabeta_max_node(board, color, alpha, beta, limit, caching = 0, ordering = 0):
    if get_possible_moves(board, color) == () or limit == 0 :
        return ((None, None), compute_utility(board, color))

    bestmove = (None, None)
    MaxEval = -2**31
    posmoves = get_possible_moves(board, color)

    if ordering:
        posmoves = nodeorderer(board, posmoves, color)
                               
    for child in posmoves:
        newboard1 = play_move(board, color, child[0], child[1])
        strboard = str(newboard1)
        if caching and strboard in dicstate:
            Max = dicstate[strboard]

        else:
            _, Max = alphabeta_min_node(newboard1, color, alpha, beta, limit - 1, caching)
            if caching:
                dicstate[strboard] = Max
                
        if Max > MaxEval:
            bestmove = child
            MaxEval = Max
        alpha = max(alpha, Max)
        if beta <= alpha:
            break
    return (bestmove, MaxEval)

def select_move_alphabeta(board, color, limit, caching = 0, ordering = 0):
    """
    Given a board and a player color, decide on a move. 
    The return value is a tuple of integers (i,j), where
    i is the column and j is the row on the board.  

    Note that other parameters are accepted by this function:
    If limit is a positive integer, your code should enfoce a depth limit that is equal to the value of the parameter.
    Search only to nodes at a depth-limit equal to the limit.  If nodes at this level are non-terminal return a heuristic 
    value (see compute_utility)
    If caching is ON (i.e. 1), use state caching to reduce the number of state evaluations.
    If caching is OFF (i.e. 0), do NOT use state caching to reduce the number of state evaluations.    
    If ordering is ON (i.e. 1), use node ordering to expedite pruning and reduce the number of state evaluations. 
    If ordering is OFF (i.e. 0), do NOT use node ordering to expedite pruning and reduce the number of state evaluations. 
    """
    alpha = -2**31
    beta = 2**31
    value = alphabeta_max_node(board, color,  alpha, beta, limit, caching )
    return value[0][0], value[0][1] 


####################################################
def run_ai():
    """
    This function establishes communication with the game manager.
    It first introduces itself and receives its color.
    Then it repeatedly receives the current score and current board state
    until the game is over.
    """
    print("Othello AI") # First line is the name of this AI
    arguments = input().split(",")
    
    color = int(arguments[0]) #Player color: 1 for dark (goes first), 2 for light. 
    limit = int(arguments[1]) #Depth limit
    minimax = int(arguments[2]) #Minimax or alpha beta
    caching = int(arguments[3]) #Caching 
    ordering = int(arguments[4]) #Node-ordering (for alpha-beta only)

    if (minimax == 1): eprint("Running MINIMAX")
    else: eprint("Running ALPHA-BETA")

    if (caching == 1): eprint("State Caching is ON")
    else: eprint("State Caching is OFF")

    if (ordering == 1): eprint("Node Ordering is ON")
    else: eprint("Node Ordering is OFF")

    if (limit == -1): eprint("Depth Limit is OFF")
    else: eprint("Depth Limit is ", limit)

    if (minimax == 1 and ordering == 1): eprint("Node Ordering should have no impact on Minimax")

    while True: # This is the main loop
        # Read in the current game status, for example:
        # "SCORE 2 2" or "FINAL 33 31" if the game is over.
        # The first number is the score for player 1 (dark), the second for player 2 (light)
        next_input = input()
        status, dark_score_s, light_score_s = next_input.strip().split()
        dark_score = int(dark_score_s)
        light_score = int(light_score_s)

        if status == "FINAL": # Game is over.
            print
        else:
            board = eval(input()) # Read in the input and turn it into a Python
                                  # object. The format is a list of rows. The
                                  # squares in each row are represented by
                                  # 0 : empty square
                                  # 1 : dark disk (player 1)
                                  # 2 : light disk (player 2)

            # Select the move and send it to the manager
            if (minimax == 1): #run this if the minimax flag is given
                movei, movej = select_move_minimax(board, color, limit, caching)
            else: #else run alphabeta
                movei, movej = select_move_alphabeta(board, color, limit, caching, ordering)
            
            print("{} {}".format(movei, movej))

if __name__ == "__main__":
    run_ai()
