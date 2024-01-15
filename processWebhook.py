import flask
import os
import openai
from flask_cors import CORS

app = flask.Flask(__name__)
CORS(app)

@app.route('/')
@app.route('/home', methods=['POST'])
def home():
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
        response = openai.Completion.create(model="gpt-4-1106-preview", prompt=prompt, max_tokens=1000)
        if 'choices' in response and len(response.choices) > 0:
            response_text = response.choices[0].text.replace('"', '\\"')
            cleaned_response_text = response_text.replace('?', '').replace('\n', '')
            return f'{{"response": "{cleaned_response_text}"}}'
        else:
            return '{"response": ""}'
    except Exception as e:
        return f'{{"response": "Error: {str(e)}"}}'

if __name__ == "__main__":
    app.secret_key = 'ItIsASecret'
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
