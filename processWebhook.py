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

    # Extract the API key from the query parameter 'api_key'
    api_key = flask.request.args.get('api_key', '')

    if not prompt:
        return f'{callback}("Waiting");'

    try:
        openai.api_key = api_key  # Use the extracted API key
        response = openai.Completion.create(model="text-davinci-003", prompt=prompt, max_tokens=1000)
        if 'choices' in response and len(response.choices) > 0:
            response_text = response.choices[0].text.replace('"', '\\"')  # Escape double quotes in the response
            # Clean the response text from '?' and '\n'
            cleaned_response_text = response_text.replace('?', '').replace('\n', '')
            return f'{callback}({{"response": "{cleaned_response_text}"}});'
        else:
            return f'{callback}({{"response": ""}});'  # Return an empty response if there is no data
    except Exception as e:
        return f'{callback}({{"response": "Error: {str(e)}"}});'

if __name__ == "__main__":
    app.secret_key = 'ItIsASecret'
    # app.debug = True
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
