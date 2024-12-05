# errors.py

class FileOrganizerError(Exception):
    """Base class for exceptions in this module."""
    pass

class DirectoryNotFoundError(FileOrganizerError):
    """Exception raised when the specified directory does not exist."""
    pass

class PermissionDeniedError(FileOrganizerError):
    """Exception raised for permission related issues."""
    pass
