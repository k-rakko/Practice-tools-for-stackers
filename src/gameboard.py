"""game field and next color."""

import random
import wx

class GameBoard(wx.Panel):
    """panel for block field and next."""
    def __init__(self, *args, **kw):
        super(GameBoard, self).__init__(*args, **kw)
        self.init_config()
        self.init_Board()
        
        
    def init_config(self):
        self.FieldWidth = 10
        self.FieldHeight = 20
        
        self.SquareSize = 20
    
        #block colors.
        #color = [No block, I, O, L, J, S, Z, T, Gray]
        self.colors = ['#000000',
                       '#87cefa',
                       "#ffff00",
                       "#ffa500",
                       "#0000ff",
                       "#00ff00",
                       "#ff0000",
                       "#9400d3",
                       "#a9a9a9"]
    
        self.light_colors = ['#000000',
                             '#add8e6',
                             "#ffffe0",
                             "#f0e68c",
                             "#1e90ff",
                             "#adff2f",
                             "#ff6347",
                             "#ee82ee",
                             "#f5f5f5"]
        
        self.dark_colors = ['#000000', 
                            "#6495ed",
                            "#ffd700",
                            "#cd853f",
                            "#191970",
                            "#32cd32",
                            "#dc143c",
                            "#8a2be2",
                            "#696969"]   
        
        
        self.config = dict()
        
        
        #Colors for next blocks.
        color_table = ["Cyan", "Yellow", "Orange", "Blue", "Green", "Red", "Purple"]
        
        self.config["colors"] = {color:True for color in color_table}
        
        #This list is used intenally.
        self.enabled_nexts = [x+1 for x in range(7)]
        
        #Average height of blocks. (-1 to random)
        self.config["height"] = -1
        
        
    def init_Board(self):

        self.field = [[0 for x in range(self.FieldWidth)] for y in range(self.FieldHeight)]
        self.Bind(wx.EVT_KEY_DOWN, self.on_key_down)
        

        
    def draw_field(self):
        for y in range(self.FieldHeight):
            for x in range(self.FieldWidth):
                self.draw_block(x, y, self.field[y][x])
                
    
    def draw_block(self, x, y, shape):
        """draw square specified by shape at x, y in board
        
        This function draws squrare in 
        
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
        
    
        
    def draw_square(self, x1, y1, x2, y2, shape):
        """This will draw rectangle x1-x2, y1-y2"""
        
        dc = wx.ClientDC(self)
        
        pen = wx.Pen(self.light_colors[shape])
        pen.SetCap(wx.CAP_PROJECTING)
        dc.SetPen(pen)
        
        dc.DrawLine(x1, y1, x1, y1+y2-1)
        dc.DrawLine(x1, y1, x1+x2-1, y1)
        
        self.dark_colorspen = wx.Pen(self.dark_colors[shape])
        self.dark_colorspen.SetCap(wx.CAP_PROJECTING)
        dc.SetPen(self.dark_colorspen)
    
        dc.DrawLine(x1+1, y1+y2-1, x1+x2-1, y1+y2-1)
        dc.DrawLine(x1+x2-1, y1+1, x1+x2-1, y1+y2-1)
        
        dc.SetPen(wx.TRANSPARENT_PEN)
        dc.SetBrush(wx.Brush(self.colors[shape]))
        dc.DrawRectangle(x1+1, y1+1, x2-2, y2-2)   
        
        
    def draw_next(self, shape):
        self.draw_square(12*self.SquareSize,
                         1*self.SquareSize,
                         int(1.5*self.SquareSize),
                         int(1.5*self.SquareSize),
                         shape)
               
        
    def on_key_down(self, event):
        
        keycode = event.GetKeyCode()
        
        if keycode == wx.WXK_SPACE:
            self.show_new_question()
            
    def show_new_question(self):
        
        self.make_new_question()
        
        self.draw_field()
        
        #create new next color.
        next_index = random.randint(0, len(self.enabled_nexts)-1)
        self.draw_next(self.enabled_nexts[next_index])
        
    def make_new_question(self):
        #At now, hole will change at most 1 time.
        
        #height of garbage block, height where hole change, 
        #list of hole position.
        
        
      
        if self.config["height"] == -1:
            garbage_height = random.randint(0, int(self.FieldHeight * 0.6))
        else:
            garbage_height = self.config["height"]
        
        height_change = [0, 0, 0, 0, 0, +1, +1, -1, -1, +2, -2]
        garbage_h_list = []
        
        for i in range(10):
            garbage_h_list.append(garbage_height)
            garbage_height += height_change[random.randint(0, len(height_change)-1)]
            
            if garbage_height < 0:
                garbage_height = 0
            elif garbage_height > 20:
                garbage_height = 20
        
        hole_change = random.randint(0, max(0, garbage_height-1))
        hole_positions = [random.randint(0, 9) for x in range(2)]
        
        #make gabage without hole.
        for x in range(self.FieldWidth):
            for y in range(self.FieldHeight):
                if y <= self.FieldHeight - garbage_h_list[x]:
                    self.field[y][x] = 0
                else:
                    self.field[y][x] = 8
 
        #create hole.
        for y in range(self.FieldHeight):
            if self.FieldHeight - y < garbage_height:
                self.field[y][hole_positions[0]] = 0
            else:
                self.field[y][hole_positions[1]] = 0
    
    def set_config(self, config):
        """setter of self.config"""
        #appdate enabled_nexts.
        index = 1
        self.enabled_nexts = []
        for color in self.config["colors"]:
            if config["colors"][color] == True:
                self.enabled_nexts.append(index)
                
            index += 1
        
        self.config = config
        
    def get_config(self):
        """getter of self.config"""
        return self.config
        
             
                
        
            
      
        
        
