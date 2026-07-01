import streamlit as st
import pandas as pd

# Configuração inicial avançada da página web
st.set_page_config(
    page_title="Equiparação Corporativa - Unimed Odonto",
    page_icon="🍏",
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

# === BANCO DE DADOS COMPLETO (EXTRAÍDO DO PDF) ===
dados_planos = [
    # --- UNIMED ODONTO (Linha de Base) ---
    {"Operadora": "Unimed ODONTO", "Plano": "Essencial", "Rol": "SIM", "Doc": "NÃO", "Manut": "NÃO", "Prot": "NÃO", "Clar": "NÃO", "Reemb": "NÃO", "Equiv": "Essencial"},
    {"Operadora": "Unimed ODONTO", "Plano": "Essencial Plus", "Rol": "SIM", "Doc": "SIM", "Manut": "NÃO", "Prot": "NÃO", "Clar": "NÃO", "Reemb": "NÃO", "Equiv": "Essencial Plus"},
    {"Operadora": "Unimed ODONTO", "Plano": "Essencial Plus DOC", "Rol": "SIM", "Doc": "SIM", "Manut": "NÃO", "Prot": "NÃO", "Clar": "NÃO", "Reemb": "NÃO", "Equiv": "Essencial Plus DOC"},
    {"Operadora": "Unimed ODONTO", "Plano": "Pleno", "Rol": "SIM", "Doc": "SIM", "Manut": "SIM", "Prot": "NÃO", "Clar": "NÃO", "Reemb": "NÃO", "Equiv": "Pleno"},
    {"Operadora": "Unimed ODONTO", "Plano": "Pleno Plus", "Rol": "SIM", "Doc": "SIM", "Manut": "SIM", "Prot": "SIM", "Clar": "NÃO", "Reemb": "NÃO", "Equiv": "Pleno Plus"},
    {"Operadora": "Unimed ODONTO", "Plano": "Pleno Top", "Rol": "SIM", "Doc": "SIM", "Manut": "SIM", "Prot": "SIM", "Clar": "SIM", "Reemb": "NÃO", "Equiv": "Pleno Top"},
    
    # --- SULAMÉRICA ---
    {"Operadora": "SulAmérica", "Plano": "Mais", "Rol": "SIM", "Doc": "SIM", "Manut": "NÃO", "Prot": "NÃO", "Clar": "NÃO", "Reemb": "NÃO", "Equiv": "Essencial Plus"},
    {"Operadora": "SulAmérica", "Plano": "Mais Doc", "Rol": "SIM", "Doc": "SIM", "Manut": "NÃO", "Prot": "NÃO", "Clar": "NÃO", "Reemb": "NÃO", "Equiv": "Essencial Plus DOC"},
    {"Operadora": "SulAmérica", "Plano": "Mais Clarear", "Rol": "SIM", "Doc": "SIM", "Manut": "NÃO", "Prot": "NÃO", "Clar": "SIM", "Reemb": "NÃO", "Equiv": "Pleno Top"},
    {"Operadora": "SulAmérica", "Plano": "Mais Orto", "Rol": "SIM", "Doc": "SIM", "Manut": "SIM", "Prot": "NÃO", "Clar": "NÃO", "Reemb": "NÃO", "Equiv": "Pleno"},
    {"Operadora": "SulAmérica", "Plano": "Mais Pro", "Rol": "SIM", "Doc": "SIM", "Manut": "NÃO", "Prot": "SIM", "Clar": "NÃO", "Reemb": "NÃO", "Equiv": "Pleno Plus"},
    {"Operadora": "SulAmérica", "Plano": "Premium", "Rol": "SIM", "Doc": "SIM", "Manut": "SIM", "Prot": "SIM", "Clar": "SIM", "Reemb": "SIM", "Equiv": "Pleno Top"},
    
    # --- AMIL DENTAL ---
    {"Operadora": "Amil Dental", "Plano": "Dental 205", "Rol": "SIM", "Doc": "NÃO", "Manut": "NÃO", "Prot": "NÃO", "Clar": "NÃO", "Reemb": "NÃO", "Equiv": "Essencial"},
    {"Operadora": "Amil Dental", "Plano": "Prótese Clínica E60", "Rol": "SIM", "Doc": "NÃO", "Manut": "NÃO", "Prot": "SIM", "Clar": "NÃO", "Reemb": "NÃO", "Equiv": "Pleno Plus"},
    {"Operadora": "Amil Dental", "Plano": "Prótese Estética E90", "Rol": "SIM", "Doc": "NÃO", "Manut": "NÃO", "Prot": "SIM", "Clar": "SIM", "Reemb": "NÃO", "Equiv": "Pleno Top"},
    {"Operadora": "Amil Dental", "Plano": "Ortodontia E80", "Rol": "SIM", "Doc": "SIM", "Manut": "SIM", "Prot": "NÃO", "Clar": "NÃO", "Reemb": "NÃO", "Equiv": "Pleno"},
    {"Operadora": "Amil Dental", "Plano": "Orto + Prótese E170", "Rol": "SIM", "Doc": "SIM", "Manut": "SIM", "Prot": "SIM", "Clar": "NÃO", "Reemb": "NÃO", "Equiv": "Pleno Plus"},
    
    # --- ODONTOPREV ---
    {"Operadora": "OdontoPrev", "Plano": "Integral DOC", "Rol": "SIM", "Doc": "SIM", "Manut": "NÃO", "Prot": "NÃO", "Clar": "NÃO", "Reemb": "NÃO", "Equiv": "Essencial Plus DOC"},
    {"Operadora": "OdontoPrev", "Plano": "Master", "Rol": "SIM", "Doc": "SIM", "Manut": "SIM", "Prot": "SIM", "Clar": "SIM", "Reemb": "NÃO", "Equiv": "Pleno Top"},
    {"Operadora": "OdontoPrev", "Plano": "Superior", "Rol": "SIM", "Doc": "SIM", "Manut": "NÃO", "Prot": "SIM", "Clar": "NÃO", "Reemb": "NÃO", "Equiv": "Pleno Plus"},
    
    # --- GRUPO NOTRE DAME INTERMÉDICA (GNDI) ---
    {"Operadora": "GNDI (Intermédica)", "Plano": "Smart Odonto", "Rol": "SIM", "Doc": "NÃO", "Manut": "NÃO", "Prot": "NÃO", "Clar": "NÃO", "Reemb": "NÃO", "Equiv": "Essencial"},
    {"Operadora": "GNDI (Intermédica)", "Plano": "Top Premium", "Rol": "SIM", "Doc": "SIM", "Manut": "NÃO", "Prot": "NÃO", "Clar": "NÃO", "Reemb": "NÃO", "Equiv": "Essencial Plus"},
    {"Operadora": "GNDI (Intermédica)", "Plano": "Top Premium DO", "Rol": "SIM", "Doc": "SIM", "Manut": "NÃO", "Prot": "NÃO", "Clar": "NÃO", "Reemb": "NÃO", "Equiv": "Essencial Plus DOC"},
    {"Operadora": "GNDI (Intermédica)", "Plano": "Top Premium Orto Select", "Rol": "SIM", "Doc": "SIM", "Manut": "SIM", "Prot": "NÃO", "Clar": "NÃO", "Reemb": "NÃO", "Equiv": "Pleno"},
    
    # --- HAPVIDA ODONTO ---
    {"Operadora": "Hapvida Odonto", "Plano": "Odonto Premium Nacional", "Rol": "SIM", "Doc": "SIM", "Manut": "NÃO", "Prot": "NÃO", "Clar": "NÃO", "Reemb": "NÃO", "Equiv": "Essencial Plus"},
    {"Operadora": "Hapvida Odonto", "Plano": "Odonto Premium Free", "Rol": "SIM", "Doc": "NÃO", "Manut": "NÃO", "Prot": "NÃO", "Clar": "NÃO", "Reemb": "NÃO", "Equiv": "Essencial"},
    
    # --- METLIFE ---
    {"Operadora": "MetLife", "Plano": "Metlife Essencial", "Rol": "SIM", "Doc": "NÃO", "Manut": "NÃO", "Prot": "NÃO", "Clar": "NÃO", "Reemb": "NÃO", "Equiv": "Essencial"},
    {"Operadora": "MetLife", "Plano": "Metlife DOC", "Rol": "SIM", "Doc": "SIM", "Manut": "NÃO", "Prot": "NÃO", "Clar": "NÃO", "Reemb": "NÃO", "Equiv": "Essencial Plus DOC"},
    {"Operadora": "MetLife", "Plano": "Metlife Orto", "Rol": "SIM", "Doc": "SIM", "Manut": "SIM", "Prot": "NÃO", "Clar": "NÃO", "Reemb": "NÃO", "Equiv": "Pleno"},
    {"Operadora": "MetLife", "Plano": "Metlife Pro Mais", "Rol": "SIM", "Doc": "SIM", "Manut": "NÃO", "Prot": "SIM", "Clar": "SIM", "Reemb": "NÃO", "Equiv": "Pleno Top"},
    
    # --- BRASILDENTAL ---
    {"Operadora": "BrasilDental", "Plano": "Integral DOC", "Rol": "SIM", "Doc": "SIM", "Manut": "NÃO", "Prot": "NÃO", "Clar": "NÃO", "Reemb": "NÃO", "Equiv": "Essencial Plus DOC"},
    {"Operadora": "BrasilDental", "Plano": "Supremo", "Rol": "SIM", "Doc": "SIM", "Manut": "SIM", "Prot": "SIM", "Clar": "SIM", "Reemb": "NÃO", "Equiv": "Pleno Top"},
    
    # --- DENTALUNI ---
    {"Operadora": "DentalUni", "Plano": "Dental Essencial", "Rol": "SIM", "Doc": "NÃO", "Manut": "NÃO", "Prot": "NÃO", "Clar": "NÃO", "Reemb": "NÃO", "Equiv": "Essencial"},
    {"Operadora": "DentalUni", "Plano": "Dental Amplo DOC", "Rol": "SIM", "Doc": "SIM", "Manut": "NÃO", "Prot": "NÃO", "Clar": "NÃO", "Reemb": "NÃO", "Equiv": "Essencial Plus DOC"},
    {"Operadora": "DentalUni", "Plano": "Dental Elite", "Rol": "SIM", "Doc": "SIM", "Manut": "SIM", "Prot": "SIM", "Clar": "NÃO", "Reemb": "NÃO", "Equiv": "Pleno Plus"},
    
    # --- PORTO SEGURO ---
    {"Operadora": "Porto Seguro", "Plano": "Bronze 10", "Rol": "SIM", "Doc": "NÃO", "Manut": "NÃO", "Prot": "NÃO", "Clar": "NÃO", "Reemb": "NÃO", "Equiv": "Essencial"},
    {"Operadora": "Porto Seguro", "Plano": "Bronze Integral DOC 10", "Rol": "SIM", "Doc": "SIM", "Manut": "NÃO", "Prot": "NÃO", "Clar": "NÃO", "Reemb": "NÃO", "Equiv": "Essencial Plus DOC"},
    {"Operadora": "Porto Seguro", "Plano": "Ouro Premium 10", "Rol": "SIM", "Doc": "SIM", "Manut": "SIM", "Prot": "SIM", "Clar": "SIM", "Reemb": "SIM", "Equiv": "Pleno Top"},
    
    # --- ODONTO EMPRESAS ---
    {"Operadora": "Odonto Empresas", "Plano": "Sigma", "Rol": "SIM", "Doc": "NÃO", "Manut": "NÃO", "Prot": "NÃO", "Clar": "NÃO", "Reemb": "NÃO", "Equiv": "Essencial"},
    {"Operadora": "Odonto Empresas", "Plano": "Alfa Orto", "Rol": "SIM", "Doc": "SIM", "Manut": "SIM", "Prot": "NÃO", "Clar": "NÃO", "Reemb": "NÃO", "Equiv": "Pleno"},
    
    # --- INPAO DENTAL ---
    {"Operadora": "INPAO Dental", "Plano": "Especial", "Rol": "SIM", "Doc": "NÃO", "Manut": "NÃO", "Prot": "NÃO", "Clar": "NÃO", "Reemb": "NÃO", "Equiv": "Essencial"},
    {"Operadora": "INPAO Dental", "Plano": "Especial Orto", "Rol": "SIM", "Doc": "SIM", "Manut": "SIM", "Prot": "NÃO", "Clar": "NÃO", "Reemb": "NÃO", "Equiv": "Pleno"}
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
        <h1>🛡️ Portal Comercial Unimed Odonto</h1>
        <p>Plataforma Inteligente de Equiparação de Planos e Análise de Coberturas da Concorrência</p>
    </div>
""", unsafe_allow_html=True)

# === FILTROS DE SELEÇÃO ===
col_box1, col_box2 = st.columns(2)

with col_box1:
    operadoras_disponiveis = sorted([op for op in df_base["Operadora"].unique() if op != "Unimed ODONTO"])
    op_selecionada = st.selectbox("🎯 1. Escolha a Operadora Concorrente:", operadoras_disponiveis)

with col_box2:
    planos_filtrados = df_base[df_base["Operadora"] == op_selecionada]["Plano"].tolist()
    plano_selecionado = st.selectbox("📋 2. Escolha o Plano da Concorrência:", planos_filtrados)

# === PROCESSAMENTO DE DADOS E DESIGN DOS RESULTADOS ===
if plano_selecionado:
    linha_cong = df_base[(df_base["Operadora"] == op_selecionada) & (df_base["Plano"] == plano_selecionado)].iloc[0]
    equiv_unimed = linha_cong["Equiv"]
    linha_uni = df_base[(df_base["Operadora"] == "Unimed ODONTO") & (df_base["Plano"] == equiv_unimed)].iloc[0]
    
    # Cálculo preciso da equivalência e gaps estruturais
    iguais, faltas, diferenciais = 0, [], []
    for cob in coberturas:
        if linha_cong[cob] == linha_uni[cob]: 
            iguais += 1
        elif linha_uni[cob] == "SIM" and linha_cong[cob] == "NÃO": 
            faltas.append(nomes_coberturas[cob])
        elif linha_cong[cob] == "SIM" and linha_uni[cob] == "NÃO": 
            diferenciais.append(nomes_coberturas[cob])
            
    porcentagem = (iguais / len(coberturas)) * 100
    
    # Cor dinâmica para a porcentagem
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

    # Barra visual de progresso estilizada com as cores dinâmicas Unimed
    st.markdown(f"""
        <div style="width: 100%; background-color: #E2E8F0; border-radius: 4px; margin-bottom: 35px; height: 8px;">
            <div style="width: {porcentagem}%; background-color: {color_perc}; height: 100%; border-radius: 4px;"></div>
        </div>
    """, unsafe_allow_html=True)

    # MÓDULO 2: COMPARATIVO TÉCNICO E ESTRUTURAL (CARDS LADO A LADO)
    col_c1, col_c2 = st.columns(2)
    
    with col_c1:
        itens_html_cong = ""
        for c in coberturas:
            badge_class = "badge-sim" if linha_cong[c] == "SIM" else "badge-nao"
            itens_html_cong += f'<div class="coverage-item">{nomes_coberturas[c]}<span class="badge {badge_class}">{linha_cong[c]}</span></div>'
        
        # Strings totalmente alinhadas à esquerda (Sem espaços extras de indentação)
        html_card_cong = f"""
<div class="comp-card concorrente">
<h3 class="card-title-concorrente">🔍 Estrutura do Concorrente</h3>
<p style="font-size:15px; margin: 0 0 15px 0;"><b>{op_selecionada}</b> — {plano_selecionado}</p>
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
<h3 class="card-title-unimed">🍏 Proposta Unimed Odonto</h3>
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
