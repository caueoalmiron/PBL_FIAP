import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import sympy as sp
from scipy import stats

from Home import carregar_dados
df, _ = carregar_dados()

# --------------------------------------------------------------------- CORRELAÇÃO
st.header("Correlação")

colunas_corr = ["tempo_viagem_min", "atraso_estimado_min", "idade_frota_anos",
                "indice_risco_falha", "chuva_mm", "satisfacao_passageiro"]
corr = df[colunas_corr].corr(method="pearson")

fig = px.imshow(corr, text_auto=".2f", color_continuous_scale="RdBu_r", zmin=-1, zmax=1,
                 title="Matriz de correlação de Pearson")
st.plotly_chart(fig, use_container_width=True)

r, p_valor = stats.pearsonr(df["idade_frota_anos"], df["indice_risco_falha"])
st.metric("Correlação idade da frota x risco de falha", f"r = {r:.3f}", f"p = {p_valor:.2e}")

fig = px.scatter(df, x="idade_frota_anos", y="indice_risco_falha", trendline="ols",
                  opacity=0.4, title="Idade da frota x índice de risco de falha")
st.plotly_chart(fig, use_container_width=True)

st.caption(
    f"Correlação forte e significativa (r={r:.2f}, p<0.001): quanto mais velha a frota, "
    "maior o risco de falha reportado."
)