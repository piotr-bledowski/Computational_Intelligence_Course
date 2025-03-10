from easyAI import AI_Player, Negamax
from easyAI.games import TicTacToe
from tictacdoh import TicTacDoh
import time
import itertools

def run_game(game_class, player1_depth, player2_depth, starting_player=1):
    # Initialize AI algorithms with different depths
    algorithm1 = Negamax(player1_depth)
    algorithm2 = Negamax(player2_depth)

    # Initialize players
    player1 = AI_Player(algorithm1)
    player2 = AI_Player(algorithm2)
    
    # Set players in the order determined by starting_player
    players = [player1, player2] if starting_player == 1 else [player2, player1]

    # Initialize timing stats
    move_times = {1: [], 2: []}
    
    # Initialize and start the game
    game = game_class(players)
    
    while not game.is_over():
        start_time = time.time()
        move = game.player.ask_move(game)
        end_time = time.time()
        
        # Record move time for current player
        # Map the current game player back to our original player numbers
        current_player = 1 if game.player == player1 else 2
        move_times[current_player].append(end_time - start_time)
        
        game.play_move(move)

    # Calculate average move times
    avg_times = {
        1: sum(move_times[1]) / len(move_times[1]) if move_times[1] else 0,
        2: sum(move_times[2]) / len(move_times[2]) if move_times[2] else 0
    }

    # Determine winner based on original player assignments
    if game.lose():
        winner = 1 if game.player == player2 else 2
    else:
        winner = 0  # Draw
    
    return {
        'winner': winner,
        'avg_times': avg_times,
        'total_moves': len(move_times[1]) + len(move_times[2])
    }

def run_experiment():
    depths = [2, 4, 6]  # Testing different depths for Negamax
    game_variants = [TicTacToe, TicTacDoh]
    results = {}
    
    # Test all combinations of depths for both players
    for game_class in game_variants:
        game_type = "Regular" if game_class == TicTacToe else "Non-Deterministic"
        results[game_type] = {}
        
        for d1, d2 in itertools.product(depths, repeat=2):
            key = f"P1(d={d1})-P2(d={d2})"
            results[game_type][key] = []
            
            # Run 100 games with each player starting
            for starting_player in [1, 2]:
                for i in range(100):
                    starter = "P1" if starting_player == 1 else "P2"
                    print(f"\nRunning {game_type} Game {i+1}/100 with {key}, {starter} starts")
                    result = run_game(game_class, d1, d2, starting_player)
                    results[game_type][key].append(result)

    # Save results to file
    with open('experiment_results.txt', 'w') as f:
        f.write("Experiment Results\n")
        f.write("=================\n\n")
        
        for variant, configs in results.items():
            f.write(f"{variant} Games:\n")
            f.write("-" * (len(variant) + 7) + "\n\n")
            
            for config, outcomes in configs.items():
                f.write(f"Configuration: {config}\n")
                f.write("-" * (len(config) + 14) + "\n")
                
                # Calculate combined statistics for all 20 games
                total_games = len(outcomes)
                p1_wins = sum(1 for x in outcomes if x['winner'] == 1)
                p2_wins = sum(1 for x in outcomes if x['winner'] == 2)
                draws = sum(1 for x in outcomes if x['winner'] == 0)
                
                # Calculate average move times across all games
                p1_avg_time = sum(x['avg_times'][1] for x in outcomes) / total_games
                p2_avg_time = sum(x['avg_times'][2] for x in outcomes) / total_games
                avg_moves = sum(x['total_moves'] for x in outcomes) / total_games
                
                f.write(f"Total Games: {total_games}\n")
                f.write(f"Player 1 Wins: {p1_wins} ({p1_wins/total_games*100:.1f}%)\n")
                f.write(f"Player 2 Wins: {p2_wins} ({p2_wins/total_games*100:.1f}%)\n")
                f.write(f"Draws: {draws} ({draws/total_games*100:.1f}%)\n")
                f.write(f"Average Moves per Game: {avg_moves:.1f}\n")
                f.write(f"Average Move Time - Player 1: {p1_avg_time*1000:.1f}ms\n")
                f.write(f"Average Move Time - Player 2: {p2_avg_time*1000:.1f}ms\n")
                f.write("\n" + "="*50 + "\n\n")

if __name__ == "__main__":
    run_experiment()
