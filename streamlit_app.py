"""Root entry point for Streamlit Cloud."""
import sys, os
repo_root = os.path.dirname(os.path.abspath(__file__))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)
exec(open(os.path.join(repo_root, "src", "ui", "app.py")).read())
