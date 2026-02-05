
from abc import ABC, abstractmethod
from argparse import ArgumentParser


class Command(ABC):

    @abstractmethod
    def execute(self) -> None:
        pass

    @abstractmethod
    def get_command_name(self) -> str:
        pass

    @staticmethod
    @abstractmethod
    def add_arguments(parser: ArgumentParser) -> None:
        pass

    @abstractmethod
    def get_help_text(self) -> str:
        pass
