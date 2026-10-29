import pytest

from models import Paciente
from estatisticas import calcular_estatisticas


def _pacientes(*idades):
    """Cria uma lista de pacientes só com as idades dadas (nomes P1, P2, ...)."""
    return [Paciente(f"P{i}", idade, "11999999999") for i, idade in enumerate(idades, start=1)]


def _nomes(lista):
    return [p.nome for p in lista]


def test_lista_vazia_devolve_none():
    assert calcular_estatisticas([]) is None


def test_total_de_pacientes():
    resultado = calcular_estatisticas(_pacientes(20, 30, 40))

    assert resultado["total"] == 3


def test_media_de_idade_inteira():
    resultado = calcular_estatisticas(_pacientes(20, 30, 40))

    assert resultado["media_idade"] == pytest.approx(30.0)


def test_media_de_idade_com_decimal():
    resultado = calcular_estatisticas(_pacientes(20, 25))

    assert resultado["media_idade"] == pytest.approx(22.5)


def test_paciente_mais_novo():
    resultado = calcular_estatisticas(_pacientes(40, 20, 30))

    assert _nomes(resultado["mais_novos"]) == ["P2"]


def test_paciente_mais_velho():
    resultado = calcular_estatisticas(_pacientes(40, 20, 30))

    assert _nomes(resultado["mais_velhos"]) == ["P1"]


def test_um_paciente_so_e_o_mais_novo_e_o_mais_velho():
    resultado = calcular_estatisticas(_pacientes(33))

    assert resultado["total"] == 1
    assert resultado["media_idade"] == pytest.approx(33.0)
    assert _nomes(resultado["mais_novos"]) == ["P1"]
    assert _nomes(resultado["mais_velhos"]) == ["P1"]


def test_empate_no_mais_novo_devolve_todos_os_empatados():
    resultado = calcular_estatisticas(_pacientes(20, 50, 20, 30))

    assert _nomes(resultado["mais_novos"]) == ["P1", "P3"]


def test_empate_no_mais_velho_devolve_todos_os_empatados():
    resultado = calcular_estatisticas(_pacientes(60, 50, 60, 30))

    assert _nomes(resultado["mais_velhos"]) == ["P1", "P3"]
