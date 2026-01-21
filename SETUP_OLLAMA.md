# Install Ollama (Required for Jarvis)

Your "Jarvis" runs on a local Large Language Model (LLM), which is powered by **Ollama**.
It seems Ollama is not installed on your computer.

## 1. Download Ollama
1.  Go to the official website: [https://ollama.com/download/windows](https://ollama.com/download/windows)
2.  Click **"Download for Windows"**.

## 2. Install
1.  Run the downloaded `OllamaSetup.exe`.
2.  Follow the prompts to install.

## 3. Verify
1.  Open a new terminal (Command Prompt or PowerShell).
2.  Type `ollama` and press Enter. You should see help text.

## 4. Pull the Model
Once installed, you need to download the "brain" (the model).
Run this command in your terminal:
```bash
ollama pull llama3
```

## 5. Run Jarvis
Now you can go back to this project folder and run:
`run_jarvis.bat`
