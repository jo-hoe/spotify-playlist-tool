from argparse import ArgumentParser, Namespace
import logging

from commands.base_command import Command
from commands.common.spotify_client import get_playlist_id, get_tracks_in_playlist, playlist_add_items, remove_all_tracks_with_id_from_playlist
import random


class SortPlaylist(Command):

    COMMAND_NAME = 'sort_playlist'

    SORT_OPTIONS = {
        'title': 'name',
        'popularity': 'popularity',
        'duration': 'duration_ms',
        'random': None
    }

    ORDER_OPTIONS = ['asc', 'desc']

    def __init__(self, args: Namespace):
        self.playlist_name = args.playlist_name
        self.sort_by = args.sort_by
        self.order = args.order

    @staticmethod
    def add_arguments(parser: ArgumentParser):
        parser.add_argument('-p', '--playlist-name', type=str,
                            help='Name of the playlist to sort', required=True)
        parser.add_argument('-s', '--sort-by', choices=SortPlaylist.SORT_OPTIONS.keys(),
                            default='random', help='Field to sort by. Random means that list will be sorted randomly for this point (default: random)')
        parser.add_argument('-o', '--order', choices=SortPlaylist.ORDER_OPTIONS,
                            default='asc', help='Order of sorting')

    @staticmethod
    def get_command_name() -> str:
        return SortPlaylist.COMMAND_NAME

    @staticmethod
    def get_help_text() -> str:
        return f'Sorts a playlist by a given field ("random" sorting is the default).'

    def execute(self):
        playlist_id = get_playlist_id(self.playlist_name)

        tracks = get_tracks_in_playlist(playlist_id)

        if not tracks:
            logging.info(f"No tracks found in playlist {self.playlist_name}")
            return

        sort_by = SortPlaylist.SORT_OPTIONS[self.sort_by]
        order = self.order

        if sort_by == None:
            random.shuffle(tracks)
        else:
            reverse = (order == 'desc')
            tracks.sort(key=lambda x: x['track'][sort_by], reverse=reverse)

        track_ids = []
        for track in tracks:
            track_ids.append(track['track']['id'])

        remove_all_tracks_with_id_from_playlist(playlist_id, track_ids)
        playlist_add_items(playlist_id, track_ids)

        if sort_by == None:
            logging.info(f"Playlist {self.playlist_name} sorted randomly")
        else:
            logging.info(f"Playlist {self.playlist_name} sorted by {sort_by} in {order} order")
