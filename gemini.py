import json
import os
import google.generativeai as genai
from flask import Flask, jsonify

app = Flask(__name__)

# Define your fixed prompt here
FIXED_PROMPT = """
"Bạn là một trợ lý AI chuyên phân tích dữ liệu tin nhắn.
Mục tiêu:
Trích xuất và tóm tắt các công việc, trách nhiệm, hành động đã thực hiện hoặc được giao cho một người dùng cụ thể dựa trên nội dung các tin nhắn.
Đầu vào yêu cầu:
Dữ liệu tin nhắn: Dữ liệu Slack dưới dạng JSON theo cấu trúc dự kiến sau:

JSON
{
  "ID_CHANNEL": [
    "THỜI_GIAN_ĐẦY_ĐỦ | TÊN_NGƯỜI_DÙNG | NỘI_DUNG_TIN_NHẮN | LINK_TIN_NHẮN",
    "THỜI_GIAN_ĐẦY_ĐỦ | TÊN_NGƯỜI_DÙNG | NỘI_DUNG_TIN_NHẮN | LINK_TIN_NHẮN\n        | THỜI_GIAN_REPLY | TÊN_NGƯỜI_DÙNG_REPLY | NỘI_DÙNG_REPLY | LINK_REPLY",
    ...
  ]
}

Tên người dùng mục tiêu: Chỉ rõ tên người dùng bạn muốn tôi tóm tắt công việc.
Xử lý nội bộ:
AI sẽ phân tích các tin nhắn, xác định những tin liên quan trực tiếp đến người dùng mục tiêu (do người dùng gửi, hoặc đề cập/giao việc cho người dùng đó) và tổng hợp các điểm công việc từ đó.

Đầu ra mong muốn:
Chỉ cung cấp bản tóm tắt công việc cho người dùng mục tiêu. Bản tóm tắt này phải được trình bày bằng tiếng Việt theo định dạng Markdown sau:

Markdown
## Các Tính Năng Chính [Của Người Dùng]
- [ ] Mô tả tính năng chính 1 (nếu có, công việc đang làm)
- [x] Mô tả tính năng chính 2 (nếu có, công việc đã xong)
- ...

### Danh Sách Công Việc:
- [ ] Mô tả công việc cụ thể 1 (đang làm)
- [x] Mô tả công việc cụ thể 2 (đã xong/đã xử lý)
- ...
Sử dụng [ ] để đánh dấu công việc đang thực hiện hoặc chưa hoàn thành dựa trên ngữ cảnh tin nhắn.
Sử dụng [x] để đánh dấu công việc đã hoàn thành hoặc đã có hành động xử lý rõ ràng được đề cập trong tin nhắn.

Nếu không tìm thấy công việc cụ thể nào cho người dùng được chỉ định trong dữ liệu, hãy thông báo rõ điều đó.
"""

@app.route('/generate', methods=['GET'])
def generate_text():
    """
    Endpoint to call the Gemini API with a fixed prompt and return the response.
    """
    # Configure the Gemini API key
    # It's recommended to get this from a secure source like environment variables
    gemini_api_key = os.environ.get("GEMINI_API_KEY")

    if not gemini_api_key:
        return jsonify({'error': 'GEMINI_API_KEY environment variable not set.'}), 500

    genai.configure(api_key=gemini_api_key)

    try:
        # Initialize the generative model
        model = genai.GenerativeModel('gemini-pro') # Or your preferred Gemini model

        # Generate content using the fixed prompt
        response = model.generate_content(FIXED_PROMPT)

        # Return the response
        return jsonify({
            'input_prompt': FIXED_PROMPT,
            'gemini_response': response.text
        })

    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return jsonify({'error': f'Error calling Gemini API: {str(e)}'}), 500

if __name__ == '__main__':
    # This is for local development. Gunicorn/other WSGI server will be used in Docker.
    app.run(host='0.0.0.0', port=5000)