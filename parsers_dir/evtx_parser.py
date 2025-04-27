# python3
# coding=utf-8

import Evtx.Evtx as evtx
import xmltodict
import argparse
import os
from utils.log import Log
from parsers_dir.abstract_parser import AbstractParser

class EvtxParser(AbstractParser):
    def __init__(self, config: dict):
        self.log = Log("EvtxParser", config)


    def file_parser(self, file_path: str) -> list[dict]:
        evtx_list = []
        try:
            # Iterate througth EVTX records
            with evtx.Evtx(file_path) as log:
                for record in log.records():
                    record_dict = xmltodict.parse(record.xml())
                    evtx_list.append(record_dict)
        except Exception as e:
            self.log.error(f"Error reading the EVTX file: {e}")
        return evtx_list

    def get_index_pattern(self, idx_name: str) -> dict:
        self.log.error(f"get_index_pattern not implemented for this parser")
        return {}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="EVTX file parser.")
    parser.add_argument('file_path', type=str, help='The path of the EVTX file to parse')
    
    # Parse the arguments
    args = parser.parse_args()

    """
    # Parse and print the log entries (EVTX)
    dir_path = os.path.dirname(__file__)
    evtx_path = os.path.join(dir_path, args.file_path)
    parsed_log = parse_evtx(evtx_path)
    print(parsed_log)
    """
