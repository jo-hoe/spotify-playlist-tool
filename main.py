
import argparse
import os
import csv


def parse_arguments() -> str:
    parser = argparse.ArgumentParser(description='Manages a spotify playlist and allow to fill that list with titles defined in a CSV file.')
    parser.add_argument('-i', '--input-file', type=str, help='path to the csv file (default is set "./music.csv")',
                      default=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'music.csv'))
    args = parser.parse_args()

    return args.input_file

def read_csv_file(file_path) -> dict[str, str]:
    """
    Read the CSV file and return a dictionary with the content.
    """
    data = {}
    with open(file_path, mode='r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            data[row['title']] = row['artist']
    
    return data

def main():
    pass

if __name__ == '__main__':
    main()
