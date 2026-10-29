import pytest

from app import create_app


@pytest.fixture
def client(tmp_path):
    """Cliente de teste: 'navega' pelas rotas sem abrir o navegador.

    Cada teste ganha um app novo, com banco e fila próprios (arquivo temporário).
    """
    app = create_app({"TESTING": True, "DATABASE": str(tmp_path / "teste.db")})
    return app.test_client()


def texto(resposta):
    """Devolve o HTML da resposta como texto."""
    return resposta.get_data(as_text=True)


def cadastrar(client, nome="João Silva", idade="45", telefone="(11) 99999-9999"):
    return client.post(
        "/pacientes/novo",
        data={"nome": nome, "idade": idade, "telefone": telefone},
    )


# ---------- início e pacientes ----------

def test_raiz_redireciona_para_pacientes(client):
    resposta = client.get("/")

    assert resposta.status_code == 302
    assert resposta.headers["Location"].endswith("/pacientes")


def test_listar_sem_pacientes(client):
    resposta = client.get("/pacientes")

    assert resposta.status_code == 200
    assert "Nenhum paciente cadastrado." in texto(resposta)


def test_form_de_cadastro_abre(client):
    resposta = client.get("/pacientes/novo")

    assert resposta.status_code == 200
    assert "<form" in texto(resposta)


def test_cadastrar_paciente_valido(client):
    resposta = cadastrar(client)
    assert resposta.status_code == 302  # volta para a lista

    pagina = texto(client.get("/pacientes"))

    assert "João Silva" in pagina
    assert "45" in pagina
    assert "11999999999" in pagina  # telefone guardado sem máscara


@pytest.mark.parametrize(
    "nome,idade,telefone,mensagem",
    [
        ("", "30", "11999999999", "O nome não pode estar vazio."),
        ("Ana", "-5", "11999999999", "Idade não pode ser negativa."),
        ("Ana", "abc", "11999999999", "Idade inválida"),
        ("Ana", "30", "123", "Telefone inválido"),
    ],
)
def test_cadastro_invalido_nao_cadastra(client, nome, idade, telefone, mensagem):
    resposta = cadastrar(client, nome, idade, telefone)

    assert resposta.status_code == 400
    assert mensagem in texto(resposta)
    assert "Nenhum paciente cadastrado." in texto(client.get("/pacientes"))


def test_cadastro_invalido_mantem_o_que_foi_digitado(client):
    resposta = cadastrar(client, nome="Ana", idade="-5")

    assert 'value="Ana"' in texto(resposta)


# ---------- busca ----------

def test_buscar_por_parte_do_nome(client):
    cadastrar(client, nome="João Silva")

    pagina = texto(client.get("/pacientes/buscar?nome=silva"))

    assert "João Silva" in pagina


def test_buscar_nome_inexistente(client):
    cadastrar(client, nome="João Silva")

    pagina = texto(client.get("/pacientes/buscar?nome=carlos"))

    assert "Paciente não encontrado." in pagina


def test_pagina_de_busca_sem_texto_abre(client):
    resposta = client.get("/pacientes/buscar")

    assert resposta.status_code == 200


# ---------- estatísticas ----------

def test_estatisticas_sem_pacientes(client):
    resposta = client.get("/estatisticas")

    assert resposta.status_code == 200
    assert "Nenhum paciente cadastrado." in texto(resposta)


def test_estatisticas_com_pacientes(client):
    cadastrar(client, nome="Maria", idade="20")
    cadastrar(client, nome="Pedro", idade="30")

    pagina = texto(client.get("/estatisticas"))

    assert "Total de pacientes: 2" in pagina
    assert "Idade média: 25.00" in pagina
    assert "Maria" in pagina
    assert "Pedro" in pagina


# ---------- fila ----------

def test_fila_comeca_vazia(client):
    resposta = client.get("/fila")

    assert resposta.status_code == 200
    assert "Ninguém na fila." in texto(resposta)


def test_entrar_na_fila(client):
    resposta = client.post(
        "/fila/entrar",
        data={"nome": "João", "cpf": "111.111.111-11"},
        follow_redirects=True,
    )

    assert resposta.status_code == 200
    assert "João" in texto(resposta)


def test_entrar_na_fila_sem_cpf_gera_erro(client):
    resposta = client.post("/fila/entrar", data={"nome": "João", "cpf": ""})

    assert resposta.status_code == 400
    assert "Ninguém na fila." in texto(client.get("/fila"))


def test_atender_proximo_segue_a_ordem(client):
    client.post("/fila/entrar", data={"nome": "João", "cpf": "111"})
    client.post("/fila/entrar", data={"nome": "Maria", "cpf": "222"})

    primeiro = texto(client.post("/fila/proximo"))
    segundo = texto(client.post("/fila/proximo"))

    assert "Em atendimento: João" in primeiro
    assert "Em atendimento: Maria" in segundo
    assert "Ninguém na fila." in texto(client.get("/fila"))


def test_atender_com_fila_vazia(client):
    resposta = client.post("/fila/proximo")

    assert resposta.status_code == 200
    assert "Fila vazia" in texto(resposta)


# ---------- regras (tabela verdade) ----------

def test_regras_pagina_abre(client):
    resposta = client.get("/regras")

    assert resposta.status_code == 200
    assert "<form" in texto(resposta)


def test_regras_caso_pratico_da_tarefa_3(client):
    # Sem agendamento (A=F), documentos OK (B=V), médico (C=V), pagamento atrasado (D=F)
    resposta = client.post("/regras", data={"b": "on", "c": "on"})
    pagina = texto(resposta)

    assert "Consulta Normal: NÃO ATENDIDO" in pagina
    assert "Emergência: ATENDIDO" in pagina


def test_regras_tudo_marcado_atende_nas_duas(client):
    resposta = client.post("/regras", data={"a": "on", "b": "on", "c": "on", "d": "on"})
    pagina = texto(resposta)

    assert "Consulta Normal: ATENDIDO" in pagina
    assert "Emergência: ATENDIDO" in pagina


def test_regras_nada_marcado_nao_atende_em_nenhuma(client):
    pagina = texto(client.post("/regras", data={}))

    assert "Consulta Normal: NÃO ATENDIDO" in pagina
    assert "Emergência: NÃO ATENDIDO" in pagina


# ---------- isolamento ----------

def test_cada_app_tem_sua_propria_fila_e_seu_proprio_banco(tmp_path):
    app1 = create_app({"TESTING": True, "DATABASE": str(tmp_path / "a.db")})
    app2 = create_app({"TESTING": True, "DATABASE": str(tmp_path / "b.db")})
    c1, c2 = app1.test_client(), app2.test_client()

    c1.post("/fila/entrar", data={"nome": "João", "cpf": "111"})
    cadastrar(c1)

    assert "Ninguém na fila." in texto(c2.get("/fila"))
    assert "Nenhum paciente cadastrado." in texto(c2.get("/pacientes"))


# ---------- CSS ----------

def test_pagina_inclui_o_link_do_css(client):
    pagina = texto(client.get("/pacientes"))

    assert "css/estilo.css" in pagina


def test_arquivo_css_e_servido(client):
    resposta = client.get("/static/css/estilo.css")

    assert resposta.status_code == 200
    assert "text/css" in resposta.content_type


# ---------- JavaScript ----------

def test_pagina_inclui_o_link_do_js(client):
    pagina = texto(client.get("/pacientes"))

    assert "js/app.js" in pagina


def test_arquivo_js_e_servido(client):
    resposta = client.get("/static/js/app.js")

    assert resposta.status_code == 200
    assert "javascript" in resposta.content_type


def test_lista_com_pacientes_tem_campo_de_filtro(client):
    cadastrar(client)

    assert 'id="filtro-tabela"' in texto(client.get("/pacientes"))
