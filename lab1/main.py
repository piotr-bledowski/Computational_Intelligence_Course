from easyAI import AI_Player, Negamax
from game import TicTacDoh

if __name__ == "__main__":
    # Initialize AI algorithm
    algorithm = Negamax(10)

    # Initialize players
    player1 = AI_Player(algorithm)
    player2 = AI_Player(algorithm)

    # Initialize and start the game
    game = TicTacDoh([player1, player2])
    
    def game_loop():
        if not game.is_over():
            move = game.player.ask_move(game)
            result = game.play_move(move)
            if result == "game_over":
                game.root.after(5000, game.root.destroy)
            else:
                game.root.after(100, game_loop)
    
    # Start the game loop
    game.root.after(1000, game_loop)
    game.root.mainloop()
