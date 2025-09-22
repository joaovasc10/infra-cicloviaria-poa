# Infraestrutura Cicloviária POA

## Pré-requisitos

- Python 3.x  
- Node.js + npm (ou yarn/pnpm)  
- (Opcional) Ambiente virtual Python ativado  

## Pipeline de geração de dados

Com o ambiente Python configurado e as dependências instaladas, o único passo necessário é importar os dados do CSV para o banco de dados SQLite.

1.  **Instale as dependências Python:**
    ```bash
    pip install django djangorestframework django-silk
    ```

2.  **Importe os dados:**
    Execute o comando de gerenciamento a partir da pasta `backend`:
    ```bash
    cd backend
    python manage.py import_csv
    ```
    Isso irá popular o banco de dados `db.sqlite3` com os dados de `data/processed/filtrado_infra_cicloviaria.csv`. O comando pode ser executado novamente para recarregar os dados.

## Executando a aplicação

1.  **Crie e popule o banco de dados:**
    Siga as instruções na seção "Pipeline de geração de dados" primeiro.

2.  **Inicie o backend Django:**
    ```bash
    cd backend
    python manage.py runserver
    ```

3.  **Inicie o frontend Vue (em outra aba do terminal):**
    ```bash
    cd frontend
    npm install
    npm run dev
    ```
4.  Acesse `http://localhost:5173` e faça buscas por logradouro ou implantação.

## Acessando o painel de performance (Silk)
   Com o Django rodando em `http://localhost:8000/`, abra no navegador:
   ```
   http://localhost:8000/silk/
   ```
   O Silk exibirá estatísticas de cada request, tempos de consulta no banco de dados, e muito mais, permitindo identificar gargalos de forma visual.
