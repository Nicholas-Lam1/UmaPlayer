from time import sleep
import random
import pytweening

movement_types = [
    pytweening.easeInQuad,
    pytweening.easeOutQuad,
    pytweening.easeInOutQuad,
    pytweening.easeInBounce,
    pytweening.easeInElastic,
]

def rand_sleep(seconds):
    sleep_time = random.uniform(seconds-seconds*0.1, seconds+seconds*0.1)
    sleep(sleep_time)

def rand_move_type():
    return movement_types[random.randrange(0,5)]