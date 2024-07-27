import re
from datetime import datetime

# Regular expression pattern for key-value pairs
kv_pattern = re.compile(
    r'(?P<key>[a-zA-Z0-9._]+)="(?P<value>[^"]*)"|(?P<key_no_value>[a-zA-Z0-9._]+)=(?P<value_no_value>\S+)')


def parse_key_value(log_line):
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


if __name__ == '__main__':
    # Sample log lines
    logs = [
        'time="2022-02-28T11:12:11.529942293Z" level=info msg="authorized request" go.version=go1.16.15 http.request.host="192.168.3.2:5000" http.request.id=cf19cbbb-ff47-4f00-9010-62faf9de0628 http.request.method=POST http.request.remoteaddr="192.168.3.13:57658" http.request.uri="/v2/eshell/genword/blobs/uploads/" http.request.useragent="docker/20.10.18 go/go1.19.1 git-commit/e42327a6d3 kernel/5.19.10-1 os/linux arch/amd64 UpstreamClient(Docker-Client/20.10.18 \(linux\))" vars.name="eshell/genword"',
        'time="2022-02-28T11:12:11.535286575Z" level=info msg="response completed" go.version=go1.16.15 http.request.host="192.168.3.2:5000" http.request.id=64ac4168-8a48-47d6-8a08-d6159f44a794 http.request.method=POST http.request.remoteaddr="192.168.3.13:57648" http.request.uri="/v2/eshell/genword/blobs/uploads/"'
    ]

    # Parse and print the logs
    for log in logs:
        parsed_log = parse_key_value(log)
        print(parsed_log)
