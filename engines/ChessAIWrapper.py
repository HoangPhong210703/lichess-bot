import chess
from chess.engine import PlayResult, Limit
from lib.engine_wrapper import MinimalEngine
from lib.lichess_types import MOVE, HOMEMADE_ARGS_TYPE
import logging
from queue import Queue
from . import ChessAI

logger = logging.getLogger(__name__)

class ChessAIEngine(MinimalEngine):
    """
    Wrapper for ChessAI to make it compatible with lichess-bot
    """
    def __init__(self, commands, options, stderr, draw_or_resign, name=None, **popen_args):
        super().__init__(commands, options, stderr, draw_or_resign, name, **popen_args)
        self.queue = Queue()
        logger.info("ChessAI engine initialized")

    def search(self, board: chess.Board, time_limit: Limit, ponder: bool, draw_offered: bool, root_moves: MOVE) -> PlayResult:
        """
        Search for the best move in the current position.
        
        :param board: The current position
        :param time_limit: Time constraints for the search
        :param ponder: Whether the engine can ponder
        :param draw_offered: Whether the opponent offered a draw
        :param root_moves: If it is a list, only these moves can be played
        :return: The move to play
        """
        # Get valid moves, considering root_moves if specified
        valid_moves = root_moves if isinstance(root_moves, list) else list(board.legal_moves)
        
        logger.debug(f"Searching for best move among {len(valid_moves)} moves")
        
        # Call the engine's findBestMove function
        ChessAI.findBestMove(board, valid_moves, self.queue)
        best_move = self.queue.get()

        # If no move is found, make a random move
        if best_move is None:
            logger.warning("No best move found, selecting random move")
            best_move = ChessAI.findRandomMove(valid_moves)
        
        logger.info(f"Selected move: {best_move}")
        return PlayResult(best_move, None, draw_offered=draw_offered)

    def get_opponent_info(self, game):
        pass  # Optional: Implement if you want to use opponent's info

    def name(self) -> str:
        return "ChessAI"  # Your engine's name

    def report_game_result(self, game, board):
        pass  # Optional: Implement to handle game results

    def quit(self):
        pass  # Optional: Implement if you need cleanup on exit
