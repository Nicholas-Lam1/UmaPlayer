class Config:
    """ Configuration class to hold settings and parameters """
    def __init__(self):
        # Argument parameters
        self.DEBUG = False
        self.MAXIMIZE = False

        # Game parameters
        self.GAME_NAME = "Umamusume"

        # OCR/EAST model parameters
        self.MODEL_PATH = "frozen_east_text_detection.pb"
        self.CONF_THRESH = 0.85
        self.NMS_THRESH = 0.3
        self.SCALE = 1.0
        self.INPUT_SIZE = (1280, 1280)
        self.MEAN = (123.68, 116.78, 103.94)
        self.SWAP_RB = True

        # Database parameters
        self.DB_CONFIG = {
            "user" : "root",
            "password" : "LilBunny<3",
            "host" : "NLPi.local",
            "database" : "NL_App"
        }

config = Config()