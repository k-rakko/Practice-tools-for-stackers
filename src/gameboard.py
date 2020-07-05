"""game field and next color."""

import random
import wx
import game_engine as ge

class GameBoard(wx.Panel):
    """panel for block field and next."""
    def __init__(self, parent, config=None):
        super(GameBoard, self).__init__(parent)
        
        self.Bind(wx.EVT_KEY_DOWN, self.on_key_down)
        
        self.parent = parent
        
        #init_boad_data
        self.FieldWidth = 10
        self.FieldHeight = 20
    
        self.SquareSize = 30
        
        self.shape_noblock = 0
        self.shape_gray = 8

        # state.
        self.next_queue = []
        self.blind_count = 0
        self.init_complete = False
    
        #block colors.
        self.color_code = {
                          0: '#000000',  #No Block
                          1: '#87cefa', # I
                          2: "#ffa500", # L
                          3: "#ffff00", # O
                          4: "#ff0000", # Z
                          5: "#9400d3", # T
                          6: "#0000ff", # J
                          7: "#00ff00", # S
                          8: "#a9a9a9"  # Gray
        }

        # game state
        self.field = [0 for x in range(self.FieldHeight*self.FieldWidth)]
        self.next_bag = [range(1, 8)]

        # set user configs if exist and set default config if doesn't exist.
        if config is None or not type(config) is ge.Config:
            self._config = ge.Config()
        else:
            self._config = config

    def init_board(self):
        """Draw background and show first question."""
        dc = wx.ClientDC(self)

        dc.SetPen(wx.TRANSPARENT_PEN)
        dc.SetBrush(wx.Brush("#616161"))
        dc.DrawRectangle(0, 0, 300, 600)
        self.init_complete = True


    def draw_block(self, x, y, shape):
        # This function is currentry not used.
        """draw square at (x, y) in board
        
        Args:
            x (int): offset of square in field. left to right. 
            y (int): offset of square in field. top to bottom.  
            shape (int): shape of square.
        
        Returns:
            None
        
        """
        self.draw_square(x*self.SquareSize,
                         y*self.SquareSize,
                         self.SquareSize,
                         self.SquareSize,
                         shape)

    def draw_square(self, x, y, side_length, shape):
        """Draw rectangle at (x,y). x, y is coordinates of the topleft"""
        
        dc = wx.ClientDC(self)
        
        dc.SetPen(wx.TRANSPARENT_PEN)
        dc.SetBrush(wx.Brush(self.color_code[shape]))
        dc.DrawRectangle(x, y, side_length, side_length)   

    def draw_next(self, number, shape):
        self.draw_square(12*self.SquareSize,
                         int(self.SquareSize * 3.5 * number) , 
                         int(2*self.SquareSize),
                         shape)

    def on_key_down(self, event):
        self.parent.inc_counter()
        keycode = event.GetKeyCode()
        
        if keycode == wx.WXK_SPACE:
            self.show_new_question()

    def update_board(self):
        if not self.init_complete:
            self.init_board()
        # set average Height of blocks.
        if self._config.ave_height == -1:
            garbage_height = random.randint(0, int(self.FieldHeight) - 1)
        else:
            garbage_height = self._config.ave_height

        # this list contains list of height of garbage blocks.
        garbage_h_list = []
        for i in range(10):
            rand = random.random()
            if rand <= 0.06:
                height_change = +2
            elif rand <= 0.5:
                height_change = +1
            else:
                height_change = 0

            rand = random.random()
            if rand <= 0.5:
                height_change *= -1
            garbage_height += height_change
            garbage_h_list.append(garbage_height)

        # hole settings.
        hole_change = random.randint(0, max(0, garbage_height - 1))
        hole_positions = [random.randint(0, 9) for x in range(2)]

        # make gabage without hole.
        for x in range(self.FieldWidth):
            for y in range(self.FieldHeight):
                if y <= garbage_h_list[x]:
                    self.field[self.f_offset(x, y)] = self.shape_gray
                else:
                    self.field[self.f_offset(x, y)] = self.shape_noblock

        # create hole.
        for y in range(self.FieldHeight):
            if y < hole_change:
                self.field[self.f_offset(hole_positions[0], y)] = self.shape_noblock
            else:
                self.field[self.f_offset(hole_positions[1], y)] = self.shape_noblock

                #Refresh entire field
        for x in range(self.FieldHeight * self.FieldWidth):
            self.draw_square((x % self.FieldWidth) * self.SquareSize,
                             (x // self.FieldWidth) * self.SquareSize,
                             self.SquareSize-1,
                             self.field[x])

    def create_next_queue(self):
        self.next_queue = []
        self.next_queue.append(random.choice(self._config.enabled_colors_index))

        for i in range(self._config.blind_num//7+3):
            self.next_queue += random.sample(range(1, 8), 7)

        for i in range(self._config.next_queue_len):
            self.draw_next(i, self.next_queue[i])
        self.next_queue = self.next_queue[1:]

    def shift_next_queue(self):
        for i in range(self._config.next_queue_len):
            self.draw_next(i, self.next_queue[i])
        self.next_queue = self.next_queue[1:]

    def show_new_question(self):
        #Make new question.
        #At now, hole will change at most 1 time.
        
        if not self._config.blind_enable:
            self.update_board()
            self.create_next_queue()
        else:
            self.blind_count %= self._config.blind_num
            if self.blind_count == 0:
                self.update_board()
                self.create_next_queue()
            else:
                self.shift_next_queue()
            self.blind_count += 1
                
    def f_offset(self, x, y, bottom_to_top=True):
        """Calculate offset of self.field from x, y"""
        
        if bottom_to_top:
            return self.FieldWidth * (self.FieldHeight - 1 - y) + x
        else:
            return self.FieldWidth * y + x

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, config):
        self._config = config


