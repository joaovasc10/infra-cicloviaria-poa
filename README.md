# Infraestrutura Cicloviária POA

## Pré-requisitos

- Python 3.x  
- Node.js + npm (ou yarn/pnpm)  
- (Opcional) Ambiente virtual Python ativado  

## Pipeline de geração de dados

1. Na raiz do projeto, converta o CSV filtrado em um arquivo binário:  
   ```
   python scripts/csv_to_bin.py
   ```
    Isso lê `data/processed/filtrado_infra_cicloviaria.csv` e gera
    `data/bin/infra_cicloviaria.bin`.
  
2. Em seguida, crie (ou atualize) os índices B+ a partir do binário:
    ```
    cd backend
    python manage.py parse_infra
    ```
    Isso gera em data/bin/:
    - `infra_cicloviaria_logradouro.idx`
    - `infra_cicloviaria_implantacao.idx`
## Executando a aplicação

1. Inicie o backend Django:
    ```
    cd backend
    python manage.py runserver
    ```
2. Inicie o frontend Vue (em outra aba do terminal):
   ```
   cd frontend
   npm install    # ou yarn/pnpm install
   npm run dev    # ou yarn dev / pnpm dev
   ```
3. Acesse `http://localhost:5173` e faça buscas por logradouro ou implantação.
   

## Acessando o painel de performance (Silk)
   Com o Django rodando em `http://localhost:8000/`, abra no navegador:
   ```
   http://localhost:8000/silk/
   ```
   O Silk exibirá estatísticas de cada request, tempos gastos em views, operações de B+Tree, I/O em disco e muito mais, permitindo identificar gargalos de forma visual.
