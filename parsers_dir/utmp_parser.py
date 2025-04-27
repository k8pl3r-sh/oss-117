import struct
import time
import argparse
import os
from utils.log import Log
from parsers_dir.abstract_parser import AbstractParser

class UtmpParser(AbstractParser):
    UTMP_FORMAT = "hi32s4s32s256shhiii4i20s"
    UTMP_SIZE = struct.calcsize(UTMP_FORMAT)

    def __init__(self, config: dict):
        self.log = Log("UtmpParser", config)

    def file_parser(self, file_path: str) -> list[dict]:
        utmp_entries = []
        try:
            with open(file_path, "rb") as file:
                while entry := file.read(self.UTMP_SIZE):
                    fields = struct.unpack(self.UTMP_FORMAT, entry)
                    user = fields[2].decode("utf-8", "ignore").strip("\x00")
                    terminal = fields[4].decode("utf-8", "ignore").strip("\x00")
                    host = fields[5].decode("utf-8", "ignore").strip("\x00")
                    timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(fields[9]))

                    if user:
                        utmp_entries.append({
                            "User": user,
                            "Terminal": terminal,
                            "Host": host,
                            "Time": timestamp
                        })
        except Exception as e:
            self.log.error(f"Error reading the UTMP file: {e}")
        return utmp_entries

    def get_index_pattern(self, idx_name: str) -> dict:
        self.log.error(f"get_index_pattern not implemented for this parser")
        return {}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="UTMP file parser.")
    parser.add_argument('file_path', type=str, help='The path of the UTMP file to parse')

    # Parse the arguments
    args = parser.parse_args()

    # Create parser instance with a dummy config (replace with actual config if needed)
    config = {}
    utmp_parser = UtmpParser(config)

    # Parse and print the log entries (UTMP)
    parsed_log = utmp_parser.file_parser(args.file_path)
    for entry in parsed_log:
        print(entry)