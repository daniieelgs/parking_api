
class InvalidSignatureException(Exception):
    def __init__(self, message:str = "Invalid signature."):
        super(InvalidSignatureException, self).__init__(message)