from app import db
from datetime import datetime

class RequestData(db.Model):
    __tablename__ = 'request_data'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    step_id = db.Column(db.Integer, nullable=False)
    headers = db.Column(db.Text)
    params = db.Column(db.Text)
    data = db.Column(db.Text)
    files = db.Column(db.Text)
    timeout = db.Column(db.Integer, default=30)
    creator_id = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<RequestData for step {self.step_id}>'