from argparse import ArgumentParser, Namespace
import csv
from datetime import datetime
import logging
import os
from tqdm import tqdm

from commands.base_command import Command
from commands.common import spotify_client


class ImportPlaylist(Command):

    COMMAND_NAME = 'import_playlist'

    def __init__(self, args: Namespace):
        self.input_file = args.input_file
        self.playlist_name = args.playlist_name

    @staticmethod
    def add_arguments(parser: ArgumentParser):
        parser.add_argument('-i', '--input-file', type=str, help='path to the csv file (default is set "music.csv")',
                            default=os.path.join(os.path.dirname(os.path.basename(os.path.abspath(__file__))), 'music.csv'))
        parser.add_argument('-p', '--playlist-name', type=str, help='name of the playlist where the songs will be added (default is empty and a new playlist will be created)',
                            default='')

    @staticmethod
    def get_command_name() -> str:
        return ImportPlaylist.COMMAND_NAME
    
    @staticmethod
    def get_help_text() -> str:
        return 'Import tracks from a CSV file to a Spotify playlist.'

    def execute(self):
        # read CSV file
        if not os.path.exists(self.input_file):
            logging.error(f'File {self.input_file} does not exist.')
            return
        data = self.read_csv_file(self.input_file)

        date_string = datetime.now().strftime("%Y%m%d%H%M%S")

        # create or get playlist
        if self.playlist_name == '':
            playlist_id = spotify_client.create_playlist(
                f'csv_playlist_{date_string}')
        else:
            playlist_id = spotify_client.get_playlist_id(
                self.playlist_name)
            if playlist_id == '':
                playlist_id = spotify_client.create_playlist(
                    self.playlist_name)
        if playlist_id == '':
            return

        # add tracks to playlist
        not_added_tracks = self.add_tracks_to_playlist(playlist_id, data)
        self.create_report_file(not_added_tracks, date_string)

    def add_tracks_to_playlist(self, playlist_id: str, tracks: csv.DictReader) -> list[dict]:
        not_found_tracks = []
        found_track_ids = []

        for row in tqdm(tracks.values(), desc="searching for matching tracks in spotify"):
            track_id = spotify_client.search_track(row['artist'], row['title'])
            if track_id:
                found_track_ids.append(track_id)
            else:
                not_found_tracks.append(row)

        spotify_client.playlist_add_items(playlist_id, found_track_ids)
        return not_found_tracks

    def read_csv_file(self, file_path) -> csv.DictReader:
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

    def create_report_file(self, not_added_tracks: list[dict], date_string: str):
        # store not added tracks in a file
        if not_added_tracks:
            report_file_name = f'not_added_tracks{date_string}.csv'

            with open(report_file_name, mode='w', encoding='utf-8', newline='') as file:
                writer = csv.DictWriter(
                    file, fieldnames=not_added_tracks[0].keys())
                writer.writeheader()
                writer.writerows(not_added_tracks)

            logging.warning(
                f'{len(not_added_tracks)} tracks could not be added to the playlist. Most likely they were not found. See file {report_file_name} for details.')
