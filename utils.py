import os
import random
import numpy as np

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
    """Converts a square's numeric value to its visual representation.

    Args:
        square_number (int): The value of the square (0, 1, or 2).

    Returns:
        str: The square's visual representation (🟨, 🟩, 🟥).
    """
    match square_number:
        case 0:
            return WHITE_SQUARE
        case 1:
            return GREEN_SQUARE
        case 2:
            return RED_SQUARE


def translate_direction(direction: dict) -> str:
    """Translates a direction dictionary into a human-readable string.

    Args:
        direction (dict): A dictionary containing movement direction, 
                          with keys 'vertical' and 'horizontal'.

    Returns:
        str: A string describing the direction (up, down, left, right).

    Raises:
        ValueError: If the direction is invalid.
    """
    if direction['vertical'] == -1:
        return "up"
    if direction['vertical'] == 1:
        return "down"
    if direction['horizontal'] == -1:
        return "left"
    if direction['horizontal'] == 1:
        return "right"
    raise ValueError("Not a valid direction")


def create_initial_table() -> np.ndarray:
    """Creates the initial game table with predefined positions for players.

    Returns:
        np.ndarray: A 6x6 numpy array representing the game table.
    """
    table = np.zeros((TABLE_SIZE, TABLE_SIZE), dtype=int)

    # Initial positions for Player 1 (1) and Player 2 (2)
    table[0][0] = 1
    table[0][2] = 2
    table[0][3] = 1
    table[0][5] = 2
    table[2][0] = 2
    table[2][5] = 1
    table[3][0] = 1
    table[3][5] = 2
    table[5][0] = 2
    table[5][2] = 1
    table[5][3] = 2
    table[5][5] = 1

    return table


def draw_table(table: np.ndarray) -> None:
    """Displays the current state of the game table.

    Args:
        table (np.ndarray): A 6x6 numpy array representing the game table.
    """
    col_headers = (" ", " A", " B", " C", " D", " E", " F\n")
    for label in col_headers:
        print(label, end="")

    for row in range(TABLE_SIZE):
        print(row + 1, end="")
        for col in range(TABLE_SIZE):
            print(draw_square(table[row][col]), end="")
        print("")
    separator()


def check_winner(table: np.ndarray) -> int:
    """Checks the game table for a winner.

    Args:
        table (np.ndarray): A 6x6 numpy array representing the game table.

    Returns:
        int: The winning player number (1 or 2), or 0 if no winner is found.
    """
    # Check rows for a winner
    for row in range(TABLE_SIZE):
        counter = 0
        last_dot = 0
        for col in range(TABLE_SIZE):
            if table[row][col] == last_dot and table[row][col] != 0:
                counter += 1
            else:
                counter = 1
            last_dot = table[row][col]
            if counter == 4:  # Four consecutive pieces in a row
                return last_dot

    # Check columns for a winner
    for col in range(TABLE_SIZE):
        counter = 0
        last_dot = 0
        for row in range(TABLE_SIZE):
            if table[row][col] == last_dot and table[row][col] != 0:
                counter += 1
            else:
                counter = 1
            last_dot = table[row][col]
            if counter == 4:  # Four consecutive pieces in a column
                return last_dot

    # If no winner is found, return 0
    return 0