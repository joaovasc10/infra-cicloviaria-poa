import pandas as pd

# Carregar o arquivo já filtrado anteriormente
df = pd.read_csv('data/raw/websin.csv', sep=';', on_bad_lines='skip')

# Lista dos prefixos considerados infraestrutura cicloviária real
prefixos_validos = [
    'marcacao de cruzamento rodocicloviario',
    'marcacao de ciclofaixa ao longo da via'
]

# Normalizar o campo 'descricao' para facilitar a comparação
df['descricao'] = df['descricao'].str.lower().str.strip()

# Filtrar o DataFrame pelos prefixos válidos
df_filtrado = df[df['descricao'].isin(prefixos_validos)]

# Salvar o resultado
df_filtrado.to_csv('data/processed/filtrado_infra_cicloviaria.csv', sep=';', index=False)

# Exibir as primeiras linhas para conferência
print(df_filtrado.head())