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

st.header("Análise:")

"""
### A Correlação Mais Forte da Base: Idade da Frota x Risco de Falha

* **Relação quase determinística:** Com **r = 0,859** e p-valor praticamente zero, `idade_frota_anos` e `indice_risco_falha` apresentam a correlação mais forte entre todas as variáveis analisadas — de longe a relação mais robusta da base. Isso indica que a idade da frota é, isoladamente, um dos melhores preditores lineares disponíveis para o risco de falha reportado.

* **Implicação operacional direta:** Diferente de outras correlações mais moderadas, essa magnitude sugere uma política de renovação ou manutenção preventiva orientada por idade da frota como ação de alto impacto potencial para reduzir falhas.

---

### Satisfação do Passageiro: Múltiplos Fatores com Peso Moderado

* **Atraso é o fator mais associado à insatisfação:** `atraso_estimado_min` tem a correlação mais forte com `satisfacao_passageiro` entre as variáveis operacionais (**r = -0,361**), superando `idade_frota_anos` (r = -0,249) e `indice_risco_falha` (r = -0,249), que apresentam magnitude idêntica entre si — o que faz sentido, já que ambas compartilham forte correlação mútua (r = 0,859).

* **Tempo de viagem e chuva têm efeito fraco sobre a satisfação:** `tempo_viagem_min` (r = -0,078) e `chuva_mm` (r = -0,092) mostram associação linear muito fraca com a satisfação, sugerindo que a percepção do passageiro é mais sensível a **atrasos e à confiabilidade da frota** do que à duração da viagem em si ou às condições climáticas.

---

### Relações Indiretas: Frota, Atraso e Clima

* **Frota mais velha associada a mais atraso:** `idade_frota_anos` e `atraso_estimado_min` têm correlação positiva moderada (**r = 0,352**), reforçando que o envelhecimento da frota não afeta só o risco de falha, mas também a pontualidade.

* **Chuva prolonga viagens, mas não gera risco de falha:** `chuva_mm` tem correlação fraca-moderada com `tempo_viagem_min` (**r = 0,267**), porém correlação praticamente nula com `indice_risco_falha` (r = 0,005) — indicando que a chuva atrasa o trajeto sem necessariamente comprometer a integridade mecânica do veículo.

* **Tempo de viagem não se relaciona com risco de falha:** `tempo_viagem_min` x `indice_risco_falha` tem r = -0,003, praticamente zero — viagens mais longas não são, por si só, indicativas de maior risco de falha, contrariando uma hipótese intuitiva.

**Síntese da análise:** A matriz de correlação aponta a **idade da frota** como a variável mais crítica da base, fortemente ligada ao risco de falha (r = 0,859) e moderadamente ligada ao atraso (r = 0,352). Já a satisfação do passageiro é mais sensível ao **atraso** do que a qualquer outro fator isolado, o que direciona investimentos em pontualidade como alavanca mais direta para melhorar a percepção do serviço — hipótese que será testada formalmente na página seguinte.
"""