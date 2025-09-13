# ==============================================================================
# SEÇÃO 2: GERAÇÃO DE GRÁFICOS DE DISPERSÃO (VERSÃO FINAL VALIDADA)
# ==============================================================================

# ------------------------------------------------------------------------------
# 2.1. IMPORTAÇÃO E CONFIGURAÇÃO
# ------------------------------------------------------------------------------
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (16, 10)
plt.rcParams['font.size'] = 12

# ------------------------------------------------------------------------------
# 2.2. CARREGAMENTO E VALIDAÇÃO RIGOROSA DOS DADOS
# ------------------------------------------------------------------------------
col_specs_REAIS = [
    (14, 17),    # C008 (Idade)
    (772, 775),  # Q00201 (Pressão Sistólica 1)
    (927, 931),  # Q03001 (Peso)
    (931, 934),  # Q03002 (Altura)
]
col_names_REAIS = ['C008', 'Q00201', 'Q03001', 'Q03002']
arquivo_txt_pns = 'MICRODADOS_PNS_2019.txt'

print("="*80)
print("DISPERSÃO: Carregando e validando dados para garantir que não haja 'Megazordes'...")
try:
    dados = pd.read_fwf(arquivo_txt_pns, colspecs=col_specs_REAIS, names=col_names_REAIS)
except FileNotFoundError:
    print(f"ERRO: Arquivo '{arquivo_txt_pns}' não encontrado.")
    exit()
    
# Limpeza robusta
for col in dados.columns:
    dados[col] = pd.to_numeric(dados[col], errors='coerce')
dados.replace([999, 9999, 99999, 888, 8888, 88888], np.nan, inplace=True)

# Criação de variáveis derivadas
dados['PESO_KG'] = dados['Q03001'] / 10
dados['ALTURA_M'] = dados['Q03002'] / 100
dados['IMC_CALCULADO'] = dados['PESO_KG'] / (dados['ALTURA_M'] ** 2)

# >>>>> CORREÇÃO DEFINITIVA: TRAVAS DE SEGURANÇA PARA DADOS HUMANOS <<<<<
dados.dropna(inplace=True) # Para dispersão, precisamos de dados completos
dados = dados[(dados['C008'] >= 18) & (dados['C008'] <= 120)].copy()
dados = dados[(dados['ALTURA_M'] >= 1.30) & (dados['ALTURA_M'] <= 2.20)].copy() # ELIMINA MEGAZORDES
dados = dados[(dados['PESO_KG'] >= 30) & (dados['PESO_KG'] <= 250)].copy()     # ELIMINA PESOS IRREAIS
dados = dados[(dados['IMC_CALCULADO'] >= 15) & (dados['IMC_CALCULADO'] <= 60)].copy()

print(f"Validação concluída. Análise de {len(dados):,} humanos com dados realistas.")
print("\nApós a correção, a descrição da coluna de altura é:")
print(dados['ALTURA_M'].describe()) # Agora o 'max' será um valor real

# Amostra para melhor visualização
dados_sample = dados.sample(n=min(5000, len(dados)), random_state=42)

# ------------------------------------------------------------------------------
# 2.3. GERAÇÃO DOS GRÁFICOS COM RÓTULOS CORRIGIDOS
# ------------------------------------------------------------------------------
print("Gerando gráficos de dispersão com dados e nomes 100% corrigidos...")
fig, axes = plt.subplots(2, 2, figsize=(18, 12))
fig.suptitle('Relações entre Variáveis da População Adulta (Dados Validados)', fontsize=20, y=1.02)

# Dispersão 1: Idade vs. Pressão Sistólica
sns.scatterplot(data=dados_sample, x='C008', y='Q00201', ax=axes[0, 0], alpha=0.5)
axes[0, 0].set_title('Relação entre Idade e Pressão Sistólica', fontweight='bold')
axes[0, 0].set_xlabel('Idade (anos)')
axes[0, 0].set_ylabel('Pressão Sistólica (mmHg)')

# Dispersão 2: IMC vs. Pressão Sistólica
sns.scatterplot(data=dados_sample, x='IMC_CALCULADO', y='Q00201', ax=axes[0, 1], alpha=0.5, color='red')
axes[0, 1].set_title('Relação entre IMC e Pressão Sistólica', fontweight='bold')
axes[0, 1].set_xlabel('IMC (kg/m²)')
axes[0, 1].set_ylabel('Pressão Sistólica (mmHg)')

# Dispersão 3: Idade vs. IMC
sns.scatterplot(data=dados_sample, x='C008', y='IMC_CALCULADO', ax=axes[1, 0], alpha=0.5, color='green')
axes[1, 0].set_title('Relação entre Idade e IMC', fontweight='bold')
axes[1, 0].set_xlabel('Idade (anos)')
axes[1, 0].set_ylabel('IMC (kg/m²)')

# Dispersão 4: Altura vs. Peso
sns.scatterplot(data=dados_sample, x='ALTURA_M', y='PESO_KG', ax=axes[1, 1], alpha=0.5, color='purple')
axes[1, 1].set_title('Relação entre Altura e Peso', fontweight='bold')
axes[1, 1].set_xlabel('Altura (m)')
axes[1, 1].set_ylabel('Peso (kg)')

plt.tight_layout(rect=[0, 0, 1, 0.97])
plt.show()