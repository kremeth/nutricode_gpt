import flask
import os
import openai
from flask_cors import CORS, cross_origin
from openai import OpenAI
from flask import request
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import re
from datetime import datetime
import pytz

app = flask.Flask(__name__)
CORS(app)

@app.route('/home', methods=['POST', 'OPTIONS'])
@cross_origin(origin='https://admin.revenuehunt.com', headers=['Content-Type', 'api_key'])
def home():


    row = {
        'Email': '',
        'Time': '',
        'Date': '',
        'Supplements': '',
        'GPT Response': '',
        'Question 5': '',
        'Question 6': '',
        'Question 8': '',
        'Question 9': '',
        'Question 10': '',
        'Question 11': '',
        'Question 12': '',
        'Question 13': '',
        'Question 14': '',
        'Question 15': '',
        'Question 16': '',
        'Question 17': '',
        'Question 18': '',
        'Question 20': '',
        'Question 21': '',
        'Question 22': '',
        'Question 23': '',
        'Question 25': '',
        'Question 26': '',
        'Question 28': '',
        'Question 29': '',
        'Question 31': '',
        'Question 32': '',
        'Question 33': '',
        'Question 34': '',
        'Question 35': '',
        'Question 36': '',
        'Question 38': '',
        'Question 39': '',
        'Question 40': '',
        'Question 41': '',
        'Question 42': '',
        'Question 43': '',
        'Question 44': '',
        'Question 46': '',
        'Question 47': '',
        'Question 48': '',
        'Question 49': '',
        'Question 50': '',
        'Question 52': '',
        'Question 53': '',
        'Question 54': '',
        'Question 55': '',
        'Question 57': '',
        'Question 58': '',
        'Question 60': '',
        'Question 61': ''

    }
            # The ID of the spreadsheet.
    SPREADSHEET_ID = '1Fo37uAlkPAFJnLAnDxbHfb-HvzZYXjTtNOuKEyV5DCI'

    # The range of the cells to access.
    RANGE_NAME = 'Sheet1'  # Only sheet name is required for appending

    # The path to the service account key.
    SERVICE_ACCOUNT_FILE = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

    # Define the scopes (change to allow writing)
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

    # Authenticate and construct service.
    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=creds)
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
        response_text = response.choices[0].message.content
        response_text = response_text.replace('"', '\\"')
        response_text = response_text.replace('?', '').replace('\n', '')
        # Split the prompt into segments containing the question and the answer
        q_and_as = prompt.split('\n\n')
        print(q_and_as[4)
        
        # Split the q_and_as into a dictionary, where the key is the question and the value is the answer
        split_qa = [re.split(r'\n Selected Answer \d+:', val) for val in q_and_as[1:-1]]

        # Tupled pairs of questions and answers
        pairs = [(val[0].split(':')[0], ''.join(val[1:])) for val in split_qa]
        # Assign the values to each one of the keys in the dictionary
        for val in pairs:
            if val[0] == 'Question 63':
                row['Email'] = val[1]
            else:
                row[val[0]] = val[1]


        # Add which supplements it recommends 
        row['Supplements'] = q_and_as[-1].split('recommendation ')[-1].split(' .')[0]

        response_text = 'test'

        # Add the gpt response
        row['GPT Response'] = response_text


        # Add the time
        # Create a timezone object for Singapore
        singapore_timezone = pytz.timezone('Asia/Singapore')

        # Get the current time in Singapore
        singapore_time = datetime.now(singapore_timezone)

        # Get the time
        row['Time'] = singapore_time.strftime('%H:%M:%S')

        # Get the date
        row['Date'] = singapore_time.strftime('%d/%m/%Y')



        values = [list(row.values())]  # API expects a list of lists

        # How the input data should be interpreted.
        value_input_option = 'RAW'  # or 'USER_ENTERED'

        # How the input data should be inserted.
        insert_data_option = 'INSERT_ROWS'  # or 'OVERWRITE'

        # Prepare the request
        r_sheets = service.spreadsheets().values().append(
            spreadsheetId=SPREADSHEET_ID, 
            range=RANGE_NAME, 
            valueInputOption=value_input_option, 
            insertDataOption=insert_data_option, 
            body={'values': values}
        )

        r_sheets.execute()


        return f'{{"response": "{response_text}"}}'

    except Exception as e:
        return f'{{"response": "Error: {str(e)}"}}'

if __name__ == "__main__":
    app.secret_key = 'ItIsASecret'
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
