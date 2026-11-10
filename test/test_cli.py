import pacientes
from cli import menu
from models import Paciente


def digitar(monkeypatch, *respostas):
    """Simula o usuário digitando as respostas, na ordem, a cada input()."""
    itens = iter(respostas)
    monkeypatch.setattr("builtins.input", lambda _prompt="": next(itens))


def rodar(conn, capsys):
    """Roda o menu e devolve tudo o que foi impresso na tela."""
    menu(conn)
    return capsys.readouterr().out


# ---------- menu e laço ----------

def test_menu_mostra_as_opcoes_e_sai_com_5(conn, monkeypatch, capsys):
    digitar(monkeypatch, "5")

    saida = rodar(conn, capsys)

    assert "=== SISTEMA CLÍNICA VIDA+ ===" in saida
    assert "1. Cadastrar paciente" in saida
    assert "2. Ver estatísticas" in saida
    assert "3. Buscar paciente" in saida
    assert "4. Listar todos os pacientes" in saida
    assert "5. Sair" in saida
    assert "Encerrando o sistema" in saida


def test_opcao_invalida_volta_ao_menu(conn, monkeypatch, capsys):
    digitar(monkeypatch, "9", "5")

    saida = rodar(conn, capsys)

    assert "Opção inválida" in saida
    assert saida.count("=== SISTEMA CLÍNICA VIDA+ ===") == 2  # mostrou o menu de novo


def test_menu_funciona_em_laco_com_varias_acoes(conn, monkeypatch, capsys):
    digitar(monkeypatch, "1", "Maria", "20", "11988887777", "4", "5")

    saida = rodar(conn, capsys)

    assert "Paciente cadastrado com sucesso!" in saida
    assert "1. Nome: Maria" in saida


def test_fim_da_entrada_encerra_sem_erro(conn, monkeypatch, capsys):
    def sem_entrada(_prompt=""):
        raise EOFError

    monkeypatch.setattr("builtins.input", sem_entrada)

    saida = rodar(conn, capsys)

    assert "Encerrando o sistema" in saida


# ---------- 1. cadastrar ----------

def test_cadastrar_paciente_valido(conn, monkeypatch, capsys):
    digitar(monkeypatch, "1", "João Silva", "45", "(11) 99999-9999", "5")

    saida = rodar(conn, capsys)

    lista = pacientes.listar(conn)
    assert "Paciente cadastrado com sucesso!" in saida
    assert len(lista) == 1
    assert lista[0].nome == "João Silva"
    assert lista[0].telefone == "11999999999"


def test_cadastrar_com_idade_negativa_nao_cadastra(conn, monkeypatch, capsys):
    digitar(monkeypatch, "1", "Ana", "-5", "11999999999", "5")

    saida = rodar(conn, capsys)

    assert "Idade não pode ser negativa." in saida
    assert pacientes.listar(conn) == []


def test_cadastrar_com_telefone_curto_nao_cadastra(conn, monkeypatch, capsys):
    digitar(monkeypatch, "1", "Ana", "30", "123", "5")

    saida = rodar(conn, capsys)

    assert "Telefone inválido" in saida
    assert pacientes.listar(conn) == []


def test_cadastrar_com_nome_vazio_nao_cadastra(conn, monkeypatch, capsys):
    digitar(monkeypatch, "1", "", "5")

    saida = rodar(conn, capsys)

    assert "O nome não pode estar vazio." in saida
    assert pacientes.listar(conn) == []


# ---------- 2. estatísticas ----------

def test_estatisticas_sem_pacientes(conn, monkeypatch, capsys):
    digitar(monkeypatch, "2", "5")

    saida = rodar(conn, capsys)

    assert "Nenhum paciente cadastrado." in saida


def test_estatisticas_com_pacientes(conn, monkeypatch, capsys):
    pacientes.cadastrar(conn, Paciente("Maria", 20, "11988887777"))
    pacientes.cadastrar(conn, Paciente("Pedro", 30, "11977776666"))
    digitar(monkeypatch, "2", "5")

    saida = rodar(conn, capsys)

    assert "Total de pacientes: 2" in saida
    assert "Idade média: 25.00" in saida
    assert "Maria (20 anos)" in saida
    assert "Pedro (30 anos)" in saida


# ---------- 3. buscar ----------

def test_buscar_encontra_por_parte_do_nome(conn, monkeypatch, capsys):
    pacientes.cadastrar(conn, Paciente("João Silva", 45, "11999999999"))
    digitar(monkeypatch, "3", "silva", "5")

    saida = rodar(conn, capsys)

    assert "=== Paciente encontrado ===" in saida
    assert "João Silva" in saida


def test_buscar_nome_inexistente(conn, monkeypatch, capsys):
    pacientes.cadastrar(conn, Paciente("João Silva", 45, "11999999999"))
    digitar(monkeypatch, "3", "carlos", "5")

    saida = rodar(conn, capsys)

    assert "Paciente não encontrado." in saida


# ---------- 4. listar ----------

def test_listar_sem_pacientes(conn, monkeypatch, capsys):
    digitar(monkeypatch, "4", "5")

    saida = rodar(conn, capsys)

    assert "Nenhum paciente cadastrado." in saida


def test_listar_mostra_pacientes_numerados(conn, monkeypatch, capsys):
    pacientes.cadastrar(conn, Paciente("Maria", 20, "11988887777"))
    pacientes.cadastrar(conn, Paciente("Pedro", 30, "11977776666"))
    digitar(monkeypatch, "4", "5")

    saida = rodar(conn, capsys)

    assert "1. Nome: Maria | Idade: 20" in saida
    assert "2. Nome: Pedro | Idade: 30" in saida
