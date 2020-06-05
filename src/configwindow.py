"""Config window."""
import wx

class Config(wx.Frame):
    """Main config window."""
    def __init__(self, parent):
        wx.Frame.__init__(self,
                          parent,
                          style=wx.DEFAULT_DIALOG_STYLE)
        self.parent = parent
        # keys for config dictionary.
        self.key_colors = "colors"
        self.key_height = "height"
        self.key_next = "next"
        self.key_blind_num = "blind_num"
        self.key_blind = "blind"

        self.col_check_list = []
        self.h_spin = wx.SpinCtrl(self, min=-1, max=20, style=wx.SP_ARROW_KEYS)
        self.next_spin = wx.SpinCtrl(self, min=1, max=6, style=wx.SP_ARROW_KEYS)
        self.blind_checkbox = wx.CheckBox(self, wx.ID_ANY, "")
        self.blind_spin = wx.SpinCtrl(self, min=0, max=99, style=wx.SP_ARROW_KEYS)

        self.init_ui()
        self.Center()
        
    def init_ui(self):
        config = self.parent.board.get_config()
        top_sizer = wx.BoxSizer(wx.VERTICAL)

        #Color variation setting.
        color_sizer = wx.BoxSizer(wx.VERTICAL)
        
        c_text = wx.StaticText(self, wx.ID_ANY, "Colors")
        color_sizer.Add(c_text)

        for color in config[self.key_colors]:
            checkbox = wx.CheckBox(self, wx.ID_ANY, color)
            checkbox.SetValue(config[self.key_colors][color])
            color_sizer.Add(checkbox)
            self.col_check_list.append((color, checkbox))
                       
        #config about average height.
        height_sizer = wx.BoxSizer(wx.VERTICAL)
        h_text = wx.StaticText(self,
                               wx.ID_ANY, 
                               "Average height of garbage blocks. (-1 to random)")
        height_sizer.Add(h_text)

        
        self.h_spin.SetValue(config[self.key_height])
        height_sizer.Add(self.h_spin)
        
        
        #Config about next.
        next_sizer = wx.BoxSizer(wx.VERTICAL)
        
        next_text = wx.StaticText(self,
                               wx.ID_ANY,
                               "Number of next to display")
        next_sizer.Add(next_text, 0, wx.ALL, 5)
        
        #Number of next.
        self.next_spin.SetValue(config[self.key_next])
        next_sizer.Add(self.next_spin, 0, wx.ALL, 5)        
        # Blind mode.
        blind_sizer = wx.BoxSizer(wx.VERTICAL)

        blind_rtext = "Blind mode: Update next without changing field."
        blind_text = wx.StaticText(self,
                                   wx.ID_ANY,
                                   blind_rtext)
        blind_sizer.Add(blind_text, 0)
        # enable or disable

        self.blind_checkbox.SetValue(config[self.key_blind])
        blind_sizer.Add(self.blind_checkbox, 0)
        # how many times update next without updating field.


        self.blind_spin.SetValue(config[self.key_blind_num])
        blind_sizer.Add(self.blind_spin, 0)

        #Save and cancel config Button
        save_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        s_button = wx.Button(self, wx.ID_ANY, "Save")
        can_button = wx.Button(self, wx.ID_ANY, "Cancel")
        
        s_button.Bind(wx.EVT_BUTTON, self.on_click_save, s_button)
        can_button.Bind(wx.EVT_BUTTON, self.on_click_cancel, can_button)
            
        save_sizer.Add(s_button)
        save_sizer.Add(can_button)
        
        top_sizer.Add(color_sizer, 0, wx.ALL, 5)
        top_sizer.Add(height_sizer, 0, wx.ALL, 5)
        top_sizer.Add(next_sizer, 0, wx.ALL, 5)
        top_sizer.Add(blind_sizer, 0, wx.ALL, 5)
        top_sizer.Add(save_sizer, 0, wx.ALL, 5)
        
        self.SetSizerAndFit(top_sizer)

    def on_click_save(self, e):
        """Launched when save button pressed."""
        #Color setting
        config = dict()
        
        config[self.key_colors] = dict()
        for color, checkbox in self.col_check_list:
            conf = checkbox.GetValue()
            config[self.key_colors][color] = conf
        #Average height setting
        config[self.key_height] = self.h_spin.GetValue()
        config[self.key_next] = self.next_spin.GetValue()
        config[self.key_blind] = self.blind_checkbox.GetValue()
        config[self.key_blind_num] = self.blind_spin.GetValue()
        #if checked == False, no box is checked so need to alert and return.
        if True in config[self.key_colors].values():
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

