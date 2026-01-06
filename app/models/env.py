from app import db
from datetime import datetime

class Env(db.Model):
    __tablename__ = 'env'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    base_url = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255))
    creator_id = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Env {self.name}>'