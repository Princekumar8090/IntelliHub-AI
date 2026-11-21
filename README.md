# IntelliHub AI

IntelliHub AI is a Streamlit-based personal AI assistant powered by a locally running Ollama model.

## Included features

- AI question answering with Ollama
- Career guidance, resume and interview preparation
- Placement practice and study planning
- Local document upload and retrieval (TXT, Markdown, PDF, DOCX)
- SQLite-backed local answer history and planner data
- Charts and application tracking

## Run locally

1. Install [Python](https://www.python.org/) and [Ollama](https://ollama.com/).
2. Download the model:

   ```bash
   ollama pull llama3.2:3b
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Copy `.env.example` to `.env` if you want to customize the Ollama model or URL.
5. Start the app:

   ```bash
   streamlit run app.py
   ```

Open http://localhost:8501.

## Important deployment note

This version uses Ollama at `http://localhost:11434`. That address points to the computer running the app. A cloud host such as Streamlit Community Cloud cannot access Ollama running on your personal computer. To make the app publicly usable, deploy Ollama on a secured, reachable server or adapt the app to a hosted model endpoint.

## Source archive

The complete source package is available as `IntelliHub-AI-source.zip` in this repository. The archive excludes the local SQLite database so personal history is not published.

## Configuration

See `.env.example` for the optional `OLLAMA_MODEL` and `OLLAMA_BASE_URL` settings. Never commit your real `.env` file, API keys, private documents, or local database.
