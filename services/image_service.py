import os, uuid, requests
from io import BytesIO

# ══════════════════════════════════════════
#  SERVICE — Image Upload & Fetch
# ══════════════════════════════════════════

def allowed_file(filename: str, allowed: set) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed


def save_upload(file, upload_folder: str, allowed_extensions: set) -> str:
    """ 
    Validate and save uploaded file with a unique UUID filename.
    Returns the absolute path of the saved file.
    """
    if not allowed_file(file.filename, allowed_extensions):
        raise ValueError(f"Format non supporté. Utilisez : {allowed_extensions}")

    ext      = file.filename.rsplit('.', 1)[1].lower()
    filename = f"{uuid.uuid4().hex}.{ext}"

    os.makedirs(upload_folder, exist_ok=True)
    path = os.path.join(upload_folder, filename)
    file.save(path)
    return path

def fetch_image_from_url(url: str, upload_folder: str, allowed_extensions: set) -> str:
    """
    Downloads an image from a URL and saves it to the upload folder.
    Returns the absolute path of the saved file.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        # Determine extension from URL or Content-Type
        filename = url.split('/')[-1].split('?')[0]
        if '.' not in filename:
            content_type = response.headers.get('Content-Type', '')
            if 'image/jpeg' in content_type: ext = 'jpg'
            elif 'image/png' in content_type: ext = 'png'
            else: raise ValueError("Type de contenu non supporté.")
        else:
            ext = filename.rsplit('.', 1)[1].lower()

        if ext not in allowed_extensions:
            raise ValueError(f"Extension .{ext} non supportée.")

        new_filename = f"{uuid.uuid4().hex}.{ext}"
        os.makedirs(upload_folder, exist_ok=True)
        path = os.path.join(upload_folder, new_filename)
        
        with open(path, 'wb') as f:
            f.write(response.content)
            
        return path
    except Exception as e:
        raise Exception(f"Erreur lors du téléchargement de l'image : {str(e)}")
