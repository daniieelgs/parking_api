
from controller.BaseController import BaseController


class GoogleMapController(BaseController):
    
    def __init__(self, api_key):
        super().__init__()
        self.api_key = api_key
        self.base_url = "https://www.google.com/maps/embed/v1/place"
        
    def generateUrlCrd(self, latitude, longitude):
        return f"{self.base_url}?key={self.api_key}&q={latitude},{longitude}"
    
    def generateUrlName(self, name):
        return f"{self.base_url}?key={self.api_key}&q={name}"
    