import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import sympy as sp
from scipy import stats

from Home import carregar_dados
df, _ = carregar_dados()

# ------------------------------------------------------- LIMITES, DERIVADAS, INTEGRAIS
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

st.header("Análise:")

"""
### O Ajuste Polinomial e seu Comportamento ao Longo do Tempo

* **Curva quase plana no período observado:** O ajuste de grau 2 sobre os 211 dias da série (`a ≈ -1,06×10⁻⁵`, `b ≈ 2,16×10⁻³`, `c ≈ 5,88`) tem coeficiente quadrático extremamente pequeno, o que explica por que a derivada em **x = 100** é praticamente nula (**≈ 4,66×10⁻⁵**) — nesse ponto do período, a taxa de variação do atraso médio diário é insignificante, indicando estabilidade operacional no meio da janela observada.

* **Início da série com leve tendência de alta:** A derivada em x = 0 é **≈ 0,00216**, ligeiramente positiva, sugerindo que o atraso médio diário começou a série com uma tendência sutil de crescimento, que se estabiliza (e depois se inverte) conforme o coeficiente quadrático negativo passa a dominar mais adiante na curva.

---

### O Limite no Infinito é um Artefato Matemático, não uma Previsão

* **Extrapolação além dos dados observados:** O limite de `f(x)` quando x → ∞ tende a **-∞**, resultado direto do coeficiente quadrático negativo (`a ≈ -1,06×10⁻⁵`). Isso não deve ser interpretado como "o atraso vai zerar ou ficar negativo no futuro" — é uma limitação inerente a qualquer ajuste polinomial, que só é confiável **dentro** do intervalo em que foi calibrado (0 a 211 dias). Fora dessa janela, a parábola cai indefinidamente por construção matemática, não por um padrão real de melhora operacional.

---

### A Integral como Validação do Modelo

* **Consistência entre o modelo e a média observada:** A integral acumulada de `f(x)` no intervalo [0, 211] é **≈ 1.256,02**. Dividindo pelo número de dias (1.256,02 / 211 ≈ **5,95 min**), obtém-se um valor praticamente idêntico à média real de `atraso_estimado_min` na base completa (**5,96 min**, calculada na estatística descritiva). Essa proximidade funciona como uma validação indireta de que o ajuste polinomial captura bem o comportamento médio da série dentro do período observado, mesmo sendo inadequado para extrapolação.

**Síntese da análise:** O modelo de cálculo confirma, por outra via, que o atraso médio diário se manteve relativamente estável ao longo dos 211 dias observados — a derivada próxima de zero no meio do período e a integral consistente com a média real reforçam essa leitura. O limite no infinito, por outro lado, é um lembrete importante de que modelos polinomiais simples são úteis para descrever tendências dentro da janela observada, mas não devem ser usados para prever o comportamento futuro do sistema de transporte da Cidade Alfa.
"""