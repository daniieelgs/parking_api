
class ParkingNotFoundException(Exception):
    def __init__(self, message:str = "Parking not found."):
        super().__init__(message)