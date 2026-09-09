import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import sympy as sp
from scipy import stats

from Home import carregar_dados
df, _ = carregar_dados()

# --------------------------------------------------------------- TESTES DE HIPÓTESE
st.header("Testes de hipótese")

autonomo = df.loc[df["tipo_veiculo"] == "Onibus_Autonomo", "tempo_viagem_min"]
convencional = df.loc[df["tipo_veiculo"] == "Onibus_Convencional", "tempo_viagem_min"]
t_stat, p_valor_t = stats.ttest_ind(autonomo, convencional, equal_var=False)

grupos = [g["satisfacao_passageiro"].values for _, g in df.groupby("regiao")]
f_stat, p_valor_anova = stats.f_oneway(*grupos)

tabela = pd.crosstab(df["status_operacional"], df["qualidade_percebida"])
chi2, p_valor_chi2, dof, esperado = stats.chi2_contingency(tabela)

c1, c2, c3 = st.columns(3)
c1.metric("Teste t (autônomo x convencional)", f"t = {t_stat:.2f}", f"p = {p_valor_t:.2e}")
c2.metric("ANOVA (satisfação por região)", f"F = {f_stat:.2f}", f"p = {p_valor_anova:.4f}")
c3.metric("Qui-quadrado (status x qualidade)", f"χ² = {chi2:.1f}", f"p = {p_valor_chi2:.2e}")

st.markdown(
    "- **Teste t:** p < 0.05 → rejeita H0. Tempo médio de viagem difere entre autônomo e convencional "
    "(autônomo é mais rápido, em média).\n"
    "- **ANOVA:** p = 0.2525 > 0.05 → não rejeita H0. A satisfação **não** difere significativamente "
    "entre regiões — o problema é operacional, não geográfico.\n"
    "- **Qui-quadrado:** p << 0.05 → rejeita H0. Status operacional está fortemente associado "
    "à qualidade percebida."
)

fig = px.box(df, x="tipo_veiculo", y="tempo_viagem_min", color="tipo_veiculo",
             title="Tempo de viagem: autônomo x convencional")
st.plotly_chart(fig, use_container_width=True)

fig = px.imshow(tabela, text_auto=True, title="Status operacional x Qualidade percebida",
                 color_continuous_scale="Blues")
st.plotly_chart(fig, use_container_width=True) 