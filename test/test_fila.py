from fila import FilaAtendimento


def _nomes(lista):
    return [p["nome"] for p in lista]


def test_fila_nova_comeca_vazia():
    fila = FilaAtendimento()

    assert fila.tamanho() == 0
    assert fila.listar() == []


def test_exemplo_do_trabalho_joao_maria_pedro():
    fila = FilaAtendimento()
    fila.entrar("João", "111.111.111-11")
    fila.entrar("Maria", "222.222.222-22")
    fila.entrar("Pedro", "333.333.333-33")

    atendido = fila.atender_proximo()

    assert atendido["nome"] == "João"
    assert _nomes(fila.listar()) == ["Maria", "Pedro"]


def test_atendido_devolve_nome_e_cpf():
    fila = FilaAtendimento()
    fila.entrar("João", "111.111.111-11")

    atendido = fila.atender_proximo()

    assert atendido == {"nome": "João", "cpf": "111.111.111-11"}


def test_atendimentos_seguem_a_ordem_de_chegada():
    fila = FilaAtendimento()
    fila.entrar("João", "111")
    fila.entrar("Maria", "222")
    fila.entrar("Pedro", "333")

    atendidos = [fila.atender_proximo()["nome"] for _ in range(3)]

    assert atendidos == ["João", "Maria", "Pedro"]


def test_tamanho_aumenta_ao_entrar_e_diminui_ao_atender():
    fila = FilaAtendimento()

    fila.entrar("João", "111")
    fila.entrar("Maria", "222")
    assert fila.tamanho() == 2

    fila.atender_proximo()
    assert fila.tamanho() == 1


def test_atender_com_fila_vazia_devolve_none():
    fila = FilaAtendimento()

    assert fila.atender_proximo() is None


def test_depois_de_atender_todos_a_fila_volta_a_ficar_vazia():
    fila = FilaAtendimento()
    fila.entrar("João", "111")

    fila.atender_proximo()

    assert fila.tamanho() == 0
    assert fila.atender_proximo() is None


def test_listar_nao_altera_a_fila():
    fila = FilaAtendimento()
    fila.entrar("João", "111")
    fila.entrar("Maria", "222")

    copia = fila.listar()
    copia.clear()                # mexer na lista devolvida...
    fila.listar()[0]["nome"] = "XXX"  # ...ou nos dados dela...

    assert _nomes(fila.listar()) == ["João", "Maria"]  # ...não muda a fila


def test_duas_filas_sao_independentes():
    fila_a = FilaAtendimento()
    fila_b = FilaAtendimento()

    fila_a.entrar("João", "111")

    assert fila_a.tamanho() == 1
    assert fila_b.tamanho() == 0
