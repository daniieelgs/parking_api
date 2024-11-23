import json
import random
import threading
import time
import traceback
from flask import request
from flask_socketio import Namespace, SocketIO, emit, join_room, disconnect, leave_room
from redis import Redis

from controller.Database.RedisController import RedisController
from controller.Socket.SocketController import ParkingStatus, SocketController

ROOM = "GLOBAL_PARKING"

class SocketMiddleware(Namespace):
    
    def __init__(self, redis_client: Redis, socketio: SocketIO, *args, **kwargs):
        super(SocketMiddleware, self).__init__(*args, **kwargs)
        self.socketController = SocketController(RedisController(redis_client))
        self.socketio = socketio
        
    def on_connect(self):
        sid = request.sid
        print('---------------- Client connected:', sid)
        join_room(ROOM)

    def on_disconnect(self):
        sid = request.sid
        print('---------------- Client disconnected:', sid)
        leave_room(ROOM)
        
    def on_status(self, data):
        id = data.get('parkingId')
        sid = request.sid
        self.notifyParkingStatus([self.socketController.getParkingStatus(id)] if id else self.socketController.getAllParkingStatus(), sid)
        
    def notifyParkingStatus(self, parkings:list[ParkingStatus], to=ROOM):        
        data = [parking.to_public_dict() for parking in parkings]
        emit('status', data, room=to)
