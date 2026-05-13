import argparse

from spotify_client import (
    get_spotify,
    get_target_device,
    play_album,
    stop_playback,
    list_devices
)

from database import get_album


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "album",
        nargs="?",
        help="Album key"
    )

    parser.add_argument(
        "--device",
        help="Target device name"
    )

    parser.add_argument(
        "--stop",
        action="store_true"
    )

    parser.add_argument(
        "--devices",
        action="store_true"
    )

    # Temporary argument for simulating NFC tag input
    parser.add_argument(
        "--tag", 
        help="Simulated NFC tag ID")
    
    args = parser.parse_args()

    sp = get_spotify()

    # List devices
    if args.devices:

        print("\nAvailable devices:\n")

        devices = list_devices(sp)

        for d in devices:

            active = "ACTIVE" if d["is_active"] else ""

            print(f"{d['name']} ({d['type']}) {active}")

        return
    
    # Check NFC tag
    if args.tag:
        from nfc import get_album_for_tag

        try:
            album_key, album = get_album_for_tag(args.tag)
        except Exception as e:
            print(e)
            return

        print("\nNFC tag matched:")
        print(f"Tag: {args.tag}")
        print(f"Album key: {album_key}")
        print(f"{album['artist']} - {album['album']}")

        try:
            device = get_target_device(sp, args.device)
        except Exception as e:
            print(e)
            return

        print(f"\nTarget device: {device['name']}")
        print("\nStarting playback...")

        try:
            play_album(sp, album["spotify_uri"], device["id"])
        except Exception as e:
            print("Playback failed:", e)
            return

        print("\nDone.")
        return

    # Stop playback
    if args.stop:

        print("Stopping playback")

        stop_playback(sp)

        return

    # Play album
    if not args.album:

        print("Provide album key")
        return

    try:

        album = get_album(args.album)

    except Exception as e:

        print(e)
        return

    print("\nAlbum found:")
    print(f"{album['artist']} - {album['album']}")

    try:

        device = get_target_device(
            sp,
            args.device
        )

    except Exception as e:

        print(e)
        return

    print(f"\nTarget device: {device['name']}")

    print("\nStarting playback...")

    try:

        play_album(
            sp,
            album["spotify_uri"],
            device["id"]
        )

    except Exception as e:

        print("Playback failed:", e)
        return

    print("\nDone.")


if __name__ == "__main__":

    main()