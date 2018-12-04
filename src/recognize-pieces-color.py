"""Main window."""

import os
import wx
import pickle

import configwindow
import gameboard


# Directory for icons
project_root_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "..")
icon_dir = os.path.join(project_root_dir, "icons/")
save_file = os.path.join(project_root_dir, "config/userconfig.pickle")


class ColorPrac(wx.Frame):
    """Main window class."""
    def __init__(self, parent):
        wx.Frame.__init__(self,
                          parent,
                          size=(300, 500),
                          style=wx.DEFAULT_FRAME_STYLE
                                ^ wx.RESIZE_BORDER
                                ^ wx.MAXIMIZE_BOX)
           
        self.Bind(wx.EVT_CLOSE, self.on_close)
        self.init_board()
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
        
        self.config = configwindow.Config(self)
        self.config.Show()
        
    
    def init_board(self):
        
        ##load previous config if exist.        
        try:
            with open(save_file, mode="rb") as f:
                config = pickle.load(f)
        except (FileNotFoundError, EOFError):
            config = None        
        
        
        self.board = gameboard.GameBoard(self, config)
        self.board.SetFocus()
        
        self.SetTitle("Next Color Practice")
        
    def on_close(self, Event):
        """Executed when window is closed. Save config."""
        with open(save_file, "wb") as f:
            pickle.dump(self.board.get_config(), f)
            
        self.Destroy()


def main():
    app = wx.App()
    ex = ColorPrac(None)
    ex.Show()
    app.MainLoop()
    
    
if __name__ == "__main__":
    main()
    
    
        
        
        
        
                                    