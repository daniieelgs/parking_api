
class InvalidAuthHeaderException(Exception):
    def __init__(self, message:str = "Invalid Authorization header."):
        super().__init__(message)