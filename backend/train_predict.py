import yfinance as yf
import numpy as np
from sklearn.linear_model import LinearRegression
import joblib
import json
import os

ticker = "RELIANCE.NS"
print(f"Fetching {ticker}...")

df = yf.download(ticker, period="2y", progress=False)["Close"].dropna()
print(f"Got {len(df)} days data")

closes = df.values.flatten()  # FLATTEN
X = np.arange(len(closes)).reshape(-1, 1)
y = closes

print(f"X shape: {X.shape}, y shape: {y.shape}")

model = LinearRegression()
model.fit(X, y)

print(f"R² score: {model.score(X, y):.4f}")

os.makedirs("models", exist_ok=True)
joblib.dump(model, "models/model.joblib")

# Predict next day
next_day = np.array([[len(closes)]])
pred = model.predict(next_day)[0].item()  # .item() FIX

last_close = closes[-1].item()  # .item() FIX

os.makedirs("docs/predictions", exist_ok=True)
with open("docs/predictions/RELIANCE.NS.json", "w") as f:
    json.dump({
        "ticker": ticker, 
        "predicted_price": round(pred, 2), 
        "last_close": round(last_close, 2),
        "signal": "BUY" if pred > last_close * 1.01 else "HOLD"
    }, f, indent=2)

print("✅ Model trained and prediction saved!")
print(f"Prediction: ₹{pred:.2f} (last: ₹{last_close:.2f})")
