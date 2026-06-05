import streamlit as st
import numpy as np
import pickle
import os

# ── Configuração da página ──────────────────────────────────────────────────
st.set_page_config(
    page_title="Previsão de Consumo de Energia",
    page_icon="⚡",
    layout="centered",
)

# ── CSS customizado ─────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main-header {
        font-size: 2rem;
        font-weight: 700;
        color: #1a73e8;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 0.95rem;
        color: #666;
        margin-bottom: 1.5rem;
    }
    .result-box {
        background: linear-gradient(135deg, #e8f4fd, #d0e8fb);
        border-left: 5px solid #1a73e8;
        padding: 1.2rem 1.5rem;
        border-radius: 8px;
        margin-top: 1rem;
    }
    .result-value {
        font-size: 2.2rem;
        font-weight: 800;
        color: #1a73e8;
    }
    .result-label {
        font-size: 0.9rem;
        color: #444;
        margin-top: 0.2rem;
    }
    .badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-top: 0.6rem;
    }
    .badge-low    { background: #d4edda; color: #155724; }
    .badge-medium { background: #fff3cd; color: #856404; }
    .badge-high   { background: #f8d7da; color: #721c24; }
    .section-title {
        font-size: 1.05rem;
        font-weight: 600;
        color: #333;
        border-bottom: 2px solid #e0e0e0;
        padding-bottom: 0.3rem;
        margin-bottom: 0.8rem;
    }
    .info-table td { padding: 0.3rem 0.8rem; }
    .info-table tr:nth-child(even) { background: #f7f9fc; }
</style>
""", unsafe_allow_html=True)

# ── Cabeçalho ───────────────────────────────────────────────────────────────
st.markdown('<p class="main-header">⚡ Previsão de Consumo de Energia</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Dataset: UCI Household Electric Power Consumption · Modelo: Random Forest · Grupo 6</p>', unsafe_allow_html=True)

# ── Carregar modelo ─────────────────────────────────────────────────────────
@st.cache_resource
def load_artifacts():
    base = os.path.dirname(__file__)
    with open(os.path.join(base, "modelo_final.pkl"), "rb") as f:
        model = pickle.load(f)
    with open(os.path.join(base, "scaler.pkl"), "rb") as f:
        scaler = pickle.load(f)
    return model, scaler

try:
    model, scaler = load_artifacts()
    st.success("✅ Modelo carregado com sucesso (Random Forest · R² ≈ 0.999)")
except FileNotFoundError:
    st.error("❌ Arquivos modelo_final.pkl / scaler.pkl não encontrados.")
    st.stop()

# ── Formulário de entrada ───────────────────────────────────────────────────
st.markdown("---")
st.markdown('<p class="section-title">📋 Dados de Entrada</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("**🕐 Informações Temporais**")
    hour = st.slider("Hora do dia", 0, 23, 20, help="Hora em que o consumo será previsto (0 = meia-noite)")
    day_of_week = st.selectbox(
        "Dia da semana",
        options=list(range(7)),
        format_func=lambda x: ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"][x],
        index=0,
    )
    month = st.slider("Mês", 1, 12, 6, help="Mês do ano (1 = Janeiro, 12 = Dezembro)")
    is_weekend = 1 if day_of_week >= 5 else 0
    st.info(f"Fim de semana: {'✅ Sim' if is_weekend else '❌ Não'} (calculado automaticamente)")

with col2:
    st.markdown("**⚡ Medições Elétricas**")
    global_reactive_power = st.number_input("Potência reativa global (kVAR)", 0.0, 2.0, 0.3, 0.01, format="%.3f")
    voltage = st.number_input("Tensão (V)", 220.0, 255.0, 237.0, 0.1, format="%.2f")
    global_intensity = st.number_input("Intensidade global (A)", 0.0, 50.0, 4.6, 0.1, format="%.1f")

st.markdown("**🔌 Sub-medidores (Wh)**")
c1, c2, c3 = st.columns(3)
with c1:
    sub1 = st.number_input("Sub-medidor 1\n(cozinha)", 0.0, 80.0, 0.0, 1.0, format="%.1f",
                            help="Lava-louças, forno, micro-ondas")
with c2:
    sub2 = st.number_input("Sub-medidor 2\n(lavanderia)", 0.0, 80.0, 1.0, 1.0, format="%.1f",
                            help="Máquina de lavar, secadora, geladeira")
with c3:
    sub3 = st.number_input("Sub-medidor 3\n(aquecedor/AC)", 0.0, 80.0, 17.0, 1.0, format="%.1f",
                            help="Aquecedor de água elétrico e ar-condicionado")

st.markdown("**🔄 Lags de Consumo (histórico)**")
l1, l2 = st.columns(2)
with l1:
    lag_1h = st.number_input("Consumo 1 hora atrás (kW)", 0.1, 10.0, 1.5, 0.01, format="%.3f",
                              help="Global_active_power medido 1 hora antes")
with l2:
    lag_24h = st.number_input("Consumo 24 horas atrás (kW)", 0.1, 10.0, 1.5, 0.01, format="%.3f",
                               help="Global_active_power medido 24 horas antes (mesmo horário ontem)")

# ── Botão de predição ────────────────────────────────────────────────────────
st.markdown("---")
predict_btn = st.button("🔮 Executar Predição", type="primary", use_container_width=True)

if predict_btn:
    features_order = [
        'hour', 'day_of_week', 'month', 'is_weekend',
        'Global_reactive_power', 'Voltage', 'Global_intensity',
        'Sub_metering_1', 'Sub_metering_2', 'Sub_metering_3',
        'lag_1h', 'lag_24h'
    ]

    input_data = np.array([[
        hour, day_of_week, month, is_weekend,
        global_reactive_power, voltage, global_intensity,
        sub1, sub2, sub3,
        lag_1h, lag_24h
    ]])

    input_scaled = scaler.transform(input_data)
    prediction = model.predict(input_scaled)[0]
    prediction = max(0.0, prediction)

    st.markdown("---")
    st.markdown('<p class="section-title">📊 Resultado da Predição</p>', unsafe_allow_html=True)

    if prediction < 1.0:
        nivel = "Baixo"
        badge_class = "badge-low"
        emoji = "🟢"
        descricao = "Consumo abaixo da média. Provavelmente poucos aparelhos ligados."
    elif prediction < 2.5:
        nivel = "Moderado"
        badge_class = "badge-medium"
        emoji = "🟡"
        descricao = "Consumo dentro da faixa típica de uma residência."
    else:
        nivel = "Alto"
        badge_class = "badge-high"
        emoji = "🔴"
        descricao = "Consumo elevado. Possível uso intenso de aquecimento, AC ou eletrodomésticos."

    st.markdown(f"""
    <div class="result-box">
        <div class="result-value">{prediction:.3f} kW</div>
        <div class="result-label">Potência Ativa Global prevista para a próxima hora</div>
        <span class="badge {badge_class}">{emoji} Nível de consumo: {nivel}</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"**Interpretação:** {descricao}")

    with st.expander("📋 Ver dados organizados utilizados na predição"):
        import pandas as pd
        nomes_amigaveis = {
            'hour': 'Hora do dia',
            'day_of_week': 'Dia da semana (0=Seg)',
            'month': 'Mês',
            'is_weekend': 'Fim de semana',
            'Global_reactive_power': 'Potência reativa global (kVAR)',
            'Voltage': 'Tensão (V)',
            'Global_intensity': 'Intensidade global (A)',
            'Sub_metering_1': 'Sub-medidor 1 – Cozinha (Wh)',
            'Sub_metering_2': 'Sub-medidor 2 – Lavanderia (Wh)',
            'Sub_metering_3': 'Sub-medidor 3 – Aquecedor/AC (Wh)',
            'lag_1h': 'Consumo 1h atrás (kW)',
            'lag_24h': 'Consumo 24h atrás (kW)',
        }
        valores = [hour, day_of_week, month, is_weekend,
                   global_reactive_power, voltage, global_intensity,
                   sub1, sub2, sub3, lag_1h, lag_24h]
        df_input = pd.DataFrame({
            'Variável': [nomes_amigaveis[f] for f in features_order],
            'Valor': valores
        })
        st.dataframe(df_input, use_container_width=True, hide_index=True)

# ── Rodapé ───────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<small>
📌 <b>Sobre o modelo:</b> Random Forest Regressor treinado com dados do UCI Household Electric Power Consumption
(2006–2010, ~300 mil registros, agrupados por hora). Features incluem variáveis temporais (hora, dia, mês),
medições elétricas e lags de consumo (1h e 24h). Divisão cronológica 70/15/15 sem embaralhamento.
R² ≈ 0.999 · MAE ≈ 0.017 kW · RMSE ≈ 0.024 kW.<br><br>
⚠️ <b>Nota metodológica:</b> O modelo inclui variáveis do mesmo instante temporal (potência reativa, tensão, intensidade,
sub-medidores), o que pode caracterizar data leakage em cenário real. As features de lag representam o componente
verdadeiramente preditivo do modelo.
</small>
""", unsafe_allow_html=True)
