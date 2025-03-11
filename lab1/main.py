from easyAI import AI_Player, Negamax
#from easyAI.AI import TT
from easyAI.games import TicTacToe
from tictacdoh import TicTacDoh
import time
import itertools

def create_ai_algorithm(depth, use_pruning=True):
    """Create an AI algorithm with or without alpha-beta pruning"""
    if use_pruning:
        return Negamax(depth)  # Default Negamax uses alpha-beta pruning
    else:
        # Create Negamax without pruning by setting win_score very high
        return Negamax(depth, win_score=float('inf'))

def run_game(game_class, player1_config, player2_config, starting_player=1):
    # Unpack configurations
    p1_depth, p1_pruning = player1_config
    p2_depth, p2_pruning = player2_config

    # Initialize AI algorithms with different configurations
    algorithm1 = create_ai_algorithm(p1_depth, p1_pruning)
    algorithm2 = create_ai_algorithm(p2_depth, p2_pruning)

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
        
        current_player = 1 if game.player == player1 else 2
        move_times[current_player].append(end_time - start_time)
        
        game.play_move(move)

    avg_times = {
        1: sum(move_times[1]) / len(move_times[1]) if move_times[1] else 0,
        2: sum(move_times[2]) / len(move_times[2]) if move_times[2] else 0
    }

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
    pruning_options = [True, False]  # With and without alpha-beta pruning
    game_variants = [TicTacToe, TicTacDoh]
    results = {}
    
    for game_class in game_variants:
        game_type = "Regular" if game_class == TicTacToe else "Non-Deterministic"
        results[game_type] = {}
        
        # Test all combinations of depths and pruning options
        configs = list(itertools.product(depths, pruning_options))
        for p1_config, p2_config in itertools.product(configs, repeat=2):
            p1_depth, p1_pruning = p1_config
            p2_depth, p2_pruning = p2_config
            
            key = f"P1(d={p1_depth},{'ab' if p1_pruning else 'std'})-P2(d={p2_depth},{'ab' if p2_pruning else 'std'})"
            results[game_type][key] = []
            
            # Run 100 games with each player starting
            for starting_player in [1, 2]:
                for i in range(100):
                    starter = "P1" if starting_player == 1 else "P2"
                    print(f"\nRunning {game_type} Game {i+1}/100 with {key}, {starter} starts")
                    result = run_game(game_class, p1_config, p2_config, starting_player)
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
                
                total_games = len(outcomes)
                p1_wins = sum(1 for x in outcomes if x['winner'] == 1)
                p2_wins = sum(1 for x in outcomes if x['winner'] == 2)
                draws = sum(1 for x in outcomes if x['winner'] == 0)
                
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
