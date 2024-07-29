import re
from transformers import AutoModel, AutoTokenizer
from elasticsearch import Elasticsearch
import torch
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

class RAGFramework:
    def __init__(self, model_path, es_host='localhost', es_port=9200):
        self.model = AutoModel.from_pretrained(model_path)
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.es = Elasticsearch([{'host': es_host, 'port': es_port, 'scheme': 'http'}])
    
    def retrieve_candidates(self, job_description, index_name='candidates'):
        logging.debug(f"Querying Elasticsearch with job description: {job_description}")
        
        response = self.es.search(
            index=index_name,
            body={
                "query": {
                    "multi_match": {
                        "query": job_description,
                        "fields": ["Job Skills^2", "Name", "Experience", "Projects", "Comments"]
                    }
                }
            }
        )
        
        logging.debug(f"Elasticsearch response: {response}")
        
        hits = response['hits']['hits']
        logging.debug(f"Elasticsearch hits: {hits}")
        
        candidates = [hit['_source'] for hit in hits]
        logging.debug(f"Retrieved candidates: {candidates}")
        return candidates
    
    def embed_text(self, text):
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True)
        with torch.no_grad():
            outputs = self.model(**inputs)
        embeddings = outputs.last_hidden_state.mean(dim=1)
        return embeddings
    
    def compute_similarity(self, emb1, emb2):
        return torch.nn.functional.cosine_similarity(emb1, emb2)
    
    def extract_top_k(self, query_text):
        # Extract number of top candidates from the query
        match = re.search(r'top (\d+)', query_text, re.IGNORECASE)
        if match:
            return int(match.group(1))
        return 5  # Default value if not specified
    def retrieve_and_classify(self, query_text):
        logging.debug(f"Received query: {query_text}")
        
        # Step 1: Extract the number of top candidates
        top_k = self.extract_top_k(query_text)
        logging.debug(f"Top k candidates: {top_k}")
        
        # Step 2: Retrieve relevant candidates from Elasticsearch based on the input query
        candidates = self.retrieve_candidates(query_text)
        logging.debug(f"Candidates retrieved: {candidates}")
        
        if not candidates:
            return ["No candidates found matching the query."]
        
        # Step 3: Embed the query text
        query_embedding = self.embed_text(query_text)
        
        # Step 4: Embed each candidate and compute similarity
        candidate_similarities = []
        for candidate in candidates:
            # Include all relevant candidate information
            candidate_info = (
                f"Name: {candidate['Name']}, "
                f"Email: {candidate.get('Contact Details', 'N/A')}, "
                f"Location: {candidate.get('Location', 'N/A')}, "
                f"Skills: {candidate.get('Job Skills', 'N/A')}, "
                f"Experience: {candidate.get('Experience', 'N/A')}, "
                f"Projects: {candidate.get('Projects', 'N/A')}, "
                f"Comments: {candidate.get('Comments', 'N/A')}"
            )
            candidate_embedding = self.embed_text(candidate_info)
            similarity = self.compute_similarity(query_embedding, candidate_embedding)
            candidate_similarities.append((similarity.item(), candidate_info))
        
        # Step 5: Sort candidates by similarity
        candidate_similarities.sort(reverse=True, key=lambda x: x[0])
        
        # Step 6: Get the top K candidates
        top_candidates = candidate_similarities[:top_k]
        
        # Step 7: Prepare the response
        responses = [
            {
                "Candidate Info": candidate_info,
                "Similarity Score": similarity
            }
            for similarity, candidate_info in top_candidates
        ]
        logging.debug(f"Top candidates: {responses}")
        
        return responses
