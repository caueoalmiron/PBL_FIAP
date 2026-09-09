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
    df["tempo_viagem_min"] = df.groupby(["tipo_veiculo", "regiao"])["tempo_viagem_min"].transform(
        lambda x: x.fillna(x.median())
    )
    df["linha"] = df["linha"].fillna("Nao_identificada")

    q1, q3 = df["tempo_viagem_min"].quantile([0.25, 0.75])
    iqr = q3 - q1
    limite_sup = q3 + 1.5 * iqr
    df["viagem_anomala"] = df["tempo_viagem_min"] > limite_sup
    return df


df = carregar_dados()

st.title("🚌 Monitor Inteligente de Transporte Público — Cidade Alfa")
st.caption("PBL Fase 5 — Inteligência Analítica, Estatística e Tomada de Decisão")

secao = st.sidebar.radio(
    "Navegação",
    [
        "Visão geral da base",
        "Limpeza e qualidade dos dados",
        "Estatística descritiva",
        "Amostragem",
        "Correlação",
        "Testes de hipótese",
        "Limites, derivadas e integrais",
    ],
)

# ---------------------------------------------------------------- VISÃO GERAL
if secao == "Visão geral da base":
    st.header("Visão geral da base")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Registros", f"{len(df):,}".replace(",", "."))
    c2.metric("Colunas", df.shape[1])
    c3.metric("Nulos originais (linha)", 25)
    c4.metric("Duplicatas (id_veiculo + data)", int(df.duplicated(subset=["id_veiculo", "data_viagem"]).sum()))

    st.subheader("Amostra dos dados")
    st.dataframe(df.head(20), use_container_width=True)

    st.subheader("Tipos de dados e nulos por coluna")
    resumo = pd.DataFrame({"tipo": df.dtypes.astype(str), "nulos": df.isna().sum()})
    st.dataframe(resumo, use_container_width=True)

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

# ---------------------------------------------------------- LIMPEZA E QUALIDADE
elif secao == "Limpeza e qualidade dos dados":
    st.header("Limpeza e qualidade dos dados")

    st.markdown(
        "- `tempo_viagem_min`: nulos imputados pela **mediana do grupo** (`tipo_veiculo` + `regiao`)\n"
        "- `linha`: nulos preenchidos como **'Nao_identificada'**\n"
        "- Outliers de `tempo_viagem_min` (regra do IQR) foram **flagados**, não removidos "
        "— eles representam falhas reais de operação"
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

# --------------------------------------------------------- ESTATÍSTICA DESCRITIVA
elif secao == "Estatística descritiva":
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

# --------------------------------------------------------------------- AMOSTRAGEM
elif secao == "Amostragem":
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

# --------------------------------------------------------------------- CORRELAÇÃO
elif secao == "Correlação":
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

# --------------------------------------------------------------- TESTES DE HIPÓTESE
elif secao == "Testes de hipótese":
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

# ------------------------------------------------------- LIMITES, DERIVADAS, INTEGRAIS
else:
    st.header("Limites, derivadas e integrais")

    serie_diaria = df.groupby(df["data_viagem"].dt.date)["atraso_estimado_min"].mean().reset_index()
    serie_diaria["dia_num"] = range(len(serie_diaria))

    coef = np.polyfit(serie_diaria["dia_num"], serie_diaria["atraso_estimado_min"], deg=2)
    x = sp.symbols("x")
    f_expr = coef[0] * x**2 + coef[1] * x + coef[2]
    f_derivada = sp.diff(f_expr, x)
    limite_longo_prazo = sp.limit(f_expr, x, sp.oo)
    integral_total = sp.integrate(f_expr, (x, 0, len(serie_diaria)))

    xs = serie_diaria["dia_num"].values
    ys_ajustado = np.polyval(coef, xs)

    fig = go.Figure()
    fig.add_scatter(x=xs, y=serie_diaria["atraso_estimado_min"], mode="markers",
                     name="Atraso médio diário observado", opacity=0.5)
    fig.add_scatter(x=xs, y=ys_ajustado, mode="lines", name="Ajuste polinomial (grau 2)")
    fig.update_layout(title="Atraso médio diário — dados observados x curva ajustada",
                       xaxis_title="Dia", yaxis_title="Atraso médio (min)")
    st.plotly_chart(fig, use_container_width=True)

    c1, c2, c3 = st.columns(3)
    c1.metric("Derivada em x=100", f"{float(f_derivada.subs(x, 100)):.6f}")
    c2.metric("Limite quando x → ∞", str(limite_longo_prazo))
    c3.metric("Integral acumulada no período", f"{float(integral_total):.2f}")

    st.caption(
        "O limite tende a -∞ por causa do coeficiente quadrático levemente negativo do ajuste — "
        "um artefato de extrapolar a parábola além da janela observada, não uma previsão real "
        "para o futuro."
    )

    st.latex(sp.latex(f_expr))
