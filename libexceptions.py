# Library custom exceptions

class TypeListError(Exception):
    """ Exception raised when the type list (types) contains wrong data """
    def __init__(self, error):
        super().__init__(error)

class ValueCastError(Exception):
    """ Exception raised when the value was not cast due to and error """
    def __init__(self, error):
        super().__init__(error)

class WrongArgumentError(Exception):
    """ Exception raised when the value was not cast due to and error """
    def __init__(self, error):
        super().__init__(error)
