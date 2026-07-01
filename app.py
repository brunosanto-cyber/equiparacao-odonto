import streamlit as st
import pandas as pd
import base64
import os

# Configuração inicial avançada da página web
st.set_page_config(
    page_title="Equiparação Corporativa - Unimed Odonto",
    page_icon="🦷",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# === FUNÇÃO AUXILIAR: CONVERSÃO DO LOGOTIPO PARA BASE64 ===
def obter_logo_base64(caminho_imagem):
    if os.path.exists(caminho_imagem):
        with open(caminho_imagem, "rb") as arquivo_img:
            return f"data:image/png;base64,{base64.b64encode(arquivo_img.read()).decode()}"
    return "https://img.icons8.com/color/tooth.png"

logo_unimed_html = obter_logo_base64("foto.png")

# === DESIGN SYSTEM & CUSTOM CSS (IDENTIDADE UNIMED ODONTO) ===
st.markdown("""
    <style>
        /* Fundo da aplicação */
        .stApp {
            background-color: #FAFAFA;
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

# === BANCO DE DADOS ATUALIZADO E REVISADO (RADAR DE MERCADO) ===
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
