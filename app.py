import pandas as pd
import ipywidgets as widgets
from IPython.display import display, clear_output
import json

# 1. BASE DE DADOS (Mapeamento baseado no documento original)
dados_planos = [
    # Referências Unimed Odonto
    {"Operadora": "Unimed ODONTO", "Plano": "Essencial", "Rol": "SIM", "Doc": "NÃO", "Manut": "NÃO", "Prot": "NÃO", "Clar": "NÃO", "Reemb": "NÃO", "Equiv": "Essencial"},
    {"Operadora": "Unimed ODONTO", "Plano": "Essencial Plus", "Rol": "SIM", "Doc": "SIM", "Manut": "NÃO", "Prot": "NÃO", "Clar": "NÃO", "Reemb": "NÃO", "Equiv": "Essencial Plus"},
    {"Operadora": "Unimed ODONTO", "Plano": "Essencial Plus DOC", "Rol": "SIM", "Doc": "SIM", "Manut": "NÃO", "Prot": "NÃO", "Clar": "NÃO", "Reemb": "NÃO", "Equiv": "Essencial Plus DOC"},
    {"Operadora": "Unimed ODONTO", "Plano": "Pleno", "Rol": "SIM", "Doc": "SIM", "Manut": "SIM", "Prot": "NÃO", "Clar": "NÃO", "Reemb": "NÃO", "Equiv": "Pleno"},
    {"Operadora": "Unimed ODONTO", "Plano": "Pleno Plus", "Rol": "SIM", "Doc": "SIM", "Manut": "SIM", "Prot": "SIM", "Clar": "NÃO", "Reemb": "NÃO", "Equiv": "Pleno Plus"},
    {"Operadora": "Unimed ODONTO", "Plano": "Pleno Top", "Rol": "SIM", "Doc": "SIM", "Manut": "SIM", "Prot": "SIM", "Clar": "SIM", "Reemb": "NÃO", "Equiv": "Pleno Top"},
    
    # SulAmérica 
    {"Operadora": "SulAmérica", "Plano": "Mais", "Rol": "SIM", "Doc": "SIM", "Manut": "NÃO", "Prot": "NÃO", "Clar": "NÃO", "Reemb": "NÃO", "Equiv": "Essencial Plus"},
    {"Operadora": "SulAmérica", "Plano": "Mais Doc", "Rol": "SIM", "Doc": "SIM", "Manut": "NÃO", "Prot": "NÃO", "Clar": "NÃO", "Reemb": "NÃO", "Equiv": "Essencial Plus DOC"},
    {"Operadora": "SulAmérica", "Plano": "Mais Clarear", "Rol": "SIM", "Doc": "SIM", "Manut": "NÃO", "Prot": "NÃO", "Clar": "SIM", "Reemb": "NÃO", "Equiv": "Pleno Top"},
    {"Operadora": "SulAmérica", "Plano": "Mais Orto", "Rol": "SIM", "Doc": "SIM", "Manut": "SIM", "Prot": "NÃO", "Clar": "NÃO", "Reemb": "NÃO", "Equiv": "Pleno"},
    {"Operadora": "SulAmérica", "Plano": "Mais Pro", "Rol": "SIM", "Doc": "SIM", "Manut": "NÃO", "Prot": "SIM", "Clar": "NÃO", "Reemb": "NÃO", "Equiv": "Pleno Plus"},
    {"Operadora": "SulAmérica", "Plano": "Premium", "Rol": "SIM", "Doc": "SIM", "Manut": "SIM", "Prot": "SIM", "Clar": "SIM", "Reemb": "SIM", "Equiv": "Pleno Top"},
    
    # Amil Dental 
    {"Operadora": "amil dental", "Plano": "Dental 205", "Rol": "SIM", "Doc": "NÃO", "Manut": "NÃO", "Prot": "NÃO", "Clar": "NÃO", "Reemb": "NÃO", "Equiv": "Essencial"},
    {"Operadora": "amil dental", "Plano": "Prótese Clínica E60", "Rol": "SIM", "Doc": "NÃO", "Manut": "NÃO", "Prot": "SIM", "Clar": "NÃO", "Reemb": "NÃO", "Equiv": "Pleno Plus"},
    {"Operadora": "amil dental", "Plano": "Prótese Estética E90", "Rol": "SIM", "Doc": "NÃO", "Manut": "NÃO", "Prot": "SIM", "Clar": "SIM", "Reemb": "NÃO", "Equiv": "Pleno Top"},
    {"Operadora": "amil dental", "Plano": "Ortodontia E80", "Rol": "SIM", "Doc": "SIM", "Manut": "SIM", "Prot": "NÃO", "Clar": "NÃO", "Reemb": "NÃO", "Equiv": "Pleno"},
    
    # OdontoPrev [cite: 1]
    {"Operadora": "OdontoPrev", "Plano": "Integral DOC", "Rol": "SIM", "Doc": "SIM", "Manut": "NÃO", "Prot": "NÃO", "Clar": "NÃO", "Reemb": "NÃO", "Equiv": "Essencial Plus DOC"},
    {"Operadora": "OdontoPrev", "Plano": "Master", "Rol": "SIM", "Doc": "SIM", "Manut": "SIM", "Prot": "SIM", "Clar": "SIM", "Reemb": "SIM", "Equiv": "Pleno Top"},
    
    # Porto Seguro [cite: 57]
    {"Operadora": "PORTO SEGURO", "Plano": "Bronze 10", "Rol": "SIM", "Doc": "NÃO", "Manut": "NÃO", "Prot": "NÃO", "Clar": "NÃO", "Reemb": "NÃO", "Equiv": "Essencial"},
    {"Operadora": "PORTO SEGURO", "Plano": "Bronze Integral DOC 10", "Rol": "SIM", "Doc": "SIM", "Manut": "NÃO", "Prot": "NÃO", "Clar": "NÃO", "Reemb": "NÃO", "Equiv": "Essencial Plus DOC"}
]

df_base = pd.DataFrame(dados_planos)
coberturas = ["Rol", "Doc", "Manut", "Prot", "Clar", "Reemb"]
nomes_coberturas = {
    "Rol": "Rol ANS Clínico", "Doc": "Documentação Ortodôntica", 
    "Manut": "Manutenção de Aparelho", "Prot": "Próteses Além do Rol", 
    "Clar": "Clareamento Estético", "Reemb": "Reembolso"
}

# 2. COMPONENTES DA INTERFACE (UI)
out = widgets.Output()
operadoras_disponiveis = sorted([op for op in df_base["Operadora"].unique() if op != "Unimed ODONTO"])

dropdown_op = widgets.Dropdown(options=operadoras_disponiveis, description='Operadora:')
dropdown_plano = widgets.Dropdown(description='Plano:')
btn_exportar = widgets.Button(description="Baixar Planilha .XLSX", button_style='success', icon='download')

# 3. LÓGICA DE ATUALIZAÇÃO DINÂMICA
def atualizar_planos(*args):
    planos = df_base[df_base["Operadora"] == dropdown_op.value]["Plano"].tolist()
    dropdown_plano.options = planos

dropdown_op.observe(atualizar_planos, 'value')
atualizar_planos()

def calcular_equiparao(change):
    with out:
        clear_output()
        op = dropdown_op.value
        plano = dropdown_plano.value
        
        if not plano: return
        
        # Obter dados do plano congênere e seu equivalente Unimed
        linha_cong = df_base[(df_base["Operadora"] == op) & (df_base["Plano"] == plano)].iloc[0]
        equiv_unimed = linha_cong["Equiv"]
        linha_uni = df_base[(df_base["Operadora"] == "Unimed ODONTO") & (df_base["Plano"] == equiv_unimed)].iloc[0]
        
        # Cálculos de Aderência e Gaps
        iguais = 0
        faltas = []
        gaps_positivos = []
        
        for cob in coberturas:
            val_cong = linha_cong[cob]
            val_uni = linha_uni[cob]
            
            if val_cong == val_uni:
                iguais += 1
            elif val_uni == "SIM" and val_cong == "NÃO":
                faltas.append(nomes_coberturas[cob])
            elif val_cong == "SIM" and val_uni == "NÃO":
                gaps_positivos.append(nomes_coberturas[cob])
                
        porcentagem = (iguais / len(coberturas)) * 100
        
        # Design do Resultado impresso na tela
        print("="*60)
        print(f"   ANÁLISE DE EQUIPARAÇÃO: {op.upper()} - {plano.upper()}")
        print("="*60)
        print(f"👉 Plano Equivalente Unimed: {equiv_unimed}")
        
        # Cor de acordo com o nível de aderência
        if porcentagem == 100:
            print(f"🟢 Porcentagem de Equiparação: {porcentagem:.1f}% (Aderência Perfeita)")
        elif porcentagem >= 70:
            print(f"🟡 Porcentagem de Equiparação: {porcentagem:.1f}% (Alta Aderência)")
        else:
            print(f"🔴 Porcentagem de Equiparação: {porcentagem:.1f}% (Baixa Aderência)")
            
        print(f"❌ O que falta no plano {op}: {', '.join(faltas) if faltas else 'Nada (Plano cobre tudo do equivalente)'}")
        print(f"⭐ O que o plano {op} tem A MAIS: {', '.join(gaps_positivos) if gaps_positivos else 'Nenhum diferencial apontado'}")
        print("="*60)

dropdown_op.observe(calcular_equiparao, 'value')
dropdown_plano.observe(calcular_equiparao, 'value')

# 4. FUNÇÃO PARA FAZER DOWNLOAD DO ARQUIVO REAL .XLSX
def exportar_excel(b):
    with out:
        file_name = "Equiparacao_Planos_Odonto.xlsx"
        with pd.ExcelWriter(file_name, engine='openpyxl') as writer:
            # Salva o mapeamento completo na Aba 1
            df_base.to_excel(writer, sheet_name="Mapeamento_Planos", index=False)
            
            # Salva uma estrutura modelo na Aba 2
            df_modelo_simulador = pd.DataFrame([{
                "Operadora Congênere": "SulAmérica",
                "Plano da Congênere": "Mais",
                "Plano Equivalente Unimed Odonto": "Essencial Plus",
                "% de Equiparação": "100.0%",
                "O que falta no plano Congênere?": "Nada",
                "O que o plano Congênere tem A MAIS?": "Nenhum"
            }])
            df_modelo_simulador.to_excel(writer, sheet_name="Simulador_Equiparacao", index=False)
            
        from google.colab import files
        files.download(file_name)
        print(f"✅ Arquivo '{file_name}' gerado e baixado com sucesso!")

btn_exportar.on_click(exportar_excel)

# EXIBIÇÃO DO LAYOUT
ui = widgets.VBox([
    widgets.HTML(value="<h2>🛠️ Simulador de Equiparação Odonto</h2>"),
    widgets.HBox([dropdown_op, dropdown_plano]),
    btn_exportar,
    out
])
display(ui)
