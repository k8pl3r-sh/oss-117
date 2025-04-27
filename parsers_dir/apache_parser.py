import re
from datetime import datetime
import json
from utils.log import Log
import argparse
import os


# Regular expression to match Apache log entry with Method, URI, HTTP Version, and User Agent
log_pattern = re.compile(
    r'(?P<host>\S+) '  # host %h
    r'(?P<identity>\S+) '  # identity %l
    r'(?P<user>\S+) '  # user %u
    r'\[(?P<time>.*?)\] '  # time %t
    r'"(?P<method>[A-Z]+)?(?P<uri>.*?)? (?P<protocol>HTTP/\d\.\d)?" '  # request "%r"
    r'(?P<status>[0-9]+) '  # status %>s
    r'(?P<size>\S+) '  # size %b
    r'"(?P<referrer>.*?)" '  # referrer
    r'"(?P<user_agent>.*?)"'  # user agent
)

class ApacheParser:
    def __init__(self, config: dict):
        self.log = Log("ApacheParser", config)

    def file_parser(self, file_path: str) -> list[dict]:
        logs = []
        with open(file_path, 'r') as file:
            for line in file:
                try:
                    parsed_line = self.parse_log_entry(line)

                except Exception as e:
                    self.log.debug(f"Error processing line: {e}")
                    continue
                logs.append(parsed_line)
        return logs

    def parse_log_entry(self, log_entry: str) -> dict:
        match = log_pattern.match(log_entry)
        if match:
            log_dict = match.groupdict()

            # Convert size to an integer or None if '-'
            log_dict['size'] = int(log_dict['size']) if log_dict['size'] != '-' and log_dict['size'].strip() else None

            # Convert time to a datetime object
            try:
                log_dict['time'] = datetime.strptime(log_dict['time'], '%d/%b/%Y:%H:%M:%S %z')
            except ValueError:
                log_dict['time'] = None

            # Check for empty or missing values and set them to None
            for key, value in log_dict.items():
                if isinstance(value, str) and (value == '-' or not value.strip()):
                    log_dict[key] = None

            self.log.debug(f"log_dict: {log_dict}")
            return log_dict
        else:
            self.log.debug(f"Failed to parse log entry: {log_entry}")
            # TODO : Resolve error on : Failed to parse log entry: 192.168.1.14 - - [23/May/2023:09:12:20 +0100] "-" 408 0 "-" "-"
            # from file : /home/runner/ingestor/data/dolibarr_access.log
            return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Apache logs file parser.")
    parser.add_argument('file_path', type=str, help='The path of the Apache log file to parse')

    # Parse the arguments
    args = parser.parse_args()

    """
    # Parse and print the log entries (Docker)
    dir_path = os.path.dirname(__file__)
    apache_logs_path = os.path.join(dir_path, args.file_path)
    parsed_log = parse_apache(apache_logs_path)
    print(parsed_log)
    """