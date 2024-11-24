import json
from marshmallow import Schema, ValidationError, fields, validate, validates

from marshmallow import Schema, fields

class ParkingSchema(Schema):
    id = fields.Str(dump_only=True)
        
    name = fields.Str(required=True)
    size = fields.Int(required=True)
    
    latitude = fields.Float(required=True)
    longitude = fields.Float(required=True)
    
    url_embed = fields.Str(dump_only=True)
    
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    
class HistorySchema(Schema):
    id = fields.Int(dump_only=True)
    
    time = fields.DateTime(required=True)
    parking_id = fields.Str(required=True)
    access = fields.Bool(required=True)
    occupation = fields.Int(required=True)
    
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    
class HistoryQuerySchema(Schema):
    start = fields.DateTime()
    end = fields.DateTime()