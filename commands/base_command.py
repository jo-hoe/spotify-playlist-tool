
from abc import ABC, abstractmethod
from argparse import ArgumentParser

class Command(ABC):

    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def get_command_name(self):
        pass

    @staticmethod
    @abstractmethod
    def add_arguments(parser: ArgumentParser):
        pass

    @abstractmethod
    def get_help_text(self):
        pass