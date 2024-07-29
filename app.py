from flask import Flask, request, jsonify
import logging
from flask_cors import CORS  # Import CORS
import os
import subprocess
from clear_all import clear_mongo, clear_elasticsearch

app = Flask(__name__)
CORS(app)  # Add this line to enable CORS

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    file_path = os.path.join('/tmp', file.filename)
    file.save(file_path)

    # Run the load_data.py script with the uploaded file
    subprocess.run(['python3', 'load_data.py', file_path], check=True)
    return jsonify({"message": "File uploaded and data loaded successfully"}), 200

@app.route('/clear', methods=['POST'])
def clear():
    try:
        clear_mongo()
        clear_elasticsearch()
        return jsonify({"message": "All data cleared successfully"}), 200
    except Exception as e:
        return jsonify({"message": f"Error clearing data: {e}"}), 500

@app.route('/query', methods=['POST'])
def query():
    try:
        data = request.json
        query_text = data.get('query')
        if not query_text:
            return jsonify({"error": "Query text is required"}), 400
        
        responses = rag.retrieve_and_classify(query_text)
        return jsonify(responses), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    
if __name__ == '__main__':
    from rag_framework import RAGFramework
    rag = RAGFramework(model_path='./fine_tuned_model')
    app.run(debug=True)
