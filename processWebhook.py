import flask
import os
import openai

app = flask.Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
    # Usage example
    os.environ["PYDEVD_WARN_EVALUATION_TIMEOUT"] = "10000"  # Timeout in milliseconds
    prompt = flask.request.args.get('text', '')  # Get the 'text' query parameter from the URL
    if not prompt:
        return f'{flask.request.args.get("callback", "jsonpCallback")}("Waiting");'

    try:
        openai.api_key = "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"
        response = openai.Completion.create(model="text-davinci-003", prompt=prompt, max_tokens=1000)
        if 'choices' in response and len(response.choices) > 0:
            return f'{flask.request.args.get("callback", "jsonpCallback")}({{"response": "{response.choices[0].text}"}});'
        else:
            return f'{flask.request.args.get("callback", "jsonpCallback")}("Error: Empty response from OpenAI");'
    except Exception as e:
        return f'{flask.request.args.get("callback", "jsonpCallback")}("Error: {str(e)}");'

if __name__ == "__main__":
    app.secret_key = 'ItIsASecret'
    # app.debug = True
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
