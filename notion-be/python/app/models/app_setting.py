from app.models import db

class AppSetting(db.Model):
    __tablename__ = 'app_settings'
    
    email = db.Column(db.String(255), primary_key=True)
    schedule_period = db.Column(db.String(255), nullable=True)
    default_channels = db.Column(db.String(255), nullable=True)
    get_notion_page = db.Column(db.String(255), nullable=True)
    slack_token = db.Column(db.String(255), nullable=True)
    notion_secret = db.Column(db.String(255), nullable=True)
    notion_page_id = db.Column(db.String(255), nullable=True)
    
    def __repr__(self):
        return f"<AppSetting email={self.email}>"
    
    def to_dict(self):
        return {
            'email': self.email,
            'schedule_period': self.schedule_period,
            'default_channels': self.default_channels,
            'get_notion_page': self.get_notion_page,
            'slack_token': self.slack_token,
            'notion_secret': self.notion_secret,
            'notion_page_id': self.notion_page_id
        } 