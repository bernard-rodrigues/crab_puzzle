from in_game import game_start, show_menu
from utils import show_rules

if __name__ == "__main__":
    while(True):
        option = show_menu()
        
        match option:
            case 1:
                game_start()
            case 2:
                show_rules()
            case 3:
                exit()