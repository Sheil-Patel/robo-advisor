#app/robo_advisor.py

import requests
import json

def to_usd(my_price):
    return "${0:,.2f}".format(my_price)

#
# INFO INPUTS
#

request_url = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=MSFT&interval=5min&apikey=demo"
response = requests.get(request_url)
parsed_response = json.loads(response.text)



last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]

ts5 = parsed_response["Time Series (5min)"]
dates = list(ts5.keys())
latest_day = dates[0] #TODO: assumes first day is on top, but consider sorting to ensure latest day is first
latest_close = ts5[latest_day]["4. close"]



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
print("RECENT HIGH: $101,000.00")
print("RECENT LOW: $99,000.00")
print("-------------------------")
print("RECOMMENDATION: BUY!")
print("RECOMMENDATION REASON: TODO")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")