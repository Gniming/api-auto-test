from app import db
from datetime import datetime

class Task(db.Model):
    __tablename__ = 'task'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    project_id = db.Column(db.Integer, nullable=False)
    case_id = db.Column(db.Integer, nullable=True)
    env_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(200), nullable=False)
    creator_id = db.Column(db.Integer)
    status = db.Column(db.Enum('pending', 'running', 'success', 'failed', 'stopped'), default='pending')
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    duration = db.Column(db.Integer)
    pass_count = db.Column(db.Integer, default=0)
    fail_count = db.Column(db.Integer, default=0)
    total_steps = db.Column(db.Integer, default=0)
    log = db.Column(db.Text)  # JSON 存储详细执行日志
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Task {self.name}>'