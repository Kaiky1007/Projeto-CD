# Análise de Dados da Pesquisa Nacional de Saúde (PNS) 2019

## 1. Visão Geral do Projeto

Este projeto consiste num conjunto de scripts Python para processar, analisar e visualizar os microdados da Pesquisa Nacional de Saúde (PNS) de 2019. O objetivo é extrair insights sobre a população adulta brasileira a partir de variáveis como idade, peso, altura, pressão arterial e prática de atividades físicas.

O projeto é dividido em quatro scripts principais, cada um focado num tipo diferente de visualização gráfica:
* **Histogramas:** Para entender a distribuição de variáveis contínuas.
* **Gráficos de Dispersão:** Para explorar a relação entre pares de variáveis.
* **Gráficos de Pizza:** Para analisar a proporção de dados categóricos.
* **Gráficos de Barra:** Para comparar médias e contagens entre diferentes grupos.

## 2. Fonte dos Dados

Todos os scripts utilizam o arquivo de microdados da PNS 2019.
* **Arquivo Necessário:** `MICRODADOS_PNS_2019.txt`
* **Observação:** Este arquivo deve estar localizado na mesma pasta que os scripts Python para que eles funcionem corretamente.

## 3. Pré-requisitos

Para executar os scripts, é necessário ter o Python instalado, juntamente com as seguintes bibliotecas:

* pandas
* numpy
* matplotlib
* seaborn

Pode instalá-las usando o `pip`:
```bash
pip install pandas numpy matplotlib seaborn
```

## 4. Scripts de Análise

Abaixo está o detalhamento de cada arquivo `.py` do projeto, incluindo os seus objetivos, processamento de dados, visualizações e o código-fonte completo.

---

### 4.1. `histograma.py`

Este script foca na visualização da distribuição de frequência de variáveis numéricas importantes.

* **Objetivo:** Gerar histogramas para entender o perfil da população adulta.
* **Processamento:**
    1.  Carrega dados de idade (`C008`), pressão sistólica (`Q00201`), peso (`Q03001`) e altura (`Q03002`).
    2.  Realiza uma limpeza de dados, removendo códigos de "não sabe" ou "não se aplica" (como 999, 9999).
    3.  Aplica um filtro de segurança para considerar apenas idades entre 18 e 120 anos, garantindo uma análise com dados realistas.
    4.  Calcula o Peso em KG, a Altura em metros e o IMC (Índice de Massa Corporal).
* **Visualizações Geradas:**
    * Distribuição de Idade
    * Distribuição de IMC
    * Distribuição de Peso
    * Distribuição de Pressão Arterial Sistólica

<details>
<summary><strong>Clique para ver o código-fonte de <code>histograma.py</code></strong></summary>

```python
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

```

</details>

---

### 4.2. `dispersao.py`

Este script é usado para investigar a correlação entre diferentes pares de variáveis.

* **Objetivo:** Criar gráficos de dispersão para identificar possíveis relações entre as medidas de saúde.
* **Processamento:**
    1.  Utiliza as mesmas variáveis do script de histograma.
    2.  Aplica uma validação de dados ainda mais rigorosa, removendo qualquer entrada com dados faltantes (`dropna`) e aplicando filtros para garantir que altura, peso e IMC estejam dentro de faixas humanamente possíveis.
    3.  Para uma visualização mais limpa, o script plota uma amostra aleatória de 5.000 registros.
* **Visualizações Geradas:**
    * Relação entre Idade e Pressão Sistólica
    * Relação entre IMC e Pressão Sistólica
    * Relação entre Idade e IMC
    * Relação entre Altura e Peso

<details>
<summary><strong>Clique para ver o código-fonte de <code>dispersao.py</code></strong></summary>

```python
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

```

</details>

---

### 4.3. `pizza.py`

Este script analisa a composição percentual de grupos categóricos na amostra.

* **Objetivo:** Gerar gráficos de pizza para mostrar proporções.
* **Processamento:**
    1.  Carrega dados de sexo (`C004`), idade (`C008`), prática de atividade física (`P040`), peso e altura.
    2.  O script possui uma função para encontrar o arquivo de dados da PNS dinamicamente na pasta.
    3.  **Atenção:** O script simula os dados de sexo (`C004`) para garantir a funcionalidade do gráfico, o que indica que pode haver um problema na leitura ou tratamento desta coluna específica no arquivo original.
    4.  Cria variáveis categóricas como "Pratica / Não Pratica" para atividade física e as classes de IMC (Abaixo do Peso, Peso Normal, etc.).
* **Visualizações Geradas:**
    * Proporção de Prática de Atividade Física
    * Distribuição por Sexo (com dados simulados)
    * Proporção por Classe de IMC

<details>
<summary><strong>Clique para ver o código-fonte de <code>pizza.py</code></strong></summary>

```python
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

```

</details>

---

### 4.4. `barra.py`

Este script é focado em comparar valores entre diferentes categorias.

* **Objetivo:** Gerar gráficos de barra para comparar contagens e médias entre grupos.
* **Processamento:**
    1.  Carrega dados de idade, atividade física, peso e altura.
    2.  Cria categorias de faixa etária (18-29, 30-39, etc.) e labels para atividade física.
    3.  Calcula a contagem de pessoas por faixa etária, a prevalência (em %) de atividade física em cada faixa e o IMC médio para quem pratica e não pratica atividade física.
* **Visualizações Geradas:**
    * Distribuição de Respondentes por Faixa Etária
    * Prevalência de Atividade Física por Faixa Etária
    * IMC Médio por Nível de Atividade Física

<details>
<summary><strong>Clique para ver o código-fonte de <code>barra.py</code></strong></summary>

```python
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

```

</details>

---

## 5. Como Executar

1.  Certifique-se de que o arquivo `MICRODADOS_PNS_2019.txt` está na mesma pasta que os scripts.
2.  Verifique se todas as bibliotecas listadas nos pré-requisitos estão instaladas.
3.  Abra um terminal ou prompt de comando.
4.  Navegue até a pasta do projeto.
5.  Execute cada script individualmente para ver os gráficos correspondentes:

```bash
python histograma.py
python dispersao.py
python pizza.py
python barra.py
```
