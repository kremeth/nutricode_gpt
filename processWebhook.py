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
    callback = flask.request.args.get('callback', 'jsonpCallback')  # Get the 'callback' query parameter from the URL

    if not prompt:
        return f'{callback}("Waiting");'

    try:
        openai.api_key = "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"
        response = openai.Completion.create(model="text-davinci-003", prompt=prompt, max_tokens=1000)
        if 'choices' in response and len(response.choices) > 0:
            response_text = response.choices[0].text.replace('"', '\\"')  # Escape double quotes in the response
            return f'{callback}({{"response": "{response_text}"}});'
        else:
            return f'{callback}("Error: Empty response from OpenAI");'
    except Exception as e:
        return f'{callback}("Error: {str(e)}");'

if __name__ == "__main__":
    app.secret_key = 'ItIsASecret'
    # app.debug = True
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
