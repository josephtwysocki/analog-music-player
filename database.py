import json

def load_albums():

    with open("albums.json") as f:
        return json.load(f)


def get_album(key):

    albums = load_albums()

    if key not in albums:
        raise Exception(f"Album key not found: {key}")

    return albums[key]