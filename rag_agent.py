from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from pinecone_db import PineconeDB

class Jarvis:
    def __init__(self, pinecone_api_key, model_name="llama3"):
        self.db = PineconeDB(api_key=pinecone_api_key)
        self.llm = OllamaLLM(model=model_name)
        
        self.prompt = ChatPromptTemplate.from_template("""
        You are Jarvis, a helpful AI assistant.
        
        Context information is below:
        {context}
        
        Question: {question}
        
        Answer the question using the context provided. If the answer is not in the context, 
        use your general knowledge but mention that it's outside your specific knowledge base.
        Keep answers concise and helpful.
        """)

    def learn(self, text_content):
        """
        Ingest text content into the knowledge base (Pinecone).
        """
        # specialized chunking could go here, for now simply splitting by newlines
        chunks = [chunk for chunk in text_content.split('\n') if chunk.strip()]
        self.db.add_texts(chunks)
        return f"Learned {len(chunks)} chunks of information."

    def ask(self, question):
        """
        Ask Jarvis a question. It performs RAG.
        """
        # 1. Retrieve relevant context
        context_list = self.db.query(question)
        context_str = "\n".join(context_list)
        
        # 2. Augment prompt
        chain = self.prompt | self.llm
        
        # 3. Generate response
        response = chain.invoke({"context": context_str, "question": question})
        return response
