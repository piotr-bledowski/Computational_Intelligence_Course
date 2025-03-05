from easyAI import AI_Player, Negamax
from game import TicTacToe

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
            # Announce winner before closing
            game.announce_winner()
            game.root.after(5000, game.root.destroy)  # Extended to 5 seconds to read the result
    
    # Start the game loop
    game.root.after(1000, game_loop)
    game.root.mainloop()
