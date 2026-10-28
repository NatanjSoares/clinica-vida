from models import Paciente


def test_paciente_guarda_os_dados():
    paciente = Paciente("João Silva", 45, "11999999999")

    assert paciente.nome == "João Silva"
    assert paciente.idade == 45
    assert paciente.telefone == "11999999999"


def test_str_mostra_os_dados_organizados():
    paciente = Paciente("João Silva", 45, "11999999999")

    assert str(paciente) == "Nome: João Silva | Idade: 45 | Telefone: 11999999999"


def test_dois_pacientes_sao_independentes():
    a = Paciente("Maria", 30, "11988887777")
    b = Paciente("Pedro", 50, "11977776666")

    assert a.nome != b.nome
    assert a.idade != b.idade
