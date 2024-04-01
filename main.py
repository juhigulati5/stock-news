import requests
import datetime as dt
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
STOCK_API_KEY = "JWNTKDXSLUY1VOYL"
NEWS_API_KEY = "c341d4a76963473db2fb5d0b4bc9adf2"
FROM_NUM = "+18333160612"
TO_NUM = '+18777804236'

ACCOUNT_SID = "AC494b7a1f43dc5ed615944d5286b51b2b"
AUTH_TOKEN = "288427d69c71f89a4d03a0efef89998b"

today=dt.datetime.now()
TODAY_DATE = f"{today.year}-{today.month}-{today.day}"

parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY
}

response = requests.get(url=STOCK_ENDPOINT, params=parameters)
response.raise_for_status()

data = response.json()
daily_data = data["Time Series (Daily)"]

closing_stock = [value for (key, value) in daily_data.items()]
yday_close_price = float(closing_stock[0]["4. close"])
two_days_close_price = float(closing_stock[1]["4. close"])
print(yday_close_price)
print(two_days_close_price)

difference = abs(yday_close_price - two_days_close_price)
percent_diff = (difference/yday_close_price) * 100
rounded_percent_diff = round(percent_diff,2)


news_parameters = {
    "apiKey": NEWS_API_KEY,
    "q": COMPANY_NAME,
    "from": TODAY_DATE,
    "sortBy": "popularity",
    "language": "en"
}
news_response = requests.get(url=NEWS_ENDPOINT,params=news_parameters)
news_response.raise_for_status()

news_data = news_response.json()
headlines = [value for (key1,value) in news_data.items()]
headlines = headlines[2]
top_3 = headlines[0:3]


to_send = [f"Headline: {article['title']}. \nBrief: {article['description']}" for article in top_3]

if rounded_percent_diff > 5:
    for i in to_send:
        client = Client(ACCOUNT_SID, AUTH_TOKEN)
        message = client.messages.create(
            body=i,
            from_='+18333160612',
            to='+18777804236'
        )


#TODO 9. - Send each article as a separate message via Twilio. 



#Optional TODO: Format the message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

