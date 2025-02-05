
from datetime import datetime, timedelta
import json
from flask import Response, stream_with_context
from flask_smorest import Blueprint, abort
from flask.views import MethodView
import redis

from controller.Bot.BotController import BotController
from controller.Database.DatabaseController import DatabaseController
from controller.Database.RedisController import RedisController
from controller.Socket.SocketController import SocketController
from globals import DEBUG, ERROR500, REDIS_URL
from models.Bot import BotModel
from models.History import HistoryModel
from models.Parking import ParkingModel
from schemas import BotSchema, HistoryQuerySchema, HistorySchema
from controller.Database.DatabaseController import db

blp = Blueprint('bot', __name__, description='IA BOT')

database = DatabaseController(BotModel)
databaseParkings = DatabaseController(ParkingModel)

botController = BotController()

redis_client = redis.StrictRedis.from_url(REDIS_URL)

socketController = SocketController(RedisController(redis_client))

@blp.route('')
class Bot(MethodView):
    
    @blp.arguments(BotSchema)
    @blp.response(200, BotSchema)
    def post(self, data):
        
        socketController.getAllParkingStatus()
        
        parkings = databaseParkings.getAll()
            
        context = []
        
        for parking in parkings:
            
            query = db.session.query(HistoryModel).filter(HistoryModel.parking_id == parking.id)
            days = 30
            query = query.filter(HistoryModel.time >= datetime.now() - timedelta(days=days)).all()
        
            hours = []
            
            for i in range(24): hours.append({"sum": 0, "len": 0})
                    
            for history in query:
                hours[history.time.hour]["sum"] += history.occupation
                hours[history.time.hour]["len"] += 1
                            
            prediction = [{"hour": f"{i:02}", "occupation": int(hour["sum"]/hour["len"]) if hour["len"] > 0 else 0} for i, hour in enumerate(hours)]
            
            parkingStatus = socketController.getParkingStatus(parking.id)
            
            status = parkingStatus.status
            ocupation =  parkingStatus.occupation
            
            context.append({
                "name": parking.name,
                "size": parking.size,
                "prediction": prediction,
                "status": status,
                "ocupation": ocupation
            })
            
        id = data.get('id', None)
        
        if not id:
            history = []
            model = database.addAndCommit(history=json.dumps(history))
            id = model.id
        else:
            model = database.getById(id)
            if model:
                history = json.loads(model.history)
            else:
                history = []
                model = database.addAndCommit(create_id = False, id = id, history=json.dumps(history))                        

        def stream_generator():
                        
            total_response = ""
                        
            for response in botController.query(data['query'], history, context):
                if response:
                         
                    total_response += response
                                        
                    data_stream = {"response": response}
                    
                    yield f"data: {json.dumps(data_stream)}\n\n"
                    
            history.append({
                "role": "user",
                "content": data['query']
            })
            
            history.append({
                "role": "assistant",
                "content": total_response
            })
                        
            database.updateAndCommit(id = id, history = json.dumps(history))
            
            data_stream = {
                "id": id,
                "query": data['query']
            }
            
            yield f"data: {json.dumps(data_stream)}\n\n"
            
        return Response(stream_with_context(stream_generator()), mimetype='text/event-stream')