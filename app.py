import streamlit as st
import pandas as pd
import base64
import os

# Configuração inicial da página
st.set_page_config(
    page_title="Equiparação Corporativa - Unimed Odonto",
    page_icon="🦷",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# === FUNÇÃO: CONVERSÃO DA LOGO PARA BASE64 ===
def obter_logo_base64(caminho_imagem):
    if os.path.exists(caminho_imagem):
        with open(caminho_imagem, "rb") as arquivo_img:
            return f"data:image/png;base64,{base64.b64encode(arquivo_img.read()).decode()}"
    return "https://img.icons8.com/color/tooth.png"

logo_unimed_html = obter_logo_base64("foto.png")

# === DESIGN SYSTEM: BLINDAGEM DE CORES (FIXO PARA MODO CLARO E ESCURO) ===
st.markdown(f"""
    <style>
        /* Fundo geral da página */
        .stApp {{
            background-color: #F0F2F6 !important;
        }}

        /* BANNER PRINCIPAL - Cores Unimed Odonto Travadas */
        .unimed-banner-blindado {{
            background: linear-gradient(135deg, #00995D 0%, #004D26 100%) !important;
            padding: 30px !important;
            border-radius: 15px !important;
            margin-bottom: 25px !important;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1) !important;
            color: white !important;
        }}

        /* CARDS DE MÉTRICAS - Fundo branco e texto escuro fixos */
        .metric-card-blindado {{
            background-color: #FFFFFF !important;
            padding: 20px !important;
            border-radius: 12px !important;
            border-bottom: 5px solid #00995D !important;
            text-align: center !important;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05) !important;
        }}
        .metric-label-blindado {{
            color: #555555 !important;
            font-size: 13px !important;
            font-weight: 600 !important;
            text-transform: uppercase !important;
        }}
        .metric-value-blindado {{
            font-size: 28px !important;
            font-weight: 700 !important;
            margin-top: 5px !important;
        }}

        /* CARDS COMPARATIVOS - Blindagem contra modo escuro */
        .comp-card-blindado {{
            background-color: #FFFFFF !important;
            padding: 25px !important;
            border-radius: 12px !important;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08) !important;
            margin-bottom: 20px !important;
            min-height: 450px !important;
        }}
        
        /* Títulos e Textos dentro dos cards */
        .card-title-text {{
            font-size: 22px !important;
            font-weight: 700 !important;
            margin-bottom: 15px !important;
            display: flex !important;
            align-items: center !important;
            gap: 10px !important;
        }}
        
        .coverage-item-blindado {{
            padding: 12px 0 !important;
            border-bottom: 1px solid #EEEEEE !important;
            color: #333333 !important; /* Texto escuro sempre visível */
            font-size: 15px !important;
            display: flex !important;
            justify-content: space-between !important;
            align-items: center !important;
        }}

        /* Badges de SIM/NÃO */
        .badge-sim-fixo {{ background-color: #E6F4EA !important; color: #137333 !important; padding: 4px 12px !important; border-radius: 20px !important; font-weight: 700 !important; font-size: 12px !important; }}
        .badge-nao-fixo {{ background-color: #FCE8E6 !important; color: #C5221F !important; padding: 4px 12px !important; border-radius: 20px !important; font-weight: 700 !important; font-size: 12px !important; }}

        /* Títulos de seção fora de cards */
        .section-header-fixo {{
            color: #1E293B !important;
            font-weight: 700 !important;
            margin: 20px 0 !important;
        }}
    </style>
""", unsafe_allow_html=True)

# === BANCO DE DADOS (DADOS DOS DOCUMENTOS ANEXADOS) ===
dados_planos = [
    {"Operadora": "Unimed ODONTO", "Plano": "Essencial", "Contratacao": "PRATELEIRA", "Rol": "SIM", "Doc": "NÃO", "Manut": "NÃO", "Prot": "NÃO", "Clar": "NÃO", "Reemb": "NÃO", "Equiv": "Essencial"},
    {"Operadora": "Unimed ODONTO", "Plano": "Essencial Plus", "Contratacao": "PRATELEIRA", "Rol": "SIM", "Doc": "SIM", "Manut": "NÃO", "Prot": "NÃO", "Clar": "NÃO", "Reemb": "NÃO", "Equiv": "Essencial Plus"},
    {"Operadora": "Unimed ODONTO", "Plano": "Essencial Plus Doc", "Contratacao": "PRATELEIRA", "Rol": "SIM", "Doc": "SIM", "Manut": "NÃO", "Prot": "NÃO", "Clar": "NÃO", "Reemb": "NÃO", "Equiv": "Essencial Plus Doc"},
    {"Operadora": "Unimed ODONTO", "Plano": "Pleno", "Contratacao": "PRATELEIRA", "Rol": "SIM", "Doc": "SIM", "Manut": "SIM", "Prot": "NÃO", "Clar": "NÃO", "Reemb": "NÃO", "Equiv": "Pleno"},
    {"Operadora": "Unimed ODONTO", "Plano": "Pleno Top", "Contratacao": "PRATELEIRA", "Rol": "SIM", "Doc": "SIM", "Manut": "SIM", "Prot": "SIM", "Clar": "SIM", "Reemb": "NÃO", "Equiv": "Pleno Top"},
    {"Operadora": "OdontoPrev", "Plano": "Bem-Estar Orto", "Contratacao": "Individual", "Rol": "SIM", "Doc": "SIM", "Manut": "SIM", "Prot": "NÃO", "Clar": "NÃO", "Reemb": "NÃO", "Equiv": "Pleno"},
    {"Operadora": "OdontoPrev", "Plano": "Master", "Contratacao": "PME e MEI", "Rol": "SIM", "Doc": "SIM", "Manut": "SIM", "Prot": "SIM", "Clar": "SIM", "Reemb": "NÃO", "Equiv": "Pleno Top"},
    {"Operadora": "OdontoPrev", "Plano": "Premium", "Contratacao": "Empresarial", "Rol": "SIM", "Doc": "SIM", "Manut": "SIM", "Prot": "SIM", "Clar": "SIM", "Reemb": "SIM", "Equiv": "Pleno Top"},
    {"Operadora": "Hapvida Odonto", "Plano": "Top Premium Orto", "Contratacao": "Empresarial", "Rol": "SIM", "Doc": "SIM", "Manut": "SIM", "Prot": "NÃO", "Clar": "NÃO", "Reemb": "NÃO", "Equiv": "Pleno"},
    {"Operadora": "MetLife", "Plano": "Premium", "Contratacao": "Empresarial", "Rol": "SIM", "Doc": "SIM", "Manut": "SIM", "Prot": "SIM", "Clar": "SIM", "Reemb": "SIM", "Equiv": "Pleno Top"},
    {"Operadora": "Amil Dental", "Plano": "Dental 205", "Contratacao": "Individual", "Rol": "SIM", "Doc": "NÃO", "Manut": "NÃO", "Prot": "NÃO", "Clar": "NÃO", "Reemb": "NÃO", "Equiv": "Essencial"},
    {"Operadora": "Amil Dental", "Plano": "Orto + Prótese E170", "Contratacao": "Empresarial", "Rol": "SIM", "Doc": "SIM", "Manut": "SIM", "Prot": "SIM", "Clar": "NÃO", "Reemb": "NÃO", "Equiv": "Pleno Top"}
]

df_base = pd.DataFrame(dados_planos)
coberturas = ["Rol", "Doc", "Manut", "Prot", "Clar", "Reemb"]
nomes_cobs = {"Rol": "Rol ANS Clínico", "Doc": "Documentação Ortodôntica", "Manut": "Manutenção de Aparelho", "Prot": "Próteses Além do Rol", "Clar": "Clareamento Estético", "Reemb": "Reembolso"}

# === UI: CABEÇALHO ===
st.markdown(f"""
    <div class="unimed-banner-blindado">
        <div style="display: flex; align-items: center; gap: 20px;">
            <img src="{logo_unimed_html}" style="max-height: 60px; border-radius: 8px;">
            <h1 style="margin:0; color: white !important; font-size: 32px; border:none;">Portal Equivalência de Planos - Odonto</h1>
        </div>
        <p style="margin: 10px 0 0 80px; color: white !important; opacity: 0.9;">Análise de Coberturas e Equiparação Inteligente de Mercado</p>
    </div>
""", unsafe_allow_html=True)

# === FILTROS ===
col1, col2, col3 = st.columns(3)
with col1:
    op_sel = st.selectbox("🎯 Operadora Concorrente:", sorted([op for op in df_base["Operadora"].unique() if op != "Unimed ODONTO"]))
with col2:
    mod_sel = st.selectbox("💼 Modelo de Contratação:", sorted(df_base[df_base["Operadora"] == op_sel]["Contratacao"].unique()))
with col3:
    plano_sel = st.selectbox("📋 Plano da Concorrência:", df_base[(df_base["Operadora"] == op_sel) & (df_base["Contratacao"] == mod_sel)]["Plano"].tolist())

# === PROCESSAMENTO ===
if plano_sel:
    linha_cong = df_base[(df_base["Operadora"] == op_sel) & (df_base["Plano"] == plano_sel)].iloc[0]
    equiv_uni = linha_cong["Equiv"]
    linha_uni = df_base[(df_base["Operadora"] == "Unimed ODONTO") & (df_base["Plano"] == equiv_uni)].iloc[0]

    iguais, faltas, diferenciais = 0, [], []
    for c in coberturas:
        if linha_cong[c] == linha_uni[c]: iguais += 1
        elif linha_uni[c] == "SIM" and linha_cong[c] == "NÃO": faltas.append(nomes_cobs[c])
        elif linha_cong[c] == "SIM" and linha_uni[c] == "NÃO": diferenciais.append(nomes_cobs[c])
    
    porcentagem = (iguais / 6) * 100
    cor_perc = "#00995D" if porcentagem == 100 else ("#A2C027" if porcentagem >= 70 else "#E05353")

    # Módulo de Indicadores
    st.markdown("<h3 class='section-header-fixo'>📊 Indicadores de Aderência</h3>", unsafe_allow_html=True)
    m_col1, m_col2, m_col3 = st.columns(3)
    
    with m_col1:
        st.markdown(f'<div class="metric-card-blindado"><div class="metric-label-blindado">Equiparação</div><div class="metric-value-blindado" style="color:{cor_perc} !important;">{porcentagem:.1f}%</div></div>', unsafe_allow_html=True)
    with m_col2:
        st.markdown(f'<div class="metric-card-blindado"><div class="metric-label-blindado">Sugestão Unimed</div><div class="metric-value-blindado" style="color:#004D26 !important;">{equiv_uni}</div></div>', unsafe_allow_html=True)
    with m_col3:
        status = "Par Perfeito" if porcentagem == 100 else ("Equivalente" if porcentagem >= 70 else "Gap Técnico")
        st.markdown(f'<div class="metric-card-blindado"><div class="metric-label-blindado">Status Comercial</div><div class="metric-value-blindado" style="color:#2D3748 !important;">{status}</div></div>', unsafe_allow_html=True)

    st.markdown(f'<div style="width:100%; background:#DDD; height:8px; border-radius:4px; margin:20px 0;"><div style="width:{porcentagem}%; background:{cor_perc}; height:100%; border-radius:4px;"></div></div>', unsafe_allow_html=True)

    # Módulo Comparativo Lado a Lado
    c_col1, c_col2 = st.columns(2)
    
    with c_col1:
        cobs_html = "".join([f'<div class="coverage-item-blindado">{nomes_cobs[c]} <span class="{"badge-sim-fixo" if linha_cong[c]=="SIM" else "badge-nao-fixo"}">{linha_cong[c]}</span></div>' for c in coberturas])
        st.markdown(f"""
            <div class="comp-card-blindado" style="border-top: 6px solid #718096 !important;">
                <div class="card-title-text" style="color: #2D3748 !important;">🔍 {op_sel} — {plano_sel}</div>
                <p style="color: #666 !important; font-size: 14px; margin-bottom: 20px;">Modalidade: {mod_sel}</p>
                {cobs_html}
            </div>
        """, unsafe_allow_html=True)

    with c_col2:
        uni_html = "".join([f'<div class="coverage-item-blindado">{nomes_cobs[c]} <span class="{"badge-sim-fixo" if linha_uni[c]=="SIM" else "badge-nao-fixo"}">{linha_uni[c]}</span></div>' for c in coberturas])
        st.markdown(f"""
            <div class="comp-card-blindado" style="border-top: 6px solid #00995D !important; background-color: #F7FDFB !important;">
                <div class="card-title-text" style="color: #00995D !important;">🦷 Unimed ODONTO — {equiv_uni}</div>
                <p style="color: #004D26 !important; font-size: 14px; margin-bottom: 20px;">Par Ideal Mapeado</p>
                {uni_html}
            </div>
        """, unsafe_allow_html=True)

    # Insights
    st.markdown(f"""
        <div class="insight-box" style="background-color: white !important; border-left: 6px solid #004D26 !important; padding: 20px !important;">
            <h4 style="color: #004D26 !important; margin-top:0;">💡 Argumentos de Vendas</h4>
            <p style="color: #333 !important; margin: 10px 0;"><b>Gap Negativo (Falta no Concorrente):</b><br> <span style="color:#C5221F;">{", ".join(faltas) if faltas else "Plano Concorrente cobre tudo."}</span></p>
            <p style="color: #333 !important; margin: 10px 0;"><b>Diferencial Concorrente:</b><br> <span style="color:#137333;">{", ".join(diferenciais) if diferenciais else "Nenhum diferencial extra detectado."}</span></p>
        </div>
    """, unsafe_allow_html=True)
