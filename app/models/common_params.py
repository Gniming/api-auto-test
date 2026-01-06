from app import db
from datetime import datetime

class CommonParams(db.Model):
    __tablename__ = 'common_params'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    project_id = db.Column(db.Integer, nullable=True)
    name = db.Column(db.String(100), nullable=False)
    headers = db.Column(db.Text, nullable=False)
    description = db.Column(db.String(255))
    creator_id = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint('project_id', 'name', name='uniq_project_name'),
    )

    def __repr__(self):
        return f'<CommonParams {self.name}>'