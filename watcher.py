# Continuous watcher for NFC tags to trigger Spotify playback
# Scanning only queues albums and commands controls playback

# Imports
from nfc import get_album_for_tag
from spotify_client import (
    get_spotify, 
    play_album, 
    get_target_device,
    resume_playback, 
    stop_playback,
    resume_playback
)
import time

# Helper function to print available commands
def print_help():
    print("\nCommands:")
    print("  scan <tag_id>  Queue tape")
    print("  play           Start queued album")
    print("  stop           Stop current playback")
    print("  eject          Clear queued tape")
    print("  status         Show current state")
    print("  q              Quit")

#
def main():

    # Initialize Spotify client and get target device
    sp = get_spotify()
    device = get_target_device(sp)

    # State variables
    queued_album_key = None
    queued_album = None
    state = "IDLE"

    print("Analog Music Player Ready")
    print("-------------------------")
    print_help()

    while True:

        command = input("\n> ").strip()

        #--- Handle Commands---

        # Quit command
        if command.lower() == "q":
            print("Exiting...")
            break

        # Scan command

        if command.startswith("scan "):
            tag_id = command.replace("scan ", "", 1).strip()

            try:
                album_key, album = get_album_for_tag(tag_id)
                queued_album_key = album_key
                queued_album = album
                state = "TAPE_INSERTED"

                print(f"\nTape inserted.")
                print(f"Queued: {album['artist']} - {album['album']}")

            except Exception as e:
                state = "ERROR"
                print(f"Error: {e}")

        # Play command
        elif command == "play":
            if not queued_album:
                print("No tape inserted.")
                continue

            try:
                # If already playing the same album, just resume
                if state == "STOPPED":
                    print(f"\nResuming: {queued_album['artist']} - {queued_album['album']}")
                    resume_playback(sp, device["id"])
                    state = "PLAYING"
                    print("Playback resumed.")

                # If already playing but different album, stop first then play new
                else:
                    print(f"\nPlaying from beginning: {queued_album['artist']} - {queued_album['album']}")
                    play_album(sp, queued_album["spotify_uri"], device["id"])
                    state = "PLAYING"
                    print("Playback started.")

            except Exception as e:
                state = "ERROR"
                print(f"Playback failed: {e}")

        # Eject command
        elif command == "eject":
            try:
                stop_playback(sp, device_id=device["id"])
                print("Playback stopped.")
            except Exception as e:
                state = "ERROR"
                print(f"Failed to stop during eject: {e}")

            # Reset state
            queued_album_key = None
            queued_album = None
            state = "IDLE"
            print("Tape ejected. Queue cleared.")

        # Stop command
        elif command == "stop":
            try:
                stop_playback(sp, device_id=device["id"])
                state = "STOPPED"
                print("Playback stopped.")
            except Exception as e:
                state = "ERROR"
                print(f"Failed to stop playback: {e}")

        # Status command
        elif command == "status":
            print(f"State: {state}")
            
            if queued_album:
                print(f"Queued tape: {queued_album['artist']} - {queued_album['album']}")
            else:
                print("No tape queued.")

        # Help command
        elif command == "help":
            print_help()

        else:
            print("Unknown command. Type 'help' for a list of commands.")

if __name__ == "__main__":
    main()