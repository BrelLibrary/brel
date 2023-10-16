class PyBRLabel():
    """ Represents a label in XBRL."""
    # TODO: Implement this class properly.

    def __init__(self, text):
        self.__text = text
    
    def __str__(self) -> str:
        return self.__text