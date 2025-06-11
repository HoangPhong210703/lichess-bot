"""
Handling the AI moves.
"""
import random
import chess

piece_score = {"K": 0, "Q": 9, "R": 5, "B": 3, "N": 3, "p": 1}

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

piece_position_scores = {"wN": knight_scores,
                         "bN": knight_scores[::-1],
                         "wB": bishop_scores,
                         "bB": bishop_scores[::-1],
                         "wQ": queen_scores,
                         "bQ": queen_scores[::-1],
                         "wR": rook_scores,
                         "bR": rook_scores[::-1],
                         "wp": pawn_scores,
                         "bp": pawn_scores[::-1]}

CHECKMATE = 1000
STALEMATE = 0
DEPTH = 3


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
    board.pop() 

    return score

def quiescence_search(board: chess.Board, alpha: int, beta: int, turn_multiplier: int) -> int:
    """
    Performs a quiescence search to avoid the horizon effect.
    Only evaluates 'noisy' moves (captures, checks, promotions).
    """
    # 1. Stand-pat evaluation: If the current position is already good enough,
    # or it's a quiet position, return the static evaluation.
    # This is also the base case if no noisy moves are found.
    stand_pat = turn_multiplier * scoreBoard(board)
    if stand_pat >= beta:
        return beta # Prune this node, we've found a better path
    if alpha < stand_pat:
        alpha = stand_pat

    # Generate only "noisy" moves: captures and potentially promotions.
    # If the king is in check, ALL legal moves must be considered (evasions).
    noisy_moves = []
    if board.is_check():
        # If in check, all legal moves are "noisy" as they are forced responses.
        # It's important to order these too!
        moves_to_search = list(board.legal_moves)
        scored_moves = []
        for move in moves_to_search:
            score = score_move(board, move) # Reuse your move scoring for ordering
            scored_moves.append((score, move))
        scored_moves.sort(key=lambda x: x[0], reverse=True)
        noisy_moves = [move for score, move in scored_moves]
    else:
        # If not in check, only consider captures and promotions for quiescence
        for move in board.legal_moves:
            if board.is_capture(move) or move.promotion is not None:
                noisy_moves.append(move)
        
        # Order the noisy moves (captures and promotions first)
        # Re-using score_move is fine here as it prioritizes these.
        scored_noisy_moves = []
        for move in noisy_moves:
            score = score_move(board, move)
            scored_noisy_moves.append((score, move))
        scored_noisy_moves.sort(key=lambda x: x[0], reverse=True)
        noisy_moves = [move for score, move in scored_noisy_moves]

    for move in noisy_moves:
        board.push(move)
        # Recursively call quiescence search for these noisy moves
        # The depth doesn't explicitly decrease here, it continues until quiet.
        score = -quiescence_search(board, -beta, -alpha, -turn_multiplier)
        board.pop()

        if score >= beta:
            return beta  # Beta cutoff
        if score > alpha:
            alpha = score # Update alpha (best score found so far for this node)

    return alpha # Return the best score found for this node


# def findBestMove(board, valid_moves, return_queue):
#     global next_move
#     next_move = None
#     random.shuffle(valid_moves)
#     findMoveNegaMaxAlphaBeta(board, valid_moves, DEPTH, -CHECKMATE, CHECKMATE,
#                              1 if board.turn == chess.WHITE else -1)
#     return_queue.put(next_move)


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

    # Pass the ordered moves to the NegaMax function
    findMoveNegaMaxAlphaBeta(board, ordered_moves, DEPTH, -CHECKMATE, CHECKMATE,
                             1 if board.turn == chess.WHITE else -1)
    return_queue.put(next_move)


def findMoveNegaMaxAlphaBeta(board, valid_moves, depth, alpha, beta, turn_multiplier):
    global next_move
    
    # Base case for the main search: call quiescence search instead of static evaluation
    if depth == 0:
        return quiescence_search(board, alpha, beta, turn_multiplier) # <--- CHANGE HERE

    # No legal moves means checkmate or stalemate
    if not valid_moves:
        if board.is_checkmate():
            # Current player is checkmated, so previous player wins
            return -CHECKMATE
        elif board.is_stalemate():
            return STALEMATE
        return turn_multiplier * scoreBoard(board) # Should ideally not be reached if board is terminal

    max_score = -CHECKMATE # Use a very small number for initial max_score
    for move in valid_moves:
        board.push(move)
        next_moves = list(board.legal_moves)
        score = -findMoveNegaMaxAlphaBeta(board, next_moves, depth - 1, -beta, -alpha, -turn_multiplier)
        if score > max_score:
            max_score = score
            if depth == DEPTH: # Only update next_move at the root depth
                next_move = move
        board.pop()
        if max_score > alpha:
            alpha = max_score
        if alpha >= beta:
            break # Alpha-beta cutoff
    return max_score



def scoreBoard(board):
    """
    Score the board. A positive score is good for white, a negative score is good for black.
    """
    import chess
    
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
            piece_color = 'w' if piece.color == chess.WHITE else 'b'
            piece_key = piece_color + piece_type
            
            # Convert square to row/col for position scoring
            row = 7 - (square // 8)  # chess.py uses 0-63, we need 0-7 rows
            col = square % 8
            
            piece_position_score = 0
            if piece_type != "K":
                if piece_key in piece_position_scores:
                    piece_position_score = piece_position_scores[piece_key][row][col]
            
            if piece.color == chess.WHITE:
                score += piece_score[piece_type] + piece_position_score
            else:
                score -= piece_score[piece_type] + piece_position_score

    return score


def findRandomMove(valid_moves):
    """
    Picks and returns a random valid move.
    """
    return random.choice(valid_moves)
