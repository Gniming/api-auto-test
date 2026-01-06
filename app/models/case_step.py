from app import db
from datetime import datetime

class CaseStep(db.Model):
    __tablename__ = 'case_step'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    case_id = db.Column(db.Integer, nullable=False)
    step_type = db.Column(db.Enum('request', 'wait', 'script'), nullable=False, default='request')
    name = db.Column(db.String(200))
    method = db.Column(db.Enum('GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD', 'OPTIONS'), default='GET')
    path = db.Column(db.String(500))
    sort = db.Column(db.Integer, default=0)
    enabled = db.Column(db.Boolean, default=True)
    creator_id = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<CaseStep {self.name}>'