import math
from typing import List, Dict
from utils import TABLE_SIZE, check_winner, get_available_squares, move_piece

def evaluate_board_normal(table: list[list[int]], player: int) -> int:
    """Assigns a score to the current board state."""
    opponent = 3 - player
    score = 0
    
    # Check rows and columns for potential wins
    for i in range(TABLE_SIZE):
        for j in range(TABLE_SIZE - 3):
            line = table[i][j:j+4]
            if line.count(player) == 4:
                return 1000  # AI wins
            elif line.count(opponent) == 4:
                return -1000  # Opponent wins
            elif line.count(player) == 3 and line.count(0) == 1:
                score += 10
            elif line.count(opponent) == 3 and line.count(0) == 1:
                score -= 10
    
    return score


def minimax_normal(table: list[list[int]], depth: int, alpha: int, beta: int, maximizing: bool, player: int) -> tuple[int, dict]:
    """Minimax algorithm with alpha-beta pruning."""
    opponent = 3 - player
    winner = check_winner(table)
    if winner == player:
        return 1000, {}
    elif winner == opponent:
        return -1000, {}
    elif depth == 0:
        return evaluate_board_normal(table, player), {}
    
    best_move = {}
    
    if maximizing:
        max_eval = -math.inf
        for move in get_available_squares(table, player):
            for direction in move['available_moves']:
                new_table = move_piece([row[:] for row in table], move['square_position'], direction, player)
                eval_score, _ = minimax_normal(new_table, depth - 1, alpha, beta, False, player)
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = {'piece': move['square_position'], 'direction': direction}
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
        return max_eval, best_move
    else:
        min_eval = math.inf
        for move in get_available_squares(table, opponent):
            for direction in move['available_moves']:
                new_table = move_piece([row[:] for row in table], move['square_position'], direction, opponent)
                eval_score, _ = minimax_normal(new_table, depth - 1, alpha, beta, True, player)
                if eval_score < min_eval:
                    min_eval = eval_score
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
        return min_eval, {}


def ai_best_move_normal(table: list[list[int]], player: int) -> dict:
    """Determines the AI's best move using Minimax."""
    _, best_move = minimax_normal(table, depth=3, alpha=-math.inf, beta=math.inf, maximizing=True, player=player)
    return best_move

def evaluate_board_hard(table: list[list[int]], player: int) -> int:
    """Enhanced board evaluation function."""
    opponent = 3 - player
    score = 0
    
    # Weights for different patterns
    WEIGHTS = {
        'win': 10000,
        'three_in_row': 100,
        'two_in_row': 10,
        'center_control': 5,
        'mobility': 2,
    }
    
    def count_consecutive(line: List[int], player: int) -> Dict[str, int]:
        """Count consecutive pieces and gaps in a line."""
        counts = {'three': 0, 'two': 0, 'gaps': 0}
        for i in range(len(line) - 3):
            window = line[i:i+4]
            player_count = window.count(player)
            empty_count = window.count(0)
            
            if player_count == 3 and empty_count == 1:
                counts['three'] += 1
            elif player_count == 2 and empty_count == 2:
                counts['two'] += 1
                
            if empty_count > 0:
                counts['gaps'] += empty_count
        return counts

    # Check horizontal lines
    for row in range(TABLE_SIZE):
        for col in range(TABLE_SIZE - 3):
            line = [table[row][col + i] for i in range(4)]
            
            # Check for immediate wins
            if line.count(player) == 4:
                return WEIGHTS['win']
            elif line.count(opponent) == 4:
                return -WEIGHTS['win']
            
            # Count patterns for both players
            player_counts = count_consecutive(line, player)
            opponent_counts = count_consecutive(line, opponent)
            
            score += (player_counts['three'] * WEIGHTS['three_in_row']
                     + player_counts['two'] * WEIGHTS['two_in_row']
                     - opponent_counts['three'] * WEIGHTS['three_in_row']
                     - opponent_counts['two'] * WEIGHTS['two_in_row'])

    # Check vertical lines
    for col in range(TABLE_SIZE):
        for row in range(TABLE_SIZE - 3):
            line = [table[row + i][col] for i in range(4)]
            
            # Check for immediate wins
            if line.count(player) == 4:
                return WEIGHTS['win']
            elif line.count(opponent) == 4:
                return -WEIGHTS['win']
            
            # Count patterns for both players
            player_counts = count_consecutive(line, player)
            opponent_counts = count_consecutive(line, opponent)
            
            score += (player_counts['three'] * WEIGHTS['three_in_row']
                     + player_counts['two'] * WEIGHTS['two_in_row']
                     - opponent_counts['three'] * WEIGHTS['three_in_row']
                     - opponent_counts['two'] * WEIGHTS['two_in_row'])

    # Evaluate center control (pieces in the central 2x2 area)
    center_pieces = sum(1 for i in range(2, 4) for j in range(2, 4) if table[i][j] == player)
    score += center_pieces * WEIGHTS['center_control']

    # Evaluate mobility (available moves)
    player_mobility = len(get_available_squares(table, player))
    opponent_mobility = len(get_available_squares(table, opponent))
    score += (player_mobility - opponent_mobility) * WEIGHTS['mobility']

    return score

def minimax_hard(table: list[list[int]], depth: int, alpha: int, beta: int, maximizing: bool, 
           player: int, max_depth: int) -> tuple[int, dict]:
    """Enhanced minimax algorithm with alpha-beta pruning and dynamic depth."""
    opponent = 3 - player
    winner = check_winner(table)
    
    # Terminal states
    if winner == player:
        return 10000 + depth, {}  # Prefer winning sooner
    elif winner == opponent:
        return -10000 - depth, {}  # Prefer losing later
    elif depth == 0:
        return evaluate_board_hard(table, player), {}

    best_move = {}
    
    if maximizing:
        max_eval = -math.inf
        moves = get_available_squares(table, player)
        
        # Sort moves by preliminary evaluation for better pruning
        moves.sort(key=lambda m: preliminary_evaluate_move(table, m, player), reverse=True)
        
        for move in moves:
            for direction in move['available_moves']:
                new_table = move_piece([row[:] for row in table], move['square_position'], direction, player)
                
                # Adaptive depth based on game phase
                current_depth = depth
                if len(moves) < 3 and depth < max_depth:  # Fewer moves available, search deeper
                    current_depth += 1
                
                eval_score, _ = minimax_hard(new_table, current_depth - 1, alpha, beta, False, player, max_depth)
                
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = {'piece': move['square_position'], 'direction': direction}
                
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
        
        return max_eval, best_move
    else:
        min_eval = math.inf
        moves = get_available_squares(table, opponent)
        
        # Sort moves by preliminary evaluation for better pruning
        moves.sort(key=lambda m: preliminary_evaluate_move(table, m, opponent), reverse=True)
        
        for move in moves:
            for direction in move['available_moves']:
                new_table = move_piece([row[:] for row in table], move['square_position'], direction, opponent)
                eval_score, _ = minimax_hard(new_table, depth - 1, alpha, beta, True, player, max_depth)
                
                if eval_score < min_eval:
                    min_eval = eval_score
                
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
        
        return min_eval, {}

def preliminary_evaluate_move(table: list[list[int]], move: dict, player: int) -> int:
    """Quick evaluation of a move for move ordering."""
    score = 0
    row, col = move['square_position']['row'], move['square_position']['col']
    
    # Prefer central positions
    score += (3 - abs(row - 2.5)) + (3 - abs(col - 2.5))
    
    # Prefer moves that can create or block winning patterns
    for direction in move['available_moves']:
        new_table = move_piece([row[:] for row in table], move['square_position'], direction, player)
        if check_winner(new_table) == player:
            score += 1000
    
    return score

def ai_best_move_hard(table: list[list[int]], player: int) -> dict:
    """Determines the AI's best move using enhanced Minimax."""
    # Increase depth for more challenging gameplay
    base_depth = 4
    
    # Adjust depth based on game phase
    available_moves = sum(1 for row in table for cell in row if cell == 0)
    if available_moves < 10:  # End game
        base_depth += 1
    
    _, best_move = minimax_hard(table, base_depth, -math.inf, math.inf, True, player, base_depth + 2)
    return best_move