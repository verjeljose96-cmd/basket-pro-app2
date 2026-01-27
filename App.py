import streamlit as st
from scipy.stats import poisson

SIMS = 10000

def simular_partido(lambda_a, lambda_b):
    pesos = [0.24, 0.26, 0.24, 0.26]
    puntos_a = 0
    puntos_b = 0

    for i in range(4):
        la = lambda_a * pesos[i]
        lb = lambda_b * pesos[i]

        if i == 3:
            diff = puntos_a - puntos_b
            if abs(diff) < 7:
                la *= 1.08
                lb *= 1.08
            elif abs(diff) > 12:
                la *= 0.90
                lb *= 0.90

        puntos_a += poisson.rvs(la)
        puntos_b += poisson.rvs(lb)

    return puntos_a, puntos_b

st.title("🏀 Basket PRO – Modelo Nivel Profesional")

lambda_a = st.number_input("Puntos esperados Equipo A", 80.0, 140.0, 112.0)
lambda_b = st.number_input("Puntos esperados Equipo B", 80.0, 140.0, 108.0)
linea_total = st.number_input("Línea total", 180.0, 260.0, 220.5)
cuota = st.number_input("Cuota ganador Equipo A", 1.01, 5.0, 1.90)

if st.button("Simular partido"):
    gana_a = 0
    over = 0

    for _ in range(SIMS):
        pa, pb = simular_partido(lambda_a, lambda_b)
        if pa > pb:
            gana_a += 1
        if pa + pb > linea_total:
            over += 1

    prob_gana = gana_a / SIMS
    prob_over = over / SIMS
    prob_imp = 1 / cuota
    edge = prob_gana - prob_imp

    st.subheader("📊 Resultados")
    st.write(f"Probabilidad gana A: **{prob_gana:.2%}**")
    st.write(f"Probabilidad Over: **{prob_over:.2%}**")

    st.subheader("💰 Decisión")
    if prob_gana < 0.55:
        st.error("❌ NO BET")
    elif edge > 0.05:
        st.success(f"✅ VALUE BET | Edge: {edge:.2%}")
    else:
        st.warning("⚠️ Sin valor suficiente")
