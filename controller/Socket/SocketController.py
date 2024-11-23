
from redis import Redis
from controller.BaseController import BaseController
from controller.Database.DatabaseController import DatabaseController, db
from controller.Database.RedisController import RedisController
from models.Parking import ParkingModel

from enum import Enum

class Status(Enum):
    ONLINE = 'online'
    OFFLINE = 'offline'

class ParkingStatus:
    
    def __init__(self, parkingId:str, name:str, status:Status, occupation:int, size:int, url_embed:str, sid:str):
        self.parking_id = parkingId
        self.name = name
        self.status = status
        self.occupation = occupation
        self.size = size
        self.url_embed = url_embed
        self.sid = sid
        
    def to_dict(self):
        return {
            'parkingId': self.parking_id,
            'name': self.name,
            'status': self.status.value if isinstance(self.status, Status) else self.status,
            'occupation': self.occupation,
            'size': self.size,
            'url_embed': self.url_embed,
            'sid': self.sid
        }
        
    def to_public_dict(self):
        data = self.to_dict()
        del data['sid']
        return data
    
PARKING = 'parking'

class SocketController(BaseController):
    
    def __init__(self, redis_controller: RedisController, parkingDb: DatabaseController = DatabaseController(ParkingModel)):
        super().__init__()
        self.redisController = redis_controller
        self.parkingDb = parkingDb
        self.initAllParkings()
        
    def _defaultParkingStatus(self, parking) -> ParkingStatus:
        return ParkingStatus(parking.id, name=parking.name, status=Status.OFFLINE, occupation=0, size=parking.size, url_embed=parking.url_embed, sid=None)
        
    def initParking(self, parking):
        self.redisController.addValues(f'{PARKING}', {parking.id: self._defaultParkingStatus(parking).to_dict()})
        
    def initAllParkings(self):
        self.redisController.remove(PARKING)
        parkings = self.parkingDb.getAll()
        
        print("PARKINGS:", parkings, flush=True)
        
        for parking in parkings:
            self.initParking(parking)
            
    def getParkingStatus(self, parking_id:str) -> ParkingStatus:
        parkings = self.redisController.get(PARKING)
        return ParkingStatus(**parkings.get(parking_id)) if parkings else None
    
    def getAllParkingStatus(self) -> list[ParkingStatus]:
        parkings = self.redisController.get(PARKING)
        
        print("PARKINGS:\n", parkings, flush=True)
        
        return [ParkingStatus(**v) for k, v in parkings.items()] if parkings else []