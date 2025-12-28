import yfinance as yf
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from xgboost import XGBRegressor
import joblib
import json
import os
from datetime import datetime, timezone

tickers = ["RELIANCE.NS"]  # Add more later

os.makedirs("docs/predictions", exist_ok=True)
os.makedirs("models", exist_ok=True)

def make_features(closes, window=5):
    X, y = [], []
    for i in range(window, len(closes)):
        X.append(closes[i-window:i])
        y.append(closes[i])
    return np.array(X).reshape(-1, window), np.array(y)

for ticker in tickers:
    print(f"\nProcessing {ticker}...")
    df = yf.download(ticker, period="2y", progress=False)["Close"].dropna()
    df.index = pd.to_datetime(df.index)
    closes = df.values

    X, y = make_features(closes)
    print(f"X shape: {X.shape}")

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = XGBRegressor(n_estimators=100, max_depth=3, random_state=42)
    model.fit(X_train, y_train)

    rmse = np.sqrt(mean_squared_error(y_test, model.predict(X_test)))
    print(f"RMSE: ₹{rmse:.2f}")

    joblib.dump(model, f"models/{ticker.replace('.NS','')}_xgb.joblib")

    pred = model.predict(X[-1:].reshape(1, -1))[0].item()
    last_close = closes[-1].item()

    recent = df.tail(20)  # Match your 20-day format
    recent_history = [{"date": d.strftime("%Y-%m-%d"), "close": float(c.item())} 
                      for d, c in zip(recent.index, recent.values)]

    data = {
        "ticker": ticker,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "predicted_price": round(pred, 2),
        "last_close": round(last_close, 2),
        "signal": "BUY" if pred > last_close*1.02 else "SELL" if pred < last_close*0.98 else "HOLD",
        "rmse": round(rmse, 2),
        "recent_history": recent_history
    }

    with open(f"docs/predictions/{ticker}.json", "w") as f:
        json.dump(data, f, indent=2)

    print("✅ JSON saved with timestamp!")
