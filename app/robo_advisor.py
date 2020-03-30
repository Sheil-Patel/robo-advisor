#app/robo_advisor.py

import csv
import requests
import json
import os
from dotenv import load_dotenv
from datetime import datetime
from twilio.rest import Client


#Import Data from API--------------------------
    
load_dotenv() #> loads contents of the .env file into the script's environment
api_key = os.environ.get("ALPHAVANTAGE_API_KEY")
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID", "OOPS, please specify env var called 'TWILIO_ACCOUNT_SID'")
TWILIO_AUTH_TOKEN  = os.environ.get("TWILIO_AUTH_TOKEN", "OOPS, please specify env var called 'TWILIO_AUTH_TOKEN'")
SENDER_SMS  = os.environ.get("SENDER_SMS", "OOPS, please specify env var called 'SENDER_SMS'")
RECIPIENT_SMS  = os.environ.get("RECIPIENT_SMS", "OOPS, please specify env var called 'RECIPIENT_SMS'")
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

def to_usd(my_price):
    """
    Takes a float or int and converts it into a string showing a proper numerical dollar amount.

    Params:
        my_price (numeric, like int or float) the number will be converted to USD format

    Examples:
        to_usd(4.50) == "$4.50" #Adds the Dollaer
        to_usd(4.5) == "$4.50" #Has two decimal places
        to_usd(4.5555555) == "$4.56" #should round to two decimal places
        to_usd(123456789.5555) == "$123,456,789.56" # should display thousand separators
    """
    return f"${my_price:,.2f}" #> $12,000.71
def write_to_csv(dates, csv_file_path):

    """
    Takes a list of dictionaries and a csv file path and writes the list into the csv

    Params:
        dates (list of dictionaries) and csv_file_path (file path name in OS language)

    Examples:
        write_to_csv(dates, csv_file_path)
    """
    # rows should be a list of dictionaries
    # csv_filepath should be a string filepath pointing to where the data should be written

    csv_headers = ["timestamp", "open", "high", "low", "close", "volume"]

    with open(csv_file_path, "w") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=csv_headers)
        writer.writeheader() # uses fieldnames set above
        for datez in dates:
            writer.writerow(datez)

    return True
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
def get_latest_close(dates):
    latest_close = dates[0]["close"]
    return latest_close
def get_yesterday_close(dates):
    yesterday_close = dates[1]["close"]
    return yesterday_close
def get_last_refreshed(parsed_response):
    last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]
    return last_refreshed
def get_recent_high(dates):
    high_prices = []
    for datez in dates:
        high_price = datez["high"]
        high_prices.append(float(high_price))
        
    
    recent_high = max(high_prices)
    
    return recent_high
    #-----------------------------
def get_recent_low(dates):
    low_prices = []
    for datez in dates:
        low_price = datez["low"]
        low_prices.append(float(low_price))
    recent_low = min(low_prices)
    return recent_low
def get_52_week_high(dates):
    #52 week high
    weeks_high = []
    x = 0
    for datez in dates:
        week_high = datez["high"]
        weeks_high.append(float(week_high))
        x += 1
        if x == 360:
            break
    recent_52high = max(weeks_high)
    return recent_52high
def get_52_week_low(dates):
    weeks_low = []
    x = 0
    for datez in dates:
        week_low = datez["low"]
        weeks_low.append(float(week_low))
        x += 1
        if x == 360:
            break
    recent_52low = min(weeks_low)
    return recent_52low

if __name__ == "__main__":
    #Current Time---------------
    today = datetime.today()
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    d3 = today.strftime("%m/%d/%y")
    #------------------------------------
    
    #
    # INFO INPUTS
    #
    
    #Writing to CSV-----------------------------------------
    
   
    csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", "prices.csv")
    
    
    #Function Calls-------------------------------------------------------
    symbol = input("Please input a stock ticker (e.g. MSFT)")
    ticker = symbol.upper()
    parsed_response = get_response(ticker)
    dates = transform_response(parsed_response)
    latest_close = get_latest_close(dates)
    yesterday_close = get_yesterday_close(dates)
    last_refreshed = get_last_refreshed(parsed_response)
    recent_high = get_recent_high(dates)
    recent_low = get_recent_low(dates)
    recent_52high = get_52_week_high(dates)
    recent_52low = get_52_week_low(dates)
    write_to_csv(dates, csv_file_path)
    breakpoint()
    #---------------------------------------------------
    
    #------------------------------
    
 
    # ---------------------------------------
    

    # ----------------------------------------
    
    #Recent High Price(Maximum of all the high prices) &
    #Recent Low Price(Minimum of all the low prices)-----
    
    #Reccomendation-----------------------------------
    if (float(latest_close) > (recent_high * 1.15)):
        reccomendation = "SELL!"
        reccomendation_reason = f"The latest closing price({to_usd(float(latest_close))}) is more than 15 percent above the recent high({to_usd(float(recent_high))}). This is an opportunistic time to SELL " 
    elif (float(latest_close) < (recent_low * 1.15)):
        reccomendation = "BUY!"
        reccomendation_reason = f"The latest closing price({to_usd(float(latest_close))}) is less than 15 percent above the recent low({to_usd(float(recent_low))}). This is an opportunistic time to BUY"
    elif True:
        reccomendation = "HOLD!"
        reccomendation_reason = "Does not satisfy requirements for BUY or SELL which were, respectively, the latest closing price is more than 15 percent above the recent high and the latest closing price is less than 15 percent above the recent low. There is no clear indication of any clear upside to selling or buying, so the best course of action is to HOLD"
    
    
    
    #-------------------------------------------------
 
    #----------------------------------------------------------
    
    
    
    
    #
    # INFO OUTPUTS
    #
    
    
    
    
    #Program Outputs
    print("-------------------------")
    print(f"SELECTED SYMBOL: {symbol}")#
    print("-------------------------")
    print("REQUESTING STOCK MARKET DATA...")
    print("REQUEST OCCURED ON: " + d3 + " at " + current_time)#
    print("-------------------------")
    print(f"LATEST DAY: {last_refreshed}")#
    print(f"LATEST CLOSE: {to_usd(float(latest_close))}")
    print(f"RECENT HIGH: {to_usd(float(recent_high))}")
    print(f"RECENT LOW:{to_usd(float(recent_low))}")
    print(f"52 WEEK HIGH:{to_usd(float(recent_52high))}")
    print(f"52 WEEK LOW:{to_usd(float(recent_52low))}")
    print("-------------------------")
    print(f"RECOMMENDATION: {reccomendation}")
    print(f"RECOMMENDATION REASON: {reccomendation_reason}")
    print("-------------------------")
    print("HAPPY INVESTING!")
    print("-------------------------")
    
    # Text Message output
    sendit = False
    if (float(latest_close)/float(yesterday_close) >= 1.05):
        content = f"ALERT: The price of {symbol.upper()} has increased by more than 5% within the past day"
        sendit = True
    if (float(latest_close)/float(yesterday_close) <= .95):
        content = f"ALERT: The price of {symbol.upper()} has decreased by more than 5% within the past day"
        sendit = True
    if sendit == True:
        message = client.messages.create(to=RECIPIENT_SMS, from_=SENDER_SMS, body=content)



