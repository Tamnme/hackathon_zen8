from flask import jsonify, request
from app.api import api_bp
from app.models import db
from app.models.summary_history import SummaryHistory, StatusEnum
from app.models.app_setting import AppSetting
from datetime import datetime

@api_bp.route('/summary/trigger', methods=['POST'])
def trigger_summary():
    """Trigger a summary process."""
    data = request.json
    
    if not data or 'email' not in data:
        return jsonify({"error": "Email is a required field"}), 400
    
    email = data['email']
    
    # Verify the user has app settings
    app_setting = AppSetting.query.get(email)
    if not app_setting:
        return jsonify({"error": "No app settings found for this email"}), 404
    
    # Create a summary history record with 'start' status
    new_summary = SummaryHistory(
        email=email,
        status=StatusEnum.START,
        start_time=datetime.utcnow(),
        channels=data.get('channels'),
    )
    
    db.session.add(new_summary)
    db.session.commit()
    
    # In a real implementation, this would trigger a background task
    # For demonstration purposes, we'll just return the created summary history
    
    return jsonify({
        "message": "Summary process triggered",
        "trigger_id": new_summary.id,
        "summary": new_summary.to_dict()
    }), 202 