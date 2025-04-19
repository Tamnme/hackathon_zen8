from flask import jsonify, request
from app.api import api_bp
from app.models import db
from app.models.summary_history import SummaryHistory, StatusEnum
from app.models.app_setting import AppSetting
from datetime import datetime
from app.services.add_content_to_database import create_notion_summary

@api_bp.route('/summary/latest', methods=['GET'])
def get_latest_summary_history():
    """Get the latest summary history for an email."""
    email = request.args.get('email')
    
    if not email:
        return jsonify({"error": "Email parameter is required"}), 400
    
    latest_history = SummaryHistory.query.filter_by(email=email) \
                                    .order_by(SummaryHistory.start_time.desc()) \
                                    .first()
    
    if not latest_history:
        return jsonify({"error": "No summary history found for this email"}), 404
        
    return jsonify(latest_history.to_dict()), 200

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
    notion_api_key = app_setting.notion_secret
    notion_database_id = app_setting.notion_page_id
    slack_token = app_setting.slack_token
    default_channels = app_setting.default_channels

    if not notion_api_key or not notion_database_id or not slack_token or not default_channels:
        return jsonify({"error": "Missing required app settings"}), 400
    
    # Get title and content from request data
    title = data.get('title', f"Summary for {email} - {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}")
    content = data.get('content', '''# Welcome to Notion API Demo
        
This is a demonstration of the Notion API integration with Python. Let me show you some basic Notion elements:
 
## Key Features
- ✅ Create pages and databases
- ✅ Add rich text content
- ✅ Manage tasks and projects
 
### Task List:
- [ ] Learn Notion API basics
- [ ] Build a simple integration
- [ ] Test database operations
- [ ] Share with team members
 
Feel free to explore and customize this template for your needs!''')
    
    # Create summary in Notion
    try:
        notion_result = create_notion_summary(
            api_key=notion_api_key,
            database_id=notion_database_id, 
            page_title=title,
            page_content=content,
            time=datetime.utcnow()
        )
        
        if not notion_result.get('success'):
            return jsonify({
                "error": f"Failed to create Notion page: {notion_result.get('error')}"
            }), 500
            
    except Exception as e:
        return jsonify({
            "error": f"Error creating Notion summary: {str(e)}"
        }), 500

    # Create a summary history record with 'start' status
    new_summary = SummaryHistory(
        email=email,
        status=StatusEnum.START,
        start_time=datetime.utcnow(),
        channels=data.get('channels'),
        notion_page_url=notion_result.get('page_url')
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