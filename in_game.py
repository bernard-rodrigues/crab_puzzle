from cpu_ai import ai_best_move_hard, ai_best_move_normal
from utils import (
    GREEN_SQUARE, RED_SQUARE, animate_move_piece, check_winner,
    choose_first_player, clear_screen, create_initial_table,
    draw_table, draw_table_with_highlight, get_available_squares, move_piece, show_logo, translate_direction
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

def handle_next_move(table: list[list[int]], available_squares: list[dict], player: int) -> list[list[int]]:
    """Handles a player's move with animated movement."""
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
    
    # Highlight selected piece
    clear_screen()
    draw_table_with_highlight(table, (chosen_piece['square_position']['row'], 
                                    chosen_piece['square_position']['col']))
    
    # Select direction
    for index, direction in enumerate(chosen_piece['available_moves'], start=1):
        print(f"{index}: {translate_direction(direction)}")
    
    chosen_direction = chosen_piece['available_moves'][get_user_choice(
        "Choose the direction you'd like to move: ", 
        chosen_piece['available_moves']
    )]
    
    return animate_move_piece(table, chosen_piece['square_position'], chosen_direction, player)


def game_start(game_mode: int, difficult: int = 1) -> None:
    """Starts and manages the main game loop until a winner is determined."""
    clear_screen()
    table, current_player = create_initial_table(), choose_first_player()
    
    while True:
        clear_screen()
        draw_table(table)
        print(f"Player {GREEN_SQUARE if current_player == 1 else RED_SQUARE} turn")
        
        if game_mode == 1 or current_player == 1:  # Human player's turn
            available_squares = get_available_squares(table, current_player)
            table = handle_next_move(table, available_squares, current_player)
        else:  # AI's turn
            move = ai_best_move_normal(table, current_player) if difficult == 1 else ai_best_move_hard(table, current_player)
            if move:
                table = animate_move_piece(table, move['piece'], move['direction'], current_player)
        
        if (winner := check_winner(table)):
            break
        
        current_player = 3 - current_player  # Switch between 1 and 2
    
    # Game over
    clear_screen()
    draw_table(table)
    if game_mode == 1:
        print(f"🎉 Player {GREEN_SQUARE if winner == 1 else RED_SQUARE} wins! Congratulations!")
    else:
        print(f"🎉 {'You' if winner == 1 else 'CPU'} win! Congratulations!")
    input("Press Enter to continue...")