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
    {"Operadora": "Amil Dental", "Plano": "Prótese Clínica E60", "Rol": "SIM", "Doc": "NÃO", "Manut": "NÃO", "Prot": "SIM", "Clar": "NÃO", "Reemb": "NÃO", "Equiv":
