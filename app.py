============================

app.py

BASKET PRO – MODELO PROFESIONAL

Ganador · Spread · Monte Carlo · Value · NO BET

============================

import streamlit as st import math import random from ratings import get_team_ratings

----------------------------

CONFIG STREAMLIT

----------------------------

st.set_page_config(page_title="Basket Pro App PRO", layout="centered")

st.title("🏀 Basket Pro – Nivel PRO") st.caption("Modelo estadístico con Monte Carlo y filtros de valor")

----------------------------

TODOS LOS EQUIPOS NBA

----------------------------

teams = { "Atlanta Hawks": "ATL", "Boston Celtics": "BOS", "Brooklyn Nets": "BKN", "Charlotte Hornets": "CHA", "Chicago Bulls": "CHI", "Cleveland Cavaliers": "CLE", "Dallas Mavericks": "DAL", "Denver Nuggets": "DEN", "Detroit Pistons": "DET", "Golden State Warriors": "GSW", "Houston Rockets": "HOU", "Indiana Pacers": "IND", "LA Clippers": "LAC", "Los Angeles Lakers": "LAL", "Memphis Grizzlies": "MEM", "Miami Heat": "MIA", "Milwaukee Bucks": "MIL", "Minnesota Timberwolves": "MIN", "New Orleans Pelicans": "NOP", "New York Knicks": "NYK", "Oklahoma City Thunder": "OKC", "Orlando Magic": "ORL", "Philadelphia 76ers": "PHI", "Phoenix Suns": "PHX", "Portland Trail Blazers": "POR", "Sacramento Kings": "SAC", "San Antonio Spurs": "SAS", "Toronto Raptors": "TOR", "Utah Jazz": "UTA", "Washington Wizards": "WAS" }

home = st.selectbox("🏠 Equipo Local", list(teams.keys())) away = st.selectbox("🚗 Equipo Visitante", list(teams.keys()))

spread_line = st.number_input("📉 Spread mercado (ej: -4.5 local)", value=-4.5)

st.subheader("💰 Cuotas") odds_home = st.number_input("Cuota Local", min_value=1.01, value=1.90) odds_away = st.number_input("Cuota Visitante", min_value=1.01, value=1.90)

SIMS = 10000

----------------------------

CÁLCULO

----------------------------

if st.button("🔍 Calcular partido"):

if home == away:
    st.error("Los equipos deben ser distintos")
    st.stop()

# Ratings últimos 10 juegos
off_h, def_h, pace_h = get_team_ratings(teams[home])
off_a, def_a, pace_a = get_team_ratings(teams[away])

# Pace promedio
pace = (pace_h + pace_a) / 2

# Puntos esperados
pts_home = (off_h * def_a) * pace / 100
pts_away = (off_a * def_h) * pace / 100

diff = pts_home - pts_away
total_points = pts_home + pts_away

# Desviación estándar dinámica
sigma = max(8, min(16, total_points * 0.055))

# ----------------------------
# MONTE CARLO
# ----------------------------
home_wins = 0
away_wins = 0
cover_home = 0

for _ in range(SIMS):
    sim_home = random.gauss(pts_home, sigma)
    sim_away = random.gauss(pts_away, sigma)

    if sim_home > sim_away:
        home_wins += 1
    else:
        away_wins += 1

    if (sim_home - sim_away) > abs(spread_line):
        cover_home += 1

prob_home = home_wins / SIMS
prob_away = away_wins / SIMS
prob_cover = cover_home / SIMS

# ----------------------------
# VALUE BETTING
# ----------------------------
ev_home = (prob_home * odds_home) - 1
ev_away = (prob_away * odds_away) - 1

# ----------------------------
# RESULTADOS
# ----------------------------
st.subheader("📊 Proyección del Partido")
st.write(f"{home}: **{pts_home:.1f}** puntos")
st.write(f"{away}: **{pts_away:.1f}** puntos")
st.write(f"Total esperado: **{total_points:.1f}**")
st.write(f"Diferencial esperado: **{diff:.1f}**")

st.subheader("🎯 Probabilidades (Monte Carlo)")
st.write(f"Gana {home}: **{prob_home:.1%}**")
st.write(f"Gana {away}: **{prob_away:.1%}**")
st.write(f"{home} cubre spread {spread_line}: **{prob_cover:.1%}**")

st.subheader("💎 Value Betting")
st.write(f"EV {home}: **{ev_home:.3f}**")
st.write(f"EV {away}: **{ev_away:.3f}**")

# ----------------------------
# DECISIÓN FINAL
# ----------------------------
st.subheader("🚦 Decisión del Modelo")

if abs(diff) < 3:
    st.warning("NO BET – Partido muy parejo")
elif ev_home > 0.05:
    st.success(f"APUESTA RECOMENDADA: {home}")
elif ev_away > 0.05:
    st.success(f"APUESTA RECOMENDADA: {away}")
else:
    st.warning("NO BET – Sin ventaja estadística")
