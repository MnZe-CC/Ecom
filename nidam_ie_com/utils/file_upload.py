import os
from werkzeug.utils import secure_filename
from flask import current_app

def allowed_file(filename):
    """
    Check if file extension is allowed.
    """
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_image(file, folder=None):
    """
    Save uploaded image file and return the filename.

    Args:
        file: The uploaded file object
        folder: Subfolder to save the file in (optional)

    Returns:
        str: The saved filename or None if failed
    """
    if not file or not allowed_file(file.filename):
        return None

    # Generate a secure filename
    filename = secure_filename(file.filename)

    # Add timestamp to prevent filename conflicts
    name, ext = os.path.splitext(filename)
    filename = f"{name}_{int(os.time())}{ext}"

    # Determine save path
    if folder:
        save_path = os.path.join(current_app.config['UPLOAD_FOLDER'], folder)
        os.makedirs(save_path, exist_ok=True)
    else:
        save_path = current_app.config['UPLOAD_FOLDER']

    # Save file
    file_path = os.path.join(save_path, filename)
    file.save(file_path)

    return filename

def delete_image(filename, folder=None):
    """
    Delete an image file.

    Args:
        filename: Name of the file to delete
        folder: Folder where the file is located (optional)

    Returns:
        bool: True if deletion successful, False otherwise
    """
    try:
        if folder:
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], folder, filename)
        else:
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)

        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        return False
    except Exception:
        return False