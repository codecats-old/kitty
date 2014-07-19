try:
    from Pillow import Image
except ImportError:
    from PIL import Image
import os
from kitty.settings import BASE_DIR


def handle_uploaded_file(f, name=None):
    if name is None: name = str(f)
    full_path = os.path.join(BASE_DIR, 'static', 'uploads', name)
    with open(full_path, 'w+b') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    im = Image.open(full_path)
    img = im.resize((250, 250), Image.ANTIALIAS)
    imgIcon = im.resize((50, 50), Image.ANTIALIAS)
    img.save(full_path, 'PNG')
    imgIcon.save(full_path + 'tiny', 'PNG')
    return full_path

