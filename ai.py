from game import move_left, move_right, move_up, move_down, is_game_over
import math
import random
def evaluate_board(board):
    """
    Calculates the score of the current state of the game.
    """
    tilemax = max_tile(board)
    max_tile_row, max_tile_col = max(((row, col) for row in range(len(board)) for col in range(len(board[row]))), key=lambda cell: board[cell[0]][cell[1]])

    smoothness_penalty = 0

    for row in range(len(board)):
        for column in range(len(board[row])):
            cell=board[row][column]
            if cell!=0:
                smoothness_penalty += math.log(cell,2)*(row+column)
    return empty_cells(board)*math.log(tilemax,2)- smoothness_penalty -(max_tile_col+max_tile_row)*math.log(tilemax,2)

def max_tile(board):
    """
    Finds the maximum tile value in the given board.

    Args:
        board (list): A 2D list representing the game board.

    Returns:
        int: The maximum tile value in the board.
    """
    return max(max(row) for row in board)

def empty_cells(board):

    return sum(row.count(0) for row in board)

def minimax(board, depth, is_player,nodes_expanded):
    """This function implements the minimax algorithm for the 2048 game.
    Parameters:
        board (List[List[int]]): The current game board
        depth (int): The current search depth
        is_player (bool): True if it is the player's turn, False if it is the computer's turn

    Returns:
        Tuple[float, Optional[Tuple[int, int]]]: A tuple containing the estimated score of the current board state and the best move, if available
    """   
    nodes_expanded += 1
    if depth == 0 or is_game_over(board):
        return evaluate_board(board), None,nodes_expanded # If the current depth is 0 or the game is over, return the score of the current state of the game and an empty list of possible moves. 
    
    if is_player:
        """
        If it is the AI's turn, determine the best move by recursively calling minimax for each possible move,
        keeping track of the best score and move.
        """
        best_score = float('-inf')
        best_move = None
        for move in [move_left, move_right, move_up, move_down]:
            new_board = move(board)
            if board!= new_board:
                score, _,nodes_expanded = minimax(new_board, depth-1, False,nodes_expanded)
                if score > best_score:
                    best_score = score
                    best_move = move
        return best_score, best_move,nodes_expanded
    else:
        """
        If it is the computer's turn, simulate the game's (random tile addition) move by recursively calling minimax
        for each possible value in the empty cells, keeping track of the best score.
        """
        best_score = float('inf')
        for row in range(len(board)):
            for col in range(len(board)):
                if board[row][col] == 0:
                    for value in [2, 4]:
                        board_copy = [row[:] for row in board]
                        board_copy[row][col] = value
                        score, _,nodes_expanded = minimax(board_copy, depth-1, True,nodes_expanded)
                        best_score = min(best_score, score)
        return best_score, None,nodes_expanded


def get_empty_cells(board):
    return [(r, c) for r in range(len(board)) for c in range(len(board[r])) if board[r][c] == 0]

def expectimax(board, depth, is_player,nodes_expanded):
    """
    This function implements the Expectimax algorithm for the 2048 game.

    Parameters:
    board (List[List[int]]): The current game board
    depth (int): The current search depth
    is_player (bool): True if it is the player's turn, False if it is the computer's turn

    Returns:
    Tuple[float, Optional[Tuple[int, int]]]: A tuple containing the estimated score of the current board state and the best move, if available
    """
    nodes_expanded += 1
    if depth == 0 or is_game_over(board):
        return evaluate_board(board), None, nodes_expanded

    if is_player:
        # If it is the player's turn, determine the best move by recursively calling expectimax for each possible move,
        # keeping track of the best score and move.
        best_score = float('-inf')
        best_move = None
        for move in [move_left, move_right, move_up, move_down]:
            new_board = move(board)
            if board != new_board:
                score, _,nodes_expanded = expectimax(new_board, depth - 1, False, nodes_expanded)
                if score > best_score:
                    best_score = score
                    best_move = move
        return best_score, best_move, nodes_expanded
    else:
        # If it is the computer's turn, simulate the game's (random tile addition) move by recursively calling expectimax
        # for each possible value in the empty cells, keeping track of the best score.
        avg_score = 0
        empty_cells = get_empty_cells(board)
        num_empty = len(empty_cells)
        if num_empty == 0:
            return score(board), None
        for cell in empty_cells:
            for value in [2, 4]:
                new_board = board.copy()
                new_board[cell[0]][cell[1]] = value
                result, _,nodes_expanded = expectimax(new_board, depth - 1, True, nodes_expanded)
                avg_score += result * (0.9 if value == 2 else 0.1)
        avg_score /= num_empty * 2
    
        return avg_score, None,nodes_expanded

def expectimax_Epsilon(board, depth, is_player,nodes_expanded):
    """
    This function implements the Expectimax algorithm with an epsilon-greedy approach for the 2048 game.

    Parameters:
    board (List[List[int]]): The current game board
    depth (int): The current search depth
    is_player (bool): True if it is the player's turn, False if it is the computer's turn

    Returns:
    Tuple[float, Optional[Tuple[int, int]]]: A tuple containing the estimated score of the current board state and the best move, if available
    """
    epsilon_min = 0.2  # Minimum epsilon value
    epsilon_max = 0.3  # Maximum epsilon value
    nodes_expanded += 1
    if depth == 0 or is_game_over(board):
        return evaluate_board(board), None, nodes_expanded

    epsilon = epsilon_max - epsilon_min * (depth / 10)  # Calculate epsilon based on the depth

    if is_player:
        best_score = float('-inf')
        best_move = None
        for move in [move_left, move_right, move_up, move_down]:
            new_board = move(board)
            if board != new_board:
                score, _,nodes_expanded = expectimax_Epsilon(new_board, depth - 1, False, nodes_expanded)
                if score > best_score:
                    best_score = score
                    best_move = move

                # Epsilon-greedy strategy
                if random.random() < epsilon:
                    best_move = random.choice([move_left, move_right, move_up, move_down])

        return best_score, best_move, nodes_expanded
    else:
        # If it is the computer's turn, simulate the game's (random tile addition) move by recursively calling expectimax
        # for each possible value in the empty cells, keeping track of the best score.
        avg_score = 0
        empty_cells = get_empty_cells(board)
        num_empty = len(empty_cells)
        if num_empty == 0:
            return score(board), None, nodes_expanded
        for cell in empty_cells:
            for value in [2, 4]:
                new_board = board.copy()
                new_board[cell[0]][cell[1]] = value
                result, _, nodes_expanded = expectimax(new_board, depth - 1, True, nodes_expanded)
                avg_score += result * (0.9 if value == 2 else 0.1)
        avg_score /= num_empty * 2
    
        return avg_score, None, nodes_expanded
    

def expectiBetter(board, depth, is_player, nodes_expanded):
    """
    This function implements the expectiBetter algorithm for the 2048 game.

    Parameters:
    board (List[List[int]]): The current game board
    depth (int): The current search depth
    is_player (bool): True if it is the player's turn, False if it is the computer's turn
    nodes_expanded (int): The number of nodes expanded during the search

    Returns:
    triple: A tuple containing the estimated score of the current board state, the best move, and the number of nodes expanded
    """
    if depth == 0 or is_game_over(board):
        return evaluate_board(board), None, nodes_expanded
    empty_cells=sum(row.count(0) for row in board)
    if depth ==5 and empty_cells>6:
        move = random.choice([move_left, move_up])
        return -1, move, nodes_expanded #should be without +1???

    if is_player:
        # If it is the player's turn, determine the best move by recursively calling expectiBetter for each possible move,
        # keeping track of the best score and move.
        best_score = float('-inf')
        best_move = None
        for move in [move_left, move_right, move_up, move_down]:
            new_board = move(board)
            nodes_expanded += 1
            if board != new_board:
                score, _ , nodes_expanded= expectiBetter(new_board, depth - 1, False, nodes_expanded)
                if score > best_score:
                    best_score = score
                    best_move = move
        return best_score, best_move, nodes_expanded
    else:
        # If it is the computer's turn, simulate the game's (random tile addition) move by recursively calling expectiBetter
        # for each possible value in the empty cells, keeping track of the best score.
        avg_score = 0
        empty_cells = get_empty_cells(board)
        num_empty = len(empty_cells)
        if num_empty == 0:
            return score(board), None
        for cell in empty_cells:
            for value in [2, 4]:
                new_board = board.copy()
                new_board[cell[0]][cell[1]] = value
                nodes_expanded += 1
                result, _ , nodes_expanded= expectiBetter(new_board, depth - 1, True, nodes_expanded)
                avg_score += result * (0.9 if value == 2 else 0.1)
        avg_score /= num_empty * 2
    

        return avg_score, None , nodes_expanded