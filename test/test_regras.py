from itertools import product

import pytest

from regras import consulta_normal, emergencia

# Legenda:
#   A = tem agendamento        B = documentos em dia
#   C = médico disponível      D = pagamentos em dia
#
# Cada linha: (A, B, C, D, esperado_consulta_normal, esperado_emergencia)
# É a mesma tabela verdade do trabalho (Tarefa 3), na mesma ordem das linhas.
TABELA = [
    (False, False, False, False, False, False),  # linha 1
    (False, False, False, True,  False, False),  # linha 2
    (False, False, True,  False, False, False),  # linha 3
    (False, False, True,  True,  False, True),   # linha 4
    (False, True,  False, False, False, False),  # linha 5
    (False, True,  False, True,  False, False),  # linha 6
    (False, True,  True,  False, False, True),   # linha 7
    (False, True,  True,  True,  True,  True),   # linha 8
    (True,  False, False, False, False, False),  # linha 9
    (True,  False, False, True,  False, False),  # linha 10
    (True,  False, True,  False, False, False),  # linha 11
    (True,  False, True,  True,  False, True),   # linha 12
    (True,  True,  False, False, False, False),  # linha 13
    (True,  True,  False, True,  False, False),  # linha 14
    (True,  True,  True,  False, True,  True),   # linha 15
    (True,  True,  True,  True,  True,  True),   # linha 16
]


@pytest.mark.parametrize(
    "a,b,c,d,esperado_cn,esperado_em",
    TABELA,
    ids=[f"linha{i}" for i in range(1, 17)],
)
def test_tabela_verdade(a, b, c, d, esperado_cn, esperado_em):
    assert consulta_normal(a, b, c, d) == esperado_cn
    assert emergencia(a, b, c, d) == esperado_em


# ---------- caso prático da Tarefa 3 ----------
# Sem agendamento (A=F), documentos OK (B=V), médico disponível (C=V),
# pagamentos atrasados (D=F).

def test_caso_pratico_consulta_normal_nao_atende():
    assert consulta_normal(False, True, True, False) is False


def test_caso_pratico_emergencia_atende():
    assert emergencia(False, True, True, False) is True


# ---------- análise: em quantas situações o paciente é atendido? ----------

def test_consulta_normal_atende_em_3_das_16_situacoes():
    total = sum(consulta_normal(a, b, c, d) for a, b, c, d in product([False, True], repeat=4))

    assert total == 3


def test_emergencia_atende_em_6_das_16_situacoes():
    total = sum(emergencia(a, b, c, d) for a, b, c, d in product([False, True], repeat=4))

    assert total == 6


# ---------- a emergência não usa o agendamento ----------

@pytest.mark.parametrize("b,c,d", list(product([False, True], repeat=3)))
def test_emergencia_nao_depende_do_agendamento(b, c, d):
    assert emergencia(True, b, c, d) == emergencia(False, b, c, d)
