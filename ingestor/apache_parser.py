import re
from datetime import datetime

# Regular expression to match the Apache log entry
log_pattern = re.compile(
    r'(?P<host>\S+) '                  # host %h
    r'(?P<identity>\S+) '              # identity %l
    r'(?P<user>\S+) '                  # user %u
    r'\[(?P<time>.*?)\] '              # time %t
    r'"(?P<request>.*?)" '             # request "%r"
    r'(?P<status>[0-9]+) '             # status %>s
    r'(?P<size>\S+)'                   # size %b
)

# Sample log entry for testing

def parse_apache(log_entry):
    match = log_pattern.match(log_entry)
    if match:
        log_dict = match.groupdict()
        # Convert size to an integer or None if '-'
        log_dict['size'] = int(log_dict['size']) if log_dict['size'] != '-' else None
        # Convert time to a datetime object
        log_dict['time'] = datetime.strptime(log_dict['time'], '%d/%b/%Y:%H:%M:%S %z')
        return log_dict
    else:
        return None
