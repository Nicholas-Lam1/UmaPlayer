from coordinate import pos
from race_handler import race_handler
from screen_reader import screen_reader
from tools import find_pos_tool, reference_pos_tool
from rand_adjust import rand_sleep
import pymsgbox

def start_handler():
    """ Main handler function to start the program """

    while True:
        function = pymsgbox.prompt("Select function (career, race):", "Start function", "")
        if function == "career":
            print("Incomplete - Upcoming feature")
        elif function == "race":
            navigate_menu("Race")
            race_handler.auto_race()
        elif function == "position":
            find_pos_tool()
            reference_pos_tool()
        elif function == "rp bar":
            race_handler.test_rp_count()
        elif function == "quit":
            exit()

def navigate_menu(select):
    """Navigate to a menu page based on the input string (Enhance, Story, Career, Race, Scout)."""

    menu_map = {
        "Enhance": ("ENHANCE_BUTTON", "TITLE_BAR", "Enhance"),
        "Story": ("STORY_BUTTON", "TITLE_BAR", "Story"),
        "Career": ("HOME_BUTTON", "CAREER_BUTTON", "CAREER"),
        "Race": ("RACE_BUTTON", "TITLE_BAR", "Race"),
        "Scout": ("SCOUT_BUTTON", "TITLE_BAR", "Scout"),
    }

    if select not in menu_map:
        raise ValueError(f"Unknown menu option: {select}. Valid options are {list(menu_map.keys())}")

    button_key, window_key, expected_text = menu_map[select]

    screen_reader.click_and_find(button_key, window_key, expected_text)

    # Delay to pass loading screen
    rand_sleep(3)

def test_menu():
    """ Test function to navigate through main menu """
    while not screen_reader.find_text_at_position(position=pos.get_window_from_game("TITLE_BAR"), text="Enhance") is not None:
        screen_reader.click(pos.get_point_from_game("ENHANCE_BUTTON"), "Enhance")
        rand_sleep(1)
    while not screen_reader.find_text_at_position(position=pos.get_window_from_game("TITLE_BAR"), text="Story") is not None:
        screen_reader.click(pos.get_point_from_game("STORY_BUTTON"), "Story")
        rand_sleep(1)
    while not screen_reader.find_text_at_position(position=pos.get_window_from_game("CAREER_BUTTON"), text="CAREER") is not None:
        screen_reader.click(pos.get_point_from_game("HOME_BUTTON"), "Home")
        rand_sleep(1)
    while not screen_reader.find_text_at_position(position=pos.get_window_from_game("TITLE_BAR"), text="Race") is not None:
        screen_reader.click(pos.get_point_from_game("RACE_BUTTON"), "Race")
        rand_sleep(1)
    while not screen_reader.find_text_at_position(position=pos.get_window_from_game("TITLE_BAR"), text="Scout") is not None:
        screen_reader.click(pos.get_point_from_game("SCOUT_BUTTON"), "Scout")
        rand_sleep(1)
