import cmath
import math
import numpy as np
import plotly.graph_objects as go
import streamlit as st

# Configuração da página (Tema Escuro e Layout Amplo)
st.set_page_config(
    page_title="Sintetizador de Neutro", 
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

# Função auxiliar para manter o ângulo entre -180° e 180°
def ajustar_angulo(ang):
    while ang > 180: ang -= 360
    while ang <= -180: ang += 360
    return ang

# --- TÍTULO PRINCIPAL ---
st.markdown("# ⚡ JÓBER FERNANDES - SINTETIZADOR DE NEUTRO")
st.markdown("<p style='color: #8b949e;'>Estipule o valor da corrente que deseja que circule pelo Neutro (In). O sistema calculará o desequilíbrio exato necessário para as fases.</p>", unsafe_allow_html=True)

# --- 1. ENTRADA DE DADOS EM COLUNAS ---
col_s1, col_s2 = st.columns(2)

with col_s1:
    st.markdown("### 🎯 Neutro Alvo Desejado")
    in_mag_alvo = st.number_input("Módulo do Neutro Desejado (In) [A]:", min_value=0.0, value=50.0, step=1.0, format="%.2f", key="in_m_alvo")
    in_ang_alvo = st.number_input("Ângulo do Neutro Desejado (°) :", min_value=-360.0, max_value=360.0, value=0.0, step=1.0, format="%.2f", key="in_a_alvo")

with col_s2:
    st.markdown("### ⚖️ Carga de Base Equilibrada")
    i_base = st.number_input("Corrente de Base equilibrada para as Fases B e C [A]:", min_value=0.0, value=100.0, step=5.0, format="%.2f", key="i_base_fases")

# --- 2. PROCESSAMENTO MATEMÁTICO VETORIAL ---
# Lógica: In = Ia + Ib + Ic  ->  Ia = In - Ib - Ic
In_alvo = cmath.rect(in_mag_alvo, math.radians(in_ang_alvo))
Ib_sint = cmath.rect(i_base, math.radians(240))  # Fase B fixa em 240° (-120°)
Ic_sint = cmath.rect(i_base, math.radians(120))  # Fase C fixa em 120°

Ia_sint = In_alvo - Ib_sint - Ic_sint
mod_Ia_sint, ang_Ia_sint = cmath.polar(Ia_sint)
ang_Ia_graus = ajustar_angulo(math.degrees(ang_Ia_sint))

# --- 3. LAYOUT INFERIOR (Resultados à esquerda, Gráfico à direita) ---
col_res, col_graf = st.columns([1, 2])

with col_res:
    st.markdown("### 📋 Resultados")
    st.markdown("Ajuste as fases com os seguintes valores para obter o neutro desejado:")
    
    st.markdown(f"<span style='color:#ff4b4b;'>**Ia (Sintetizada) :**</span> {mod_Ia_sint:.4f}  |  {ang_Ia_graus:.2f}°  A", unsafe_allow_html=True)
    st.markdown(f"<span style='color:#00cc96;'>**Ib (Base Fixa)   :**</span> {i_base:.4f}  |  -120.00°  A", unsafe_allow_html=True)
    st.markdown(f"<span style='color:#636efa;'>**Ic (Base Fixa)   :**</span> {i_base:.4f}  |  120.00°  A", unsafe_allow_html=True)
    
    st.markdown("<br>**Neutro Resultante:**", unsafe_allow_html=True)
    st.markdown(f"<span style='color:orange;'>**In Conquistado :**</span> {in_mag_alvo:.4f}  |  {ajustar_angulo(in_ang_alvo):.2f}°  A", unsafe_allow_html=True)

with col_graf:
    st.markdown("### 📈 Diagrama Fasorial Interativo")
    
    fig = go.Figure()
    
    # Adicionando os fasores de fase
    fig.add_trace(go.Scatterpolar(r=[0, mod_Ia_sint], theta=[0, ang_Ia_graus], mode='lines+markers', name='Ia (Sintetizada)', line=dict(color='#ff4b4b', width=3)))
    fig.add_trace(go.Scatterpolar(r=[0, i_base], theta=[0, -120], mode='lines+markers', name='Ib (Base)', line=dict(color='#00cc96', width=3)))
    fig.add_trace(go.Scatterpolar(r=[0, i_base], theta=[0, 120], mode='lines+markers', name='Ic (Base)', line=dict(color='#636efa', width=3)))
    
    # Adicionando o fasor de neutro resultante alvo
    fig.add_trace(go.Scatterpolar(r=[0, in_mag_alvo], theta=[0, in_ang_alvo], mode='lines+markers', name='In Alvo', line=dict(color='orange', width=4, dash='dash')))
    
    # Configuração do gráfico polar interativo
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#161b22",
        plot_bgcolor="#161b22",
        margin=dict(l=40, r=40, t=40, b=40),
        polar=dict(angularaxis=dict(direction="counterclockwise", period=360)),
        height=450
    )
    
    st.plotly_chart(fig, use_container_width=True)
