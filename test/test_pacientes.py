from models import Paciente
import pacientes


# ---------- listar ----------

def test_listar_banco_vazio_devolve_lista_vazia(conn):
    assert pacientes.listar(conn) == []


def test_cadastrar_e_listar_devolve_o_paciente(conn):
    pacientes.cadastrar(conn, Paciente("João Silva", 45, "11999999999"))

    lista = pacientes.listar(conn)

    assert len(lista) == 1
    assert isinstance(lista[0], Paciente)
    assert lista[0].nome == "João Silva"
    assert lista[0].idade == 45
    assert lista[0].telefone == "11999999999"


def test_listar_mantem_ordem_de_cadastro(conn):
    pacientes.cadastrar(conn, Paciente("Maria", 30, "11988887777"))
    pacientes.cadastrar(conn, Paciente("Pedro", 50, "11977776666"))
    pacientes.cadastrar(conn, Paciente("Ana", 22, "11966665555"))

    nomes = [p.nome for p in pacientes.listar(conn)]

    assert nomes == ["Maria", "Pedro", "Ana"]


# ---------- cadastrar ----------

def test_cadastrar_devolve_id_novo_a_cada_paciente(conn):
    id1 = pacientes.cadastrar(conn, Paciente("Maria", 30, "11988887777"))
    id2 = pacientes.cadastrar(conn, Paciente("Pedro", 50, "11977776666"))

    assert id1 != id2


# ---------- buscar por nome ----------

def test_buscar_pelo_nome_completo(conn):
    pacientes.cadastrar(conn, Paciente("João Silva", 45, "11999999999"))

    achados = pacientes.buscar_por_nome(conn, "João Silva")

    assert [p.nome for p in achados] == ["João Silva"]


def test_buscar_por_parte_do_nome(conn):
    pacientes.cadastrar(conn, Paciente("João Silva", 45, "11999999999"))

    achados = pacientes.buscar_por_nome(conn, "silva")

    assert [p.nome for p in achados] == ["João Silva"]


def test_buscar_ignora_maiusculas_e_minusculas(conn):
    pacientes.cadastrar(conn, Paciente("João Silva", 45, "11999999999"))

    achados = pacientes.buscar_por_nome(conn, "JOÃO")

    assert len(achados) == 1


def test_buscar_devolve_todos_que_combinam(conn):
    pacientes.cadastrar(conn, Paciente("Maria Souza", 30, "11988887777"))
    pacientes.cadastrar(conn, Paciente("Pedro Souza", 50, "11977776666"))
    pacientes.cadastrar(conn, Paciente("Ana Lima", 22, "11966665555"))

    achados = pacientes.buscar_por_nome(conn, "souza")

    assert [p.nome for p in achados] == ["Maria Souza", "Pedro Souza"]


def test_buscar_nome_inexistente_devolve_lista_vazia(conn):
    pacientes.cadastrar(conn, Paciente("João Silva", 45, "11999999999"))

    assert pacientes.buscar_por_nome(conn, "Carlos") == []


def test_buscar_termo_vazio_devolve_lista_vazia(conn):
    pacientes.cadastrar(conn, Paciente("João Silva", 45, "11999999999"))

    assert pacientes.buscar_por_nome(conn, "   ") == []
