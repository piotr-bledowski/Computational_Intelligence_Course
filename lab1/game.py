from easyAI import TwoPlayerGame
import tkinter as tk
import random
import time

class TicTacToe(TwoPlayerGame):
    def __init__(self, players=None):
        self.players = players
        self.board = [0 for _ in range(9)]  # Initialize empty board (0 = empty, 1 = X, 2 = O)
        self.current_player = 1  # Player 1 starts
        self.root = tk.Tk()
        self.root.title("Tic Tac Toe")
        self.buttons = []
        self.create_board()
        
        # Add log display
        self.log_text = tk.Text(self.root, height=5, width=40)
        self.log_text.grid(row=3, column=0, columnspan=3)

        self.winning_combo = None  # Store the winning combination

    def log_message(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.root.update()

    def create_board(self):
        for i in range(3):
            for j in range(3):
                button = tk.Button(self.root, text="", width=10, height=4,
                                 command=lambda x=i*3+j: self.button_click(x))
                button.grid(row=i, column=j)
                self.buttons.append(button)

    def update_display(self):
        for i, val in enumerate(self.board):
            text = "X" if val == 1 else "O" if val == 2 else ""
            self.buttons[i].config(text=text)
        self.root.update()

    def possible_moves(self):
        return [i + 1 for i, val in enumerate(self.board) if val == 0]

    def make_move(self, move):
        # Check if move is valid
        if self.board[int(move) - 1] != 0:
            self.log_message(f"Player {self.current_player} tried invalid move at position {move}")
            return False  # Return False to indicate move wasn't made
            
        # Apply probability of failure
        if random.random() < 0.2:
            self.log_message(f"Player {self.current_player}'s move at position {move} failed (20% chance)")
            return True  # Return True to indicate turn should end
            
        self.board[int(move) - 1] = self.current_player
        symbol = "X" if self.current_player == 1 else "O"
        self.log_message(f"Player {self.current_player} successfully placed {symbol} at position {move}")
        self.update_display()
        time.sleep(2)
        return True  # Return True to indicate turn should end

    def unmake_move(self, move):  # Required for AI's internal calculations
        # Create a copy of the board for AI calculations
        board_copy = self.board.copy()
        self.board[int(move) - 1] = 0
        result = self.scoring()  # Get the score
        self.board = board_copy  # Restore the actual board
        return result

    def lose(self):
        combinations = [(0,1,2), (3,4,5), (6,7,8),  # Horizontal
                       (0,3,6), (1,4,7), (2,5,8),  # Vertical
                       (0,4,8), (2,4,6)]           # Diagonal
        
        for combo in combinations:
            if all(self.board[i] == self.opponent_index for i in combo):
                self.winning_combo = combo
                return True
        return False

    def is_over(self):
        return (self.lose() or  # Game is lost
                (0 not in self.board))  # Board is full (draw)

    def show(self):
        # GUI handles the display, so we can skip console output
        pass

    def scoring(self):
        return -100 if self.lose() else 0

    def announce_winner(self):
        if self.winning_combo:
            winner = "Player 1 (X)" if self.opponent_index == 1 else "Player 2 (O)"
            self.log_message(f"Game Over! {winner} wins!")
            # Highlight winning combination
            for pos in self.winning_combo:
                self.buttons[pos].config(bg='light green')
        elif self.is_over():  # Board is full but no winner
            self.log_message("Game Over! It's a draw!")