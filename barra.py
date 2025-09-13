# ==============================================================================
# SEÇÃO 4: GERAÇÃO DE GRÁFICOS DE BARRA (VERSÃO FINAL, ROBUSTA E FUNCIONAL)
# ==============================================================================

# ------------------------------------------------------------------------------
# 4.1. IMPORTAÇÃO E CONFIGURAÇÃO
# ------------------------------------------------------------------------------
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Configurações visuais dos gráficos
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (16, 10)
plt.rcParams['font.size'] = 12

# ------------------------------------------------------------------------------
# 4.2. CARREGAMENTO E VALIDAÇÃO RIGOROSA DOS DADOS
# ------------------------------------------------------------------------------
def encontrar_arquivo_pns(diretorio='.'):
    """Procura por um arquivo de microdados da PNS 2019 no diretório."""
    for nome_arquivo in os.listdir(diretorio):
        if 'pns' in nome_arquivo.lower() and '2019' in nome_arquivo and nome_arquivo.lower().endswith('.txt'):
            return nome_arquivo
    return None

arquivo_txt_pns = encontrar_arquivo_pns()
if not arquivo_txt_pns:
    print("ERRO: Nenhum arquivo de dados da PNS 2019 foi encontrado.")
    exit()

col_specs_REAIS = [
    (14, 17),    # C008 (Idade)
    (444, 445),  # P040 (Atividade Física)
    (927, 931),  # Q03001 (Peso)
    (931, 934),  # Q03002 (Altura)
]
col_names_REAIS = ['C008', 'P040', 'Q03001', 'Q03002']

print("="*80)
print("BARRAS: Carregando e validando dados...")
try:
    dados = pd.read_fwf(arquivo_txt_pns, colspecs=col_specs_REAIS, names=col_names_REAIS)
except Exception as e:
    print(f"ERRO ao ler o arquivo: {e}")
    exit()

# Limpeza robusta
for col in dados.columns:
    dados[col] = pd.to_numeric(dados[col], errors='coerce')
dados.replace([999, 9999, 8, 9], np.nan, inplace=True)

# Travas de segurança e criação de labels
dados = dados[(dados['C008'] >= 18) & (dados['C008'] <= 120)].copy()
print(f"Validação inicial: {len(dados):,} adultos na amostra.")

dados['ATIV_FISICA_LABEL'] = dados['P040'].map({1: 'Pratica', 2: 'Não Pratica'})
labels_idade = ['18-29', '30-39', '40-49', '50-59', '60+']
dados['FAIXA_ETARIA'] = pd.cut(dados['C008'], bins=[17, 29, 39, 49, 59, 120], labels=labels_idade, right=True)
dados['IMC_CALCULADO'] = (dados['Q03001'] / 10) / ((dados['Q03002'] / 100) ** 2)

# >>>>> CORREÇÃO PRINCIPAL: REMOVIDO o dropna() global que eliminava dados <<<<<

# ------------------------------------------------------------------------------
# 4.3. GERAÇÃO DOS GRÁFICOS CORRIGIDOS
# ------------------------------------------------------------------------------
print("Gerando gráficos de barra...")
fig, axes = plt.subplots(1, 3, figsize=(24, 8))
fig.suptitle('Gráficos de Barra para Comparação entre Grupos da População Adulta', fontsize=20, y=1.03)

# Barra 1: Contagem de Respondentes por Faixa Etária
dados_idade = dados.dropna(subset=['FAIXA_ETARIA'])
sns.countplot(data=dados_idade, y='FAIXA_ETARIA', ax=axes[0], hue='FAIXA_ETARIA', palette='viridis', order=labels_idade, legend=False)
axes[0].set_title('Distribuição de Respondentes por Idade', fontweight='bold')
axes[0].set_xlabel('Quantidade de Pessoas')
axes[0].set_ylabel('Faixa Etária')

# Barra 2: PREVALÊNCIA de Atividade Física por FAIXA ETÁRIA (Lógica Robusta)
dados_prevalencia = dados.dropna(subset=['FAIXA_ETARIA', 'ATIV_FISICA_LABEL'])
# Usando crosstab para um cálculo mais seguro e direto
proporcoes = pd.crosstab(index=dados_prevalencia['FAIXA_ETARIA'],
                           columns=dados_prevalencia['ATIV_FISICA_LABEL'],
                           normalize='index').mul(100).reset_index()
proporcoes_long = proporcoes.melt(id_vars='FAIXA_ETARIA', var_name='ATIV_FISICA_LABEL', value_name='percentual')

sns.barplot(data=proporcoes_long, x='percentual', y='FAIXA_ETARIA', hue='ATIV_FISICA_LABEL', ax=axes[1], palette='Set2', order=labels_idade)
axes[1].set_title('Prevalência de Atividade Física por Faixa Etária', fontweight='bold')
axes[1].set_xlabel('Percentual (%)')
axes[1].set_ylabel('Faixa Etária')
axes[1].legend(title='Nível de Atividade')
axes[1].set_xlim(0, 100)
for p in axes[1].patches:
    width = p.get_width()
    axes[1].text(width + 1, p.get_y() + p.get_height() / 2, f'{width:.1f}%', va='center')

# Barra 3: IMC Médio por Prática de Atividade Física
dados_imc = dados.dropna(subset=['ATIV_FISICA_LABEL', 'IMC_CALCULADO'])
imc_medio_ativ = dados_imc.groupby('ATIV_FISICA_LABEL', observed=True)['IMC_CALCULADO'].mean().reset_index()
sns.barplot(data=imc_medio_ativ, x='ATIV_FISICA_LABEL', y='IMC_CALCULADO', ax=axes[2], palette='coolwarm')
axes[2].set_title('IMC Médio por Nível de Atividade Física', fontweight='bold')
axes[2].set_xlabel('Prática de Atividade Física')
axes[2].set_ylabel('IMC Médio (kg/m²)')
for p in axes[2].patches:
    axes[2].annotate(f'{p.get_height():.2f}', (p.get_x() + p.get_width() / 2., p.get_height()), ha='center', va='center', fontsize=12, color='black', xytext=(0, 8), textcoords='offset points')
axes[2].set_ylim(0, imc_medio_ativ['IMC_CALCULADO'].max() * 1.15)


plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.show()