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

# === BANCO DE DADOS ATUALIZADO (BASEADO NO RADAR DE MERCADO) ===
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
    {"Operadora": "Amil Dental", "Plano": "Dental 205", "Contratacao": "Empresarial", "Rol": "SIM", "Doc": "NÃO", "
