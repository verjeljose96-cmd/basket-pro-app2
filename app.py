import streamlit as st
import random
from ratings import get_team_ratings

st.set_page_config(page_title="Basket Pro", layout="centered")

st.title("Basket Pro - NBA")
st.write("Modelo NBA con Monte Carlo y Value")

teams = {
    "Atlanta Hawks": "ATL",
    "Boston Celtics": "BOS",
    "Brooklyn Nets": "BKN",
    "Charlotte Hornets": "CHA",
    "Chicago Bulls": "CHI",
    "Cleveland Cavaliers": "CLE",
    "Dallas Mavericks": "DAL",
    "Denver Nuggets": "DEN",
    "Detroit Pistons": "DET",
    "Golden State Warriors": "GSW",
    "Houston Rockets": "HOU",
    "Indiana Pacers": "IND",
    "LA Clippers": "LAC",
    "Los Angeles Lakers": "LAL",
    "Memphis Grizzlies": "MEM",
    "Miami Heat": "MIA",
    "Milwaukee Bucks": "MIL",
    "Minnesota Timberwolves": "MIN",
    "New Orleans Pelicans": "NOP",
    "New York Knicks": "NYK",
    "Oklahoma City Thunder": "OKC",
    "Orlando Magic": "ORL",
    "Philadelphia 76ers": "PHI",
    "Phoenix Suns": "PHX",
    "Portland Trail Blazers": "POR",
    "Sacramento Kings": "SAC",
    "San Antonio Spurs": "SAS",
    "Toronto Raptors": "TOR",
    "Utah Jazz": "UTA",
    "Washington Wizards": "WAS"
}

home = st.selectbox("Equipo local", list(teams.keys()))
away = st.selectbox("Equipo visitante", list(teams.keys()))

spread = st.number_input("Spread del mercado (local)", value=-4.5)
odds_home = st.number_input("Cuota local", value=1.90)
odds_away = st.number_input("Cuota visitante", value=1.90)

SIMS = 10000

if st.button("Calcular"):
    if home == away:
        st.error("Selecciona equipos distintos")
        st.stop()

    off_h, def_h, pace_h = get_team_ratings(teams[home])
    off_a, def_a, pace_a = get_team_ratings(teams[away])

    pace = (pace_h + pace_a) / 2

    # PUNTOS ESPERADOS CORRECTOS
    pts_home = off_h * (pace / 100)
    pts_away = off_a * (pace / 100)

    total_points = pts_home + pts_away
    diff = pts_home - pts_away

    sigma = 12  # desviacion tipica NBA

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

        if (sim_home - sim_away) > spread:
            cover_home += 1

    prob_home = home_wins / SIMS
    prob_away = away_wins / SIMS
    prob_cover = cover_home / SIMS

    ev_home = prob_home * odds_home - 1
    ev_away = prob_away * odds_away - 1

    # -------- RESULTADOS --------
    st.subheader("Puntos esperados")
    st.write(home, round(pts_home, 1))
    st.write(away, round(pts_away, 1))
    st.write("Total esperado:", round(total_points, 1))

    st.subheader("Probabilidades")
    st.write(f"Gana {home}: {prob_home:.1%}")
    st.write(f"Gana {away}: {prob_away:.1%}")
    st.write(f"Local cubre spread: {prob_cover:.1%}")

    st.subheader("Value (EV)")
    st.write("EV local:", round(ev_home, 3))
    st.write("EV visitante:", round(ev_away, 3))

    # -------- DECISION --------
    st.subheader("Decision del modelo")

    if abs(diff) < 3:
        st.warning("NO BET - partido muy parejo")
    elif ev_home > 0.05:
        st.success("Apostar LOCAL")
    elif ev_away > 0.05:
        st.success("Apostar VISITANTE")
    else:
        st.warning("NO BET - sin value")
