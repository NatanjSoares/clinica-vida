"""Conexão com o banco SQLite da Clínica Vida+."""

import sqlite3

SCHEMA = """
CREATE TABLE IF NOT EXISTS pacientes (
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    nome     TEXT    NOT NULL,
    idade    INTEGER NOT NULL CHECK (idade >= 0),
    telefone TEXT    NOT NULL
);
"""


def conectar(caminho="clinica.db"):
    """Abre o banco. Use ':memory:' para um banco temporário (testes)."""
    conn = sqlite3.connect(caminho)
    conn.row_factory = sqlite3.Row  # permite ler colunas pelo nome
    return conn


def criar_tabelas(conn):
    """Cria as tabelas se ainda não existirem."""
    conn.executescript(SCHEMA)
    conn.commit()
