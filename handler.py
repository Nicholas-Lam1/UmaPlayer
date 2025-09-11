from coordinate import pos
from ocr import find_text_at_position, click
from tools import find_pos_tool, reference_pos_tool
from rand_adjust import rand_sleep

def start_handler():
    # start_game()
    # test_menu()
    find_pos_tool()
    rand_sleep(1)
    reference_pos_tool()

def test_menu():
    while find_text_at_position(position=pos.TITLE_BAR_POS, text="Enhance") is not None:
        click(find_text_at_position(position=pos.ENHANCE_BUTTON_POS, text="Enhance"), "Enhance")
        rand_sleep(2)
    while not find_text_at_position(position=pos.TITLE_BAR_POS, text="Story") is not None:
        click(find_text_at_position(position=pos.STORY_BUTTON_POS, text="Story"), "Story")
        rand_sleep(2)
    while not find_text_at_position(position=pos.CAREER_BUTTON_POS, text="CAREER") is not None:
        click(find_text_at_position(position=pos.HOME_BUTTON_POS, text="Home"), "Home")
        rand_sleep(2)
    while not find_text_at_position(position=pos.TITLE_BAR_POS, text="Race") is not None:
        click(find_text_at_position(position=pos.RACE_BUTTON_POS, text="Race"), "Race")
        rand_sleep(2)
    while not find_text_at_position(position=pos.TITLE_BAR_POS, text="Scout") is not None:
        click(find_text_at_position(position=pos.SCOUT_BUTTON_POS, text="Scout"), "Scout")
        rand_sleep(2)
