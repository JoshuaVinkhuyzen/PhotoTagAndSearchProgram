from HomeScreen import start_home_screen
from SearchPhotos import start_search_photos
from TagPhotos import start_tag_photos, MainFrame
import os

tags_csv_file = "tags.csv"
photos_csv_file = "photos.csv"


# Create a new CSV file with a header if it doesn't exist
def create_csv_file(file_name, header):
    if not os.path.exists(file_name):
        with open(file_name, "w", newline="") as f:
            f.write(header + "\n")


# Start the program to tag photos. Also check for the csv files and maken them is they dont exist
def tag_photos(tagsfile, photosfile):
    create_csv_file(tagsfile, "Tag")
    create_csv_file(photosfile, "Location,Filename,Year,Month,Tags")
    start_tag_photos(tagsfile, photosfile)
    return ()


# Start the search photos program
def search_photos():
    start_search_photos()
    return ()


# Start the homescreen and check for the imputed response to start the next program
def home_screen():
    search, tag = start_home_screen()

    start_search_photos = False
    start_tag_photos = False

    if search:
        start_search_photos = True
        return start_search_photos

    if tag:
        return start_tag_photos


if __name__ == '__main__':
    start_program = home_screen()
    if not start_program:
        tag_photos(tags_csv_file, photos_csv_file)
    if start_program:
        search_photos()