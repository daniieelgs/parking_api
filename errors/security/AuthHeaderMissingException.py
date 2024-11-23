
class AuthHeaderMissingException(Exception):
    def __init__(self, message:str = "Authorization header is missing."):
        super().__init__(message)