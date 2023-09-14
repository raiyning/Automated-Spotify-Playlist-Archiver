import datetime as dt
import logging
import os
import sys

import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os
from os.path import join, dirname


logger = logging.getLogger("discovered-weekly")
handler = logging.StreamHandler(stream=sys.stdout)
handler.setFormatter(logging.Formatter(fmt="%(asctime)s : %(levelname)s : %(message)s"))
logger.addHandler(handler)
logger.setLevel(logging.INFO)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
REDIRECT_URI = os.environ.get("REDIRECT_URI")
USERNAME = os.environ.get("USERNAME")
REFRESH_TOKEN = os.environ.get("REFRESH_TOKEN")

DISCOVER_WEEKLY_PLAYLIST_ID = os.environ.get("DISCOVER_WEEKLY_PLAYLIST_ID")
ALL_DISCOVERED_PLAYLIST_ID = os.environ.get("ALL_DISCOVERED_PLAYLIST_ID")


RELEASE_RADAR_PLAYLIST_ID = os.environ.get("RELEASE_RADAR_PLAYLIST_ID")
ALL_RELEASE_RADAR_PLAYLIST_ID = os.environ.get("ALL_RELEASE_RADAR_PLAYLIST_ID")


def main():
    # Override sample with non-sample file-based env variables,
    # and override both with actual env variables
    logger.info("Start discover weekly archiving")
    client = load_client(
        CLIENT_ID,
        CLIENT_SECRET,
        REDIRECT_URI,
        USERNAME,
        REFRESH_TOKEN,
    )

    # running discover weekly
    playlist_date, dw_uris = parse_this_week(
        client, DISCOVER_WEEKLY_PLAYLIST_ID
    )
    logger.info(f"Found this week's playlist for {playlist_date} ")
    logger.info("Adding to all time playlist")
    add_to_all_time_playlist(client, dw_uris, ALL_DISCOVERED_PLAYLIST_ID)

    # running release radar
    playlist_date, dw_uris = parse_this_week(
        client, RELEASE_RADAR_PLAYLIST_ID
    )
    logger.info(f"Found this week's playlist for {playlist_date} ")
    logger.info("Adding to all time playlist")
    add_to_all_time_playlist(client, dw_uris, ALL_RELEASE_RADAR_PLAYLIST_ID)


    logger.info("Done discover weekly and release radar archiving")


def load_client(client_id, client_secret, redirect_uri, username, refresh_token):
    scopes = ["playlist-read-private", "playlist-modify-private"]
    # Authenticate
    auth_manager = SpotifyOAuth(
        scope=scopes,
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        username=username,
    )
    auth_manager.refresh_access_token(refresh_token)
    client = spotipy.Spotify(auth_manager=auth_manager)
    return client


def parse_this_week(client, discover_weekly_playlist_id):

    # Grab this week's Discover Weekly (DW) and parse for some info
    dw_items = client.playlist_items(discover_weekly_playlist_id)
    playlist_created = dt.datetime.strptime(
        dw_items["items"][0]["added_at"], "%Y-%m-%dT%H:%M:%S%z"
    )
    playlist_date = playlist_created.strftime("%Y-%m-%d")

    dw_uris = [item["track"]["uri"] for item in dw_items["items"]]
    return playlist_date, dw_uris


def add_to_all_time_playlist(client, dw_uris, all_discovered_playlist_id):
    # First, add to the all time DW

    # Determine total number of tracks
    total = client.playlist(all_discovered_playlist_id)["tracks"]["total"]
    # Now, query for the last 5 tracks
    offset = max(0, total - 5)
    last_five = client.playlist_items(all_discovered_playlist_id, offset=offset)
    # If the last 5 tracks match the last 5 from the current week, then we've already added
    # this week's playlist.
    match = len(last_five["items"]) >= 5 and all(
        [
            dw_uri == item["track"]["uri"]
            for dw_uri, item in zip(dw_uris[-5:], last_five["items"])
        ]
    )
    if match:
        logger.info(
            "This script has already been run for this week."
            " Skipping add to all time playlist."
        )
        return

    client.playlist_add_items(all_discovered_playlist_id, dw_uris)


if __name__ == "__main__":
    main()