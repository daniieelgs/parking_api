
from controller.BaseController import BaseController

import traceback
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine

from datetime import datetime

import uuid

db = SQLAlchemy()

class DatabaseController(BaseController):
    
    def __init__(self, model, field_id = 'id'):
        super().__init__()
        
        self.model = model
        self.field_id = field_id
        
    def _current_datetime(self):
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    def _generate_uuid(self):
        return str(uuid.uuid4())
    
    def exists(self, **data):
        
        model = self.model(**data)
        
        if not model.id: return False
        
        instance = db.session.query(model.__class__).get(model.id)
        return instance is not None

    def existsById(self, id):            
        instance = db.session.query(self.model).get(id)
        return instance is not None

    def addDateTimes(self, **data):
        
        try:    
            
            if data:
                
                data['updated_at'] = self._current_datetime()
                
                if not self.exists(**data): data['created_at'] = self._current_datetime()
        except:
            traceback.print_exc()
        
        return data

    def addAndCommit(self, create_id = True, **data):
        
        if create_id: data[self.field_id] = self._generate_uuid()
        
        model = self.model(**self.addDateTimes(**data))
        
        print("MODEL: ", model)
        
        db.session.add(model)
        
        db.session.commit()
        
        return model

    def updateAndCommit(self, **data):
            
        model = db.session.query(self.model).get(data[self.field_id])
        
        if model:
            
            data = self.addDateTimes(**data)
            
            for key, value in data.items():
                setattr(model, key, value)
            
            db.session.commit()
        
        return model

    def deleteAndCommit(self, **data):
        
        model = db.session.query(self.model).get(data[self.field_id])
        
        if model:
            db.session.delete(model)
            db.session.commit()

        return True
    
    def get(self, **data):
        
        return db.session.query(self.model).get(data[self.field_id])
    
    def getById(self, id):
        
        if not self.existsById(id): return None
        
        return db.session.query(self.model).get(id)
    
    def getAll(self):
            
        return self.model.query.all()
    
    