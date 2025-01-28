import os
import random
import numpy as np

from texts import LOGO, RULES

TABLE_SIZE = 6

GREEN_SQUARE = "🟩"
RED_SQUARE = "🟥"
WHITE_SQUARE = "🟨"

def show_logo():
    print(LOGO)

def choose_first_player():
    return random.choice((1, 2))

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def separator():
    print("\n")

def show_rules():
    clear_screen()
    print(RULES)
    input("Press Enter to continue...")

def draw_square(square_number):
    match square_number:
        case 0:
            return WHITE_SQUARE
        case 1:
            return GREEN_SQUARE
        case 2:
            return RED_SQUARE

def translate_direction(direction):
    if direction['vertical'] == -1:
        return "up"
    if direction['vertical'] == 1:
        return "down"
    if direction['horizontal'] == -1:
        return "left"
    if direction['horizontal'] == 1:
        return "right"
    raise ValueError("Not a valid direction")

def create_initial_table():
    table = np.zeros((TABLE_SIZE, TABLE_SIZE), dtype=int)

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

def draw_table(table):
    col_headers = (" ", " A", " B", " C", " D", " E", " F\n")
    for label in col_headers: print(label, end="")

    for row in range(TABLE_SIZE):
        print(row+1, end="")
        for col in range(TABLE_SIZE):
            print(draw_square(table[row][col]), end="")
        print("")
    separator()

def check_winner(table):
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
            if counter == 4:  # Four consecutive dots in a row
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
            if counter == 4:  # Four consecutive dots in a column
                return last_dot

    # If no winner is found, return 0
    return 0