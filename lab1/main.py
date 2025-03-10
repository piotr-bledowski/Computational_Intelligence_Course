from easyAI import AI_Player, Negamax
from easyAI.games import TicTacToe
from tictacdoh import TicTacDoh
import time

def run_game(game_class, starting_player):
    # Initialize AI algorithm
    algorithm = Negamax(15)

    # Initialize players
    player1 = AI_Player(algorithm)
    player2 = AI_Player(algorithm)

    # Initialize and start the game
    game = game_class([player1, player2])
    
    while not game.is_over():
        move = game.player.ask_move(game)
        game.play_move(move)

    # Return game result
    if game.lose():  # Using lose() from TwoPlayerGame
        winner = f"Player {game.opponent_index} ({'X' if game.opponent_index == 1 else 'O'})"
        return winner
    else:
        return "Draw"

def run_experiment():
    results = {
        "Regular": [],
        "Non-Deterministic": []
    }
    
    # Run 10 games for each variant
    for i in range(10):
        print(f"\nRunning Regular Game {i+1}/10")
        results["Regular"].append(run_game(TicTacToe, 1))  # Regular always starts with player 1
        time.sleep(1)  # Brief pause between games
        
        print(f"\nRunning Non-Deterministic Game {i+1}/10")
        results["Non-Deterministic"].append(run_game(TicTacDoh, 1))  # Non-deterministic starts with player 1
        time.sleep(1)
    
    # Save results to file
    with open('experiment_results.txt', 'w') as f:
        f.write("Experiment Results\n")
        f.write("=================\n\n")
        
        for variant, outcomes in results.items():
            f.write(f"{variant} Games:\n")
            f.write("-" * (len(variant) + 7) + "\n")
            for i, result in enumerate(outcomes, 1):
                f.write(f"Game {i}: {result}\n")
            
            # Calculate statistics
            total_games = len(outcomes)
            player1_wins = sum(1 for x in outcomes if "Player 1" in x)
            player2_wins = sum(1 for x in outcomes if "Player 2" in x)
            draws = sum(1 for x in outcomes if x == "Draw")
            
            f.write(f"\nStatistics:\n")
            f.write(f"Player 1 Wins: {player1_wins} ({player1_wins/total_games*100:.1f}%)\n")
            f.write(f"Player 2 Wins: {player2_wins} ({player2_wins/total_games*100:.1f}%)\n")
            f.write(f"Draws: {draws} ({draws/total_games*100:.1f}%)\n\n")

if __name__ == "__main__":
    run_experiment()
