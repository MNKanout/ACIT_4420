# filetype_handlers.py

import re

file_type_registry = []

def register_file_type(pattern, target_directory):
    def decorator(func):
        compiled_pattern = re.compile(pattern, re.IGNORECASE)
        file_type_registry.append((compiled_pattern, target_directory))
        return func
    return decorator

# Register default file types
@register_file_type(r'\.txt$', 'TextFiles')
def handle_text_file():
    pass

@register_file_type(r'\.(jpg|jpeg|png|gif)$', 'Images')
def handle_image_file():
    pass

@register_file_type(r'\.pdf$', 'PDFs')
def handle_pdf_file():
    pass

@register_file_type(r'\.(mp3|wav)$', 'Music')
def handle_music_file():
    pass
