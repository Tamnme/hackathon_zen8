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

    # First try to get latest by end_time
    latest_by_end_time = SummaryHistory.query.filter_by(email=email) \
                                    .order_by(SummaryHistory.end_time.desc()) \
                                    .first()
    
    # Then try to get latest by start_time
    latest_by_start_time = SummaryHistory.query.filter_by(email=email) \
                                    .order_by(SummaryHistory.start_time.desc()) \
                                    .first()
    
    # Compare timestamps and return the most recent one
    if latest_by_end_time and latest_by_start_time:
        end_time = latest_by_end_time.end_time or datetime.min
        start_time = latest_by_start_time.start_time or datetime.min
        return jsonify(latest_by_start_time.to_dict() if start_time > end_time 
                      else latest_by_end_time.to_dict()), 200
    elif latest_by_end_time:
        return jsonify(latest_by_end_time.to_dict()), 200
    elif latest_by_start_time:
        return jsonify(latest_by_start_time.to_dict()), 200
    
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
        'notion_page_id': app_setting.notion_page_id,
        'slack_token': app_setting.slack_token
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


def fetch_slack_messages(token, channels, limit, oldest, latest):
    url = "https://slack-crawl.vercel.app/crawl"
    params = {
        "token": token,
        "channels": channels,
        "limit": limit,
        "oldest": oldest,
        "lastest": latest
    }

    try:
        response = pip._vendor.requests.get(url, params=params)
        response.raise_for_status()  # Raise an error for bad HTTP status
        return response.json()
    except pip._vendor.requests.RequestException as e:
        print(f"Error fetching Slack messages: {e}")
        return None

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
        slack_token = app_setting_data['slack_token']

        if not notion_api_key or not notion_database_id or not slack_token:
            new_summary.status = StatusEnum.FAILED
            new_summary.end_time = datetime.utcnow()
            db.session.add(new_summary)
            db.session.commit()
            print("Error: ", "Missing app setting")
            return
        
        slack_messages = fetch_slack_messages(slack_token, "C08MUTY5MN1", 10, 1744473355, 1745078155)
        if not slack_messages:
            new_summary.status = StatusEnum.FAILED
            new_summary.end_time = datetime.utcnow()
            db.session.add(new_summary)
            db.session.commit()
            print("Error: ", "Slack messages not found")
            return

        # Get title and content from request data
        title = data.get("title", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        content = slack_messages
        print("Content: ", slack_messages)

        result = send_analysis_request(content);
        content = result['message']['content']
        print("Result: ", result)
        if is_markdown_empty(content) or result.get('error'):
            new_summary.status = StatusEnum.FAILED
            new_summary.end_time = datetime.utcnow()
            print("Error: markdown empty or chat request failed ", result.get('error'))
            db.session.add(new_summary)
            db.session.commit()
            return 
        print("pass chat request")

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
    Post chat request to API endpoint.
    
    Args:
        user_content: The user content to process
        
    Returns:
        dict: The response from the API containing the generated summary
    """
    try:
        # Generate the request payload
        payload = generate_request_payload(user_content)
        print("Payload: ", payload)
        # Make POST request to Ollama API
        response = pip._vendor.requests.post(
            'http://18.142.243.64:5000/analyze_messages',
            data=payload.encode('utf-8'),
            headers={'Content-Type': 'application/json;'},
        )
        
        # Check if request was successful
        response.raise_for_status()
        
        # Parse and return JSON response
        return response.json()
        
    except pip._vendor.requests.RequestException as e:
        current_app.logger.error(f"Error making request to API: {str(e)}")
        return {"error": str(e.response.text)}
    except json.JSONDecodeError as e:
        current_app.logger.error(f"Error decoding JSON response: {str(e)}")
        return {"error": "Invalid JSON response"}
    except Exception as e:
        current_app.logger.error(f"Unexpected error in post_chat_request: {str(e)}")
        return {"error Unexpected": str(e)}
import re

def is_markdown_empty(content: str) -> bool:
    """
    Check if content contains any markdown formatted content.
    
    Args:
        content: The string content to check
        
    Returns:
        bool: True if no markdown content found, False otherwise
    """
    # Check for common markdown patterns
    markdown_patterns = [
        r'#+ .*',           # Headers
        r'\[[ x]\]',        # Task lists
        r'- .*',            # Unordered lists
        r'\d+\. .*',        # Ordered lists
        r'\*\*.*\*\*',      # Bold text
        r'`.*`',            # Code blocks
        r'\[.*\]\(.*\)',    # Links
        r'\|.*\|'           # Tables
    ]
    
    # Strip whitespace
    content = content.strip()
    if not content:
        return True
        
    # Check each pattern
    for pattern in markdown_patterns:
        if re.search(pattern, content):
            return False
            
    return True

# --- Configuration ---
# Replace with your EC2 instance's public IP address and the correct port (5000)
EC2_PUBLIC_IP = "18.142.243.64" # !! IMPORTANT: Replace with your actual IP !!
PORT = 5000
ENDPOINT = "/analyze_messages"

# Construct the base URL (kept outside the function as it's likely constant)
BASE_URL = f"http://{EC2_PUBLIC_IP}:{PORT}{ENDPOINT}"

def send_analysis_request(payload: dict):
    """
    Sends an analysis request to the EC2 application with the given payload.

    Args:
        payload: A dictionary containing the request body data
                 (e.g., {"target_user_name": "...", "messages_data": {...}}).

    Returns:
        The JSON response body as a Python dictionary if successful.
        Returns None or the error response body if an error occurs.
    """
    print(f"Sending request to: {BASE_URL}")
    print(f"Payload: {json.dumps(payload, indent=2)}") # Print payload being sent

    try:
        # requests.post with the json parameter automatically sets Content-Type to application/json
        response = pip._vendor.requests.post(BASE_URL, json=generate_request_payload(payload))

        # Raise an exception for bad status codes (4xx or 5xx)
        response.raise_for_status()

        # Return the JSON response body
        print(f"\nStatus Code: {response.status_code}")
        print("Response Body:")
        response_json = response.json()
        print(json.dumps(response_json, indent=2))
        return response_json

    except pip._vendor.requests.exceptions.RequestException as e:
        print(f"\nAn error occurred during the request: {e}")
        # Print and return the error response body if available
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response status code: {e.response.status_code}")
            try:
                error_response_json = e.response.json()
                print("Error Response body:")
                print(json.dumps(error_response_json, indent=2))
                return error_response_json # Return the error body
            except json.JSONDecodeError:
                 print("Non-JSON error response body:")
                 print(e.response.text)
                 return {"error": f"Request failed, non-JSON response: {e.response.text}"} # Return a structured error
        return {"error": f"Request failed: {e}"} # Return a structured error

def extract_text_from_dict(data):
    output = []
    for key, value in data.items():
        if isinstance(value, list):
            for item in value:
                output.append(item)
    return '\n'.join(output)

def generate_request_payload(user_content: str) -> str:
#     template = {
#        "prompt": f"""Bạn là một AI trợ lý làm nhiệm vụ phân tích tin nhắn từ một đoạn JSON.
# Nhiệm vụ của bạn là:
# Mục tiêu:
# Trích xuất và tóm tắt các công việc, trách nhiệm, hành động đã thực hiện hoặc được giao cho một người dùng cụ thể dựa trên nội dung các tin nhắn.
# Tên người dùng mục tiêu: Chỉ rõ tên người dùng bạn muốn tôi tóm tắt công việc.
# Xử lý nội bộ:
# AI sẽ phân tích các tin nhắn, xác định những tin liên quan trực tiếp đến người dùng mục tiêu (do người dùng gửi, hoặc đề cập/giao việc cho người dùng đó) và tổng hợp các điểm công việc từ đó.
# Đầu ra mong muốn:
# Chỉ cung cấp bản tóm tắt công việc cho người dùng mục tiêu. 
# Markdown
# ## Các nội dung Chính [Của Người Dùng]
# - [ ] Mô tả tính năng chính 1 (nếu có, công việc đang làm)
# - [x] Mô tả tính năng chính 2 (nếu có, công việc đã xong)
# - ...

# ### Danh Sách Công Việc:
# - [ ] Mô tả công việc cụ thể 1 (đang làm)
# - [x] Mô tả công việc cụ thể 2 (đã xong/đã xử lý)

# Sử dụng [ ] để đánh dấu công việc đang thực hiện hoặc chưa hoàn thành dựa trên ngữ cảnh tin nhắn.
# Sử dụng [x] để đánh dấu công việc đã hoàn thành hoặc đã có hành động xử lý rõ ràng được đề cập trong tin nhắn.
# Dưới đây là một danh sách tin nhắn và trình bày kết quả ở dạng markdown. Nếu không có tin nào phù hợp thì trả lời: Không tìm thấy tin nhắn nào liên quan:\n{extract_text_from_dict(user_content)}"""
    # }
    template =     {
      "target_user_name": "User name",
      "messages_data": user_content
    }
    return json.dumps(template, ensure_ascii=False, indent=2)