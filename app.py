from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "https://bot-frontend-psi.vercel.app"}})  # Allow CORS for the specified origin

genai.configure(api_key="AIzaSyAmPpGYto4N9vJrSpMJklZN_tNI0UJmTzo")  

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

@app.route('/ask', methods=['POST', 'OPTIONS'])
def ask_gemini():

    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': 'https://bot-frontend-psi.vercel.app',
            'Access-Control-Allow-Methods': 'POST',
            'Access-Control-Allow-Headers': 'Content-Type'
        }
        return '', 200, headers

    data = request.get_json()
    prompt = data.get('prompt', '')

    if not prompt:
        return jsonify({'error': 'Prompt is required'}), 400

    try:
        chat_session = model.start_chat(history=[])
        response = chat_session.send_message(prompt)
        answer = response.text.strip()
        return jsonify({'answer': answer}), 200, {'Access-Control-Allow-Origin': 'https://bot-frontend-psi.vercel.app'}
    except Exception as e:
        app.logger.error(f"Error: {e}")
        return jsonify({'error': str(e)}), 500, {'Access-Control-Allow-Origin': 'https://bot-frontend-psi.vercel.app'}
    
if __name__ == '__main__':
    app.run(debug=True)
