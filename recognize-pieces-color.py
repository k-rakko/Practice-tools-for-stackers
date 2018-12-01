import wx
import random

class ColorPrac(wx.Frame):
    
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, size=(300, 500),
            style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER ^ wx.MAXIMIZE_BOX)
        
        self.init_frame()
        self.init_ui()
        
    def init_ui(self):
        
        toolbar = self.CreateToolBar()
        ctool = toolbar.AddTool(wx.ID_ANY, "", wx.Bitmap("config.png"))
        toolbar.Realize()
        
        self.Bind(wx.EVT_TOOL, self.OnConfig, ctool)
        
    def OnConfig(self, e):
        
        con_app = wx.App()
        self.config = Config(self)
        self.config.Show()
        con_app.MainLoop()
        
    
    def init_frame(self):
        
        self.board = Board(self)
        self.board.SetFocus()
        
        self.SetTitle("Next Color Practice")

class Config(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self
                          , parent
                          ,style=wx.DEFAULT_DIALOG_STYLE)
        
        self.board = parent.board
        self.init_ui()
        
    def init_ui(self):
        
        self.config = self.board.get_config()
        
        panel = wx.Panel(self, wx.ID_ANY)
        sizer = wx.GridBagSizer(2, 10)
        grid_y = 0
        
        
        ##Color variation setting.
        self.col_check_list = []
        c_text = wx.StaticText(panel, wx.ID_ANY, "Colors")
        sizer.Add(c_text, pos=(grid_y, 0))
        grid_y += 1
        
        #checkbox to choose color
        color_labels = ["Cyan", "Yellow", "Orange", "Blue", "Green", "Red", "Purple"]
        
        for color in color_labels:
            checkbox = wx.CheckBox(panel, wx.ID_ANY, color)
            checkbox.SetValue(self.config["colors"][color])
            sizer.Add(checkbox, pos=(grid_y, 0))
            self.col_check_list.append((color, checkbox))
            grid_y += 1
                       

        
        ##Save and cancel config Button
        s_button = wx.Button(panel, wx.ID_ANY, "Save")
        can_button = wx.Button(panel, wx.ID_ANY, "Cancel")
        
        s_button.Bind(wx.EVT_BUTTON, self.OnClickSave, s_button)
        can_button.Bind(wx.EVT_BUTTON, self.OnClickCansel, can_button)
            
        sizer.Add(s_button, pos=(grid_y, 0))
        sizer.Add(can_button, pos=(grid_y, 1))
        
        
        #Sizer
        panel.SetSizer(sizer)
        
        #General Frame setting
        self.SetSize((200, 500))
        self.Center()
        
        
    def OnClickSave(self, e):
        
        ##Color setting
        checked = False
        for color, checkbox in self.col_check_list:
            conf = checkbox.GetValue()
            self.config["colors"][color] = conf
            if conf:
                checked = True
        
        #if checked == False, no box is checked so need to alert and return.
        if checked:
            self.board.set_config(self.config)
            self.Close()
        else:
            dial = wx.MessageDialog(None
                                    , "At least one color must be checked!"
                                    , "Alert"
                                    , wx.OK)
            dial.ShowModal()
            
    def OnClickCansel(self, e):
        self.Close()

class Board(wx.Panel):
    
    def __init__(self, *args, **kw):
        super(Board, self).__init__(*args, **kw)
        self.init_config()
        self.init_Board()
        
        
    def init_config(self):
        self.FieldWidth = 10
        self.FieldHeight = 20
        
        self.SquareSize = 20
    
        #block colors.
        #color = [No block, I, O, L, J, S, Z, T, Gray]
        self.colors = ['#000000', '#87cefa', "#ffff00", "#ffa500", "#0000ff"
                  , "#00ff00", "#ff0000", "#9400d3", "#a9a9a9"]
    
        self.light_colors = ['#000000', '#add8e6', "#ffffe0", "#f0e68c", "#1e90ff"
                  , "#adff2f", "#ff6347", "#ee82ee", "#f5f5f5"]
        
        self.dark_colors = ['#000000', "#6495ed", "#ffd700", "#cd853f", "#191970"
                  , "#32cd32", "#dc143c", "#8a2be2", "#696969"]   
        
        self.color_table = ["Cyan", "Yellow", "Orange", "Blue", "Green", "Red", "Purple"]
        self.enabled_colors = [x for x in range(1, 8)]
    
        
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
        self.draw_square(x*self.SquareSize, y*self.SquareSize,
                         self.SquareSize, self.SquareSize, shape)
        
    
        
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
        self.draw_square(12*self.SquareSize, 1*self.SquareSize
                         , int(1.5*self.SquareSize), int(1.5*self.SquareSize), shape)
               
        
    def on_key_down(self, event):
        
        keycode = event.GetKeyCode()
        
        if keycode == wx.WXK_SPACE:
            self.show_new_question()
            
    def show_new_question(self):
        
        self.make_new_question()
        
        self.draw_field()
        
        #create new next color.
        next_index = random.randint(0, len(self.enabled_colors)-1)
        self.draw_next(self.enabled_colors[next_index])
        
    def make_new_question(self):
        #At now, hole will change at most 1 time.
        
        #height of garbage block, height where hole change, 
        #list of hole position.
        
        
      

        garbage_height = random.randint(0, int(self.FieldHeight * 0.6))
        
        height_change = [0, 0, 0, 0, 0, +1, +1, -1, -1, +2, -2]
        garbage_h_list = []
        
        for i in range(10):
            garbage_h_list.append(garbage_height)
            garbage_height += height_change[random.randint(0, len(height_change)-1)]
        
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
        index = 1
        self.enabled_colors = []
        for color in self.color_table:
            if config["colors"][color] == True:
                self.enabled_colors.append(index)
                
            index += 1
        
    def get_config(self):
        config = dict()
        color_config = dict()
        index = 1
        for color in self.color_table:
            if index in self.enabled_colors:
                color_config[color] = True
            else:
                color_config[color] = False
                
            index += 1
            
        config["colors"] = color_config
        
        return config
        
             
                
        
            
      
        
        
def main():
    app = wx.App()
    ex = ColorPrac(None)
    ex.Show()
    app.MainLoop()
    
    
if __name__ == "__main__":
    main()
    
    
        
        
        
        
                                    