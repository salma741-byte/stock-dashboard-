# 📊 EquityTrack — Stock Market Dashboard

> Tableau de bord interactif Power BI pour le suivi et l'analyse des **10 plus grandes entreprises du S&P 500**, alimenté automatiquement par Yahoo Finance via GitHub Actions.

![Power BI](https://img.shields.io/badge/Power%20BI-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-2088FF?style=for-the-badge&logo=githubactions&logoColor=white)
![Yahoo Finance](https://img.shields.io/badge/Yahoo%20Finance-6001D2?style=for-the-badge&logo=yahoo&logoColor=white)

---

## 🏢 Entreprises suivies

| Ticker | Entreprise |
|--------|-----------|
| AAPL | Apple Inc. |
| MSFT | Microsoft Corporation |
| NVDA | NVIDIA Corporation |
| AMZN | Amazon.com Inc. |
| GOOGL | Alphabet Inc. |
| META | Meta Platforms Inc. |
| BRK-B | Berkshire Hathaway |
| LLY | Eli Lilly and Company |
| AVGO | Broadcom Inc. |
| TSLA | Tesla Inc. |

---

## 📁 Structure du projet

```
stock-dashboard/
│
├── 📄 10_entreprises_data.csv     # Données boursières (mis à jour automatiquement)
├── 🐍 extract_yfinance.py         # Script d'extraction Yahoo Finance
├── ⚙️  .github/
│   └── workflows/
│       └── update_data.yml        # Pipeline GitHub Actions
└── 📊 power_bi_projet_final.pbix  # Fichier Power BI
```

---

## 📈 Pages du Dashboard

### 🕯️ Page 1 — Chandelier
Analyse technique détaillée par entreprise.
- Graphique en chandelier interactif (Plotly via HTML Viewer)
- Fond dégradé violet avec bougies vertes/rouges
- Boutons de période : 1M / 6M / 1Y / 2Y / ALL
- Curseur de zoom (rangeslider)
- KPI Cards : Dernier prix · Variation · Position 52W

### 🌍 Page 2 — Vue d'Ensemble
Vision globale du marché.
- Comparaison des volumes échangés par entreprise
- Évolution des prix multi-courbes
- Segment de dates interactif

### 📊 Page 3 — Analyse du Marché
Graphiques d'analyse comparative.
- Donut Rendement Moyen par entreprise
- Treemap Market Cap
- Heatmap mensuelle des performances (HTML Viewer)
- Scatter Risque / Rendement

### 💼 Page 4 — Aide à l'Investissement
Outils d'aide à la décision d'investissement.
- Scatter Risque vs Rendement *(Où investir intelligemment ?)*
- Performance Base 100 *(Si vous aviez investi 100$ en 2021...)*
- Palmarès des Performances *(Rendement cumulé depuis 2021)*
- Pire Chute Historique *(Drawdown Maximum)*

---

## ⚙️ Pipeline de données automatique

### Fonctionnement
```
Chaque jour ouvrable à 22h UTC (17h EST, après clôture Wall Street)
        │
        ▼
GitHub Actions → extract_yfinance.py → 10_entreprises_data.csv
        │
        ▼
Power BI Service → Actualisation planifiée à 23h UTC
```

### Colonnes du CSV

| Colonne | Description |
|---------|-------------|
| `Date` | Date de la séance |
| `Ticker` | Symbole boursier |
| `Nom` | Nom complet de l'entreprise |
| `close` | Prix de clôture |
| `open` | Prix d'ouverture |
| `high` | Plus haut de la séance |
| `Low` | Plus bas de la séance |
| `Volume` | Volume échangé |
| `Market_Cap_B` | Capitalisation boursière (Md$) |
| `PE_Ratio` | Price-to-Earnings Ratio |
| `52W_High` | Plus haut sur 52 semaines |
| `52W_Low` | Plus bas sur 52 semaines |
| `Variation_%` | Variation journalière (%) |

---

## 🚀 Installation & Configuration

### Prérequis
- Python 3.10+
- Power BI Desktop
- Compte GitHub (pour les Actions)
- Compte Power BI Service (pour l'actualisation automatique)

### 1. Cloner le repo
```bash
git clone https://github.com/salma741-byte/stock-dashboard-.git
cd stock-dashboard-
```

### 2. Installer les dépendances Python
```bash
pip install yfinance pandas
```

### 3. Lancer manuellement l'extraction
```bash
python extract_yfinance.py
```

### 4. Configurer Power BI
1. Ouvrir `power_bi_projet_final.pbix`
2. Transformer les données → changer la source vers l'URL du CSV GitHub :
```
https://raw.githubusercontent.com/salma741-byte/stock-dashboard-/main/10_entreprises_data.csv
```
3. Installer le visuel **HTML Viewer** depuis AppSource
4. Actualiser les données

### 5. Configurer l'actualisation automatique (Power BI Service)
1. Publier le rapport sur Power BI Service
2. Paramètres du jeu de données → Actualisation planifiée
3. Heure : **23h00 UTC** (après le pipeline GitHub Actions à 22h UTC)

---

## 🔄 GitHub Actions Workflow

Le fichier `.github/workflows/update_data.yml` :
- Se déclenche automatiquement **du lundi au vendredi à 22h UTC**
- Peut aussi être lancé manuellement depuis l'onglet **Actions**
- Committe et push automatiquement le CSV mis à jour

---

## 🎨 Design

| Élément | Valeur |
|---------|--------|
| Fond principal | `#211F3C` |
| Texte | `#DFDFE5` |
| Accent | `#00d4ff` |
| Grille | `#2d2b52` |
| Hausse | `#00e676` |
| Baisse | `#ff4d6d` |
| Violet accent | `#7c6fcd` |

---

## 🛠️ Technologies utilisées

- **Power BI Desktop & Service** — Visualisation et publication
- **Python / yfinance** — Extraction des données boursières
- **GitHub Actions** — Automatisation du pipeline
- **Plotly.js** — Graphiques interactifs (candlestick, base 100)
- **DAX** — Mesures et calculs dans Power BI

---

## 📌 Notes importantes

> ⚠️ Les données sont fournies à titre informatif uniquement et ne constituent pas un conseil en investissement.

> 💡 Pour backfiller des données manquantes, lancer manuellement le workflow depuis l'onglet **Actions** de GitHub.

---

## 👤 Auteur

Projet réalisé dans le cadre d'une analyse financière des grandes capitalisations boursières américaines.

---

*Dernière mise à jour : Mars 2026*
