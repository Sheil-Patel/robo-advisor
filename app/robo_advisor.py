#app/robo_advisor.py

import csv
import requests
import json
import os
from dotenv import load_dotenv
from datetime import date
from datetime import datetime
from twilio.rest import Client

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

#Import Data from API--------------------------

load_dotenv() #> loads contents of the .env file into the script's environment
api_key = os.environ.get("ALPHAVANTAGE_API_KEY")
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID", "OOPS, please specify env var called 'TWILIO_ACCOUNT_SID'")
TWILIO_AUTH_TOKEN  = os.environ.get("TWILIO_AUTH_TOKEN", "OOPS, please specify env var called 'TWILIO_AUTH_TOKEN'")
SENDER_SMS  = os.environ.get("SENDER_SMS", "OOPS, please specify env var called 'SENDER_SMS'")
RECIPIENT_SMS  = os.environ.get("RECIPIENT_SMS", "OOPS, please specify env var called 'RECIPIENT_SMS'")

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
#Validation for ticker Input--------------------------
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
#52 week high
weeks_high = []
weeks_low = []

request_url2 = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&outputsize=full&apikey={api_key}"
response2 = requests.get(request_url2)
parsed_response2 = json.loads(response2.text)
ts52 = parsed_response2["Time Series (Daily)"]
dates2 = list(ts52.keys())
x = 0
for datez2 in dates2:
    week_high = ts52[datez2]["2. high"]
    week_low = ts52[datez2]["3. low"]
    weeks_high.append(float(week_high))
    weeks_low.append(float(week_low))
    x += 1
    if x == 360:
        break
recent_52high = max(weeks_high)
recent_52low = min(weeks_low)
#------------------------------

# Last Refreshed Time
last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]
# ---------------------------------------

# Latest Close Price and day before close ---------------------
ts5 = parsed_response["Time Series (Daily)"]
dates = list(ts5.keys())
latest_day = dates[0] 
yester_day = dates[1]
latest_close = ts5[latest_day]["4. close"]
yesterday_close = ts5[yester_day]["4. close"]
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




#Program Outputs
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



