from easyAI.games import TicTacToe
import random

class TicTacDoh(TicTacToe):
    """
    A non-deterministic version of TicTacToe where moves have a 20% chance to fail
    """
    def __init__(self, players):
        super().__init__(players)
        self.failure_rate = 0.20  # 20% chance of move failing

    def make_move(self, move):
        """
        Overrides the make_move method to add a chance of failure.
        If the move fails, switches the current player without making the move.
        """
        if random.random() < self.failure_rate:
            # Move fails, switch player and return
            self.switch_player()
            return
            
        # If no failure, proceed with normal move
        super().make_move(move)