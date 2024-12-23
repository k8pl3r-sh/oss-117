from opensearchpy import OpenSearch

host = '192.168.7.41'
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
"""

##### Create an index
index_name = 'python-test-index'
index_body = {
  'settings': {
    'index': {
      'number_of_shards': 4
    }
  }
}

response = client.indices.create(index_name, body=index_body)
print(response)

##### Create a document
document = {
  'source': 'app-test',
  'level': 'INFO',
  'event_id': '4624'
}

response = client.index(
    index = 'python-test-index',
    body = document,
    id = '1',
    refresh = True
)
print(response)
"""

##### Bulk operations
# Multiple operations at once
# movies = '{ "index" : { "_index" : "my-dsl-index", "_id" : "2" } } \n { "title" : "Interstellar", "director" : "Christopher Nolan", "year" : "2014"} \n { "create" : { "_index" : "my-dsl-index", "_id" : "3" } } \n { "title" : "Star Trek Beyond", "director" : "Justin Lin", "year" : "2015"} \n { "update" : {"_id" : "3", "_index" : "my-dsl-index" } } \n { "doc" : {"year" : "2016"} }'
# client.bulk(movies)

