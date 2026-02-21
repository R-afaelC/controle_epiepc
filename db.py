import psycopg2
import os


-- Tabela EPI
CREATE TABLE IF NOT EXISTS epi (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descricao TEXT,
    quantidade INTEGER NOT NULL,
    tamanho VARCHAR(50)
);

-- Tabela EPC
CREATE TABLE IF NOT EXISTS epc (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descricao TEXT,
    local_instalacao VARCHAR(100),
    status_epc VARCHAR(50),
    quantidade INTEGER NOT NULL
);
