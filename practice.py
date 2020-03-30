
import csv
import requests
import json
import os
from dotenv import load_dotenv
from datetime import datetime
from twilio.rest import Client
load_dotenv() #> loads contents of the .env file into the script's environment
api_key = os.environ.get("ALPHAVANTAGE_API_KEY")
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID", "OOPS, please specify env var called 'TWILIO_ACCOUNT_SID'")
TWILIO_AUTH_TOKEN  = os.environ.get("TWILIO_AUTH_TOKEN", "OOPS, please specify env var called 'TWILIO_AUTH_TOKEN'")
SENDER_SMS  = os.environ.get("SENDER_SMS", "OOPS, please specify env var called 'SENDER_SMS'")
RECIPIENT_SMS  = os.environ.get("RECIPIENT_SMS", "OOPS, please specify env var called 'RECIPIENT_SMS'")
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
def get_response(symbol):
    request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}"
    response = requests.get(request_url)
    parsed_response = json.loads(response.text)
    validation = True
    while validation == True:
        if (len(symbol) > 6):
            print("OOPS! Length of Ticker above 4 characters")
            validation = True
        elif (len(symbol) < 1):
            print("OOPS! Please input at least 1 character")
            validation = True
        elif (symbol.isalpha() == False):
            print("OOPS! You cannot have numbers in a stock ticker")
            validation = True
        elif "Error Message" in response.text:
            print("OOPS! Could not find data for that ticker(Most likely does not exist)")
            validation = True
        elif True:
            print("Gathering Stock Data...")
            validation = False
    return parsed_response
def transform_response(parsed_response):
    # parsed_response should be a dictionary representing the original JSON response
    # it should have keys: "Meta Data" and "Time Series Daily"
    tsd = parsed_response["Time Series (Daily)"]

    dates = []
    for date, daily_prices in tsd.items(): # see: https://github.com/prof-rossetti/georgetown-opim-243-201901/blob/master/notes/python/datatypes/dictionaries.md
        datez = {
            "timestamp": date,
            "open": float(daily_prices["1. open"]),
            "high": float(daily_prices["2. high"]),
            "low": float(daily_prices["3. low"]),
            "close": float(daily_prices["4. close"]),
            "volume": int(daily_prices["5. volume"])
        }
        dates.append(datez)

    return dates
symbol = input("Please input a stock ticker (e.g. MSFT)")
ticker = symbol.upper()
parsed_response = get_response(symbol)
dates = transform_response(parsed_response)
breakpoint()