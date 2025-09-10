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

        # Relative windows (x%, y%, width%, height%)
        self.RELATIVE_WINDOWS = {
            "START_BUTTON": (0.4, 0.89, 0.2, 0.08),
            "BOTTOM_MENU": (0.1375, 0.8, 0.3, 0.05),
            "ENHANCE_BUTTON": (0.1375, 0.8, 0.0525, 0.05),
            "STORY_BUTTON": (0.19, 0.8, 0.0525, 0.05), 
            "HOME_BUTTON": (0.2425, 0.8, 0.091, 0.05),
            "RACE_BUTTON": (0.3335, 0.8, 0.0525, 0.05), 
            "SCOUT_BUTTON": (0.386, 0.8, 0.0525, 0.05),
            "TITLE_BAR": (0.065, 0, 0.1, 0.15),
            "CAREER_BUTTON": (0.31, 0.895, 0.12, 0.05),
            "CLUB_SHOP_BUTTONS": (0.1375, 0.92, 0.12, 0.035),
        }

        # Relative points (x%, y%)
        self.RELATIVE_POINTS = {
            "START_BUTTON": (0.9, 0.95),
        }

    def rel_to_abs(self, rel):
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

    def get_window(self, name):
        """ Get absolute position by name """
        if name not in self.RELATIVE_WINDOWS:
            raise KeyError(f"'{name}' not in RELATIVE_POSITIONS")
        return self.rel_to_abs(self.RELATIVE_WINDOWS[name])
    
    def get_point(self, name):
        """ Get absolute point by name """
        if name not in self.RELATIVE_POINTS:
            raise KeyError(f"'{name}' not in RELATIVE_POINTS")
        return self.rel_to_abs(self.RELATIVE_POINTS[name])

pos = Positions()
