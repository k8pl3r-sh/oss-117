import re
from datetime import datetime
import os
import argparse
from utils.log import Log
# Define the regex pattern to match the syslog entries with flexible space between month and day
log_pattern = re.compile(
    r'^(?P<month>\w{3})\s{1,2}(?P<day>\d{1,2}) (?P<time>\d{2}:\d{2}:\d{2}) (?P<host>\S+) (?P<process>[^\[]+)(?:\[(?P<pid>\d+)\])?: (?P<message>.*)$'
)
# INFO : manage one and 2 space between month and day (syslog and auth.log

class SyslogParser:
    def __init__(self, config: dict):
        self.log = Log("SyslogParser", config)

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

    def parse_log_entry(self, log_entry: str) -> dict:
        match = log_pattern.match(log_entry)
        if match:
            log_dict = match.groupdict()

            # Convert the log entry to a dictionary
            #log_dict['datetime'] = datetime.strptime(
            #    f"{log_dict.pop('month')} {log_dict.pop('day')} {log_dict.pop('time')}", "%b %d %H:%M:%S")

            # Warning if year not specified -> default to current year
            current_year = datetime.now().year
            default_timezone = "+0000"  # UTC timezone

            # Populate 'datetime' in log_dict with the desired format
            log_dict['datetime'] = datetime.strptime(
                f"{log_dict['day']}/{log_dict['month']}/{current_year}:{log_dict['time']} {default_timezone}",
                "%d/%b/%Y:%H:%M:%S %z"
            )

            # Ensure PID is an integer if present, otherwise set to None
            log_dict['pid'] = int(log_dict['pid']) if log_dict['pid'] else None
            return log_dict
        else:
            self.log.error("Failed to parse log entry:", log_entry)
            return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Syslog file parser.")
    parser.add_argument('file_path', type=str, help='The path of the Syslog file to parse')

    # Parse the arguments
    args = parser.parse_args()


    config = {'log':
                  {'path': "./debug.log",
                    'mode': ["stream", "journal", "file"],
                    'logger': {},
                    'level': "DEBUG"
                   }
    }
    sy = SyslogParser(config)
    dir_path = os.path.dirname(__file__)
    syslog_path = os.path.join(dir_path, args.file_path)
    parsed_log = sy.file_parser(syslog_path)
    #print(parsed_log)
