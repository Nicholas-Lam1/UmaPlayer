from startup import open_game, find_and_open_window
from time import sleep

def initialize_game():
    open_game()
    find_and_open_window()
    sleep(10)
    
    start_game()

def start_game():
    from ocr import find_text
    find_text()
