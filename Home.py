import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import sympy as sp
from scipy import stats

st.set_page_config(page_title="Cidade Alfa - Transporte Público", layout="wide")

CAMINHO_EXCEL = "cidade_alfa_transporte_publico.xlsx"

@st.cache_data
def carregar_dados():
    df = pd.read_excel(CAMINHO_EXCEL)
    
    # GUARDAR OS NULOS ORIGINAIS ANTES DE QUALQUER LIMPEZA
    nulos_originais = df.isna().sum().to_dict()
    
    df["tempo_viagem_min"] = df.groupby(["tipo_veiculo", "regiao"])["tempo_viagem_min"].transform(
        lambda x: x.fillna(x.median())
    )
    df["linha"] = df["linha"].fillna("Nao_identificada")

    # CÁLCULO DO IQR POR GRUPO (CORRIGIDO)
    def detectar_anomalia(x):
        q1 = x.quantile(0.25)
        q3 = x.quantile(0.75)
        iqr = q3 - q1
        limite_sup = q3 + 1.5 * iqr
        return x > limite_sup
    
    df["viagem_anomala"] = df.groupby(["tipo_veiculo", "regiao"])["tempo_viagem_min"].transform(detectar_anomalia)

    # Retornar dataframe E o dicionário de nulos originais
    return df, nulos_originais

df, nulos_originais = carregar_dados()

st.title("🚌 Monitor Inteligente de Transporte Público — Cidade Alfa")
st.caption("PBL Fase 5 — Inteligência Analítica, Estatística e Tomada de Decisão")

st.header("Visão geral da base")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Registros", f"{len(df):,}".replace(",", "."))
c2.metric("Colunas", df.shape[1])
c3.metric("Total de nulos originais", sum(nulos_originais.values()))
c4.metric("Duplicatas (id_veiculo + data)", int(df.duplicated(subset=["id_veiculo", "data_viagem"]).sum()))

st.subheader("Amostra dos dados")
st.dataframe(df.head(20), use_container_width=True)

st.subheader("Distribuição dos dados")
c1, c2 = st.columns(2)
with c1:
    fig = px.pie(df, names="tipo_veiculo", title="Distribuição por tipo de veículo", hole=0.4)
    st.plotly_chart(fig, use_container_width=True)
with c2:
    fig = px.bar(
        df["regiao"].value_counts().reset_index(),
        x="regiao", y="count", title="Registros por região",
    )
    st.plotly_chart(fig, use_container_width=True)

st.header("Análise:")

st.markdown(
    """
    ### Volume e Qualidade da Amostra Coletada

    **Dimensão da base**: A base conta com **5.069 registros e 18 variáveis**, constituindo uma massa de dados significativa para a investigação da eficiência do transporte público da Cidade Alfa.\n
    **Integridade estrutural**: Não foram identificados registros duplicados considerando a combinação ***id_veiculo + data_viagem***, indicando consistência nessa dimensão de identificação dos registros. A taxa inicial de valores ausentes é de aproximadamente **1,3%**, representando um volume reduzido de dados a ser tratado durante a etapa de preparação e limpeza.
    """
)

st.markdown(
    """
    ### Composição da Frota (Distribuição por Tipo de Veículo)

    **Predomínio dos ônibus autônomos**: Os ônibus autônomos representam **54,5% das operações**, seguidos pelos convencionais (29%), micro-ônibus (11,5%) e vans compartilhadas (5,03%).\n
    **Potencial analítico**: A predominância dos ônibus autônomos possibilita uma comparação com os veículos convencionais, permitindo investigar diferenças relacionadas à **eficiência operacional, tempo de viagem, atrasos e indicadores de risco.**
    """
)

st.markdown(
    """
    ### Distribuição Geográfica dos Registros

    **Cobertura das regiões**: As cinco regiões da Cidade Alfa apresentam uma distribuição relativamente equilibrada dos registros, com aproximadamente **900 a 1.150 observações por região**, permitindo análises comparativas entre diferentes áreas.\n
    **Pontos de atenção**: As regiões Norte e Leste apresentam maior concentração de registros. Essa diferença deverá ser considerada nas análises estatísticas posteriores, sem assumir previamente que ela representa maior demanda ou maior densidade de sensores.
    """
)

st.markdown(
    """
    ### Variáveis Operacionais e Ambientais

    **Multidimensionalidade**: Além das informações relacionadas ao transporte, a base apresenta variáveis operacionais e ambientais, como ***status_operacional, indice_risco_falha, idade_frota_anos, temperatura_c e chuva_mm.***\n
    **Potencial para investigação estatística**: A diversidade de variáveis permite investigar associações entre características da frota, condições operacionais e fatores climáticos com indicadores como **tempo de viagem, atrasos e risco de falha**, utilizando posteriormente técnicas de estatística descritiva, correlação e testes de hipóteses.
    """
)