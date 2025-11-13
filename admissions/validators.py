# uploads/validators.py
from django.core.exceptions import ValidationError

def validate_file_size(value):
    filesize = value.size
    
    # Define your maximum file size in bytes (e.g., 5MB)
    max_upload_size = 5 * 1024 * 1024  # 5 MB
    
    if filesize > max_upload_size:
        raise ValidationError(f"The maximum file size allowed is {max_upload_size / (1024 * 1024):.0f}MB. Your file size is {filesize / (1024 * 1024):.2f}MB.")
    return value