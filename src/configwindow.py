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
        
        self.config = self.board.get_config()
        
        panel = wx.Panel(self, wx.ID_ANY)
        sizer = wx.GridBagSizer(2, 12)
        grid_y = 0
        
        
        ##Color variation setting.
        self.col_check_list = []
        c_text = wx.StaticText(panel, wx.ID_ANY, "Colors")
        sizer.Add(c_text, pos=(grid_y, 0))
        grid_y += 1
        
       
        
        for color in self.config["colors"]:
            checkbox = wx.CheckBox(panel, wx.ID_ANY, color)
            checkbox.SetValue(self.config["colors"][color])
            sizer.Add(checkbox, pos=(grid_y, 0))
            self.col_check_list.append((color, checkbox))
            grid_y += 1
                       
        ##config about average height.
        grid_y += 1
        h_text = wx.StaticText(panel,
                               wx.ID_ANY,
                               "Average height of garbage blocks.\n(-1 to random)")
        sizer.Add(h_text, pos=(grid_y, 0))
        grid_y += 1
        
        
        self.h_spin = wx.SpinCtrl(panel, min=-1, max=20, style=wx.SP_ARROW_KEYS)
        
        self.h_spin.SetValue(self.config["height"])
        sizer.Add(self.h_spin, pos=(grid_y, 0))
        grid_y += 1
        
        
        
        
        ##Save and cancel config Button
        grid_y += 1
        s_button = wx.Button(panel, wx.ID_ANY, "Save")
        can_button = wx.Button(panel, wx.ID_ANY, "Cancel")
        
        s_button.Bind(wx.EVT_BUTTON, self.on_click_save, s_button)
        can_button.Bind(wx.EVT_BUTTON, self.on_click_cancel, can_button)
            
        sizer.Add(s_button, pos=(grid_y, 0))
        sizer.Add(can_button, pos=(grid_y, 1))
        
        
        #Sizer
        panel.SetSizer(sizer)
        
        #General Frame setting
        self.SetSize((300, 500))
        self.Center()
        
        
    def on_click_save(self, e):
        """Launched when save button pressed."""
        ##Color setting
        checked = False
        for color, checkbox in self.col_check_list:
            conf = checkbox.GetValue()
            self.config["colors"][color] = conf
            if conf:
                checked = True
                
        ##Average height setting
        self.config["height"] = self.h_spin.GetValue()
        
        #if checked == False, no box is checked so need to alert and return.
        if checked:
            self.board.set_config(self.config)
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

