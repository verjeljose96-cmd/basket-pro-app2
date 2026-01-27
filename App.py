import streamlit as st
from scipy.stats import poisson
import numpy as np

SIMS = 10000

# -------------------------
# SIMULACIÓN POR CUARTOS
# -------------------------
def simular_partido(lambda_a, lambda_b):
    pesos = [0.24, 0.26, 0.24, 0.26]
    qa, qb = [], []
    pa = pb = 0

    for i in range(4):
        la = lambda_a * pesos[i]
        lb = lambda_b * pesos[i]

        # Ajuste clutch / garbage en Q4
        if i == 3:
            diff = pa - pb
            if abs(diff) < 7:
                la *= 1.08
                lb *= 1.08
            elif abs(diff) > 12:
                la *= 0.90
                lb *= 0.90

        p_a = poisson.rvs(la)
        p_b = poisson.rvs(lb)

        pa += p_a
        pb += p_b

        qa.append(p_a)
        qb.append(p_b)

    return pa, pb, qa, qb

# -------------------------
# UI
# -------------------------
st.title("🏀 Basket PRO — Dashboard de Apuestas")

lambda_a = st.number_input("Puntos esperados Equipo A", 80.0, 140.0, 112.0)
lambda_b = st.number_input("Puntos esperados Equipo B", 80.0, 140.0, 108.0)
linea_total = st.number_input("Línea total (FT)", 180.0, 260.0, 220.5)
spread_casa = st.number_input("Spread casa (A)", -20.0, 20.0, -3.5)
cuota_a = st.number_input("Cuota ganador A", 1.01, 5.0, 1.90)

if st.button("Simular escenario completo"):

    gana_a = 0
    over_ft = 0
    spread_win = 0

    totales = []
    diffs = []
    cuartos = [[] for _ in range(4)]

    for _ in range(SIMS):
        pa, pb, qa, qb = simular_partido(lambda_a, lambda_b)

        totales.append(pa + pb)
        diffs.append(pa - pb)

        for i in range(4):
            cuartos[i].append(qa[i] + qb[i])

        if pa > pb:
            gana_a += 1
        if pa + pb > linea_total:
            over_ft += 1
        if (pa - pb) > abs(spread_casa):
            spread_win += 1

    # -------------------------
    # RESULTADOS GENERALES
    # -------------------------
    prob_gana = gana_a / SIMS
    prob_over = over_ft / SIMS
    prob_spread = spread_win / SIMS

    st.subheader("📊 Full Time")

    st.write(f"Prob. gana A: **{prob_gana:.2%}**")
    st.write(f"Prob. Over {linea_total}: **{prob_over:.2%}**")
    st.write(f"Prob. cubrir spread {spread_casa}: **{prob_spread:.2%}**")

    # NO BET por mercado
    st.subheader("🚦 Decisión por mercado")

    def decision(p, nombre):
        if p < 0.55:
            st.error(f"{nombre}: ❌ NO BET")
        elif p > 0.58:
            st.success(f"{nombre}: ✅ BET")
        else:
            st.warning(f"{nombre}: ⚠️ Zona gris")

    decision(prob_gana, "Ganador")
    decision(prob_over, "Total FT")
    decision(prob_spread, "Spread")

    # -------------------------
    # DESGLOSE ESTADÍSTICO
    # -------------------------
    st.subheader("📈 Panorama ampliado")

    st.write(f"Total esperado (media): **{np.mean(totales):.1f}**")
    st.write(f"Rango 10–90% total: **{np.percentile(totales,10):.0f} – {np.percentile(totales,90):.0f}**")

    st.write(f"Diferencia esperada (A-B): **{np.mean(diffs):.1f}**")

    # -------------------------
    # MERCADOS POR CUARTO
    # -------------------------
    st.subheader("⏱️ Mercados por cuarto")

    for i in range(4):
        prob_over_q = np.mean(np.array(cuartos[i]) > np.mean(cuartos[i]))
        media_q = np.mean(cuartos[i])

        st.write(f"Q{i+1} — Total medio: **{media_q:.1f}** | Prob > media: **{prob_over_q:.2%}**")

        if prob_over_q < 0.54:
            st.write("→ ❌ NO BET")
        else:
            st.write("→ ✅ BET interesante")
