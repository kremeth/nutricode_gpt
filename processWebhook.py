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
        return "Waiting"  # Return "Waiting" if the 'text' query parameter is not provided.
    
    openai.api_key = "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"
    response = openai.Completion.create(model="text-davinci-003", prompt=prompt, max_tokens=1000)
    return response.choices[0].text

if __name__ == "__main__":
    app.secret_key = 'ItIsASecret'
    # app.debug = True
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))