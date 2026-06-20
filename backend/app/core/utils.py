import json
import re
import os
import sys


def extract_json(text: str) -> dict:
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if lines:
        last = lines[-1]
        if last.startswith("{") and last.endswith("}"):
            try:
                return json.loads(last)
            except json.JSONDecodeError:
                pass

    matches = list(re.finditer(r"\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}", text, re.DOTALL))
    if matches:
        candidate = matches[-1].group()
        try:
            return json.loads(candidate)
        except json.JSONDecodeError:
            pass

    raise ValueError("No valid JSON found in the response.")


import sys
import os

def static_path() -> str:
    if hasattr(sys, '_MEIPASS'):
        base_dir = sys._MEIPASS
    elif os.path.basename(sys.executable).startswith('python'):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    else:
        base_dir = os.path.dirname(sys.executable)
    return os.path.join(base_dir, "static")