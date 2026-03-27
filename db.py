import sqlite3

## SQLite NÃO usa CREATE DATABASE / USE

##Tabela EPI
CREATE TABLE epi (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    descricao TEXT,
    quantidade INTEGER NOT NULL,
    tamanho TEXT
);

##Tabela EPC
CREATE TABLE epc (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    descricao TEXT,
    local_instalacao TEXT,
    status_epc TEXT,
    quantidade INTEGER NOT NULL
);
