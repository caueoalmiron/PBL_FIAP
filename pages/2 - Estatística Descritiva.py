import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import sympy as sp
from scipy import stats

from Home import carregar_dados
df, _ = carregar_dados()

# --------------------------------------------------------- ESTATÍSTICA DESCRITIVA
st.header("Estatística descritiva")

colunas_num = ["tempo_viagem_min", "atraso_estimado_min", "indice_risco_falha",
               "nivel_bateria_pct", "satisfacao_passageiro"]

st.subheader("Resumo geral")
st.dataframe(df[colunas_num].describe().T, use_container_width=True)

st.subheader("Assimetria (skew) e curtose (kurt)")
skew_kurt = df[["tempo_viagem_min", "atraso_estimado_min"]].agg(["skew", "kurt"])
st.dataframe(skew_kurt, use_container_width=True)
st.caption(
    "Valores altos de skew/kurt em `tempo_viagem_min` refletem as viagens anômalas "
    "(outliers) mantidas de propósito na base."
)

st.subheader("Por tipo de veículo")
st.dataframe(
    df.groupby("tipo_veiculo")[["tempo_viagem_min", "atraso_estimado_min"]].agg(["mean", "median", "std"]),
    use_container_width=True,
)

st.subheader("Satisfação média por região")
desc_regiao = df.groupby("regiao")["satisfacao_passageiro"].agg(["mean", "std", "count"]).reset_index()
fig = px.bar(desc_regiao, x="regiao", y="mean", error_y="std",
             title="Satisfação média do passageiro por região")
st.plotly_chart(fig, use_container_width=True)

fig = px.histogram(df, x="tempo_viagem_min", nbins=60, title="Distribuição do tempo de viagem")
st.plotly_chart(fig, use_container_width=True)