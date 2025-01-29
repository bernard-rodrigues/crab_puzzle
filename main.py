from in_game import game_start, show_menu
from texts import DIFFICULT, GAME_MODE
from utils import show_rules

if __name__ == "__main__":
    difficult = 0
    game_mode = 0
    while(True):
        option = show_menu()
        
        match option:
            case 1:
                while game_mode not in [1, 2]:
                    game_mode = int(input(GAME_MODE))
                
                if game_mode == 2:  # vs CPU
                    while difficult not in [1, 2]:
                        difficult = int(input(DIFFICULT))
                
                game_start(game_mode, difficult)
                game_mode = 0  # Reset for next game
                difficult = 0  # Reset for next game
            case 2:
                show_rules()
            case 3:
                exit()