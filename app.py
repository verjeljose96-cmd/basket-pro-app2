import streamlit as st
from ratings import get_team_ratings
from scipy.stats import norm

st.set_page_config(page_title="🏀 NBA PRO Model", layout="centered")

st.title("🏀 Modelo NBA PRO")
st.write("Predicción automática con ratings reales (OffRtg, DefRtg, Pace)")

# TODOS LOS EQUIPOS NBA
teams = {
    "Atlanta Hawks": "ATL",
    "Boston Celtics": "BOS",
    "Brooklyn Nets": "BRK",
    "Charlotte Hornets": "CHO",
    "Chicago Bulls": "CHI",
    "Cleveland Cavaliers": "CLE",
    "Dallas Mavericks": "DAL",
    "Denver Nuggets": "DEN",
    "Detroit Pistons": "DET",
    "Golden State Warriors": "GSW",
    "Houston Rockets": "HOU",
    "Indiana Pacers": "IND",
    "LA Clippers": "LAC",
    "LA Lakers": "LAL",
    "Memphis Grizzlies": "MEM",
    "Miami Heat": "MIA",
    "Milwaukee Bucks": "MIL",
    "Minnesota Timberwolves": "MIN",
    "New Orleans Pelicans": "NOP",
    "New York Knicks": "NYK",
    "Oklahoma City Thunder": "OKC",
    "Orlando Magic": "ORL",
    "Philadelphia 76ers": "PHI",
    "Phoenix Suns": "PHO",
    "Portland Trail Blazers": "POR",
    "Sacramento Kings": "SAC",
    "San Antonio Spurs": "SAS",
    "Toronto Raptors": "TOR",
    "Utah Jazz": "UTA",
    "Washington Wizards": "WAS"
}

home = st.selectbox("🏠 Equipo LOCAL", list(teams.keys()))
away = st.selectbox("✈️ Equipo VISITANTE", list(teams.keys()))

if st.button("🔍 Calcular partido"):

    off_h, def_h, pace_h = get_team_ratings(teams[home])
    off_a, def_a, pace_a = get_team_ratings(teams[away])

    # Ritmo promedio del partido
    pace_game = (pace_h + pace_a) / 2

    # Puntos esperados (fórmula correcta)
    pts_home = (off_h * def_a * pace_game) / 10000 + 3
    pts_away = (off_a * def_h * pace_game) / 10000 - 3

    total_points = pts_home + pts_away
    diff = pts_home - pts_away

    st.subheader("📊 Desglose de resultados")

    st.write(f"**{home}**")
    st.write(f"- OffRtg: {off_h}")
    st.write(f"- DefRtg rival: {def_a}")
    st.write(f"- Pace partido: {pace_game:.1f}")
    st.write(f"➡️ **Puntos esperados: {pts_home:.1f}**")

    st.write("---")

    st.write(f"**{away}**")
    st.write(f"- OffRtg: {off_a}")
    st.write(f"- DefRtg rival: {def_h}")
    st.write(f"- Pace partido: {pace_game:.1f}")
    st.write(f"➡️ **Puntos esperados: {pts_away:.1f}**")

    st.subheader("🔥 Total del partido")
    st.success(f"Total esperado: **{total_points:.1f} puntos**")

    st.subheader("🏆 Probabilidad de ganador")

    sigma = max(8, min(16, total_points * 0.055))
    prob_home = norm.cdf(diff, 0, sigma)
    prob_away = 1 - prob_home

    st.write(f"{home}: {prob_home*100:.1f}%")
    st.write(f"{away}: {prob_away*100:.1f}%")
    st.write(f"σ usado: {sigma:.2f}")

    st.subheader("🎯 Recomendación final")

    if abs(diff) < 3:
        st.warning("🤝 **NO BET** – partido demasiado parejo")
    elif diff > 0:
        st.success(f"✅ **Ganador probable: {home}**")
    else:
        st.success(f"✅ **Ganador probable: {away}**")
