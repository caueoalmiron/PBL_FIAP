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

st.header("Análise:")

"""
### Dimensão da Base e Preservação de Dados

* **Tratamento sem Perda:** Foram identificados apenas 41 nulos em `tempo_viagem_min` e 25 em `linha`. A decisão estratégica de **não remover nenhum registro** preserva as observações originais da base e permite investigar posteriormente se a ocorrência de valores ausentes está associada a determinadas condições operacionais, tipos de veículo ou regiões.

* **Imputação Inteligente:** A escolha da **mediana agrupada** por tipo de veículo e região foi adequada para reduzir a influência de valores extremos sobre os valores imputados. Como a distribuição de `tempo_viagem_min` apresenta valores atípicos elevados, com viagens superiores a 300 minutos, a utilização da média poderia deslocar os valores imputados em direção aos extremos. A mediana, por ser menos sensível a valores atípicos, fornece uma estimativa central mais robusta para o preenchimento dos registros ausentes.

* **Linhas Não Identificadas:** A criação da categoria **`Nao_identificada`** em vez da exclusão dos registros preserva essas observações e possibilita investigar posteriormente se a ausência de identificação da linha está associada a determinados tipos de veículo ou regiões, contribuindo para a identificação de possíveis padrões nos dados.

---

### **Detecção de Valores Atípicos Superiores (Regra do IQR por Tipo de Veículo e Região)**

* **Critério de Identificação:** Após o tratamento dos valores ausentes, foi aplicada a **regra do IQR** sobre `tempo_viagem_min`, calculando os limites individualmente para cada combinação de `tipo_veiculo` e `regiao`. Uma viagem foi classificada como atípica quando seu tempo ultrapassou o **limite superior definido por \(Q3 + 1,5 \times IQR\)**. Dessa forma, a classificação considera o comportamento esperado dentro de cada grupo, em vez de aplicar um único limite para toda a cidade.

* **Quantidade de Valores Atípicos:** Pela aplicação desse critério, foram identificadas **53 viagens, correspondentes a aproximadamente 1,0% da base**, como valores atípicos superiores. Essas observações foram preservadas para investigação, pois representam desvios relevantes em relação ao comportamento central de seus respectivos grupos.

* **Magnitude dos Valores Extremos:** Embora representem uma parcela reduzida da base, alguns registros apresentam tempos de viagem superiores a **200 e até mais de 300 minutos**, caracterizando desvios expressivos em relação ao comportamento central observado. Esses casos não devem ser automaticamente interpretados como falhas operacionais, mas como ocorrências que merecem investigação por meio do cruzamento com outras variáveis disponíveis na base, como região, tipo de veículo, `status_operacional` e condições climáticas.

* **Análise da Distribuição:** O boxplot evidencia que a maior parte das observações permanece concentrada em uma faixa próxima aos valores centrais, enquanto uma quantidade reduzida de registros apresenta tempos significativamente mais elevados. Esse comportamento reforça a importância de preservar e investigar os valores atípicos, buscando compreender se estão associados a condições específicas da operação ou a características particulares dos registros.

---

### **Desempenho Comparativo por Tipo de Veículo**

* **Comportamento dos Ônibus Autônomos:** O gráfico de barras revela que os **Ônibus Autônomos** apresentam uma das menores proporções relativas de viagens classificadas como atípicas, abaixo de 1%. Esse resultado sugere uma menor ocorrência relativa de tempos de viagem extremos nesse grupo. Entretanto, essa diferença representa uma **associação observada na base** e, isoladamente, não permite afirmar que a automação seja a causa da menor frequência de valores atípicos.

* **O Ponto de Atenção nos Micro-Ônibus:** Em contrapartida, os **Micro-Ônibus** apresentam a maior proporção relativa de valores atípicos, ultrapassando 1,5%. Esse resultado levanta hipóteses relevantes para investigação, como possíveis diferenças na **idade da frota, características das regiões atendidas, condições operacionais, infraestrutura das rotas e exposição a condições climáticas adversas**.

* **O Extremo do Convencional:** Embora o **Ônibus Convencional** não apresente o maior percentual de valores atípicos, o boxplot mostra que esse grupo concentra os **valores máximos mais elevados** observados na base, incluindo o registro superior a 300 minutos. Essa diferença entre a frequência relativa de ocorrências atípicas e a magnitude dos valores extremos demonstra a importância de analisar tanto a quantidade de anomalias quanto a intensidade dos desvios observados.

**Síntese da análise:** Após o tratamento dos valores ausentes, a aplicação da regra do IQR permitiu identificar **53 viagens (aproximadamente 1,0% da base) como valores atípicos superiores**, utilizando limites calculados individualmente por combinação de tipo de veículo e região. As diferenças observadas entre os grupos fornecem evidências exploratórias importantes e levantam hipóteses que poderão ser investigadas nas etapas estatísticas seguintes, especialmente por meio do cruzamento com variáveis como `idade_frota_anos`, `regiao`, `status_operacional`, `chuva_mm` e demais atributos disponíveis na base.
"""