import wx
import os
import csv


def save_tag_to_csv(tag, csv_filename):
    if not os.path.exists(csv_filename):
        with open(csv_filename, "w") as f:
            f.write("Tag\n")  # Write the header if the file doesn't exist

    lowercase_tag = tag.lower()  # Convert the tag to lowercase
    with open(csv_filename, "a") as f:
        f.write(lowercase_tag + "\n")  # Append the lowercase tag to the CSV file


def tag_exists(tag):
    lowercase_tag = tag.lower()  # Convert the tag to lowercase
    csv_filename = "tags.csv"

    if os.path.exists(csv_filename):
        with open(csv_filename, "r") as f:
            for line in f:
                if lowercase_tag in line.lower():  # Check if the lowercase tag exists in the CSV file
                    return True
    return False


class ImagePanel(wx.Panel):
    def __init__(self, parent, image_size, tags_file_name, photos_file_name):
        super().__init__(parent)

        self.tags_file_name = tags_file_name  # Store the CSV file name
        self.photos_file_name = photos_file_name  # Store the photos CSV file name

        self.max_height = int(image_size[1] * 0.85)
        self.max_width = int(image_size[0] * 0.85)

        self.image_index = 0
        self.image_folder = None

        img = wx.Image(self.max_width, self.max_height)
        self.image_ctrl = wx.StaticBitmap(self,
                                          bitmap=wx.Bitmap(img))

        # Set a standart font
        standart_font = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)

        # Create text to display information and apply the standart font
        self.file_location = wx.StaticText(self, label='Location: ')
        self.file_location.SetFont(standart_font)
        self.file_name = wx.StaticText(self, label='Name: ')
        self.file_name.SetFont(standart_font)
        self.status_text = wx.StaticText(self, label='Status')
        self.status_text.SetFont(standart_font)
        self.available_tags_text = wx.StaticText(self, label='Available Tags:')
        self.available_tags_text.SetFont(standart_font)
        self.selected_tags_text = wx.StaticText(self, label='Selected Tags:')
        self.selected_tags_text.SetFont(standart_font)
        self.applied_tags_text = wx.StaticText(self, label='Applied Tags:')
        self.applied_tags_text.SetFont(standart_font)

        # Create and bind the buttons and text inputs
        self.create_tag = wx.Button(self, label='Create Tag')
        self.create_tag.Bind(wx.EVT_BUTTON, self.on_create_tag)
        self.tag_input = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER)  # TextCtrl for tag input
        self.tag_input.Bind(wx.EVT_TEXT_ENTER, self.on_create_tag)
        self.browse_button = wx.Button(self, label='Browse')
        self.browse_button.Bind(wx.EVT_BUTTON, self.on_browse)
        self.previous_button = wx.Button(self, label='Previous')
        self.previous_button.Bind(wx.EVT_BUTTON, self.on_previous)
        self.next_button = wx.Button(self, label='Next')
        self.next_button.Bind(wx.EVT_BUTTON, self.on_next)
        self.add_tags = wx.Button(self, label='Add Tags')
        self.add_tags.Bind(wx.EVT_BUTTON, self.on_add_tags)
        self.year_text = wx.StaticText(self, label="Year:")
        self.year_text.SetFont(standart_font)

        # Create a ListBox to display tags
        self.available_tags_listbox = wx.ListBox(self, style=wx.LB_SINGLE | wx.LB_HSCROLL)
        self.available_tags_listbox.Bind(wx.EVT_LISTBOX_DCLICK, self.on_double_click_available_tag)
        self.populate_available_tags_listbox()
        self.selected_tags_listbox = wx.ListBox(self, style=wx.LB_SINGLE | wx.LB_HSCROLL)
        self.selected_tags_listbox.Bind(wx.EVT_LISTBOX_DCLICK, self.on_double_click_selected_tag)
        self.applied_tags_listbox = wx.ListBox(self, style=wx.LB_SINGLE | wx.LB_HSCROLL)
        self.applied_tags_listbox.Bind(wx.EVT_LISTBOX_DCLICK, self.on_double_click_applied_tags)

        # Create a slider to select the year
        self.year_slider = wx.Slider(self, value=2000, minValue=1900, maxValue=2099, style=wx.SL_HORIZONTAL)
        self.year_slider.Bind(wx.EVT_SCROLL, self.on_year_slider_change)

        # Create sizers for the different areas
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        top_sizer = wx.BoxSizer(wx.HORIZONTAL)
        middle_sizer = wx.BoxSizer(wx.HORIZONTAL)
        file_info_sizer = wx.BoxSizer(wx.HORIZONTAL)
        create_tag_sizer = wx.BoxSizer(wx.HORIZONTAL)
        tag_list_sizer = wx.BoxSizer(wx.VERTICAL)
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # Create a sizer to hold the file information elements
        file_info_sizer.Add(self.file_location, 0, wx.ALL, 5)
        file_info_sizer.AddSpacer(200)
        file_info_sizer.Add(self.file_name, 0, wx.ALL, 5)
        file_info_sizer.AddSpacer(500)
        file_info_sizer.Add(self.status_text, 0, wx.ALL, 5)

        # Add the create tags part to the create_tag_sizer
        create_tag_sizer.Add(self.create_tag, 0, wx.ALL | wx.EXPAND, 5)
        create_tag_sizer.Add(self.tag_input, 0, wx.ALL, 5)

        # Merge the info sizer and the add tags sizer to top_sizer
        top_sizer.Add(self.browse_button, 1, wx.ALL | wx.EXPAND | wx.ALIGN_LEFT, 5)
        top_sizer.Add(file_info_sizer, 0, wx.EXPAND | wx.ALIGN_LEFT, 5)
        top_sizer.AddSpacer(500)  # TODO: Push the create_tag_sizer to the right !!TEMPORARY SOLUTION!!
        top_sizer.Add(create_tag_sizer, 1, wx.EXPAND, 5)

        # Merge everything required to see and add tags and year
        tag_list_sizer.Add(self.available_tags_text, 0, wx.ALL, 5)
        tag_list_sizer.Add(self.available_tags_listbox, 0, wx.EXPAND, 5)
        tag_list_sizer.Add(self.selected_tags_text, 0, wx.ALL, 5)
        tag_list_sizer.Add(self.selected_tags_listbox, 0, wx.EXPAND, 5)
        tag_list_sizer.Add(self.applied_tags_text, 0, wx.ALL, 5)
        tag_list_sizer.Add(self.applied_tags_listbox, 0, wx.ALL, 5)
        tag_list_sizer.Add(self.year_text, 0, wx.ALL, 5)
        tag_list_sizer.Add(self.year_slider, 0, wx.EXPAND, 5)

        # Combine the image control and the list of tags
        middle_sizer.Add(self.image_ctrl, 0, wx.ALIGN_LEFT, 5)
        middle_sizer.Add(tag_list_sizer, 0, wx.ALL, 5)

        # Add the buttons to the button_sizer
        button_sizer.Add(self.previous_button, 2, wx.ALL | wx.EXPAND, 5)
        button_sizer.Add(self.next_button, 2, wx.ALL | wx.EXPAND, 5)
        button_sizer.Add(self.add_tags, 1, wx.ALL | wx.EXPAND, 5)

        # Add the different elements to the main sizer in the correct order
        main_sizer.Add(top_sizer, 0, wx.ALL | wx.ALIGN_TOP, 5)
        main_sizer.Add(middle_sizer, 0, wx.ALIGN_LEFT, 5)
        main_sizer.Add(button_sizer, 1, wx.EXPAND, 5)

        self.SetSizer(main_sizer)
        main_sizer.Fit(parent)
        self.Layout()

    def set_status(self, status):
        if status == 'RESET':
            self.status_text.SetLabel('Status')
            self.status_text.SetForegroundColour(wx.Colour(0, 0, 0))
        if status == 'TAG_SAVED':
            self.status_text.SetLabel('Saved new tag')
            self.status_text.SetForegroundColour(wx.Colour(0, 128, 0))
        if status == 'TAG_EXISTS':
            self.status_text.SetLabel('Tag already exists')
            self.status_text.SetForegroundColour(wx.Colour(128, 0, 0))
        if status == 'TAGS_ADDED':
            self.status_text.SetLabel('Added tags')
            self.status_text.SetForegroundColour(wx.Colour(0, 128, 0))
        if status == 'TAG_REMOVED':
            self.status_text.SetLabel('Tag removed')
            self.status_text.SetForegroundColour(wx.Colour(128, 0, 0))

    def on_create_tag(self, event):
        tag = self.tag_input.GetValue().strip()  # Get the tag text and remove leading/trailing spaces
        if tag:
            lowercase_tag = tag.lower()  # Convert the tag to lowercase

            if not tag_exists(lowercase_tag):
                save_tag_to_csv(lowercase_tag, self.tags_file_name)

                # Add new tag to the available tags list in the correct alphabetical position
                tags = self.available_tags_listbox.GetStrings()
                tags.append(lowercase_tag)
                tags.sort()  # Sort the tags alphabetically
                self.available_tags_listbox.SetItems(tags)

                # Add new tag to the selected tags list in the correct alphabetical position
                tags = self.selected_tags_listbox.GetStrings()
                tags.append(lowercase_tag)
                tags.sort()  # Sort the tags alphabetically
                self.selected_tags_listbox.SetItems(tags)

                self.set_status('TAG_SAVED')
            else:
                self.set_status('TAG_EXISTS')

            self.tag_input.SetValue("")  # Clear the text input after saving

    def display_image(self):
        if hasattr(self, "image_folder"):
            image_files = [f for f in os.listdir(self.image_folder) if f.lower().endswith(".jpg")]
            if 0 <= self.image_index < len(image_files):
                image_path = os.path.join(self.image_folder, image_files[self.image_index])
                img = wx.Image(image_path, wx.BITMAP_TYPE_ANY)

                # Calculate new dimensions while preserving aspect ratio and limiting max height
                img_width = img.GetWidth()
                img_height = img.GetHeight()
                new_height = min(img_height, self.max_height)
                new_width = int(new_height * img_width / img_height)

                # Create a black background bitmap
                background_bitmap = wx.Bitmap(self.max_width, self.max_height)
                dc = wx.MemoryDC()
                dc.SelectObject(background_bitmap)
                dc.SetBackground(wx.Brush(wx.Colour(0, 0, 0)))
                dc.Clear()

                # Calculate the position to overlay the image
                x_position = (self.max_width - new_width) // 2
                y_position = (self.max_height - new_height) // 2

                # Rescale the image keeping the aspect ratio
                img = img.Rescale(new_width, new_height, quality=wx.IMAGE_QUALITY_HIGH)

                # Overlay the rescaled image on the black background
                dc.DrawBitmap(wx.Bitmap(img), x_position, y_position)

                # Clean up
                dc.SelectObject(wx.NullBitmap)

                # Set the bitmap
                self.image_ctrl.SetBitmap(background_bitmap)

                # Set the labels
                self.file_location.SetLabel('Location: ' + os.path.basename(os.path.dirname(image_path)))
                self.file_name.SetLabel('Name: ' + os.path.basename(image_path))

    def on_browse(self, event):
        wildcard = "JPEG files (*.jpg)|*.jpg"
        with wx.DirDialog(None, "Choose a folder", style=wx.DD_DEFAULT_STYLE) as dialog:
            if dialog.ShowModal() == wx.ID_OK:
                selected_folder = dialog.GetPath()
                image_files = [f for f in os.listdir(selected_folder) if f.lower().endswith(".jpg")]

                if image_files:
                    self.image_index = 0
                    self.image_folder = selected_folder
                    self.display_image()

                    image_path = os.path.join(self.image_folder, image_files[self.image_index])
                    filename = os.path.basename(image_path)
                    self.populate_applied_tags_listbox(filename)

    def on_previous(self, event):
        if hasattr(self, "image_index") and self.image_index > 0:
            self.image_index -= 1
            self.display_image()

            image_files = [f for f in os.listdir(self.image_folder) if f.lower().endswith(".jpg")]
            image_path = os.path.join(self.image_folder, image_files[self.image_index])
            filename = os.path.basename(image_path)
            self.populate_applied_tags_listbox(filename)

            self.populate_available_tags_listbox()

            self.set_status('RESET')

    def on_next(self, event):
        if hasattr(self, "image_folder"):
            image_files = [f for f in os.listdir(self.image_folder) if f.lower().endswith(".jpg")]
            if self.image_index < len(image_files) - 1:
                self.image_index += 1
                self.display_image()

                image_path = os.path.join(self.image_folder, image_files[self.image_index])
                filename = os.path.basename(image_path)
                self.populate_applied_tags_listbox(filename)

                self.populate_available_tags_listbox()

                self.set_status('RESET')

    def on_add_tags(self, event):
        if hasattr(self, "image_folder") and self.image_index >= 0:
            image_files = [f for f in os.listdir(self.image_folder) if f.lower().endswith(".jpg")]

            if 0 <= self.image_index < len(image_files):
                image_path = os.path.join(self.image_folder, image_files[self.image_index])
                location = os.path.basename(os.path.dirname(image_path))
                filename = os.path.basename(image_path)
                selected_tags = self.selected_tags_listbox.GetStrings()

                # Search for the corresponding row in the photos CSV file
                rows = []
                entry_found = False
                if os.path.exists(self.photos_file_name):
                    with open(self.photos_file_name, "r") as csvfile:
                        reader = csv.reader(csvfile)
                        for row in reader:
                            if row[0] == location and row[1] == filename:
                                existing_tags = row[3].split(", ")
                                updated_tags = list(set(existing_tags) | set(selected_tags))  # Combine old and new tags
                                row[3] = ", ".join(updated_tags)  # Update the tags for the photo
                                rows.append(row)
                                entry_found = True
                            else:
                                rows.append(row)

                if not entry_found:
                    rows.append([location, filename, "", ", ".join(selected_tags)])

                # Write the updated or new rows back to the photos CSV file
                with open(self.photos_file_name, "w", newline="") as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerows(rows)

                self.set_status('TAGS_ADDED')
                self.populate_applied_tags_listbox(filename)

    def populate_available_tags_listbox(self):
        # Read tags from the CSV file and populate the ListBox
        tags = []
        if os.path.exists(self.tags_file_name):
            with open(self.tags_file_name, "r") as f:
                next(f)
                tags = [line.strip() for line in f.readlines()]

        # Sort the tags alphabetically
        tags.sort()

        self.available_tags_listbox.Set(tags)

    def populate_applied_tags_listbox(self, photo_filename):
        self.applied_tags_listbox.Clear()  # Clear the applied tags listbox

        # Load the photo details from the photos.csv file
        if os.path.exists(self.photos_file_name):
            with open(self.photos_file_name, "r") as f:
                reader = csv.reader(f)
                header = next(reader)  # Read the header
                for row in reader:
                    _, filename, _, tags = row  # Assuming the structure is Location, Filename, Year, Tags
                    if filename == photo_filename:
                        applied_tags = tags.split(", ")
                        self.applied_tags_listbox.Set(applied_tags)
                        break  # No need to continue searching

    def on_double_click_available_tag(self, event):
        selected_tag = self.available_tags_listbox.GetStringSelection()
        if selected_tag:
            self.selected_tags_listbox.Append(selected_tag)
            self.available_tags_listbox.Delete(self.available_tags_listbox.GetSelection())

    def on_double_click_selected_tag(self, event):
        selected_tag = self.selected_tags_listbox.GetStringSelection()
        if selected_tag:
            self.selected_tags_listbox.Delete(self.selected_tags_listbox.GetSelection())

    def on_double_click_applied_tags(self, event):
        selected_tag = self.applied_tags_listbox.GetStringSelection()
        if selected_tag:
            image_files = [f for f in os.listdir(self.image_folder) if f.lower().endswith(".jpg")]
            photo_filename = image_files[self.image_index]

            # Find the corresponding row in the photos CSV file
            rows = []
            entry_found = False
            if os.path.exists(self.photos_file_name):
                with open(self.photos_file_name, "r") as csvfile:
                    reader = csv.reader(csvfile)
                    for row in reader:
                        _, filename, _, tags = row
                        if filename == photo_filename:
                            applied_tags = [tag.strip() for tag in tags.split(", ")]
                            if selected_tag in applied_tags:
                                applied_tags.remove(selected_tag)  # Remove the tag
                            row[3] = ", ".join(applied_tags)  # Update the tags for the photo
                            rows.append(row)
                            entry_found = True
                        else:
                            rows.append(row)

            if entry_found:
                # Write the updated rows back to the photos CSV file
                with open(self.photos_file_name, "w", newline="") as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerows(rows)

                # Update the applied tags listbox and status
                self.populate_applied_tags_listbox(photo_filename)
                self.set_status('TAG_REMOVED')

    def on_year_slider_change(self, event):
        selected_year = self.year_slider.GetValue()
        self.year_text.SetLabel('Year: ' + str(selected_year))

        self.set_status('RESET')


class MainFrame(wx.Frame):
    def __init__(self, tags_file_name, photos_file_name):
        super().__init__(None, title='Tag Photos')
        self.Maximize(True)
        screen_size = wx.DisplaySize()  # Get the screen size
        panel = ImagePanel(self, image_size=screen_size, tags_file_name=tags_file_name,
                           photos_file_name=photos_file_name)
        self.Show()


def start_tag_photos(tags_file_name, photos_file_name):
    app = wx.App(redirect=False)
    frame = MainFrame(tags_file_name, photos_file_name)  # Pass the CSV files
    app.MainLoop()


if __name__ == '__main__':
    start_tag_photos("tags.csv", "photos.csv")

# TODO: Delete photo??
# TODO: Delete Tag
