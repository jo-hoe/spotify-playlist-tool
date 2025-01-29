from argparse import ArgumentParser, Namespace
import csv
import logging
import os

from requests import get

from commands.base_command import Command
from commands.common.spotify_client import get_playlist_id, get_tracks_in_playlist


class ExportPlaylist(Command):

    COMMAND_NAME = 'export_playlist'

    def __init__(self, args: Namespace):
        self.output_file = args.output_file
        self.playlist_name = args.playlist_name

    @staticmethod
    def add_arguments(parser: ArgumentParser):
        parser.add_argument('-o', '--output-file', type=str, help='path to the csv file (default is set "exported_playlist.csv")',
                            default=os.path.join(os.path.dirname(os.path.basename(os.path.abspath(__file__))), 'exported_playlist.csv'))
        parser.add_argument('-p', '--playlist-name', type=str,
                            help='Name of the playlist to export', required=True)

    @staticmethod
    def get_command_name() -> str:
        return ExportPlaylist.COMMAND_NAME

    @staticmethod
    def get_help_text() -> str:
        return 'Export tracks from a Spotify playlist to a CSV file.'

    def execute(self):
        playlist_id = get_playlist_id(self.playlist_name)

        if not playlist_id:
            logging.error(f'Playlist {self.playlist_name} not found.')
            return

        tracks = get_tracks_in_playlist(playlist_id)
        self.write_csv_file(tracks)

    def write_csv_file(self, data: list[dict]):
        with open(self.output_file, mode='w', encoding='utf-8', newline='') as file:
            fieldnames = ['artist', 'title', 'album']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for track in data:
                writer.writerow({
                    'artist': track['track']['artists'][0]['name'],
                    'title': track['track']['name'],
                    'album': track['track']['album']['name']
                })
