import pinecone
from config import PINECONE_API_KEY, PINECONE_ENV, INDEX_NAME
from embeddings import embed_text

pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENV)

if INDEX_NAME not in pinecone.list_indexes():
    pinecone.create_index(
        name=INDEX_NAME,
        dimension=384,
        metric="cosine"
    )

index = pinecone.Index(INDEX_NAME)

def store_memory(id, text):
    index.upsert([(id, embed_text(text), {"text": text})])

def retrieve_memory(query, k=5):
    results = index.query(embed_text(query), top_k=k, include_metadata=True)
    return [m["metadata"]["text"] for m in results["matches"]]
