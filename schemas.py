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