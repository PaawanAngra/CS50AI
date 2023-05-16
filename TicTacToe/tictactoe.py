"""
Tic Tac Toe Player
"""

import math
import copy

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
    condition_empty = 1
    
    for row in board:
        for cell in row:
            if cell == X or cell == O:
                condition_empty = 0
    
    if condition_empty == 1:
        return X
    
    x_count = 0
    y_count = 0

    for row in board:
        for cell in row:
            if cell == X:
                x_count += 1
            if cell == O:
                y_count += 1
    
    if x_count > y_count:
        return O
    
    if y_count > x_count:
        return X

    return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    valid_actions = set()
    
    for i in range (3):
        for j in range (3):
            if board[i][j] == EMPTY:
                valid_actions.add((i,j))
    
    return valid_actions



def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    copy_board = copy.deepcopy(board)
    
    if copy_board [action[0]][action[1]] == X or copy_board [action[0]][action[1]] == O:
        raise NameError;"Invalid Action"
    
    player_turn = player (copy_board)
    copy_board[action[0]][action[1]] = player_turn

    return copy_board

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    #Checking rows
    for row in board:
        if (row[0] == X and row[1] == X and row[2] == X):
            return X
        if (row[0] == O and row[1] == O and row[2] == O):
            return O
    
    #Checking columns for X
    if (board[0][0] == X and board[1][0] == X and board[2][0] == X):
        return X

    if (board[0][1] == X and board[1][1] == X and board[2][1] == X):
        return X

    if (board[0][2] == X and board[1][2] == X and board[2][2] == X):
        return X
    
    #Checking columns for O
    if (board[0][0] == O and board[1][0] == O and board[2][0] == O):
        return O

    if (board[0][1] == O and board[1][1] == O and board[2][1] == O):
        return O

    if (board[0][2] == O and board[1][2] == O and board[2][2] == O):
        return O
    
    #Checking diagonals for X
    if (board[0][0] == X and board[1][1] == X and board[2][2] == X):
        return X

    if (board[0][2] == X and board[1][1] == X and board[2][0] == X):
        return X

    #Checking diagonals for O
    if (board[0][0] == O and board[1][1] == O and board[2][2] == O):
        return O

    if (board[0][2] == O and board[1][1] == O and board[2][0] == O):
        return O
    
    return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    win_player = winner(board)
    if (win_player != None):
        return True

    for row in board:
        for cell in row:
            if (cell == EMPTY):
                return False

    return True

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    win_player = winner(board)
    if (win_player == X):
        return 1
    
    if (win_player == O):
        return -1

    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if (terminal(board)):
        return None

    if (player(board) == X):
        maxu = -3
        result_action = (3,3)
        for action in actions(board):
            if minimax_helper(result(board, action)) > maxu:
                maxu = minimax_helper(result(board,action))
                result_action = action
        return result_action

    elif (player(board) == O):
        minu = 3
        result_action = (3,3)
        for action in actions(board):
            if (minimax_helper(result(board, action)) < minu):
                minu = minimax_helper(result(board, action))
                result_action = action
        return result_action

def minimax_helper(board):
    if (terminal(board)):
        return utility(board)

    if (player(board) == X):
        maxu = -3
        for action in actions(board):
            if (minimax_helper(result(board, action)) > maxu):
                maxu = minimax_helper(result(board, action))
        return maxu

    if (player(board) == O):
        minu = 3
        for action in actions(board):
            if (minimax_helper(result(board, action)) < minu):
                minu = minimax_helper(result(board, action))
        return minu

