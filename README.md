# IntelliHub AI

IntelliHub AI is a Streamlit-based assistant for study help, career guidance, placement preparation, document Q&A, task planning, and application tracking. It uses a local Ollama model by default.

## Run locally on Windows

1. Install [Ollama](https://ollama.com/) and start it.
2. In PowerShell, download the default model:

   ```powershell
   ollama pull llama3.2:3b
   ```

3. Clone this repository and open its folder in VS Code.
4. Create and activate a virtual environment (recommended):

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

When Ollama is running on your computer, the app uses the local `llama3.2:3b` model and generates real answers.

## Public demo on Streamlit Community Cloud

- Select this repository, branch `main`, and main file `app.py`.
- The launcher loads the application source from `IntelliHub-AI-source.zip`.
- If Ollama is not reachable from the cloud app, the interface switches to **Public demo mode** and displays clearly labelled sample responses instead of a localhost connection error.
- Public demo responses are prepared examples, not AI-generated answers. The public demo does not send visitor questions to an external AI service.
- The public demo is intended to let visitors explore the interface and workflow. Live AI generation requires a running Ollama server.

**Why the error happens:** `localhost:11434` on Streamlit Cloud refers to the cloud container, not your Windows computer. Your computer's Ollama service is therefore not reachable by the deployed app.

### Optional: connect a hosted Ollama server

You may configure `OLLAMA_BASE_URL` and `OLLAMA_MODEL` under **App settings → Secrets** only when you have a securely hosted Ollama endpoint reachable from Streamlit Cloud. Do not expose your personal computer's Ollama port directly to the public internet.

The deployed app's local SQLite database and uploaded files may be temporary. Use managed persistent storage for production multi-user data.

## Configuration

Optional local `.env`:

```env
OLLAMA_MODEL=llama3.2:3b
OLLAMA_BASE_URL=http://localhost:11434
```

Never commit `.env`, API keys, passwords, database files, or private documents.
