""" class and method to manage game."""

class Config:
    """Load, save, hold config information."""
    def __init__(self, source=None):
        """ load config from source
        parameters
            source: file path or config object
        """
        # load default config value
        self._all_colors = ["Cyan",
                           "Orange",
                           "Yellow",
                           "Red",
                           "Purple",
                           "Blue",
                           "Green"]
        self._enabled_colors = self._all_colors
        self._ave_height = -1
        self._next_queue = 3
        self._blind_enable = False
        self._blind_num = 3

        if not source:
            self.load(source)

    @property
    def all_colors(self):
        return self._all_colors

    @property
    def enabled_colors(self):
        return self._enabled_colors

    @enabled_colors.setter
    def enabled_colors(self, source):
        if type(source) is Config and "enabled_colors" in dir(source):
            new_colors = source.enabled_colors
        elif type(source) is list:
            new_colors = source
        else:
            return
        _enabled_colors = []
        for color in new_colors:
            if color in self._all_colors:
                _enabled_colors.append(color)
        self._enabled_colors = _enabled_colors

    @property
    def enabled_colors_index(self):
        table = {
        "Cyan": 1,
        "Orange": 2,
        "Yellow": 3,
        "Red": 4,
        "Purple": 5,
        "Blue": 6,
        "Green": 7
        }
        return [table[color] for color in self.enabled_colors]

    @property
    def ave_height(self):
        return self._ave_height

    @ave_height.setter
    def ave_height(self, source):
        self._ave_height = source

    @property
    def next_queue_len(self):
        return self._next_queue

    @next_queue_len.setter
    def next_queue_len(self, source):
        self._next_queue = source

    @property
    def blind_enable(self):
        return self._blind_enable
    
    @blind_enable.setter
    def blind_enable(self, source):
        self._blind_enable = source
     
    @property
    def blind_num(self):
        return self._blind_num

    @blind_num.setter
    def blind_num(self, source):
        self._blind_num = source
        
    def load(self, source):
        if source is Config:
            self.enabled_colors = source.enabled_colors
            self.ave_height= source.ave_height
            self.next_queue_len = source.next_queue_len
            self.blind_enable = source.blind_enable
            self.blind_num = soure.blind_num







