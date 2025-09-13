# ==============================================================================
# SEÇÃO 1: GERAÇÃO DE HISTOGRAMAS (VERSÃO FINAL CORRIGIDA)
# ==============================================================================

# ------------------------------------------------------------------------------
# 1.1. IMPORTAÇÃO E CONFIGURAÇÃO
# ------------------------------------------------------------------------------
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Configurações visuais dos gráficos
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (16, 10)
plt.rcParams['font.size'] = 12

# ------------------------------------------------------------------------------
# 1.2. CARREGAMENTO E PREPARAÇÃO DOS DADOS
# ------------------------------------------------------------------------------
# Definição das colunas a serem lidas do arquivo da PNS 2019
col_specs_REAIS = [
    (14, 17),    # C008 (Idade)
    (772, 775),  # Q00201 (Pressão Sistólica 1)
    (927, 931),  # Q03001 (Peso)
    (931, 934),  # Q03002 (Altura)
]
col_names_REAIS = ['C008', 'Q00201', 'Q03001', 'Q03002']
arquivo_txt_pns = 'MICRODADOS_PNS_2019.txt'

print("Carregando e preparando dados para os Histogramas...")
try:
    dados = pd.read_fwf(arquivo_txt_pns, colspecs=col_specs_REAIS, names=col_names_REAIS)
except FileNotFoundError:
    print(f"ERRO: Arquivo '{arquivo_txt_pns}' não encontrado. Verifique o caminho.")
    exit()

# Limpeza de códigos especiais (Não sabe/Não se aplica)
for col in dados.columns:
    dados[col] = pd.to_numeric(dados[col], errors='coerce')
    
# Substituindo códigos como 999, 9999, etc., por NaN (valor nulo)
dados.replace([999, 9999, 99999], np.nan, inplace=True)
print("Limpeza de dados realizada.")


# >>>>> CORREÇÃO DEFINITIVA: TRAVA DE SEGURANÇA PARA IDADES VÁLIDAS <<<<<
# Filtra o DataFrame para incluir apenas idades biologicamente possíveis
dados = dados[(dados['C008'] >= 18) & (dados['C008'] <= 120)].copy()
print(f"Filtro de segurança aplicado! Analisando {len(dados):,} adultos com idades realistas.")
print("\nApós a correção, a descrição da coluna de idade é:")
print(dados['C008'].describe()) # Agora o 'max' será um valor real


# Criação de variáveis derivadas (Peso em KG e IMC)
dados['PESO_KG'] = dados['Q03001'] / 10
dados['ALTURA_M'] = dados['Q03002'] / 100
dados['IMC_CALCULADO'] = dados['PESO_KG'] / (dados['ALTURA_M'] ** 2)
dados['IMC_CALCULADO'] = dados['IMC_CALCULADO'].apply(lambda x: x if 10 < x < 100 else np.nan)
print("\nDados prontos para plotagem.")

# ------------------------------------------------------------------------------
# 1.3. GERAÇÃO DOS GRÁFICOS
# ------------------------------------------------------------------------------
print("Gerando os 4 histogramas com dados REALISTAS...")
fig, axes = plt.subplots(2, 2, figsize=(18, 12))
fig.suptitle('Histogramas da População Adulta com Dados Válidos (PNS 2019)', fontsize=20, y=1.02)

# Histograma 1: Idade (Corrigido)
sns.histplot(data=dados, x='C008', kde=True, ax=axes[0, 0], color='skyblue', binwidth=5)
axes[0, 0].set_title('Distribuição de Idade (População Adulta)', fontweight='bold')
axes[0, 0].set_xlabel('Idade (anos)')
axes[0, 0].set_ylabel('Frequência')

# Os outros histogramas também se beneficiam da limpeza e do filtro
# Histograma 2: IMC (Adultos)
sns.histplot(data=dados, x='IMC_CALCULADO', kde=True, ax=axes[0, 1], color='salmon')
axes[0, 1].set_title('Distribuição de IMC (População Adulta)', fontweight='bold')
axes[0, 1].set_xlabel('IMC (kg/m²)')
axes[0, 1].set_ylabel('Frequência')

# Histograma 3: Peso (Adultos)
sns.histplot(data=dados, x='PESO_KG', kde=True, ax=axes[1, 0], color='lightgreen')
axes[1, 0].set_title('Distribuição de Peso (População Adulta)', fontweight='bold')
axes[1, 0].set_xlabel('Peso (kg)')
axes[1, 0].set_ylabel('Frequência')

# Histograma 4: Pressão Arterial Sistólica (Adultos)
sns.histplot(data=dados, x='Q00201', kde=True, ax=axes[1, 1], color='plum')
axes[1, 1].set_title('Distribuição de Pressão Arterial Sistólica (População Adulta)', fontweight='bold')
axes[1, 1].set_xlabel('Pressão Sistólica (mmHg)')
axes[1, 1].set_ylabel('Frequência')

plt.tight_layout(rect=[0, 0, 1, 0.97])
plt.show()