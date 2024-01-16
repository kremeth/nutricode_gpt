import flask
import os
import openai
from flask_cors import CORS, cross_origin
from openai import OpenAI
from flask import request

app = flask.Flask(__name__)
CORS(app)

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
    api_key = flask.request.args.get('api_key', '')

    if not prompt:
        return f'{{"response": "Waiting"}}'

    try:
        openai.api_key = api_key
        client = OpenAI(api_key=api_key)

        response = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="gpt-3.5-turbo",
        )        
        # return response.choices[0].message.content
        return f'{{"response": "{response.choices[0].message.content}"}}'

    except Exception as e:
        return f'{{"response": "Error: {str(e)}"}}'

if __name__ == "__main__":
    app.secret_key = 'ItIsASecret'
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
