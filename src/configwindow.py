"""Config window."""
import wx

class Config(wx.Frame):
    """Main config window."""
    def __init__(self, parent):
        wx.Frame.__init__(self,
                          parent,
                          style=wx.DEFAULT_DIALOG_STYLE)
        
        self.board = parent.board
        self.init_ui()
        
    def init_ui(self):
        
        config = self.board.get_config()
        
        toppanel = wx.Panel(self, wx.ID_ANY)
        topsizer = wx.BoxSizer(wx.VERTICAL)
        
        
        #Color variation setting.
        self.colorconf = ColorConf(self, config["colors"])
        topsizer.Add(self.colorconf, 0, wx.EXPAND)         
        
                       
        #config about average height.
        self.heightconf = HeightConf(self, config["height"])
        topsizer.Add(self.heightconf, 0, wx.EXPAND)
        
        #Save and cancel config Button
        self.savebuttons = SaveButtons(self)
        topsizer.Add(self.savebuttons, 0, wx.EXPAND)
        
        self.SetSizerAndFit(topsizer)
        
        
        
        
        #General Frame setting
        # self.SetSize((400, 400))
        self.Center()
        
        
        
        
    def save_config(self, e):
        """Launched when save button pressed."""
        
        config = dict()
        
        #Color setting
        config["colors"] = self.colorconf.get_state()
        
                
        ##Average height setting
        config["height"] = self.heightconf.get_state()
        
        #if no colors are checked, alert and return config menu.
        if True in config["colors"].values():
            self.board.set_config(config)
            self.Close()
        else:
            dial = wx.MessageDialog(None,
                                    "At least one color must be checked!",
                                    "Alert",
                                    wx.OK)
            dial.ShowModal()
            
    def cancel_config(self, e):
        """Launched when cancel button pressed."""
        self.Close()


class ColorConf(wx.Panel):
    """Config checkboxes for color config"""
    
    def __init__(self, parent, colors):
        """Constructor
        
        Args:
            parent: parent Frame.
            colors: dict of colorname:bool for initial setting of checkbox
        """
        super().__init__(parent, wx.ID_ANY)
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        #Print "Colors"
        c_text = wx.StaticText(self, wx.ID_ANY, "colors")
        sizer.Add(c_text)
        
        #Make checkboxes.
        self.col_check_list = []
        for color in colors:
            checkbox = wx.CheckBox(self, wx.ID_ANY, color)
            checkbox.SetValue(colors[color])
            sizer.Add(checkbox, 1, wx.EXPAND)
            self.col_check_list.append((color, checkbox))
            
        self.SetSizer(sizer)
                  
    def get_state(self):
        """return state of checkboxes.
        
        This returns dict object.
          keys: colorname of checkbox
          val: Ture if checked.
        """
        
        state = dict()
        for color, checkbox in self.col_check_list:
            conf = checkbox.GetValue()
            state[color] = conf
            
        return state
     
    
class HeightConf(wx.Panel):
    """config panel for Height."""
    def __init__(self, parent, current_height):
        super().__init__(parent, wx.ID_ANY)
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        #print description of height config.
        h_text = wx.StaticText(self,
                               wx.ID_ANY,
                               "Average height of garbage blocks.\n"
                                   "(-1 to random)")
        
        sizer.Add(h_text)
        
        #spinctrl
        self.h_spin = wx.SpinCtrl(self, min=-1, max=20, style=wx.SP_ARROW_KEYS)
        self.h_spin.SetValue(current_height)
        sizer.Add(self.h_spin, 1, wx.EXPAND)
        
        self.SetSizer(sizer)
    
    def get_state(self):
        return self.h_spin.GetValue()
    
        

class SaveButtons(wx.Panel):
    """Save config and cancel buttons."""
    
    def __init__(self, parent):
        super().__init__(parent, wx.ID_ANY)
        
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        s_button = wx.Button(self, wx.ID_ANY, "Save")
        can_button = wx.Button(self, wx.ID_ANY, "Cancel")
        
        s_button.Bind(wx.EVT_BUTTON, parent.save_config, s_button)
        can_button.Bind(wx.EVT_BUTTON, parent.cancel_config, can_button)
            
        sizer.Add(s_button)
        sizer.Add(can_button)
        
        self.SetSizer(sizer)
        

        
    
    
    
           