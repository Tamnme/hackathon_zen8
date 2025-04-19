from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from app.models.summary_history import SummaryHistory
from app.models.app_setting import AppSetting
from app.models.trigger_setting import TriggerSetting 