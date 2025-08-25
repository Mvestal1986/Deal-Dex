"""Bootstrap a local Python virtual environment for development.

This script creates a `.venv` directory using Python's built-in `venv`
module and installs project dependencies listed in `requirements.txt`.
"""

from __future__ import annotations

import subprocess
import sys
import venv
from pathlib import Path


def main() -> None:
    env_dir = Path(".venv")
    if not env_dir.exists():
        venv.create(env_dir, with_pip=True)
    python = env_dir / ("Scripts" if sys.platform == "win32" else "bin") / "python"
    subprocess.check_call(
        [str(python), "-m", "pip", "install", "-r", "requirements.txt"]
    )


if __name__ == "__main__":
    main()
