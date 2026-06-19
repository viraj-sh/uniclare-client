#!/usr/bin/env python3

from __future__ import annotations

import argparse
import platform
import shutil
import socket
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BACKEND_DIR = ROOT / "backend"
FRONTEND_DIR = ROOT / "frontend"
VENV_DIR = BACKEND_DIR / ".venv"
IS_WINDOWS = platform.system() == "Windows"
DEFAULT_PORT = 3000

DEBUG = False


# Helpers


def header(msg: str) -> None:
    """Stage title -- always printed, in both quiet and debug mode."""
    print(f"\n\033[1;36m==> {msg}\033[0m")


def run(cmd: list[str], cwd: Path, label: str) -> None:
    if DEBUG:
        print(f"    $ {' '.join(cmd)}   (cwd: {cwd})")
        try:
            subprocess.run(cmd, cwd=cwd, check=True)
        except FileNotFoundError as exc:
            sys.exit(f"\n✗ {label} failed: command not found -> {exc}")
        except subprocess.CalledProcessError as exc:
            sys.exit(
                f"\n✗ {label} failed (exit code {exc.returncode}). "
                "Aborting -- backend will not start."
            )
    else:
        try:
            subprocess.run(
                cmd,
                cwd=cwd,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
            )
        except FileNotFoundError as exc:
            sys.exit(f"\n✗ {label} failed: command not found -> {exc}")
        except subprocess.CalledProcessError as exc:
            print(f"\n--- output from: {' '.join(cmd)} ---")
            print(exc.stdout)
            print("--- end output ---")
            sys.exit(
                f"\n✗ {label} failed (exit code {exc.returncode}). "
                "Aborting -- backend will not start. "
                "(Re-run with --debug to see live output as it happens.)"
            )


def require_tool(name: str, install_hint: str | None = None) -> None:
    if shutil.which(name) is None:
        msg = f"✗ '{name}' was not found on PATH."
        if install_hint:
            msg += f"\n  {install_hint}"
        sys.exit(msg)


def venv_paths() -> tuple[Path, Path]:
    """Return (python_executable, scripts_dir) inside the fallback venv."""
    if IS_WINDOWS:
        scripts_dir = VENV_DIR / "Scripts"
        python_exe = scripts_dir / "python.exe"
    else:
        scripts_dir = VENV_DIR / "bin"
        python_exe = scripts_dir / "python"
    return python_exe, scripts_dir


def find_available_port(
    start_port: int, host: str = "0.0.0.0", max_tries: int = 50
) -> int:
    """Return the first free port at or after start_port."""
    port = start_port
    for _ in range(max_tries):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                sock.bind((host, port))
                return port
            except OSError:
                port += 1
    sys.exit(f"✗ Could not find a free port after trying {start_port}-{port - 1}.")


# Backend setup -- uv path


def setup_backend_uv() -> None:
    header("Syncing backend dependencies (uv sync)")
    run(["uv", "sync"], cwd=BACKEND_DIR, label="uv sync")


def start_backend_uv(port: int) -> None:
    header(f"Starting backend on port {port} (uv run fastapi run app/main.py)")
    print(f"    Serving at http://localhost:{port}\n")
    cmd = ["uv", "run", "fastapi", "run", "app/main.py", "--port", str(port)]
    subprocess.run(cmd, cwd=BACKEND_DIR)


# Backend setup -- plain venv + pip fallback


def setup_backend_pip() -> Path:
    """Returns the path to the fastapi CLI inside the fallback venv."""
    python_exe, scripts_dir = venv_paths()

    if not python_exe.exists():
        header("uv not found -- creating a plain venv instead (backend/.venv)")
        run(
            [sys.executable, "-m", "venv", str(VENV_DIR)],
            cwd=ROOT,
            label="venv creation",
        )
    else:
        header("Reusing existing backend/.venv")

    header("Upgrading pip")
    run(
        [str(python_exe), "-m", "pip", "install", "--upgrade", "pip"],
        cwd=BACKEND_DIR,
        label="pip upgrade",
    )

    header("Installing backend requirements (requirements.txt)")
    run(
        [str(python_exe), "-m", "pip", "install", "-r", "requirements.txt"],
        cwd=BACKEND_DIR,
        label="backend dependency install",
    )

    return scripts_dir / ("fastapi.exe" if IS_WINDOWS else "fastapi")


def start_backend_pip(fastapi_bin: Path, port: int) -> None:
    if not fastapi_bin.exists():
        sys.exit(
            "✗ Could not find the 'fastapi' CLI in the venv.\n"
            "  Make sure backend/requirements.txt includes 'fastapi[standard]'."
        )

    header(f"Starting backend on port {port} (fastapi run app/main.py)")
    print(f"    Serving at http://localhost:{port}\n")
    cmd = [str(fastapi_bin), "run", "app/main.py", "--port", str(port)]
    subprocess.run(cmd, cwd=BACKEND_DIR)


# Frontend


def build_frontend() -> None:
    require_tool("npm")

    header("Installing frontend dependencies (npm install)")
    run(["npm", "install"], cwd=FRONTEND_DIR, label="npm install")

    header("Building frontend (npm run build)")
    run(["npm", "run", "build"], cwd=FRONTEND_DIR, label="frontend build")


# Main


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build the frontend and launch the uniclare-client backend with one command."
    )
    verbosity = parser.add_mutually_exclusive_group()
    verbosity.add_argument(
        "--quiet",
        action="store_true",
        help="Minimal output: only stage titles (default).",
    )
    verbosity.add_argument(
        "--debug",
        action="store_true",
        help="Verbose output: show every command run and its full live output.",
    )
    return parser.parse_args()


def main() -> None:
    global DEBUG

    args = parse_args()
    DEBUG = args.debug

    if not BACKEND_DIR.is_dir() or not FRONTEND_DIR.is_dir():
        sys.exit(
            "✗ Run this script from the project root "
            "(backend/ and frontend/ must exist next to it)."
        )

    use_uv = shutil.which("uv") is not None
    fastapi_bin: Path | None = None

    if use_uv:
        setup_backend_uv()
    else:
        print(
            "\n(i) 'uv' not found on PATH -- falling back to venv + pip.\n"
            "    For faster, more reliable installs, consider installing uv:\n"
            "    https://docs.astral.sh/uv/getting-started/installation/"
        )
        fastapi_bin = setup_backend_pip()

    build_frontend()

    port = find_available_port(DEFAULT_PORT)
    if port != DEFAULT_PORT:
        header(f"Port {DEFAULT_PORT} is busy -- using {port} instead")

    if use_uv:
        start_backend_uv(port)
    else:
        assert fastapi_bin is not None
        start_backend_pip(fastapi_bin, port)


if __name__ == "__main__":
    main()
