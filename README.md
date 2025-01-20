# CSV to Spotify Playlist

Small script that take a csv as input and creates a playlist from the entries.

## Prerequisites to run locally

### Python

This program is tested on python 3.13.

### Run via plain Python commands

Install the requirements by.

```PowerShell
pip install -r requirements.txt
```

and run the program by

```PowerShell
python main.py
```

### Run with "make"

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
