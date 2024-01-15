from flask import Flask, request, jsonify, make_response
import os
import openai
from flask_cors import CORS, cross_origin
from openai import OpenAI

app = Flask(__name__)

# Configure CORS specifically for the desired origin
CORS(app, resources={r"/home": {"origins": "https://admin.revenuehunt.com"}})

@app.route('/home', methods=['POST', 'OPTIONS'])
@cross_origin(origin='https://admin.revenuehunt.com')  # Apply CORS to this route
def home():
    if request.method == 'OPTIONS':
        # Create a response for the preflight request with explicit headers
        response = make_response()
        response.headers["Access-Control-Allow-Origin"] = "https://admin.revenuehunt.com"
        response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, api_key"
        return response

    if not request.is_json:
        return jsonify({"response": "Invalid content type, must be application/json"}), 400

    data = request.get_json()

    if 'text' not in data:
        return jsonify({"response": "Missing 'text' parameter in JSON data"}), 400

    prompt = data['text']
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
