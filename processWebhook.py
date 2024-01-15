from flask import Flask, request, jsonify
import os
import openai
from flask_cors import CORS
from openai import OpenAI

app = Flask(__name__)

# Setting up CORS for all domains. Modify accordingly if you want to restrict to certain domains.
CORS(app)

@app.route('/home', methods=['POST'])
def home():
    # Ensuring that the content type is application/json
    if not request.is_json:
        return jsonify({"response": "Invalid content type, must be application/json"}), 400

    data = request.get_json()

    # Validating 'text' parameter in JSON data
    if 'text' not in data:
        return jsonify({"response": "Missing 'text' parameter in JSON data"}), 400

    prompt = data['text']

    # API key handling
    api_key = request.args.get('api_key', '')
    if not api_key:
        return jsonify({"response": "Missing API key"}), 403

    try:
        openai.api_key = api_key
        client = OpenAI(api_key=api_key)

        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="gpt-3.5-turbo",
        )
        
        if 'choices' in response and len(response.choices) > 0:
            response_text = response.choices[0].text.strip().replace('"', '\\"')
            return jsonify({"response": response_text})
        else:
            return jsonify({"response": "No response from OpenAI"})

    except Exception as e:
        return jsonify({"response": f"Error: {str(e)}"}), 500

if __name__ == "__main__":
    app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'ItIsASecret')
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
