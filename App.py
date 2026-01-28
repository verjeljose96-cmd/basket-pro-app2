import streamlit as st
from ratings import get_team_ratings
from scipy.stats import norm

st.set_page_config(page_title="Modelo Baloncesto PRO", layout="centered")

st.title("🏀 Modelo NBA PRO – Ratings Reales")
st.write("Predicción automática con OffRtg, DefRtg y Pace reales")

teams = {
    "Chicago Bulls": "CHI",
    "LA Lakers": "LAL",
    "Boston Celtics": "BOS",
    "Miami Heat": "MIA",
    "Golden State Warriors": "GSW",
    "Denver Nuggets": "DEN"
}

home = st.selectbox("Equipo LOCAL", list(teams.keys()))
away = st.selectbox("Equipo VISITANTE", list(teams.keys()))

if st.button("Calcular partido"):
    off_h, def_h, pace_h = get_team_ratings(teams[home])
    off_a, def_a, pace_a = get_team_ratings(teams[away])

    pace_game = (pace_h + pace_a) / 2

    pts_home = (off_h * def_a * pace_game) / 10000 + 3
    pts_away = (off_a * def_h * pace_game) / 10000 - 3

    total_points = pts_home + pts_away
    diff = pts_home - pts_away

    st.subheader("📊 Resultados Esperados")

    st.write(f"**{home}:** {pts_home:.1f} puntos")
    st.write(f"**{away}:** {pts_away:.1f} puntos")
    st.write(f"🔥 **Total esperado:** {total_points:.1f}")

    st.subheader("🏆 Probabilidad de ganador")
    win_prob_home = norm.cdf(diff, 0, 12)
    win_prob_away = 1 - win_prob_home

    st.write(f"{home}: {win_prob_home*100:.1f}%")
    st.write(f"{away}: {win_prob_away*100:.1f}%")

    st.subheader("🎯 Recomendación")
    if abs(diff) < 3:
        st.success("🤝 NO BET – partido muy parejo")
    elif diff > 0:
        st.success(f"✅ Ganador probable: {home}")
    else:
        st.success(f"✅ Ganador probable: {away}")
