"""
Quick-launch: opens the Agentic Swarm frontend directly in the browser.
No server needed: the frontend is fully self-contained HTML.
"""
import os, webbrowser, pathlib

html_path = pathlib.Path(__file__).parent / "templates" / "index.html"
url = html_path.resolve().as_uri()
print(f"Opening: {url}")
webbrowser.open(url)
