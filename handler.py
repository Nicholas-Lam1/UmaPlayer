from coordinate import pos
from ocr import find_text_at_position, click
from tools import find_pos_tool, reference_pos_tool
from rand_adjust import rand_sleep
import pyautogui
import cv2
import numpy as np

def start_handler():
    """ Main handler function to start the program """
    # test_menu()
    find_pos_tool()
    rand_sleep(1)
    # reference_pos_tool()
    find_text_at_position(position=pos.get_window_from_game("RP_COUNT"), text="5/5")
    # image = pyautogui.screenshot(region=pos.get_window_from_game("RP_COUNT"))
    # image = np.array(image)
    # image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # cv2.imshow("Position Tool", image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

def test_menu():
    """ Test function to navigate through main menu """
    while find_text_at_position(position=pos.get_window_from_game("TITLE_BAR"), text="Enhance") is not None:
        click(pos.get_point_from_game("ENHANCE_BUTTON"), "Enhance")
        rand_sleep(2)
    while not find_text_at_position(position=pos.get_window_from_game("TITLE_BAR"), text="Story") is not None:
        click(pos.get_point_from_game("STORY_BUTTON"), "Story")
        rand_sleep(2)
    while not find_text_at_position(position=pos.get_window_from_game("CAREER_BUTTON"), text="CAREER") is not None:
        click(pos.get_point_from_game("HOME_BUTTON"), "Home")
        rand_sleep(2)
    while not find_text_at_position(position=pos.get_window_from_game("TITLE_BAR"), text="Race") is not None:
        click(pos.get_point_from_game("RACE_BUTTON"), "Race")
        rand_sleep(2)
    while not find_text_at_position(position=pos.get_window_from_game("TITLE_BAR"), text="Scout") is not None:
        click(pos.get_point_from_game("SCOUT_BUTTON"), "Scout")
        rand_sleep(2)
