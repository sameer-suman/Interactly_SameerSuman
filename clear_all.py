import pymongo
from elasticsearch import Elasticsearch

# MongoDB cleanup
def clear_mongo():
    try:
        # Connect to MongoDB
        client = pymongo.MongoClient('mongodb://localhost:27017/')
        db = client['candidate_db']
        collection = db['candidates']

        # Delete all documents from the collection
        result = collection.delete_many({})
        print(f"Deleted {result.deleted_count} documents from MongoDB!")
    except Exception as e:
        print(f"Error clearing MongoDB: {e}")

# Elasticsearch cleanup
def clear_elasticsearch():
    try:
        # Connect to Elasticsearch
        es = Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme': 'http'}])
        index_name = 'candidates'

        # Check if the index exists
        if es.indices.exists(index=index_name):
            # Delete the index
            es.indices.delete(index=index_name)
            print("All documents have been deleted from Elasticsearch!")
        else:
            print("Elasticsearch index does not exist!")
    except Exception as e:
        print(f"Error clearing Elasticsearch: {e}")

if __name__ == "__main__":
    clear_mongo()
    clear_elasticsearch()
