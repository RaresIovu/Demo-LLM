from sentence_transformers import SentenceTransformer, util
from functools import lru_cache
import torch
import json
@lru_cache(maxsize=1)
def getModel():
    return SentenceTransformer('all-MiniLM-L6-v2')

def get_embedding(text):
    embedding = getModel().encode(text, convert_to_tensor=True)
    return embedding.tolist()

def get_top_category_ids(product_name, categories, top_k=3):
    if not categories:
        return []

    category_embeddings = [json.loads(c['embedding']) for c in categories]
    
    query_embedding = getModel().encode(product_name, convert_to_tensor=True)
    cat_embeddings_tensor = torch.tensor(category_embeddings)
    
    hits = util.semantic_search(query_embedding, cat_embeddings_tensor, top_k=top_k)
    
    top_ids = [categories[hit['corpus_id']]['id'] for hit in hits[0] if hit["score"] > 0.35]
    return top_ids
