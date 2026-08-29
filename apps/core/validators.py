"""
Validation helpers for secure file uploads and inputs.
"""
import os
from django.core.exceptions import ValidationError
from django.utils.text import slugify

ALLOWED_IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.webp', '.svg', '.gif'}
MAX_UPLOAD_SIZE_BYTES = 5 * 1024 * 1024  # 5MB

def validate_image_file(uploaded_file):
    """
    Validates uploaded image file size and extension.
    """
    if not uploaded_file:
        return

    # Check file size
    if uploaded_file.size > MAX_UPLOAD_SIZE_BYTES:
        max_mb = MAX_UPLOAD_SIZE_BYTES / (1024 * 1024)
        raise ValidationError(f"File size exceeds maximum allowed limit of {max_mb:.0f}MB.")

    # Check file extension
    ext = os.path.splitext(uploaded_file.name)[1].lower()
    if ext not in ALLOWED_IMAGE_EXTENSIONS:
        allowed_list = ", ".join(ALLOWED_IMAGE_EXTENSIONS)
        raise ValidationError(f"Unsupported file format '{ext}'. Allowed image formats: {allowed_list}")

    return uploaded_file

def sanitize_filename(filename):
    """Sanitizes filename keeping extension safe."""
    name, ext = os.path.splitext(filename)
    safe_name = slugify(name) or 'upload'
    return f"{safe_name}{ext.lower()}"
