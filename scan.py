import os

for root, dirs, files in os.walk("."):
    if "venv" in root or "__pycache__" in root:
        continue
    for filename in files:
        path = os.path.join(root, filename)
        try:
            with open(path, "rb") as fh:
                if b"\x00" in fh.read():
                    print(path)
        except Exception:
            pass
