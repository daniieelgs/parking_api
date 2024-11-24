
from datetime import datetime
from flask_smorest import Blueprint, abort
from flask.views import MethodView

from controller.Database.DatabaseController import DatabaseController
from globals import DEBUG, ERROR500
from models.History import HistoryModel
from models.Parking import ParkingModel
from schemas import HistoryQuerySchema, HistorySchema
from controller.Database.DatabaseController import db

blp = Blueprint('history', __name__, description='Check History Parkings.')

database = DatabaseController(ParkingModel)

@blp.route('<string:id>')
class History(MethodView):
    
    @blp.arguments(HistoryQuerySchema, location='query')
    @blp.response(404, description='Parking not found.')
    @blp.response(200, HistorySchema(many=True))
    def get(self, args, id):
        try:
            parking = database.getById(id)
        except Exception as e:
            abort(500, message=str(e) if DEBUG else ERROR500)
        if not parking:
            abort(404, message=f"Parking '{id}' not found.")
        
        start = args.get('start')
        end = args.get('end', datetime.now())

        query = db.session.query(HistoryModel).filter(HistoryModel.parking_id == parking.id)

        if start:
            query = query.filter(HistoryModel.time >= start, HistoryModel.time <= end)
        
        return query.all()