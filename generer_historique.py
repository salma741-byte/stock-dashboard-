

import yfinance as yf
import pandas as pd
from datetime import datetime

TICKERS = ["AAPL", "MSFT", "NVDA", "AMZN", "GOOGL", "META", "BRK-B", "LLY", "AVGO", "TSLA"]
CSV_FILE = "10_entreprises_data.csv"
DATE_DEBUT = "2021-01-01"

print(f" Téléchargement historique 2021 → {datetime.today().strftime('%Y-%m-%d')}")
print(" Patiente ~2-3 minutes...\n")

all_rows = []

for ticker in TICKERS:
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(start=DATE_DEBUT, end=datetime.today().strftime("%Y-%m-%d"))
        info = stock.info
        nom = info.get("longName", ticker)

        if hist.empty:
            print(f"  Pas de données pour {ticker}")
            continue

        for date, row in hist.iterrows():
            ouverture = row["Open"]
            cloture = row["Close"]
            variation = round(((cloture - ouverture) / ouverture) * 100, 2) if ouverture != 0 else 0

            all_rows.append({
                "Date":          date.strftime("%Y-%m-%d"),
                "Ticker":        ticker,
                "Nom":           nom,
                "Prix_Actuel":   round(cloture, 2),
                "Ouverture":     round(ouverture, 2),
                "Plus_Haut":     round(row["High"], 2),
                "Plus_Bas":      round(row["Low"], 2),
                "Volume":        int(row["Volume"]),
                "Market_Cap_B":  round(info.get("marketCap", 0) / 1e9, 2),
                "PE_Ratio":      info.get("trailingPE", None),
                "52W_High":      info.get("fiftyTwoWeekHigh", None),
                "52W_Low":       info.get("fiftyTwoWeekLow", None),
                "Variation_%":   variation,
            })

        print(f" {ticker} ({nom}) — {len(hist)} jours chargés")

    except Exception as e:
        print(f" Erreur pour {ticker}: {e}")

df = pd.DataFrame(all_rows)
df = df.sort_values(["Date", "Ticker"]).reset_index(drop=True)
df.to_csv(CSV_FILE, index=False)

print(f"\n TERMINÉ !")
print(f" {len(df)} lignes enregistrées dans '{CSV_FILE}'")
print(f" Du {df['Date'].min()} au {df['Date'].max()}")
print(f"\n Maintenant upload '{CSV_FILE}' sur GitHub dans ton repo stock-dashboard")
