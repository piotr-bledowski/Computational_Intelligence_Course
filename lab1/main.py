from easyAI import TwoPlayerGame, AI_Player, Negamax
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
            return
            
        # Apply probability of failure
        if random.random() < 0.2:
            self.log_message(f"Player {self.current_player}'s move at position {move} failed (20% chance)")
            return
            
        self.board[int(move) - 1] = self.current_player
        symbol = "X" if self.current_player == 1 else "O"
        self.log_message(f"Player {self.current_player} successfully placed {symbol} at position {move}")
        self.update_display()
        time.sleep(2)

    def unmake_move(self, move):  # Required for the AI
        self.board[int(move) - 1] = 0

    def lose(self):
        # Returns True if the current player has lost
        combinations = [(0,1,2), (3,4,5), (6,7,8),  # Horizontal
                       (0,3,6), (1,4,7), (2,5,8),  # Vertical
                       (0,4,8), (2,4,6)]           # Diagonal
        
        return any([all([(self.board[i] == self.opponent_index) for i in combo])
                   for combo in combinations])

    def is_over(self):
        return (self.lose() or  # Game is lost
                (0 not in self.board))  # Board is full (draw)

    def show(self):
        # GUI handles the display, so we can skip console output
        pass

    def scoring(self):
        return -100 if self.lose() else 0

if __name__ == "__main__":
    # Initialize AI algorithm
    algorithm = Negamax(6)

    # Initialize players
    player1 = AI_Player(algorithm)
    player2 = AI_Player(algorithm)

    # Initialize and start the game
    game = TicTacToe([player1, player2])
    
    def game_loop():
        if not game.is_over():
            move = game.player.ask_move(game)
            game.play_move(move)
            game.root.after(100, game_loop)
        else:
            # Game over - wait a bit then close
            game.root.after(3000, game.root.destroy)
    
    # Start the game loop
    game.root.after(1000, game_loop)
    game.root.mainloop()
