# Stock-Market-Predict (India MVP)

This repository contains an MVP to predict Indian stocks (NSE and BSE) using Yahoo Finance as the data source. It provides daily/weekly/monthly price predictions and buy/sell/hold signals. Models included: baseline, XGBoost, and LSTM (starter implementations).

Disclaimer: This project is for educational and informational purposes only. It is NOT financial advice. Use predictions at your own risk.

Repository layout (feature/indian-market-mvp branch):
- backend/train_predict.py  # data fetch, training, prediction
- backend/requirements.txt
- docs/ (static frontend for GitHub Pages)
- .github/workflows/ (scheduled training + manual dispatch)
- notebooks/ (development notebooks)
- models/ (gitignored; model artifacts saved here locally)

How it works (high level):
- A scheduled GitHub Actions workflow runs daily after market close (11:00 UTC) to fetch fresh data, retrain models for configured tickers, and write prediction JSON files into docs/predictions/ for the frontend to consume.
- Ad-hoc prediction requests are handled via GitHub Issues and a maintainer-triggered workflow (workflow_dispatch).

Next steps: inspect backend/train_predict.py to customize tickers, thresholds, and retraining schedule.
