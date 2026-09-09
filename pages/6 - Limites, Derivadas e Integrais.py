import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import sympy as sp
from scipy import stats

from Home import carregar_dados
df, _ = carregar_dados()

# ------------------------------------------------------- LIMITES, DERIVADAS, INTEGRAIS
st.header("Limites, derivadas e integrais")

serie_diaria = df.groupby(df["data_viagem"].dt.date)["atraso_estimado_min"].mean().reset_index()
serie_diaria["dia_num"] = range(len(serie_diaria))

coef = np.polyfit(serie_diaria["dia_num"], serie_diaria["atraso_estimado_min"], deg=2)
x = sp.symbols("x")
f_expr = coef[0] * x**2 + coef[1] * x + coef[2]
f_derivada = sp.diff(f_expr, x)
limite_longo_prazo = sp.limit(f_expr, x, sp.oo)
integral_total = sp.integrate(f_expr, (x, 0, len(serie_diaria)))

xs = serie_diaria["dia_num"].values
ys_ajustado = np.polyval(coef, xs)

fig = go.Figure()
fig.add_scatter(x=xs, y=serie_diaria["atraso_estimado_min"], mode="markers",
                 name="Atraso médio diário observado", opacity=0.5)
fig.add_scatter(x=xs, y=ys_ajustado, mode="lines", name="Ajuste polinomial (grau 2)")
fig.update_layout(title="Atraso médio diário — dados observados x curva ajustada",
                   xaxis_title="Dia", yaxis_title="Atraso médio (min)")
st.plotly_chart(fig, use_container_width=True)

c1, c2, c3 = st.columns(3)
c1.metric("Derivada em x=100", f"{float(f_derivada.subs(x, 100)):.6f}")
c2.metric("Limite quando x → ∞", str(limite_longo_prazo))
c3.metric("Integral acumulada no período", f"{float(integral_total):.2f}")

st.caption(
    "O limite tende a -∞ por causa do coeficiente quadrático levemente negativo do ajuste — "
    "um artefato de extrapolar a parábola além da janela observada, não uma previsão real "
    "para o futuro."
)

st.latex(sp.latex(f_expr))