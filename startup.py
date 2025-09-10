from configuration import config
import subprocess
import time
from time import sleep
from win32 import win32gui
from win32.lib import win32con
from coordinate_handler import find_game_area

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
    start_time = time.time()
    while time.time() - start_time < 15:
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
            find_game_area()
        except:
            raise Exception("Window Not Found")