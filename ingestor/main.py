import re
import json
from datetime import datetime
from opensearchpy import OpenSearch
from apache_parser import parse_apache
from typing import Callable

# Initialize the OpenSearch client
host = '192.168.146.41'
port = 9200
auth = ('admin', 'eLej1Zvctg#')


# Create the client with SSL/TLS and hostname verification disabled.
client = OpenSearch(
    hosts = [{'host': host, 'port': port}],
    http_compress = True, # enables gzip compression for request bodies
    http_auth = auth,
    use_ssl = True,
    verify_certs = False,
    ssl_assert_hostname = False,
    ssl_show_warn = False
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
        print(f"Error creating index: {e}")
# Function to read log file and ingest into OpenSearch
def ingest_logs(file_path: str, index: str, parser: Callable):
    with open(file_path, 'r') as file:
        for line in file:

            # Index the log into OpenSearch
            response = client.index(
                index=index,
                body=parse_apache(line),
                id=None  # Auto-generate ID
            )
            print(response)



# Example usage
log_file_path = 'data/apache_logs'  # Replace with your actual log file path
create_index("apache-logs")
ingest_logs(log_file_path, "apache-logs", parse_apache)
