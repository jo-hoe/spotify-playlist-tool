
import os
import csv
import logging
import argparse
from datetime import datetime

from tqdm import tqdm
from dotenv import load_dotenv

import spotipy
from spotipy.oauth2 import SpotifyOAuth


def parse_arguments() -> tuple[str, str]:
    parser = argparse.ArgumentParser(
        description='Manages a spotify playlist and allow to fill that list with titles defined in a CSV file.')
    parser.add_argument('-i', '--input-file', type=str, help='path to the csv file (default is set "music.csv")',
                        default=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'music.csv'))
    parser.add_argument('-p', '--playlist-name', type=str, help='name of the playlist where the songs will be added (default is empty and a new playlist will be created)',
                        default='')
    args = parser.parse_args()

    return args.input_file, args.playlist_name


def get_playlist_id(sp: spotipy.Spotify, playlist_name: str) -> str:
    playlists = sp.current_user_playlists()
    for playlist in playlists['items']:
        if playlist['name'] == playlist_name:
            return playlist['id']

    return ''


def create_playlist(sp: spotipy.Spotify, playlist_name: str) -> str:
    playlist = sp.user_playlist_create(
        sp.me()['id'], playlist_name, public=False)
    return playlist['id']


def search_track(sp: spotipy.Spotify, artist: str, title: str) -> str:
    query = f"artist:{artist} track:{title}"

    results = sp.search(q=query, type='track', limit=1)
    tracks = results.get('tracks', {}).get('items', [])
    if tracks:
        return tracks[0]['id']

    return ''


def add_tracks_to_playlist(sp: spotipy.Spotify, playlist_id: str, tracks: csv.DictReader) -> list[dict]:
    not_added_tracks = []

    for row in tqdm(tracks.values(), desc="adding tracks to playlist"):
        track_id = search_track(
            sp, row['artist'], row['title'])
        if track_id:
            sp.playlist_add_items(playlist_id, [track_id])
        else:
            not_added_tracks.append(row)

    return not_added_tracks


def read_csv_file(file_path) -> csv.DictReader:
    """
    Read the CSV file and return a dictionary with the content.

    The CSV file is expected to have at least the following headers/columns:
    - artist
    - title
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
    # parse input parameters
    load_dotenv()
    input_file, playlist_name = parse_arguments()

    # read CSV file
    if not os.path.exists(input_file):
        print(f'File {input_file} does not exist.')
        return
    data = read_csv_file(input_file)

    # setup Spotify API
    scope = "user-library-read,playlist-read-private,playlist-modify-private,playlist-modify-public"
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

    # create or get playlist
    if playlist_name == '':
        playlist_id = create_playlist(
            sp, f'playlist_{datetime.now().strftime("%Y%m%d%H%M%S")}')
    else:
        playlist_id = get_playlist_id(sp, playlist_name)
        if playlist_id == '':
            print(
                f'Playlist {playlist_name} not found. Either leave the playlist name empty or provide an existing playlist name.')
    if playlist_id == '':
        return

    # add tracks to playlist
    not_added_tracks = add_tracks_to_playlist(sp, playlist_id, data)

    # store not added tracks in a file
    if not_added_tracks:
        report_file_name = 'not_added_tracks.csv'

        logging.warning(
            f'{len(not_added_tracks)} tracks could not be added to the playlist. See file {report_file_name} for details.')
        
        with open(report_file_name, mode='w', encoding='utf-8') as file:
            writer = csv.DictWriter(
                file, fieldnames=not_added_tracks[0].keys())
            writer.writeheader()
            writer.writerows(not_added_tracks)


if __name__ == '__main__':
    main()
