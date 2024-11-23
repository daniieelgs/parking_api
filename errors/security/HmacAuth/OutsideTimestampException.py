
class OutsideTimestampException(Exception):
    def __init__(self, message: str = "Request timestamp is outside the acceptable time window."):
        self.message = message