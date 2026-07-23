import streamlit as st
import pandas as pd
import base64
import os

# Configuração inicial da página web
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

# === DESIGN SYSTEM: BLINDAGEM DE SITE E ESTILIZAÇÃO PREMIUM ===
st.markdown(f"""
    <style>
        /* Importação da fonte executiva Inter */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

        /* Fundo global de toda a plataforma (Claro e Neutro) */
        .stApp {{
            background-color: #F8F9FA !important;
            font-family: 'Inter', -apple-system, sans-serif !important;
        }}

        /* 🔒 REMOÇÃO COMPLETA DAS BARRAS NATIVAS DE APLICATIVO */
        [data-testid="stHeader"], .stAppHeader, header, .stActionButton, .stDeployButton {{
            display: none !important;
            visibility: hidden !important;
            height: 0px !important;
        }}
        footer {{
            visibility: hidden !important;
            display: none !important;
        }}

        /* Forçar a cor escura nos textos dos filtros superiores */
        div[data-testid="stWidgetLabel"] p {{
            color: #2D3748 !important;
            font-weight: 600 !important;
            font-size: 14px !important;
        }}

        /* BANNER PRINCIPAL - Verde Unimed */
        .unimed-banner-blindado {{
            background-color: #00995D !important;
            padding: 30px !important;
            border-radius: 15px !important;
            margin-bottom: 25px !important;
            box-shadow: 0 4px 15px rgba(0,0,0,0.12) !important;
            color: white !important;
        }}

        /* CARDS DE MÉTRICAS */
        .metric-card-blindado {{
            background-color: #00995D !important;
            padding: 20px !important;
            border-radius: 12px !important;
            text-align: center !important;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08) !important;
            color: white !important;
        }}
        .metric-label-blindado {{
            color: #E0F2F1 !important;
            font-size: 13px !important;
            font-weight: 600 !important;
            text-transform: uppercase !important;
            letter-spacing: 1px !important;
        }}
        .metric-value-blindado {{
            font-size: 28px !important;
            font-weight: 700 !important;
            margin-top: 5px !important;
            color: white !important;
        }}

        /* CARDS COMPARATIVOS */
        .comp-card-blindado {{
            background-color: #00995D !important;
            padding: 25px !important;
            border-radius: 15px !important;
            box-shadow: 0 6px 18px rgba(0,0,0,0.1) !important;
            margin-bottom: 20px !important;
            min-height: 480px !important;
            color: white !important;
            border: 1px solid #007A4B !important;
        }}
        
        .coverage-item-blindado {{
            padding: 10px 0 !important;
            border-bottom: 1px solid rgba(255,255,255,0.15) !important;
            color: white !important;
            font-size: 14px !important;
            display: flex !important;
            justify-content: space-between !important;
            align-items: center !important;
        }}

        /* Badges customizados */
        .badge-sim-verde {{ background-color: #FFFFFF !important; color: #00995D !important; padding: 3px 10px !important; border-radius: 20px !important; font-weight: 700 !important; font-size: 11px !important; }}
        .badge-nao-verde {{ background-color: #FFCDD2 !important; color: #B71C1C !important; padding: 3px 10px !important; border-radius: 20px !important; font-weight: 700 !important; font-size: 11px !important; }}

        /* Títulos de seção */
        .section-header-fixo {{
            color: #004D26 !important;
            font-weight: 700 !important;
            margin: 25px 0 15px 0 !important;
        }}

        summary {{
            list-style: none !important;
        }}
        summary::-webkit-details-marker {{
            display: none !important;
        }}
    </style>
""", unsafe_allow_html=True)

# === BANCO DE DADOS: PANORAMA DE MERCADO ===
dados_mercado = {
    "OdontoPrev": {"posicao": "1ª", "vidas": "8,78 milhões", "perfil": "Líder absoluta do mercado. Capital aberto na B3 (ODPV3), possui a maior rede credenciada nacional e parcerias de distribuição estratégicas (como a operação conjunta com o Bradesco Dental)."},
    "Hapvida Odonto": {"posicao": "2ª", "vidas": "3,93 milhões", "perfil": "Vice-líder. Impulsionada pela fusão Hapvida/GNDI e pela aquisição de operadoras regionais. Possui fortíssima penetração nas regiões Norte, Nordeste e Sudeste."},
    "SulAmérica": {"posicao": "3ª", "vidas": "2,90 milhões", "perfil": "Parte do grupo Rede D'Or (RDOR3), tem forte presença no segmento corporativo e brokerage, atendendo de PMEs a grandes contas multinacionais."},
    "Amil Dental": {"posicao": "5ª", "vidas": "2,67 milhões", "perfil": "Uma das marcas mais tradicionais do país em odontologia suplementar, com ampla variedade de grades (do rol básico a planos com cobertura estética e de próteses)."},
    "Porto Seguro": {"posicao": "6ª", "vidas": "1,18 milhão", "perfil": "Destaca-se pela alta retenção de clientes e sinergia com o portfólio de seguros corporativos da Porto."},
    "MetLife": {"posicao": "8ª", "vidas": "~850 mil", "perfil": "Multinacional focada no mercado de apólices e benefícios corporativos de médio e grande porte."},
    "Dental Uni": {"posicao": "9ª", "vidas": "~650 mil", "perfil": "Cooperativa odontológica de destaque nacional com forte presença na Região Sul."},
    "INPAO Dental": {"posicao": "10ª", "vidas": "~450 mil", "perfil": "Atuação focada em segmentos premium corporativos, com alto padrão de atendimento e programas focados em saúde bucal preventiva."}
}

# === BANCO DE DADOS DE PLANOS ===
dados_planos = [
    # ================= PLANOS UNIMED ODONTO =================
    {"Operadora": "Unimed ODONTO", "Plano": "Essencial", "Contratacao": "Empresarial", "Rol_ANS": "SIM", "Rol_Amp": "NÃO", "Doc_Orto": "NÃO", "Comp_Prot": "NÃO", "Orto_Comp": "NÃO", "Prot_Comp": "NÃO", "Clar_Cas": "NÃO", "Clar_Las": "NÃO", "Alinhador": "NÃO", "Implantes": "NÃO", "Equiv": "Essencial"},
    {"Operadora": "Unimed ODONTO", "Plano": "Essencial Plus", "Contratacao": "Empresarial", "Rol_ANS": "SIM", "Rol_Amp": "SIM", "Doc_Orto": "NÃO", "Comp_Prot": "NÃO", "Orto_Comp": "NÃO", "Prot_Comp": "NÃO", "Clar_Cas": "NÃO", "Clar_Las": "NÃO", "Alinhador": "NÃO", "Implantes": "NÃO", "Equiv": "Essencial Plus"},
    {"Operadora": "Unimed ODONTO", "Plano": "Essencial Plus DOC", "Contratacao": "Empresarial", "Rol_ANS": "SIM", "Rol_Amp": "SIM", "Doc_Orto": "SIM", "Comp_Prot": "NÃO", "Orto_Comp": "NÃO", "Prot_Comp": "NÃO", "Clar_Cas": "NÃO", "Clar_Las": "NÃO", "Alinhador": "NÃO", "Implantes": "NÃO", "Equiv": "Essencial Plus DOC"},
    {"Operadora": "Unimed ODONTO", "Plano": "Pleno", "Contratacao": "Empresarial", "Rol_ANS": "SIM", "Rol_Amp": "SIM", "Doc_Orto": "NÃO", "Comp_Prot": "SIM", "Orto_Comp": "NÃO", "Prot_Comp": "NÃO", "Clar_Cas": "NÃO", "Clar_Las": "NÃO", "Alinhador": "NÃO", "Implantes": "NÃO", "Equiv": "Pleno"},
    {"Operadora": "Unimed ODONTO", "Plano": "Pleno Plus", "Contratacao": "Empresarial", "Rol_ANS": "SIM", "Rol_Amp": "SIM", "Doc_Orto": "NÃO", "Comp_Prot": "NÃO", "Orto_Comp": "NÃO", "Prot_Comp": "SIM", "Clar_Cas": "NÃO", "Clar_Las": "NÃO", "Alinhador": "NÃO", "Implantes": "NÃO", "Equiv": "Pleno Plus"},
    {"Operadora": "Unimed ODONTO", "Plano": "Pleno Plus DOC", "Contratacao": "Empresarial", "Rol_ANS": "SIM", "Rol_Amp": "SIM", "Doc_Orto": "SIM", "Comp_Prot": "NÃO", "Orto_Comp": "NÃO", "Prot_Comp": "SIM", "Clar_Cas": "NÃO", "Clar_Las": "NÃO", "Alinhador": "NÃO", "Implantes": "NÃO", "Equiv": "Pleno Plus DOC"},
    {"Operadora": "Unimed ODONTO", "Plano": "Pleno Ortodontia", "Contratacao": "Empresarial", "Rol_ANS": "SIM", "Rol_Amp": "SIM", "Doc_Orto": "NÃO", "Comp_Prot": "SIM", "Orto_Comp": "SIM", "Prot_Comp": "NÃO", "Clar_Cas": "NÃO", "Clar_Las": "NÃO", "Alinhador": "NÃO", "Implantes": "NÃO", "Equiv": "Pleno Ortodontia"},
    {"Operadora": "Unimed ODONTO", "Plano": "Pleno Top", "Contratacao": "Empresarial", "Rol_ANS": "SIM", "Rol_Amp": "SIM", "Doc_Orto": "SIM", "Comp_Prot": "SIM", "Orto_Comp": "SIM", "Prot_Comp": "SIM", "Clar_Cas": "NÃO", "Clar_Las": "NÃO", "Alinhador": "NÃO", "Implantes": "NÃO", "Equiv": "Pleno Top"},
    {"Operadora": "Unimed ODONTO", "Plano": "Unimed Alinhador", "Contratacao": "Empresarial", "Rol_ANS": "SIM", "Rol_Amp": "SIM", "Doc_Orto": "SIM", "Comp_Prot": "NÃO", "Orto_Comp": "SIM", "Prot_Comp": "NÃO", "Clar_Cas": "NÃO", "Clar_Las": "NÃO", "Alinhador": "SIM", "Implantes": "NÃO", "Equiv": "Unimed Alinhador"},

    {"Operadora": "Unimed ODONTO", "Plano": "Essencial", "Contratacao": "PME e MEI", "Rol_ANS": "SIM", "Rol_Amp": "NÃO", "Doc_Orto": "NÃO", "Comp_Prot": "NÃO", "Orto_Comp": "NÃO", "Prot_Comp": "NÃO", "Clar_Cas": "NÃO", "Clar_Las": "NÃO", "Alinhador": "NÃO", "Implantes": "NÃO", "Equiv": "Essencial"},
    {"Operadora": "Unimed ODONTO", "Plano": "Essencial Plus", "Contratacao": "PME e MEI", "Rol_ANS": "SIM", "Rol_Amp": "SIM", "Doc_Orto": "NÃO", "Comp_Prot": "NÃO", "Orto_Comp": "NÃO", "Prot_Comp": "NÃO", "Clar_Cas": "NÃO", "Clar_Las": "NÃO", "Alinhador": "NÃO", "Implantes": "NÃO", "Equiv": "Essencial Plus"},
    {"Operadora": "Unimed ODONTO", "Plano": "Essencial Plus DOC", "Contratacao": "PME e MEI", "Rol_ANS": "SIM", "Rol_Amp": "SIM", "Doc_Orto": "SIM", "Comp_Prot": "NÃO", "Orto_Comp": "NÃO", "Prot_Comp": "NÃO", "Clar_Cas": "NÃO", "Clar_Las": "NÃO", "Alinhador": "NÃO", "Implantes": "NÃO", "Equiv": "Essencial Plus DOC"},
    {"Operadora": "Unimed ODONTO", "Plano": "Pleno", "Contratacao": "PME e MEI", "Rol_ANS": "SIM", "Rol_Amp": "SIM", "Doc_Orto": "NÃO", "Comp_Prot": "SIM", "Orto_Comp": "NÃO", "Prot_Comp": "NÃO", "Clar_Cas": "NÃO", "Clar_Las": "NÃO", "Alinhador": "NÃO", "Implantes": "NÃO", "Equiv": "Pleno"},
    {"Operadora": "Unimed ODONTO", "Plano": "Pleno Ortodontia", "Contratacao": "PME e MEI", "Rol_ANS": "SIM", "Rol_Amp": "SIM", "Doc_Orto": "NÃO", "Comp_Prot": "SIM", "Orto_Comp": "SIM", "Prot_Comp": "NÃO", "Clar_Cas": "NÃO", "Clar_Las": "NÃO", "Alinhador": "NÃO", "Implantes": "NÃO", "Equiv": "Pleno Ortodontia"},
    {"Operadora": "Unimed ODONTO", "Plano": "Unimed Alinhador", "Contratacao": "PME e MEI", "Rol_ANS": "SIM", "Rol_Amp": "SIM", "Doc_Orto": "SIM", "Comp_Prot": "NÃO", "Orto_Comp": "SIM", "Prot_Comp": "NÃO", "Clar_Cas": "NÃO", "Clar_Las": "NÃO", "Alinhador": "SIM", "Implantes": "NÃO", "Equiv": "Unimed Alinhador"},

    {"Operadora": "Unimed ODONTO", "Plano": "Essencial", "Contratacao": "Individual", "Rol_ANS": "SIM", "Rol_Amp": "NÃO", "Doc_Orto": "NÃO", "Comp_Prot": "NÃO", "Orto_Comp": "NÃO", "Prot_Comp": "NÃO", "Clar_Cas": "NÃO", "Clar_Las": "NÃO", "Alinhador": "NÃO", "Implantes": "NÃO", "Equiv": "Essencial"},
    {"Operadora": "Unimed ODONTO", "Plano": "Essencial Plus", "Contratacao": "Individual", "Rol_ANS": "SIM", "Rol_Amp": "SIM", "Doc_Orto": "NÃO", "Comp_Prot": "NÃO", "Orto_Comp": "NÃO", "Prot_Comp": "NÃO", "Clar_Cas": "NÃO", "Clar_Las": "NÃO", "Alinhador": "NÃO", "Implantes": "NÃO", "Equiv": "Essencial Plus"},
    {"Operadora": "Unimed ODONTO", "Plano": "Pleno", "Contratacao": "Individual", "Rol_ANS": "SIM", "Rol_Amp": "SIM", "Doc_Orto": "NÃO", "Comp_Prot": "SIM", "Orto_Comp": "NÃO", "Prot_Comp": "NÃO", "Clar_Cas": "NÃO", "Clar_Las": "NÃO", "Alinhador": "NÃO", "Implantes": "NÃO", "Equiv": "Pleno"},

    # ================= AMIL DENTAL =================
    {"Operadora": "Amil Dental", "Plano": "Amil Dental 205", "Contratacao": "Individual", "Rol_ANS": "SIM", "Rol_Amp": "NÃO", "Doc_Orto": "NÃO", "Comp_Prot": "NÃO", "Orto_Comp": "NÃO", "Prot_Comp": "NÃO", "Clar_Cas": "NÃO", "Clar_Las": "NÃO", "Alinhador": "NÃO", "Implantes": "NÃO", "Equiv": "Essencial"},
    {"Operadora": "Amil Dental", "Plano": "Amil Dental E30", "Contratacao": "Individual", "Rol_ANS": "SIM", "Rol_Amp": "NÃO", "Doc_Orto": "NÃO", "Comp_Prot": "NÃO", "Orto_Comp": "NÃO", "Prot_Comp": "NÃO", "Clar_Cas": "SIM", "Clar_Las": "NÃO", "Alinhador": "NÃO", "Implantes": "NÃO", "Equiv": "Essencial Plus"},
    {"Operadora": "Amil Dental", "Plano": "Amil Dental E40", "Contratacao": "Individual", "Rol_ANS": "SIM", "Rol_Amp": "NÃO", "Doc_Orto": "SIM", "Comp_Prot": "NÃO", "Orto_Comp": "SIM", "Prot_Comp": "NÃO", "Clar_Cas": "NÃO", "Clar_Las": "NÃO", "Alinhador": "NÃO", "Implantes": "NÃO", "Equiv": "Pleno"},
    {"Operadora": "Amil Dental", "Plano": "Amil Dental E50", "Contratacao": "Individual", "Rol_ANS": "SIM", "Rol_Amp": "NÃO", "Doc_Orto": "NÃO", "Comp_Prot": "NÃO", "Orto_Comp": "NÃO", "Prot_Comp": "SIM", "Clar_Cas": "NÃO", "Clar_Las": "NÃO", "Alinhador": "NÃO", "Implantes": "NÃO", "Equiv": "Pleno"},
    {"Operadora": "Amil Dental", "Plano": "Amil Dental 205 PME", "Contratacao": "PME e MEI", "Rol_ANS": "SIM", "Rol_Amp": "NÃO", "Doc_Orto": "NÃO", "Comp_Prot": "NÃO", "Orto_Comp": "NÃO", "Prot_Comp": "NÃO", "Clar_Cas": "NÃO", "Clar_Las": "NÃO", "Alinhador": "NÃO", "Implantes": "NÃO", "Equiv": "Essencial"},
    {"Operadora": "Amil Dental", "Plano": "Amil Dental E30 PME", "Contratacao": "PME e MEI", "Rol_ANS": "SIM", "Rol_Amp": "NÃO", "Doc_Orto": "NÃO", "Comp_Prot": "NÃO", "Orto_Comp": "NÃO", "Prot_Comp": "NÃO", "Clar_Cas": "SIM", "Clar_Las": "NÃO", "Alinhador": "NÃO", "Implantes": "NÃO", "Equiv": "Essencial Plus"},
    {"Operadora": "Amil Dental", "Plano": "Amil Dental E40 PME", "Contratacao": "PME e MEI", "Rol_ANS": "SIM", "Rol_Amp": "NÃO", "Doc_Orto": "SIM", "Comp_Prot": "NÃO", "Orto_Comp": "SIM", "Prot_Comp": "NÃO", "Clar_Cas": "NÃO", "Clar_Las": "NÃO", "Alinhador": "NÃO", "Implantes": "NÃO", "Equiv": "Pleno Ortodontia"},
    {"Operadora": "Amil Dental", "Plano": "Amil Dental E50 PME", "Contratacao": "PME e MEI", "Rol_ANS": "SIM", "Rol_Amp": "NÃO", "Doc_Orto": "NÃO", "Comp_Prot": "NÃO", "Orto_Comp": "NÃO", "Prot_Comp": "SIM", "Clar_Cas": "NÃO", "Clar_Las": "NÃO", "Alinhador": "NÃO", "Implantes": "NÃO", "Equiv": "Pleno"},
    {"Operadora": "Amil Dental", "Plano": "Amil Dental 205 Empresarial", "Contratacao": "Empresarial", "Rol_ANS": "SIM", "Rol_Amp": "NÃO", "Doc_Orto": "NÃO", "Comp_Prot": "NÃO", "Orto_Comp": "NÃO", "Prot_Comp": "NÃO", "Clar_Cas": "NÃO", "Clar_Las": "NÃO", "Alinhador": "NÃO", "Implantes": "NÃO", "Equiv": "Essencial"},
    {"Operadora": "Amil Dental", "Plano": "Amil Dental E30 Empresarial", "Contratacao": "Empresarial", "Rol_ANS": "SIM", "Rol_Amp": "NÃO", "Doc_Orto": "NÃO", "Comp_Prot": "NÃO", "Orto_Comp": "NÃO", "Prot_Comp": "NÃO", "Clar_Cas": "SIM", "Clar_Las": "NÃO", "Alinhador": "NÃO", "Implantes": "NÃO", "Equiv": "Essencial Plus"},
    {"Operadora": "Amil Dental", "Plano": "Amil Dental E40 Empresarial", "Contratacao": "Empresarial", "Rol_ANS": "SIM", "Rol_Amp": "NÃO", "Doc_Orto": "SIM", "Comp_Prot": "NÃO", "Orto_Comp": "SIM", "Prot_Comp": "NÃO", "Clar_Cas": "NÃO", "Clar_Las": "NÃO", "Alinhador": "NÃO", "Implantes": "NÃO", "Equiv": "Pleno Ortodontia"},
    {"Operadora": "Amil Dental", "Plano": "Amil Dental E50 Empresarial", "Contratacao": "Empresarial", "Rol_ANS": "SIM", "Rol_Amp": "NÃO", "Doc_Orto": "NÃO", "Comp_Prot": "NÃO", "Orto_Comp": "NÃO", "Prot_Comp": "SIM", "Clar_Cas": "NÃO", "Clar_Las": "NÃO", "Alinhador": "NÃO", "Implantes": "NÃO", "Equiv": "Pleno Plus"},
    {"Operadora": "Amil Dental", "Plano": "Amil Dental E60 Empresarial", "Contratacao": "Empresarial", "Rol_ANS": "SIM", "Rol_Amp": "SIM", "Doc_Orto": "SIM", "Comp_Prot": "NÃO", "Orto_Comp": "SIM", "Prot_Comp": "SIM", "Clar_Cas": "SIM", "Clar_Las": "NÃO", "Alinhador": "NÃO", "Implantes": "NÃO", "Equiv": "Pleno Top"},

    # ================= HAPVIDA ODONTO =================
    {"Operadora": "Hapvida Odonto", "Plano": "Odonto Premium Free", "Contratacao": "Individual", "Rol_ANS": "SIM", "Rol_Amp": "NÃO", "Doc_Orto": "NÃO", "Comp_Prot": "NÃO", "Orto_Comp": "NÃO", "Prot_Comp": "NÃO", "Clar_Cas": "NÃO", "Clar_Las": "NÃO", "Alinhador": "NÃO", "Implantes": "NÃO", "Equiv": "Essencial"},
    {"Operadora": "Hapvida Odonto", "Plano": "Odonto Premium TM", "Contratacao": "Individual", "Rol_ANS": "SIM", "Rol_Amp": "NÃO", "Doc_Orto": "NÃO", "Comp_Prot": "NÃO", "Orto_Comp": "NÃO", "Prot_Comp": "NÃO", "Clar_Cas": "NÃO", "Clar_Las": "NÃO", "Alinhador": "NÃO", "Implantes": "NÃO", "Equiv": "Essencial"},
    {"Operadora": "Hapvida Odonto", "Plano": "+Odonto Premium Total CE", "Contratacao": "PME e MEI", "Rol_ANS": "SIM", "Rol_Amp": "NÃO", "Doc_Orto": "NÃO", "Comp_Prot": "NÃO", "Orto_Comp": "NÃO", "Prot_Comp": "NÃO", "Clar_Cas": "NÃO", "Clar_Las": "NÃO", "Alinhador": "NÃO", "Implantes": "NÃO", "Equiv": "Essencial"},
    {"Operadora": "Hapvida Odonto", "Plano": "Smart Odonto", "Contratacao": "PME e MEI", "Rol_ANS": "SIM", "Rol_Amp": "NÃO", "Doc_Orto": "NÃO", "Comp_Prot": "NÃO", "Orto_Comp": "NÃO", "Prot_Comp": "NÃO", "Clar_Cas": "NÃO", "Clar_Las": "NÃO", "Alinhador": "NÃO", "Implantes": "NÃO", "Equiv": "Essencial"},
    {"Operadora": "Hapvida Odonto", "Plano": "Top Premium", "Contratacao": "PME e MEI", "Rol_ANS": "SIM", "Rol_Amp": "SIM", "Doc_Orto": "NÃO", "Comp_Prot": "NÃO", "Orto_Comp": "NÃO", "Prot_Comp": "NÃO", "Clar_Cas": "NÃO", "Clar_Las": "NÃO", "Alinhador": "NÃO", "Implantes": "NÃO", "Equiv": "Essencial Plus"},
    {"Operadora": "Hapvida Odonto", "Plano": "Top Premium DO", "Contratacao": "PME e MEI", "Rol_ANS": "SIM", "Rol_Amp": "SIM", "Doc_Orto": "SIM", "Comp_Prot": "NÃO", "Orto_Comp": "NÃO", "Prot_Comp": "NÃO", "Clar_Cas": "NÃO", "Clar_Las": "NÃO", "Alinhador": "NÃO", "Implantes": "NÃO", "Equiv": "Essencial Plus DOC"},
    {"Operadora": "Hapvida Odonto", "Plano": "+Odonto Premium Top", "Contratacao": "Empresarial", "Rol_ANS": "SIM", "Rol_Amp": "NÃO", "Doc_Orto": "NÃO", "Comp_Prot": "NÃO", "Orto_Comp": "NÃO", "Prot_Comp": "NÃO", "Clar_Cas": "NÃO", "Clar_Las": "NÃO", "Alinhador": "NÃO", "Implantes": "NÃO", "Equiv": "Essencial"},
    {"Operadora": "Hapvida Odonto", "Plano": "Top Premium Gold", "Contratacao": "Empresarial", "Rol_ANS": "SIM", "Rol_Amp": "SIM", "Doc_Orto": "SIM", "Comp_Prot": "NÃO", "Orto_Comp": "NÃO", "Prot_Comp": "NÃO", "Clar_Cas": "SIM", "Clar_Las": "NÃO", "Alinhador": "NÃO", "Implantes": "NÃO", "Equiv": "Essencial Plus DOC"},
    {"Operadora": "Hapvida Odonto", "Plano": "Top Premium Orto", "Contratacao": "Empresarial", "Rol_ANS": "SIM", "Rol_Amp": "SIM", "Doc_Orto": "SIM", "Comp_Prot": "NÃO", "Orto_Comp": "SIM", "Prot_Comp": "NÃO", "Clar_Cas": "SIM", "Clar_Las": "NÃO", "Alinhador": "NÃO", "Implantes": "NÃO", "Equiv": "Pleno Ortodontia"},
    {"Operadora": "Hapvida Odonto", "Plano": "Select", "Contratacao": "Empresarial", "Rol_ANS": "SIM", "Rol_Amp": "SIM", "Doc_Orto": "NÃO", "Comp_Prot": "NÃO", "Orto_Comp": "NÃO", "Prot_Comp": "SIM", "Clar_Cas": "SIM", "Clar_Las": "NÃO", "Alinhador": "NÃO", "Implantes": "NÃO", "Equiv": "Pleno Plus"},
    {"Operadora": "Hapvida Odonto", "Plano": "Excelence", "Contratacao": "Empresarial", "Rol_ANS": "SIM", "Rol_Amp": "SIM", "Doc_Orto": "SIM", "Comp_Prot": "NÃO", "Orto_Comp": "SIM", "Prot_Comp": "SIM", "Clar_Cas": "SIM", "Clar_Las": "NÃO", "Alinhador": "NÃO", "Implantes": "NÃO", "Equiv": "Pleno Top"},

    # ================= OUTRAS OPERADORAS CONCORRENTES =================
    {"Operadora": "OdontoPrev", "Plano": "Bem-Estar Orto", "Contratacao": "Individual", "Rol_ANS": "SIM", "Rol_Amp": "SIM", "Doc_Orto": "SIM", "Comp_Prot": "NÃO", "Orto_Comp": "SIM", "Prot_Comp": "NÃO", "Clar_Cas": "NÃO", "Clar_Las": "NÃO", "Alinhador": "NÃO", "Implantes": "NÃO", "Equiv": "Pleno"},
    {"Operadora": "OdontoPrev", "Plano": "Master", "Contratacao": "PME e MEI", "Rol_ANS": "SIM", "Rol_Amp": "SIM", "Doc_Orto": "SIM", "Comp_Prot": "SIM", "Orto_Comp": "SIM", "Prot_Comp": "NÃO", "Clar_Cas": "NÃO", "Clar_Las": "NÃO", "Alinhador": "NÃO", "Implantes": "SIM", "Equiv": "Pleno Ortodontia"},
    {"Operadora": "OdontoPrev", "Plano": "Integral Doc", "Contratacao": "Empresarial", "Rol_ANS": "SIM", "Rol_Amp": "SIM", "Doc_Orto": "SIM", "Comp_Prot": "NÃO", "Orto_Comp": "NÃO", "Prot_Comp": "NÃO", "Clar_Cas": "NÃO", "Clar_Las": "NÃO", "Alinhador": "NÃO", "Implantes": "NÃO", "Equiv": "Essencial Plus DOC"},
    {"Operadora": "OdontoPrev", "Plano": "Premium", "Contratacao": "Empresarial", "Rol_ANS": "SIM", "Rol_Amp": "SIM", "Doc_Orto": "SIM", "Comp_Prot": "SIM", "Orto_Comp": "SIM", "Prot_Comp": "SIM", "Clar_Cas": "NÃO", "Clar_Las": "NÃO", "Alinhador": "NÃO", "Implantes": "NÃO", "Equiv": "Pleno Top"},
    {"Operadora": "Porto Seguro", "Plano": "Bronze Integral Doc 10", "Contratacao": "Empresarial", "Rol_ANS": "SIM", "Rol_Amp": "SIM", "Doc_Orto": "SIM", "Comp_Prot": "NÃO", "Orto_Comp": "NÃO", "Prot_Comp": "NÃO", "Clar_Cas": "NÃO", "Clar_Las": "NÃO", "Alinhador": "NÃO", "Implantes": "NÃO", "Equiv": "Essencial Plus DOC"},
    {"Operadora": "Porto Seguro", "Plano": "Ouro Premium 10", "Contratacao": "Empresarial", "Rol_ANS": "SIM", "Rol_Amp": "SIM", "Doc_Orto": "SIM", "Comp_Prot": "SIM", "Orto_Comp": "SIM", "Prot_Comp": "SIM", "Clar_Cas": "SIM", "Clar_Las": "NÃO", "Alinhador": "NÃO", "Implantes": "NÃO", "Equiv": "Pleno Top"},
    {"Operadora": "SulAmérica", "Plano": "Mais", "Contratacao": "Individual", "Rol_ANS": "SIM", "Rol_Amp": "SIM", "Doc_Orto": "NÃO", "Comp_Prot": "NÃO", "Orto_Comp": "NÃO", "Prot_Comp": "NÃO", "Clar_Cas": "NÃO", "Clar_Las": "NÃO", "Alinhador": "NÃO", "Implantes": "NÃO", "Equiv": "Essencial Plus"},
    {"Operadora": "SulAmérica", "Plano": "Premium", "Contratacao": "Empresarial", "Rol_ANS": "SIM", "Rol_Amp": "SIM", "Doc_Orto": "SIM", "Comp_Prot": "SIM", "Orto_Comp": "SIM", "Prot_Comp": "SIM", "Clar_Cas": "SIM", "Clar_Las": "NÃO", "Alinhador": "NÃO", "Implantes": "NÃO", "Equiv": "Pleno Top"},
    {"Operadora": "MetLife", "Plano": "Gold Doc", "Contratacao": "PME e MEI", "Rol_ANS": "SIM", "Rol_Amp": "SIM", "Doc_Orto": "SIM", "Comp_Prot": "NÃO", "Orto_Comp": "NÃO", "Prot_Comp": "NÃO", "Clar_Cas": "NÃO", "Clar_Las": "NÃO", "Alinhador": "NÃO", "Implantes": "NÃO", "Equiv": "Essencial Plus DOC"},
    {"Operadora": "MetLife", "Plano": "Premium", "Contratacao": "Empresarial", "Rol_ANS": "SIM", "Rol_Amp": "SIM", "Doc_Orto": "SIM", "Comp_Prot": "SIM", "Orto_Comp": "SIM", "Prot_Comp": "SIM", "Clar_Cas": "SIM", "Clar_Las": "NÃO", "Alinhador": "NÃO", "Implantes": "NÃO", "Equiv": "Pleno Top"},
    {"Operadora": "Dental Uni", "Plano": "Dental Amplo DOC", "Contratacao": "Empresarial", "Rol_ANS": "SIM", "Rol_Amp": "SIM", "Doc_Orto": "SIM", "Comp_Prot": "NÃO", "Orto_Comp": "NÃO", "Prot_Comp": "NÃO", "Clar_Cas": "NÃO", "Clar_Las": "NÃO", "Alinhador": "NÃO", "Implantes": "NÃO", "Equiv": "Essencial Plus DOC"},
    {"Operadora": "INPAO Dental", "Plano": "Especial Orto", "Contratacao": "Empresarial", "Rol_ANS": "SIM", "Rol_Amp": "SIM", "Doc_Orto": "NÃO", "Comp_Prot": "SIM", "Orto_Comp": "SIM", "Prot_Comp": "NÃO", "Clar_Cas": "NÃO", "Clar_Las": "NÃO", "Alinhador": "NÃO", "Implantes": "NÃO", "Equiv": "Pleno Ortodontia"},
    {"Operadora": "Odonto Empresas", "Plano": "Alfa Orto", "Contratacao": "Empresarial", "Rol_ANS": "SIM", "Rol_Amp": "SIM", "Doc_Orto": "NÃO", "Comp_Prot": "SIM", "Orto_Comp": "SIM", "Prot_Comp": "NÃO", "Clar_Cas": "NÃO", "Clar_Las": "NÃO", "Alinhador": "NÃO", "Implantes": "NÃO", "Equiv": "Pleno Ortodontia"},
    {"Operadora": "BB Dental", "Plano": "Integral Doc", "Contratacao": "Empresarial", "Rol_ANS": "SIM", "Rol_Amp": "SIM", "Doc_Orto": "SIM", "Comp_Prot": "NÃO", "Orto_Comp": "NÃO", "Prot_Comp": "NÃO", "Clar_Cas": "NÃO", "Clar_Las": "NÃO", "Alinhador": "NÃO", "Implantes": "NÃO", "Equiv": "Essencial Plus DOC"}
]

df_base = pd.DataFrame(dados_planos)

# === MAPEAMENTO DAS 10 COBERTURAS ===
coberturas = [
    "Rol_ANS", "Rol_Amp", "Doc_Orto", "Comp_Prot", "Orto_Comp", 
    "Prot_Comp", "Clar_Cas", "Clar_Las", "Alinhador", "Implantes"
]
nomes_cobs = {
    "Rol_ANS": "Rol ANS",
    "Rol_Amp": "Rol Ampliado",
    "Doc_Orto": "Documentação Ortodôntica",
    "Comp_Prot": "Complementares de Prótese",
    "Orto_Comp": "Ortodontia Completa",
    "Prot_Comp": "Prótese Completa",
    "Clar_Cas": "Clareamento Caseiro",
    "Clar_Las": "Clareamento Laser",
    "Alinhador": "Alinhador",
    "Implantes": "Implantes"
}

# === UI: CABEÇALHO ===
st.markdown(f"""
    <div class="unimed-banner-blindado">
        <div style="display: flex; align-items: center; gap: 20px;">
            <img src="{logo_unimed_html}" style="max-height: 65px; border-radius: 5px;">
            <h1 style="margin:0; color: white !important; font-size: 32px; border:none; font-family: 'Inter', sans-serif;">Portal Equivalência de Planos - Odonto</h1>
        </div>
        <p style="margin: 10px 0 0 85px; color: white !important; opacity: 0.9; font-family: 'Inter', sans-serif;">Dashboard Corporativo de Equiparação de Coberturas</p>
    </div>
""", unsafe_allow_html=True)

# === FILTROS ===
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown('<p style="color: #2D3748 !important; font-weight: 600; font-size: 14px; margin-bottom: 5px; font-family: \'Inter\', sans-serif;">🎯 1. Escolha a Operadora Concorrente:</p>', unsafe_allow_html=True)
    operadoras_disponiveis = sorted([op for op in df_base["Operadora"].unique() if op != "Unimed ODONTO"])
    op_sel = st.selectbox("op_label", operadoras_disponiveis, label_visibility="collapsed")
with col2:
    st.markdown('<p style="color: #2D3748 !important; font-weight: 600; font-size: 14px; margin-bottom: 5px; font-family: \'Inter\', sans-serif;">💼 2. Modelo de Contratação:</p>', unsafe_allow_html=True)
    contratacoes_disponiveis = sorted(df_base[df_base["Operadora"] == op_sel]["Contratacao"].unique().tolist())
    mod_sel = st.selectbox("mod_label", contratacoes_disponiveis, label_visibility="collapsed")
with col3:
    st.markdown('<p style="color: #2D3748 !important; font-weight: 600; font-size: 14px; margin-bottom: 5px; font-family: \'Inter\', sans-serif;">📋 3. Escolha o Plano da Concorrência:</p>', unsafe_allow_html=True)
    planos_filtrados = df_base[(df_base["Operadora"] == op_sel) & (df_base["Contratacao"] == mod_sel)]["Plano"].tolist()
    plano_sel = st.selectbox("plano_label", planos_filtrados, label_visibility="collapsed")

# === PROCESSAMENTO ===
if plano_sel:
    linha_cong = df_base[(df_base["Operadora"] == op_sel) & (df_base["Contratacao"] == mod_sel) & (df_base["Plano"] == plano_sel)].iloc[0]
    equiv_uni = linha_cong["Equiv"]
    
    linha_uni = df_base[(df_base["Operadora"] == "Unimed ODONTO") & (df_base["Contratacao"] == mod_sel) & (df_base["Plano"] == equiv_uni)].iloc[0]

    iguais, faltas, diferenciais = 0, [], []
    for c in coberturas:
        if linha_cong[c] == linha_uni[c]: 
            iguais += 1
        elif linha_uni[c] == "SIM" and linha_cong[c] == "NÃO": 
            faltas.append(nomes_cobs[c])
        elif linha_cong[c] == "SIM" and linha_uni[c] == "NÃO": 
            diferenciais.append(nomes_cobs[c])
    
    porcentagem = (iguais / 10) * 100
    cor_perc = "#00995D" if porcentagem == 100 else ("#A2C027" if porcentagem >= 70 else "#E05353")

    # Módulo de Indicadores
    st.markdown("<h3 class='section-header-fixo'>### 📈 Indicadores de Aderência</h3>", unsafe_allow_html=True)
    m_col1, m_col2, m_col3 = st.columns(3)
    
    with m_col1:
        st.markdown(f'<div class="metric-card-blindado"><div class="metric-label-blindado">Percentual de Equiparação</div><div class="metric-value-blindado">{porcentagem:.1f}%</div></div>', unsafe_allow_html=True)
    with m_col2:
        st.markdown(f'<div class="metric-card-blindado"><div class="metric-label-blindado">Recomendação Unimed</div><div class="metric-value-blindado">{equiv_uni}</div></div>', unsafe_allow_html=True)
    with m_col3:
        status = "Par Perfeito" if porcentagem == 100 else ("Equivalente" if porcentagem >= 70 else "Gap Técnico")
        st.markdown(f'<div class="metric-card-blindado"><div class="metric-label-blindado">Status Comercial</div><div class="metric-value-blindado">{status}</div></div>', unsafe_allow_html=True)

    # Barra visual de progresso
    st.markdown(f'<div style="width:100%; background:rgba(0,0,0,0.08); height:10px; border-radius:10px; margin:25px 0;"><div style="width:{porcentagem}%; background:{cor_perc}; height:100%; border-radius:10px; border:1px solid rgba(255,255,255,0.4);"></div></div>', unsafe_allow_html=True)

    # Módulo Comparativo Lado a Lado
    c_col1, c_col2 = st.columns(2)
    
    with c_col1:
        cobs_html = "".join([f'<div class="coverage-item-blindado">{nomes_cobs[c]} <span class="{"badge-sim-verde" if linha_cong[c]=="SIM" else "badge-nao-verde"}">{linha_cong[c]}</span></div>' for c in coberturas])
        
        html_card_cong = f"""
<div class="comp-card-blindado">
<div style="color: #FFFFFF !important; font-weight: 700; margin-top: 0; margin-bottom: 12px; font-size: 22px !important; line-height: 1.2; display: flex; align-items: center; gap: 8px; font-family: 'Inter', sans-serif;">
<span>🔍</span> <span style="color: #FFFFFF !important;">{op_sel} — {plano_sel}</span>
</div>
<p style="color: #E0F2F1 !important; font-size: 14px; margin-bottom: 20px; opacity:0.9; font-family: 'Inter', sans-serif;">Modalidade Selecionada: {mod_sel}</p>
<hr style="border:0; border-top:1px solid rgba(255,255,255,0.2); margin-bottom:15px;">
{cobs_html}
</div>
"""
        st.markdown(html_card_cong, unsafe_allow_html=True)

    with c_col2:
        uni_html = "".join([f'<div class="coverage-item-blindado">{nomes_cobs[c]} <span class="{"badge-sim-verde" if linha_uni[c]=="SIM" else "badge-nao-verde"}">{linha_uni[c]}</span></div>' for c in coberturas])
        
        html_card_uni = f"""
<div class="comp-card-blindado" style="background-color: #007A4B !important;">
<div style="color: #FFFFFF !important; font-weight: 700; margin-top: 0; margin-bottom: 12px; font-size: 22px !important; line-height: 1.2; display: flex; align-items: center; gap: 8px; font-family: 'Inter', sans-serif;">
<span>🦷</span> <span style="color: #FFFFFF !important;">Unimed ODONTO — {equiv_uni}</span>
</div>
<p style="color: #E0F2F1 !important; font-size: 14px; margin-bottom: 20px; opacity:0.9; font-family: 'Inter', sans-serif;">Par Ideal Mapeado em {mod_sel}</p>
<hr style="border:0; border-top:1px solid rgba(255,255,255,0.2); margin-bottom:15px;">
{uni_html}
</div>
"""
        st.markdown(html_card_uni, unsafe_allow_html=True)

    # === SEÇÃO INFERIOR DIVIDIDA: ARGUMENTOS COMERCIAIS E PANORAMA DE MERCADO ===
    col_bottom1, col_bottom2 = st.columns(2)
    
    with col_bottom1:
        html_insights = f"""
        <details style="background-color: #FFFFFF !important; border-left: 8px solid #00995D !important; padding: 25px !important; border-radius: 16px; box-shadow: 0 4px 12px rgba(0,0,0,0.04); margin-top:10px; cursor: pointer; height: 100%;">
        <summary style="background: linear-gradient(135deg, #00995D 0%, #004D26 100%) !important; color: #FFFFFF !important; margin-top:0; font-size: 16px !important; font-weight: 700 !important; font-family: 'Inter', sans-serif; display: inline-flex; align-items: center; gap: 10px; padding: 10px 22px; border-radius: 30px; box-shadow: 0 4px 12px rgba(0,153,93,0.15); outline: none; transition: transform 0.2s;">
        <span>💡</span> Argumentos Comerciais de Abordagem Técnica &nbsp; <small style="font-size:11px; font-weight:400; color:#E0F2F1;">(Clique para consultar)</small>
        </summary>
        <div style="margin-top: 25px; cursor: default;">
        <div style="background-color: #F4FDFB !important; border: 1px solid #E6F4EA !important; border-left: 5px solid #00995D !important; padding: 20px !important; border-radius: 10px !important; margin-bottom: 18px !important; box-shadow: 0 2px 6px rgba(0,0,0,0.01) !important;">
        <div style="color: #00995D !important; font-weight: 700 !important; font-size: 15px !important; font-family: 'Inter', sans-serif; margin-bottom: 8px !important; text-transform: uppercase; letter-spacing: 0.5px;">Onde a Concorrência perde (Falta no Concorrente):</div>
        <div style="color: #2D3748 !important; font-weight: 600 !important; font-size: 16px !important; font-family: 'Inter', sans-serif; padding-left: 5px;">{", ".join(faltas) if faltas else "Plano Concorrente cobre todos os itens mapeados."}</div>
        </div>
        <div style="background-color: #FFF5F5 !important; border: 1px solid #FED7D7 !important; border-left: 5px solid #C5221F !important; padding: 20px !important; border-radius: 10px !important; box-shadow: 0 2px 6px rgba(0,0,0,0.01) !important;">
        <div style="color: #C5221F !important; font-weight: 700 !important; font-size: 15px !important; font-family: 'Inter', sans-serif; margin-bottom: 8px !important; text-transform: uppercase; letter-spacing: 0.5px;">Diferencial de Cobertura Extra da Concorrência:</div>
        <div style="color: #2D3748 !important; font-weight: 600 !important; font-size: 16px !important; font-family: 'Inter', sans-serif; padding-left: 5px;">{", ".join(diferenciais) if diferenciais else "Nenhum extra detectado em relação à prateleira Unimed."}</div>
        </div>
        </div>
        </details>
        """
        st.markdown(html_insights, unsafe_allow_html=True)
        
    with col_bottom2:
        if op_sel in dados_mercado:
            info = dados_mercado[op_sel]
            content = f"""
            <div style="background-color: #F8F9FA !important; border: 1px solid #E2E8F0 !important; border-left: 5px solid #2D3748 !important; padding: 15px !important; border-radius: 10px !important; margin-bottom: 12px !important; box-shadow: 0 2px 6px rgba(0,0,0,0.01) !important;">
                <div style="color: #2D3748 !important; font-weight: 700 !important; font-size: 13px !important; font-family: 'Inter', sans-serif; text-transform: uppercase; letter-spacing: 0.5px;">Posição no Ranking: <span style="font-weight: 400;">{info['posicao']}</span></div>
            </div>
            <div style="background-color: #F8F9FA !important; border: 1px solid #E2E8F0 !important; border-left: 5px solid #2D3748 !important; padding: 15px !important; border-radius: 10px !important; margin-bottom: 12px !important; box-shadow: 0 2px 6px rgba(0,0,0,0.01) !important;">
                <div style="color: #2D3748 !important; font-weight: 700 !important; font-size: 13px !important; font-family: 'Inter', sans-serif; text-transform: uppercase; letter-spacing: 0.5px;">Beneficiários (Vidas): <span style="font-weight: 400;">{info['vidas']}</span></div>
            </div>
            <div style="background-color: #F8F9FA !important; border: 1px solid #E2E8F0 !important; border-left: 5px solid #2D3748 !important; padding: 15px !important; border-radius: 10px !important; box-shadow: 0 2px 6px rgba(0,0,0,0.01) !important;">
                <div style="color: #2D3748 !important; font-weight: 700 !important; font-size: 13px !important; font-family: 'Inter', sans-serif; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 5px;">Perfil & Modelo de Atuação:</div>
                <div style="color: #4A5568 !important; font-weight: 400 !important; font-size: 14px !important; font-family: 'Inter', sans-serif; line-height: 1.5;">{info['perfil']}</div>
            </div>
            """
        else:
            content = """
            <div style="background-color: #FFF5F5 !important; border: 1px solid #FED7D7 !important; border-left: 5px solid #C5221F !important; padding: 20px !important; border-radius: 10px !important; box-shadow: 0 2px 6px rgba(0,0,0,0.01) !important; text-align: center;">
                <div style="color: #C5221F !important; font-weight: 700 !important; font-size: 15px !important; font-family: 'Inter', sans-serif;">Seguradora não se encontra no ranking</div>
            </div>
            """

        html_panorama = f"""
        <details style="background-color: #FFFFFF !important; border-left: 8px solid #2D3748 !important; padding: 25px !important; border-radius: 16px; box-shadow: 0 4px 12px rgba(0,0,0,0.04); margin-top:10px; cursor: pointer; height: 100%;">
        <summary style="background: linear-gradient(135deg, #4A5568 0%, #2D3748 100%) !important; color: #FFFFFF !important; margin-top:0; font-size: 16px !important; font-weight: 700 !important; font-family: 'Inter', sans-serif; display: inline-flex; align-items: center; gap: 10px; padding: 10px 22px; border-radius: 30px; box-shadow: 0 4px 12px rgba(45,55,72,0.15); outline: none; transition: transform 0.2s;">
        <span>📊</span> Panorama de Mercado &nbsp; <small style="font-size:11px; font-weight:400; color:#E2E8F0;">(Clique para consultar)</small>
        </summary>
        <div style="margin-top: 25px; cursor: default;">
        {content}
        </div>
        </details>
        """
        st.markdown(html_panorama, unsafe_allow_html=True)

# === RODAPÉ CORPORATIVO COM A MARCA ===
st.markdown(f"""
    <div style="margin-top: 50px; padding-top: 20px; border-top: 1px solid #E2E8F0; text-align: center; font-family: 'Inter', sans-serif;">
        <img src="{logo_unimed_html}" style="max-height: 40px; width: auto; object-fit: contain; margin-bottom: 10px; opacity: 0.85;">
        <p style="color: #A0AEC0 !important; font-size: 12px; margin: 0; font-weight: 500;">Unimed Odonto © 2026 — Inteligência de Vendas e Mercado</p>
    </div>
""", unsafe_allow_html=True)
