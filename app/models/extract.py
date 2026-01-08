from app import db
from datetime import datetime

class Extract(db.Model):
    __tablename__ = 'extract'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    step_id = db.Column(db.Integer, nullable=False)
    var_name = db.Column(db.String(100), nullable=False)
    expression = db.Column(db.Text, nullable=False)
    scope = db.Column(db.Enum('case', 'global'), default='case')
    var_type = db.Column(db.Enum('string', 'int', 'bool', 'float'), default='string')
    creator_id = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Extract {self.var_name}>'