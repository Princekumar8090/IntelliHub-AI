# IntelliHub AI

IntelliHub AI is a Streamlit-based assistant for study help, career guidance, placement preparation, document Q&A, task planning, and application tracking. The project uses a local Ollama model by default.

## Run locally on Windows

1. Install [Ollama](https://ollama.com/) and start it.
2. In PowerShell, download the default model:

   ```powershell
   ollama pull llama3.2:3b
   ```

3. Clone this repository and open its folder in VS Code.
4. Create and activate a virtual environment (optional but recommended):

   ```powershell
   python -m venv .venv
   .venv\Scripts\activate
   ```

5. Install packages and run:

   ```powershell
   pip install -r requirements.txt
   streamlit run app.py
   ```

6. Open http://localhost:8501.

## Deploy on Streamlit Community Cloud

- Choose this repository, branch `main`, and main file `app.py`.
- The launcher loads the original app source from `IntelliHub-AI-source.zip`.
- Add `OLLAMA_BASE_URL` and `OLLAMA_MODEL` under **App settings → Secrets** only if you have an Ollama server reachable from the public cloud app.

**Important:** `http://localhost:11434` on Streamlit Cloud refers to the cloud container, not your personal computer. Therefore, the default local Ollama model will not be reachable from a deployed app. To make AI answers work online, you must provide a securely hosted, network-accessible Ollama endpoint. Do not expose your personal computer's Ollama port directly to the internet. The deployed app's local SQLite and uploaded files may also be temporary; use managed persistent storage for production data.

## Configuration

Local optional `.env`:

```env
OLLAMA_MODEL=llama3.2:3b
OLLAMA_BASE_URL=http://localhost:11434
```

Never commit `.env`, API keys, passwords, database files, or private documents.
