

import yfinance as yf
import pandas as pd
from datetime import datetime
import os

TICKERS = ["AAPL", "MSFT", "NVDA", "AMZN", "GOOGL", "META", "BRK-B", "LLY", "AVGO", "TSLA"]
CSV_FILE = "10_entreprises_data.csv"

def fetch_today_data():
    today = datetime.today().strftime("%Y-%m-%d")
    print(f" Mise à jour quotidienne — {today}\n")
    rows = []

    for ticker in TICKERS:
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period="2d")
            info = stock.info

            if hist.empty:
                print(f"  Pas de données pour {ticker}")
                continue

            latest = hist.iloc[-1]
            ouverture = latest["Open"]
            cloture = latest["Close"]
            variation = round(((cloture - ouverture) / ouverture) * 100, 2) if ouverture != 0 else 0

            rows.append({
                "Date":          today,
                "Ticker":        ticker,
                "Nom":           info.get("longName", ticker),
                "Prix_Actuel":   round(cloture, 2),
                "Ouverture":     round(ouverture, 2),
                "Plus_Haut":     round(latest["High"], 2),
                "Plus_Bas":      round(latest["Low"], 2),
                "Volume":        int(latest["Volume"]),
                "Market_Cap_B":  round(info.get("marketCap", 0) / 1e9, 2),
                "PE_Ratio":      info.get("trailingPE", None),
                "52W_High":      info.get("fiftyTwoWeekHigh", None),
                "52W_Low":       info.get("fiftyTwoWeekLow", None),
                "Variation_%":   variation,
            })
            print(f" {ticker} — {round(cloture, 2)} USD  ({variation:+}%)")

        except Exception as e:
            print(f" Erreur pour {ticker}: {e}")

    return pd.DataFrame(rows)

def update_csv(new_data):
    today = new_data["Date"].iloc[0]

    if os.path.exists(CSV_FILE):
        existing = pd.read_csv(CSV_FILE)
        # Supprimer le jour actuel si déjà présent (évite les doublons)
        existing = existing[existing["Date"] != today]
        combined = pd.concat([existing, new_data], ignore_index=True)
    else:
        combined = new_data

    combined = combined.sort_values(["Date", "Ticker"]).reset_index(drop=True)
    combined.to_csv(CSV_FILE, index=False)

    print(f"\n CSV mis à jour : {len(combined)} lignes totales")
    print(f" Du {combined['Date'].min()} au {combined['Date'].max()}")

if __name__ == "__main__":
    print(f" GitHub Actions — {datetime.today().strftime('%Y-%m-%d %H:%M')}\n")
    df = fetch_today_data()

    if not df.empty:
        update_csv(df)
    else:
        print(" Aucune donnée récupérée.")
