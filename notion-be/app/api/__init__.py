from flask import Blueprint

api_bp = Blueprint('api', __name__, url_prefix='/api')

from app.api import summary_histories
from app.api import app_settings
from app.api import trigger_settings
from app.api import summary
<<<<<<< HEAD
from app.api import notion_validation
=======
from app.api import notion_validation
from app.api import health
>>>>>>> c720ba8e45f7550d7a328ef6e0795df02c969ea0
