from argparse import ArgumentParser, Namespace
import logging
import os

from tqdm import tqdm
from requests import get

from commands.base_command import Command
from commands.common.spotify_client import get_playlist_id, get_tracks_in_playlist


class ExportPlaylistAlbumCovers(Command):

    COMMAND_NAME = 'export_playlist_album_covers'

    def __init__(self, args: Namespace):
        self.output_file = args.output_directory
        self.playlist_name = args.playlist_name

    @staticmethod
    def add_arguments(parser: ArgumentParser):
        parser.add_argument('-o', '--output-directory', type=str, help='path to the output directory (default is set "/output/album_covers")',
                            default=os.path.join(os.path.dirname(os.path.basename(os.path.abspath(__file__))), 'output', 'album_covers'))
        parser.add_argument('-p', '--playlist-name', type=str,
                            help='Name of the playlist to export', required=True)

    @staticmethod
    def get_command_name() -> str:
        return ExportPlaylistAlbumCovers.COMMAND_NAME

    @staticmethod
    def get_help_text() -> str:
        return 'Export album covers from a Spotify playlist to a CSV file.'

    def execute(self):
        playlist_id = get_playlist_id(self.playlist_name)

        if not playlist_id:
            logging.error(f'Playlist {self.playlist_name} not found.')
            return

        tracks = get_tracks_in_playlist(playlist_id)
        album_covers = {}
        for track in tqdm(tracks, desc="Getting details of tracks in playlist"):
            album_id = track['track']['album']['id']
            album_name = track['track']['album']['name']
            key = f'{album_name}_spotifyid_{album_id}'
            album_covers[key] = track['track']['album']['images'][0]['url']

        directory_path = self.create_output_directory()
        self.download_album_covers(album_covers, directory_path)

    def sanitize_filename(self, name: str) -> str:
        return "".join(c for c in name if c.isalnum() or c in (' ', '_', '-')).rstrip()

    def download_album_covers(self, album_covers: dict, directory_path: str):
        for key, url in tqdm(album_covers.items(), desc="Downloading album covers"):
            response = get(url)
            if response.status_code == 200:
                sanitized_name = self.sanitize_filename(key)
                with open(os.path.join(directory_path, f'{sanitized_name}.jpg'), 'wb') as f:
                    f.write(response.content)
            else:
                logging.error(
                    f'Failed to download album cover for {key} from {url}')

    def create_output_directory(self) -> str:
        if not os.path.exists(self.output_file):
            os.makedirs(self.output_file)
        return self.output_file
