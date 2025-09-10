import subprocess
import time
from time import sleep
from win32 import win32gui
from win32.lib import win32con
import constants
from coordinate_handler import find_game_area

def open_game():
    subprocess.run(f"start steam://run/3224770", shell=True)

def enum_windows_callback(hwnd, window_titles):
    if win32gui.IsWindowVisible(hwnd):
        title = win32gui.GetWindowText(hwnd)
        if title:  
            window_titles.append(title)
    return True  

def get_open_window_titles():
    window_titles = []
    win32gui.EnumWindows(enum_windows_callback, window_titles)
    return window_titles

def find_and_open_window():
    start_time = time.time()
    while time.time() - start_time < 15:
        open_windows = get_open_window_titles()
        if constants.DEBUG:
            print("Open Windows:")
            for title in open_windows:
                print(f"- {title}")
        
        if constants.GAME_NAME in open_windows:
            break

    hwnd = win32gui.FindWindow(None, constants.GAME_NAME)
    if hwnd:
        try:
            win32gui.SetForegroundWindow(hwnd)
            print("Window Opened")
            if constants.MAXIMIZE:
                sleep(1)
                win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
            sleep(3)
            find_game_area()
        except:
            print("Window Not Found.")