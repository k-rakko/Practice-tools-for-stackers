"""game field and next color."""

import random
import wx
import os

class GameBoard(wx.Panel):
    """panel for block field and next."""
    def __init__(self, parent, config=None):
        super(GameBoard, self).__init__(parent)
        
        self.Bind(wx.EVT_KEY_DOWN, self.on_key_down)
        
        self.parent = parent
        
        ##init_boad_data
        self.FieldWidth = 10
        self.FieldHeight = 20
    
        self.SquareSize = 20
        
        self.shape_noblock = 0
        self.shape_gray = 8
    
        #block colors.
        #color = [No block, I, L, O, J, S, Z, T, Gray]
        self.colors = ['#000000', # No block
                           '#87cefa', # I
                           "#ffa500", # L
                           "#ffff00", # O
                           "#ff0000", # Z
                           "#9400d3", # T
                           "#0000ff", # J
                           "#00ff00", # S
                           "#a9a9a9"] # Gray
        

        self.field = [0 for x in range(self.FieldHeight*self.FieldWidth)]
        
        self.nextbag = [x + 1 for x in range(7)]
        
        # keys for config dictionary
        self.key_height = "height"
        self.key_colors = "colors"
        self.key_next = "next"
        self.key_colful = "colorful_next"          
        
        ##set user configs if exist and set default config if doesn't exist.
        self.config = config
        if config is None or not type(config) is dict:
            self.config = dict()
            
        
        if not self.key_colors in self.config.keys():
            #Colors for next blocks.
            color_table = ["Cyan",
                           "Orange",
                           "Yellow",
                           "Red",
                           "Purple",
                           "Blue",
                           "Green"]
            
            self.config[self.key_colors] = {color:True for color in color_table}
            
        if not self.key_height in self.config.keys():
            #Average height of blocks. (-1 to random)
            self.config[self.key_height] = -1
        if not self.key_next in self.config.keys():
            self.config[self.key_next] = 1
        
        
        # Update self.enabled_nexts
        self.set_config(self.config)
        
              
        
                
    
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
        dc.SetBrush(wx.Brush(self.colors[shape]))
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
            
    def show_new_question(self):
        ##Make new question.
        #At now, hole will change at most 1 time.
        
        # set average Height of blocks.
        if self.config[self.key_height] == -1:
            garbage_height = random.randint(0, int(self.FieldHeight) - 1)
        else:
            garbage_height = self.config[self.key_height]
        
        height_change = [0, 0, 0, 0, 0, +1, +1, -1, -1, +2, -2]
        
        # this list contains list of height of garbage blocks.
        garbage_h_list = []
        for i in range(10):
            garbage_height += height_change[random.randint(0, len(height_change)-1)]
            garbage_h_list.append(garbage_height)
        
        #hole settings.
        hole_change = random.randint(0, max(0, garbage_height-1))
        hole_positions = [random.randint(0, 9) for x in range(2)]
        
        #make gabage without hole.
        for x in range(self.FieldWidth):
            for y in range(self.FieldHeight):
                if y <= garbage_h_list[x]:
                    self.field[self.f_offset(x, y)] = self.shape_gray
                else:
                    self.field[self.f_offset(x, y)] = self.shape_noblock
 
        #create hole.
        for y in range(self.FieldHeight):
            if y < hole_change:
                self.field[self.f_offset(hole_positions[0], y)] = self.shape_noblock
            else:
                self.field[self.f_offset(hole_positions[1], y)] = self.shape_noblock        
        
        
        ##Refresh entire field
        for x in range(self.FieldHeight * self.FieldWidth):
            self.draw_square((x % self.FieldWidth) * self.SquareSize,
                             (x // self.FieldWidth) * self.SquareSize,
                             self.SquareSize,
                             self.field[x])
        
        
        #Draw next
        next_index = random.randint(0, len(self.enabled_nexts)-1)
        self.draw_next(0, self.enabled_nexts[next_index])
        
        #create new next color fro additional next.
        for number in range(self.config[self.key_next] - 1):
            next_index = random.randint(0, len(self.nextbag) - 1)
            self.draw_next(number+1, self.nextbag.pop(next_index))
            if len(self.nextbag) == 0:
                self.nextbag = [x + 1 for x in range(0, 7)]
                
            else:
                next_index = random.randint(0, len(self.enabled_nexts)-1)
                self.draw_next(number, self.enabled_nexts[next_index])
            

                
    def f_offset(self, x, y, bottom_to_top=True):
        """Calculate offset of self.field from x, y"""
        
        if bottom_to_top:
            return self.FieldWidth * (self.FieldHeight - 1 - y) + x
        else:
            return self.FieldWidth * y + x
        
    
    def set_config(self, config):
        """setter of self.config"""
        #appdate enabled_nexts.
        index = 1
        self.enabled_nexts = []
        for color in config[self.key_colors]:
            if config[self.key_colors][color] == True:
                self.enabled_nexts.append(index)
                
            index += 1
        
        self.config = config
        
    def get_config(self):
        """getter of self.config"""
        return self.config
        
             
                
        
            
      
        
        
