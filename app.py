app.py

import streamlit as st from ratings import get_team_ratings import math import random

st.set_page_config(page_title="Basket Pro App PRO", layout="centered")

st.title("🏀 Basket Pro – Nivel PRO") st.caption("Spread + Monte Carlo + Filtros No Bet")

teams = { "Lakers": "LAL", "Warriors": "GSW", "Celtics": "BOS", "Bucks": "MIL", "Nuggets": "DEN", "Heat": "MIA", "Suns": "PHX", "Mavericks": "DAL", "76ers": "PHI", "Clippers": "LAC" }

home = st.selectbox("🏠 Local", list(teams.keys())) away = st.selectbox("🚗 Visitante", list(teams.keys()))

spread_line = st.number_input("Spread mercado (ej: -4.5 local)", value=-4.5) odds_home = st.number_input("Cuota Local", value=1.90) odds_away = st.number_input("Cuota Visitante", value=1.90)

SIMS = 10000

if st.button("Calcular"): if home == away: st.error("Equipos iguales") st.stop()

off_h, def_h, pace_h = get_team_ratings(teams[home])
off_a, def_a, pace_a = get_team_ratings(teams[away])

pace = (pace_h + pace_a) / 2

pts_home = (off_h * def_a) * pace / 100
pts_away = (off_a * def_h) * pace / 100
diff = pts_home - pts_away

sigma = max(8, min(16, (pts_home + pts_away) * 0.055))

# ---- Monte Carlo ----
home_wins = 0
cover_home = 0

for _ in range(SIMS):
    sim_h = random.gauss(pts_home, sigma)
    sim_a = random.gauss(pts_away, sigma)
    if sim_h > sim_a:
        home_wins += 1
    if (sim_h - sim_a) > abs(spread_line):
        cover_home += 1

prob_home = home_wins / SIMS
prob_away = 1 - prob_home
prob_cover = cover_home / SIMS

ev_home = (prob_home * odds_home) - 1
ev_away = (prob_away * odds_away) - 1

st.subheader("📊 Resultado Principal")
st.write(f"{home}: {pts_home:.1f} pts")
st.write(f"{away}: {pts_away:.1f} pts")
st.write(f"Diferencial esperado: {diff:.1f}")

st.subheader("🎯 Probabilidades (Monte Carlo)")
st.write(f"Gana {home}: {prob_home:.1%}")
st.write(f"Gana {away}: {prob_away:.1%}")
st.write(f"{home} cubre spread {spread_line}: {prob_cover:.1%}")

st.subheader("💎 Value Betting")
st.write(f"EV {home}: {ev_home:.3f}")
st.write(f"EV {away}: {ev_away:.3f}")

# ---- NO BET FILTER ----
st.subheader("🚦 Decisión")
if abs(diff) < 3:
    st.warning("NO BET – Partido parejo")
elif ev_home > 0.05:
    st.success(f"APUESTA RECOMENDADA: {home}")
elif ev_away > 0.05:
    st.success(f"APUESTA RECOMENDADA: {away}")
else:
    st.warning("NO BET – Sin value")
