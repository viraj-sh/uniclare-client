import os
import ctypes
from app import app
import uvicorn

# Enable VT100 colors on Windows only (safe for macOS)
def enable_vt100():
    if os.name == "nt":
        try:
            kernel32 = ctypes.windll.kernel32
            handle = kernel32.GetStdHandle(-11)
            mode = ctypes.c_uint()
            kernel32.GetConsoleMode(handle, ctypes.byref(mode))
            kernel32.SetConsoleMode(handle, mode.value | 0x0004)
        except Exception:
            pass

# Disable color output for consistent logs
os.environ["NO_COLOR"] = "1"
os.environ["UVICORN_NO_COLOR"] = "1"

enable_vt100()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)