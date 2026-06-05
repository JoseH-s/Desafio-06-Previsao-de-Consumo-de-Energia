# Previsão de Consumo de Energia — Grupo 6

Aplicação Streamlit para prever o consumo de energia elétrica residencial (Global Active Power em kW) usando Random Forest.

**Dataset:** UCI Household Electric Power Consumption  
**Modelos treinados:** Regressão Linear, Regressão Polinomial, Random Forest  
**Melhor modelo:** Random Forest (R² ≈ 0.999, MAE ≈ 0.017 kW)

---

## 📁 Estrutura do repositório

```
├── app.py                              # Aplicação Streamlit
├── model.joblib                          # Modelo Random Forest salvo
├── scaler.joblib                        # StandardScaler salvo
├── requirements.txt                    # Dependências Python
└── household_power_consumption.txt     # Dataset UCI (não incluído — baixar separado)
```

---

## 🚀 Como rodar localmente

### 1. Instalar dependências
```bash
pip install -r requirements.txt
```

### 2. Baixar o dataset
Baixe o arquivo `household_power_consumption.txt` do [UCI Repository](https://archive.ics.uci.edu/dataset/235/individual+household+electric+power+consumption)
e coloque na raiz do projeto.

### 3. Treinar e salvar o modelo
```bash
python train_model.py
```
Isso gera os arquivos `model.pkl` e `scaler.pkl`.

### 4. Rodar a aplicação
```bash
streamlit run app.py
```

---

## ☁️ Deploy no Streamlit Community Cloud

1. Crie um repositório no GitHub e suba os arquivos:
   - `app.py`
   - `model.joblib` ← **obrigatório** (gere localmente e suba)
   - `scaler.joblib` ← **obrigatório** (gere localmente e suba)
   - `requirements.txt`

2. Acesse [share.streamlit.io](https://share.streamlit.io) e faça login com GitHub.

3. Clique em **"New app"**, selecione o repositório e defina:
   - **Branch:** main
   - **Main file path:** app.py

4. Clique em **Deploy** e aguarde. O link público será gerado automaticamente.

> ⚠️ Os arquivos `model.joblib` e `scaler.joblib` precisam estar no repositório GitHub.
> O dataset **não** precisa estar no repositório após o treinamento.

---

## 🔢 Variáveis de entrada do modelo

| Variável | Descrição |
|---|---|
| `hour` | Hora do dia (0–23) |
| `day_of_week` | Dia da semana (0=Segunda … 6=Domingo) |
| `month` | Mês (1–12) |
| `is_weekend` | Fim de semana (calculado automaticamente) |
| `Global_reactive_power` | Potência reativa global (kVAR) |
| `Voltage` | Tensão elétrica (V) |
| `Global_intensity` | Intensidade global (A) |
| `Sub_metering_1` | Sub-medidor 1 – Cozinha (Wh) |
| `Sub_metering_2` | Sub-medidor 2 – Lavanderia (Wh) |
| `Sub_metering_3` | Sub-medidor 3 – Aquecedor/AC (Wh) |
| `lag_1h` | Consumo da hora anterior (kW) |
| `lag_24h` | Consumo 24 horas atrás (kW) |

---

## ⚠️ Nota metodológica (devolutiva P1)

O modelo inclui variáveis contemporâneas ao target (potência reativa, tensão, intensidade, sub-medidores),
o que pode caracterizar **data leakage** em cenário de predição real. Em produção, apenas as features de
lag (lag_1h, lag_24h) e as temporais (hora, dia, mês) estariam disponíveis antes do momento de predição.
Os resultados elevados (R² ≈ 0.999) refletem parcialmente essa limitação metodológica.
