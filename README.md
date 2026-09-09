# PBL Fase 05 — Análise Inteligente do Transporte Público da Cidade Alfa

## Descrição do Projeto

Este projeto foi desenvolvido como parte da disciplina de Projeto Baseado em Problemas (PBL), com o objetivo de aplicar conceitos de Estatística, Ciência de Dados, Matemática Aplicada e Desenvolvimento de Aplicações para análise operacional do sistema de transporte público da Cidade Alfa.

A solução realiza o tratamento, análise e visualização de dados relacionados às operações de transporte, permitindo identificar padrões, anomalias e indicadores relevantes para apoiar a tomada de decisão da gestão pública.

---

## Objetivos

- Realizar a limpeza e preparação dos dados.
- Aplicar técnicas de estatística descritiva.
- Executar processos de amostragem.
- Analisar correlações entre variáveis operacionais.
- Realizar testes de hipóteses estatísticos.
- Aplicar conceitos de cálculo utilizando limites, derivadas e integrais.
- Disponibilizar os resultados em uma interface interativa utilizando Streamlit.

---

## Tecnologias Utilizadas

- Python
- Pandas
- NumPy
- SciPy
- SymPy
- Plotly
- Streamlit
- Microsoft Excel

---

## Estrutura do Projeto

```text
PBL_Fase_05/
│
├── home.py
├── pages
  └── 1 - Limpeza e Qualidade dos Dados.py
  └── 2 - Estatística Descritiva.py
  └── 3 - Amostragem.py
  └── 4 - Correlação.py
  └── 5 - Testes de Hipótese.py
  └── 6 - Limites, Derivadas e Integrais.py
├── cidade_alfa_transporte_publico.xlsx
├── pbl_fase_5_08092026.ipynb
└── README.md
```

### Arquivos Principais

| Arquivo | Descrição |
|----------|------------|
| `Home.py` | Aplicação principal desenvolvida em Streamlit |
| `pages` | Páginas do projeto em Streamlit |
| `cidade_alfa_transporte_publico.xlsx` | Base de dados utilizada nas análises |
| `pbl_fase_5_08092026.ipynb` | Notebook contendo toda a análise exploratória e estatística |

---

## Funcionalidades Implementadas

### Limpeza e Qualidade dos Dados

- Tratamento de valores nulos.
- Imputação de dados utilizando mediana por grupo.
- Identificação de registros anômalos através da técnica IQR.
- Verificação de registros duplicados.

### Estatística Descritiva

- Média, mediana e desvio padrão.
- Assimetria e curtose.
- Análises segmentadas por região e tipo de veículo.

### Amostragem

- Amostragem aleatória simples.
- Amostragem estratificada por tipo de veículo.

### Correlação

- Matriz de correlação de Pearson.
- Avaliação da relação entre idade da frota, risco de falha e demais indicadores operacionais.

### Testes de Hipótese

- Teste t de Student.
- ANOVA.
- Teste Qui-Quadrado.

### Cálculo Aplicado

- Ajuste de função polinomial.
- Derivadas para análise de tendência.
- Limites e integrais aplicados ao comportamento dos atrasos.

### Dashboard Interativo

A aplicação Streamlit disponibiliza painéis interativos contendo:

- Indicadores gerais da operação.
- Distribuição dos veículos.
- Análise de anomalias.
- Estatísticas descritivas.
- Correlações.
- Resultados dos testes estatísticos.
- Visualizações gráficas dinâmicas.

---

## Como Executar

### Instalar Dependências

```bash
pip install pandas numpy scipy sympy plotly streamlit openpyxl
```

### Executar a Aplicação

```bash
streamlit run Home.py
```

---

## Resultados Esperados

A solução permite identificar:

- Regiões com maior incidência de atrasos.
- Comportamentos anômalos nas viagens.
- Relações entre idade da frota e risco operacional.
- Diferenças estatisticamente significativas entre tipos de veículos.
- Tendências temporais relacionadas ao desempenho do sistema de transporte.

---

## Conclusão

O projeto demonstra a aplicação integrada de técnicas de análise de dados, estatística e modelagem matemática para apoiar a gestão do transporte público. A utilização de dashboards interativos facilita a interpretação dos resultados e contribui para a tomada de decisões baseada em dados.

---

**Instituição:** FIAP  
**Curso:** Data Science  
**Disciplina:** Projeto Baseado em Problemas (PBL)  
**Fase:** 05
