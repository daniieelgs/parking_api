from flask.views import MethodView
from flask_smorest import Blueprint, abort

from controller.Database.DatabaseController import DatabaseController
from controller.Database.GoogleMapController import GoogleMapController
from globals import GOOGLE_MAPS_API_KEY
from models.Parking import ParkingModel
from schemas import ParkingSchema

blp = Blueprint('parking', __name__, description='CRUD parkings.')

database = DatabaseController(ParkingModel)
googleMaps = GoogleMapController(GOOGLE_MAPS_API_KEY)

@blp.route('')
class Parkings(MethodView):
    
    @blp.response(200, ParkingSchema(many=True))
    def get(self):
        return database.getAll()
    
    @blp.arguments(ParkingSchema)
    @blp.response(201, ParkingSchema)
    def post(self, new_data):
                
        new_data['url_embed'] = googleMaps.generateUrlCrd(new_data['latitude'], new_data['longitude'], new_data['name'])
        return database.addAndCommit(**new_data)
    
@blp.route('/<string:id>')
class Parking(MethodView):
    
    @blp.response(404, description='Parking not found.')
    @blp.response(200, ParkingSchema)
    def get(self, id):
        if not database.existsById(id): abort(404, message=f"Parking '{id}' not found.")
        return database.getById(id)
    
    @blp.arguments(ParkingSchema)
    @blp.response(404, description='Parking not found.')
    @blp.response(200, ParkingSchema)
    def put(self, new_data, id):
        new_data['id'] = id
        if not database.existsById(id): abort(404, message=f"Parking '{new_data['id']}' not found.")
        new_data['url_embed'] = googleMaps.generateUrlCrd(new_data['latitude'], new_data['longitude'])
        return database.updateAndCommit(**new_data)
    
    @blp.response(404, description='Parking not found.')
    @blp.response(204)
    def delete(self, id):
        if not database.existsById(id): abort(404, message=f"Parking '{id}' not found.")
        database.deleteAndCommit(id=id)
        return {}