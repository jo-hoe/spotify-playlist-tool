import csv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from functools import lru_cache


@lru_cache(maxsize=1)
def get_spotify_client() -> spotipy.Spotify:
    # setup Spotify API
    scope = "user-library-read,playlist-read-private,playlist-modify-private,playlist-modify-public"
    return spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))


def get_playlist_id(playlist_name: str) -> str:
    client = get_spotify_client()

    playlists = client.current_user_playlists()
    for playlist in playlists['items']:
        if playlist['name'] == playlist_name:
            return playlist['id']

    return ''


def get_tracks_in_playlist(playlist_id: str) -> list[dict]:
    tracks = []
    client = get_spotify_client()

    results = client.playlist_items(playlist_id)
    tracks.extend(results['items'])
    while results['next']:
        results = client.next(results)
        tracks.extend(results['items'])
    return tracks


def tracks_to_csv(tracks: list[dict], file_path: str):
    with open(file_path, mode='w', encoding='utf-8', newline='') as file:
        fieldnames = ['artist', 'title']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for track in tracks:
            writer.writerow({
                'artist': track['track']['artists'][0]['name'],
                'title': track['track']['name']
            })


def create_playlist(playlist_name: str) -> str:
    client = get_spotify_client()
    playlist = client.user_playlist_create(
        client.me()['id'], playlist_name, public=False)
    return playlist['id']


def search_track(artist: str, title: str) -> str:
    client = get_spotify_client()
    query = f"artist:{artist} track:{title}"

    results = client.search(q=query, type='track', limit=1)
    tracks = results.get('tracks', {}).get('items', [])
    if tracks:
        return tracks[0]['id']

    return ''


def remove_all_tracks_with_id_from_playlist(playlist_id: str, track_ids: list[str]):
    client = get_spotify_client()
    client.playlist_remove_all_occurrences_of_items(playlist_id, track_ids)


def playlist_add_items(playlist_id: str, track_ids: list[str], item_position: int = None):
    client = get_spotify_client()
    client.playlist_add_items(playlist_id, track_ids, position=item_position)
