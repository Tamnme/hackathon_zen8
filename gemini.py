import json
import os
import google.generativeai as genai
from flask import Flask, request, jsonify

app = Flask(__name__)

# Define the model you want to use
GEMINI_MODEL = 'gemini-2.5-flash-preview-04-17' # Or your preferred Gemini model

# Define your fixed Vietnamese instruction prompt here
FIXED_INSTRUCTION_PROMPT = """Bạn là một AI trợ lý làm nhiệm vụ phân tích tin nhắn từ một đoạn JSON.
Nhiệm vụ của bạn là:
Mục tiêu:
Trích xuất và tóm tắt các công việc, trách nhiệm, hành động đã thực hiện hoặc được giao cho một người dùng cụ thể dựa trên nội dung các tin nhắn.
Tên người dùng mục tiêu: {target_user}
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
Sử dụng [x] để đánh dấu công việc đã hoàn thành hoặc đã có hành động xử lý rõ ràng được đề cập trong tin nhắn.
Dưới đây là một danh sách tin nhắn và trình bày kết quả ở dạng markdown. Nếu không có tin nào phù hợp thì trả lời: Không tìm thấy tin nhắn nào liên quan:
""" # Note: The message data will be appended after this.

@app.route('/analyze_messages', methods=['POST']) # Changed endpoint name for clarity
def analyze_messages_with_gemini():
    """
    Endpoint to analyze messages using Gemini with a fixed instruction.

    Request body should be JSON:
    {
      "target_user_name": "Name of the user to analyze",
      "messages_data": { ... your JSON object of messages ... }
    }
    """
    # Configure the Gemini API key
    gemini_api_key = os.environ.get("GEMINI_API_KEY")

    if not gemini_api_key:
        return jsonify({'error': 'GEMINI_API_KEY environment variable not set.'}), 500

    genai.configure(api_key=gemini_api_key)

    try:
        # Get JSON data from the request body
        request_data = request.get_json()

        if not request_data:
            return jsonify({'error': 'Request body must be valid JSON.'}), 400

        target_user = request_data.get('target_user_name')
        messages_data = request_data.get('messages_data')

        if not target_user or not messages_data:
             return jsonify({'error': 'Request body must contain "target_user_name" and "messages_data".'}), 400

        # --- Combine the fixed instruction, target user, and messages data ---
        try:
            messages_json_string = json.dumps(messages_data, indent=2)
            # Format the fixed prompt with the target user name
            formatted_instruction = FIXED_INSTRUCTION_PROMPT.format(target_user=target_user)
            # Construct the final prompt sent to Gemini
            combined_prompt = f"{formatted_instruction}\n{messages_json_string}"
        except Exception as e:
            return jsonify({'error': f'Could not process input data: {str(e)}'}), 400
        # ----------------------------------------

        # Initialize the generative model
        model = genai.GenerativeModel(GEMINI_MODEL)

        # Generate content using the combined prompt
        response = model.generate_content(combined_prompt)

        # Return the response
        # Check if the response contains the "Không tìm thấy tin nhắn nào liên quan" string
        # You might want more sophisticated checking depending on expected negative responses
        if "Không tìm thấy tin nhắn nào liên quan" in response.text:
             return jsonify({
                'analysis_status': 'No relevant messages found',
                'gemini_response': response.text
             })


        return jsonify({
            'analysis_status': 'Success',
            'target_user_analyzed': target_user,
            'input_prompt_to_gemini_prefix': formatted_instruction, # Show the instruction sent
            'input_messages_data': messages_data, # Show the input messages
            'gemini_response': response.text # This should contain the Markdown summary
        })

    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return jsonify({'error': f'Error calling Gemini API: {str(e)}'}), 500


if __name__ == '__main__':
    # This is for local development. Gunicorn/other WSGI server will be used in Docker.
    app.run(host='0.0.0.0', port=5000)