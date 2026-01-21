# Build Your Own Jarvis

This project is a personal AI assistant powered by a self-hosted Large Language Model (LLM) via Ollama and a vector database (Pinecone) for Retrieval-Augmented Generation (RAG).

## Prerequisites

1.  **Python 3.9+** installed.
2.  **Ollama** installed and running.
    *   Download from [ollama.com](https://ollama.com/).
    *   Pull the Llama 3 model:
        ```bash
        ollama pull llama3
        ```
    *   Ensure Ollama is running in the background (`ollama serve`).
3.  **Pinecone API Key**.
    *   Sign up at [pinecone.io](https://www.pinecone.io/).
    *   Create a standard Serverless index (the code defaults to `us-east-1` AWS by default, but you can adjust `pinecone_db.py` if needed). *Note: The code handles index creation automatically if provided with a valid API key.*

## Installation

1.  Clone this repository or navigate to the project folder:
    ```bash
    cd c:\Users\Asus\OneDrive\Documents\Desktop\deligent
    ```

2.  Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1.  Run the Streamlit application:
    ```bash
    streamlit run app.py
    ```

2.  **Configuration**:
    *   Open the app in your browser (usually http://localhost:8501).
    *   In the sidebar, enter your **Pinecone API Key**.
    *   (Optional) Change the "Ollama Model Name" if you are using a model other than `llama3`.

3.  **Train Jarvis**:
    *   Upload a text file (e.g., a document, notes, or article) in the "Knowledge Base" section.
    *   Click "Learn from File". Jarvis will chunk the text, generate embeddings, and store them in your Pinecone index.

4.  **Chat**:
    *   Type your questions in the main chat interface.
    *   Jarvis will answer based on the context it has learned.

## Project Structure

*   `app.py`: The main Streamlit web application.
*   `rag_agent.py`: Contains the `Jarvis` class that orchestrates the LLM and Database.
*   `pinecone_db.py`: Handles interactions with the Pinecone vector database.
*   `requirements.txt`: List of dependencies.
