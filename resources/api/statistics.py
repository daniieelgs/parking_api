
from datetime import datetime, timedelta
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from globals import DEBUG, ERROR500
from models.History import HistoryModel
from models.Parking import ParkingModel
from schemas import HourStadisticsSchema, StadisticsQuerySchema

from controller.Database.DatabaseController import DatabaseController, db

blp = Blueprint('statistics', __name__, description='Check Statistics Parkings.')

database = DatabaseController(ParkingModel)

@blp.route('<string:id>')
class Stadistics(MethodView):
    
    @blp.arguments(StadisticsQuerySchema, location='query')
    @blp.response(404, description='Parking not found.')
    @blp.response(200, HourStadisticsSchema(many=True))
    def get(self, args, id):
        try:
            parking = database.getById(id)
        except Exception as e:
            abort(500, message=str(e) if DEBUG else ERROR500)
        if not parking:
            abort(404, message=f"Parking '{id}' not found.")
            
        query = db.session.query(HistoryModel).filter(HistoryModel.parking_id == parking.id)
        days = args.get('days', 30)
        query = query.filter(HistoryModel.time >= datetime.now() - timedelta(days=days)).all()
        
        hours = []
        
        for i in range(24): hours.append({"sum": 0, "len": 0})
                
        for history in query:
            hours[history.time.hour]["sum"] += history.occupation
            hours[history.time.hour]["len"] += 1
                        
        return [{"hour": f"{i:02}", "occupation": hour["sum"]/hour["len"] if hour["len"] > 0 else 0} for i, hour in enumerate(hours)]
        
        