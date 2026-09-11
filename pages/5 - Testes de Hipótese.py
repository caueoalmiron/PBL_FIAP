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

st.header("Análise:")

"""
### Teste t: Autônomo é Estatisticamente Mais Rápido

* **Diferença expressiva e altamente significativa:** O teste t (Welch) resulta em **t = -12,18** e **p ≈ 7,2×10⁻³³**, muito abaixo do limiar de 0,05, rejeitando com folga a hipótese nula de igualdade. A diferença nas médias — **24,74 min** para o Ônibus Autônomo contra **31,62 min** para o Convencional — confirma quantitativamente o que a estatística descritiva já sugeria: os autônomos são consistentemente mais rápidos, e não por acaso amostral.

---

### ANOVA: Satisfação é Homogênea entre Regiões

* **Não há evidência de diferença regional:** Com **F = 1,34** e **p = 0,2525**, muito acima de 0,05, não se rejeita a hipótese nula de médias iguais entre as cinco regiões. Isso confirma formalmente o padrão observado na estatística descritiva, onde as médias de satisfação variavam pouco (3,95 a 4,03). **A insatisfação do passageiro, portanto, não é um problema geográfico** — está distribuída de forma parecida por toda a cidade, reforçando que a causa raiz é operacional (atraso, confiabilidade da frota) e não relacionada à região atendida.

---

### Qui-quadrado: Status Operacional e Qualidade Percebida Estão Fortemente Associados

* **Associação extremamente significativa:** χ² = **1.465,76** com 12 graus de liberdade e p-valor essencialmente zero — a associação entre `status_operacional` e `qualidade_percebida` é a mais forte entre os três testes realizados.

* **Padrão visível na tabela de contingência:** Veículos em status **Normal** concentram a maioria das avaliações **Boa/Excelente** (1.852 de 2.176 registros), enquanto **Falha Mecânica** e **Superlotado** concentram a maior parte das avaliações **Regular/Ruim** — 423 de 601 registros em Falha Mecânica e 496 de 861 em Superlotado. Isso indica que a percepção de qualidade do passageiro está diretamente ligada ao status operacional do veículo no momento da viagem, não a fatores externos.

**Síntese da análise:** Os três testes convergem para uma leitura consistente: a diferença de desempenho entre tipos de veículo é real e estatisticamente robusta (teste t), a satisfação não varia por região (ANOVA), e a qualidade percebida está fortemente ligada ao status operacional do veículo (qui-quadrado). Combinado com a correlação já observada entre idade da frota e risco de falha, o quadro aponta para **condição operacional e confiabilidade da frota** — não geografia — como os principais alavancas para melhorar a experiência do passageiro na Cidade Alfa.
"""