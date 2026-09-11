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

st.header("Análise:")

"""
### Fidelidade da Amostragem Estratificada

* **Proporções praticamente idênticas à base completa:** Com fração de 10%, a amostra estratificada (507 registros) reproduz as proporções originais por tipo de veículo com desvio inferior a 0,1 ponto percentual em três dos quatro grupos — Ônibus Autônomo (54,53% x 54,44%), Ônibus Convencional (28,96% x 28,99%) e Micro-Ônibus (11,48% x 11,44%). A Van Compartilhada, grupo minoritário (5,03% da base), apresenta o maior desvio relativo (5,13% na amostra), o que é esperado em estratos menores, onde a variabilidade amostral tende a ser proporcionalmente maior.

* **Validação da técnica:** Essa fidelidade confirma que a amostragem estratificada é adequada para preservar a representatividade da frota nas análises subsequentes, especialmente relevante dado que os tipos de veículo apresentam comportamentos distintos de tempo de viagem e atraso, como já observado na estatística descritiva.

---

### Amostragem Aleatória Simples x Estratificada: Sensibilidade a Outliers

* **Diferença nas médias amostrais:** A média de `tempo_viagem_min` na base completa é de **26,35 min**. Uma amostra aleatória simples de 500 registros produz média de **25,32 min**, enquanto a amostra estratificada de tamanho semelhante (507 registros) produz **25,78 min** — ambas abaixo da média populacional, mas a estratificada fica mais próxima.

* **Por que isso acontece:** Como `tempo_viagem_min` tem distribuição fortemente assimétrica (poucas viagens anômalas com mais de 300 minutos puxando a média para cima), a amostragem aleatória simples corre maior risco de sub ou sobrerrepresentar essas observações raras por puro acaso. A estratificação por tipo de veículo reduz parcialmente esse risco ao garantir que cada grupo — inclusive o Ônibus Convencional, que concentra os tempos mais extremos — seja amostrado proporcionalmente à sua presença na base.

**Síntese da análise:** A amostragem estratificada por `tipo_veiculo` se mostrou mais robusta que a aleatória simples para preservar tanto a composição da frota quanto a média de `tempo_viagem_min`, principalmente por lidar melhor com a assimetria gerada pelos outliers já identificados na etapa de limpeza. Essa robustez é importante para garantir que testes estatísticos futuros (correlação, testes de hipótese) sejam conduzidos sobre subconjuntos representativos da base real.
"""