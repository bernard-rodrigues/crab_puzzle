from utils import GREEN_SQUARE, RED_SQUARE, TABLE_SIZE, check_winner, choose_first_player, clear_screen, create_initial_table, draw_table, separator, show_logo, translate_direction

COL_HEADERS = ("A", "B", "C", "D", "E", "F")
MENU_OPTIONS = ("START", "SHOW RULES", "EXIT")

def show_menu():
    clear_screen()
    show_logo()
    option = 0
    
    while option not in range(1, len(MENU_OPTIONS)+1):
        for index, option in enumerate(MENU_OPTIONS, start=1):
            print(f"{index}. {option}")

        option = int(input("Choose an option: "))
    
    return option

def get_available_moves(table, row, col):
    # Define possible moves: up, down, left, right
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    # Check each move and ensure it's within bounds
    available_moves = []
    for dr, dc in moves:
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < TABLE_SIZE and 0 <= new_col < TABLE_SIZE:  # Use TABLE_SIZE
            if table[new_row][new_col] == 0:  # Check if the move is available
                available_moves.append({'vertical': dr, 'horizontal': dc})
    return available_moves

def get_available_squares(table, player):
    if player not in [1, 2]:  # Validate player input
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

def move_piece(table, piece_position, move_direction, player):
    row, col = piece_position['row'], piece_position['col']
    
    while True:
        # Calculate the new position
        new_row = row + move_direction['vertical']
        new_col = col + move_direction['horizontal']

        # Check if the new position is within bounds
        if 0 <= new_row < 6 and 0 <= new_col < 6:
            # Check if the new position is empty
            if table[new_row, new_col] == 0:
                # Move the piece
                table[row, col] = 0
                table[new_row, new_col] = player
                row, col = new_row, new_col
            else: break
        else: break
    return table

def handle_next_move(table, available_squares, player):
    for index, square in enumerate(available_squares, start=1):
        row = square['square_position']['row'] + 1
        col = COL_HEADERS[square['square_position']['col']]

        print(f"{index}: {col}{row}")
    
    chosen_piece_index = 0
    while chosen_piece_index not in range(1, len(available_squares) + 1):
        chosen_piece_index = int(input("Choose the piece you'd like to move: "))

    chosen_piece = available_squares[chosen_piece_index-1]
    
    for index, direction in enumerate(chosen_piece['available_moves'], start=1):
        print(f"{index}: {translate_direction(direction)}")
    
    chosen_direction_index = 0
    while chosen_direction_index not in range(1, len(chosen_piece['available_moves']) + 1):
        chosen_direction_index = int(input("Choose the direction you'd like to move: "))

    chosen_direction = chosen_piece['available_moves'][chosen_direction_index-1]
    
    return move_piece(table, chosen_piece['square_position'], chosen_direction, player)

def game_start():
    clear_screen()
    table = create_initial_table()
    current_player = choose_first_player()
    winner = 0

    while(True):
        clear_screen()
        draw_table(table)

        print(f"Player {GREEN_SQUARE if current_player == 1 else RED_SQUARE} turn")

        available_squares = get_available_squares(table, current_player)
        table = handle_next_move(table, available_squares, current_player)
        winner = check_winner(table)
        if not winner:
            current_player = 1 if current_player == 2 else 2
        else:
            break
    
    clear_screen()
    draw_table(table)

    print(f"🎉 Player {GREEN_SQUARE if winner == 1 else RED_SQUARE} wins! Congratulations!")
    input("Press Enter to continue...")