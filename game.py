from ai import *
import tkinter as tk
import random
import csv
import time

def initialize_game(size=4):
    """
    Initializes the game board with a given size, filling all positions with zeros
    and placing two initial numbers.
    """
    board = [[0] * size for _ in range(size)]
    board = add_new_tile(board)
    board = add_new_tile(board)
    return board
def reverse(board):
    new_board = []
    for row in board:
        new_board.append(row[::-1])
    return new_board

def transpose(board):
    new_board = [list(row) for row in zip(*board)]
    return new_board

def add_new_tile(board):
    """
    Adds a new tile (2 or 4) to a randomly selected empty spot on the board.
    """
    size = len(board)
    empty_cells = [(r, c) for r in range(size) for c in range(size) if board[r][c] == 0]
    if empty_cells:
        row, col = random.choice(empty_cells)
        board[row][col] = 2 if random.random() < 0.9 else 4
    return board

def compress(board):
    """
    Compresses the board, moving all tiles to the left (removing empty spaces).
    """
    new_board = [[0] * len(board) for _ in range(len(board))]
    for row in range(len(board)):
        pos = 0
        for col in range(len(board)):
            if board[row][col] != 0:
                new_board[row][pos] = board[row][col]
                pos += 1
    return new_board

def merge(board):
    """
    Merges tiles with the same value that are next to each other (to the left).
    """
    for row in range(len(board)):
        for col in range(len(board)-1):
            if board[row][col] == board[row][col + 1] and board[row][col] != 0:
                board[row][col] *= 2
                board[row][col + 1] = 0
    return board

def move_left(board):
    """
    Makes a move to the left, combining the compress and merge operations.
    """
    board = compress(board)
    board = merge(board)
    board = compress(board)
    return board


def move_right(board):
    """
    Makes a move to the right by reversing, then moving left, then reversing back.
    """
    board = reverse(board)
    board = move_left(board)
    board = reverse(board)
    return board


def move_up(board):
    """
    Makes a move up by transposing, moving left, and transposing again.
    """
    board = transpose(board)
    board = move_left(board)
    board = transpose(board)
    return board


def move_down(board):
    """
    Makes a move down by transposing, moving right, and transposing again.
    """
    board = transpose(board)
    board = move_right(board)
    board = transpose(board)
    return board


def is_game_over(board):
    """
    Checks if there are no more valid moves left.
    """
    if any(0 in row for row in board):
        return False
    for row in range(len(board)):
        for col in range(len(board) - 1):
            if board[row][col] == board[row][col + 1] or board[col][row] == board[col + 1][row]:
                return False
    return True


class BaseGame2048(tk.Tk):
    """
    Base class for the 2048 game.

    Attributes:
        game_size (int): The size of the game board.
        board (list): The game board, represented as a 2D list of integers.
        grid_cells (list): A list of Tkinter labels that represent the game cells.
    """
    def __init__(self):
        super().__init__()
        self.title('2048 Game')
        self.game_size = 4  # Default game size
        self.board = initialize_game(self.game_size)
        self.grid_cells = []
        self.init_grid()
        self.update_grid_cells()

    def init_grid(self):
        """
        Initializes the game grid by creating Tkinter labels for each cell.
        """
        background = tk.Frame(self, bg='azure3', width=400, height=400)
        background.grid()
        for i in range(self.game_size):
            grid_row = []
            for j in range(self.game_size):
                cell = tk.Frame(background, bg='azure4', width=100, height=100)
                cell.grid(row=i, column=j, padx=5, pady=5)
                t = tk.Label(master=cell, text='', bg='azure4', justify=tk.CENTER, font=('Arial', 22, 'bold'), width=4, height=2)
                t.grid()
                grid_row.append(t)
            self.grid_cells.append(grid_row)

    def update_grid_cells(self):
        """
        Updates the contents of the game grid cells with the current game state.
        """
        for i in range(self.game_size):
            for j in range(self.game_size):
                if self.board[i][j] == 0:
                    self.grid_cells[i][j].configure(text='', bg='azure4')
                else:
                    self.grid_cells[i][j].configure(text=str(self.board[i][j]), bg='light goldenrod')
        self.update_idletasks()

    def game_over(self):
        """
        Displays a "Game Over" message when the game is over.
        """
        game_over_frame = tk.Frame(self, borderwidth=2)
        game_over_frame.place(relx=0.5, rely=0.5, anchor="center")
        tk.Label(game_over_frame, text='Game Over!', bg='red', font=('Arial', 20, 'bold')).pack()

class AI_Game2048(BaseGame2048):
    """
    A version of the 2048 game with an AI player.

    The AI player uses the minimax/expectimax algorithm with alpha-beta pruning to determine
    its moves.
    """
    
    def count_tiles(self, value):        
        return sum(row.count(value) for row in self.board)
    def calculate_score(self):
        """
        Calculates the score based on the occurrences of specific tiles.

        Args:
          board (list): A 2D list representing the game board.

        Returns:
            int: The calculated score.
        """
        tile_scores = {2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096}
        score = 0
        for row in self.board:
            for tile in row:
                if tile in tile_scores:
                    score += tile
        return score
    def write_statistics(self, algorithm):
        """
        Writes the statistics of the current game to a csv file.

        Args:
        algorithm (str): A string representing the name of the algorithm used.
        """
        stats = {
            "Algorithm": algorithm,
            "Moves": self.moves_made ,
            "Score": self.calculate_score(),
            "Nodes Expanded": self.nodes_expanded,
            "2048 Tiles": self.count_tiles(2048)+self.count_tiles(4096)*2,
            "1024 Tiles": self.count_tiles(1024),
            "512 Tiles": self.count_tiles(512),
            "128 Tiles": self.count_tiles(128),
            "64 Tiles": self.count_tiles(64),
        }
        with open("game_stats.csv", "a") as file:
            writer = csv.DictWriter(file, fieldnames=stats.keys())
            if file.tell() == 0:
                writer.writeheader()
            writer.writerow(stats)

    def auto_play_minimax(self):
        """
        The AI player's turn.

        This method uses the minimax algorithm with alpha-beta pruning to determine
        the best move, and then executes it. It then schedules the next move
        for a short delay. If the game is over, it displays a "Game Over" message.
        """
        if not hasattr(self, 'moves_made'):
            self.moves_made = 0  # Initialize counter if not already done
            self.nodes_expanded = 0  # Initialize nodes expanded counter 

        _, best_move, self.nodes_expanded = minimax(self.board, depth=5, is_player=True, nodes_expanded=self.nodes_expanded)  # Adjust depth as needed
        if best_move is not None:
            self.moves_made += 1
            self.board = best_move(self.board)  # Execute the best move
            self.board = add_new_tile(self.board)
            self.update_grid_cells()

            if not is_game_over(self.board):
                self.after(0, self.auto_play_minimax)  # Schedule the next move after a delay
            else:
                self.game_over()
                self.write_statistics("minimax")
        else:
            self.game_over()
            self.write_statistics("minimax")   

    def auto_play_expectimax(self):
        """
        The AI player's turn.

        This method uses the expectimax algorithm with alpha-beta pruning to determine
        the best move, and then executes it. It then schedules the next move
        for a short delay. If the game is over, it displays a "Game Over" message.
        """  
        if not hasattr(self, 'moves_made'):
            self.moves_made = 0  # Initialize counter if not already done
            self.nodes_expanded = 0  # Initialize nodes expanded counter 

        _, best_move, self.nodes_expanded = expectimax(self.board, depth=5, is_player=True, nodes_expanded=self.nodes_expanded)  # Adjust depth as needed
        if best_move is not None:
            self.moves_made += 1
            self.board = best_move(self.board)  # Execute the best move
            self.board = add_new_tile(self.board)
            self.update_grid_cells()

            if not is_game_over(self.board):
                self.after(0, self.auto_play_expectimax)  # Schedule the next move after a delay
            else:
                self.game_over()
                self.write_statistics("expectimax")
        else:
            self.game_over()
            self.write_statistics("expectimax")    


    def auto_play_expectimax_Epsilon(self):
        """
        The AI player's turn.

        This method uses the expectimax algorithm with alpha-beta pruning to determine
        the best move, and then executes it. It then schedules the next move
        for a short delay. If the game is over, it displays a "Game Over" message.
        """   
        if not hasattr(self, 'moves_made'):
            self.moves_made = 0  # Initialize counter if not already done
            self.nodes_expanded = 0  # Initialize nodes expanded counte

        _, best_move, self.nodes_expanded = expectimax_Epsilon(self.board, depth=5, is_player=True, nodes_expanded=self.nodes_expanded)  # Adjust depth as needed
        if best_move is not None:
            self.moves_made += 1
            self.board = best_move(self.board)  # Execute the best move
            self.board = add_new_tile(self.board)
            self.update_grid_cells()

            if not is_game_over(self.board):
                self.after(0, self.auto_play_expectimax_Epsilon)  # Schedule the next move after a delay
            else:
                self.game_over()
                self.write_statistics("expectimax_epsilon")
        else:
            self.game_over()  
            self.write_statistics("expectimax_epsilon")  

    def auto_play_expectiBetter(self):
        """
        The AI player's turn.

        This method uses the expectimax algorithm with alpha-beta pruning to determine
        the best move, and then executes it. It then schedules the next move
        for a short delay. If the game is over, it displays a "Game Over" message.
        """
        if not hasattr(self, 'moves_made'):
            self.moves_made = 0  # Initialize counter if not already done
            self.nodes_expanded = 0  # Initialize nodes expanded counter  
        depth=5
        max=max_tile(self.board)
        # if max >= 512:
        #     depth = 7
        if max >= 1024 and empty_cells(self.board) < 4:
            depth = 7
        _, best_move, self.nodes_expanded = expectiBetter(self.board, depth, is_player=True, nodes_expanded=self.nodes_expanded)  # Adjust depth as needed
        if best_move is not None:
            self.moves_made += 1
            self.board = best_move(self.board)  # Execute the best move
            self.board = add_new_tile(self.board)
            self.update_grid_cells()

            if not is_game_over(self.board):
                self.after(0, self.auto_play_expectiBetter)  # Schedule the next move after a delay
            else:
                self.game_over()
                self.write_statistics("expectibetter")

        else:
            self.game_over()
            self.write_statistics("expectibetter")   


class Auto_Game2048(BaseGame2048):
    """
    A version of the 2048 game with a human player.

    The human player can control the game using the arrow keys.
    """
    def __init__(self):
        super().__init__()
        self.bind("<Key>", self.key_press)

    def key_press(self, event):
        """
        Handles keyboard input from the human player.

        This method listens for keyboard input using the bind method, and
        updates the game state accordingly. If the game is over, it displays
        a "Game Over" message.
        """
        key = event.keysym
        if key == 'Up':
            self.board = move_up(self.board)
        elif key == 'Down':
            self.board = move_down(self.board)
        elif key == 'Left':
            self.board = move_left(self.board)
        elif key == 'Right':
            self.board = move_right(self.board)
        else:
            pass
        self.board = add_new_tile(self.board)
        self.update_grid_cells()
        if is_game_over(self.board):
            self.game_over()    

def start_human_game():
    """
    Starts a new game with a human player.
    """   
    human_game = Auto_Game2048()
    human_game.mainloop()

def start_ai_game_better_faster_stronger():
    """
    Starts a new game with an AI player (a star algorithm).
    """
    ai_game = AI_Game2048()  
    ai_game.auto_play_better_faster_stronger()

def start_ai_game_a_star():
    """
    Starts a new game with an AI player (a star algorithm).
    """
    ai_game = AI_Game2048()  
    ai_game.auto_play_a_star()

def start_ai_game_minimax():
    """
    Starts a new game with an AI player (minimax algorithm).
    """
    ai_game = AI_Game2048()  
    ai_game.auto_play_minimax()

def start_ai_game_expectimax():
    """
    Starts a new game with an AI player (expectimax algorithm).
    """
    ai_game = AI_Game2048()  
    ai_game.auto_play_expectimax()

def start_ai_game_expectimax_Epsilon():
    """
    Starts a new game with an AI player (expectimax algorithm).
    """
    ai_game = AI_Game2048()  
    ai_game.auto_play_expectimax_Epsilon()    

def start_ai_game_expectiBetter():
    """
    Starts a new game with an AI player (expectimax algorithm).
    """
    for i in range(1):
        ai_game = AI_Game2048()
        ai_game.auto_play_expectiBetter()

if __name__ == "__main__":
    #start_ai_game_expectiBetter()
    root = tk.Tk()
    root.title("2048 Game Modes")

    # Use colors that match the game's theme
    bg_color = "#bbada0"
    button_color = "#8f7a66"
    text_color = "#f9f6f2"
    font = ("Arial",18,"bold")
            

    # Set a matching background color
    root.configure(bg=bg_color)

    tk.Label(root, text="Choose Game Mode:", font=font, bg=bg_color, fg=text_color).pack(pady=20)

    human_button = tk.Button(root, text="Human Player", font=font, command=start_human_game, bg=button_color, fg=text_color)
    human_button.pack(fill='x', padx=15, pady=5)

    minimax_button = tk.Button(root, text="AI Player (minimax)", font=font, command=start_ai_game_minimax, bg=button_color, fg=text_color)
    minimax_button.pack(fill='x', padx=15, pady=5)

    expectimax_button = tk.Button(root, text="AI Player (expectimax)", font=font, command=start_ai_game_expectimax, bg=button_color, fg=text_color)
    expectimax_button.pack(fill='x', padx=15, pady=5)

    expectimax_Epsilon_button = tk.Button(root, text="AI Player (expectimax_Epsilon)", font=font, command=start_ai_game_expectimax_Epsilon, bg=button_color, fg=text_color)
    expectimax_Epsilon_button.pack(fill='x', padx=15, pady=5)

    b_button = tk.Button(root, text="AI Player (expectiBetter)", font=font, command=start_ai_game_expectiBetter, bg=button_color, fg=text_color)
    b_button.pack(fill='x', padx=15, pady=5)

    # Set window size to match the game window and center it on screen
    window_width = 400
    window_height = 500
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    center_x = int(screen_width/2 - window_width / 2)
    center_y = int(screen_height/2 - window_height / 2)
    root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

    root.mainloop()
    
