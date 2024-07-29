import pandas as pd
from pymongo import MongoClient
from elasticsearch import Elasticsearch, helpers
import sys

# Check if file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python3 load_data.py <path_to_excel_file>")
    sys.exit(1)

file_path = sys.argv[1]

# Load the spreadsheet
df = pd.read_excel(file_path)

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['candidate_db']
collection = db['candidates']

# Convert DataFrame to dictionary
data = df.to_dict(orient='records')

# Function to check if a record already exists in MongoDB
def record_exists(record, collection):
    return collection.find_one({"Contact Details": record["Contact Details"]}) is not None

# Filter out records that already exist in MongoDB
new_records = [record for record in data if not record_exists(record, collection)]

if new_records:
    # Insert new records into MongoDB
    inserted_ids = collection.insert_many(new_records).inserted_ids
    print("New data successfully inserted into MongoDB!")
    
    # Fetch the inserted data to include ObjectId
    data_with_ids = list(collection.find({"_id": {"$in": inserted_ids}}))

    # Connect to Elasticsearch
    es = Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme': 'http'}])
    index_name = 'candidates'

    # Define a generator function to create Elasticsearch documents
    def generate_actions(data):
        for record in data:
            # Remove _id field from the source document
            doc_id = str(record.pop('_id'))
            yield {
                "_index": index_name,
                "_id": doc_id,
                "_source": record
            }

    # Index data in Elasticsearch with error logging
    try:
        success, failed = helpers.bulk(es, generate_actions(data_with_ids), stats_only=True)
        print(f"Successfully indexed {success} documents.")
        if failed > 0:
            print(f"Failed to index {failed} documents.")
    except helpers.BulkIndexError as e:
        print(f"Bulk indexing failed with {len(e.errors)} errors:")
        for error in e.errors:
            print(error)
else:
    print("No new data to insert. All records already exist.")
