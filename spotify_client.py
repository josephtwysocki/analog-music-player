import spotipy
from spotipy.oauth2 import SpotifyOAuth

from config import (
    SPOTIFY_CLIENT_ID,
    SPOTIFY_CLIENT_SECRET,
    SPOTIFY_REDIRECT_URI,
    SCOPE
)


def get_spotify():

    return spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            client_id=SPOTIFY_CLIENT_ID,
            client_secret=SPOTIFY_CLIENT_SECRET,
            redirect_uri=SPOTIFY_REDIRECT_URI,
            scope=SCOPE,
            open_browser=True,
            cache_path=".spotify_cache"
        )
    )


def list_devices(sp):

    return sp.devices()["devices"]


def get_target_device(sp, device_name=None):

    devices = list_devices(sp)

    if not devices:
        raise Exception("No Spotify devices found")

    # If user specified device
    if device_name:

        for device in devices:
            if device_name.lower() in device["name"].lower():
                return device

        raise Exception(f"Device not found: {device_name}")

    # Otherwise prefer active
    for device in devices:
        if device["is_active"]:
            return device

    # Fallback first
    return devices[0]


def play_album(sp, album_uri, device_id):

    sp.start_playback(
        device_id=device_id,
        context_uri=album_uri
    )


def stop_playback(sp):

    sp.pause_playback()