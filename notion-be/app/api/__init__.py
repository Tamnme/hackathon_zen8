from flask import Blueprint

api_bp = Blueprint('api', __name__, url_prefix='/api')

from app.api import summary_histories
from app.api import app_settings
from app.api import trigger_settings
from app.api import summary
from app.api import notion_validation