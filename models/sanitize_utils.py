# sanitize_utils.py

import re

def sanitize_filename(filename):
    """
    Sanitizes the filename by removing or replacing invalid characters.
    """
    # Define invalid characters for Windows filenames
    invalid_chars = r'[<>:"/\\|?*]'
    # Replace invalid characters with an underscore or remove them
    sanitized = re.sub(invalid_chars, '', filename)
    return sanitized
