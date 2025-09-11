class Positions:
    """Class to handle coordinate storage and transformations """
    def __init__(self):
        # Window coordinates
        self.WINDOW_LEFT = 0
        self.WINDOW_RIGHT = 0
        self.WINDOW_TOP = 0
        self.WINDOW_BOTTOM = 0
        self.WINDOW_WIDTH = 0
        self.WINDOW_HEIGHT = 0

        # Game area coordinates
        self.GAME_LEFT = 0
        self.GAME_RIGHT = 0
        self.GAME_TOP = self.WINDOW_TOP         # Not handled yet. When windowed, these values match window
        self.GAME_BOTTOM = self.WINDOW_BOTTOM   # When maximized, these values dont match window. Will need to be found
        self.GAME_WIDTH = 0
        self.GAME_HEIGHT = 0

        self.GAME_LEFT_OFFSET = 0
        self.GAME_TOP_OFFSET = 0                # Not handled yet

        # Relative windows (x%, y%, width%, height%)
        self.RELATIVE_REGIONS = {
            "START_BUTTON": (0.375, 0.8, 0.25, 0.14),       # Uses full window dimensions
            "TITLE_BAR": (0, 0, 0.25, 0.18),
            "CAREER_BUTTON": (0.63, 0.836, 0.23, 0.054),
            "RP_BAR": (0.545, 0.0425, 0.17, 0.02),
        }

        # Relative points (x%, y%)
        self.RELATIVE_POINTS = {
            "ENHANCE_BUTTON": (0.2, 0.96),
            "STORY_BUTTON": (0.325, 0.96), 
            "HOME_BUTTON": (0.5, 0.96),
            "RACE_BUTTON": (0.675, 0.96), 
            "SCOUT_BUTTON": (0.8, 0.96),       
        }

    def rel_to_abs_win(self, rel):
        """
        Convert relative coordinates -> absolute
        If rel = (x%, y%) -> returns (x, y)
        If rel = (x%, y%, w%, h%) -> returns (x, y, w, h)
        """
        if len(rel) == 2:
            x, y = rel
            abs_x = int(x * self.WINDOW_WIDTH)
            abs_y = int(y * self.WINDOW_HEIGHT)
            return (abs_x, abs_y)

        elif len(rel) == 4:
            x, y, w, h = rel
            abs_x = int(x * self.WINDOW_WIDTH)
            abs_y = int(y * self.WINDOW_HEIGHT)
            abs_w = int(w * self.WINDOW_WIDTH)
            abs_h = int(h * self.WINDOW_HEIGHT)
            return (abs_x, abs_y, abs_w, abs_h)

        else:
            raise ValueError(f"Unsupported rel format: {rel}")

    def rel_to_abs(self, rel):
        """
        Convert relative coordinates -> absolute
        If rel = (x%, y%) -> returns (x, y)
        If rel = (x%, y%, w%, h%) -> returns (x, y, w, h)
        """
        if len(rel) == 2:
            x, y = rel
            abs_x = int(x * self.GAME_WIDTH)
            abs_y = int(y * self.GAME_HEIGHT)
            return (abs_x, abs_y)

        elif len(rel) == 4:
            x, y, w, h = rel
            abs_x = int(x * self.GAME_WIDTH)
            abs_y = int(y * self.GAME_HEIGHT)
            abs_w = int(w * self.GAME_WIDTH)
            abs_h = int(h * self.GAME_HEIGHT)
            return (abs_x, abs_y, abs_w, abs_h)

        else:
            raise ValueError(f"Unsupported rel format: {rel}")
        
    def get_window_from_win(self, name):
        """ Get absolute position for region relative to the window by name """
        if name not in self.RELATIVE_REGIONS:
            raise KeyError(f"'{name}' not in RELATIVE_POSITIONS")
        window = self.rel_to_abs_win(self.RELATIVE_REGIONS[name])
        window = (window[0] + self.WINDOW_LEFT, window[1] + self.WINDOW_TOP, window[2], window[3])
        return window
    
    def get_point_from_win(self, name):
        """ Get absolute point relative to the window by name """
        if name not in self.RELATIVE_POINTS:
            raise KeyError(f"'{name}' not in RELATIVE_POINTS")
        point = self.rel_to_abs_win(self.RELATIVE_POINTS[name])
        point = (point[0] + self.WINDOW_LEFT, point[1] + self.WINDOW_TOP)
        return point

    def get_window_from_game(self, name):
        """ Get absolute position for region relative to the game area by name """
        if name not in self.RELATIVE_REGIONS:
            raise KeyError(f"'{name}' not in RELATIVE_POSITIONS")
        window = self.rel_to_abs(self.RELATIVE_REGIONS[name])
        window = (window[0] + self.GAME_LEFT, window[1] + self.GAME_TOP, window[2], window[3])
        return window
    
    def get_point_from_game(self, name):
        """ Get absolute point relative to the game area by name """
        if name not in self.RELATIVE_POINTS:
            raise KeyError(f"'{name}' not in RELATIVE_POINTS")
        point = self.rel_to_abs(self.RELATIVE_POINTS[name])
        point = (point[0] + self.GAME_LEFT, point[1] + self.GAME_TOP)
        return point

pos = Positions()
