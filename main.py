import yfinance as yf
import requests
from ta.momentum import RSIIndicator
from ta.trend import MACD
import pandas as pd
import os

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

tickers = ["GPRO", "SLDB", "ABCL", "NOK", "PLTR"]
messages = []

for ticker in tickers:
    df = yf.download(ticker, period="1mo", interval="1d")
    if df.empty:
        continue

    df["RSI"] = RSIIndicator(df["Close"]).rsi()
    macd = MACD(df["Close"])
    df["MACD"] = macd.macd_diff()

    latest = df.iloc[-1]
    if latest["RSI"] < 30 and latest["MACD"] > 0:
        messages.append(f"*{ticker}* 價格 {latest['Close']:.2f}, RSI {latest['RSI']:.1f}, MACD {latest['MACD']:.2f}")

if messages:
    text = "\n".join(messages)
else:
    text = "今天沒有符合進場條件的股票"

url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
requests.post(url, data={"chat_id": TELEGRAM_CHAT_ID, "text": text})
