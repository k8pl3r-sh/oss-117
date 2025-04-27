import ast
import os
import argparse
import json
from utils.log import Log
from parsers_dir.abstract_parser import AbstractParser


class CustomjsonParser(AbstractParser):
    def __init__(self, config: dict):
        self.log = Log("JsonLineParser", config)

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
        try:
            return json.loads(log_line)
        except json.JSONDecodeError as e:
            try:
                return ast.literal_eval(log_line)
            except Exception as e:
                self.log.error(f"Error parsing JSON line: {e}")
                return None

    def nested_parsing(self, log_line: str) -> dict:
        ll = json.loads(log_line)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="JSONline file parser.")
    parser.add_argument('file_path', type=str, help='The path of the JSONline file to parse')

    # Parse the arguments
    args = parser.parse_args()

    # Parse and print the log entries (Jsonline)
    dir_path = os.path.dirname(__file__)
    jsonline_path = os.path.join(dir_path, args.file_path)
    jl = CustomjsonParser(jsonline_path)
    parsed_log = jl.file_parser(jsonline_path)
    print(parsed_log)
