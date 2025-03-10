from easyAI import TwoPlayerGame
import tkinter as tk
import random
import time

class TicTacToe(TwoPlayerGame):
    def __init__(self, starting_player, players=None):
        self.players = players
        self.board = [0 for _ in range(9)]  # Initialize empty board (0 = empty, 1 = X, 2 = O)
        self.current_player = starting_player  # Player 1 starts
        self.root = tk.Tk()
        self.root.title("Tic Tac Toe")
        self.buttons = []
        self.create_board()
        
        # Add log display
        self.log_text = tk.Text(self.root, height=5, width=40)
        self.log_text.grid(row=3, column=0, columnspan=3)

        self.winning_combo = None  # Store the winning combination

    def possible_moves(self):
        return [i + 1 for i, val in enumerate(self.board) if val == 0]

    def log_message(self, message):
        # Print to terminal
        print(message)
        # Add to GUI log
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
        # First check if game is already over
        print("BBBBB")
        if self.is_over():
            print("CCCCC")
            return "game_over"
        
        # Check if move is valid
        if self.board[int(move) - 1] != 0:
            self.log_message(f"Player {self.current_player} ({'X' if self.current_player == 1 else 'O'}) tried invalid move at position {move}")
            return False
        
        if not self._execute_move(move):  # Template method pattern
            return True
        
        # Check for win condition immediately after move
        if self.lose():  # Now checks if current player won with this move
            winner = f"Player {self.current_player} ({'X' if self.current_player == 1 else 'O'})"
            self.root.quit()
            return "game_over"
        elif 0 not in self.board:  # Check for draw
            self.root.quit()
            return "game_over"
        
        return True

    def _execute_move(self, move):
        """Template method to be overridden by child classes"""
        raise NotImplementedError

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
        
        # Check for current player's win (not opponent's)
        for combo in combinations:
            if all(self.board[i] == self.current_player for i in combo):
                self.winning_combo = combo
                return True
        return False

    def is_over(self):
        game_over = (self.lose() or (0 not in self.board))
        if game_over:
            self.update_display()  # Make sure final state is shown
        return game_over

    def show(self):
        # GUI handles the display, so we can skip console output
        pass

    def scoring(self):
        return -1 if self.lose() else 1

    def announce_winner(self):
        if self.winning_combo:
            winner = f"Player {self.current_player} ({'X' if self.current_player == 1 else 'O'})"
            self.log_message(f"Game Over! {winner} wins!")
            # Highlight winning combination
            for pos in self.winning_combo:
                self.buttons[pos].config(bg='light green')

    def play_move(self, move):
        result = self.make_move(move)
        print("AAAAA")
        if result != "game_over":
            self.switch_player()
        return result

    def switch_player(self):
        """Switch to next player (between 1 and 2)"""
        self.current_player = 3 - self.current_player  # Toggles between 1 and 2

class TicTacToeDeterministic(TicTacToe):
    def __init__(self, starting_player, players=None):
        super().__init__(starting_player, players)
        self.root.title("Tic Tac Toe - Deterministic")

    def _execute_move(self, move):
        self.board[int(move) - 1] = self.current_player
        symbol = "X" if self.current_player == 1 else "O"
        self.log_message(f"Player {self.current_player} ({symbol}) successfully placed {symbol} at position {move}")
        self.update_display()
        time.sleep(0.5)
        return True

class TicTacToeNonDeterministic(TicTacToe):
    def __init__(self, starting_player, players=None):
        super().__init__(starting_player, players)
        self.root.title("Tic Tac Toe - Non-Deterministic")

    def _execute_move(self, move):
        # Apply probability of failure
        if random.random() < 0.2:
            self.log_message(f"Player {self.current_player} ({'X' if self.current_player == 1 else 'O'})'s move at position {move} failed (20% chance)")
            time.sleep(0.5)
            return False
        
        self.board[int(move) - 1] = self.current_player
        symbol = "X" if self.current_player == 1 else "O"
        self.log_message(f"Player {self.current_player} ({symbol}) successfully placed {symbol} at position {move}")
        self.update_display()
        time.sleep(0.5)
        return True
