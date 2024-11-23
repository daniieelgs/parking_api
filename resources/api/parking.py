from flask.views import MethodView
from flask_smorest import Blueprint, abort

from controller.Database.DatabaseController import DatabaseController
from controller.Database.GoogleMapController import GoogleMapController
from globals import DEBUG, ERROR500, GOOGLE_MAPS_API_KEY
from models.Parking import ParkingModel
from schemas import ParkingSchema

blp = Blueprint('parking', __name__, description='CRUD parkings.')

database = DatabaseController(ParkingModel)
googleMaps = GoogleMapController(GOOGLE_MAPS_API_KEY)

@blp.route('')
class Parkings(MethodView):
    
    @blp.response(200, ParkingSchema(many=True))
    def get(self):
        try:
            return database.getAll()
        except Exception as e:
            abort(500, message=str(e) if DEBUG else ERROR500)
    
    @blp.arguments(ParkingSchema)
    @blp.response(201, ParkingSchema)
    def post(self, new_data):
             
        try:
        
            new_data['url_embed'] = googleMaps.generateUrlCrd(new_data['latitude'], new_data['longitude'])
        
            return database.addAndCommit(**new_data)
        
        except Exception as e:
            abort(400, message=str(e) if DEBUG else ERROR500)
    
@blp.route('/<string:id>')
class Parking(MethodView):
    
    @blp.response(404, description='Parking not found.')
    @blp.response(200, ParkingSchema)
    def get(self, id):
        
        try:
        
            parking = database.getById(id)
        
        except Exception as e:
            abort(500, message=str(e) if DEBUG else ERROR500)
                     
        if not parking: abort(404, message=f"Parking '{id}' not found.")
        
        return parking
    
    @blp.arguments(ParkingSchema)
    @blp.response(404, description='Parking not found.')
    @blp.response(200, ParkingSchema)
    def put(self, new_data, id):
        
        try:
        
            new_data['id'] = id
        
            if not database.existsById(id): abort(404, message=f"Parking '{new_data['id']}' not found.")
        
            new_data['url_embed'] = googleMaps.generateUrlCrd(new_data['latitude'], new_data['longitude'])
        
            return database.updateAndCommit(**new_data)
        
        except Exception as e:
            abort(500, message=str(e) if DEBUG else ERROR500)
    
    @blp.response(404, description='Parking not found.')
    @blp.response(204)
    def delete(self, id):
        
        try:
            
            if not database.existsById(id): abort(404, message=f"Parking '{id}' not found.")
            
            
            database.deleteAndCommit(id=id)
            
            return {}
        
        except Exception as e:
            abort(500, message=str(e) if DEBUG else ERROR500)