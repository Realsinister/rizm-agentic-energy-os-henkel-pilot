import os
import sys
import time
import threading
import webbrowser
import importlib.metadata

class DummyDist:
    version = "1.60.0"
    metadata = {"Version": "1.60.0", "Name": "streamlit"}

_orig_version = importlib.metadata.version
_orig_distribution = importlib.metadata.distribution

def _safe_version(distribution_name):
    if distribution_name == "streamlit":
        return "1.60.0"
    try:
        return _orig_version(distribution_name)
    except Exception:
        return "1.0.0"

def _safe_distribution(distribution_name):
    if distribution_name == "streamlit":
        return DummyDist()
    try:
        return _orig_distribution(distribution_name)
    except Exception:
        return DummyDist()

importlib.metadata.version = _safe_version
importlib.metadata.distribution = _safe_distribution

def resolve_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def open_browser():
    time.sleep(2.0)
    try:
        webbrowser.open("http://localhost:8501")
    except Exception:
        pass

if __name__ == '__main__':
    print("=================================================================")
    print("  Sample Energy OS -- Henkel Duesseldorf Industrial Energy OS    ")
    print("=================================================================")
    print("Launching embedded Web Application server on http://localhost:8501...")
    
    base_dir = resolve_path(".")
    if base_dir not in sys.path:
        sys.path.insert(0, base_dir)
        
    src_dir = resolve_path("src")
    if src_dir not in sys.path:
        sys.path.insert(0, src_dir)

    app_path = resolve_path(os.path.join("src", "app.py"))
    
    threading.Thread(target=open_browser, daemon=True).start()

    import streamlit.web.cli as stcli
    
    sys.argv = [
        "streamlit",
        "run",
        app_path,
        "--global.developmentMode=false",
        "--server.headless=false",
        "--server.port=8501"
    ]
    
    sys.exit(stcli.main())
