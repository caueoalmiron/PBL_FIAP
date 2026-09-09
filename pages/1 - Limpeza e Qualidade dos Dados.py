import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import sympy as sp
from scipy import stats

# Importando a função e instanciando os dados para uso nesta página
from Home import carregar_dados
df, nulos_originais = carregar_dados()

# ---------------------------------------------------------- LIMPEZA E QUALIDADE
st.header("Limpeza e qualidade dos dados")

st.markdown("### 🧹 Tratamento de Valores Nulos")
col1, col2 = st.columns(2)
with col1:
    st.markdown("##### ⚠️ **Nulos Originais (Antes da Limpeza)**")
    resumo_antes = pd.DataFrame({
        "Coluna": list(nulos_originais.keys()),
        "Nulos": list(nulos_originais.values())
    }).sort_values("Nulos", ascending=False)
    resumo_antes = resumo_antes[resumo_antes["Nulos"] > 0]  # Mostrar só colunas com nulos
    if len(resumo_antes) > 0:
        st.dataframe(resumo_antes, use_container_width=True, hide_index=True)
    else:
        st.info("Nenhuma coluna com nulos (todas têm 0)")

with col2:
    st.markdown("##### ✅ **Nulos Atuais (Depois da Limpeza)**")
    resumo_depois = pd.DataFrame({
        "tipo": df.dtypes.astype(str),
        "nulos": df.isna().sum()
    })
    resumo_depois = resumo_depois[resumo_depois["nulos"] > 0]  # Mostrar só colunas com nulos
    if len(resumo_depois) > 0:
        st.dataframe(resumo_depois, use_container_width=True)
    else:
        st.info("✓ Todos os nulos foram tratados com sucesso!")   

st.markdown(
    "- **`tempo_viagem_min` (41 nulos)**: Imputados pela **mediana do grupo** (`tipo_veiculo` + `regiao`)\n"
    "- **`linha` (25 nulos)**: Preenchidos com **'Nao_identificada'** (sem identificação de linha)\n"
    "- **Resultado**: Nenhum registro removido; todos tratados com sucesso ✓"
)
    
st.markdown("### 🚨 Detecção de Anomalias")
st.markdown(
    "Outliers de `tempo_viagem_min` (regra do IQR) foram **flagados**, não removidos "
    "— eles representam falhas reais de operação."
)

n_anomalas = int(df["viagem_anomala"].sum())
st.metric("Viagens flagadas como anômalas", f"{n_anomalas} ({n_anomalas / len(df):.1%})")

por_tipo = df.groupby("tipo_veiculo")["viagem_anomala"].mean().reset_index()
por_tipo["viagem_anomala"] = (por_tipo["viagem_anomala"] * 100).round(2)

fig = px.bar(por_tipo, x="tipo_veiculo", y="viagem_anomala",
             title="% de viagens anômalas por tipo de veículo",
             labels={"viagem_anomala": "% anômalas"})
st.plotly_chart(fig, use_container_width=True)

fig = px.box(df, x="tipo_veiculo", y="tempo_viagem_min", color="tipo_veiculo",
             title="Distribuição do tempo de viagem por tipo de veículo (outliers visíveis)")
st.plotly_chart(fig, use_container_width=True)