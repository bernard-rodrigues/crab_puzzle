import os
import random
import time
from typing import List, Dict
from texts import LOGO, RULES

# Constants
TABLE_SIZE: int = 6  # The size of the table (6x6)
GREEN_SQUARE: str = "🟩"  # Represents Player 1
RED_SQUARE: str = "🟥"    # Represents Player 2
WHITE_SQUARE: str = "🟨"  # Represents an empty square

GREEN_CIRCLE: str = "🟢"
RED_CIRCLE: str = "🔴"
WHITE_CIRCLE: str = "🟡"


def show_logo() -> None:
    """Displays the game logo."""
    print(LOGO)


def choose_first_player() -> int:
    """Randomly chooses the first player (1 or 2).

    Returns:
        int: The player number (1 for Player 1, 2 for Player 2).
    """
    return random.choice((1, 2))


def clear_screen() -> None:
    """Clears the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def separator() -> None:
    """Prints a blank separator line."""
    print("\n")


def show_rules() -> None:
    """Displays the game rules."""
    clear_screen()
    print(RULES)
    input("Press Enter to continue...")


def draw_square(square_number: int, highlight: bool = False) -> str:
    """Converts a square's numeric value to its visual representation."""
    if highlight:
        return {0: WHITE_CIRCLE, 1: GREEN_CIRCLE, 2: RED_CIRCLE}.get(square_number, WHITE_CIRCLE)
    else:
        return {0: WHITE_SQUARE, 1: GREEN_SQUARE, 2: RED_SQUARE}.get(square_number, WHITE_SQUARE)


def translate_direction(direction: Dict[str, int]) -> str:
    """Translates a direction dictionary into a human-readable string."""
    directions = {(-1, 0): "up", (1, 0): "down", (0, -1): "left", (0, 1): "right"}
    return directions.get((direction.get('vertical', 0), direction.get('horizontal', 0)), "Invalid direction")


def create_initial_table() -> List[List[int]]:
    """Creates the initial game table with predefined positions for players."""
    table = [[0 for _ in range(TABLE_SIZE)] for _ in range(TABLE_SIZE)]
    positions = [(0, 0, 1), (0, 2, 2), (0, 3, 1), (0, 5, 2),
                 (2, 0, 2), (2, 5, 1), (3, 0, 1), (3, 5, 2),
                 (5, 0, 2), (5, 2, 1), (5, 3, 2), (5, 5, 1)]
    for row, col, player in positions:
        table[row][col] = player
    return table

def draw_table(table: List[List[int]]) -> None:
    """Displays the current state of the game table."""
    print("   A B C D E F")
    for row in range(TABLE_SIZE):
        print(row + 1, end=" ")
        for col in range(TABLE_SIZE):
            print(draw_square(table[row][col]), end="")
        print("")
    separator()

def draw_table_with_highlight(table: List[List[int]], highlight_pos: tuple[int, int] = None) -> None:
    """Displays the current state of the game table with optional highlight."""
    print("   A B C D E F")
    for row in range(TABLE_SIZE):
        print(row + 1, end=" ")
        for col in range(TABLE_SIZE):
            if highlight_pos and (row, col) == highlight_pos:
                # Highlight the current piece with a different color
                print(draw_square(table[row][col], highlight=True), end="")
            else:
                print(draw_square(table[row][col]), end="")
        print("")
    separator()

def get_available_moves(table: list[list[int]], row: int, col: int) -> list[dict[str, int]]:
    """Calculates all available moves for a piece at the given position."""
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    return [
        {'vertical': dr, 'horizontal': dc}
        for dr, dc in directions
        if 0 <= (new_row := row + dr) < TABLE_SIZE
        and 0 <= (new_col := col + dc) < TABLE_SIZE
        and table[new_row][new_col] == 0
    ]

def get_available_squares(table: list[list[int]], player: int) -> list[dict]:
    """Finds all squares with pieces belonging to the given player and their possible moves."""
    if player not in [1, 2]:
        raise ValueError("Player must be 1 or 2")
    
    return [
        {
            "square_position": {"row": row, "col": col},
            "available_moves": available_moves
        }
        for row in range(TABLE_SIZE)
        for col in range(TABLE_SIZE)
        if table[row][col] == player and (available_moves := get_available_moves(table, row, col))
    ]

def move_piece(table: list[list[int]], piece_position: dict[str, int], move_direction: dict[str, int], player: int) -> list[list[int]]:
    """Moves a piece in the specified direction until it hits an obstacle or the board limit."""
    row, col = piece_position['row'], piece_position['col']
    
    while True:
        new_row, new_col = row + move_direction['vertical'], col + move_direction['horizontal']
        if 0 <= new_row < TABLE_SIZE and 0 <= new_col < TABLE_SIZE and table[new_row][new_col] == 0:
            table[row][col], table[new_row][new_col] = 0, player
            row, col = new_row, new_col
        else:
            break
    
    return table

def animate_move_piece(table: list[list[int]], piece_position: dict[str, int], 
                      move_direction: dict[str, int], player: int) -> list[list[int]]:
    """Moves a piece with animation, showing each step of movement."""
    row, col = piece_position['row'], piece_position['col']
    original_table = [row[:] for row in table]  # Create a copy of the original table
    
    # Calculate the path before animation
    path = []
    current_row, current_col = row, col
    while True:
        new_row = current_row + move_direction['vertical']
        new_col = current_col + move_direction['horizontal']
        if (0 <= new_row < TABLE_SIZE and 
            0 <= new_col < TABLE_SIZE and 
            original_table[new_row][new_col] == 0):
            path.append((new_row, new_col))
            current_row, current_col = new_row, new_col
        else:
            break

    # Animate the movement
    for step_row, step_col in path:
        # Clear the previous position
        table[row][col] = 0
        # Set the new position
        table[step_row][step_col] = player
        
        # Clear screen and redraw
        clear_screen()
        draw_table(table)
        
        # Add a small delay for smooth animation
        time.sleep(0.15)
        
        # Update current position
        row, col = step_row, step_col
    
    return table

def check_winner(table: List[List[int]]) -> int:
    """Checks the game table for a winner."""
    # Check rows and columns
    for i in range(TABLE_SIZE):
        for j in range(TABLE_SIZE - 3):
            if table[i][j] != 0 and all(table[i][j] == table[i][j + k] for k in range(4)):
                return table[i][j]
            if table[j][i] != 0 and all(table[j][i] == table[j + k][i] for k in range(4)):
                return table[j][i]
    return 0