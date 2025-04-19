from flask import jsonify, request
from app.api import api_bp
from app.models import db
from app.models.app_setting import AppSetting
from app.services.notion_client_manager import NotionManager
import json

@api_bp.route('/notion/validate-connection', methods=['POST'])
def validate_notion_connection():
    """
    Validate connection to Notion API using the provided credentials.
    
    Request body:
    {
        "notion_secret": "your-notion-secret-key",
        "notion_page_id": "your-notion-page-id"
    }
    
    Returns:
    {
        "success": true/false,
        "message": "Success message or error details"
    }
    """
    data = request.json
    
    if not data:
        return jsonify({"success": False, "message": "No data provided"}), 400
        
    notion_secret = data.get('notion_secret')
    notion_page_id = data.get('notion_page_id')
    
    if not notion_secret:
        return jsonify({"success": False, "message": "Notion secret key is required"}), 400
    
    if not notion_page_id:
        return jsonify({"success": False, "message": "Notion page ID is required"}), 400
    
    try:
        # Initialize the Notion manager and validate connection
        notion_manager = NotionManager(api_key=notion_secret)
        notion_manager.validate_connection()
        
        # Format and validate the page ID
        formatted_page_id = notion_manager._format_page_id(notion_page_id)
        
        return jsonify({
            "success": True,
            "message": "Successfully connected to Notion API",
            "formatted_page_id": formatted_page_id
        }), 200
    except ValueError as e:
        return jsonify({"success": False, "message": str(e)}), 400
    except Exception as e:
        return jsonify({"success": False, "message": f"Failed to connect to Notion API: {str(e)}"}), 500

@api_bp.route('/app-settings/notion', methods=['PUT'])
def update_notion_settings():
    """
    Update Notion API settings (notion_secret and notion_page_id) for a user.
    
    Request body:
    {
        "email": "user@example.com",
        "notion_secret": "your-notion-secret-key",
        "notion_page_id": "your-notion-page-id"
    }
    
    Returns updated AppSetting object
    """
    data = request.json
    
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    if 'email' not in data:
        return jsonify({"error": "Email is required"}), 400
    
    if 'notion_secret' not in data or 'notion_page_id' not in data:
        return jsonify({"error": "Both notion_secret and notion_page_id are required"}), 400
    
    email = data['email']
    notion_secret = data['notion_secret']
    notion_page_id = data['notion_page_id']
    
    # Find the app settings for this email
    setting = AppSetting.query.get(email)
    
    if not setting:
        return jsonify({"error": f"No app settings found for email: {email}"}), 404
    
    # Update Notion settings
    setting.notion_secret = notion_secret
    setting.notion_page_id = notion_page_id
    
    db.session.commit()
    
    return jsonify(setting.to_dict()), 200

@api_bp.route('/app-settings/slack', methods=['PUT'])
def update_slack_settings():
    """
    Update Slack API settings (slack_token) for a user.
    
    Request body:
    {
        "email": "user@example.com",
        "slack_token": "your-slack-token"
    }
    
    Returns updated AppSetting object
    """
    data = request.json
    
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    if 'email' not in data:
        return jsonify({"error": "Email is required"}), 400
    
    if 'slack_token' not in data:
        return jsonify({"error": "slack_token is required"}), 400
    
    email = data['email']
    slack_token = data['slack_token']
    
    # Find the app settings for this email
    setting = AppSetting.query.get(email)
    
    if not setting:
        return jsonify({"error": f"No app settings found for email: {email}"}), 404
    
    # Update Slack settings
    setting.slack_token = slack_token
    
    db.session.commit()
    
    return jsonify(setting.to_dict()), 200 