import os
from kitty.settings import BASE_DIR


def handle_uploaded_file(f, name=None):
    if name is None: name = str(f)
    full_path = os.path.join(BASE_DIR, 'static', 'uploads', name)
    with open(full_path, 'w+b') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return full_path

