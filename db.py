import psycopg2
import os

def criar_tabelas():
    DATABASE_URL = os.environ.get("DATABASE_URL")

    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()

    # Tabela EPI
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS epi (
        id SERIAL PRIMARY KEY,
        nome VARCHAR(100) NOT NULL,
        descricao TEXT,
        quantidade INTEGER NOT NULL,
        data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # Tabela EPC
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS epc (
        id SERIAL PRIMARY KEY,
        nome VARCHAR(100) NOT NULL,
        descricao TEXT,
        quantidade INTEGER NOT NULL,
        data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    conn.commit()
    cursor.close()
    conn.close()
