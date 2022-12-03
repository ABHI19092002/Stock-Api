import requests
import smtplib

# useful news and stocks news sites:
# https://www.alphavantage.co/
# https://newsapi.org/
# for sending sms use this api - https://www.twilio.com/
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

API_KEY = "CSIM5C9ZF4CVLGZP"
news_key = "b6d281cd1fbc49a69a4b5a90769ea963"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

data_parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": API_KEY
}


r1 = requests.get(url=STOCK_ENDPOINT, params=data_parameters)
r1.raise_for_status()
tsla_data = r1.json()["Time Series (Daily)"]
data_list = [value for (key, value) in tsla_data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]
day_before_yesterday = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday["4. close"]

difference_in_stocks = abs(float(yesterday_closing_price) - float(day_before_yesterday_closing_price))

diff_percent = float(difference_in_stocks) / float(yesterday_closing_price) *100

my_email = "abhigaikwad11110@gmail.com"
my_password = "abhishek9755"

if diff_percent >-1:
    news_parameters = {
        "qInTitle": COMPANY_NAME,
        "apiKey": news_key
    }
    r2 = requests.get(url=NEWS_ENDPOINT, params=news_parameters)
    r2.raise_for_status()
    articles = r2.json()["articles"]
    print(articles)
    three_articles = articles[0:3]
    headline = [f"Subject:Tesla News \n\nHeadline:{article['title']},\nBrief:{article['description']}" for article in three_articles]
    with smtplib.SMTP("smtp.gmail.com:587") as connection:
        connection.starttls()
        connection.login(user=my_email, password=my_password)
        for news in headline:
            connection.sendmail(from_addr=my_email, to_addrs="abhigaikwad2002@yahoo.com", msg=news.encode('utf-8'))
