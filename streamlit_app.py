"""Streamlit Cloud entry point — adds repo root to sys.path then runs UI."""
import sys, os
r = os.path.dirname(os.path.abspath(__file__))
if r not in sys.path:
    sys.path.insert(0, r)
exec(open(os.path.join(r, "src", "ui", "app.py")).read())
