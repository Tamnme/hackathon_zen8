import json
import os
import google.generativeai as genai
from flask import Flask, request, jsonify

app = Flask(__name__)

# Define the model you want to use
GEMINI_MODEL = 'gemini-pro' # Or your preferred Gemini model

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

@app.route('/generate', methods=['POST'])
def generate_text_with_json_only():
    """
    Endpoint to call the Gemini API with a fixed prompt and JSON data from the request body.

    Request body should be the JSON content directly:
    { ... your JSON object or array ... }
    """
    # Configure the Gemini API key
    gemini_api_key = os.environ.get("GEMINI_API_KEY")

    if not gemini_api_key:
        return jsonify({'error': 'GEMINI_API_KEY environment variable not set.'}), 500

    genai.configure(api_key=gemini_api_key)

    try:
        # Get JSON data directly from the request body
        request_data = request.get_json()

        if request_data is None:
            return jsonify({'error': 'Request body must be valid JSON.'}), 400

        # --- Combine the fixed prompt and JSON data ---
        # Convert the JSON content to a string and append it to the fixed prompt.
        try:
            json_string = json.dumps(request_data, indent=2) # Pretty print JSON in prompt
            # Construct the final prompt sent to Gemini
            combined_prompt = f"{FIXED_PROMPT}\n\n---\n\n{json_string}"
        except Exception as e:
            return jsonify({'error': f'Could not process JSON data: {str(e)}'}), 400
        # ----------------------------------------

        # Initialize the generative model
        model = genai.GenerativeModel(GEMINI_MODEL)

        # Generate content using the combined prompt
        response = model.generate_content(combined_prompt)

        # Return the response
        return jsonify({
            'input_prompt_to_gemini': combined_prompt, # Show the actual prompt sent
            'fixed_prompt_used': FIXED_PROMPT,
            'input_json_data': request_data,
            'gemini_response': response.text
        })

    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error calling Gemini API: {str(e)}')
        }

if __name__ == '__main__':
    # This is for local development. Gunicorn/other WSGI server will be used in Docker.
    app.run(host='0.0.0.0', port=5000)