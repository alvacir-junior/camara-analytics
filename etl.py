import os
import logging
import requests
import duckdb
import pandas as pd
from datetime import datetime

# Configuração de logs para acompanhar o progresso no terminal
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

DB_FILE = "data/camara.duckdb"
API_BASE_URL = "https://dadosabertos.camara.leg.br/api/v2"
CURRENT_YEAR = datetime.now().year


def fetch_deputados():
    """Extrai a lista atualizada de deputados federais da API."""
    logging.info("Buscando lista de deputados...")
    url = f"{API_BASE_URL}/deputados?ordem=ASC&ordenarPor=nome"
    response = requests.get(url, headers={"Accept": "application/json"}, timeout=30)
    response.raise_for_status()
    dados = response.json().get("dados", [])
    logging.info(f"Total de deputados retornados: {len(dados)}")
    return dados


def fetch_despesas_deputado(deputado_id, ano=CURRENT_YEAR):
    """Extrai despesas da cota parlamentar (CEAP) de um deputado específico."""
    url = f"{API_BASE_URL}/deputados/{deputado_id}/despesas?ano={ano}&ordem=ASC&ordenarPor=mes"
    try:
        response = requests.get(url, headers={"Accept": "application/json"}, timeout=15)
        if response.status_code == 200:
            return response.json().get("dados", [])
    except Exception as e:
        logging.warning(f"Falha ao buscar despesas do deputado {deputado_id}: {e}")
    return []


def setup_duckdb(con):
    """Cria os schemas Bronze, Silver e Gold no DuckDB se não existirem."""
    logging.info("Criando schemas no DuckDB (Medallion Architecture)...")
    con.execute("CREATE SCHEMA IF NOT EXISTS bronze;")
    con.execute("CREATE SCHEMA IF NOT EXISTS silver;")
    con.execute("CREATE SCHEMA IF NOT EXISTS gold;")


def populate_bronze(con, deputados, despesas_list):
    """Carrega os dados em estado bruto (Staging) na Camada Bronze."""
    logging.info("Carregando camada Bronze (Staging)...")
    
    # 1. Staging Deputados
    df_deputados = pd.DataFrame(deputados)
    if not df_deputados.empty:
        con.execute("CREATE OR REPLACE TABLE bronze.stg_deputados AS SELECT * FROM df_deputados")
    
    # 2. Staging Despesas
    if despesas_list:
        df_despesas = pd.DataFrame(despesas_list)
        con.execute("CREATE OR REPLACE TABLE bronze.stg_despesas AS SELECT * FROM df_despesas")
    else:
        # Tabela vazia estruturada como fallback caso a API não retorne dados de despesas
        con.execute("""
            CREATE OR REPLACE TABLE bronze.stg_despesas (
                deputado_id INTEGER, ano INTEGER, mes INTEGER, tipoDespesa VARCHAR,
                valorLiquido DECIMAL(12,2), nomeFornecedor VARCHAR
            )
        """)


def transform_silver(con):
    """Transforma os dados brutos da Bronze no modelo dimensional (Silver - Star Schema)."""
    logging.info("Transformando dados para a camada Silver (Modelo Dimensional)...")

    # Dimensão Deputados
    con.execute("""
        CREATE OR REPLACE TABLE silver.dim_deputados AS
        SELECT 
            CAST(id AS INTEGER) AS id_deputado,
            nome AS nome_deputado,
            siglaPartido AS partido,
            siglaUf AS uf,
            CAST(idLegislatura AS INTEGER) AS id_legislatura,
            urlFoto AS url_foto,
            email
        FROM bronze.stg_deputados;
    """)

    # Fato Despesas
    con.execute("""
        CREATE OR REPLACE TABLE silver.fato_despesas AS
        SELECT 
            CAST(deputado_id AS INTEGER) AS id_deputado,
            CAST(ano AS INTEGER) AS ano,
            CAST(mes AS INTEGER) AS mes,
            tipoDespesa AS tipo_despesa,
            CAST(valorLiquido AS DECIMAL(12,2)) AS valor_liquido,
            nomeFornecedor AS fornecedor
        FROM bronze.stg_despesas;
    """)


def generate_gold_obt(con):
    """Gera a One Big Table (OBT) consolidada com índices analíticos na Camada Gold."""
    logging.info("Gerando camada Gold (OBT - One Big Table)...")

    con.execute("""
        CREATE OR REPLACE TABLE gold.obt_eficiencia_deputados AS
        WITH gastos_agregados AS (
            SELECT 
                id_deputado,
                SUM(valor_liquido) AS total_gasto_ceap,
                COUNT(*) AS qtd_lancamentos_gastos
            FROM silver.fato_despesas
            GROUP BY id_deputado
        )
        SELECT 
            d.id_deputado,
            d.nome_deputado,
            d.partido,
            d.uf,
            d.url_foto,
            d.email,
            COALESCE(g.total_gasto_ceap, 0.0) AS total_gasto_ceap,
            COALESCE(g.qtd_lancamentos_gastos, 0) AS qtd_gastos,
            
            -- Nota de Eficiência Financeira (Escala 0 a 10)
            -- Quanto menor o gasto total com cota, maior a pontuação de economia
            ROUND(
                GREATEST(0.0, LEAST(10.0, 
                    10.0 - (COALESCE(g.total_gasto_ceap, 0.0) / 35000.0)
                )), 2
            ) AS nota_eficiencia_geral
            
        FROM silver.dim_deputados d
        LEFT JOIN gastos_agregados g ON d.id_deputado = g.id_deputado
        ORDER BY nota_eficiencia_geral DESC;
    """)


def main():
    os.makedirs("data", exist_ok=True)
    logging.info("Iniciando pipeline ETL da Câmara dos Deputados...")
    
    # 1. Extração de Deputados
    deputados = fetch_deputados()
    if not deputados:
        logging.error("Nenhum deputado retornado da API. Finalizando pipeline.")
        return

    # 2. Extração de Despesas (Processamento de TODOS os deputados sem limitação)
    despesas_todas = []
    total_deputados = len(deputados)
    logging.info(f"Coletando despesas de TODOS os {total_deputados} deputados...")
    
    for idx, dep in enumerate(deputados, start=1):
        dep_id = dep["id"]
        logging.info(f"[{idx}/{total_deputados}] Extraindo despesas do deputado ID {dep_id} ({dep['nome']})...")
        despesas = fetch_despesas_deputado(dep_id, ano=CURRENT_YEAR)
        for des in despesas:
            des["deputado_id"] = dep_id
            despesas_todas.append(des)

    # 3. Conexão ao DuckDB e Execução das Camadas
    con = duckdb.connect(DB_FILE)
    try:
        setup_duckdb(con)
        populate_bronze(con, deputados, despesas_todas)
        transform_silver(con)
        generate_gold_obt(con)
        logging.info("✨ Pipeline ETL concluído com sucesso! Banco 'data/camara.duckdb' gerado.")
    finally:
        con.close()


if __name__ == "__main__":
    main()