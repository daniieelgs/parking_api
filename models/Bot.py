
import json
from controller.Database.DatabaseController import db

TABLENAME = 'bot'

class BotModel(db.Model):
    
    __tablename__ = TABLENAME
    
    id = db.Column(db.String(36), primary_key=True)
    history = db.Column(db.Text)
    
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)
    
    def to_dict(self):
        return {
            "id": self.id,
            "history": json.loads(self.history)
        }