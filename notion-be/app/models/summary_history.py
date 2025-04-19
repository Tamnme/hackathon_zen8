from app.models import db
from datetime import datetime
from enum import Enum
import json

class StatusEnum(str, Enum):
    START = "start"
    IN_PROGRESS = "in_progress"
    SUCCESS = "success"
    FAILED = "failed"

class SummaryHistory(db.Model):
    __tablename__ = 'summary_histories'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False, index=True)
    status = db.Column(db.String(20), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    end_time = db.Column(db.DateTime, nullable=True)
    _channels = db.Column('channels', db.Text, nullable=True)
    notion_page_url = db.Column(db.String(255), nullable=True)
    
    @property
    def channels(self):
        return json.loads(self._channels) if self._channels else []
    
    @channels.setter
    def channels(self, value):
        if value is not None:
            self._channels = json.dumps(value) if isinstance(value, list) else value
        else:
            self._channels = None
    
    def __repr__(self):
        return f"<SummaryHistory id={self.id}, email={self.email}, status={self.status}>"
    
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'status': self.status,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'channels': self.channels,
            'notion_page_url': self.notion_page_url
        } 