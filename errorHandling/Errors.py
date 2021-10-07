class DirNotMatchingError(Exception):
    """Raised when the urls of both files are not in the same directory"""
    pass


class ListLengthError(Exception):
    """Raised if the length of two lists are different"""
    pass


class MisMatchError(Exception):
    """Raised if the length of two lists are different"""
    pass


class MissingValueError(Exception):
    """One or several values are missing"""
    pass
