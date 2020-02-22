#app/robo_advisor.py

import csv
import requests
import json
import os

def to_usd(my_price):
    return "${0:,.2f}".format(my_price)

#
# INFO INPUTS
#

#Import Data--------------------------
request_url = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=MSFT&interval=5min&apikey=demo"
response = requests.get(request_url)
parsed_response = json.loads(response.text)
#------------------------------

# Last Refreshed Time
last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]
# ---------------------------------------

# Latest Close Price ---------------------
ts5 = parsed_response["Time Series (5min)"]
dates = list(ts5.keys())
latest_day = dates[0] #TODO: assumes first day is on top, but consider sorting to ensure latest day is first
latest_close = ts5[latest_day]["4. close"]
# ----------------------------------------

#Recent High Price(Maximum of all the high prices) &
#Recent Low Price(Minimum of all the low prices)-----

high_prices = []
low_prices = []

for date in dates:
    high_price = ts5[date]["2. high"]
    low_price = ts5[date]["3. low"]
    high_prices.append(float(high_price))
    low_prices.append(float(low_price))

recent_high = max(high_prices)
recent_low = min(low_prices)
#--------------------------------
#Writing to CSV-----------------------------------------
csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", "prices.csv")
csv_headers = ["timestamp", "open", "high", "low", "close", "volume"]


with open(csv_file_path, "w") as csv_file: # "w" means "open the file for writing"
    writer = csv.DictWriter(csv_file, fieldnames=csv_headers)
    writer.writeheader() # uses fieldnames set above
    for date in dates:
        daily_prices = ts5[date]
        writer.writerow({
            "timestamp": date,  
            "open": daily_prices["1. open"], 
            "high": daily_prices["2. high"], 
            "low": daily_prices["3. low"], 
            "close": daily_prices["4. close"], 
            "volume": daily_prices["5. volume"]
        })

#----------------------------------------------------------



#breakpoint()

#
# INFO OUTPUTS
#









print("-------------------------")
print("SELECTED SYMBOL: XYZ")
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
print("REQUEST AT: 2018-02-20 02:00pm")
print("-------------------------")
print(f"LATEST DAY: {last_refreshed}")
print(f"LATEST CLOSE: {to_usd(float(latest_close))}")
print(f"RECENT HIGH: {to_usd(float(recent_high))}")
print(f"RECENT LOW:{to_usd(float(recent_low))}")
print("-------------------------")
print("RECOMMENDATION: BUY!")
print("RECOMMENDATION REASON: TODO")
print("-------------------------")

print(f"Writing Data to CSV: {csv_file_path}...")


print("HAPPY INVESTING!")
print("-------------------------")