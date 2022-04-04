"""
An AI player for Othello. 
"""

from email import utils
from hashlib import new
import random
import sys, os
import time
import pdb
from turtle import pos

# You can use the functions in othello_shared to write your AI
from othello_shared import find_lines, get_possible_moves, get_score, play_move
cache = {}
def eprint(*args, **kwargs): #you can use this for debugging, as it will print to sterr and not stdout
    print(*args, file=sys.stderr, **kwargs)
    
# Method to compute utility value of terminal state
def compute_utility(board, color):
    #IMPLEMENT
    score = get_score(board)
    if color == 1:
        return score[0] - score[1]
    else:
        return score[1] - score[0]

# Better heuristic value of board
def compute_heuristic(board, color): #not implemented, optional
    #IMPLEMENT
    corner_weight = 2
    opponent = int(2/color)
    util = compute_utility(board, color)
    possible_moves = get_possible_moves(board, color)
    opp_possible_moves = get_possible_moves(board, opponent)
    # eprint("opp moves", opp_possible_moves)
    heuristic = len(possible_moves) - len(opp_possible_moves) + util

    if board[0][0] == color:
        heuristic += corner_weight
    elif board[-1][-1] == color:
        heuristic += corner_weight
    elif board[-1][0] == color:
        heuristic += corner_weight
    elif board[0][-1] == color:
        heuristic += corner_weight

    return heuristic

def ordered_moves(board, moves, color, current_player):
    '''This is for node ordering'''
    moves_dict = dict()
    result = []
    for move in moves:
        column, row = move
        new_board = play_move(board, current_player, column, row)
        new_util = compute_utility(new_board, color)
        if new_util in moves_dict and moves_dict[new_util] != [move]:
            moves_dict[new_util].append(move)
        else:
            moves_dict[new_util] = [move]
    ordered_utils = sorted(list(moves_dict.keys()), reverse=True)
    for util in ordered_utils:
        result += moves_dict[util]
    return result

############ MINIMAX ###############################
def minimax_min_node(board, color, limit, caching = 0):
    opponent = int(2/color)
    min_util = float('inf')
    possible_moves = get_possible_moves(board, opponent)
    if len(possible_moves) != 0:
        best_move = possible_moves[0]
    else:
        best_move = None
    str_tuple = str(board)
    
    if len(possible_moves) == 0 or limit == 0:
        return None, compute_utility(board, color)

    for move in possible_moves:
        column, row = move
        new_board = play_move(board, opponent, column, row)
        str_board = str(new_board)
        if caching and str_board in cache:
            min_util = cache[str_tuple]
        else:
            _, util = minimax_max_node(new_board, color, limit - 1, caching)
            if caching:
                cache[str(new_board)] = (move, util)
            if util < min_util:
                best_move = move
                min_util = util

    return best_move, min_util

def minimax_max_node(board, color, limit, caching = 0): #returns highest possible utility
    max_util = -float('inf')
    possible_moves = get_possible_moves(board, color)
    if len(possible_moves) != 0:
        best_move = possible_moves[0]
    else:
        best_move = None
    str_tuple = str(board)

    if len(possible_moves) == 0 or limit == 0:
        return None, compute_utility(board, color)

    for move in possible_moves:
        column, row = move
        new_board = play_move(board, color, column, row)
        str_board = str(new_board)
        if caching and str_board in cache:
            util = cache[str_board]
        else:
            _, util = minimax_min_node(new_board, color, limit - 1, caching)
            if caching:
                cache[str(new_board)] = utils
        if util > max_util:
            best_move = move
            max_util = util
    return best_move, max_util

def select_move_minimax(board, color, limit, caching = 0):
    """
    Given a board and a player color, decide on a move. 
    The return value is a tuple of integers (i,j), where
    i is the column and j is the row on the board.  

    Note that other parameters are accepted by this function:
    If limit is a positive integer, your code should enfoce a depth limit that is equal to the value of the parameter.
    Search only to nodes at a depth-limit equal to the limit.  If nodes at this level are non-terminal return a heuristic 
    value (see compute_heuristic)
    If caching is ON (i.e. 1), use state caching to reduce the number of state evaluations.
    If caching is OFF (i.e. 0), do NOT use state caching to reduce the number of state evaluations.    
    """
    #IMPLEMENT (and replace the line below)
    return minimax_max_node(board, color, limit, caching = 0)[0]

############ ALPHA-BETA PRUNING #####################
def alphabeta_min_node(board, color, alpha, beta, limit, caching = 0, ordering = 0):
    opponent = int(2/color)
    min_util = float('inf')
    possible_moves = get_possible_moves(board, opponent)
    if len(possible_moves) != 0:
        best_move = possible_moves[0]
    else:
        best_move = None

    if len(possible_moves) == 0 or limit == 0:
        return None, compute_utility(board, color)

    # new_boards = [play_move(board, opponent, column, row) for move in possible_moves]

    for move in possible_moves:
        column, row = move
        new_board = play_move(board, opponent, column, row)
        str_board = str(new_board)
        if caching and str_board in cache:
            util = cache[str_board]
        else:
            _, util = alphabeta_max_node(new_board, color, alpha, beta, limit - 1, caching, ordering)
            if caching:
                cache[str_board] = util
        if util < min_util:
            best_move = move
            min_util = util
        # Conducting alpha-beta pruning
        beta = min(beta, util)
        if beta <= alpha:
            break

    return best_move, min_util

def alphabeta_max_node(board, color, alpha, beta, limit, caching = 0, ordering = 0):
    #IMPLEMENT (and replace the line below)
    max_util = -float('inf')
    possible_moves = get_possible_moves(board, color)
    if len(possible_moves) != 0:
        best_move = possible_moves[0]
    else:
        best_move = None

    if len(possible_moves) == 0 or limit == 0:
        return None, compute_utility(board, color)

    if ordering:
        possible_moves = ordered_moves(board, possible_moves, color, color)
    for move in possible_moves:
        column, row = move
        new_board = play_move(board, color, column, row)
        str_board = str(new_board)
        if caching and str_board in cache:
            util= cache[str(new_board)]
        else:
            _, util = alphabeta_min_node(new_board, color, alpha, beta, limit - 1, caching, ordering)
            if caching:
                cache[str(new_board)] = util
        if util > max_util:
            best_move = move
            max_util = util
        # alpha-beta pruning
        alpha = max(alpha, util)
        if beta <= alpha:
            break
    return best_move, max_util

def select_move_alphabeta(board, color, limit, caching = 0, ordering = 0):
    """
    Given a board and a player color, decide on a move. 
    The return value is a tuple of integers (i,j), where
    i is the column and j is the row on the board.  

    Note that other parameters are accepted by this function:
    If limit is a positive integer, your code should enfoce a depth limit that is equal to the value of the parameter.
    Search only to nodes at a depth-limit equal to the limit.  If nodes at this level are non-terminal return a heuristic 
    value (see compute_heuristic)
    If caching is ON (i.e. 1), use state caching to reduce the number of state evaluations.
    If caching is OFF (i.e. 0), do NOT use state caching to reduce the number of state evaluations.    
    If ordering is ON (i.e. 1), use node ordering to expedite pruning and reduce the number of state evaluations. 
    If ordering is OFF (i.e. 0), do NOT use node ordering to expedite pruning and reduce the number of state evaluations. 
    """
    #IMPLEMENT (and replace the line below)
    move = alphabeta_max_node(board, color, -float('inf'), float('inf'), limit, caching, ordering)[0]
    return move

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
