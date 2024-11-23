import json
import random
import threading
import time
import traceback
from flask import request
from flask_socketio import Namespace, SocketIO, emit, join_room, disconnect, leave_room
from redis import Redis

ROOM = "room1"

class SocketMiddleware(Namespace):
    
    def __init__(self, redis_client: Redis, socketio: SocketIO, *args, **kwargs):
        super(SocketMiddleware, self).__init__(*args, **kwargs)
        self.redisClient = redis_client
        self.socketio = socketio
        self.thread = None
        self.activeConnections = set()
        self.start_background_task()
        
    def start_background_task(self):
        if self.thread is None:
            self.thread = self.socketio.start_background_task(self.random_number_broadcast)

    def random_number_broadcast(self):
        while True:
            try:
                number = random.randint(1, 100)
                print(f"Broadcasting random number: {number}", flush=True)
                
                self.emit("random_number", {"number": number}, room=ROOM)
                
                time.sleep(10)
            except Exception as e:
                print("Error in random_number_broadcast:", str(e))
                traceback.print_exc()
        
    def on_connect(self):
        """Se ejecuta cuando un cliente se conecta."""
        sid = request.sid
        print('---------------- Client connected:', sid)
        join_room(ROOM)
        self.activeConnections.add(sid)

    def on_message(self, message):
        sid = request.sid
        print('---------------- Message received:', message, 'from:', sid)
        emit("response", {"number": 9}, room=sid)

    def on_disconnect(self):
        sid = request.sid
        print('---------------- Client disconnected:', sid)
        leave_room(ROOM)
        self.activeConnections.remove(sid)