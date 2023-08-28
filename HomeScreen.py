import wx


class ImagePanel(wx.Panel):
    def __init__(self, parent, image_size):
        super().__init__(parent)
        self.max_size = 720

        self.search_button = wx.Button(self, label='Search Photos')
        self.tag_button = wx.Button(self, label='Tag Photos')

        # Create a font iwth a larger size
        button_font = wx.Font(wx.FontInfo(32))

        # Set the created font for the button labels
        self.search_button.SetFont(button_font)
        self.tag_button.SetFont(button_font)

        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        main_sizer.Add(self.search_button, 1, wx.EXPAND, 5)
        main_sizer.Add(self.tag_button, 1, wx.EXPAND, 5)
        self.SetSizer(main_sizer)

        self.search_button.Bind(wx.EVT_BUTTON, self.on_search_button)
        self.tag_button.Bind(wx.EVT_BUTTON, self.on_tag_button)

        self.search_clicked = False
        self.tag_clicked = False

    def on_search_button(self, event):
        self.search_clicked = True
        self.GetTopLevelParent().Close()

    def on_tag_button(self, event):
        self.tag_clicked = True
        self.GetTopLevelParent().Close()


class MainFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title='Photo Search Program')
        self.Maximize(True)
        self.panel = ImagePanel(self, image_size=(720, 720))
        self.Show()


def start_home_screen():
    app = wx.App(False)
    frame = MainFrame()
    app.MainLoop()
    return frame.panel.search_clicked, frame.panel.tag_clicked


if __name__ == '__main__':
    start_home_screen()

"""
TO DO:

Tags file name search and destroy??
Photo's file name??
"""
