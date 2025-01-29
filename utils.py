import os
import random
from typing import List, Dict
from texts import LOGO, RULES

# Constants
TABLE_SIZE: int = 6  # The size of the table (6x6)
GREEN_SQUARE: str = "🟩"  # Represents Player 1
RED_SQUARE: str = "🟥"    # Represents Player 2
WHITE_SQUARE: str = "🟨"  # Represents an empty square


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


def draw_square(square_number: int) -> str:
    """Converts a square's numeric value to its visual representation."""
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