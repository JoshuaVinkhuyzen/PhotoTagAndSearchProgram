import wx
import os


class ImagePanel(wx.Panel):
    def __init__(self, parent, image_size):
        super().__init__(parent)
        self.max_size = 720

        img = wx.Image(*image_size)
        self.image_ctrl = wx.StaticBitmap(self,
                                          bitmap=wx.Bitmap(img))

        self.file_name = wx.StaticText(self, label='File Name')
        font = wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        self.file_name.SetFont(font)

        browse_btn = wx.Button(self, label='Browse')
        browse_btn.Bind(wx.EVT_BUTTON, self.on_browse)
        self.photo_txt = wx.TextCtrl(self, size=(200, -1))
        self.previous_button = wx.Button(self, label='Previous')
        self.next_button = wx.Button(self, label='Next')

        topsizer = wx.BoxSizer(wx.HORIZONTAL)
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)

        topsizer.Add(self.file_name, 0, wx.ALL, 5)
        topsizer.Add(browse_btn, 0, wx.ALL, 5)
        topsizer.Add(self.photo_txt, 0, wx.ALL, 5)
        main_sizer.Add(topsizer, 0, wx.ALL | wx.CENTER, 5)

        main_sizer.Add(self.image_ctrl, 0, wx.ALL | wx.CENTER, 5)

        hsizer.Add(self.previous_button, 0, wx.ALL, 5)
        hsizer.Add(self.next_button, 0, wx.ALL, 5)
        main_sizer.Add(hsizer, 0, wx.ALL | wx.CENTER, 5)

        self.SetSizer(main_sizer)
        main_sizer.Fit(parent)
        self.Layout()

    def on_browse(self, event):
        wildcard = "JPEG files (*.jpg)|*.jpg"
        with wx.FileDialog(None, "Choose a file",
                           wildcard=wildcard,
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as dialog:
            if dialog.ShowModal() == wx.ID_OK:
                selected_path = dialog.GetPath()
                self.photo_txt.SetValue(selected_path)
                self.load_image()

    def load_image(self):
        filepath = self.photo_txt.GetValue()
        img = wx.Image(filepath, wx.BITMAP_TYPE_ANY)

        # Scale the image while preserving the aspect ratio
        img = self.scale_image(img)

        self.image_ctrl.SetBitmap(wx.Bitmap(img))
        self.Refresh()

        # Update the image label with the file name
        file_name = os.path.basename(filepath)
        self.file_name.SetLabel(file_name)

    def scale_image(self, img):
        w = img.GetWidth()
        h = img.GetHeight()
        if w > h:
            new_w = self.max_size
            new_h = self.max_size * h / w
        else:
            new_h = self.max_size
            new_w = self.max_size * w / h
        return img.Scale(int(new_w), int(new_h))


class MainFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title='Image Viewer')
        panel = ImagePanel(self, image_size=(720, 720))
        self.Show()


def start_search_photos():
    app = wx.GetApp()  # Get the existing wx.App instance
    if app is None:
        app = wx.App()  # Create an instance only if it doesn't exist
    frame = MainFrame()
    if app.IsMainLoopRunning():
        frame.Show()
    else:
        app.MainLoop()


if __name__ == '__main__':
    start_search_photos()
    # app = wx.App(False)
    # frame = MainFrame()
    # app.MainLoop()
