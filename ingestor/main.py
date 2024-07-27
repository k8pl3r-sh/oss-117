from opensearchpy import OpenSearch
from parsers.apache_parser import parse_apache
from typing import Callable
from parsers.jsonline_parser import parse_jsonline
from opensearchpy import helpers

# TODO : logging

# Initialize the OpenSearch client
host = '127.0.0.1'
port = 9200
auth = ('admin', 'eLej1Zvctg#')

# Create the client with SSL/TLS and hostname verification disabled.
client = OpenSearch(
    hosts=[{'host': host, 'port': port}],
    http_compress=True,  # enables gzip compression for request bodies
    http_auth=auth,
    use_ssl=True,
    verify_certs=False,
    ssl_assert_hostname=False,
    ssl_show_warn=False
)


def create_index(index_name: str):
    index_body = {
        'settings': {
            'index': {
                'number_of_shards': 4
            }
        }
    }
    try:
        response = client.indices.create(index_name, body=index_body)
        print(response)
    except Exception as e:
        if e.error == 'resource_already_exists_exception':
            print(f"Index {index_name} already exists")
        else:
            print(f"Error creating index: {e}")


# Function to read log file and ingest into OpenSearch

def ingest_file(file_path: str, index: str, parser: Callable, bulk_size: int = 1000):
    # TODO : find an optimization for bulk_size
    actions = []

    with open(file_path, 'r') as file:
        for line in file:
            try:
                parsed_line = parser(line)
                if parsed_line is not None:
                    action = {
                        '_op_type': 'index',
                        '_index': index,
                        '_source': parsed_line
                    }
                    actions.append(action)

                if len(actions) >= bulk_size:
                    # Send bulk request and clear actions list
                    resp = helpers.bulk(client, actions, max_retries=3)
                    actions = []

            except Exception as e:
                print(f"Error processing line: {e}")
                continue

    # Final bulk request for remaining actions
    if actions:
        try:
            resp = helpers.bulk(client, actions, max_retries=3)
        except Exception as e:
            print(f"Error in final bulk request: {e}")


# Example usage
log_file_path = 'data/access.log'  # Replace with your actual log file path
create_index("access-logs")
ingest_file(log_file_path, "access-logs", parse_apache)

log_file_path = 'data/dolibarr_access.log'
create_index("dolibarr-logs")
ingest_file(log_file_path, "dolibarr-logs", parse_apache)

log_file_path = 'data/owncloud.log'  # Replace with your actual log file path
create_index("owncloud-logs")
ingest_file(log_file_path, "owncloud-logs", parse_jsonline)
