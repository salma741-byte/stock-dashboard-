import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests
from io import StringIO
from datetime import datetime, timedelta

st.set_page_config(
    page_title="StockPulse Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=DM+Mono:wght@300;400;500&display=swap');
html, body, [class*="css"] { font-family: 'DM Mono', monospace; }
.stApp { background-color: #080c14; }
[data-testid="stSidebar"] { background: #0d1420 !important; border-right: 1px solid #1e2d42; }
.metric-card {
    background: #111827; border: 1px solid #1e2d42;
    border-radius: 14px; padding: 20px 22px;
    position: relative; overflow: hidden;
}
.metric-card::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, #00d4ff, transparent);
}
.metric-label { font-size: 10px; color: #5a7090; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 6px; }
.metric-value { font-family: 'Syne', sans-serif; font-size: 26px; font-weight: 800; color: #e8edf5; }
.metric-sub   { font-size: 11px; color: #5a7090; margin-top: 4px; }
.pos { color: #00e676 !important; }
.neg { color: #ff4d6d !important; }
.section-title {
    font-family: 'Syne', sans-serif; font-size: 11px; font-weight: 700;
    text-transform: uppercase; letter-spacing: 3px; color: #5a7090; margin: 28px 0 16px;
}
.candle-header {
    background: #111827; border: 1px solid #1e2d42; border-radius: 16px;
    padding: 20px 24px; margin-bottom: 4px;
}
.candle-title { font-family: 'Syne', sans-serif; font-size: 18px; font-weight: 800; color: #e8edf5; }
.candle-sub   { font-size: 11px; color: #5a7090; margin-top: 4px; }
div[data-testid="stMetric"] {
    background: #111827; border: 1px solid #1e2d42; border-radius: 14px; padding: 16px 20px;
}
div[data-testid="stMetric"] label { color: #5a7090 !important; font-size: 11px !important; }
div[data-testid="stMetric"] [data-testid="stMetricValue"] { color: #e8edf5 !important; font-family: 'Syne', sans-serif !important; }
h1, h2, h3 { font-family: 'Syne', sans-serif !important; color: #e8edf5 !important; }
</style>
""", unsafe_allow_html=True)

COLORS = {
    'AAPL':'#00d4ff','MSFT':'#7c4dff','NVDA':'#00e676','AMZN':'#ffc400',
    'GOOGL':'#ff6e40','META':'#ff4d6d','BRK-B':'#b0bec5','LLY':'#e040fb',
    'AVGO':'#40c4ff','TSLA':'#ff6d00'
}

PLOT_LAYOUT = dict(
    paper_bgcolor='#111827', plot_bgcolor='#111827',
    font=dict(family='DM Mono', color='#5a7090', size=11),
    xaxis=dict(gridcolor='#1e2d42', linecolor='#1e2d42'),
    yaxis=dict(gridcolor='#1e2d42', linecolor='#1e2d42'),
    legend=dict(bgcolor='#0d1420', bordercolor='#1e2d42', borderwidth=1),
    margin=dict(l=10, r=10, t=30, b=10)
)

@st.cache_data(ttl=3600)
def load_data():
    url = "https://raw.githubusercontent.com/salma741-byte/stock-dashboard-/main/10_entreprises_data.csv"
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        df = pd.read_csv(StringIO(r.text))
        df['Date'] = pd.to_datetime(df['Date'])
        df = df.sort_values('Date')
        for col in ['Prix_Actuel','Ouverture','Plus_Haut','Plus_Bas','Variation_%','Market_Cap_B','PE_Ratio','Volume']:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        return df
    except Exception as e:
        st.error(f"❌ Erreur chargement données : {e}")
        return pd.DataFrame()

# ── SIDEBAR ──
with st.sidebar:
    st.markdown("## 📈 StockPulse")
    st.markdown("<div style='color:#5a7090;font-size:11px;margin-bottom:24px'>Top 10 Entreprises Mondiales</div>", unsafe_allow_html=True)
    st.markdown("### 🎯 Filtres")
    periode = st.selectbox("Période", ["1 Mois","3 Mois","6 Mois","1 An","Tout"], index=3)
    periode_map = {"1 Mois":30,"3 Mois":90,"6 Mois":180,"1 An":365,"Tout":9999}
    jours = periode_map[periode]
    df_all = load_data()
    if not df_all.empty:
        tickers_dispo = sorted(df_all['Ticker'].unique().tolist())
        tickers_sel = st.multiselect("Entreprises (courbes)", tickers_dispo, default=tickers_dispo)
    else:
        tickers_sel = []
    st.markdown("---")
    if st.button("🔄 Rafraîchir"):
        st.cache_data.clear()
        st.rerun()
    st.markdown("<div style='color:#5a7090;font-size:10px;margin-top:20px'>Auto-update via GitHub Actions<br>Tous les jours à 14h UTC</div>", unsafe_allow_html=True)

# ── HEADER ──
st.markdown("<h1 style='font-size:32px;font-weight:800;margin-bottom:4px'>STOCK<span style='color:#00d4ff'>PULSE</span></h1>", unsafe_allow_html=True)
st.markdown(f"<div style='color:#5a7090;font-size:12px;margin-bottom:28px'>Dashboard automatisé · {datetime.now().strftime('%d/%m/%Y %H:%M')}</div>", unsafe_allow_html=True)

if df_all.empty:
    st.warning("Impossible de charger les données.")
    st.stop()

# Filtrer par période
if jours < 9999:
    cutoff = pd.Timestamp.now() - timedelta(days=jours)
    df = df_all[df_all['Date'] >= cutoff]
else:
    df = df_all.copy()

df = df[df['Ticker'].isin(tickers_sel)] if tickers_sel else df.copy()
latest = df.sort_values('Date').groupby('Ticker').last().reset_index()

# ── KPI CARDS ──
st.markdown("<div class='section-title'>📊 Vue d'ensemble</div>", unsafe_allow_html=True)
cols = st.columns(5)
total_cap = latest['Market_Cap_B'].sum()
avg_var   = latest['Variation_%'].mean()
top_gainer = latest.loc[latest['Variation_%'].idxmax()]
last_date  = df['Date'].max().strftime('%Y-%m-%d')

metrics = [
    ("Entreprises",     f"{len(latest)}",          "Top mondial 🏢"),
    ("Market Cap Total",f"${total_cap:,.0f}B",      "Capitalisation 💰"),
    ("Variation Moy.",  f"{avg_var:+.2f}%",         "Moyenne du jour 📈"),
    ("Top Gagnant",     top_gainer['Ticker'],        f"+{top_gainer['Variation_%']:.2f}% 🚀"),
    ("Dernière Update", last_date,                   "GitHub Actions 🔄"),
]
for i,(label,val,sub) in enumerate(metrics):
    with cols[i]:
        color = "pos" if ("Variation" in label and avg_var>=0) or "Gagnant" in label else ""
        st.markdown(f"""<div class='metric-card'>
          <div class='metric-label'>{label}</div>
          <div class='metric-value {color}'>{val}</div>
          <div class='metric-sub'>{sub}</div></div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ════════════════════════════════════════════
# 🕯️ SECTION CANDLESTICK
# ════════════════════════════════════════════
st.markdown("<div class='section-title'>🕯️ Graphique Chandeliers Japonais</div>", unsafe_allow_html=True)

# Sélecteur ticker + période candlestick
cc1, cc2 = st.columns([2, 1])
with cc1:
    ticker_candle = st.selectbox(
        "Choisir l'entreprise",
        sorted(df_all['Ticker'].unique().tolist()),
        index=0,
        key="candle_ticker"
    )
with cc2:
    periode_candle = st.selectbox(
        "Période candlestick",
        ["1 Mois","3 Mois","6 Mois","1 An","Tout"],
        index=2,
        key="candle_periode"
    )

jours_candle = {"1 Mois":30,"3 Mois":90,"6 Mois":180,"1 An":365,"Tout":9999}[periode_candle]
if jours_candle < 9999:
    cutoff_c = pd.Timestamp.now() - timedelta(days=jours_candle)
    df_candle = df_all[(df_all['Ticker']==ticker_candle) & (df_all['Date']>=cutoff_c)].sort_values('Date')
else:
    df_candle = df_all[df_all['Ticker']==ticker_candle].sort_values('Date')

if not df_candle.empty:
    # Infos résumé
    last_row  = df_candle.iloc[-1]
    first_row = df_candle.iloc[0]
    perf_tot  = ((last_row['Prix_Actuel'] - first_row['Prix_Actuel']) / first_row['Prix_Actuel']) * 100
    var_jour  = last_row['Variation_%']
    nom_entreprise = str(last_row.get('Nom', ticker_candle)).replace('"','')

    # Mini KPIs candlestick
    ck1, ck2, ck3, ck4, ck5 = st.columns(5)
    ck_data = [
        ("Prix Actuel",   f"${last_row['Prix_Actuel']:.2f}",  ""),
        ("Ouverture",     f"${last_row['Ouverture']:.2f}",    ""),
        ("+ Haut",        f"${last_row['Plus_Haut']:.2f}",    "pos"),
        ("+ Bas",         f"${last_row['Plus_Bas']:.2f}",     "neg"),
        ("Perf. Période", f"{perf_tot:+.1f}%",                "pos" if perf_tot>=0 else "neg"),
    ]
    for col_k, (lbl, v, cls) in zip([ck1,ck2,ck3,ck4,ck5], ck_data):
        with col_k:
            st.markdown(f"""<div class='metric-card' style='padding:14px 16px'>
              <div class='metric-label'>{lbl}</div>
              <div class='metric-value {cls}' style='font-size:20px'>{v}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── CANDLESTICK CHART ──
    fig_candle = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        row_heights=[0.75, 0.25],
        vertical_spacing=0.03
    )

    # Bougies
    fig_candle.add_trace(go.Candlestick(
        x=df_candle['Date'],
        open=df_candle['Ouverture'],
        high=df_candle['Plus_Haut'],
        low=df_candle['Plus_Bas'],
        close=df_candle['Prix_Actuel'],
        name=ticker_candle,
        increasing=dict(line=dict(color='#00e676', width=1), fillcolor='rgba(0,230,118,0.7)'),
        decreasing=dict(line=dict(color='#ff4d6d', width=1), fillcolor='rgba(255,77,109,0.7)'),
    ), row=1, col=1)

    # Moyenne mobile 20j
    df_candle['MA20'] = df_candle['Prix_Actuel'].rolling(20).mean()
    df_candle['MA50'] = df_candle['Prix_Actuel'].rolling(50).mean()

    fig_candle.add_trace(go.Scatter(
        x=df_candle['Date'], y=df_candle['MA20'],
        name='MA 20', line=dict(color='#ffc400', width=1.5, dash='dot'),
        opacity=0.8
    ), row=1, col=1)

    fig_candle.add_trace(go.Scatter(
        x=df_candle['Date'], y=df_candle['MA50'],
        name='MA 50', line=dict(color='#e040fb', width=1.5, dash='dot'),
        opacity=0.8
    ), row=1, col=1)

    # Volume bars
    colors_vol = ['#00e676' if c >= o else '#ff4d6d'
                  for c, o in zip(df_candle['Prix_Actuel'], df_candle['Ouverture'])]
    fig_candle.add_trace(go.Bar(
        x=df_candle['Date'],
        y=df_candle['Volume']/1e6,
        name='Volume (M)',
        marker_color=colors_vol,
        marker_opacity=0.6,
        showlegend=True
    ), row=2, col=1)

    fig_candle.update_layout(
        **PLOT_LAYOUT,
        height=560,
        title=dict(
            text=f"<b>{ticker_candle}</b> — {nom_entreprise}",
            font=dict(family='Syne', size=16, color='#e8edf5'),
            x=0.01
        ),
        xaxis_rangeslider_visible=False,
        showlegend=True,
        yaxis=dict(gridcolor='#1e2d42', linecolor='#1e2d42', title='Prix ($)', title_font=dict(color='#5a7090')),
        yaxis2=dict(gridcolor='#1e2d42', linecolor='#1e2d42', title='Volume (M)', title_font=dict(color='#5a7090')),
        xaxis2=dict(gridcolor='#1e2d42', linecolor='#1e2d42'),
    )

    st.plotly_chart(fig_candle, use_container_width=True)

    # Légende expliquée
    st.markdown("""
    <div style='background:#0d1420;border:1px solid #1e2d42;border-radius:10px;padding:14px 20px;font-size:11px;color:#5a7090;display:flex;gap:28px;flex-wrap:wrap'>
      <span>🟢 <b style='color:#00e676'>Bougie verte</b> = Prix clôture > ouverture (hausse)</span>
      <span>🔴 <b style='color:#ff4d6d'>Bougie rouge</b> = Prix clôture < ouverture (baisse)</span>
      <span>🟡 <b style='color:#ffc400'>MA 20</b> = Moyenne mobile 20 jours</span>
      <span>🟣 <b style='color:#e040fb'>MA 50</b> = Moyenne mobile 50 jours</span>
    </div>
    """, unsafe_allow_html=True)
else:
    st.warning(f"Pas de données pour {ticker_candle}")

st.markdown("<br>", unsafe_allow_html=True)

# ── COURBE PRIX ──
st.markdown("<div class='section-title'>📉 Évolution du Prix de Clôture</div>", unsafe_allow_html=True)
fig_price = go.Figure()
for ticker in tickers_sel:
    d = df[df['Ticker']==ticker].sort_values('Date')
    fig_price.add_trace(go.Scatter(
        x=d['Date'], y=d['Prix_Actuel'], name=ticker, mode='lines',
        line=dict(color=COLORS.get(ticker,'#00d4ff'), width=2),
        hovertemplate=f"<b>{ticker}</b><br>%{{x|%d/%m/%Y}}<br>$%{{y:.2f}}<extra></extra>"
    ))
fig_price.update_layout(**PLOT_LAYOUT, height=360, showlegend=True)
st.plotly_chart(fig_price, use_container_width=True)

# ── 2 COLONNES ──
col1, col2 = st.columns(2)
with col1:
    st.markdown("<div class='section-title'>🏆 Market Cap (Mds $)</div>", unsafe_allow_html=True)
    lat_s = latest.sort_values('Market_Cap_B', ascending=True)
    fig_cap = go.Figure(go.Bar(
        x=lat_s['Market_Cap_B'], y=lat_s['Ticker'], orientation='h',
        marker_color=[COLORS.get(t,'#00d4ff') for t in lat_s['Ticker']],
        marker_opacity=0.8,
        hovertemplate="<b>%{y}</b><br>$%{x:.0f}B<extra></extra>"
    ))
    fig_cap.update_layout(**PLOT_LAYOUT, height=320)
    st.plotly_chart(fig_cap, use_container_width=True)

with col2:
    st.markdown("<div class='section-title'>📊 Variation % du Jour</div>", unsafe_allow_html=True)
    lat_var = latest.sort_values('Variation_%', ascending=False)
    fig_var = go.Figure(go.Bar(
        x=lat_var['Ticker'],
        y=lat_var['Variation_%'],
        marker_color=['#00e676' if v>=0 else '#ff4d6d' for v in lat_var['Variation_%']],
        marker_opacity=0.85,
        hovertemplate="<b>%{x}</b><br>%{y:+.2f}%<extra></extra>"
    ))
    fig_var.add_hline(y=0, line_color='#1e2d42', line_width=1)
    fig_var.update_layout(**PLOT_LAYOUT, height=320)
    st.plotly_chart(fig_var, use_container_width=True)

# ── COMPARAISON NORMALISÉE ──
st.markdown("<div class='section-title'>🔀 Performance Relative (Base 100)</div>", unsafe_allow_html=True)
fig_norm = go.Figure()
for ticker in tickers_sel:
    d = df[df['Ticker']==ticker].sort_values('Date').copy()
    if len(d) == 0: continue
    base = d['Prix_Actuel'].iloc[0]
    if base == 0: continue
    d['norm'] = (d['Prix_Actuel']/base)*100
    fig_norm.add_trace(go.Scatter(
        x=d['Date'], y=d['norm'], name=ticker, mode='lines',
        line=dict(color=COLORS.get(ticker,'#00d4ff'), width=2),
        hovertemplate=f"<b>{ticker}</b><br>%{{x|%d/%m/%Y}}<br>%{{y:.1f}}<extra></extra>"
    ))
fig_norm.add_hline(y=100, line_color='#1e2d42', line_dash='dash', line_width=1)
fig_norm.update_layout(**PLOT_LAYOUT, height=340, showlegend=True)
st.plotly_chart(fig_norm, use_container_width=True)

# ── VOLUME ──
st.markdown("<div class='section-title'>📦 Volume des Échanges</div>", unsafe_allow_html=True)
lat_vol = latest.sort_values('Volume', ascending=False)
fig_vol = go.Figure(go.Bar(
    x=lat_vol['Ticker'], y=lat_vol['Volume']/1e6,
    marker_color=[COLORS.get(t,'#00d4ff') for t in lat_vol['Ticker']],
    marker_opacity=0.8,
    hovertemplate="<b>%{x}</b><br>%{y:.1f}M<extra></extra>"
))
fig_vol.update_layout(**PLOT_LAYOUT, height=280)
st.plotly_chart(fig_vol, use_container_width=True)

# ── TABLEAU ──
st.markdown("<div class='section-title'>📋 Tableau Détaillé</div>", unsafe_allow_html=True)
table = latest[['Ticker','Nom','Prix_Actuel','Ouverture','Plus_Haut','Plus_Bas','Variation_%','Market_Cap_B','PE_Ratio','Volume']].copy()
table = table.sort_values('Market_Cap_B', ascending=False)
table['Volume']      = (table['Volume']/1e6).round(1).astype(str) + 'M'
table['Market_Cap_B']= '$' + table['Market_Cap_B'].round(0).astype(int).astype(str) + 'B'
table['Prix_Actuel'] = '$' + table['Prix_Actuel'].round(2).astype(str)
table['Variation_%'] = table['Variation_%'].apply(lambda x: f"+{x:.2f}%" if x>=0 else f"{x:.2f}%")
table.columns = ['Ticker','Entreprise','Prix','Ouverture','+ Haut','+ Bas','Variation','Market Cap','PE Ratio','Volume']
st.dataframe(table.set_index('Ticker'), use_container_width=True, height=380)

st.markdown("<br><div style='text-align:center;color:#1e2d42;font-size:10px'>StockPulse · Yahoo Finance · GitHub Actions Auto-Update</div>", unsafe_allow_html=True)
