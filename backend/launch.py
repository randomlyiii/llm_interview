"""Redirect: backend launcher moved to project root."""
import subprocess, sys
from pathlib import Path

ROOT_LAUNCH = Path(__file__).resolve().parent.parent / "launch.py"

if __name__ == "__main__":
    print("Backend launcher moved to project root. Redirecting...")
    subprocess.run([sys.executable, str(ROOT_LAUNCH)] + sys.argv[1:])
