import argparse
import constants

parser = argparse.ArgumentParser()
parser.add_argument("--DEBUG", help="Use flag for debug statements", default=False, action=argparse.BooleanOptionalAction)
parser.add_argument("--MAXIMIZE", help="Use flag to maximize the game window", default=False, action=argparse.BooleanOptionalAction)
parser.parse_args()
args = parser.parse_args()

constants.DEBUG = args.DEBUG
constants.MAXIMIZE = args.MAXIMIZE

if args.DEBUG:
    print(args)

from handler import initialize_game
import ctypes

ctypes.windll.user32.SetProcessDPIAware()

def main():
    initialize_game()
    
if __name__ == "__main__":
    main()