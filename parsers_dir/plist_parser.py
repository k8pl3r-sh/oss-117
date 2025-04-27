# python3
# coding=utf-8

import plistlib
import argparse
import os
from distutils.command.config import config
from parsers_dir.abstract_parser import AbstractParser

from utils.log import Log

class PlistParser(AbstractParser):
    def __init__(self, config: dict):
        self.log = Log("PlistParser", config)

    def file_parser(self, file_path: str) -> list[dict]:
        plist_list = []
        try:
            with open(file_path, 'rb') as file:
                # Load the content of the plist file
                plist_data = plistlib.load(file)

                # If the file contains a list, extend plist_list with it
                if isinstance(plist_data, list):
                    plist_list.extend(plist_data)
                # If the file contains a dictionary, add it to plist_list
                elif isinstance(plist_data, dict):
                    plist_list.append(plist_data)

            return plist_list
        except Exception as e:
            self.log.error(f"Error reading the plist file: {e}")
            return None

    def get_index_pattern(self, idx_name: str) -> dict:
        self.log.error(f"get_index_pattern not implemented for this parser")
        return {}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="plist file parser.")
    parser.add_argument('file_path', type=str, help='The path of the plist file to parse')
    
    # Parse the arguments
    args = parser.parse_args()
    """
    # Parse and print the log entries (plist)
    dir_path = os.path.dirname(__file__)
    plist_path = os.path.join(dir_path, args.file_path)
    parsed_log = parse_plist(plist_path)
    print(parsed_log)
    """
