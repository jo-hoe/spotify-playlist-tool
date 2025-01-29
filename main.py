import argparse
from dotenv import load_dotenv

from commands.base_command import Command
from commands.export_playlist import ExportPlaylist
from commands.import_playlist import ImportPlaylist

# List of available commands
COMMANDS = [
    ImportPlaylist,
    ExportPlaylist
]

def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='Allows to organize your Spotify playlists.')

    subparsers = parser.add_subparsers(dest='command', required=True)

    # Add subparser for each command
    for command in COMMANDS:
        subparser = subparsers.add_parser(
            command.get_command_name(), help=command.get_help_text())
        command.add_arguments(subparser)

    args = parser.parse_args()
    return args


def create_command(command: str, args: argparse.Namespace) -> Command:
    for cmd in COMMANDS:
        if command == cmd.get_command_name():
            return cmd(args)
    raise ValueError(f'Unknown command: {command}')


def main():
    # parse input parameters
    load_dotenv()
    args = parse_arguments()

    command = create_command(args.command, args)

    command.execute()


if __name__ == '__main__':
    main()
