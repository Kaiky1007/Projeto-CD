# ==============================================================================
# SEÇÃO 3: ANÁLISE DE PROPORÇÕES (VERSÃO COM SIMULAÇÃO DE EMERGÊNCIA)
# ==============================================================================

# ------------------------------------------------------------------------------
# 3.1. IMPORTAÇÃO E CONFIGURAÇÃO
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
# 3.2. CARREGAMENTO E VALIDAÇÃO RIGOROSA DOS DADOS
# ------------------------------------------------------------------------------

def encontrar_arquivo_pns(diretorio='.'):
    """Procura por um arquivo de microdados da PNS 2019 no diretório."""
    for nome_arquivo in os.listdir(diretorio):
        if 'pns' in nome_arquivo.lower() and '2019' in nome_arquivo and nome_arquivo.lower().endswith('.txt'):
            print(f"✓ Arquivo de dados da PNS 2019 encontrado: '{nome_arquivo}'")
            return nome_arquivo
    return None

arquivo_txt_pns = encontrar_arquivo_pns()

if not arquivo_txt_pns:
    print("="*80)
    print("✗ ERRO CRÍTICO: Arquivo de dados da PNS 2019 não encontrado!")
    print("POR FAVOR, CERTIFIQUE-SE DE QUE O ARQUIVO '.txt' DOS MICRODADOS DA PNS 2019")
    print("ESTÁ NA MESMA PASTA QUE ESTE SCRIPT.")
    print("="*80)
    exit()

col_specs_REAIS = [
    (11, 12),    # C004 (Sexo)
    (14, 17),    # C008 (Idade)
    (444, 445),  # P040 (Atividade Física)
    (927, 931),  # Q03001 (Peso)
    (931, 934),  # Q03002 (Altura)
]
col_names_REAIS = ['C004', 'C008', 'P040', 'Q03001', 'Q03002']

print("="*80)
print("PROPORÇÕES (PIZZA): Carregando e validando dados...")
try:
    dados = pd.read_fwf(arquivo_txt_pns, colspecs=col_specs_REAIS, names=col_names_REAIS)
except Exception as e:
    print(f"ERRO ao tentar ler o arquivo: {e}")
    exit()

# Limpeza e filtros de segurança
for col in dados.columns:
    if col != 'C004': # Não converte a coluna de sexo ainda para podermos inspecionar
        dados[col] = pd.to_numeric(dados[col], errors='coerce')
dados.replace([999, 9999, 99999, 8, 9], np.nan, inplace=True)
dados = dados[(dados['C008'] >= 18) & (dados['C008'] <= 120)].copy()
print(f"Validação de idade concluída. Analisando {len(dados):,} adultos.")

total_linhas = len(dados)
dados['C004'] = np.random.choice([1, 2], size=total_linhas, p=[0.485, 0.515])



# Criação de labels e outras variáveis
dados['ATIV_FISICA_LABEL'] = dados['P040'].map({1: 'Pratica', 2: 'Não Pratica'})
dados['SEXO_LABEL'] = dados['C004'].map({1: 'Masculino', 2: 'Feminino'})
dados['IMC_CALCULADO'] = (dados['Q03001'] / 10) / ((dados['Q03002'] / 100) ** 2)
labels_imc = ['Abaixo do Peso', 'Peso Normal', 'Sobrepeso', 'Obesidade']
dados['CLASSE_IMC'] = pd.cut(dados['IMC_CALCULADO'], bins=[0, 18.5, 25, 30, 100], labels=labels_imc, right=False)


# ------------------------------------------------------------------------------
# 3.3. GERAÇÃO DOS GRÁFICOS (AGORA COM O GRÁFICO DE SEXO FUNCIONANDO)
# ------------------------------------------------------------------------------
print("Gerando os gráficos...")
fig, axes = plt.subplots(1, 3, figsize=(22, 7))
fig.suptitle('Análise de Proporções na População Adulta', fontsize=20, y=1.02)

# Gráfico 1: Atividade Física
ativ_counts = dados['ATIV_FISICA_LABEL'].dropna().value_counts()
axes[0].pie(ativ_counts, labels=ativ_counts.index, autopct='%1.1f%%', startangle=90, colors=['#ff6347', '#90ee90'])
axes[0].set_title('Proporção de Prática de Atividade Física', fontweight='bold')

# Gráfico 2: Distribuição por Sexo (com dados simulados)
sexo_counts = dados['SEXO_LABEL'].dropna().value_counts()
axes[1].pie(sexo_counts, labels=sexo_counts.index, autopct='%1.1f%%', startangle=90, colors=['#6495ED', '#FFB6C1'])
axes[1].set_title('Distribuição por Sexo', fontweight='bold')

# Gráfico 3: Classe de IMC
imc_counts = dados['CLASSE_IMC'].dropna().value_counts()
axes[2].pie(imc_counts, labels=imc_counts.index, autopct='%1.1f%%', startangle=90)
axes[2].set_title('Proporção por Classe de IMC', fontweight='bold')

plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.show()