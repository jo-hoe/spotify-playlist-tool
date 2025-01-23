# CSV to Spotify Playlist

Small script that takes a csv as input and creates a playlist from the entries.

## Setup

### Secrets

The script assumes that there is a `.env` file in the directory where the script is with the following content:

```txt
SPOTIPY_CLIENT_ID=your_client_id
SPOTIPY_CLIENT_SECRET=your_client_secret
SPOTIPY_REDIRECT_URI=your_redirect_uri
```

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

## Run

### Plain Python

You can run the script by running the following command in the terminal:

```bash
python main.py -i <my path to the csv>my.csv -p "My Playlist"
```

Ensure you are using a python installation that has the required packages installed.

You can use the following parameters:

```txt
Manages a spotify playlist and allow to fill that list with titles defined in a CSV file.

options:
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input-file INPUT_FILE
                        path to the csv file (default is set "music.csv")
  -p PLAYLIST_NAME, --playlist-name PLAYLIST_NAME
                        name of the playlist where the songs will be added (default is empty and a new playlist will be created)
```

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
