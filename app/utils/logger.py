import time
import json

def log(msg: str, **kwargs):
    ts = time.time()
    try:
        print(f"[{ts}] {msg} {json.dumps(kwargs)}")
    except Exception:
        print(f"[{ts}] {msg}")
