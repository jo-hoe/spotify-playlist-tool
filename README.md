# Spotify Playlist Organization Tool

Small script that allows to manage a Spotify playlist.

Current functions:

```txt
usage: main.py [-h] {import_playlist,export_playlist,deduplicate_playlist,sort_playlist} ...

Allows to organize your Spotify playlists.

positional arguments:
  {import_playlist,export_playlist,deduplicate_playlist,sort_playlist}
    import_playlist     Import tracks from a CSV file to a Spotify playlist.
    export_playlist     Export tracks from a Spotify playlist to a CSV file.
    deduplicate_playlist
                        Deduplicate tracks from a Spotify playlist and export them to a CSV file.
    sort_playlist       Sorts a playlist by a given field ('random' sorting is the default).

options:
  -h, --help            show this help message and exit
```

You can get more information about the subcommands by running `-h` after the subcommand.
Here is an example for the `import_playlist` subcommand:

```bash
python main.py import_playlist -h
```

## Word for caution

This is a script I wrote quickly.
It does not have integration tests, nor is it particularly robust.
Before you use it to alter your playlists, consider exporting your playlist to CSV for a backup.

## Setup

### Secrets

The script assumes that there is a `.env` file in the directory where the script is with the following content:

```txt
SPOTIPY_CLIENT_ID=your_client_id
SPOTIPY_CLIENT_SECRET=your_client_secret
SPOTIPY_REDIRECT_URI=your_redirect_uri (e.g. 'http://127.0.0.1:9090')
```

You can get these values by creating a Spotify Developer account and [creating a new app](https://developer.spotify.com/documentation/web-api/concepts/apps).

### Dependencies

You will also need to ensure you have all the required packages installed.
You can do this by running:

```bash
pip install -r requirements.txt
```

or use a virtual environment:

```bash
python -m venv .venv
```

Alternatively, you can use the provided `make` commands to install the dependencies.

```bash
make init
```

## CSV File

It is expected that the csv file has the following format:

```csv
title,artist
"Song 1","Artist 1"
Song_2,Artist_2
```

The CSV can have more columns, but the script will only use the `title` and `artist`.
Currently, the script requires that the separator is a `,`.

## Run with "make"

The project is using `make`.
`make` is not strictly required, but it helps and documents commonly used commands.

You can directly install it from [gnuwin32](https://gnuwin32.sourceforge.net/packages/make.htm) or via `winget`

```PowerShell
winget install GnuWin32.Make
```

You will also need Docker and Python.
Run `make init` to install all dependencies in a virtual Python environment.

### How to Use

You can check all `make` commands by running.

```bash
make help
```
