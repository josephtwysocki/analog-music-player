from database import get_album
import json


def load_tags(path="tags.json"):
    with open(path, "r") as f:
        return json.load(f)


def get_album_key_for_tag(tag_id, path="tags.json"):
    tags = load_tags(path)

    normalized_tag = tag_id.strip().upper()

    if normalized_tag not in tags:
        raise Exception(f"NFC tag not mapped: {normalized_tag}")

    return tags[normalized_tag]


def get_album_for_tag(tag_id):
    album_key = get_album_key_for_tag(tag_id)
    album = get_album(album_key)
    return album_key, album