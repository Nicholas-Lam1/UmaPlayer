import argparse
import constants
import pyautogui
from startup import open_game, find_and_open_window


parser = argparse.ArgumentParser()
parser.add_argument("--DEBUG", help="Use flag for debug statements", default=False, action=argparse.BooleanOptionalAction)
parser.add_argument("--MAXIMIZE", help="Use flag to maximize the game window", default=False, action=argparse.BooleanOptionalAction)
parser.parse_args()
args = parser.parse_args()

if args.DEBUG:
    print(args)

def main():
    open_game()
    win_left, win_top, win_width, win_height = find_and_open_window(args.MAXIMIZE)
    print(win_left, win_top, win_width, win_height)
    startbutton = pyautogui.locateOnScreen('reference_images\start_screen\image.png', confidence=0.9)

if __name__ == "__main__":
    main()