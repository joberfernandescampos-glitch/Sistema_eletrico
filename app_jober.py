import streamlit as st
import cmath
import math
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Configuração da página web (Título da aba do navegador)
st.set_page_config(page_title="COMPONENTES SIMÉTRICAS", layout="wide")

# Título Principal da Página
st.title("⚡JOBER - COMPONENTES SIMÉTRICAS")
st.write("Insira os valores das correntes de fase para calcular e plotar as componentes de sequência.")

# Criando colunas para organizar as entradas do operador
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Fase A")
    Ia_mod = st.number_input("Ia - Módulo (A)", value=20.0, step=1.0, key="ia_m")
    Ia_ang = st.number_input("Ia - Ângulo (°)", value=0.0, step=1.0, key="ia_a")

with col2:
    st.subheader("Fase B")
    Ib_mod = st.number_input("Ib - Módulo (A)", value=30.0, step=1.0, key="ib_m")
    Ib_ang = st.number_input("Ib - Ângulo (°)", value=-120.0, step=1.0, key="ib_a")

with col3:
    st.subheader("Fase C")
    Ic_mod = st.number_input("Ic - Módulo (A)", value=40.0, step=1.0, key="ic_m")
    Ic_ang = st.number_input("Ic - Ângulo (°)", value=120.0, step=1.0, key="ic_a")

# Cálculos Matemáticos
a = cmath.rect(1, math.radians(120))
a2 = a * a

Ia = cmath.rect(Ia_mod, math.radians(Ia_ang))
Ib = cmath.rect(Ib_mod, math.radians(Ib_ang))
Ic = cmath.rect(Ic_mod, math.radians(Ic_ang))

I0 = (Ia + Ib + Ic) / 3
I1 = (Ia + a * Ib + a2 * Ic) / 3
I2 = (Ia + a2 * Ib + a * Ic) / 3

def formatar_polar(c):
    mod, rad = cmath.polar(c)
    ang = math.degrees(rad)
    if mod < 1e-4: ang = 0.0
    return mod, ang

I0_mod, I0_ang = formatar_polar(I0)
I1_mod, I1_ang = formatar_polar(I1)
I2_mod, I2_ang = formatar_polar(I2)

st.markdown("---")

# Criando colunas para os Resultados e Gráficos
col_res, col_graf = st.columns(2)

with col_res:
    st.subheader("📊 Resultados")
    
    st.markdown("**Correntes de Fase (Entrada):**")
    st.code(f"Ia = {Ia_mod:.4f} |_ {Ia_ang:.2f}° A\n"
            f"Ib = {Ib_mod:.4f} |_ {Ib_ang:.2f}° A\n"
            f"Ic = {Ic_mod:.4f} |_ {Ic_ang:.2f}° A")
    
    st.markdown("**Componentes de Sequência:**")
    st.code(f"I0 = {I0_mod:.4f} |_ {I0_ang:.2f}° A\n"
            f"I1 = {I1_mod:.4f} |_ {I1_ang:.2f}° A\n"
            f"I2 = {I2_mod:.4f} |_ {I2_ang:.2f}° A", language="text")

with col_graf:
    st.subheader("📈 Gráficos dos Fasores")
    
    # Gerando a figura polar
    fig, (ax1, ax2) = plt.subplots(1, 2, subplot_kw={'projection': 'polar'}, figsize=(9, 4.5))
    
    # Define o limite máximo do raio dinamicamente com folga
    max_raio = float(max(Ia_mod, Ib_mod, Ic_mod, 1.0) * 1.1)
    
    # --- Gráfico 1: Fases ---
    ax1.set_ylim(0, max_raio)
    
    ax1.annotate('', xy=(math.radians(Ia_ang), Ia_mod), xytext=(0,0), 
                 xycoords='data', textcoords='data',
                 arrowprops=dict(arrowstyle="->", color='red', lw=2.5))
                 
    ax1.annotate('', xy=(math.radians(Ib_ang), Ib_mod), xytext=(0,0), 
                 xycoords='data', textcoords='data',
                 arrowprops=dict(arrowstyle="->", color='green', lw=2.5))
                 
    ax1.annotate('', xy=(math.radians(Ic_ang), Ic_mod), xytext=(0,0), 
                 xycoords='data', textcoords='data',
                 arrowprops=dict(arrowstyle="->", color='blue', lw=2.5))
                 
    ax1.set_title("Fases (Ia, Ib, Ic)", va='bottom', color='darkblue', weight='bold')
    
    # Legendas
    ax1.plot([], [], color='red', label='Ia')
    ax1.plot([], [], color='green', label='Ib')
    ax1.plot([], [], color='blue', label='Ic')
    ax1.legend(loc='lower left', bbox_to_anchor=(-0.2, -0.2), fontsize=9)

    # --- Gráfico 2: Sequências ---
    ax2.set_ylim(0, max_raio)
    
    ax2.annotate('', xy=(math.radians(I0_ang), I0_mod), xytext=(0,0), 
                 xycoords='data', textcoords='data',
                 arrowprops=dict(arrowstyle="->", color='orange', lw=2.5))
                 
    ax2.annotate('', xy=(math.radians(I1_ang), I1_mod), xytext=(0,0), 
                 xycoords='data', textcoords='data',
                 arrowprops=dict(arrowstyle="->", color='purple', lw=2.5))
                 
    ax2.annotate('', xy=(math.radians(I2_ang), I2_mod), xytext=(0,0), 
                 xycoords='data', textcoords='data',
                 arrowprops=dict(arrowstyle="->", color='brown', lw=2.5))
                 
    ax2.set_title("Sequências (I0, I1, I2)", va='bottom', color='darkcyan', weight='bold')
    
    # Legendas
    ax2.plot([], [], color='orange', label='I0 (Zero)')
    ax2.plot([], [], color='purple', label='I1 (Pos)')
    ax2.plot([], [], color='brown', label='I2 (Neg)')
    ax2.legend(loc='lower left', bbox_to_anchor=(-0.2, -0.2), fontsize=9)

    plt.tight_layout()
    st.pyplot(fig)
