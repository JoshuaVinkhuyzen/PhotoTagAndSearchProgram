from HomeScreen import start_home_screen
from SearchPhotos import start_search_photos
from TagPhotos import start_tag_photos

tagscsvfile = "tags.csv"


# LUT[] = {folder_name, file_name, tags} jaar? locatie?
# Animals_LUT[] = {folder_name, file_name}

# geef foto's een tag
def tag_photos(tagsfile):
    start_tag_photos(tagsfile)
    return ()


# zoek foto's aan de hand van de gegeven tags
def search_photos():
    start_search_photos()
    return ()


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
        tag_photos(tagscsvfile)
    if start_program:
        search_photos()
