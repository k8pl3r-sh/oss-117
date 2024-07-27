import re
from datetime import datetime

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


def parse_apache(log_entry):
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

        return log_dict
    else:
        print("Failed to parse log entry:", log_entry)
        # TODO : Resolve error on : Failed to parse log entry: 192.168.1.14 - - [23/May/2023:09:12:20 +0100] "-" 408 0 "-" "-"
        # from file : /home/runner/ingestor/data/dolibarr_access.log
        return None


if __name__ == '__main__':
    # Sample Apache log entries
    log_entries = [
        '83.149.9.216 - - [17/May/2015:10:05:03 +0000] "GET /presentations/logstash-monitorama-2013/images/kibana-search.png HTTP/1.1" 200 203023 "http://semicomplete.com/presentations/logstash-monitorama-2013/" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.77 Safari/537.36"',
        '83.149.9.216 - - [17/May/2015:10:05:43 +0000] "GET /presentations/logstash-monitorama-2013/images/kibana-dashboard3.png HTTP/1.1" 200 171717 "http://semicomplete.com/presentations/logstash-monitorama-2013/" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.77 Safari/537.36"',
        # An example with some fields potentially empty
        '83.149.9.216 - - [17/May/2015:10:10:00 +0000] "POST / HTTP/1.1" 400 - "-" "-"'
    ]

    # Parse and print the log entries
    for log in log_entries:
        parsed_log = parse_apache(log)
        print(parsed_log)
