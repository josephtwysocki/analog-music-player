# Continuous watcher for NFC tags to trigger Spotify playback
from nfc import get_album_for_tag
from spotify_client import get_spotify, play_album, get_target_device
import time


def main():

    sp = get_spotify()

    device = get_target_device(sp)

    print("Analog Music Player Ready")
    print("-------------------------")

    while True:

        tag_id = input("\nScan tag (or q): ").strip()

        if tag_id.lower() == "q":
            break

        try:
            album_key, album = get_album_for_tag(tag_id)

            print(f"\nMatched: {album['artist']} - {album['album']}")

            play_album(
                sp,
                album["spotify_uri"],
                device["id"]
            )

            print("Playback started.")

        except Exception as e:
            print(f"Error: {e}")

        time.sleep(1)


if __name__ == "__main__":
    main()