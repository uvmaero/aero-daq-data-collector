class CanUtilError(Exception):
    def __init__(self, message):
        # pass the exception error message to the parent object
        super().__init__(message)