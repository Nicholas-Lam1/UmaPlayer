from time import sleep
import random

def rand_sleep(seconds):
    sleep_time = random.uniform(seconds-seconds*0.1, seconds+seconds*0.1)
    sleep(sleep_time)