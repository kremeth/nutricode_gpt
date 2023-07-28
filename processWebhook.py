import datetime
from ebaysdk.exception import ConnectionError
from ebaysdk.finding import Connection
from datetime import datetime, timedelta
from ebaysdk.trading import Connection as Trading
from tqdm import tqdm
import itertools
import numpy as np
import pandas as pd
from ebaysdk.shopping import Connection as Shopping
import flask
import os
from ebaysdk.trading import Connection as Trading
from ebaysdk.exception import ConnectionError
# Import smtplib for the actual sending function
import smtplib

# For guessing MIME type
import mimetypes

# Import the email modules we'll need
import email
import email.mime.application
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from tqdm import tqdm
import pandas as pd
import time
import openai
import ast


app = flask.Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
    # Usage example
    os.environ["PYDEVD_WARN_EVALUATION_TIMEOUT"] = "10000"  # Timeout in milliseconds
    data = pd.read_csv('/Users/mathieukremeth/Desktop/tt.csv')
    prompt = data.iloc[0,1]
    openai.api_key = "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"
    response = openai.Completion.create(model="text-davinci-003", prompt=prompt, max_tokens=1000)
    return response.choices[0].text


if __name__ == "__main__":
    app.secret_key = 'ItIsASecret'
    # app.debug = True
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))







