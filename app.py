import streamlit as st
import random
from ratings import get_team_ratings

st.title("Basket Pro - NBA")

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

home = st.selectbox("Local", teams.keys())
away = st.selectbox("Visitante", teams.keys())

SIMS = 10000

if st.button("Calcular"):
    off_h, def_h, pace_h = get_team_ratings(teams[home])
    off_a, def_a, pace_a = get_team_ratings(teams[away])

    pace = (pace_h + pace_a) / 2

    pts_home = off_h * (pace / 100)
    pts_away = off_a * (pace / 100)

    total = pts_home + pts_away

    sigma = 12

    wins_h = 0

    for _ in range(SIMS):
        sh = random.gauss(pts_home, sigma)
        sa = random.gauss(pts_away, sigma)
        if sh > sa:
            wins_h += 1

    st.subheader("Resultados")
    st.write(home, round(pts_home, 1))
    st.write(away, round(pts_away, 1))
    st.write("Total esperado:", round(total, 1))
    st.write("Probabilidad local:", round(wins_h / SIMS * 100, 1), "%")
