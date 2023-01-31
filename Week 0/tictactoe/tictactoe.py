"""
Tic Tac Toe Player
"""

import copy
import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x_count = 0
    o_count = 0

    for row in board:
        x_count += row.count(X)
        o_count += row.count(O)
    
    if x_count == o_count:
        return X
    elif x_count > o_count:
        return O
    else:
        return None



def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    available_actions = []

    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] is EMPTY:
                available_actions.append(tuple((i, j)))

    return available_actions

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    
    for i in range(2):
        if action[i] < 0 or action[i] > 2:
            raise ValueError()
    
    board_copy = copy.deepcopy(board)
    current_player = player(board_copy)
    board_copy[action[0]][action[1]] = current_player
    return board_copy


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for row in board:
        if row.count(X) == 3:
            return X
        elif row.count(O) == 3:
            return O

    for i in range(3):    
        if [row[i] for row in board] == [X, X, X]:
            return X    
        if [row[i] for row in board] == [O, O, O]:
            return O
    
    if board[0][0] == X and board[1][1] == X and board[2][2] == X:
        return X
    elif board[0][2] == X and board[1][1] == X and board[2][0] == X:
        return X
    
    if board[0][0] == O and board[1][1] == O and board[2][2] == O:
        return O
    elif board[0][2] == O and board[1][1] == O and board[2][0] == O:
        return O
    
    return None
    

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    game_winner = winner(board)
    if(game_winner == X or game_winner == O):
        return True
    
    for row in board:
        if row.count(EMPTY) > 0:
            return False
    
    return True

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    game_winner = winner(board)
    if game_winner == X:
        return 1
    elif game_winner == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    current_player = player(board)
    possible_actions = actions(board)
 
    current_max_value = -999
    current_min_value = 999

    optimal_action = None
    
    if terminal(board):
        return None
    
    for action in possible_actions:
        if current_player == X:
            action_value = min_value(result(board, action))
            if action_value > current_max_value:
                current_max_value = action_value
                optimal_action = action
        else:
            action_value = max_value(result(board, action))
            if action_value < current_min_value:
                current_min_value = action_value
                optimal_action = action    
    
    return optimal_action


def max_value(board):
    v = -999
    if terminal(board):
        return utility(board)
    for action in actions(board):
        v = max(v, min_value(result(board, action)))
        if v == 1:
            return v
    return v

def min_value(board):
    v = 999
    if terminal(board):
        return utility(board)
    for action in actions(board):
        v = min(v, max_value(result(board, action)))
        if v == -1:
            return v
    return v 

def max(a, b):
    if a < b:
        return b
    else:
        return a

def min(a, b):
    if a > b:
        return b
    else:
        return a