"""Main window."""

import os
import wx

import configwindow
import gameboard


# Directory for icons.
icon_dir = "../icons/"


class ColorPrac(wx.Frame):
    """Main window class."""
    def __init__(self, parent):
        wx.Frame.__init__(self,
                          parent,
                          size=(300, 500),
                          style=wx.DEFAULT_FRAME_STYLE
                                ^ wx.RESIZE_BORDER
                                ^ wx.MAXIMIZE_BOX)
        
        self.init_frame()
        self.init_ui()
        
    def init_ui(self):
        
        toolbar = self.CreateToolBar()
        ctool = toolbar.AddTool(wx.ID_ANY,
                                "",
                                wx.Bitmap(os.path.join(icon_dir,
                                                       "config.png")))
        toolbar.Realize()
        
        self.Bind(wx.EVT_TOOL, self.on_config, ctool)
        
    def on_config(self, e):
        """run when config button in toolbar."""
        con_app = wx.App()
        self.config = configwindow.Config(self)
        self.config.Show()
        con_app.MainLoop()
        
    
    def init_frame(self):
        
        self.board = gameboard.GameBoard(self)
        self.board.SetFocus()
        
        self.SetTitle("Next Color Practice")

def main():
    app = wx.App()
    ex = ColorPrac(None)
    ex.Show()
    app.MainLoop()
    
    
if __name__ == "__main__":
    main()
    
    
        
        
        
        
                                    