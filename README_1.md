# ⚡ Previsão de Consumo de Energia Elétrica Residencial

Aplicação de Machine Learning para prever o consumo de energia elétrica residencial (Global Active Power em kW) com base em variáveis elétricas e temporais.

---

## 👥 Integrantes e RAs

| Nome | RA |
|------|----|
| (preencher) | (preencher) |
| (preencher) | (preencher) |
| (preencher) | (preencher) |

---

## 📌 Descrição do Problema

O consumo de energia elétrica residencial varia ao longo do dia, da semana e das estações do ano. Prever esse consumo com antecedência permite um uso mais eficiente da energia, redução de custos e melhor planejamento energético. Este projeto utiliza dados reais de uma residência francesa coletados entre 2006 e 2010 para construir um modelo preditivo do consumo de potência ativa global.

---

## 🎯 Objetivo do Projeto

Desenvolver um modelo de regressão capaz de prever o valor de `Global_active_power` (potência ativa global em kW) a partir de variáveis elétricas medidas no mesmo instante e de variáveis temporais e de histórico (lags), e disponibilizar esse modelo em uma aplicação web interativa via Streamlit.

---

## 📂 Dataset Utilizado

- **Nome:** UCI Household Electric Power Consumption
- **Fonte:** [UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/235/individual+household+electric+power+consumption)
- **Período:** Dezembro de 2006 a Novembro de 2010
- **Registros originais:** ~2 milhões de medições por minuto
- **Após agregação horária e limpeza:** ~34.000 registros
- **Variável-alvo:** `Global_active_power` (kW)

---

## 🤖 Tipo de Problema de Machine Learning

**Regressão supervisionada** — o modelo aprende a partir de dados históricos rotulados para prever um valor numérico contínuo (consumo em kW).

---

## 🔬 Metodologia

1. Carregamento e inspeção do dataset
2. Tratamento de valores ausentes (remoção de registros com `?`)
3. Agregação dos dados por hora (média horária)
4. Engenharia de features: criação de variáveis temporais (`hour`, `day_of_week`, `month`, `is_weekend`) e lags de consumo (`lag_1h`, `lag_24h`)
5. Remoção de outliers com método IQR
6. Separação cronológica dos dados: **70% treino / 15% validação / 15% teste** (sem embaralhamento, respeitando a ordem temporal)
7. Padronização das features com `StandardScaler`
8. Treinamento e comparação de três modelos
9. Seleção do melhor modelo com base nas métricas
10. Salvamento do modelo final com `pickle`
11. Deploy da aplicação no Streamlit Community Cloud

---

## 🧪 Modelos Treinados

| Modelo | R² (teste) | MAE (teste) | RMSE (teste) |
|--------|-----------|-------------|--------------|
| Regressão Linear | — | — | — |
| Regressão Polinomial | — | — | — |
| **Random Forest** | **≈ 0.999** | **≈ 0.017 kW** | **≈ 0.024 kW** |

> Preencha os valores exatos das métricas conforme os resultados do notebook.

---

## 🏆 Modelo Final Escolhido

**Random Forest Regressor** — apresentou o melhor desempenho em todas as métricas avaliadas, com alta capacidade de capturar relações não-lineares entre as variáveis e robustez a outliers.

**Parâmetros utilizados:**
- `n_estimators=200`
- `max_depth=15`
- `min_samples_leaf=5`
- `random_state=42`

---

## 📊 Métricas de Avaliação

- **R² (Coeficiente de Determinação):** mede a proporção da variância explicada pelo modelo. Quanto mais próximo de 1, melhor.
- **MAE (Mean Absolute Error):** erro médio absoluto em kW. Indica o desvio médio das previsões.
- **RMSE (Root Mean Squared Error):** raiz do erro quadrático médio, penaliza erros maiores.

---

## 📈 Principais Resultados

- O Random Forest obteve R² ≈ 0.999 no conjunto de teste, indicando excelente ajuste.
- As features mais importantes foram os sub-medidores, a intensidade global e os lags de consumo.
- A divisão cronológica garantiu que o modelo fosse avaliado em dados futuros, simulando um cenário real.

---

## 🗂️ Estrutura dos Arquivos

```
previsao-consumo-energia/
│
├── app.py                          # Aplicação Streamlit
├── modelo_final.pkl                # Modelo Random Forest salvo
├── scaler.pkl                      # StandardScaler salvo
├── requirements.txt                # Dependências do projeto
├── README.md                       # Documentação do projeto
│
├── notebooks/
│   └── notebook_atualizado.ipynb   # Notebook revisado com todo o pipeline
│
└── reports/
    └── relatorio_atualizado.pdf    # Relatório final em PDF
```

> O dataset (`household_power_consumption.txt`) não está incluído no repositório por conta do tamanho. Baixe diretamente no [UCI Repository](https://archive.ics.uci.edu/dataset/235/individual+household+electric+power+consumption).

---

## 🛠️ Tecnologias Utilizadas

- Python 3.10+
- Pandas
- NumPy
- Scikit-learn
- Matplotlib / Seaborn
- Streamlit
- Pickle
- Google Colab (treinamento)
- GitHub (versionamento)
- Streamlit Community Cloud (deploy)

---

## ▶️ Instruções para Executar o Notebook

1. Acesse o Google Colab: [colab.research.google.com](https://colab.research.google.com)
2. Faça upload do arquivo `notebooks/notebook_atualizado.ipynb`
3. Faça upload do dataset `household_power_consumption.txt` no ambiente do Colab
4. Execute todas as células em ordem (`Runtime > Run all`)

---

## 🚀 Instruções para Executar o App Streamlit Localmente

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Execute a aplicação:
```bash
streamlit run app.py
```

> Os arquivos `modelo_final.pkl` e `scaler.pkl` já estão no repositório e serão carregados automaticamente.

---

## 🌐 Link do App Publicado

🔗 **[https://desafio-06---previs-o-de-consumo-de-energia-73wndexm6bbfhxzhuv.streamlit.app/](https://desafio-06---previs-o-de-consumo-de-energia-73wndexm6bbfhxzhuv.streamlit.app/)**

---

## ⚠️ Limitações

- **Data leakage:** o modelo utiliza variáveis do mesmo instante temporal que o target (`Global_reactive_power`, `Voltage`, `Global_intensity`, sub-medidores). Em um cenário de predição real, essas variáveis não estariam disponíveis antes da medição. As features verdadeiramente preditivas são os lags e as variáveis temporais.
- **Domínio restrito:** o modelo foi treinado com dados de uma única residência francesa. Sua generalização para outras residências ou regiões é limitada.
- **Dados históricos nos lags:** a aplicação exige que o usuário informe manualmente o consumo das últimas 1h e 24h, o que em produção seria obtido automaticamente de um banco de dados.

---

## ✅ Conclusão

O projeto demonstrou que é possível prever com alta precisão o consumo de energia elétrica residencial utilizando Random Forest. A aplicação desenvolvida em Streamlit permite que qualquer usuário insira os dados elétricos e obtenha instantaneamente a previsão de consumo com interpretação do resultado. As limitações metodológicas — especialmente o data leakage — foram identificadas e documentadas, reforçando a importância da análise crítica dos resultados mesmo quando as métricas são elevadas.

---

*Projeto desenvolvido para a disciplina de Machine Learning — UNIMAR 1/2026*
