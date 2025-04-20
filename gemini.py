import json
import os
import google.generativeai as genai
from flask import Flask, request, jsonify

app = Flask(__name__)

# Define the model you want to use
GEMINI_MODEL = 'gemini-pro' # Or your preferred Gemini model

@app.route('/generate', methods=['POST'])
def generate_dynamic_text():
    """
    Endpoint to call the Gemini API with a dynamic text prompt from the request body.

    Request body should be JSON:
    {
      "prompt": "Your text prompt here..."
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

        # Get the dynamic prompt from the request body
        user_prompt = request_data.get('prompt')

        if not user_prompt:
             return jsonify({'error': 'Request body must contain a "prompt" field with text.'}), 400

        # Initialize the generative model
        model = genai.GenerativeModel(GEMINI_MODEL)

        # Generate content using *only* the dynamic prompt
        response = model.generate_content(user_prompt)

        # Return the response
        return jsonify({
            'input_prompt': user_prompt, # Show the actual prompt sent
            'gemini_response': response.text
        })

    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return jsonify({'error': f'Error calling Gemini API: {str(e)}'}), 500


if __name__ == '__main__':
    # This is for local development. Gunicorn/other WSGI server will be used in Docker.
    app.run(host='0.0.0.0', port=5000)