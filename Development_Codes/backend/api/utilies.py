from google_images_search import GoogleImagesSearch


def gis_url(query):
    # API key and CX
    gis = GoogleImagesSearch(
        'AIzaSyDavRxKC9Jcs6YRYWE0nJTe1ylyrlrtfY0', '47d748b4b3354fccc')
    gis.search(search_params={'q': query, 'num': 1})
    return gis.results()[0].url
