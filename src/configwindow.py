"""Config window."""
import wx

class Config(wx.Frame):
    """Main config window."""
    def __init__(self, parent):
        wx.Frame.__init__(self,
                          parent,
                          style=wx.DEFAULT_DIALOG_STYLE)
        
        self.parent = parent
        self.init_ui()
        self.Center()
        
    def init_ui(self):
        
        config = self.parent.board.get_config()
        
        top_sizer = wx.BoxSizer(wx.VERTICAL)
        
        
        ##Color variation setting.
        color_sizer = wx.BoxSizer(wx.VERTICAL)
        
        c_text = wx.StaticText(self, wx.ID_ANY, "Colors")
        color_sizer.Add(c_text)
                
        self.col_check_list = []
        for color in config["colors"]:
            checkbox = wx.CheckBox(self, wx.ID_ANY, color)
            checkbox.SetValue(config["colors"][color])
            color_sizer.Add(checkbox)
            self.col_check_list.append((color, checkbox))
                       
        ##config about average height.
        height_sizer = wx.BoxSizer(wx.VERTICAL)
        
        h_text = wx.StaticText(self,
                               wx.ID_ANY,
                               "Average height of garbage blocks.\n(-1 to random)")
        height_sizer.Add(h_text)
        
        
        self.h_spin = wx.SpinCtrl(self, min=-1, max=20, style=wx.SP_ARROW_KEYS)
        
        self.h_spin.SetValue(config["height"])
        height_sizer.Add(self.h_spin)
        
        
        ##Save and cancel config Button
        save_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        s_button = wx.Button(self, wx.ID_ANY, "Save")
        can_button = wx.Button(self, wx.ID_ANY, "Cancel")
        
        s_button.Bind(wx.EVT_BUTTON, self.on_click_save, s_button)
        can_button.Bind(wx.EVT_BUTTON, self.on_click_cancel, can_button)
            
        save_sizer.Add(s_button)
        save_sizer.Add(can_button)
        
        top_sizer.Add(color_sizer, 0, wx.ALL, 5)
        top_sizer.Add(height_sizer, 0, wx.ALL, 5)
        top_sizer.Add(save_sizer, 0, wx.ALL, 5)
        
        self.SetSizerAndFit(top_sizer)
        
        
    def on_click_save(self, e):
        """Launched when save button pressed."""
        ##Color setting
        config = dict()
        
        config["colors"] = dict()
        for color, checkbox in self.col_check_list:
            conf = checkbox.GetValue()
            config["colors"][color] = conf
                
        ##Average height setting
        config["height"] = self.h_spin.GetValue()
        
        #if checked == False, no box is checked so need to alert and return.
        if True in config["colors"].values():
            self.parent.board.set_config(config)
            self.Close()
        else:
            dial = wx.MessageDialog(None,
                                    "At least one color must be checked!",
                                    "Alert",
                                    wx.OK)
            dial.ShowModal()
            
    def on_click_cancel(self, e):
        """Launched when cancel button pressed."""
        self.Close()
        
    
           