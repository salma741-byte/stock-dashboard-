import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import os

TICKERS = ["AAPL", "MSFT", "NVDA", "AMZN", "GOOGL", "META", "BRK-B", "LLY", "AVGO", "TSLA"]

CSV_FILE = "10_entreprises_data.csv"

def fetch_today_data():
    rows = []
    today = datetime.today().strftime("%Y-%m-%d")
    
    for ticker in TICKERS:
        try:
            stock = yf.Ticker(ticker)
           
            hist = stock.history(period="2d")
            if hist.empty:
                print(f"Pas de données pour {ticker}")
                continue
            
            latest = hist.iloc[-1]
            info = stock.info
            
            row = {
                "Date": today,
                "Ticker": ticker,
                "Nom": info.get("longName", ticker),
                "Prix_Actuel": round(latest["Close"], 2),
                "Ouverture": round(latest["Open"], 2),
                "Plus_Haut": round(latest["High"], 2),
                "Plus_Bas": round(latest["Low"], 2),
                "Volume": int(latest["Volume"]),
                "Market_Cap_B": round(info.get("marketCap", 0) / 1e9, 2),
                "PE_Ratio": info.get("trailingPE", None),
                "52W_High": info.get("fiftyTwoWeekHigh", None),
                "52W_Low": info.get("fiftyTwoWeekLow", None),
                "Variation_%": round(((latest["Close"] - latest["Open"]) / latest["Open"]) * 100, 2),
            }
            rows.append(row)
            print(f" {ticker} - {row['Prix_Actuel']} USD")
        except Exception as e:
            print(f" Erreur pour {ticker}: {e}")
    
    return pd.DataFrame(rows)

def update_csv(new_data):
    if os.path.exists(CSV_FILE):
        existing = pd.read_csv(CSV_FILE)
        # Supprimer les lignes du même jour si déjà présentes
        existing = existing[existing["Date"] != new_data["Date"].iloc[0]]
        combined = pd.concat([existing, new_data], ignore_index=True)
    else:
        combined = new_data
    
    combined.to_csv(CSV_FILE, index=False)
    print(f"\n CSV mis à jour : {len(combined)} lignes totales dans {CSV_FILE}")

if __name__ == "__main__":
    print(f" Mise à jour des données - {datetime.today().strftime('%Y-%m-%d %H:%M')}")
    df = fetch_today_data()
    if not df.empty:
        update_csv(df)
        print(df.to_string())
    else:
        print(" Aucune donnée récupérée.")
