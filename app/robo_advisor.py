#app/robo_advisor.py

import csv
import requests
import json
import os
from dotenv import load_dotenv
from datetime import datetime
from twilio.rest import Client


#Import Data from Alphavantage API and import .env API keys--------------------------
    
load_dotenv() #> loads contents of the .env file into the script's environment
api_key = os.environ.get("ALPHAVANTAGE_API_KEY")


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
    """
    Takes stock ticker(as a string) up to 5 letters and returns the data as a dictionary of lists for the company stock through AlphaVantage API

    Params:
        symbol (string)

    Examples:
        get_response(MSFT) #>Returns Data for Microsoft Stock
        get_response(GM) #>Returns Data for General Motors Stock
    """
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
    """
    Takes a parsed_response from the get_response() function and transforms it into a list, which is able to be used by the other functions

    Params:
        parsed_response(dictionary datatype)

    Examples:
        transform_response(parsed_response) #>Transfroms parsed_response dictionary in to a list
    """
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
    """
    Takes a list of dictionaries with stock information and returns the latest close price

    Params:
        dates (list of dictionaries with stock data)

    Examples:
        get_latest_close(dates) #>returns close price as float
    """
    latest_close = dates[0]["close"]
    return latest_close
def get_yesterday_close(dates):
    """
    Takes a list of dictionaries with stock information and returns yesterday's closing price

    Params:
        dates (list of dictionaries with stock data)

    Examples:
        get_yesterday_close(dates) #>returns yesterday's closing price as float
    """
    yesterday_close = dates[1]["close"]
    return yesterday_close
def get_last_refreshed(parsed_response):
    """
    Takes a parsed_response from the get_response() function and returns the date of the latest day of stock information

    Params:
        parsed_response (dictionary datatype)

    Examples:
        get_last_refreshed(parsed_response) #>returns the last refreshed date as a string
    """
    last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]
    return last_refreshed
def get_recent_high(dates):
    """
    Takes a list of dictionaries with stock information and returns the recent high price for the stock

    Params:
        dates (list of dictionaries with stock data)

    Examples:
        get_recent_high(dates) #>returns recent high price as a float
    """
    high_prices = []
    for datez in dates:
        high_price = datez["high"]
        high_prices.append(float(high_price))
        
    
    recent_high = max(high_prices)
    
    return recent_high
    #-----------------------------
def get_recent_low(dates):
    """
    Takes a list of dictionaries with stock information and returns the recent low price for the stock

    Params:
        dates (list of dictionaries with stock data)

    Examples:
        get_recent_low(dates) #>returns recent low price as a float
    """
    low_prices = []
    for datez in dates:
        low_price = datez["low"]
        low_prices.append(float(low_price))
    recent_low = min(low_prices)
    return recent_low
def get_52_week_high(symbol):
    """
    Takes the stock ticker returns the 52 week high price for the stock

    Params:
        symbol (string)

    Examples:
        get_52_week_high(dates) #>returns 52 week high price as a float
    """
    #52 week high
    request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&outputsize=full&apikey={api_key}"
    response = requests.get(request_url)
    parsed_response = json.loads(response.text)
    tsd = parsed_response["Time Series (Daily)"]
    dates = list(tsd.keys())
    x = 0
    weeks_high = []
    for datez in dates:
        week_high = tsd[datez]["2. high"]
        weeks_high.append(float(week_high))
        x += 1
        if x == 360:
            break
    recent_52high = max(weeks_high)
    return recent_52high
def get_52_week_low(symbol):
    """
    Takes the stock ticker and returns the 52 week low price for the stock

    Params:
        symbol (string)

    Examples:
        get_52_low_high(dates) #>returns 52 week low price as a float
    """
    request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&outputsize=full&apikey={api_key}"
    response = requests.get(request_url)
    parsed_response = json.loads(response.text)
    tsd = parsed_response["Time Series (Daily)"]
    dates = list(tsd.keys())
    x = 0
    weeks_low = []

    for datez in dates:
        week_low = tsd[datez]["3. low"]
        weeks_low.append(float(week_low))
        x += 1
        if x == 360:
            break
    recent_52low = min(weeks_low)
    return recent_52low
def display_time():
    """
    Takes the current time and outputs it in a human friendly way

    Params:
        N/A

    Examples:
        display_time() #> Will print current time. e.g. "REQUEST OCCURED ON: 03/31/20 at 14:00:36"
    """
    today = datetime.today()
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    d3 = today.strftime("%m/%d/%y")
    print("REQUEST OCCURED ON: " + d3 + " at " + current_time)
def get_reccomendation(latest_close,recent_high,recent_low):
    """
    Takes the latest close price, recent high price, recent low price and prints the correct reccomendation(BUY , HOLD , or SELL) for the stock as well as a reccomendation reason

    Params:
        latest_close (float) , recent_high (float) , recent_low (float)

    Examples:
        get_reccomendation(latest_close,recent_high,recent_low) #> prints reccomendation (string) and a reccomendation reason (string)
    """
    if (float(latest_close) > (recent_high * 1.15)):
        reccomendation = "SELL!"
        reccomendation_reason = f"The latest closing price({to_usd(float(latest_close))}) is more than 15 percent above the recent high({to_usd(float(recent_high))}). This is an opportunistic time to SELL " 
    elif (float(latest_close) < (recent_low * 1.15)):
        reccomendation = "BUY!"
        reccomendation_reason = f"The latest closing price({to_usd(float(latest_close))}) is less than 15 percent above the recent low({to_usd(float(recent_low))}). This is an opportunistic time to BUY"
    elif True:
        reccomendation = "HOLD!"
        reccomendation_reason = "Does not satisfy requirements for BUY or SELL which were, respectively, the latest closing price is more than 15 percent above the recent high and the latest closing price is less than 15 percent above the recent low. There is no clear indication of any clear upside to selling or buying, so the best course of action is to HOLD"
    print(f"RECOMMENDATION: {reccomendation}")
    print(f"RECOMMENDATION REASON: {reccomendation_reason}")
def receipt_header(symbol):
    """
    Takes the stock ticker and uses that information to print the header for the receipt

    Params:
        symbol (string)

    Examples:
        receipt_header(symbol) #> prints the header for the receipt
    """
    print("-------------------------")
    print(f"SELECTED SYMBOL: {symbol}")
    print("-------------------------")
    print("REQUESTING STOCK MARKET DATA...")
def receipt_body(last_refreshed,latest_close,recent_high, recent_low, recent_52high,recent_52low):
    """
    Takes the last refreshed date, latest close price, recent and 52 week high price, recent and 52 week low price and prints a formatted receipt body

    Params:
        last_refreshed (string), latest_close (float) ,recent_high (float) ,  recent_low (float), recent_52high (float), recent_52low (float)

    Examples:
        receipt_body(last_refreshed,latest_close,recent_high, recent_low, recent_52high,recent_52low) #> prints the receipt body
    """
    print("-------------------------")
    print(f"LATEST DAY: {last_refreshed}")
    print(f"LATEST CLOSE: {to_usd(float(latest_close))}")
    print(f"RECENT HIGH: {to_usd(float(recent_high))}")
    print(f"RECENT LOW:{to_usd(float(recent_low))}")
    print(f"52 WEEK HIGH:{to_usd(float(recent_52high))}")
    print(f"52 WEEK LOW:{to_usd(float(recent_52low))}")
    print("-------------------------")
def receipt_footer():
    """
    Prints the receipt footer

    Params:
        N/A

    Examples:
        receipt_footer() #> prints the footer for the receipt
    """
    print("-------------------------")
    print("HAPPY INVESTING!")
    print("-------------------------")

def send_text(latest_close,yesterday_close):
    """
    Takes the latest close price and yesterdays close price and uses that to determine if a message text message needs to be sent.
    A text message will send if the stock has increased or decreased by more than 5% within the past day

    Params:
        latest_close (float) , yesterday_close (float)

    Examples:
        send_text(latest_close,yesterday_close) #> sends text message if parameters are satisfied
    """
    TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID", "OOPS, please specify env var called 'TWILIO_ACCOUNT_SID'")
    TWILIO_AUTH_TOKEN  = os.environ.get("TWILIO_AUTH_TOKEN", "OOPS, please specify env var called 'TWILIO_AUTH_TOKEN'")
    SENDER_SMS  = os.environ.get("SENDER_SMS", "OOPS, please specify env var called 'SENDER_SMS'")
    RECIPIENT_SMS  = os.environ.get("RECIPIENT_SMS", "OOPS, please specify env var called 'RECIPIENT_SMS'")
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    sendit = False
    if (float(latest_close)/float(yesterday_close) >= 1.05):
        content = f"ALERT: The price of {symbol.upper()} has increased by more than 5% within the past day"
        sendit = True
    if (float(latest_close)/float(yesterday_close) <= .95):
        content = f"ALERT: The price of {symbol.upper()} has decreased by more than 5% within the past day"
        sendit = True
    if sendit == True:
        message = client.messages.create(to=RECIPIENT_SMS, from_=SENDER_SMS, body=content)
if __name__ == "__main__":
    #Writing to CSV-----------------------------------------
    csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", "prices.csv") #Filepath to .csv file

    #Function Calls for calculations-------------------------------------------------------
    symbol = input("Please input a stock ticker (e.g. MSFT)") #Input Stock Ticker
    ticker = symbol.upper() #Makes sure upper case stock ticker
    parsed_response = get_response(ticker) #Returns data for stock ticker
    dates = transform_response(parsed_response) #Transforms data from stock ticker into user friendly format

    latest_close = get_latest_close(dates) #Returns Latest closing price
    yesterday_close = get_yesterday_close(dates) #Returns yesterdays closing price
    last_refreshed = get_last_refreshed(parsed_response)
    recent_high = get_recent_high(dates) #Returns recent high pricce
    recent_low = get_recent_low(dates) #Returns recent low price
    recent_52high = get_52_week_high(symbol) #Returns 52 week high price
    recent_52low = get_52_week_low(symbol) #Returns 52 week low price

    write_to_csv(dates, csv_file_path) #Write stock data to a .csv file

    #Program Outputs(Receipt)
    receipt_header(symbol) #Print receipt header
    display_time() #Print timestamp
    receipt_body(last_refreshed,latest_close,recent_high, recent_low, recent_52high,recent_52low) #Prints receipt body with most of information
    get_reccomendation(latest_close,recent_high,recent_low) #Prints stock reccomendation(BUY, SELL, HOLD)
    receipt_footer() #Prints receipt footer

    #Text Message output
    send_text(latest_close,yesterday_close) #Calls function to send alert if stock moves up or down within a day by more than 5%


