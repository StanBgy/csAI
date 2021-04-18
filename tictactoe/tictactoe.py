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
    turn = 0
    # for each action, turn += 1
    # can do that by taking board info
    for row in range(3):
        for col in range(3):
            if board[row][col] == EMPTY:
                turn += 1

    if turn % 2 != 0:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    moves = set()
    # define i and j, could be done as random?
    for row in range(len(board)):
        for col in range(len(board)):
            if board[row][col] == EMPTY:
                moves.add((row, col))

    return moves


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    new_board = copy.deepcopy(board)
    (i, j) = action
    if new_board[i][j] is not EMPTY:
        raise Exception("Illegal move")
    else:
        new_board[i][j] = player(board)

    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    numbers_of_x = 0
    numbers_of_o = 0
    for row in board:
        if row.count(X) == len(row):
            return X
        if row.count(O) == len(row):
            return O

    for col in range(len(board)):
        columns = []
        for row in board:
            columns.append(row[col])
        if columns.count(X) == len(row):
            return X
        if columns.count(O) == len(row):
            return O


    # onto diag
    if board[1][1] != 0:

        if board[1][1] == board[0][0] == board[2][2] == X:
            return X
        elif board[1][1] == board[0][0] == board[2][2] == O:
            return O
        elif board[1][1] == board[0][2] == board[2][0] == X:
            return X
        if board[1][1] == board[0][2] == board[2][0] == O:
            return O

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None or not actions(board):
        return True
    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """

    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    if player(board) is X:
        best_value = -math.inf
        for action in actions(board):
            value = min_value(result(board, action))
            if value > best_value:
                best_value = value
                best_action = action
    elif player(board) is O:
        best_value = math.inf
        for action in actions(board):
            value = max_value(result(board, action))
            if value < best_value:
                best_value = value
                best_action = action

    return best_action


def max_value(board):
    if terminal(board):
        return utility(board)
    v = -math.inf
    for action in actions(board):
        v = max(v, min_value(result(board, action)))
    return v


def min_value(board):
    if terminal(board):
        return utility(board)
    v = math.inf
    for action in actions(board):
        v = min(v, max_value(result(board, action)))
    return v
