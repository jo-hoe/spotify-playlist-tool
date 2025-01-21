
import os
import csv
import logging
import argparse
from datetime import datetime

import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv


def parse_arguments() -> tuple[str, str]:
    parser = argparse.ArgumentParser(
        description='Manages a spotify playlist and allow to fill that list with titles defined in a CSV file.')
    parser.add_argument('-i', '--input-file', type=str, help='path to the csv file (default is set "music.csv")',
                        default=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'music.csv'))
    parser.add_argument('-p', '--playlist-name', type=str, help='name of the playlist where the songs will be added (default is empty and a new playlist will be created)',
                        default='')
    args = parser.parse_args()

    return args.input_file, args.playlist_name


def get_existing_playlist_id(sp: spotipy.Spotify, playlist_name: str) -> str:
    playlists = sp.current_user_playlists()
    for playlist in playlists['items']:
        if playlist['name'] == playlist_name:
            return playlist['id']

    return ''


def create_playlist(sp: spotipy.Spotify, playlist_name: str) -> str:
    playlist = sp.user_playlist_create(
        sp.me()['id'], playlist_name, public=False)
    return playlist['id']


def get_playlist_id(sp: spotipy.Spotify, playlist_name: str):
    if playlist_name == '':
        playlist_id = create_playlist(
            sp, f'playlist_{datetime.now().strftime("%Y%m%d%H%M%S")}')
    else:
        playlist_id = get_playlist_id(sp, playlist_name)
        if playlist_id == '':
            print(
                f'Playlist {playlist_name} not found. Either leave the playlist name empty or provide an existing playlist name.')


def search_track(sp: spotipy.Spotify, artist: str, title: str, album: str, release_year: str) -> str:
    query = f"artist:{artist} track:{title}"
    if album:
        query += f" album:{album}"
    if release_year:
        query += f" year:{release_year}"

    results = sp.search(q=query, type='track', limit=1)
    tracks = results.get('tracks', {}).get('items', [])
    if tracks:
        return tracks[0]['id']

    return ''


def add_tracks_to_playlist(sp: spotipy.Spotify, playlist_id: str, tracks: csv.DictReader) -> None:
    for row in tracks.values():
        track_id = search_track(
            sp, row['artist'], row['title'], row.get('album', ''), row.get('release_year', ''))
        if track_id:
            sp.playlist_add_items(playlist_id, [track_id])
        else:
            logging.warning(
                f'Track {row["artist"]} - {row["title"]} not found.')


def read_csv_file(file_path) -> csv.DictReader:
    """
    Read the CSV file and return a dictionary with the content.

    The CSV file is expected to have at least the following headers/columns:
    - artist
    - title
    And optionally:
    - album
    - release_year
    """
    data = {}
    with open(file_path, mode='r', encoding='utf-8') as file:
        # load data into a DictReader but ensure that the fieldnames
        # are not case sensitive and have no leading/trailing spaces
        # whitespace are also removed for the values
        reader = csv.DictReader(file)
        for row in reader:
            cleaned_row = {k.strip().lower(): v.strip()
                           for k, v in row.items()}
            data[reader.line_num] = cleaned_row

    return data


def main():
    load_dotenv()
    input_file, playlist_name = parse_arguments()

    if not os.path.exists(input_file):
        print(f'File {input_file} does not exist.')
        return
    data = read_csv_file(input_file)

    scope = "user-library-read"
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

    playlist_id = get_playlist_id(sp, playlist_name)


if __name__ == '__main__':
    main()
