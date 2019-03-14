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
                          size=(300, 520),
                          style=wx.DEFAULT_FRAME_STYLE
                                ^ wx.RESIZE_BORDER
                                ^ wx.MAXIMIZE_BOX)
           
        self.Bind(wx.EVT_CLOSE, self.on_close)
        
        ##init board.
        #load previous config if exist.        
        try:
            with open(save_file, mode="rb") as f:
                config = pickle.load(f)
        except (FileNotFoundError, EOFError):
            config = dict()
            
        ##Read config about counter
        self.Ctotal = config.get("Ctotal", 0)
        self.Ccurrent = 0
        
        
        self.board = gameboard.GameBoard(self, config)
        self.board.SetFocus()
        
        self.SetTitle("Next Color Practice")        
        
        
        ##init UI
        self.sb = self.CreateStatusBar()
        self.sb.SetFieldsCount(2)
        self.sb.SetStatusWidths([-1, -1])
        self.sb.SetStatusText("Counter: "+str(self.Ccurrent), 0)
        self.sb.SetStatusText("Total: "+str(self.Ctotal), 1)
        
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
        
    

        
    def on_close(self, Event):
        """Executed when window is closed. Save config."""
        with open(save_file, "wb") as f:
            
            current_config = self.board.get_config()
            current_config["Ctotal"] = self.Ctotal
            pickle.dump(current_config, f)
            
        self.Destroy()
        
    #----------------------------------------------------------------------
    def inc_counter(self):
        """Increment counters"""
        self.Ccurrent += 1
        self.Ctotal += 1
        self.SetStatusText("Counter: "+str(self.Ccurrent), 0)
        self.SetStatusText("Total: "+str(self.Ctotal), 1)        


def main():
    app = wx.App()
    ex = ColorPrac(None)
    ex.Show()
    app.MainLoop()
    
    
if __name__ == "__main__":
    main()
    
    
        
        
        
        
                                    