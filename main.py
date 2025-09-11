from configuration import config
from startup import open_game, find_and_open_window
from menu_handler import start_handler
import argparse
import ctypes

def main():
    """ Main function to handle arguments and start the program """
    # Set the process to be DPI aware, handles Windows scaling issues
    ctypes.windll.user32.SetProcessDPIAware()

    # Argument handler, debug provides statements, maximize maximizes the game window (not handled yet)
    parser = argparse.ArgumentParser()
    parser.add_argument("--DEBUG", help="Use flag for debug statements", default=False, action=argparse.BooleanOptionalAction)
    parser.add_argument("--MAXIMIZE", help="Use flag to maximize the game window", default=False, action=argparse.BooleanOptionalAction)
    parser.parse_args()
    args = parser.parse_args()

    config.DEBUG = args.DEBUG
    config.MAXIMIZE = args.MAXIMIZE

    if args.DEBUG:
        print(args)

    # Opens game and defines window coordinates for visual operations
    open_game()
    find_and_open_window()

    # Begin the main handler
    start_handler()
    
if __name__ == "__main__":
    main()