import pytest

from db import conectar, criar_tabelas


@pytest.fixture
def conn():
    """Banco novo, vazio e em memória para cada teste (some no final)."""
    conexao = conectar(":memory:")
    criar_tabelas(conexao)
    yield conexao
    conexao.close()
