import pytest

from validacoes import validar_idade, validar_telefone


# ---------- idade ----------

def test_idade_valida_retorna_inteiro():
    assert validar_idade("45") == 45


def test_idade_zero_e_aceita():
    assert validar_idade("0") == 0


def test_idade_negativa_gera_erro():
    with pytest.raises(ValueError, match="negativa"):
        validar_idade("-5")


@pytest.mark.parametrize("entrada", ["abc", "", "4.5", "  "])
def test_idade_nao_numerica_gera_erro(entrada):
    with pytest.raises(ValueError, match="inválida"):
        validar_idade(entrada)


# ---------- telefone ----------

def test_telefone_so_numeros():
    assert validar_telefone("999999999") == "999999999"


def test_telefone_com_mascara_e_limpo():
    # formato do exemplo do enunciado
    assert validar_telefone("(11) 99999-9999") == "11999999999"


def test_telefone_curto_gera_erro():
    with pytest.raises(ValueError, match="Telefone inválido"):
        validar_telefone("1234567")


@pytest.mark.parametrize("entrada", ["abcdefgh", "9999-99a9", ""])
def test_telefone_com_letras_ou_vazio_gera_erro(entrada):
    with pytest.raises(ValueError, match="Telefone inválido"):
        validar_telefone(entrada)
