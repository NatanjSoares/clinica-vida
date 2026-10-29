"""Acesso ao banco para pacientes. Não valida dados: isso é feito antes (validacoes.py)."""

from models import Paciente


def cadastrar(conn, paciente):
    """Guarda o paciente no banco e devolve o id criado."""
    cursor = conn.execute(
        "INSERT INTO pacientes (nome, idade, telefone) VALUES (?, ?, ?)",
        (paciente.nome, paciente.idade, paciente.telefone),
    )
    conn.commit()
    return cursor.lastrowid


def listar(conn):
    """Devolve todos os pacientes, na ordem em que foram cadastrados."""
    linhas = conn.execute(
        "SELECT nome, idade, telefone FROM pacientes ORDER BY id"
    ).fetchall()
    return [Paciente(l["nome"], l["idade"], l["telefone"]) for l in linhas]


def buscar_por_nome(conn, nome):
    """Devolve os pacientes cujo nome contém o texto buscado (ignora maiúsculas)."""
    termo = nome.strip().lower()
    if not termo:
        return []
    return [p for p in listar(conn) if termo in p.nome.lower()]
