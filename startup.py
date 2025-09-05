import subprocess
import time
from time import sleep
from win32 import win32gui
from win32.lib import win32con
from constants import *
from coordinate_handler import get_win_cords

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

def find_and_open_window(m_flag):
    print(m_flag)
    start_time = time.time()
    while time.time() - start_time < 15:
        open_windows = get_open_window_titles()
        if DEBUG:
            print("Open Windows:")
            for title in open_windows:
                print(f"- {title}")
        
        if "Umamusume" in open_windows:
            break

    hwnd = win32gui.FindWindow(None, "Umamusume")
    if hwnd:
        try:
            win32gui.SetForegroundWindow(hwnd)
            print("Window Opened")
            if m_flag:
                sleep(3)
                win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
            return get_win_cords(hwnd)
        except:
            print("Window Not Found.")