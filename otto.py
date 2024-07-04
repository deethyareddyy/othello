import random
import sys
import time
import pickle

# You can use the functions in othello_shared to write your AI 
from othello_shared import find_lines, get_possible_moves, get_score, play_move

cache = {}
#cache = pickle.load(open("othello_storage.pcl", "rb"))

def compute_utility(board, color):
    p1, p2 = get_score(board)
    utility = 0
    
    if (board[0][0] == color):
        utility += 100
        
        i = 1
        while (i in range(len(board))) and board[i][i] == color:
            utility += 2
            i += 1
        
        i = 1
        while (i in range(len(board))) and board[i][0] == color:
            utility += 2
            i += 1
        
        i = 1
        while (i in range(len(board))) and board[0][i] == color:
            utility += 2
            i += 1
    elif (board[0][0] != color) and (board[0][0] != 0):
        if (board[1][1] == color):
            utility -= 50
        if (board[1][0] == color):
            utility -= 50
        if (board[0][1] == color):
            utility -= 50
    else:
        if (board[1][1] == color):
            utility -= 20
        if (board[1][0] == color):
            utility -= 10
        if (board[0][1] == color):
            utility -= 10
    
    if (board[-1][0] == color):
        utility += 100
        
        i = 1
        while (i in range(len(board))) and board[-1][i] == color:
            utility += 2
            i += 1
        
        i = 2
        while (i in range(len(board))) and board[-i][0] == color:
            utility += 2
            i += 1
        
        i = 2
        while (i in range(len(board))) and board[-i][i - 1] == color:
            utility += 2
            i += 1
    elif (board[-1][0] != color) and (board[-1][0] != 0):
        if (board[-1][1] == color):
            utility -= 50
        if (board[-2][0] == color):
            utility -= 50
        if (board[-2][1] == color):
            utility -= 50
    else:
        if (board[-1][1] == color):
            utility -= 10
        if (board[-2][0] == color):
            utility -= 10
        if (board[-2][1] == color):
            utility -= 20
    
    if (board[0][-1] == color):
        utility += 100
        
        i = 2
        while (i in range(len(board))) and board[0][-i] == color:
            utility += 2
            i += 1
        
        i = 1
        while (i in range(len(board))) and board[i][-1] == color:
            utility += 2
            i += 1
        
        i = 2
        while (i in range(len(board))) and board[i - 1][-i] == color:
            utility += 2
            i += 1
    elif (board[0][-1] != color) and (board[0][-1] != 0):
        if (board[0][-2] == color):
            utility -= 50
        if (board[1][-2] == color):
            utility -= 50
        if (board[1][-1] == color):
            utility -= 50
    else:
        if (board[0][-2] == color):
            utility -= 10
        if (board[1][-2] == color):
            utility -= 20
        if (board[1][-1] == color):
            utility -= 10
    
    if (board[-1][-1] == color):
        utility += 100
        
        i = 2
        while (i in range(len(board))) and board[-i][-i] == color:
            utility += 2
            i += 1
        
        i = 2
        while (i in range(len(board))) and board[-i][-1] == color:
            utility += 2
            i += 1
        
        i = 2
        while (i in range(len(board))) and board[-1][-i] == color:
            utility += 2
            i += 1
    elif (board[-1][-1] != color) and (board[-1][-1] != 0):
        if (board[-2][-1] == color):
            utility -= 50
        if (board[-2][-2] == color):
            utility -= 50
        if (board[-1][-2] == color):
            utility -= 50
    else:
        if (board[-2][-1] == color):
            utility -= 10
        if (board[-2][-2] == color):
            utility -= 20
        if (board[-1][-2] == color):
            utility -= 10
    i = 2
    while i <= 5:
        j = 2
        while j <= 5:
            if board[i][j] == color:
                utility += 0.1
            j += 1
        i += 1
    
    if color == 1:
        opp_color = 2
    else:
        opp_color = 1
    
    i = 2
    while i <= 5:
        if board[i][0] == color:
            if board[i - 1][0] == opp_color or board[i + 1][0] == opp_color:
                utility -= 10
            else:
                utility += 10
        if board[0][i] == color:
            if board[0][i - 1] == opp_color or board[0][i + 1] == opp_color:
                utility -= 10
            else:
                utility += 10
        if board[i][-1] == color:
            if board[i - 1][-1] == opp_color or board[i + 1][-1] == opp_color:
                utility -= 10
            else:
                utility += 10
        if board[-1][i] == color:
            if board[-1][i - 1] == opp_color or board[-1][i + 1] == opp_color:
                utility -= 10
            else:
                utility += 10
        i += 1
    
    if (board[0][0] == opp_color):
        utility -= 200
    if (board[-1][0] == opp_color):
        utility -= 200
    if (board[0][-1] == opp_color):
        utility -= 200
    if (board[-1][-1] == opp_color):
        utility -= 200
    
    return utility

############ MINIMAX ###############################

def minimax_min_node(board, color):
    opp_color = 1 if color == 2 else 2
    moves = get_possible_moves(board, opp_color)
    if len(moves) == 0:
        #print("Out of moves", file=sys.stderr)
        return compute_utility(board, color)
    else:
        min = float("inf")
        for i, j in moves:
            n = play_move(board, opp_color, i, j)
            uti = minimax_max_node(n, color)
            if uti < min:
                min = uti
        return min


def minimax_max_node(board, color):
    moves = get_possible_moves(board, color)
    if len(moves) == 0:
        #print("Out of moves", file=sys.stderr)
        return compute_utility(board, color)
    else:
        max = float("-inf")
        for i, j in moves:
            n = play_move(board, color, i, j)
            uti = minimax_min_node(n, color)
            if uti > max:
                max = uti
        return max
    
def select_move_minimax(board, color):
    """
    Given a board and a player color, decide on a move. 
    The return value is a tuple of integers (i,j), where
    i is the column and j is the row on the board.
    """
    moves = get_possible_moves(board, color)
    max = float("-inf")
    max_move = None
    for i,j in moves:
        new = play_move(board, color, i, j)
        check = minimax_min_node(new, color)
        if check > max:
            max = check
            max_move = i,j
    return max_move
    
############ ALPHA-BETA PRUNING #####################

#alphabeta_min_node(board, color, alpha, beta, level, limit)
def alphabeta_min_node(board, color, alpha, beta, start):
    opp_color = 1 if color == 2 else 2
    moves = get_possible_moves(board, opp_color)
    end = time.time()
    if len(moves) == 0 or end - start >= 9:
        #print("Out of moves", file=sys.stderr)
        return compute_utility(board, color)
    else:
        for i, j in moves:
            n = play_move(board, opp_color, i, j)
            uti = alphabeta_max_node(n, color, alpha, beta, start)
            if uti < beta:
                beta = uti
                if beta < alpha:
                    return beta
        return beta

#alphabeta_max_node(board, color, alpha, beta, level, limit)
def alphabeta_max_node(board, color, alpha, beta, start):
    moves = get_possible_moves(board, color)
    end = time.time()
    if len(moves) == 0 or end - start >= 9:
        #print("Out of moves", file=sys.stderr)
        return compute_utility(board, color)
    else:
        for i, j in moves:
            n = play_move(board, color, i, j)
            uti = alphabeta_min_node(n, color, alpha, beta, start)
            if uti > alpha:
                alpha = uti
                if beta < alpha:
                    return alpha
        return alpha

def select_move_alphabeta(board, color, start):
    if board in cache:
        return cache[board]
    else:
        moves = get_possible_moves(board, color)
        max = float("-inf")
        max_move = None
        for i,j in moves:
            new = play_move(board, color, i, j)
            check = alphabeta_min_node(new, color, float("-inf"), float("inf"), start)
            if check > max:
                max = check
                max_move = i,j
        cache[board] = max_move
        return max_move


####################################################
def run_ai():
    """
    This function establishes communication with the game manager. 
    It first introduces itself and receives its color. 
    Then it repeatedly receives the current score and current board state
    until the game is over. 
    """
    print("Otto") # First line is the name of this AI  
    color = int(input()) # Then we read the color: 1 for dark (goes first), 
                         # 2 for light.

    while True: # This is the main loop 
        # Read in the current game status, for example:
        # "SCORE 2 2" or "FINAL 33 31" if the game is over.
        # The first number is the score for player 1 (dark),
        # the second for player 2 (light)
        next_input = input() 
        status, dark_score_s, light_score_s = next_input.strip().split()
        dark_score = int(dark_score_s)
        light_score = int(light_score_s)

        if status == "FINAL": # Game is over. 
            #pickle.dump(cache, open("othello_storage.pcl", "wb"))
            print 
        else: 
            board = eval(input()) # Read in the input and turn it into a Python
                                  # object. The format is a list of rows. The 
                                  # squares in each row are represented by 
                                  # 0 : empty square
                                  # 1 : dark disk (player 1)
                                  # 2 : light disk (player 2)
                    
            start = time.time()
            # Select the move and send it to the manager 
            #movei, movej = select_move_minimax(board, color)
            movei, movej = select_move_alphabeta(board, color, start)
            print("{} {}".format(movei, movej)) 


if __name__ == "__main__":
    run_ai()
