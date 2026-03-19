"""
Root-level entry point for Streamlit Cloud.

Streamlit Cloud serves the file specified in the app settings
(typically the repo root). This file patches sys.path so that
`from src.ephemeris import ...` resolves correctly, then runs
the real UI from src/ui/app.py.

Local dev: use `streamlit run src/ui/app.py` directly.
Streamlit Cloud: point deployment to this file (streamlit_app.py).
"""

import sys
import os

# Ensure repo root is on the path so `src.*` imports resolve
repo_root = os.path.dirname(os.path.abspath(__file__))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

# Run the real app
exec(open(os.path.join(repo_root, "src", "ui", "app.py")).read())
