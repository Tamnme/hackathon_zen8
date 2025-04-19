from app.models import db
from datetime import date
import json

class TriggerSetting(db.Model):
    __tablename__ = 'trigger_settings'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False, index=True)
    _channels = db.Column('channels', db.Text, nullable=True)
    start_date = db.Column(db.Date, nullable=True)
    end_date = db.Column(db.Date, nullable=True)
    
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
        return f"<TriggerSetting id={self.id}, email={self.email}>"
    
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'channels': self.channels,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None
        } 