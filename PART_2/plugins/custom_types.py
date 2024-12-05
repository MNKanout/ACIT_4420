# plugins/custom_types.py

from filetype_handlers import register_file_type

@register_file_type(r'\.docx$', 'Documents')
def handle_docx_file():
    pass

@register_file_type(r'\.csv$', 'Spreadsheets')
def handle_csv_file():
    pass
