
import json

from redis import Redis
from controller.BaseController import BaseController


class RedisController(BaseController):
    
    def __init__(self, redis_client:Redis):
        super().__init__()
        self.redisClient = redis_client
        
    def set(self, key:str, value:dict):
        self.redisClient.set(key, json.dumps(value))
        
    def get(self, key:str) -> dict:
        value = self.redisClient.get(key)
        return json.loads(value) if value else None
    
    def remove(self, key:str):
        self.redisClient.delete(key)
    
    def addValues(self, key:str, value:dict):
        _value = self.get(key)
        
        if not _value: _value = {}
        
        for k, v in value.items():
            _value[k] = v
            
        self.set(key, _value)
        
    def removeValues(self, key:str, value:list[str]):
        _value = self.get(key)
        
        if not _value: return
        
        for k in value:
            if k in _value: del _value[k]
        
        self.set(key, _value)