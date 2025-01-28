from utils import (
    GREEN_SQUARE, RED_SQUARE, TABLE_SIZE, check_winner,
    choose_first_player, clear_screen, create_initial_table,
    draw_table, show_logo, translate_direction
)

COL_HEADERS = ("A", "B", "C", "D", "E", "F")
MENU_OPTIONS = ("START", "SHOW RULES", "EXIT")


def show_menu() -> int:
    """
    Displays the main menu and prompts the user to select an option.
    Returns the selected menu option as an integer.
    """
    clear_screen()
    show_logo()
    option = 0

    while option not in range(1, len(MENU_OPTIONS) + 1):
        for index, option_text in enumerate(MENU_OPTIONS, start=1):
            print(f"{index}. {option_text}")

        option = int(input("Choose an option: "))

    return option


def get_available_moves(table: list[list[int]], row: int, col: int) -> list[dict[str, int]]:
    """
    Calculates all available moves for a piece at the given position.

    Args:
        table (list[list[int]]): The game board.
        row (int): The row of the piece.
        col (int): The column of the piece.

    Returns:
        list[dict[str, int]]: A list of possible moves, each represented as a dictionary with 'vertical' and 'horizontal' keys.
    """
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # up, down, left, right
    available_moves = []

    for dr, dc in moves:
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < TABLE_SIZE and 0 <= new_col < TABLE_SIZE:  # Within bounds
            if table[new_row][new_col] == 0:  # Check if the square is empty
                available_moves.append({'vertical': dr, 'horizontal': dc})
    return available_moves


def get_available_squares(table: list[list[int]], player: int) -> list[dict]:
    """
    Finds all squares with pieces belonging to the given player and calculates their possible moves.

    Args:
        table (list[list[int]]): The game board.
        player (int): The player (1 or 2).

    Returns:
        list[dict]: A list of dictionaries with square positions and available moves.
    """
    if player not in [1, 2]:
        raise ValueError("Player must be 1 or 2")

    available_squares = []

    for row in range(TABLE_SIZE):
        for col in range(TABLE_SIZE):
            if table[row][col] == player:
                available_moves = get_available_moves(table, row, col)
                if available_moves:
                    available_squares.append({
                        "square_position": {"row": row, "col": col},
                        "available_moves": available_moves
                    })
    return available_squares


def move_piece(table: list[list[int]], piece_position: dict[str, int], move_direction: dict[str, int], player: int) -> list[list[int]]:
    """
    Moves a piece in the specified direction until it hits an obstacle or the board limit.

    Args:
        table (list[list[int]]): The game board.
        piece_position (dict[str, int]): The starting position of the piece.
        move_direction (dict[str, int]): The direction to move ('vertical' and 'horizontal').
        player (int): The player making the move.

    Returns:
        list[list[int]]: The updated game board.
    """
    row, col = piece_position['row'], piece_position['col']

    while True:
        new_row = row + move_direction['vertical']
        new_col = col + move_direction['horizontal']

        # Check if the move stays within bounds and ends on an empty square
        if 0 <= new_row < TABLE_SIZE and 0 <= new_col < TABLE_SIZE:
            if table[new_row][new_col] == 0:  # Square is empty
                table[row][col] = 0
                table[new_row][new_col] = player
                row, col = new_row, new_col
            else:
                break
        else:
            break

    return table


def handle_next_move(table: list[list[int]], available_squares: list[dict], player: int) -> list[list[int]]:
    """
    Handles a player's move, prompting them to choose a piece and a direction to move.

    Args:
        table (list[list[int]]): The game board.
        available_squares (list[dict]): List of squares with pieces that can be moved.
        player (int): The player making the move.

    Returns:
        list[list[int]]: The updated game board.
    """
    # Display available pieces to move
    for index, square in enumerate(available_squares, start=1):
        row = square['square_position']['row'] + 1
        col = COL_HEADERS[square['square_position']['col']]
        print(f"{index}: {col}{row}")

    # Prompt the player to choose a piece
    chosen_piece_index = 0
    while chosen_piece_index not in range(1, len(available_squares) + 1):
        chosen_piece_index = int(input("Choose the piece you'd like to move: "))

    chosen_piece = available_squares[chosen_piece_index - 1]

    # Display available directions to move
    for index, direction in enumerate(chosen_piece['available_moves'], start=1):
        print(f"{index}: {translate_direction(direction)}")

    # Prompt the player to choose a direction
    chosen_direction_index = 0
    while chosen_direction_index not in range(1, len(chosen_piece['available_moves']) + 1):
        chosen_direction_index = int(input("Choose the direction you'd like to move: "))

    chosen_direction = chosen_piece['available_moves'][chosen_direction_index - 1]

    return move_piece(table, chosen_piece['square_position'], chosen_direction, player)


def game_start() -> None:
    """
    Starts and manages the main game loop until a winner is determined.
    """
    clear_screen()
    table = create_initial_table()
    current_player = choose_first_player()
    winner = 0

    while True:
        clear_screen()
        draw_table(table)
        print(f"Player {GREEN_SQUARE if current_player == 1 else RED_SQUARE} turn")

        available_squares = get_available_squares(table, current_player)
        table = handle_next_move(table, available_squares, current_player)
        winner = check_winner(table)

        if winner:
            break
        else:
            current_player = 1 if current_player == 2 else 2

    # Game over
    clear_screen()
    draw_table(table)
    print(f"🎉 Player {GREEN_SQUARE if winner == 1 else RED_SQUARE} wins! Congratulations!")
    input("Press Enter to continue...")