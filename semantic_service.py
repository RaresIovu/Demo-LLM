from sentence_transformers import SentenceTransformer, util
import torch
import json

# Load the model
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_embedding(text):
    """Generates an embedding for the given text."""
    embedding = model.encode(text, convert_to_tensor=True)
    # Convert tensor to list for storage (though we might store as BLOB if we use pickle/numpy)
    # But for SQLite, storing as JSON or BLOB is fine.
    # The prompt mentions "field(not the junction list, though)"
    # We'll store it as a JSON string for simplicity, or we can use bytes.
    # Let's use JSON for readability in this context if it's not too big, 
    # but the prompt says "all will contain a field", implying it's for embeddings.
    return embedding.tolist()

def get_top_categories(product_name, category_names, category_embeddings, top_k=3):
    """Finds the top_k categories for a product name."""
    if not category_embeddings:
        return []
    
    query_embedding = model.encode(product_name, convert_to_tensor=True)
    cat_embeddings_tensor = torch.tensor(category_embeddings)
    
    hits = util.semantic_search(query_embedding, cat_embeddings_tensor, top_k=top_k)
    
    top_indices = [hit['corpus_id'] for hit in hits[0]]
    return [category_names[i] for i in top_indices]

def get_top_category_ids(product_name, categories, top_k=3):
    """
    Finds the top_k category IDs for a product name.
    categories: list of dicts with 'id', 'name', 'embedding'
    """
    if not categories:
        return []
        
    category_names = [c['name'] for c in categories]
    category_embeddings = [json.loads(c['embedding']) for c in categories]
    
    query_embedding = model.encode(product_name, convert_to_tensor=True)
    cat_embeddings_tensor = torch.tensor(category_embeddings)
    
    hits = util.semantic_search(query_embedding, cat_embeddings_tensor, top_k=top_k)
    
    top_ids = [categories[hit['corpus_id']]['id'] for hit in hits[0]]
    return top_ids
