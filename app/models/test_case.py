from app import db
from datetime import datetime

class TestCase(db.Model):
    __tablename__ = 'test_case'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    project_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    sort = db.Column(db.Integer, default=0)
    creator_id = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<TestCase {self.name}>'