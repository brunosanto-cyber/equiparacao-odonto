import streamlit as st
import pandas as pd

# Configuração inicial avançada da página web
st.set_page_config(
    page_title="Equiparação Corporativa - Unimed Odonto",
    page_icon="🦷",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# === DESIGN SYSTEM & CUSTOM CSS (IDENTIDADE UNIMED ODONTO) ===
st.markdown("""
    <style>
        /* Fundo da aplicação */
        .stApp {
            background-color: #FAFAFA;
        }
        
        /* Banner principal Unimed */
        .unimed-banner {
            background: linear-gradient(135deg, #00995D 0%, #004D26 100%);
            padding: 35px 30px;
            border-radius: 12px;
            color: white;
            margin-bottom: 30px;
            box-shadow: 0 4px 20px rgba(0, 153, 93, 0.15);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            position: relative;
        }
        
        /* Imagem de dente no banner */
        .tooth-banner-img {
            float: right;
            max-width: 60px;
            position: absolute;
            right: 30px;
            top: 30px;
        }
        
        .unimed-banner h1 {
            color: white !important;
            margin: 0;
            font-size: 32px;
            font-weight: 700;
        }
        .unimed-banner p {
            margin: 5px 0 0 0;
            font-size: 16px;
            opacity: 0.9;
        }
        
        /* Cards de Métricas Rápidas */
        .metric-box {
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.03);
            text-align: center;
            border-bottom: 4px solid #E2E8F0;
        }
        .metric-value {
            font-size: 32px;
            font-weight: 700;
            margin: 5px 0;
        }
        .metric-label {
            font-size: 12px;
            color: #718096;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        /* Bloco de Comparação Lado a Lado */
        .comp-card {
            background-color: white;
            padding: 25px;
            border-radius: 12px;
            box-shadow: 0 6px 16px rgba(0,0,0,0.04);
            margin-bottom: 25px;
        }
        .comp-card.concorrente {
            border-top: 5px solid #718096;
        }
        .comp-card.unimed {
            border-top: 5px solid #00995D;
            background-color: #F7FDFB;
            border-left: 1px solid #E6F4EA;
        }
        
        /* Títulos internos dos Cards */
        .card-title-concorrente { color: #4A5568; font-weight: 700; margin-top: 0; }
        .card-title-unimed { color: #00995D; font-weight: 700; margin-top: 0; }
        
        /* Badges de Cobertura SIM/NÃO */
        .badge {
            display: inline-block;
            padding: 3px 10px;
            border-radius: 12px;
            font-size: 11px;
            font-weight: 700;
            float: right;
        }
        .badge-sim { background-color: #E6F4EA; color: #137333; }
        .badge-nao { background-color: #FCE8E6; color: #C5221F; }
        
        /* Linhas da listagem de coberturas */
        .coverage-item {
            padding: 10px 0;
            border-bottom: 1px solid #EDF2F7;
            font-size: 14px;
            color: #2D3748;
        }
        
        /* Card de Conclusões Comerciais */
        .insight-box {
            background-color: white;
            padding: 25px;
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.03);
            border-left: 5px solid #004D26;
        }
    </style>
""", unsafe_allow_html=True)

# === BANCO DE DADOS ATUALIZADO E REVISADO ===
dados_planos = [
    # --- UNIMED ODONTO (Linha de Base - Ref: Página 1 e 7) ---
    {"Operadora": "Unimed ODONTO", "Plano": "Essencial", "Contratacao": "PRATELEIRA", "Rol": "SIM", "Doc": "NÃO", "Manut": "NÃO", "Prot": "NÃO", "Clar": "NÃO", "Reemb": "NÃO", "Equiv": "Essencial"},
    {"Operadora": "Unimed ODONTO", "Plano": "Essencial Plus", "Contratacao": "PRATELEIRA", "Rol": "SIM", "Doc": "SIM", "Manut": "NÃO", "Prot": "NÃO", "Clar": "NÃO", "Reemb": "NÃO", "Equiv": "Essencial Plus"},
    {"Operadora": "Unimed ODONTO", "Plano": "Essencial Plus Doc", "Contratacao": "PRATELEIRA", "Rol": "SIM", "Doc": "SIM", "Manut": "NÃO", "Prot": "NÃO", "Clar": "NÃO", "Reemb": "NÃO", "Equiv": "Essencial Plus Doc"},
    {"Operadora": "Unimed ODONTO", "Plano": "Pleno", "Contratacao": "PRATELEIRA", "Rol": "SIM", "Doc": "SIM", "Manut": "SIM", "Prot": "NÃO", "Clar": "NÃO", "Reemb": "NÃO", "Equiv": "Pleno"},
    {"Operadora": "Unimed ODONTO", "Plano": "Pleno Top", "Contratacao": "PRATELEIRA", "Rol": "SIM", "Doc": "SIM", "Manut": "SIM", "Prot": "SIM", "Clar": "SIM", "Reemb": "NÃO", "Equiv": "Pleno Top"},

    # --- ODONTOPREV (Ref: Página 1) ---
    {"Operadora": "OdontoPrev", "Plano": "Dental Júnior", "Contratacao": "Individual", "Rol": "SIM", "Doc": "NÃO", "Manut": "NÃO", "Prot": "NÃO", "Clar": "NÃO", "Reemb": "NÃO", "Equiv": "Essencial"},
    {"Operadora": "OdontoPrev", "Plano": "Bem-Estar", "Contratacao": "Individual", "Rol": "SIM", "Doc": "NÃO", "Manut": "NÃO", "Prot": "NÃO", "Clar": "NÃO", "Reemb": "NÃO", "Equiv": "Essencial"},
    {"Operadora": "OdontoPrev", "Plano": "Bem-Estar Orto", "Contratacao": "Individual", "Rol": "SIM", "Doc": "SIM", "Manut": "SIM", "Prot": "NÃO", "Clar": "NÃO", "Reemb": "NÃO", "Equiv": "Pleno"},
    {"Operadora": "OdontoPrev", "Plano": "Integral", "Contratacao": "PME e MEI", "Rol": "SIM", "Doc": "NÃO", "Manut": "NÃO", "Prot": "NÃO", "Clar": "NÃO", "Reemb": "NÃO", "Equiv": "Essencial"},
    {"Operadora": "OdontoPrev", "Plano": "Master", "Contratacao": "PME e MEI", "Rol": "SIM", "Doc": "SIM", "Manut": "SIM", "Prot": "SIM", "Clar": "SIM", "Reemb": "NÃO", "Equiv": "Pleno Top"},
    {"Operadora": "OdontoPrev", "Plano": "Convencional", "Contratacao": "Empresarial", "Rol": "SIM", "Doc": "NÃO", "Manut": "NÃO", "Prot": "NÃO", "Clar": "NÃO", "Reemb": "NÃO", "Equiv": "Essencial"},
    {"Operadora": "OdontoPrev", "Plano": "Integral Doc", "Contratacao": "Empresarial", "Rol": "SIM", "Doc": "SIM", "Manut": "NÃO", "Prot": "NÃO", "Clar": "NÃO", "Reemb": "NÃO", "Equiv": "Essencial Plus Doc"},
    {"Operadora": "OdontoPrev", "Plano": "Premium", "Contratacao": "Empresarial", "Rol": "SIM", "Doc": "SIM", "Manut": "SIM", "Prot": "SIM", "Clar": "SIM", "Reemb": "SIM", "Equiv": "Pleno Top"},
    {"Operadora": "OdontoPrev", "Plano": "Superior", "Contratacao": "Empresarial", "Rol": "SIM", "Doc": "SIM", "Manut": "NÃO", "Prot": "SIM", "Clar": "NÃO", "Reemb": "NÃO", "Equiv": "Essencial Plus Doc"},

    # --- HAPVIDA ODONTO (Ref: Página 2) ---
    {"Operadora": "Hapvida Odonto", "Plano": "Smart Odonto", "Contratacao": "Empresarial", "Rol": "SIM", "Doc": "NÃO", "Manut": "NÃO", "Prot": "NÃO", "Clar": "NÃO", "Reemb": "NÃO", "Equiv": "Essencial"},
    {"Operadora": "Hapvida Odonto", "Plano": "Top Premium DO", "Contratacao": "Empresarial", "Rol": "SIM", "Doc": "SIM", "Manut": "NÃO", "Prot": "NÃO", "Clar": "NÃO", "Reemb": "NÃO", "Equiv": "Essencial Plus Doc"},
    {"Operadora": "Hapvida Odonto", "Plano": "Top Premium Orto", "Contratacao": "Empresarial", "Rol": "SIM", "Doc": "SIM", "Manut": "SIM", "Prot": "NÃO", "Clar": "NÃO", "Reemb": "NÃO", "Equiv": "Pleno"},
    {"Operadora": "Hapvida Odonto", "Plano": "Odonto Premium Free", "Contratacao": "Individual", "Rol": "SIM", "Doc": "NÃO", "Manut": "NÃO", "Prot": "NÃO", "Clar": "NÃO", "Reemb": "NÃO", "Equiv": "Essencial"},

    # --- PORTO SEGURO (Ref: Página 2) ---
    {"Operadora": "Porto Seguro", "Plano": "Bronze 10", "Contratacao": "Empresarial", "Rol": "SIM", "Doc": "NÃO", "Manut": "NÃO", "Prot": "NÃO", "Clar": "NÃO", "Reemb": "NÃO", "Equiv": "Essencial"},
    {"Operadora": "Porto Seguro", "Plano": "Bronze Integral Doc 10", "Contratacao": "Empresarial", "Rol": "SIM", "Doc": "SIM", "Manut": "NÃO", "Prot": "NÃO", "Clar": "NÃO", "Reemb": "NÃO", "Equiv": "Essencial Plus Doc"},
    {"Operadora": "Porto Seguro", "Plano": "Ouro Premium 10", "Contratacao": "Empresarial", "Rol": "SIM", "Doc": "SIM", "Manut": "SIM", "Prot": "SIM", "Clar": "SIM", "Reemb": "SIM", "Equiv": "Pleno Top"},

    # --- SULAMÉRICA (Ref: Página 2 e 3) ---
    {"Operadora": "SulAmérica", "Plano": "Mais", "Contratacao": "Individual", "Rol": "SIM", "Doc": "SIM", "Manut": "NÃO", "Prot": "NÃO", "Clar": "NÃO", "Reemb": "NÃO", "Equiv": "Essencial Plus"},
    {"Operadora": "SulAmérica", "Plano": "Mais Doc", "Contratacao": "Individual", "Rol": "SIM", "Doc": "SIM", "Manut": "NÃO", "Prot": "NÃO", "Clar": "NÃO", "Reemb": "NÃO", "Equiv": "Essencial Plus Doc"},
    {"Operadora": "SulAmérica", "Plano": "Mais", "Contratacao": "PME e MEI", "Rol": "SIM", "Doc": "SIM", "Manut": "NÃO", "Prot": "NÃO", "Clar": "NÃO", "Reemb": "NÃO", "Equiv": "Essencial Plus"},
    {"Operadora": "SulAmérica", "Plano": "Mais Orto", "Contratacao": "Empresarial", "Rol": "SIM", "Doc": "SIM", "Manut": "SIM", "Prot": "NÃO", "Clar": "NÃO", "Reemb": "NÃO", "Equiv": "Pleno"},
    {"Operadora": "SulAmérica", "Plano": "Premium", "Contratacao": "Empresarial", "Rol": "SIM", "Doc": "SIM", "Manut": "SIM", "Prot": "SIM", "Clar": "SIM", "Reemb": "SIM", "Equiv": "Pleno Top"},

    # --- AMIL DENTAL (Ref: Página 3) ---
    {"Operadora": "Amil Dental", "Plano": "Dental 205", "Contratacao": "Individual", "Rol": "SIM", "Doc": "NÃO", "Manut": "NÃO", "Prot": "NÃO", "Clar": "NÃO", "Reemb": "NÃO", "Equiv": "Essencial"},
    {"Operadora": "Amil Dental", "Plano": "Ortodontia E80", "Contratacao": "Individual", "Rol": "SIM", "Doc": "SIM", "Manut": "SIM", "Prot": "NÃO", "Clar": "NÃO", "Reemb": "NÃO", "Equiv": "Pleno"},
    {"Operadora": "Amil Dental", "Plano": "Dental 205", "Contratacao": "Empresarial", "Rol": "SIM", "Doc": "NÃO", "Manut": "NÃO", "Prot": "NÃO", "Clar": "NÃO", "Reemb": "NÃO", "Equiv": "Essencial"},
    {"Operadora": "Amil Dental", "Plano": "Orto + Prótese E170", "Contratacao": "Empresarial", "Rol": "SIM", "Doc": "SIM", "Manut": "SIM", "Prot": "SIM", "Clar": "NÃO", "Reemb": "NÃO", "Equiv": "Pleno Top"},

    # --- METLIFE (Ref: Página 4) ---
    {"Operadora": "MetLife", "Plano": "MetLife Essencial", "Contratacao": "Individual", "Rol": "SIM", "Doc": "NÃO", "Manut": "NÃO", "Prot": "NÃO", "Clar": "NÃO", "Reemb": "NÃO", "Equiv": "Essencial"},
    {"Operadora": "MetLife", "Plano": "MetLife Doc", "Contratacao": "Individual", "Rol": "SIM", "Doc": "SIM", "Manut": "NÃO", "Prot": "NÃO", "Clar": "NÃO", "Reemb": "NÃO", "Equiv": "Essencial Plus Doc"},
    {"Operadora": "MetLife", "Plano": "Gold Doc", "Contratacao": "PME e MEI", "Rol": "SIM", "Doc": "SIM", "Manut": "NÃO", "Prot": "NÃO", "Clar": "NÃO", "Reemb": "NÃO", "Equiv": "Essencial Plus Doc"},
    {"Operadora": "MetLife", "Plano": "Premium", "Contratacao": "Empresarial", "Rol": "SIM", "Doc": "SIM", "Manut": "SIM", "Prot": "SIM", "Clar": "SIM", "Reemb": "SIM", "Equiv": "Pleno Top"},

    # --- DENTAL UNI (Ref: Página 4) ---
    {"Operadora": "Dental Uni", "Plano": "Essencial", "Contratacao": "Individual", "Rol": "SIM", "Doc": "NÃO", "Manut": "NÃO", "Prot": "NÃO", "Clar": "NÃO", "Reemb": "NÃO", "Equiv": "Essencial"},
    {"Operadora": "Dental Uni", "Plano": "Dental Amplo DOC", "Contratacao": "Empresarial", "Rol": "SIM", "Doc": "SIM", "Manut": "NÃO", "Prot": "NÃO", "Clar": "NÃO", "Reemb": "NÃO", "Equiv": "Essencial Plus Doc"},

    # --- INPAO (Ref: Página 4 e 5) ---
    {"Operadora": "INPAO Dental", "Plano": "Especial", "Contratacao": "PME e MEI", "Rol": "SIM", "Doc": "NÃO", "Manut": "NÃO", "Prot": "NÃO", "Clar": "NÃO", "Reemb": "NÃO", "Equiv": "Essencial"},
    {"Operadora": "INPAO Dental", "Plano": "Especial Orto", "Contratacao": "Empresarial", "Rol": "SIM", "Doc": "SIM", "Manut": "SIM", "Prot": "NÃO", "Clar": "NÃO", "Reemb": "NÃO", "Equiv": "Pleno"},

    # --- ODONTO EMPRESAS (Ref: Página 5) ---
    {"Operadora": "Odonto Empresas", "Plano": "Sigma", "Contratacao": "Individual", "Rol": "SIM", "Doc": "NÃO", "Manut": "NÃO", "Prot": "NÃO", "Clar": "NÃO", "Reemb": "NÃO", "Equiv": "Essencial"},
    {"Operadora": "Odonto Empresas", "Plano": "Alfa Orto", "Contratacao": "Empresarial", "Rol": "SIM", "Doc": "SIM", "Manut": "SIM", "Prot": "NÃO", "Clar": "NÃO", "Reemb": "NÃO", "Equiv": "Pleno"},

    # --- BB DENTAL (Ref: Página 5) ---
    {"Operadora": "BB Dental", "Plano": "Dental Essência", "Contratacao": "Individual", "Rol": "SIM", "Doc": "NÃO", "Manut": "NÃO", "Prot": "NÃO", "Clar": "NÃO", "Reemb": "NÃO", "Equiv": "Essencial"},
    {"Operadora": "BB Dental", "Plano": "Integral Doc", "Contratacao": "Empresarial", "Rol": "SIM", "Doc": "SIM", "Manut": "NÃO", "Prot": "NÃO", "Clar": "NÃO", "Reemb": "NÃO", "Equiv": "Essencial Plus Doc"}
]

df_base = pd.DataFrame(dados_planos)
coberturas = ["Rol", "Doc", "Manut", "Prot", "Clar", "Reemb"]
nomes_coberturas = {
    "Rol": "Rol ANS Clínico", "Doc": "Documentação Ortodôntica", 
    "Manut": "Manutenção de Aparelho", "Prot": "Próteses Além do Rol", 
    "Clar": "Clareamento Estético", "Reemb": "Reembolso"
}

# === BANNER DE ENTRADA ===
st.markdown("""
    <div class="unimed-banner">
        <img src="https://img.icons8.com/color/tooth.png" alt="Dente Icon" class="tooth-banner-img">
        <h1>🛡️ Portal Comercial Unimed Odonto</h1>
        <p>Plataforma Inteligente de Equiparação de Planos e Análise de Coberturas da Concorrência</p>
    </div>
""", unsafe_allow_html=True)

# === FILTROS DE SELEÇÃO TRIPLO (CASCATA INTELIGENTE) ===
col_box1, col_box2, col_box3 = st.columns(3)

with col_box1:
    operadoras_disponiveis = sorted([op for op in df_base["Operadora"].unique() if op != "Unimed ODONTO"])
    op_selecionada = st.selectbox("🎯 1. Escolha a Operadora Concorrente:", operadoras_disponiveis)

with col_box2:
    contratacoes_disponiveis = sorted(df_base[df_base["Operadora"] == op_selecionada]["Contratacao"].unique().tolist())
    contratacao_selecionada = st.selectbox("💼 2. Modelo de Contratação:", contratacoes_disponiveis)

with col_box3:
    planos_filtrados = df_base[(df_base["Operadora"] == op_selecionada) & (df_base["Contratacao"] == contratacao_selecionada)]["Plano"].tolist()
    plano_selecionado = st.selectbox("📋 3. Escolha o Plano da Concorrência:", planos_filtrados)

# === PROCESSAMENTO DE DADOS E DESIGN DOS RESULTADOS ===
if plano_selecionado:
    linha_cong = df_base[(df_base["Operadora"] == op_selecionada) & (df_base["Contratacao"] == contratacao_selecionada) & (df_base["Plano"] == plano_selecionado)].iloc[0]
    equiv_unimed = linha_cong["Equiv"]
    linha_uni = df_base[(df_base["Operadora"] == "Unimed ODONTO") & (df_base["Plano"] == equiv_unimed)].iloc[0]
    
    iguais, faltas, diferenciais = 0, [], []
    for cob in coberturas:
        if linha_cong[cob] == linha_uni[cob]: 
            iguais += 1
        elif linha_uni[cob] == "SIM" and linha_cong[cob] == "NÃO": 
            faltas.append(nomes_coberturas[cob])
        elif linha_cong[cob] == "SIM" and linha_uni[cob] == "NÃO": 
            diferenciais.append(nomes_coberturas[cob])
            
    porcentagem = (iguais / len(coberturas)) * 100
    color_perc = "#00995D" if porcentagem == 100 else ("#A2C027" if porcentagem >= 70 else "#E05353")

    # MÓDULO 1: INDICADORES E PORCENTAGENS DE EQUIPARAÇÃO
    st.markdown("### 📈 Indicadores de Aderência")
    col_m1, col_m2, col_m3 = st.columns(3)
    
    with col_m1:
        st.markdown(f"""
            <div class="metric-box">
                <div class="metric-label">Percentual de Equiparação</div>
                <div class="metric-value" style="color: {color_perc};">{porcentagem:.1f}%</div>
            </div>
        """, unsafe_allow_html=True)
        
    with col_m2:
        st.markdown(f"""
            <div class="metric-box">
                <div class="metric-label">Recomendação Unimed</div>
                <div class="metric-value" style="color: #004D26; font-size:24px; padding-top:8px;">{equiv_unimed}</div>
            </div>
        """, unsafe_allow_html=True)
        
    with col_m3:
        status_venda = "Par Perfeito" if porcentagem == 100 else ("Equivalente" if porcentagem >= 70 else "Ajuste Necessário")
        st.markdown(f"""
            <div class="metric-box">
                <div class="metric-label">Status Comercial</div>
                <div class="metric-value" style="color: #4A5568; font-size:26px; padding-top:5px;">{status_venda}</div>
            </div>
        """, unsafe_allow_html=True)

    # Barra visual de progresso estilizada
    st.markdown(f"""
        <div style="width: 100%; background-color: #E2E8F0; border-radius: 4px; margin-bottom: 35px; height: 8px;">
            <div style="width: {porcentagem}%; background-color: {color_perc}; height: 100%; border-radius: 4px;"></div>
        </div>
    """, unsafe_allow_html=True)

    # MÓDULO 2: COMPARATIVO TÉCNICO E ESTRUTURAL
    col_c1, col_c2 = st.columns(2)
    
    with col_c1:
        itens_html_cong = ""
        for c in coberturas:
            badge_class = "badge-sim" if linha_cong[c] == "SIM" else "badge-nao"
            itens_html_cong += f'<div class="coverage-item">{nomes_coberturas[c]}<span class="badge {badge_class}">{linha_cong[c]}</span></div>'
        
        html_card_cong = f"""
<div class="comp-card concorrente">
<h3 class="card-title-concorrente">🔍 Estrutura do Concorrente</h3>
<p style="font-size:15px; margin: 0 0 15px 0;"><b>{op_selecionada}</b> ({contratacao_selecionada}) — {plano_selecionado}</p>
{itens_html_cong}
</div>
"""
        st.markdown(html_card_cong, unsafe_allow_html=True)
        
    with col_c2:
        itens_html_uni = ""
        for c in coberturas:
            badge_class = "badge-sim" if linha_uni[c] == "SIM" else "badge-nao"
            itens_html_uni += f'<div class="coverage-item">{nomes_coberturas[c]}<span class="badge {badge_class}">{linha_uni[c]}</span></div>'
            
        html_card_uni = f"""
<div class="comp-card unimed">
<h3 class="card-title-unimed">🦷 Proposta Unimed Odonto</h3>
<p style="font-size:15px; margin: 0 0 15px 0; color:#006633;"><b>Par Ideal:</b> {equiv_unimed}</p>
{itens_html_uni}
</div>
"""
        st.markdown(html_card_uni, unsafe_allow_html=True)

    # MÓDULO 3: RELATÓRIO DE INSIGHTS E GAPS PARA VENDAS
    html_insights = f"""
<div class="insight-box">
<h3 style="color: #004D26; margin-top:0; font-size:18px;">💡 Estratégia de Abordagem Comercial</h3>
<p style="font-size:14px; margin-bottom:8px;">Use os argumentos técnicos abaixo para fechar o negócio:</p>
<p style="font-size:14px; margin: 4px 0;">
<span style="color:#C5221F; font-weight:700;">❌ O que o concorrente deixa a desejar (Faltas):</span><br>
<span style="color:#555; padding-left:15px; display:inline-block;">
{', '.join(faltas) if faltas else '<i>Nenhum gap negativo. O plano da concorrência possui cobertura técnica equivalente ou superior.</i>'}
</span>
</p>
<p style="font-size:14px; margin: 12px 0 4px 0;">
<span style="color:#137333; font-weight:700;">⭐ Diferenciais do Concorrente (A mais):</span><br>
<span style="color:#555; padding-left:15px; display:inline-block;">
{', '.join(diferenciais) if diferenciais else '<i>Nenhum extra detectado. A Unimed Odonto cobre rigorosamente os mesmos pontos.</i>'}
</span>
</p>
</div>
"""
    st.markdown(html_insights, unsafe_allow_html=True)
