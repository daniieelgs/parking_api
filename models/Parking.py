from controller.Database.DatabaseController import db

TABLENAME = 'parking'

class ParkingModel(db.Model):
    
    __tablename__ = TABLENAME
    
    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    
    size = db.Column(db.Integer, nullable=False)
    url_embed = db.Column(db.String(255), nullable=True)
    
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'size': self.size,
            'url_embed': self.url_embed,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }