from flask import jsonify, request, current_app
from app.api import api_bp
from app.models import db
from app.models.summary_history import SummaryHistory, StatusEnum
from app.models.app_setting import AppSetting
from datetime import datetime
from app.services.add_content_to_database import create_notion_summary
import json
import pip._vendor.requests  # Ensure requests is imported
from flask import copy_current_request_context

# 192.168.1.49:11434

@api_bp.route('/summary/latest', methods=['GET'])
def get_latest_summary_history():
    """Get the latest summary history for an email."""
    email = request.args.get('email')
    
    if not email:
        return jsonify({"error": "Email parameter is required"}), 400
    
    latest_history = SummaryHistory.query.filter_by(email=email) \
                                    .order_by(SummaryHistory.end_time.desc()) \
                                    .first() or \
                    SummaryHistory.query.filter_by(email=email) \
                                    .order_by(SummaryHistory.start_time.desc()) \
                                    .first()
    print("Latest history: ", latest_history)
    
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
    
    # Create a summary history record with 'start' status
    new_summary = SummaryHistory(
        email=email,
        status=StatusEnum.START,
        start_time=datetime.utcnow(),
        channels=data.get('channels'),
        notion_page_url=""
    )
    
    db.session.add(new_summary)
    db.session.commit()

    # Extract only the necessary values from app_setting instead of passing the ORM object
    app_setting_data = {
        'notion_secret': app_setting.notion_secret,
        'notion_page_id': app_setting.notion_page_id
    }
    
    # Get the summary ID to use in the background thread
    summary_id = new_summary.id

    # Wrap process_summary with the current request context
    @copy_current_request_context
    def run_process_summary(data, app_setting_data, summary_id):
        process_summary(data, app_setting_data, summary_id)

    # Start processing in background thread
    from threading import Thread
    thread = Thread(target=run_process_summary, args=(data, app_setting_data, summary_id))
    thread.daemon = True  # Make thread daemon so it doesn't block app shutdown
    thread.start()
    print("Thread started")

    return jsonify({
        "message": "Summary process triggered successfully",
        "trigger_id": new_summary.id,
        "summary": new_summary.to_dict()
    }), 202

def process_summary(data, app_setting_data, summary_id):
    """Process summary in background thread"""
    print("Processing summary: ", summary_id)
    
    # Get the summary record from the database using the ID
    summary_history = SummaryHistory.query.get(summary_id)
    if not summary_history:
        print("Error: Summary history not found")
        return
        
    new_summary = SummaryHistory(
        email=summary_history.email,
        status=summary_history.status,
        start_time=summary_history.start_time,
        channels=summary_history.channels,
        notion_page_url=""
    )
    try:
        notion_api_key = app_setting_data['notion_secret']
        notion_database_id = app_setting_data['notion_page_id']

        if not notion_api_key or not notion_database_id:
            new_summary.status = StatusEnum.FAILED
            new_summary.end_time = datetime.utcnow()
            db.session.add(new_summary)
            db.session.commit()
            print("Error: ", "Missing app setting")
            return

        # Get title and content from request data
        title = data.get("title", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        content = '''# Welcome to Notion API Demo
        
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
 
Feel free to explore and customize this template for your needs!'''

        # result = post_chat_request("Hi");
        # print("Result: ", result)
        # if result.get('error'):
        #     new_summary.status = StatusEnum.FAILED
        #     new_summary.end_time = datetime.utcnow()
        #     print("Error: ", result.get('error'))
        #     db.session.add(new_summary)
        #     db.session.commit()
        #     return 
        # print("pass chat request")
        # Create summary in Notion
        notion_result = create_notion_summary(
            api_key=notion_api_key,
            database_id=notion_database_id,
            page_title=title,
            page_content=content,
            time=datetime.utcnow()
        )

        if not notion_result.get('success'):
            new_summary.status = StatusEnum.FAILED
            new_summary.end_time = datetime.utcnow()
            print("Error: ", "Notion failed")
            db.session.add(new_summary)
            db.session.commit()
            return

        new_summary.status = StatusEnum.SUCCESS
        new_summary.end_time = datetime.utcnow()
        new_summary.notion_page_url = notion_result.get('page_url')
        print("Notion page URL: ", notion_result.get('page_url'))
        db.session.add(new_summary)
        db.session.commit()

    except Exception as e:
        new_summary.status = StatusEnum.FAILED
        new_summary.end_time = datetime.utcnow()
        print("Error: ", e)
        db.session.add(new_summary)
        db.session.commit()

def post_chat_request(user_content: str) -> dict:
    """
    Post chat request to local Ollama API endpoint.
    
    Args:
        user_content: The user content to process
        
    Returns:
        dict: The response from the API containing the generated summary
    """
    try:
        # Generate the request payload
        payload = generate_request_payload(user_content)
        
        # Make POST request to Ollama API
        response = pip._vendor.requests.post(
            'http://192.168.1.49:11434/api/chat',
            data=payload.encode('utf-8'),
            headers={'Content-Type': 'application/json;'},
        )
        
        # Check if request was successful
        response.raise_for_status()
        
        # Parse and return JSON response
        return response.json()
        
    except pip._vendor.requests.RequestException as e:
        current_app.logger.error(f"Error making request to API: {str(e)}")
        return {"error": str(e)}
    except json.JSONDecodeError as e:
        current_app.logger.error(f"Error decoding JSON response: {str(e)}")
        return {"error": "Invalid JSON response"}
    except Exception as e:
        current_app.logger.error(f"Unexpected error in post_chat_request: {str(e)}")
        return {"error": str(e)}

def generate_request_payload(user_content: str) -> str:
    template = {
        "model": "mistral-nemo",
        "stream": False,
        "messages": [
            {
                "role": "system",
                "content": """Bạn là một AI trợ lý làm nhiệm vụ phân tích tin nhắn từ một đoạn JSON.
Nhiệm vụ của bạn là:
Mục tiêu:
Trích xuất và tóm tắt các công việc, trách nhiệm, hành động đã thực hiện hoặc được giao cho một người dùng cụ thể dựa trên nội dung các tin nhắn.
Tên người dùng mục tiêu: Chỉ rõ tên người dùng bạn muốn tôi tóm tắt công việc.
Xử lý nội bộ:
AI sẽ phân tích các tin nhắn, xác định những tin liên quan trực tiếp đến người dùng mục tiêu (do người dùng gửi, hoặc đề cập/giao việc cho người dùng đó) và tổng hợp các điểm công việc từ đó.
Đầu ra mong muốn:
Chỉ cung cấp bản tóm tắt công việc cho người dùng mục tiêu. 
Markdown
## Các nội dung Chính [Của Người Dùng]
- [ ] Mô tả tính năng chính 1 (nếu có, công việc đang làm)
- [x] Mô tả tính năng chính 2 (nếu có, công việc đã xong)
- ...

### Danh Sách Công Việc:
- [ ] Mô tả công việc cụ thể 1 (đang làm)
- [x] Mô tả công việc cụ thể 2 (đã xong/đã xử lý)

Sử dụng [ ] để đánh dấu công việc đang thực hiện hoặc chưa hoàn thành dựa trên ngữ cảnh tin nhắn.
Sử dụng [x] để đánh dấu công việc đã hoàn thành hoặc đã có hành động xử lý rõ ràng được đề cập trong tin nhắn."""
            },
            {
                "role": "user",
                "content": f"Dưới đây là một danh sách tin nhắn và trình bày kết quả ở dạng markdown. Nếu không có tin nào phù hợp thì trả lời: Không tìm thấy tin nhắn nào liên quan:\n{user_content}"
            }
        ]
    }
    return json.dumps(template, ensure_ascii=False, indent=2)