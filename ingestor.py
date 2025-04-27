from opensearchpy import OpenSearch, Object
from typing import Callable, Dict
from opensearchpy import helpers
from utils.log import Log

from yaml import safe_load
import importlib.util
import os
import requests
import json
import inspect


class OsIngestor:
    def __init__(self):
        self.config = self.load_config()
        self.log = Log("OS_INGESTOR", self.config)
        self.parsers = self.dynamic_load_parsers(self.config['parsers']['directory'])
        self.auth = (self.config['opensearch']['auth'].split(':')[0], self.config['opensearch']['auth'].split(':')[1])
        print(f"Loaded parsers: {self.parsers}")
        # Create the client with SSL/TLS and hostname verification disabled.
        self.client = OpenSearch(
            hosts=[{'host': self.config['opensearch']['host'], 'port': self.config['opensearch']['port']}],
            http_compress=True,  # enables gzip compression for request bodies
            http_auth=self.auth,
            use_ssl=True,
            verify_certs=False,
            ssl_assert_hostname=False,
            ssl_show_warn=False
        )

    def reload_dynamic_parsers(self):
        parsers_callable_dict = self.dynamic_load_parsers(self.config['parsers']['directory'])
        parsers_callable = {k: v for k, v in parsers_callable_dict.items() if not k.endswith("entry")}
        parsers = list(parsers_callable.keys())
        return parsers # TODO : check qu'on peut les call directement

    def dynamic_load_parsers(self, directory: str) -> Dict[str, Object]:
        instances = {}

        # Traverse the specified directory
        for filename in os.listdir(directory):
            if filename.endswith(".py") and filename != "log.py" and filename != "abstract_parser.py":
                module_name = filename[:-3]  # Remove the '.py' extension
                module_path = os.path.join(directory, filename)

                # Dynamically load the module
                spec = importlib.util.spec_from_file_location(module_name, module_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                # Filter and load only the classes defined in the current module
                for attr_name in dir(module):
                    attr = getattr(module, attr_name)

                    # Ensure it's a class defined in the current module, not an imported class
                    if isinstance(attr, type) and attr.__module__ == module.__name__:
                        # Check the init signature for required arguments
                        init_params = inspect.signature(attr.__init__).parameters
                        required_params = [
                            param for param, details in init_params.items()
                            if details.default == inspect.Parameter.empty and param != 'self'
                        ]

                        # Pass the required arguments to the class
                        if 'config' in required_params:
                            required_params.remove('config')
                            instance_args = [self.config]  # Add the config as the first argument
                        else:
                            instance_args = []

                        # Instantiate the class with the required arguments
                        try:
                            instance = attr(*instance_args)
                            instances[f"{attr_name}"] = instance
                        except TypeError as e:
                            self.log.info(f"Skipping {attr_name} - error instantiating class: {str(e)}")
                            continue  # Skip this class if instantiation fails

                        """
                        # Load methods of the class
                        for method_name in dir(instance):
                            method = getattr(instance, method_name)
                            if callable(method) and not method_name.startswith("__"):
                                functions[f"{attr_name}.{method_name}"] = method
                        """

        return instances

    def load_config(self):
        with open('config.yml', 'r') as file:
            config = safe_load(file)
        return config

    def get_fields(self, idx_name: str) -> dict:
        self.log.info(f"Getting fields for index {idx_name}")
        url = self.config["opensearch"]["domain"] + 'api/index_patterns/_fields_for_wildcard'
        headers = {
            'Content-Type': 'application/json',
            'osd-xsrf': 'osd-fetch',
            'securitytenant': 'global'
        }
        params = {
            'pattern': idx_name,
            'meta_fields': ['_source', '_id', '_type', '_index', '_score']
        }
        try:
            response = requests.get(url, headers=headers, params=params, auth=self.auth)
            if response.status_code == 200 or response.status_code == 201:
                response = response.json() 
                return response
            else:
                self.log.error(f"Request failed with status code {response.status_code}")
                self.log.error(response.text)
        except Exception as e:
            self.log.error(f"Error in request: {e}")
        
    def create_index_pattern(self, idx_name: str, timefield: str, parser: Callable):
        self.log.info(f"Creating index {idx_name} for {parser}")
        # parser_class = self.parsers.get(parser)

        #if parser_class:
        # Instantiate the parser class with the required arguments
        #if hasattr(parser_class, 'get_index_pattern'):
        #parser_instance = parser(idx_name)  # Pass file_path if required

        # Dynamically get the method
        #method = getattr(parser_instance, 'get_index_pattern', None)

        #if method:
        # Call the method dynamically
        fields = self.get_fields(idx_name)["fields"]
        
        data = {
            "attributes": {
                "title": idx_name,
                "timeFieldName": timefield,
                "fields": json.dumps(fields)
            },
            "references": []
        }

        self.log.info(f"Data: {data}")  
        # Proceed with the API call
        url = self.config["opensearch"]["domain"] + '/api/saved_objects/index-pattern'
        headers = {
            'Content-Type': 'application/json',
            'osd-xsrf': 'osd-fetch',
            'securitytenant': 'global'
        }
        try:
            response = requests.post(url, headers=headers, auth=self.auth, json=data)
            if response.status_code == 200 or response.status_code == 201:
                self.log.info(f"Index pattern created {response.status_code}, {response}")
                return True
            else:
                self.log.info(f"Index pattern failed")
                return False
        except Exception as e:
            self.log.error(e)
            return False
        #else:
        #    print(f"Method 'get_index_pattern' not found in {parser}")
        #    return False
        #else:
        #    self.log.error(f"Parser class '{parser_class}' does not have 'get_index_pattern' method")
        #S    return False
        #else:
        #    self.log.error(f"Parser class not found for log type: {parser}")
        #    return False

    def create_index(self, index_name: str):
        index_name.lower()
        index_body = {
            'settings': {
                'index': {
                    'number_of_shards': 4
                }
            }
        }
        try:
            response = self.client.indices.create(index_name, body=index_body)
            print(response)
        except Exception as e:
            self.log.error(f"Error creating index: {e}")
            """
            if e.error == 'resource_already_exists_exception':
                print(f"Index {index_name} already exists")
            else:
                print(f"Error creating index: {e}")
            """


    def ingest_file(self, file_path: str, index: str, parser: Callable, bulk_size: int = 1000):
        # TODO : find an optimization for bulk_size
        actions = []
        self.log.info(f"Ingesting file")

        log_lines = parser.file_parser(file_path) # NOT dynamic
        for parsed_line in log_lines:
            if parsed_line is not None:
                action = {
                    '_op_type': 'index',
                    '_index': index,
                    '_source': parsed_line
                }
                actions.append(action)

            if len(actions) >= bulk_size:
                # Send bulk request and clear actions list
                resp = helpers.bulk(self.client, actions, max_retries=3)
                actions = []


        # Final bulk request for remaining actions
        if actions:
            try:
                resp = helpers.bulk(self.client, actions, max_retries=3)
            except Exception as e:
                self.log.error(f"Error in final bulk request: {e}")


if __name__ == '__main__':
    pass
    # Example usage
    #log_file_path = dir + 'auth.log'  # Replace with your actual log file path
    #create_index("auth-logs")
    #ingest_file(log_file_path, "auth-logs", parsers['parse_syslog'])

    #log_file_path = dir + 'access.log'  # Replace with your actual log file path
    #create_index("access-logs")
    #ingest_file(log_file_path, "access-logs", parsers['parse_apache'])
    #create_index_pattern("access-logs", "time")


    #log_file_path = dir + 'dolibarr_access.log'
    #create_index("dolibarr-logs")
    #ingest_file(log_file_path, "dolibarr-logs", parsers['parse_apache'])

    #log_file_path = dir + 'owncloud.log'  # Replace with your actual log file path
    #create_index("owncloud-logs")
    #ingest_file(log_file_path, "owncloud-logs", parsers['parse_jsonline'])

    #log_file_path = dir + 'daemon.log'  # Replace with your actual log file path
    #create_index("daemon-logs")
    #ingest_file(log_file_path, "daemon-logs", parsers['parse_syslog'])

    #log_file_path = dir + 'docker.log'  # Replace with your actual log file path
    #create_index("docker-logs")
    #ingest_file(log_file_path, "docker-logs", parsers['parse_docker'])
