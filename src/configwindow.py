"""Config window."""
import wx
import game_engine as ge

class ConfigWindow(wx.Frame):
    """Main config window."""
    def __init__(self, parent):
        wx.Frame.__init__(self,
                          parent,
                          style=wx.DEFAULT_DIALOG_STYLE)
        self.parent = parent
        self.col_check_list = []
        self.h_spin = wx.SpinCtrl(self, min=-1, max=20, style=wx.SP_ARROW_KEYS)
        self.next_spin = wx.SpinCtrl(self, min=1, max=6, style=wx.SP_ARROW_KEYS)
        self.blind_checkbox = wx.CheckBox(self, wx.ID_ANY, "")
        self.blind_spin = wx.SpinCtrl(self, min=0, max=99, style=wx.SP_ARROW_KEYS)
        self.mode_radios = []

        self.init_ui()
        self.Center()
        
    def init_ui(self):
        config = self.parent.board.config
        top_sizer = wx.BoxSizer(wx.VERTICAL)

        #Color variation setting.
        color_sizer = wx.BoxSizer(wx.VERTICAL)
        
        c_text = wx.StaticText(self, wx.ID_ANY, "Colors")
        color_sizer.Add(c_text)

        for color in config.all_colors:
            checkbox = wx.CheckBox(self, wx.ID_ANY, color)
            checkbox.SetValue(color in config.enabled_colors)
            color_sizer.Add(checkbox)
            self.col_check_list.append((color, checkbox))
                       
        #config about average height.
        height_sizer = wx.BoxSizer(wx.VERTICAL)
        h_text = wx.StaticText(self,
                               wx.ID_ANY, 
                               "Average height of garbage blocks. (-1 to random)")
        height_sizer.Add(h_text)

        
        self.h_spin.SetValue(config.ave_height)
        height_sizer.Add(self.h_spin)
        
        
        #Config about next.
        next_sizer = wx.BoxSizer(wx.VERTICAL)
        
        next_text = wx.StaticText(self,
                               wx.ID_ANY,
                               "Number of next to display")
        next_sizer.Add(next_text, 0, wx.ALL, 5)
        
        #Number of next.
        self.next_spin.SetValue(config.next_queue_len)
        next_sizer.Add(self.next_spin, 0, wx.ALL, 5)        
        # Blind mode.
        blind_sizer = wx.BoxSizer(wx.VERTICAL)

        blind_rtext = "Blind mode: Update next without changing field."
        blind_text = wx.StaticText(self,
                                   wx.ID_ANY,
                                   blind_rtext)
        blind_sizer.Add(blind_text, 0)
        # enable or disable

        self.blind_checkbox.SetValue(config.blind_enable)
        blind_sizer.Add(self.blind_checkbox, 0)
        # how many times update next without updating field.


        self.blind_spin.SetValue(config.blind_num)
        blind_sizer.Add(self.blind_spin, 0)

        # field mode.
        field_mode_sizer = wx.BoxSizer(wx.VERTICAL)
        field_rtext = "Field complexity"
        field_text = wx.StaticText(self,
                                   wx.ID_ANY,
                                   field_rtext)
        field_mode_sizer.Add(field_text, 0)
        for mode in config.all_field_mode:
            radio = wx.RadioButton(self, wx.ID_ANY, mode)
            if mode == config.field_mode:
                radio.SetValue(True)
            else:
                radio.SetValue(False)
            field_mode_sizer.Add(radio)
            self.mode_radios.append((radio, mode))

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
        top_sizer.Add(field_mode_sizer, 0, wx.ALL, 5)
        top_sizer.Add(save_sizer, 0, wx.ALL, 5)
        
        self.SetSizerAndFit(top_sizer)

    def on_click_save(self, e):
        """Launched when save button pressed."""
        config = ge.Config()
        enabled_colors = []
        for color, checkbox in self.col_check_list:
            if checkbox.GetValue():
                enabled_colors.append(color)
        config.enabled_colors = enabled_colors
        config.ave_height = self.h_spin.GetValue()
        config.next_queue_len = self.next_spin.GetValue()
        config.blind_enable = self.blind_checkbox.GetValue()
        config.blind_num = self.blind_spin.GetValue()
        for radio, mode in self.mode_radios:
            if radio.GetValue():
                config.field_mode = mode
        #if checked == False, no box is checked so need to alert and return.
        if enabled_colors:
            self.parent.board.config = config
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

