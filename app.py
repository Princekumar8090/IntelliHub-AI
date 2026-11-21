"""Streamlit entry point for IntelliHub AI.

The full app source is packaged in IntelliHub-AI-source.zip.
This small launcher loads it so Streamlit Cloud can use app.py at the repo root.
"""
from pathlib import Path
import os
import zipfile

import streamlit as st

ROOT = Path(__file__).resolve().parent
ARCHIVE = ROOT / "IntelliHub-AI-source.zip"

# Streamlit Community Cloud stores configuration in st.secrets.
# Forward optional Ollama settings to the existing app's environment config.
try:
    for key in ("OLLAMA_BASE_URL", "OLLAMA_MODEL"):
        value = st.secrets.get(key)
        if value:
            os.environ[key] = str(value)
except Exception:
    pass

if not ARCHIVE.exists():
    st.error("The IntelliHub-AI-source.zip file is missing from the repository.")
    st.stop()

try:
    with zipfile.ZipFile(ARCHIVE) as package:
        app_name = next(
            (name for name in package.namelist()
             if name == "app.py" or name.endswith("/app.py")),
            None,
        )
        if app_name is None:
            st.error("Could not find app.py inside IntelliHub-AI-source.zip.")
            st.stop()
        source = package.read(app_name).decode("utf-8")
except (zipfile.BadZipFile, UnicodeDecodeError, OSError) as exc:
    st.error(f"Could not load the packaged IntelliHub AI source: {exc}")
    st.stop()

# Run the original application in this module so its ROOT points to the repo.
exec(compile(source, str(ROOT / "app.py"), "exec"), globals())
