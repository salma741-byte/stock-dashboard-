import yfinance as yf
import pandas as pd
from datetime import datetime
import os

TICKERS = ["AAPL", "MSFT", "NVDA", "AMZN", "GOOGL", "META", "BRK-B", "LLY", "AVGO", "TSLA"]
CSV_FILE = "10_entreprises_data.csv"
DATE_DEBUT = "2021-01-01"

def fetch_historique_complet():
    print(f" Premier lancement - chargement depuis {DATE_DEBUT}...\n")
    all_rows = []

    for ticker in TICKERS:
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(start=DATE_DEBUT)
            info = stock.info
            nom = info.get("longName", ticker)

            if hist.empty:
                print(f"  Pas de données pour {ticker}")
                continue

            for date, row in hist.iterrows():
                ouverture = row["Open"]
                cloture   = row["Close"]
                variation = round(((cloture - ouverture) / ouverture) * 100, 2) if ouverture != 0 else 0

                all_rows.append({
                    "Date":         date.strftime("%Y-%m-%d"),
                    "Ticker":       ticker,
                    "Nom":          nom,
                    "Prix_Actuel":  round(cloture, 2),
                    "Ouverture":    round(ouverture, 2),
                    "Plus_Haut":    round(row["High"], 2),
                    "Plus_Bas":     round(row["Low"], 2),
                    "Volume":       int(row["Volume"]),
                    "Market_Cap_B": round(info.get("marketCap", 0) / 1e9, 2),
                    "PE_Ratio":     info.get("trailingPE", None),
                    "52W_High":     info.get("fiftyTwoWeekHigh", None),
                    "52W_Low":      info.get("fiftyTwoWeekLow", None),
                    "Variation_%":  variation,
                })

            print(f" {ticker} ({nom}) — {len(hist)} jours chargés")

        except Exception as e:
            print(f" Erreur pour {ticker}: {e}")

    return pd.DataFrame(all_rows)


def fetch_today_data():
    today = datetime.today().strftime("%Y-%m-%d")
    print(f" Mise à jour quotidienne — {today}\n")
    rows = []

    for ticker in TICKERS:
        try:
            stock = yf.Ticker(ticker)
            hist  = stock.history(period="2d")
            info  = stock.info

            if hist.empty:
                print(f"  Pas de données pour {ticker}")
                continue

            latest    = hist.iloc[-1]
            ouverture = latest["Open"]
            cloture   = latest["Close"]
            variation = round(((cloture - ouverture) / ouverture) * 100, 2) if ouverture != 0 else 0

            rows.append({
                "Date":         today,
                "Ticker":       ticker,
                "Nom":          info.get("longName", ticker),
                "Prix_Actuel":  round(cloture, 2),
                "Ouverture":    round(ouverture, 2),
                "Plus_Haut":    round(latest["High"], 2),
                "Plus_Bas":     round(latest["Low"], 2),
                "Volume":       int(latest["Volume"]),
                "Market_Cap_B": round(info.get("marketCap", 0) / 1e9, 2),
                "PE_Ratio":     info.get("trailingPE", None),
                "52W_High":     info.get("fiftyTwoWeekHigh", None),
                "52W_Low":      info.get("fiftyTwoWeekLow", None),
                "Variation_%":  variation,
            })
            print(f" {ticker} — {round(cloture,2)} USD  ({variation:+}%)")

        except Exception as e:
            print(f" Erreur pour {ticker}: {e}")

    return pd.DataFrame(rows)


def update_csv(new_data):
    if os.path.exists(CSV_FILE):
        existing = pd.read_csv(CSV_FILE)
        dates_nouvelles = new_data["Date"].unique()
        existing = existing[~existing["Date"].isin(dates_nouvelles)]
        combined = pd.concat([existing, new_data], ignore_index=True)
    else:
        combined = new_data

    combined = combined.sort_values(["Date", "Ticker"]).reset_index(drop=True)
    combined.to_csv(CSV_FILE, index=False)
    print(f"\n {len(combined)} lignes totales | Du {combined['Date'].min()} au {combined['Date'].max()}")


if __name__ == "__main__":
    print(f" Démarrage — {datetime.today().strftime('%Y-%m-%d %H:%M')}\n")

    # Si le CSV n'existe pas → charge tout depuis 2021
    # Si le CSV existe déjà  → ajoute seulement aujourd'hui
    if not os.path.exists(CSV_FILE):
        df = fetch_historique_complet()
    else:
        df = fetch_today_data()

    if not df.empty:
        update_csv(df)
    else:
        print(" Aucune donnée récupérée.")
