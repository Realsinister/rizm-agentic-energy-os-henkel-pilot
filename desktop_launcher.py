import os
import sys
import webbrowser
import time
import threading

def resolve_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def open_browser():
    time.sleep(1.5)
    webbrowser.open("http://localhost:8501")

if __name__ == '__main__':
    print("=" * 65)
    print("  ⚡ Sample Energy OS — Henkel Düsseldorf Industrial Energy OS ⚡  ")
    print("=" * 65)
    print("Launching embedded Web Application server on http://localhost:8501...")
    
    # Set sys.path so src module can be imported
    base_dir = resolve_path(".")
    if base_dir not in sys.path:
        sys.path.insert(0, base_dir)
        
    src_dir = resolve_path("src")
    if src_dir not in sys.path:
        sys.path.insert(0, src_dir)

    app_path = resolve_path(os.path.join("src", "app.py"))
    
    # Thread to open browser automatically
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
