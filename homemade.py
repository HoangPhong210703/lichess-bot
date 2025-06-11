"""
Some example classes for people who want to create a homemade bot.

With these classes, bot makers will not have to implement the UCI or XBoard interfaces themselves.
"""
import chess
import chess.polyglot
from chess.engine import PlayResult, Limit
import random 
from lib.engine_wrapper import MinimalEngine 
from lib.lichess_types import MOVE, HOMEMADE_ARGS_TYPE
import logging
from queue import Queue

logger = logging.getLogger(__name__)

class ExampleEngine(MinimalEngine):
    """An example engine that all homemade engines inherit."""
    pass

class RandomMove(ExampleEngine):
    """Get a random move."""
    def search(self, board: chess.Board, *args: HOMEMADE_ARGS_TYPE) -> PlayResult:
        """Choose a random move."""
        return PlayResult(random.choice(list(board.legal_moves)), None)


piece_score = {"K": 0, "Q": 9, "R": 5, "B": 3, "N": 3, "P": 1}

knight_scores = [[0.0, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1, 0.0],
                 [0.1, 0.3, 0.5, 0.5, 0.5, 0.5, 0.3, 0.1],
                 [0.2, 0.5, 0.6, 0.65, 0.65, 0.6, 0.5, 0.2],
                 [0.2, 0.55, 0.65, 0.7, 0.7, 0.65, 0.55, 0.2],
                 [0.2, 0.5, 0.65, 0.7, 0.7, 0.65, 0.5, 0.2],
                 [0.2, 0.55, 0.6, 0.65, 0.65, 0.6, 0.55, 0.2],
                 [0.1, 0.3, 0.5, 0.55, 0.55, 0.5, 0.3, 0.1],
                 [0.0, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1, 0.0]]

bishop_scores = [[0.0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.0],
                 [0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.2],
                 [0.2, 0.4, 0.5, 0.6, 0.6, 0.5, 0.4, 0.2],
                 [0.2, 0.5, 0.5, 0.6, 0.6, 0.5, 0.5, 0.2],
                 [0.2, 0.4, 0.6, 0.6, 0.6, 0.6, 0.4, 0.2],
                 [0.2, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.2],
                 [0.2, 0.5, 0.4, 0.4, 0.4, 0.4, 0.5, 0.2],
                 [0.0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.0]]

rook_scores = [[0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
               [0.5, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.5],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.25, 0.25, 0.25, 0.5, 0.5, 0.25, 0.25, 0.25]]

queen_scores = [[0.0, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2, 0.0],
                [0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.2],
                [0.2, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.2],
                [0.3, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.3],
                [0.4, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.3],
                [0.2, 0.5, 0.5, 0.5, 0.5, 0.5, 0.4, 0.2],
                [0.2, 0.4, 0.5, 0.4, 0.4, 0.4, 0.4, 0.2],
                [0.0, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2, 0.0]]

pawn_scores = [[0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8],
               [0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7],
               [0.3, 0.3, 0.4, 0.5, 0.5, 0.4, 0.3, 0.3],
               [0.25, 0.25, 0.3, 0.45, 0.45, 0.3, 0.25, 0.25],
               [0.2, 0.2, 0.2, 0.4, 0.4, 0.2, 0.2, 0.2],
               [0.25, 0.15, 0.1, 0.2, 0.2, 0.1, 0.15, 0.25],
               [0.25, 0.3, 0.3, 0.0, 0.0, 0.3, 0.3, 0.25],
               [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2]]

piece_position_scores = {"N": knight_scores,
                        "B": bishop_scores,
                        "Q": queen_scores,
                        "R": rook_scores,
                        "P": pawn_scores}

CHECKMATE = 1000
STALEMATE = 0
DEPTH = 4

# Constants for move scoring (added for move ordering)
CAPTURE_BONUS = 1000
PROMOTION_BONUS = 900
CHECK_BONUS = 50

def score_move(board: chess.Board, move: chess.Move) -> int:
    """
    Assign a score to a move based on heuristics.
    Higher score means better move.
    """
    score = 0

    # 1. Captures (MVV-LVA: Most Valuable Victim - Least Valuable Aggressor)
    if board.is_capture(move):
        # Get the piece being captured (victim)
        captured_piece_type = board.piece_type_at(move.to_square)
        captured_value = piece_score.get(chess.Piece(captured_piece_type, not board.turn).symbol().upper(), 0)

        # Get the piece making the capture (aggressor)
        moving_piece_type = board.piece_type_at(move.from_square)
        moving_value = piece_score.get(chess.Piece(moving_piece_type, board.turn).symbol().upper(), 0)

        # Calculate a score based on MVV-LVA. Higher value for captured piece, lower for moving piece.
        score += CAPTURE_BONUS + (captured_value * 10) - moving_value

    # 2. Promotions
    if move.promotion is not None:
        # Give a big bonus for promotion, especially to a queen
        promoted_value = piece_score.get(chess.Piece(move.promotion, board.turn).symbol().upper(), 0)
        score += PROMOTION_BONUS + promoted_value

    # 3. Checks
    # Temporarily make the move to see if it results in a check
    board.push(move)
    if board.is_check():
        score += CHECK_BONUS
    board.pop() # Undo the move

    return score


def findBestMove(board, valid_moves, return_queue):
    global next_move
    next_move = None

    # --- Start of Move Ordering ---
    # Create a list of (score, move) tuples
    scored_moves = []
    for move in valid_moves:
        score = score_move(board, move)
        scored_moves.append((score, move))

    # Sort moves in descending order of score
    # The 'key=lambda x: x[0]' tells sorted() to sort based on the first element of each tuple (the score)
    # 'reverse=True' ensures descending order (highest score first)
    scored_moves.sort(key=lambda x: x[0], reverse=True)

    # Extract only the moves in the new sorted order
    ordered_moves = [move for score, move in scored_moves]
    # --- End of Move Ordering ---

    findMoveNegaMaxAlphaBeta(board, ordered_moves, DEPTH, -CHECKMATE, CHECKMATE,
                             1 if board.turn == chess.WHITE else -1)
    return_queue.put(next_move)

def findMoveNegaMaxAlphaBeta(board, valid_moves, depth, alpha, beta, turn_multiplier):
    global next_move
    if depth == 0:
        return turn_multiplier * scoreBoard(board)
    
    max_score = -CHECKMATE
    for move in valid_moves: # Now iterates through ordered moves
        board.push(move)
        next_moves = list(board.legal_moves) # Legal moves are generated fresh for each new position
        # Recurse with the newly generated legal moves for the child node
        score = -findMoveNegaMaxAlphaBeta(board, next_moves, depth - 1, -beta, -alpha, -turn_multiplier)
        if score > max_score:
            max_score = score
            if depth == DEPTH: # Only update next_move at the root depth
                next_move = move
        board.pop() # Undo the move
        if max_score > alpha:
            alpha = max_score
        if alpha >= beta: # Alpha-beta cutoff
            break
    return max_score

def scoreBoard(board):
    """
    Score the board. A positive score is good for white, a negative score is good for black.
    """
    if board.is_checkmate():
        if board.turn == chess.WHITE:
            return -CHECKMATE  # black wins
        else:
            return CHECKMATE  # white wins
    elif board.is_stalemate():
        return STALEMATE
    
    score = 0
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece is not None:
            piece_type = piece.symbol().upper()
            
            # Convert square to row/col for position scoring
            row = 7 - (square // 8)  # chess.py uses 0-63, we need 0-7 rows
            col = square % 8
            
            piece_position_score = 0
            if piece_type != "K" and piece_type in piece_position_scores:
                position_table = piece_position_scores[piece_type]
                # For black pieces, flip the position table
                if piece.color == chess.BLACK:
                    position_table = position_table[::-1]
                piece_position_score = position_table[row][col]
            
            piece_value = piece_score.get(piece_type, 0)
            
            if piece.color == chess.WHITE:
                score += piece_value + piece_position_score
            else:
                score -= piece_value + piece_position_score

    return score

class ChessAI(MinimalEngine):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queue = Queue()
        self.book_path = "engines/books/Performance.bin" # Make sure this path is correct
        logger.info("ChessAI engine initialized")

    def search(self, board: chess.Board, time_limit: Limit, ponder: bool, draw_offered: bool, root_moves: MOVE) -> PlayResult:
        """
        Search for the best move in the current position.
        """
        # First try to get a move from the opening book
        try:
            with chess.polyglot.open_reader(self.book_path) as reader:
                entry = reader.get_weighted_choice(board)
                if entry is not None:
                    logger.info(f"Book move found: {entry.move}")
                    return PlayResult(entry.move, None, draw_offered=draw_offered)
        except Exception as e:
            logger.warning(f"Error reading opening book: {e}")

        # If no book move is found, use the engine
        # root_moves typically passed from the UCI/XBoard interface
        valid_moves = root_moves if isinstance(root_moves, list) else list(board.legal_moves)
        
        logger.debug(f"Searching for best move among {len(valid_moves)} moves")
        
        # Call the engine's findBestMove function
        # This will now use the sorted moves internally
        findBestMove(board, valid_moves, self.queue)
        best_move = self.queue.get()

        # If no move is found (shouldn't happen with legal_moves unless board is terminal),
        # make a random move as a fallback.
        if best_move is None:
            logger.warning("No best move found, selecting random move")
            # Ensure valid_moves is not empty before random.choice
            if valid_moves:
                best_move = random.choice(valid_moves)
            else:
                # This state implies no legal moves, e.g., checkmate or stalemate
                # In a real engine, you'd handle this by returning a resignation or draw
                logger.error("No legal moves available. Board is likely terminal.")
                return PlayResult(None, None, resign=True) # Or handle as a draw

        logger.info(f"Selected move: {best_move}")
        return PlayResult(best_move, None, draw_offered=draw_offered)

    def name(self) -> str:
        return "ChessAI"