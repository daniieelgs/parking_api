import json
import random
import threading
import time
import traceback
from flask import request
from flask_socketio import Namespace, SocketIO, emit, join_room, disconnect, leave_room
from redis import Redis

from controller.Database.RedisController import RedisController
from controller.Security.HmacAuthController import HmacAuthController
from controller.Socket.SocketController import ParkingStatus, SocketController

ROOM = "GLOBAL_PARKING"

hmac = HmacAuthController()

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
        parkings = self.socketController.getAllParkingStatus()
        for parking in parkings:
            if parking.sid == sid:
                parking = self.socketController.updateParkingStatus(parking.parking_id, 'offline')
                self.notifyChangeParking(parking, ROOM)
                break
        leave_room(ROOM)
        
    def on_status(self, data):
        id = data.get('parkingId')
        sid = request.sid
        self.notifyParkingStatus([self.socketController.getParkingStatus(id)] if id else self.socketController.getAllParkingStatus(), sid)
        
    def on_change_parking(self, data):
        parkingId, signature, timestamp = hmac.read_signature_header(data)

        sid = request.sid

        try:
            
            hmac.verify_hmac_signature(parkingId, signature, timestamp, "change_parking")
            
            occupation = data.get('occupation')
                
            parking = self.socketController.updateParkingOccupation(parkingId, occupation)
            self.notifyChangeParking(parking, ROOM)
        except Exception as e:
            self.emit_error(str(e), to=sid)
        
    def on_status_parking(self, data):
        print('---------------- Status Parking:', data)
        
        parkingId, signature, timestamp = hmac.read_signature_header(data)

        sid = request.sid

        try:
            
            hmac.verify_hmac_signature(parkingId, signature, timestamp, "status_parking")
        
            status = data.get('status')
            
            parking = self.socketController.updateParkingStatus(parkingId, status, sid)
            self.notifyChangeParking(parking, ROOM)
        except Exception as e:
            self.emit_error(str(e), sid)
        
    def notifyParkingStatus(self, parkings:list[ParkingStatus], to=ROOM):        
        data = [parking.to_public_dict() for parking in parkings]
        emit('status', data, room=to)
        
    def notifyChangeParking(self, parking: ParkingStatus, to=ROOM):
        data = parking.to_public_dict()
        emit('change_parking', data, room=to)

    def emit_error(self, error, to):
        emit('error', error, to=to)