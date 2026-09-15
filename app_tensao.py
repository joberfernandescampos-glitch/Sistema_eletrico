
import streamlit as st
import numpy as np
import plotly.graph_objects as go

# Configuração da página (Tema Escuro e Layout Amplo)
st.set_page_config(
    page_title="Componentes de Tensão", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# Estilização CSS para forçar o tema Dark e ajustar os cards
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    div[data-testid="stBlock"] {
        background-color: #161b22;
        padding: 20px;
        border-radius: 8px;
        margin-bottom: 15px;
    }
    h1, h2, h3, h4, h5 { color: #ffffff !important; }
    </style>
    """, unsafe_allow_html=True)

# --- TÍTULO PRINCIPAL ---
st.markdown("# ⚡ JÓBER FERNANDES - CALCULADORA DE TENSÕES")
st.markdown("<p style='color: #8b949e;'>Insira os valores das tensões monofásicas de fase para calcular e plotar as tensões de linha correspondentes.</p>", unsafe_allow_html=True)

# --- 1. ENTRADA DE DADOS EM COLUNAS (Fase A, B e C) ---
col_A, col_B, col_C = st.columns(3)

with col_A:
    st.markdown("### Fase A")
    vA_mag = st.number_input("Va - Módulo (V)", value=127.0, step=1.0, format="%.2f", key="vA_m")
    vA_ang = st.number_input("Va - Ângulo (°)", value=0.0, step=1.0, format="%.2f", key="vA_a")

with col_B:
    st.markdown("### Fase B")
    vB_mag = st.number_input("Vb - Módulo (V)", value=127.0, step=1.0, format="%.2f", key="vB_m")
    vB_ang = st.number_input("Vb - Ângulo (°)", value=-120.0, step=1.0, format="%.2f", key="vB_a")

with col_C:
    st.markdown("### Fase C")
    vC_mag = st.number_input("Vc - Módulo (V)", value=127.0, step=1.0, format="%.2f", key="vC_m")
    vC_ang = st.number_input("Vc - Ângulo (°)", value=120.0, step=1.0, format="%.2f", key="vC_a")

# --- 2. PROCESSAMENTO MATEMÁTICO ---
V_A = vA_mag * np.exp(1j * np.radians(vA_ang))
V_B = vB_mag * np.exp(1j * np.radians(vB_ang))
V_C = vC_mag * np.exp(1j * np.radians(vC_ang))

# Tensões de linha (Fase-Fase)
V_AB = V_A - V_B
V_BC = V_B - V_C
V_CA = V_C - V_A

# Funções auxiliares para formatar strings de exibição
def format_fasor(v_complex):
    mag = np.abs(v_complex)
    ang = np.degrees(np.angle(v_complex))
    return f"{mag:.4f}  |  {ang:.2f}°  V"

# --- 3. LAYOUT INFERIOR (Resultados à esquerda, Gráficos à direita) ---
col_res, col_graf = st.columns([1, 2])

with col_res:
    st.markdown("### 📋 Resultados")
    
    st.markdown("**Tensões de Fase (Entrada):**")
    st.markdown(f"<span style='color:#ff4b4b;'>**Va :**</span> {format_fasor(V_A)}", unsafe_allow_html=True)
    st.markdown(f"<span style='color:#00cc96;'>**Vb :**</span> {format_fasor(V_B)}", unsafe_allow_html=True)
    st.markdown(f"<span style='color:#636efa;'>**Vc :**</span> {format_fasor(V_C)}", unsafe_allow_html=True)
    
    st.markdown("<br>**Tensões de Linha (Calculadas):**", unsafe_allow_html=True)
    st.markdown(f"<span style='color:#ef553b;'>**Vab :**</span> {format_fasor(V_AB)}", unsafe_allow_html=True)
    st.markdown(f"<span style='color:#00cc96;'>**Vbc :**</span> {format_fasor(V_BC)}", unsafe_allow_html=True)
    st.markdown(f"<span style='color:#ab63fa;'>**Vca :**</span> {format_fasor(V_CA)}", unsafe_allow_html=True)

with col_graf:
    st.markdown("### 📈 Gráficos dos Fasores")
    
    # Criando os subplots polares lado a lado usando Plotly
    fig = go.Figure()
    
    # Gráfico 1: TENSÕES DE FASE (Subplot Polar 1)
    fig.add_trace(go.Scatterpolar(r=[0, np.abs(V_A)], theta=[0, np.degrees(np.angle(V_A))], mode='lines+markers', name='Va (Fase)', line=dict(color='#ff4b4b', width=3), subplot='polar1'))
    fig.add_trace(go.Scatterpolar(r=[0, np.abs(V_B)], theta=[0, np.degrees(np.angle(V_B))], mode='lines+markers', name='Vb (Fase)', line=dict(color='#00cc96', width=3), subplot='polar1'))
    fig.add_trace(go.Scatterpolar(r=[0, np.abs(V_C)], theta=[0, np.degrees(np.angle(V_C))], mode='lines+markers', name='Vc (Fase)', line=dict(color='#636efa', width=3), subplot='polar1'))
    
    # Gráfico 2: TENSÕES DE LINHA (Subplot Polar 2)
    fig.add_trace(go.Scatterpolar(r=[0, np.abs(V_AB)], theta=[0, np.degrees(np.angle(V_AB))], mode='lines+markers', name='Vab (Linha)', line=dict(color='#ef553b', width=2.5, dash='dash'), subplot='polar2'))
    fig.add_trace(go.Scatterpolar(r=[0, np.abs(V_BC)], theta=[0, np.degrees(np.angle(V_BC))], mode='lines+markers', name='Vbc (Linha)', line=dict(color='#00cc96', width=2.5, dash='dash'), subplot='polar2'))
    fig.add_trace(go.Scatterpolar(r=[0, np.abs(V_CA)], theta=[0, np.degrees(np.angle(V_CA))], mode='lines+markers', name='Vca (Linha)', line=dict(color='#ab63fa', width=2.5, dash='dash'), subplot='polar2'))
    
    # Configurações do layout escuro dos gráficos polares
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#161b22",
        plot_bgcolor="#161b22",
        margin=dict(l=20, r=20, t=40, b=20),
        grid=dict(rows=1, columns=2, pattern='independent'),
        polar1=dict(domain=dict(x=[0, 0.45]), angularaxis=dict(direction="counterclockwise", period=360)),
        polar2=dict(domain=dict(x=[0.55, 1]), angularaxis=dict(direction="counterclockwise", period=360)),
        title=dict(text="Fases (Va, Vb, Vc)                       |                       Linha (Vab, Vbc, Vca)", x=0.05, y=0.95),
        legend=dict(orientation="h", y=-0.1, x=0.05)
    )
    
    st.plotly_chart(fig, use_container_width=True)
