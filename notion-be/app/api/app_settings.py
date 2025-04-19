from flask import jsonify, request
from app.api import api_bp
from app.models import db
from app.models.app_setting import AppSetting
import json

@api_bp.route('/app-settings', methods=['GET'])
def get_app_setting():
    """Get app settings for an email. Creates default settings if none exist."""
    email = request.args.get('email')
    
    if not email:
        return jsonify({"error": "Email parameter is required"}), 400
    
    setting = AppSetting.query.get(email)
    
    # If no settings exist for this email, create default app settings
    if not setting:
        default_setting = AppSetting(
            email=email,
            schedule_period="daily",
            default_channels=[],  # Empty array as default
            get_notion_page="method1",
            slack_token="",
            notion_secret="",
            notion_page_id=""
        )
        
        db.session.add(default_setting)
        db.session.commit()
        
        return jsonify(default_setting.to_dict()), 200
        
    return jsonify(setting.to_dict()), 200

@api_bp.route('/app-settings', methods=['POST'])
def create_app_setting():
    """Create or update app settings."""
    data = request.json
    
    if not data or 'email' not in data:
        return jsonify({"error": "Email is a required field"}), 400
        
    # Check if settings already exist for this email
    existing = AppSetting.query.get(data['email'])
    
    if existing:
        # Update existing settings
        if 'slack_token' in data:
            existing.slack_token = data['slack_token']
        if 'notion_secret' in data:
            existing.notion_secret = data['notion_secret']
        if 'notion_page_id' in data:
            existing.notion_page_id = data['notion_page_id']
        if 'default_channels' in data:
            existing.default_channels = data['default_channels']
        
        db.session.commit()
        return jsonify(existing.to_dict()), 200
    
    # Create new settings
    new_setting = AppSetting(
        email=data['email'],
        schedule_period=data.get('schedule_period'),
        default_channels=data.get('default_channels', []),
        get_notion_page=data.get('get_notion_page'),
        slack_token=data.get('slack_token', ''),
        notion_secret=data.get('notion_secret', ''),
        notion_page_id=data.get('notion_page_id', '')
    )
    
    db.session.add(new_setting)
    db.session.commit()
    
    return jsonify(new_setting.to_dict()), 201

@api_bp.route('/app-settings/<string:email>', methods=['PUT'])
def update_app_setting(email):
    """Update app settings for an email."""
    data = request.json
    
    if not data:
        return jsonify({"error": "No data provided"}), 400
        
    setting = AppSetting.query.get(email)
    
    if not setting:
        return jsonify({"error": "App settings not found for this email"}), 404
    
    # Update fields
    if 'schedule_period' in data:
        setting.schedule_period = data['schedule_period']
    if 'default_channels' in data:
        setting.default_channels = data['default_channels']
    if 'get_notion_page' in data:
        setting.get_notion_page = data['get_notion_page']
    if 'slack_token' in data:
        setting.slack_token = data['slack_token']
    if 'notion_secret' in data:
        setting.notion_secret = data['notion_secret']
    if 'notion_page_id' in data:
        setting.notion_page_id = data['notion_page_id']
    
    db.session.commit()
    
    return jsonify(setting.to_dict()), 200 