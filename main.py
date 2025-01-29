import argparse
from dotenv import load_dotenv

from commands.base_command import Command
from commands.export_playlist import ExportPlaylist
from commands.import_playlist import ImportPlaylist


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='Allows to organize your Spotify playlists.')

    subparsers = parser.add_subparsers(dest='command', required=True)

    # Add subparser for each command
    import_playlist_parser = subparsers.add_parser(
        ImportPlaylist.get_command_name(), help=ImportPlaylist.get_help_text())
    ImportPlaylist.add_arguments(import_playlist_parser)

    export_playlist_parser = subparsers.add_parser(
        ExportPlaylist.get_command_name(), help=ExportPlaylist.get_help_text())
    ExportPlaylist.add_arguments(export_playlist_parser)

    args = parser.parse_args()
    return args


def create_command(command: str, args: argparse.Namespace) -> Command:
    if command == ImportPlaylist.get_command_name():
        return ImportPlaylist(args)
    if command == ExportPlaylist.get_command_name():
        return ExportPlaylist(args)

    # Add more commands here as needed
    raise ValueError(f'Unknown command: {command}')


def main():
    # parse input parameters
    load_dotenv()
    args = parse_arguments()

    command = create_command(args.command, args)

    command.execute()


if __name__ == '__main__':
    main()
