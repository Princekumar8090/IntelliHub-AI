"""Streamlit entry point for IntelliHub AI with a safe public demo fallback."""
from pathlib import Path
import os
import zipfile

import streamlit as st

ROOT = Path(__file__).resolve().parent
ARCHIVE = ROOT / "IntelliHub-AI-source.zip"

# Optional remote Ollama settings can be supplied in Streamlit Cloud Secrets.
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
            (name for name in package.namelist() if name == "app.py" or name.endswith("/app.py")),
            None,
        )
        if app_name is None:
            st.error("Could not find app.py inside IntelliHub-AI-source.zip.")
            st.stop()
        source = package.read(app_name).decode("utf-8")
except (zipfile.BadZipFile, UnicodeDecodeError, OSError) as exc:
    st.error(f"Could not load the packaged IntelliHub AI source: {exc}")
    st.stop()

# Rename the original model function, then add a transparent fallback for public hosting.
if "def answer_with_ollama(" not in source or "\ndef local_doc_context(" not in source:
    st.error("The packaged app source has an unexpected layout. Please check the source archive.")
    st.stop()
source = source.replace("def answer_with_ollama(", "def _answer_with_ollama(", 1)

public_demo_patch = r'''

def public_demo_answer(question, section="General AI", context=""):
    """Prepared sample content for public hosting when no Ollama server is reachable."""
    header = (
        "## Public demo preview\n\n"
        "This is a **sample response**, not an AI-generated answer. This public preview is not connected "
        "to an Ollama model, and your question is not sent to an external AI service.\n\n"
        f"**Workspace:** {section}\n\n"
        "For live AI answers, run IntelliHub AI on your computer with Ollama and model llama3.2:3b.\n\n"
    )
    if section == "Ask AI":
        sample = (
            "### Example: preparing for an AI/ML internship\n"
            "1. Strengthen Python, SQL, statistics, and core machine-learning concepts.\n"
            "2. Build two end-to-end projects and document them clearly on GitHub.\n"
            "3. Practice data structures, model evaluation, and project-based interview questions.\n"
            "4. Tailor your resume and apply through official company career pages.\n\n"
            "**Demo limitation:** This prepared example has not analysed your question or private documents."
        )
    elif section in {"Career roadmap", "Resume & interview", "Placement practice"}:
        sample = (
            "### Example career preparation plan\n"
            "- **Weeks 1–2:** Revise Python, SQL, statistics, and data structures.\n"
            "- **Weeks 3–5:** Practice data cleaning, EDA, and supervised machine learning.\n"
            "- **Weeks 6–8:** Complete an ML project with evaluation and documentation.\n"
            "- **Weeks 9–10:** Prepare your resume and explain each project clearly.\n"
            "- **Weeks 11–12:** Practice interviews and apply to relevant roles.\n\n"
            "This is a general example, not a personalized assessment."
        )
    elif section == "Jobs":
        sample = (
            "### Job-search demo\n"
            "This preview cannot check live vacancies, eligibility, deadlines, or application status.\n\n"
            "1. Search for the role on official company career pages.\n"
            "2. Confirm location, eligibility, skills, and closing date on the listing.\n"
            "3. Save the official application URL in the Application Tracker.\n\n"
            "Do not treat this demo as a list of verified current openings."
        )
    elif section in {"Courses", "Company research"}:
        sample = (
            "### Research demo\n"
            "This preview cannot verify current course fees, company hiring details, internship eligibility, "
            "or live openings. Use the provider's or company's official website as the source of truth.\n\n"
            "Check the latest syllabus, prerequisites, fees, role requirements, location, and application dates."
        )
    elif section == "Study planner":
        sample = (
            "### Example daily study plan\n"
            "| Session | Activity |\n|---|---|\n"
            "| 1 | Learn one concept (60 minutes) |\n"
            "| 2 | Solve practice problems (60 minutes) |\n"
            "| 3 | Revise notes and track mistakes (30 minutes) |\n\n"
            "Adjust this example to your actual exam date and available study time."
        )
    else:
        sample = (
            "### IntelliHub AI preview\n"
            "Explore the dashboard, document-library interface, task planner, analytics, and application tracker. "
            "AI-generated answers require a running Ollama model."
        )
    return header + sample


def answer_with_ollama(question, section="General AI", use_web=False, context=""):
    """Use Ollama when reachable; otherwise return clearly labelled public-demo content."""
    available, _ = ollama_status()
    if not available:
        return public_demo_answer(question, section, context), [], "Public demo mode"
    return _answer_with_ollama(question, section, use_web, context)


def current_ai_mode():
    return "Ollama (local)" if ollama_status()[0] else "Public demo mode"
'''
source = source.replace("\ndef local_doc_context(", public_demo_patch + "\ndef local_doc_context(", 1)

# Update labels so visitors understand which mode is running.
replacements = {
    'st.caption("Local Ollama-powered study, career & company assistant")': 'st.caption("AI study, career & company assistant")',
    'st.caption("Ollama: " + ("Connected" if ollama_ok else "Not running"))': 'st.caption("AI mode: " + ("Ollama connected" if ollama_ok else "Public demo preview"))',
    'st.caption("Model: " + os.getenv("OLLAMA_MODEL", "llama3.2:3b"))': 'st.caption("Model: " + (os.getenv("OLLAMA_MODEL", "llama3.2:3b") if ollama_ok else "Sample responses (no model)"))',
    'st.caption("IntelliHub AI · Local prototype")': 'st.caption("IntelliHub AI · Portfolio demo")',
    'col3.metric("Model", os.getenv("OLLAMA_MODEL", "llama3.2:3b"))': 'col3.metric("AI mode", os.getenv("OLLAMA_MODEL", "llama3.2:3b") if ollama_ok else "Demo")',
    'with st.spinner("Asking local Ollama...")': 'with st.spinner("Generating answer..." if ollama_ok else "Loading public demo response...")',
    'mode = "Ollama (local)"': 'mode = model if model == "Public demo mode" else "Ollama (local)"',
    'if context:\n                    mode += " + local documents"': 'if context and model != "Public demo mode":\n                    mode += " + local documents"',
    'answer, citations, model = answer_with_ollama(question.strip(), "Ask AI", False, context)': 'answer, citations, model = answer_with_ollama(question.strip(), "Ask AI", False, context)\n                if model == "Public demo mode":\n                    doc_names = []',
    'save_history("Career roadmap", q, a, "Ollama (local)")': 'save_history("Career roadmap", q, a, current_ai_mode())',
    'save_history("Resume & interview", q, a, "Ollama (local)")': 'save_history("Resume & interview", q, a, current_ai_mode())',
    'save_history("Placement practice", q, a, "Ollama (local)")': 'save_history("Placement practice", q, a, current_ai_mode())',
    'save_history("Jobs", q, a, "Ollama (local; no live web)")': 'save_history("Jobs", q, a, current_ai_mode() + "; no live web")',
    'save_history("Courses", q, a, "Ollama (local; no live web)")': 'save_history("Courses", q, a, current_ai_mode() + "; no live web")',
    'save_history("Company research", q, a, "Ollama (local; no live web)")': 'save_history("Company research", q, a, current_ai_mode() + "; no live web")',
    'save_history("Study planner", q, a, "Ollama (local)")': 'save_history("Study planner", q, a, current_ai_mode())',
}
for old, new in replacements.items():
    source = source.replace(old, new)

banner = '\nif not ollama_ok:\n    st.info("🌐 **Public demo mode:** The online interface is available, but no Ollama model is attached to this cloud app. Buttons show labelled sample content. Run IntelliHub AI locally with Ollama for real AI-generated answers.")\n'
source = source.replace("\n# ----------------------- Ask AI -----------------------", banner + "\n# ----------------------- Ask AI -----------------------", 1)
source = source.replace('with st.spinner("Building roadmap..."):', 'with st.spinner("Preparing response..."):')
source = source.replace('with st.spinner("Searching current openings..."):', 'with st.spinner("Preparing job-search guidance..."):')
source = source.replace('with st.spinner("Searching courses..."):', 'with st.spinner("Preparing course guidance..."):')
source = source.replace('with st.spinner("Researching..."):', 'with st.spinner("Preparing company-research guidance..."):')
source = source.replace('with st.spinner("Planning..."):', 'with st.spinner("Preparing study-plan example..."):')

settings_marker = '    st.markdown("**Important limitations**")'
settings_patch = (
    '    st.markdown("**Public deployment behavior**")\n'
    '    st.write("- Streamlit Community Cloud runs on a separate server and cannot access Ollama at localhost on your personal computer.")\n'
    '    st.write("- When Ollama is unavailable, this portfolio preview displays labelled sample responses instead of connection errors.")\n'
    '    st.write("- For live AI responses, run the app locally with Ollama or configure a securely hosted Ollama endpoint.")\n'
)
source = source.replace(settings_marker, settings_patch + settings_marker, 1)

# Run the original application with the public-demo fallback injected.
exec(compile(source, str(ROOT / "packaged_app.py"), "exec"), globals())
