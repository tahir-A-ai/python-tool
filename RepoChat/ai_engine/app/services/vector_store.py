import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List, Dict
import os

class VectorStore:
    """
    Manages the Vector Database (FAISS) and Embedding Model.
    """
    
    def __init__(self, index_path="faiss_index.bin", metadata_path="metadata.pkl"):
        self.index_path = index_path
        self.metadata_path = metadata_path
        
        # Load a free, local, lightweight model
        print("Loading embedding model (this may take a moment)...")
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Dimension of this model is 384
        self.dimension = 384
        # Check if index exists on disk before creating a new one
        if os.path.exists(self.index_path) and os.path.exists(self.metadata_path):
            print(f"Loading existing Vector Store from {self.index_path}...")
            self.index = faiss.read_index(self.index_path)
            
            with open(self.metadata_path, "rb") as f:
                self.metadata = pickle.load(f)
        else:
            print("Creating NEW Vector Store...")
            self.index = faiss.IndexFlatL2(self.dimension)
            self.metadata = []

    def add_documents(self, documents: List[Dict]):
        """
        Embeds code chunks and saves them to FAISS.
        """
        if not documents:
            return

        texts = [doc['text'] for doc in documents]
        
        # Generate Embeddings (Locally!)
        embeddings = self.model.encode(texts)
        
        # Convert to numpy array for FAISS
        embeddings_np = np.array(embeddings).astype('float32')
        
        # Add to Index
        self.index.add(embeddings_np)
        
        # Store Metadata (Map Index ID to Document Data)
        # We append new metadata to our list
        self.metadata.extend(documents)
        
        print(f"Added {len(documents)} documents to the Vector Store.")
        
        # 5. Save to Disk
        self._save_local()

    def search(self, query: str, repo_id: int = None, k: int = 3):
        """
        Finds the top K relevant code chunks for a query.
        """
        # Embed the query
        query_vector = self.model.encode([query])
        query_np = np.array(query_vector).astype('float32')
        
        search_k = k * 10
        # Search FAISS
        distances, indices = self.index.search(query_np, search_k)
        
        results = []
        for i, idx in enumerate(indices[0]):
            if idx != -1 and idx < len(self.metadata):
                item = self.metadata[idx]
                # 🕵️‍♂️ SPY PRINT: What are we comparing?
                stored_id = item['metadata'].get('repo_id')
                print(f"👀 Comparing Stored ID: {stored_id} vs Query ID: {repo_id}")
                if repo_id is not None:
                    if stored_id != repo_id:
                        continue # Skip this result, it's from another repo!
                
                results.append(item)
                # Stop once we have found enough "Valid" results
                if len(results) >= k:
                    break
        return results
    

    def _save_local(self):
        """Saves the index and metadata to disk so we don't lose it on restart."""
        faiss.write_index(self.index, self.index_path)
        with open(self.metadata_path, "wb") as f:
            pickle.dump(self.metadata, f)