import re
from datetime import datetime
import os
import argparse
from utils.log import Log
from parsers_dir.abstract_parser import AbstractParser

# Regular expression pattern for key-value pairs
kv_pattern = re.compile(
    r'(?P<key>[a-zA-Z0-9._]+)="(?P<value>[^"]*)"|(?P<key_no_value>[a-zA-Z0-9._]+)=(?P<value_no_value>\S+)')

class KeyValueParser(AbstractParser):
    def __init__(self, config: dict):
        self.log = Log("KeyValueParser", config)

    def file_parser(self, file_path: str) -> list[dict]:
        logs = []
        with open(file_path, 'r') as file:
            for line in file:
                try:
                    parsed_line = self.parse_log_entry(line)

                except Exception as e:
                    self.log.error(f"Error processing line: {e}")
                    continue
                logs.append(parsed_line)
        return logs

    def get_index_pattern(self, idx_name: str) -> dict:
        self.log.error(f"get_index_pattern not implemented for this parser")
        return {}

    def parse_log_entry(self, log_line: str) -> dict:
        # Initialize the dictionary to store key-value pairs
        log_data = {}

        # Find all matches
        for match in kv_pattern.finditer(log_line):
            if match.group('value'):
                key = match.group('key')
                value = match.group('value')
            elif match.group('value_no_value'):
                key = match.group('key_no_value')
                value = match.group('value_no_value')
            elif match.group('key_no_value_no_eq'):
                key = match.group('key_no_value_no_eq')
                value = None
            else:
                continue

            # Handle specific parsing for timestamps
            if key == 'time':
                value = datetime.fromisoformat(value.replace('Z', '+00:00'))

            # Add key-value pair to dictionary
            log_data[key] = value

        return log_data


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Key-value file parser.")
    parser.add_argument('file_path', type=str, help='The path of the Key-value file to parse')

    # Parse the arguments
    args = parser.parse_args()
    """
    # Parse and print the log entries (Key-value)
    dir_path = os.path.dirname(__file__)
    kv_path = os.path.join(dir_path, args.file_path)
    parsed_log = parse_key_value(kv_path)
    print(parsed_log)
    """