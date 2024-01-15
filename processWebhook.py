# /path/to/your/flask_app.py
import flask
import openai
from flask import Flask, request, make_response
from flask_cors import CORS, cross_origin
import os
from openai import OpenAI

app = Flask(__name__)
cors = CORS(app)

@app.route('/home', methods=['POST', 'OPTIONS'])
@cross_origin(origin='https://admin.revenuehunt.com', headers=['Content-Type', 'api_key'])
def home():
    if request.method == 'OPTIONS':
        # Create a response for the preflight request with explicit headers
        response = make_response()
        response.headers["Access-Control-Allow-Origin"] = "https://admin.revenuehunt.com"
        response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, api_key"
        return response

    # Usage example
    os.environ["PYDEVD_WARN_EVALUATION_TIMEOUT"] = "10000"  # Timeout in milliseconds
    data = flask.request.json

    if not data:
        return "Invalid JSON data", 400

    # Check if the 'text' parameter is present in the JSON data
    if 'text' not in data:
        return "Missing 'text' parameter in JSON data", 400

    prompt = data.get('text', '')

    callback = flask.request.args.get('callback', 'jsonpCallback')
    api_key = os.environ.get('OPENAI_API_KEY')  # Retrieve API key from environment variable

    if not prompt:
        return f'{{"response": "Waiting"}}'

    try:
        openai.api_key = api_key
        
        client = OpenAI(api_key=api_key)

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="gpt-3.5-turbo",
        )

        return chat_completion.choices[0].message.content

    except Exception as e:
        return f'{{"response": "Error: {str(e)}"}}'

if __name__ == "__main__":
    app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'DefaultSecretKey')
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
