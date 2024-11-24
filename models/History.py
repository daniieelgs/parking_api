from controller.Database.DatabaseController import db

TABLENAME = 'history'

class HistoryModel(db.Model):
    
    __tablename__ = TABLENAME
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    time = db.Column(db.DateTime, nullable=False)
    parking_id = db.Column(db.String(36), db.ForeignKey(f'parking.id'), nullable=False)
    access = db.Column(db.Boolean, nullable=False)
    occupation = db.Column(db.Integer, nullable=False)
    
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)
    
    parking = db.relationship('ParkingModel', back_populates='histories')
    
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