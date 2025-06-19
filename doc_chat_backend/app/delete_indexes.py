import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import NotFoundError

# Set your Elasticsearch URL
es_url = "http://localhost:9200"

# Create a client
client = Elasticsearch(es_url)

# Index name to delete
index_name = "user_docs_9"

# Delete the index if it exists
try:
    if client.indices.exists(index=index_name):
        client.indices.delete(index=index_name)
        print(f"✅ Index '{index_name}' deleted successfully.")
    else:
        print(f"ℹ️ Index '{index_name}' does not exist.")
except NotFoundError:
    print(f"❌ Index '{index_name}' not found.")
except Exception as e:
    print(f"❌ Error deleting index '{index_name}': {str(e)}")
