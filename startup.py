from configuration import config
from coordinate import pos
from coordinate_handler import get_win_cords, find_game_area
from ocr import find_text_at_position, click
from rand_adjust import rand_sleep
from tools import find_start_tool
from time import sleep, time
from win32 import win32gui
from win32.lib import win32con
import subprocess

def open_game():
    """ Function to open the game via Steam """
    subprocess.run(f"start steam://run/3224770", shell=True)
    sleep(10)  

def find_windows(hwnd, window_titles): 
    """ Function to collect open window titles """
    if win32gui.IsWindowVisible(hwnd):
        title = win32gui.GetWindowText(hwnd)
        if title:  
            window_titles.append(title)
    return True  

def get_open_window_titles():
    """ Function to get a list of open window titles """
    window_titles = []
    win32gui.EnumWindows(find_windows, window_titles)
    return window_titles

def find_and_open_window():
    """ Function to find and open the game window """
    # Wait up to 15 seconds for the game window to appear
    start_time = time()
    while time() - start_time < 15:
        open_windows = get_open_window_titles()
        if config.DEBUG:
            print("Open Windows:")
            for title in open_windows:
                print(f"- {title}")
        
        if config.GAME_NAME in open_windows:
            break

    # If the game window is found, bring it to the foreground
    hwnd = win32gui.FindWindow(None, config.GAME_NAME)
    if hwnd:
        try:
            win32gui.SetForegroundWindow(hwnd)
            if config.DEBUG:
                print("Window Opened")

            # Maximize if specified in arguments
            if config.MAXIMIZE:
                sleep(1)
                win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)

            # Allow time for the window to stabilize, then set window coordinates   
            sleep(3)
            get_win_cords()
            sleep(3)
            if config.DEBUG:
                find_start_tool()  
                sleep(3)
            # click_start_game()
            sleep(3)
            find_game_area()
        except:
            raise Exception("Window Not Found")
        
def click_start_game():
    while (position := find_text_at_position(position=pos.get_window_from_win("START_BUTTON"), text="TAP TO START")) is not None:
        click(position, "TAP TO START")
        rand_sleep(3)