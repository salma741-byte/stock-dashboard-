# EquityTrack — Stock Market Dashboard

Tableau de bord interactif Power BI pour le suivi et l'analyse des 10 plus grandes entreprises du S&P 500, alimenté automatiquement par Yahoo Finance via GitHub Actions.

Accéder au dashboard en ligne : https://app.powerbi.com/groups/me/reports/5e14554b-ba53-4889-a2e8-80dec5eb39ab/681a0ff062e54c50ea76?experience=power-bi

---

## Entreprises suivies

| Ticker | Entreprise |
|--------|------------|
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

## Structure du projet

```
stock-dashboard/
├── 10_entreprises_data.csv          Données boursières mises à jour automatiquement
├── extract_yfinance.py              Script d'extraction Yahoo Finance
├── power_bi_projet_final.pbix       Fichier Power BI
└── .github/
    └── workflows/
        └── update_data.yml          Pipeline GitHub Actions
```

---

## Pages du Dashboard

### Page 1 — Chandelier

Analyse technique détaillée par entreprise avec un graphique en chandelier interactif. Affiche le prix d'ouverture, de clôture, le plus haut et le plus bas de chaque séance. Inclut un curseur de zoom et des boutons de période (1M, 6M, 1Y, 2Y, ALL). Les KPI Cards affichent le dernier prix, la variation journalière et la position sur 52 semaines.

### Page 2 — Vue d'Ensemble

Vision globale du marché avec la comparaison des volumes échangés par entreprise et l'évolution des prix sur la période sélectionnée. Un segment de dates permet de filtrer l'ensemble des visuels.

### Page 3 — Analyse du Marché

Analyse comparative entre les 10 entreprises. Contient le rendement moyen par entreprise, le treemap des capitalisations boursières, la heatmap mensuelle des performances et le scatter Risque / Rendement.

### Page 4 — Aide à l'Investissement

Page dédiée à la prise de décision d'investissement. Répond à la question : dans quelle action investir et pourquoi ? Comprend la performance Base 100 depuis 2021, le palmarès des rendements cumulés et l'analyse du drawdown maximum historique de chaque action.

---

## Pipeline de données automatique

Les données sont mises à jour automatiquement chaque jour ouvrable selon le schéma suivant :

- 22h00 UTC : GitHub Actions exécute extract_yfinance.py et met à jour le fichier CSV
- 23h00 UTC : Power BI Service actualise le rapport depuis le nouveau CSV

Le déclenchement manuel est également disponible depuis l'onglet Actions du repository.

---

## Colonnes du fichier CSV

| Colonne | Description |
|---------|-------------|
| Date | Date de la séance |
| Ticker | Symbole boursier |
| Nom | Nom complet de l'entreprise |
| close | Prix de clôture |
| open | Prix d'ouverture |
| high | Plus haut de la séance |
| Low | Plus bas de la séance |
| Volume | Volume échangé |
| Market_Cap_B | Capitalisation boursière en milliards de dollars |
| PE_Ratio | Price-to-Earnings Ratio |
| 52W_High | Plus haut sur 52 semaines |
| 52W_Low | Plus bas sur 52 semaines |
| Variation_% | Variation journalière en pourcentage |

---

## Installation

### Prérequis

- Python 3.10 ou supérieur
- Power BI Desktop
- Compte GitHub
- Compte Power BI Service

### Étapes

Cloner le repository :

```bash
git clone https://github.com/salma741-byte/stock-dashboard-.git
cd stock-dashboard-
```

Installer les dépendances Python :

```bash
pip install yfinance pandas
```

Lancer l'extraction manuellement :

```bash
python extract_yfinance.py
```

Ouvrir le fichier power_bi_projet_final.pbix dans Power BI Desktop, changer la source de données vers l'URL suivante et actualiser :

```
https://raw.githubusercontent.com/salma741-byte/stock-dashboard-/main/10_entreprises_data.csv
```

---

## Configuration Power BI Service

1. Publier le rapport depuis Power BI Desktop
2. Aller dans les paramètres du jeu de données
3. Activer l'actualisation planifiée
4. Définir l'heure à 23h00 UTC

---

## Technologies utilisées

- Power BI Desktop et Power BI Service pour la visualisation et la publication
- Python et la bibliothèque yfinance pour l'extraction des données boursières
- GitHub Actions pour l'automatisation du pipeline quotidien
- Plotly.js pour les graphiques interactifs en HTML (chandelier, base 100, heatmap)
- DAX pour les mesures et calculs dans Power BI

---

## Avertissement

Les données et visualisations présentées dans ce projet sont fournies à titre informatif uniquement et ne constituent pas un conseil en investissement financier.

---

Dernière mise à jour : Mars 2026
