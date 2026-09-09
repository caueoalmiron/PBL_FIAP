import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import sympy as sp
from scipy import stats

from Home import carregar_dados
df, _ = carregar_dados()

# --------------------------------------------------------------------- AMOSTRAGEM
st.header("Amostragem")

tamanho = st.slider("Tamanho da amostra aleatória simples", 100, 2000, 500, step=100)
amostra_simples = df.sample(n=tamanho, random_state=42)

fracao = st.slider("Fração da amostra estratificada por tipo de veículo", 0.05, 0.5, 0.1, step=0.05)
amostra_estratificada = df.groupby("tipo_veiculo", group_keys=False).sample(frac=fracao, random_state=42)

comparacao = pd.DataFrame({
    "Base completa": df["tipo_veiculo"].value_counts(normalize=True),
    "Amostra estratificada": amostra_estratificada["tipo_veiculo"].value_counts(normalize=True),
})
st.subheader("Proporções: base completa x amostra estratificada")
st.dataframe((comparacao * 100).round(2), use_container_width=True)

fig = go.Figure()
fig.add_bar(x=comparacao.index, y=comparacao["Base completa"], name="Base completa")
fig.add_bar(x=comparacao.index, y=comparacao["Amostra estratificada"], name="Amostra estratificada")
fig.update_layout(barmode="group", title="Comparação de proporções por tipo de veículo")
st.plotly_chart(fig, use_container_width=True)

st.caption("A amostra estratificada mantém as proporções da base original — validação da técnica.")