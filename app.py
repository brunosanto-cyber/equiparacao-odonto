import streamlit as st
import pandas as pd

# Configuração inicial da página web
st.set_page_config(
    page_title="Simulador de Equiparação - Unimed Odonto",
    page_icon="🛡️",
    layout="wide"
)

# === ESTILIZAÇÃO CUSTOMIZADA: IDENTIDADE UNIMED ODONTO ===
st.markdown("""
    <style>
        /* Cor de fundo geral */
        .stApp {
            background-color: #fcfdfd;
        }
        /* Customização do título principal */
        .title-unimed {
            color: #00995D;
            font-family: 'Segoe UI', Arial, sans-serif;
            font-weight: 700;
            border-bottom: 3px solid #006633;
            padding-bottom: 10px;
            margin-bottom: 25px;
        }
        /* Estilo dos cards */
        .card-concorrente {
            background-color: #ffffff;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
            border-top: 4px solid #707070;
        }
        .card-unimed {
            background-color: #ffffff;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            border-top: 4px solid #00995D;
            border-left: 1px solid #e0ebd8;
        }
        .card-conclusoes {
            background-color: #ffffff;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
            border-left: 4px solid #006633;
            margin-top: 20px;
        }
    </style>
""", unsafe_allow_html=True)

# === BANCO DE DADOS INTEGRADO (DADOS DO SEU PDF) ===
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
    
    # --- ODONTOPREV ---
    {"Operadora": "OdontoPrev", "Plano": "Integral DOC", "Rol": "SIM", "Doc": "SIM", "Manut": "NÃO", "Prot": "NÃO", "Clar": "NÃO", "Reemb": "NÃO", "Equiv": "Essencial Plus DOC"},
    {"Operadora": "OdontoPrev", "Plano": "Master", "Rol": "SIM", "Doc": "SIM", "Manut": "SIM", "Prot": "SIM", "Clar": "SIM", "Reemb": "NÃO", "Equiv": "Pleno Top"},
    
    # --- GRUPO NOTRE DAME INTERMÉDICA (GNDI) ---
    {"Operadora": "GNDI (Intermédica)", "Plano": "Smart Odonto", "Rol": "SIM", "Doc": "NÃO", "Manut": "NÃO", "Prot": "NÃO", "Clar": "NÃO", "Reemb": "NÃO", "Equiv": "Essencial"},
    {"Operadora": "GNDI (Intermédica)", "Plano": "Top Premium", "Rol": "SIM", "Doc": "SIM", "Manut": "NÃO", "Prot": "NÃO", "Clar": "NÃO", "Reemb": "NÃO", "Equiv": "Essencial Plus"},
    {"Operadora": "GNDI (Intermédica)", "Plano": "Top Premium DO", "Rol": "SIM", "Doc": "SIM", "Manut": "NÃO", "Prot": "NÃO", "Clar": "NÃO", "Reemb": "NÃO", "Equiv": "Essencial Plus DOC"},
    
    # --- HAPVIDA ---
    {"Operadora": "Hapvida Odonto", "Plano": "Odonto Premium Nacional", "Rol": "SIM", "Doc": "SIM", "Manut": "NÃO", "Prot": "NÃO", "Clar": "NÃO", "Reemb": "NÃO", "Equiv": "Essencial Plus"},
    
    # --- DENTALUNI ---
    {"Operadora": "DentalUni", "Plano": "Dental Essencial", "Rol": "SIM", "Doc": "NÃO", "Manut": "NÃO", "Prot": "NÃO", "Clar": "NÃO", "Reemb": "NÃO", "Equiv": "Essencial"},
    {"Operadora": "DentalUni", "Plano": "Dental Elite", "Rol": "SIM", "Doc": "SIM", "Manut": "SIM", "Prot": "SIM", "Clar": "NÃO", "Reemb": "NÃO", "Equiv": "Pleno Plus"},
    
    # --- PORTO SEGURO ---
    {"Operadora": "Porto Seguro", "Plano": "Bronze 10", "Rol": "SIM", "Doc": "NÃO", "Manut": "NÃO", "Prot": "NÃO", "Clar": "NÃO", "Reemb": "NÃO", "Equiv": "Essencial"},
    {"Operadora": "Porto Seguro", "Plano": "Bronze Integral DOC 10", "Rol": "SIM", "Doc": "SIM", "Manut": "NÃO", "Prot": "NÃO", "Clar": "NÃO", "Reemb": "NÃO", "Equiv": "Essencial Plus DOC"}
]

df_base = pd.DataFrame(dados_planos)
coberturas = ["Rol", "Doc", "Manut", "Prot", "Clar", "Reemb"]
nomes_coberturas = {
    "Rol": "Rol ANS Clínico", "Doc": "Documentação Ortodôntica", 
    "Manut": "Manutenção de Aparelho", "Prot": "Próteses Além do Rol", 
    "Clar": "Clareamento Estético", "Reemb": "Reembolso"
}

# === INTERFACE DO USUÁRIO ===
st.markdown("<h1 class='title-unimed'>🛡️ Plataforma União Comercial Unimed Odonto</h1>", unsafe_allow_html=True)
st.subheader("Ferramenta de Equiparação Técnica e Inteligência de Mercado")

# Área de Seleção (Filtros superiores)
col_filtro1, col_filtro2 = st.columns(2)

with col_filtro1:
    operadoras_disponiveis = sorted([op for op in df_base["Operadora"].unique() if op != "Unimed ODONTO"])
    op_selecionada = st.selectbox("1. Selecione a Operadora Concorrente:", operadoras_disponiveis)

with col_filtro2:
    planos_filtrados = df_base[df_base["Operadora"] == op_selecionada["Plano"].tolist()
    plano_selecionado = st.selectbox("2. Selecione o Plano da Congênere:", planos_filtrados)

# Lógica de cálculo
if plano_selecionado:
    linha_cong = df_base[(df_base["Operadora"] == op_selecionada) & (df_base["Plano"] == plano_selecionado)].iloc[0]
    equiv_unimed = linha_cong["Equiv"]
    linha_uni = df_base[(df_base["Operadora"] == "Unimed ODONTO") & (df_base["Plano"] == equiv_unimed)].iloc[0]
    
    iguais, faltas, diferenciais = 0, [], []
    for cob in coberturas:
        if linha_cong[cob] == linha_uni[cob]: iguais += 1
        elif linha_uni[cob] == "SIM" and linha_cong[cob] == "NÃO": faltas.append(nomes_coberturas[cob])
        elif linha_cong[cob] == "SIM" and linha_uni[cob] == "NÃO": diferenciais.append(nomes_coberturas[cob])
            
    porcentagem = (iguais / len(coberturas)) * 100

    # Layout de Resultados em Colunas (Cards Lado a Lado)
    st.markdown("---")
    col_card1, col_card2 = st.columns(2)
    
    with col_card1:
        st.markdown(f"""
            <div class="card-concorrente">
                <h3 style="color: #707070; margin-top:0;">🔍 Plano da Concorrência</h3>
                <h2 style="margin: 5px 0 15px 0; color:#333;">{op_selecionada}</h2>
                <p><b>Plano:</b> {plano_selecionado}</p>
                <hr style="border: 0; border-top: 1px solid #eee;">
                {"".join([f"<p style='margin:4px 0;'>• <b>{nomes_coberturas[c]}:</b> {linha_cong[c]}</p>" for c in coberturas])}
            </div>
        """, unsafe_allow_html=True)
        
    with col_card2:
        st.markdown(f"""
            <div class="card-unimed">
                <h3 style="color: #00995D; margin-top:0;">💡 Recomendação Comercial</h3>
                <h2 style="margin: 5px 0 15px 0; color:#00995D;">Unimed ODONTO</h2>
                <p><b>Par Ideal:</b> <span style="background-color:#e0ebd8; padding: 3px 8px; border-radius:4px; font-weight:bold;">{equiv_unimed}</span></p>
                <hr style="border: 0; border-top: 1px solid #eee;">
                {"".join([f"<p style='margin:4px 0;'>• <b>{nomes_coberturas[c]}:</b> {linha_uni[c]}</p>" for c in coberturas])}
            </div>
        """, unsafe_allow_html=True)

    # Métricas e Conclusões Abaixo
    st.markdown(f"""
        <div class="card-conclusoes">
            <h3 style="color: #006633; margin-top:0;">📈 Relatório Técnico de Cobertura</h3>
            <p style="font-size:18px;">Aderência Estrutural: <b>{porcentagem:.1f}%</b></p>
            <p style="margin-bottom:5px;"><b style="color:#d9534f;">❌ Gap de Vendas (O que falta no concorrente):</b></p>
            <p style="color:#555; margin-top:0; padding-left:15px;">{', '.join(faltas) if faltas else 'Nenhum gap técnico encontrado.'}</p>
            <p style="margin-bottom:5px;"><b style="color:#5cb85c;">⭐ Diferenciais da Congênere (A mais):</b></p>
            <p style="color:#555; margin-top:0; padding-left:15px;">{', '.join(diferenciais) if diferenciais else 'Nenhum diferencial extra detectado.'}</p>
        </div>
    """, unsafe_allow_html=True)