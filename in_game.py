from utils import (
    GREEN_SQUARE, RED_SQUARE, TABLE_SIZE, check_winner,
    choose_first_player, clear_screen, create_initial_table,
    draw_table, show_logo, translate_direction
)

COL_HEADERS = ("A", "B", "C", "D", "E", "F")
MENU_OPTIONS = ("START", "SHOW RULES", "EXIT")


def show_menu() -> int:
    """Displays the main menu and prompts the user to select an option."""
    clear_screen()
    show_logo()
    
    while True:
        for index, option_text in enumerate(MENU_OPTIONS, start=1):
            print(f"{index}. {option_text}")
        
        try:
            option = int(input("Choose an option: "))
            if 1 <= option <= len(MENU_OPTIONS):
                return option
        except ValueError:
            pass  # Ignore invalid input


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


def handle_next_move(table: list[list[int]], available_squares: list[dict], player: int) -> list[list[int]]:
    """Handles a player's move by prompting them to choose a piece and a direction."""
    
    def get_user_choice(prompt: str, options: list) -> int:
        while True:
            try:
                choice = int(input(prompt))
                if 1 <= choice <= len(options):
                    return choice - 1
            except ValueError:
                pass  # Ignore invalid input
    
    # Select piece
    for index, square in enumerate(available_squares, start=1):
        row, col = square['square_position']['row'] + 1, COL_HEADERS[square['square_position']['col']]
        print(f"{index}: {col}{row}")
    
    chosen_piece = available_squares[get_user_choice("Choose the piece you'd like to move: ", available_squares)]
    
    # Select direction
    for index, direction in enumerate(chosen_piece['available_moves'], start=1):
        print(f"{index}: {translate_direction(direction)}")
    
    chosen_direction = chosen_piece['available_moves'][get_user_choice("Choose the direction you'd like to move: ", chosen_piece['available_moves'])]
    
    return move_piece(table, chosen_piece['square_position'], chosen_direction, player)


def game_start() -> None:
    """Starts and manages the main game loop until a winner is determined."""
    clear_screen()
    table, current_player = create_initial_table(), choose_first_player()
    
    while True:
        clear_screen()
        draw_table(table)
        print(f"Player {GREEN_SQUARE if current_player == 1 else RED_SQUARE} turn")
        
        available_squares = get_available_squares(table, current_player)
        table = handle_next_move(table, available_squares, current_player)
        
        if (winner := check_winner(table)):
            break
        
        current_player = 3 - current_player  # Switch between 1 and 2
    
    # Game over
    clear_screen()
    draw_table(table)
    print(f"🎉 Player {GREEN_SQUARE if winner == 1 else RED_SQUARE} wins! Congratulations!")
    input("Press Enter to continue...")