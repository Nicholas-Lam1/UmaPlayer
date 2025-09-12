from configuration import config
from coordinate import pos
from screen_reader import screen_reader
from coordinate_handler import get_win_cords, find_game_area
from rand_adjust import rand_sleep
from tools import find_start_tool
from time import sleep, time
from win32 import win32gui
from win32.lib import win32con
import subprocess

class Starter():
    def open_game(self):
        """ Function to open the game via Steam """
        subprocess.run(f"start steam://run/3224770", shell=True)
        sleep(10)  

    def find_windows(self, hwnd, window_titles): 
        """ Function to collect open window titles """
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if title:  
                window_titles.append(title)
        return True  

    def get_open_window_titles(self):
        """ Function to get a list of open window titles """
        window_titles = []
        win32gui.EnumWindows(self.find_windows, window_titles)
        return window_titles

    def find_and_open_window(self, timeout = 600):
        """ Function to find and open the game window """
        # Wait up to 15 seconds for the game window to appear
        end_time = None if timeout is None else time.monotonic() + timeout
        while end_time is None or time.monotonic() < end_time:
            open_windows = self.get_open_window_titles()
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
                self.click_start_game()
                end_time = time.monotonic() + 60
                while  time.monotonic() < end_time:
                    if find_game_area():
                        break
                    sleep(0.5)
            except:
                raise Exception("Window Not Found")
            
    def click_start_game(self):
        while (position := screen_reader.find_text_at_position(position=pos.get_window_from_win("START_BUTTON"), text="TAP TO START")) is not None:
            screen_reader.click(position, "TAP TO START")