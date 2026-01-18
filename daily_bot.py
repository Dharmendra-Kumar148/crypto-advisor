import yfinance as yf
import google.generativeai as genai
import os

# 1. Get Secret Key (GitHub will provide this automatically later)
KEY = os.getenv("GEMINI_API_KEY")

if not KEY:
    print("No Key Found!")
    exit()

genai.configure(api_key=KEY)
model = genai.GenerativeModel('gemini-flash-latest')

# 2. Get Data
symbol = "NHPC.NS"
ticker = yf.Ticker(symbol)
data = ticker.history(period="1d")
price = data['Close'].iloc[0]

# 3. Get Advice
prompt = f"Price of {symbol} is {price}. Give me a funny 1-sentence financial advice."
response = model.generate_content(prompt)

# 4. Print Report
print("-" * 30)
print(f"DAILY REPORT FOR {symbol}")
print(f"Price:  {round(price, 2)}")
print(f"Advice: {response.text}")
print("-" * 30)