from pinecone_db import retrieve_memory
from llm import call_llm

def jarvis_answer(user_query):
    memories = retrieve_memory(user_query)
    context = "\n".join(memories)

    prompt = f"""
You are Jarvis, an intelligent personal AI assistant.

Context:
{context}

User Question:
{user_query}

Respond clearly and professionally.
"""

    return call_llm(prompt)
