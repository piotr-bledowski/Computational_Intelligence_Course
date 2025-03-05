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
            # Game over - wait a bit then close
            game.root.after(3000, game.root.destroy)
    
    # Start the game loop
    game.root.after(1000, game_loop)
    game.root.mainloop()
