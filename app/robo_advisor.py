#app/robo_advisor.py

import csv
import requests
import json
import os
from dotenv import load_dotenv
from datetime import date
from datetime import datetime

def to_usd(my_price):
    return "${0:,.2f}".format(my_price)

#Current Time---------------
today = date.today()
now = datetime.now()
current_time = now.strftime("%H:%M:%S")
d3 = today.strftime("%m/%d/%y")
#------------------------------------

#
# INFO INPUTS
#

#Import Data--------------------------

load_dotenv() #> loads contents of the .env file into the script's environment
#Validation for ticket Input--------------------------
api_key = os.environ.get("ALPHAVANTAGE_API_KEY")
validation = True
while validation == True:
    symbol = input("Please input a stock ticker (e.g. MSFT)")
    ticker = symbol.upper()
    request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}"
    response = requests.get(request_url)
    parsed_response = json.loads(response.text)
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
#---------------------------------------------------



#------------------------------

# Last Refreshed Time
last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]
# ---------------------------------------

# Latest Close Price ---------------------
ts5 = parsed_response["Time Series (Daily)"]
dates = list(ts5.keys())
latest_day = dates[0] #TODO: assumes first day is on top, but consider sorting to ensure latest day is first
latest_close = ts5[latest_day]["4. close"]
# ----------------------------------------

#Recent High Price(Maximum of all the high prices) &
#Recent Low Price(Minimum of all the low prices)-----

high_prices = []
low_prices = []

for datez in dates:
    high_price = ts5[datez]["2. high"]
    low_price = ts5[datez]["3. low"]
    high_prices.append(float(high_price))
    low_prices.append(float(low_price))

recent_high = max(high_prices)
recent_low = min(low_prices)
#--------------------------------
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
#Writing to CSV-----------------------------------------
csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", "prices.csv")
csv_headers = ["timestamp", "open", "high", "low", "close", "volume"]


with open(csv_file_path, "w") as csv_file: # "w" means "open the file for writing"
    writer = csv.DictWriter(csv_file, fieldnames=csv_headers)
    writer.writeheader() # uses fieldnames set above
    for datez in dates:
        daily_prices = ts5[datez]
        writer.writerow({
            "timestamp": datez,  
            "open": daily_prices["1. open"], 
            "high": daily_prices["2. high"], 
            "low": daily_prices["3. low"], 
            "close": daily_prices["4. close"], 
            "volume": daily_prices["5. volume"]
        })

#----------------------------------------------------------




#
# INFO OUTPUTS
#









print("-------------------------")
print(f"SELECTED SYMBOL: {symbol}")
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
print("REQUEST OCCURED ON: " + d3 + " at " + current_time)
print("-------------------------")
print(f"LATEST DAY: {last_refreshed}")
print(f"LATEST CLOSE: {to_usd(float(latest_close))}")
print(f"RECENT HIGH: {to_usd(float(recent_high))}")
print(f"RECENT LOW:{to_usd(float(recent_low))}")
print("-------------------------")
print(f"RECOMMENDATION: {reccomendation}")
print(f"RECOMMENDATION REASON: {reccomendation_reason}")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")
