from fastapi import FastAPI
import yfinance as yf
import google.generativeai as genai
import os
from dotenv import load_dotenv # Import the tool

# 1. Load the secret .env file (for your laptop)
load_dotenv()

app = FastAPI()

# 2. Get key securely
GENAI_API_KEY = os.getenv("GEMINI_API_KEY") 

# 3. Stop if no key (prevents you from uploading broken code)
if not GENAI_API_KEY:
    raise ValueError("No API Key found! Check your .env file.")

genai.configure(api_key=GENAI_API_KEY)
model = genai.GenerativeModel('gemini-flash-latest')

@app.get("/")
def home():
    return {"message": "AI Financial Advisor is Ready"}

@app.get("/analyze/{symbol}")
def analyze_stock(symbol: str):
    ticker = yf.Ticker(symbol)
    data = ticker.history(period="1d")
    
    if data.empty:
        return {"error": "Symbol not found"}
    
    current_price = data['Close'].iloc[0]
    
    prompt = f"""
    The current price of {symbol} is {current_price}.
    You are a funny financial advisor.
    In one short sentence, tell me if I should be happy or sad.
    """
    
    response = model.generate_content(prompt)
    
    return {
        "symbol": symbol.upper(),
        "price": round(current_price, 2),
        "ai_advice": response.text
    }