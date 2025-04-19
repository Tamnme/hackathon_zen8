from flask import jsonify, request
from app.api import api_bp
from app.models import db
from app.models.trigger_setting import TriggerSetting
from datetime import date
import json

@api_bp.route('/trigger-settings', methods=['GET'])
def get_trigger_settings():
    """Get trigger settings for an email. Creates default settings if none exist."""
    email = request.args.get('email')
    
    if not email:
        return jsonify({"error": "Email parameter is required"}), 400
    
    settings = TriggerSetting.query.filter_by(email=email).all()
    
    # If no settings exist for this email, create default trigger settings
    if not settings:
        default_setting = TriggerSetting(
            email=email,
            channels=[],  # Empty array as default
            start_date=None,
            end_date=None
        )
        
        db.session.add(default_setting)
        db.session.commit()
        
        return jsonify([default_setting.to_dict()]), 200
    
    return jsonify([setting.to_dict() for setting in settings]), 200

@api_bp.route('/trigger-settings', methods=['POST'])
def create_trigger_setting():
    """Create trigger settings."""
    data = request.json
    
    if not data or 'email' not in data:
        return jsonify({"error": "Email is a required field"}), 400
    
    new_setting = TriggerSetting(
        email=data['email'],
        channels=data.get('channels', []),
        start_date=date.fromisoformat(data['start_date']) if 'start_date' in data and data['start_date'] else None,
        end_date=date.fromisoformat(data['end_date']) if 'end_date' in data and data['end_date'] else None
    )
    
    db.session.add(new_setting)
    db.session.commit()
    
    return jsonify(new_setting.to_dict()), 201

@api_bp.route('/trigger-settings/<int:setting_id>', methods=['PUT'])
def update_trigger_setting(setting_id):
    """Update trigger settings."""
    data = request.json
    
    if not data:
        return jsonify({"error": "No data provided"}), 400
        
    setting = TriggerSetting.query.get(setting_id)
    
    if not setting:
        return jsonify({"error": "Trigger setting not found"}), 404
    
    # Update fields
    if 'channels' in data:
        setting.channels = data['channels']
    if 'start_date' in data and data['start_date']:
        setting.start_date = date.fromisoformat(data['start_date'])
    if 'end_date' in data and data['end_date']:
        setting.end_date = date.fromisoformat(data['end_date'])
    
    db.session.commit()
    
    return jsonify(setting.to_dict()), 200 