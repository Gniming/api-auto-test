from app import db
from datetime import datetime

class AssertRule(db.Model):
    __tablename__ = 'assert_rule'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    step_id = db.Column(db.Integer, nullable=False)
    assert_type = db.Column(db.Enum('status_code', 'contain', 'not_contain', 'json_equal', 'json_schema', 'regex', 'length', 'database'), nullable=False)
    expect_value = db.Column(db.Text)
    actual_source = db.Column(db.Enum('response_body', 'response_headers', 'response_status'), default='response_body')
    description = db.Column(db.String(255))
    creator_id = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<AssertRule {self.assert_type}>'