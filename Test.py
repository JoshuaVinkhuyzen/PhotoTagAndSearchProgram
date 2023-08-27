import wx


class ImagePanel(wx.Panel):
    def __init__(self, parent, image_size):
        super().__init__(parent)
        self.max_size = 240

        self.image_ctrl = wx.StaticBitmap(self)
        self.load_button = wx.Button(self, label='Load Image')
        self.load_button.Bind(wx.EVT_BUTTON, self.load_image)

        main_sizer = wx.BoxSizer(wx.HORIZONTAL)

        main_sizer.Add(self.image_ctrl, 0, wx.ALL | wx.CENTER, 5)
        main_sizer.Add(self.load_button, 0, wx.ALL | wx.CENTER, 5)

        self.SetSizer(main_sizer)

    def load_image(self, event):
        wildcard = "JPEG files (*.jpg)|*.jpg"
        with wx.FileDialog(None, "Choose a file",
                           wildcard=wildcard,
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as dialog:
            if dialog.ShowModal() == wx.ID_OK:
                selected_path = dialog.GetPath()
                img = wx.Image(selected_path, wx.BITMAP_TYPE_ANY)
                img = self.scale_image(img)
                self.image_ctrl.SetBitmap(wx.Bitmap(img))
                self.Refresh()

    def scale_image(self, img):
        W = img.GetWidth()
        H = img.GetHeight()
        if W > H:
            NewW = self.max_size
            NewH = self.max_size * H / W
        else:
            NewH = self.max_size
            NewW = self.max_size * W / H
        return img.Scale(int(NewW), int(NewH))


class MainFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title='Image Viewer')
        panel = ImagePanel(self, image_size=(240, 240))
        self.Show()


if __name__ == '__main__':
    app = wx.App(False)
    frame = MainFrame()
    app.MainLoop()
