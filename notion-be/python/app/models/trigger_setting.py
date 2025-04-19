from app.models import db
from datetime import date

class TriggerSetting(db.Model):
    __tablename__ = 'trigger_settings'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False, index=True)
    channels = db.Column(db.String(255), nullable=True)
    start_date = db.Column(db.Date, nullable=True)
    end_date = db.Column(db.Date, nullable=True)
    
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