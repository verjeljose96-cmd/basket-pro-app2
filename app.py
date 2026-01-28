import streamlit as st
import math
import random
from ratings import get_team_ratings

st.set_page_config(page_title="Basket Pro", layout="centered")

st.title("Basket Pro NBA")
st.write("Ganador - Spread - Totales - Value - 1H - 1Q")

# -----------------------------
# EQUIPOS NBA (COMPLETO)
# -----------------------------
teams = [
    "Atlanta Hawks", "Boston Celtics", "Brooklyn Nets", "Charlotte Hornets",
    "Chicago Bulls", "Cleveland Cavaliers", "Dallas Mavericks", "Denver Nuggets",
    "Detroit Pistons", "Golden State Warriors", "Houston Rockets", "Indiana Pacers",
    "LA Clippers", "Los Angeles Lakers", "Memphis Grizzlies", "Miami Heat",
    "Milwaukee Bucks", "Minnesota Timberwolves", "New Orleans Pelicans",
    "New York Knicks", "Oklahoma City Thunder", "Orlando Magic",
    "Philadelphia 76ers", "Phoenix Suns", "Portland Trail Blazers",
    "Sacramento Kings", "San Antonio Spurs", "Toronto Raptors",
    "Utah Jazz", "Washington Wizards"
]

home_team = st.selectbox("Equipo Local", teams)
away_team = st.selectbox("Equipo Visitante", teams, index=1)

spread = st.number_input("Spread local", value=-3.5, step=0.5)

st.subheader("Mercado Totales")
total_line = st.number_input("Linea Total Partido", value=224.5, step=0.5)
odds_over = st.number_input("Cuota Over", value=1.90)
odds_under = st.number_input("Cuota Under", value=1.90)

simulaciones = 5000

if st.button("Calcular"):
    # -----------------------------
    # RATINGS
    # -----------------------------
    off_h, def_h, pace_h = get_team_ratings(home_team)
    off_a, def_a, pace_a = get_team_ratings(away_team)

    pace = (pace_h + pace_a) / 2

    exp_home = pace * (off_h / 100) * (def_a / 112)
    exp_away = pace * (off_a / 100) * (def_h / 112)

    total_exp = exp_home + exp_away
    total_1h = total_exp * 0.52
    total_1q = total_exp * 0.26

    home_wins = 0
    spread_cover = 0
    over_hits = 0

    for _ in range(simulaciones):
        h = random.gauss(exp_home, 12)
        a = random.gauss(exp_away, 12)

        if h > a:
            home_wins += 1

        if h + spread > a:
            spread_cover += 1

        if h + a > total_line:
            over_hits += 1

    # -----------------------------
    # PROBABILIDADES
    # -----------------------------
    prob_home = home_wins / simulaciones
    prob_spread = spread_cover / simulaciones
    prob_over = over_hits / simulaciones
    prob_under = 1 - prob_over

    value_over = (prob_over * odds_over) - 1
    value_under = (prob_under * odds_under) - 1

    # -----------------------------
    # RESULTADOS
    # -----------------------------
    st.subheader("Puntos Esperados")
    st.write(home_team + ": " + str(round(exp_home, 1)))
    st.write(away_team + ": " + str(round(exp_away, 1)))
    st.write("Total Partido: " + str(round(total_exp, 1)))

    st.subheader("Ganador y Spread")
    st.write("Probabilidad gana local: " + str(round(prob_home * 100, 1)) + "%")
    st.write("Probabilidad cubre spread local: " + str(round(prob_spread * 100, 1)) + "%")

    st.subheader("Over / Under Partido")
    st.write("Prob Over: " + str(round(prob_over * 100, 1)) + "%")
    st.write("Value Over: " + str(round(value_over, 3)))
    st.write("Prob Under: " + str(round(prob_under * 100, 1)) + "%")
    st.write("Value Under: " + str(round(value_under, 3)))

    if value_over > 0.05:
        st.success("BET: OVER con valor")
    elif value_under > 0.05:
        st.success("BET: UNDER con valor")
    else:
        st.warning("NO BET en Totales")

    st.subheader("Mercados por Periodo")
    st.write("Total esperado 1H: " + str(round(total_1h, 1)))
    st.write("Total esperado 1Q: " + str(round(total_1q, 1)))
