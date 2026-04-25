import os
import uuid

def save_uploaded_file(uploaded_file, folder):
    os.makedirs(folder, exist_ok=True)
    name = f"{uuid.uuid4()}_{uploaded_file.name}"
    path = os.path.join(folder, name)
    with open(path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return path

def ensure_dirs():
    for d in ["media/uploads", "media/outputs"]:
        os.makedirs(d, exist_ok=True)