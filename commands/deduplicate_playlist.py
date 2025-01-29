from argparse import ArgumentParser, Namespace
import logging

from commands.base_command import Command
from commands.common.spotify_client import get_playlist_id, get_tracks_in_playlist, playlist_add_items, remove_all_tracks_with_id_from_playlist


class DeduplicatePlaylist(Command):

    COMMAND_NAME = 'deduplicate_playlist'

    def __init__(self, args: Namespace):
        self.playlist_name = args.playlist_name

    @staticmethod
    def add_arguments(parser: ArgumentParser):
        parser.add_argument('-p', '--playlist-name', type=str,
                            help='Name of the playlist to deduplicate', required=True)

    @staticmethod
    def get_command_name() -> str:
        return DeduplicatePlaylist.COMMAND_NAME

    @staticmethod
    def get_help_text() -> str:
        return 'Deduplicate tracks from a Spotify playlist and export them to a CSV file.'

    def execute(self):
        playlist_id = get_playlist_id(self.playlist_name)

        if not playlist_id:
            logging.error(f'Playlist {self.playlist_name} not found.')
            return

        # this can also be solved with less requests by using
        # basic arithmetic operations on the list of tracks
        while True:
            tracks = get_tracks_in_playlist(playlist_id)

            track_occurrences = {}
            for i, track in enumerate(tracks):
                track_occurrences[track['track']['id']] = {
                    "track_name": track['track']['name'],
                    "positions": track_occurrences.get(track['track']['id'], {}).get("positions", []) + [i]
                }

            duplicated_tracks = {
                track_id: item for track_id, item in track_occurrences.items() if len(item["positions"]) > 1
            }

            if len(duplicated_tracks) <= 0:
                break

            track_id, item = next(iter(duplicated_tracks.items()))

            logging.info(
                f'removing duplicates of track "{item["track_name"]}" (number of items to remove: {len(item["positions"]) - 1})')
            remove_all_tracks_with_id_from_playlist(playlist_id, [track_id])
            playlist_add_items(playlist_id, [track_id], item["positions"][0])
