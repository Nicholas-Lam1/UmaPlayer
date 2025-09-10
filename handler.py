from ocr import find_text_at_position, click, find_pos_tool
from rand_adjust import rand_sleep
import constants as const

def start_handler():
    # start_game()
    # test_menu()
    find_pos_tool([const.ENHANCE_BUTTON_POS, 
                   const.STORY_BUTTON_POS, 
                   const.HOME_BUTTON_POS, 
                   const.RACE_BUTTON_POS, 
                   const.SCOUT_BUTTON_POS,
                   const.TITLE_BAR_POS,
                   const.CAREER_BUTTON_POS])

def start_game():
    while (pos := find_text_at_position(position=const.START_BUTTON_POS, text="TAP TO START")) is not None:
        click(pos, "TAP TO START")
        rand_sleep(5)

def test_menu():
    while find_text_at_position(position=const.TITLE_BAR_POS, text="Enhance") is not None:
        click(find_text_at_position(position=const.ENHANCE_BUTTON_POS, text="Enhance"), "Enhance")
        rand_sleep(2)
    while not find_text_at_position(position=const.TITLE_BAR_POS, text="Story") is not None:
        click(find_text_at_position(position=const.STORY_BUTTON_POS, text="Story"), "Story")
        rand_sleep(2)
    while not find_text_at_position(position=const.CAREER_BUTTON_POS, text="CAREER") is not None:
        click(find_text_at_position(position=const.HOME_BUTTON_POS, text="Home"), "Home")
        rand_sleep(2)
    while not find_text_at_position(position=const.TITLE_BAR_POS, text="Race") is not None:
        click(find_text_at_position(position=const.RACE_BUTTON_POS, text="Race"), "Race")
        rand_sleep(2)
    while not find_text_at_position(position=const.TITLE_BAR_POS, text="Scout") is not None:
        click(find_text_at_position(position=const.SCOUT_BUTTON_POS, text="Scout"), "Scout")
        rand_sleep(2)
