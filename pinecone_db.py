import os
import time
from pinecone import Pinecone, ServerlessSpec
from langchain_community.embeddings import HuggingFaceEmbeddings

class PineconeDB:
    def __init__(self, api_key, index_name="jarvis-index"):
        if not api_key:
            raise ValueError("Pinecone API Key is required")
        
        self.pc = Pinecone(api_key=api_key)
        self.index_name = index_name
        
        # Initialize embeddings (runs locally, no API key needed)
        # Using a small, fast model
        try:
            self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        except Exception as e:
            print(f"Error loading embeddings: {e}")
            raise
        
        # Check if index exists, if not create it
        existing_indexes = [index.name for index in self.pc.list_indexes()]
        if self.index_name not in existing_indexes:
            print(f"Creating index: {self.index_name}")
            try:
                self.pc.create_index(
                    name=self.index_name,
                    dimension=384, # Dimensions for all-MiniLM-L6-v2
                    metric="cosine",
                    spec=ServerlessSpec(
                        cloud="aws",
                        region="us-east-1"
                    )
                )
                # Wait for index to be initialized
                while not self.pc.describe_index(self.index_name).status['ready']:
                    time.sleep(1)
            except Exception as e:
                print(f"Error creating index: {e}")
                # Fallback or re-raise depending on strictness
                raise

        self.index = self.pc.Index(self.index_name)

    def add_texts(self, texts):
        """
        Embeds and adds text chunks to the Pinecone index.
        """
        if not texts:
            return
            
        print(f"Embedding {len(texts)} texts...")
        # Create embeddings
        vectors = []
        for i, text in enumerate(texts):
            clean_text = text.strip()
            if clean_text:
                embedding = self.embeddings.embed_query(clean_text)
                # ID can be just a simple hash or timestamp + index
                id = f"{str(hash(clean_text))}-{i}" 
                vectors.append({
                    "id": id,
                    "values": embedding,
                    "metadata": {"text": clean_text}
                })
        
        # Upsert in batches
        if vectors:
            batch_size = 100
            for i in range(0, len(vectors), batch_size):
                batch = vectors[i:i+batch_size]
                self.index.upsert(vectors=batch)
            print(f"Added {len(vectors)} vectors to index.")

    def query(self, query_text, top_k=3):
        """
        Queries the index for similar text.
        """
        if not query_text:
            return []

        query_embedding = self.embeddings.embed_query(query_text)
        
        results = self.index.query(
            vector=query_embedding,
            top_k=top_k,
            include_metadata=True
        )
        
        matches = [match['metadata']['text'] for match in results['matches'] if 'metadata' in match and 'text' in match['metadata']]
        return matches
