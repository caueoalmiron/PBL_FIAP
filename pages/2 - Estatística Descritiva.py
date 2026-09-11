import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import sympy as sp
from scipy import stats

# Importando a função e instanciando os dados para uso nesta página
from Home import carregar_dados
df, _ = carregar_dados()

# --------------------------------------------------------- ESTATÍSTICA DESCRITIVA
st.header("Estatística descritiva")

colunas_num = ["tempo_viagem_min", "atraso_estimado_min", "indice_risco_falha",
               "nivel_bateria_pct", "satisfacao_passageiro"]

st.markdown("### 📊 Resumo Geral")
st.dataframe(df[colunas_num].describe().T, use_container_width=True)
st.caption(
    "`tempo_viagem_min` tem média de ~26 min mas máximo de 371 min — sinal claro "
    "de que os outliers flagados na página anterior seguem presentes na análise geral."
)

st.markdown("### 📈 Assimetria (skew) e Curtose (kurt)")
skew_kurt = df[["tempo_viagem_min", "atraso_estimado_min"]].agg(["skew", "kurt"])
st.dataframe(skew_kurt, use_container_width=True)
st.caption(
    "Valores altos de skew/kurt em `tempo_viagem_min` refletem as viagens anômalas "
    "(outliers) mantidas de propósito na base."
)

st.markdown("### 🚌 Por Tipo de Veículo")
st.dataframe(
    df.groupby("tipo_veiculo")[["tempo_viagem_min", "atraso_estimado_min"]].agg(["mean", "median", "std"]),
    use_container_width=True,
)

st.markdown("### 🗺️ Satisfação Média por Região")
col1, col2 = st.columns(2)
with col1:
    desc_regiao = df.groupby("regiao")["satisfacao_passageiro"].agg(["mean", "std", "count"]).reset_index()
    fig = px.bar(desc_regiao, x="regiao", y="mean", error_y="std",
                 title="Satisfação média do passageiro por região")
    st.plotly_chart(fig, use_container_width=True)
with col2:
    fig = px.histogram(df, x="tempo_viagem_min", nbins=60, title="Distribuição do tempo de viagem")
    st.plotly_chart(fig, use_container_width=True)

st.header("Análise:")

"""
### Dispersão e Assimetria dos Indicadores Operacionais

* **`tempo_viagem_min` fortemente assimétrico:** O skew de aproximadamente **12,8** e a curtose de **234,6** confirmam que a distribuição do tempo de viagem é extremamente concentrada à esquerda, com uma cauda longa à direita puxada pelas viagens anômalas (algumas ultrapassando 300 minutos, contra uma mediana de ~25 minutos). Isso reforça a decisão, já tomada na etapa de limpeza, de **flagar e não remover** esses registros: eles distorcem estatísticas como a média, mas carregam informação operacional relevante.

* **`atraso_estimado_min` próximo da normalidade:** Skew de **0,21** e curtose de **-0,26** indicam uma distribuição bem mais simétrica e sem caudas pesadas, sugerindo que o atraso segue um comportamento operacional mais previsível do que o tempo de viagem — o que faz sentido, já que os atrasos extremos tendem a estar associados às próprias viagens anômalas isoladas na página anterior.

---

### Desempenho Comparativo por Tipo de Veículo

* **Ônibus Convencional é o mais lento e o mais atrasado:** Apresenta a maior média de `tempo_viagem_min` (~31,6 min) e a maior mediana de `atraso_estimado_min` (~6,7 min) entre os quatro tipos de veículo, consistente com o achado da página de limpeza de que esse grupo concentra os valores máximos mais extremos de tempo de viagem.

* **Micro-Ônibus é o mais rápido, mas não o mais pontual:** Tem a menor média de tempo de viagem (~22,2 min), porém isso não se traduz necessariamente em menor atraso — reforçando que **tempo de viagem** e **atraso** são dimensões distintas do desempenho operacional e merecem ser cruzadas com cautela.

* **Ônibus Autônomo e Van Compartilhada ficam em posição intermediária**, com médias de tempo de viagem próximas (~24,7 min e ~23,1 min, respectivamente), o que já era esperado dado o baixo percentual de viagens anômalas encontrado para os autônomos na etapa de limpeza.

---

### Satisfação do Passageiro por Região

* **Baixa variação entre regiões:** As médias de `satisfacao_passageiro` variam pouco — de **3,95** (Centro) a **4,03** (Leste), numa escala de 1 a 5 — com desvios-padrão semelhantes (~0,87 a ~0,94) em todas as regiões. Isso sugere que a percepção de qualidade do serviço é relativamente homogênea na Cidade Alfa, sem uma região se destacando isoladamente como melhor ou pior avaliada.

* **Leste levemente à frente:** Apesar da diferença ser pequena, a região Leste apresenta tanto a maior satisfação média quanto o maior volume de registros (1.142), o que caracteriza uma boa base amostral para sustentar esse resultado nas etapas seguintes de teste de hipótese.

**Síntese da análise:** A estatística descritiva confirma o padrão já identificado na limpeza dos dados: `tempo_viagem_min` é fortemente assimétrico por causa dos outliers preservados, enquanto `atraso_estimado_min` se comporta de forma mais regular. O Ônibus Convencional se destaca negativamente em tempo e atraso, e a satisfação do passageiro é homogênea entre regiões — um indício de que fatores regionais isoladamente **não explicam** grandes diferenças na percepção do serviço, hipótese que poderá ser testada formalmente nas páginas de correlação e testes de hipótese.
"""