"""Aplicação web (Flask) da Clínica Vida+.

As rotas só recebem o pedido do navegador e chamam os módulos que já existem
e já estão testados: validacoes, models, pacientes, estatisticas, regras e fila.
"""
import os
from flask import Flask, g, redirect, render_template, request, url_for

import db
import estatisticas
import pacientes
import regras
from fila import FilaAtendimento
from models import Paciente
from validacoes import validar_idade, validar_telefone


def create_app(config=None):
    """Cria e configura o app. Cada chamada gera um app novo (banco e fila próprios)."""
    app = Flask(__name__)

    ambiente = os.environ.get("APP_ENV", "development").lower()

    chave_secreta = (
        os.environ.get("SECRET_KEY")
        or (config or {}).get("SECRET_KEY")
    )

    if ambiente == "production" and not chave_secreta:
        raise RuntimeError(
            "Configure a variável de ambiente SECRET_KEY em produção."
        )

    app.config.from_mapping(
        SECRET_KEY=chave_secreta or "chave-local-desenvolvimento",
        DATABASE=os.environ.get(
            "DATABASE_PATH",
            os.path.join(app.instance_path, "clinica.db")
        ),
        TESTING=False,
        DEBUG=ambiente != "production",
    )

    if config:
        app.config.update(config)

    if ambiente == "production":
        app.config["DEBUG"] = False

    # A fila fica em memória e pertence a este app.
    fila_atendimento = FilaAtendimento()

    # Garante que a tabela existe antes da primeira requisição.
    conn = db.conectar(app.config["DATABASE"])
    db.criar_tabelas(conn)
    conn.close()

    # ---------- conexão com o banco (uma por requisição) ----------

    def get_conn():
        if "conn" not in g:
            g.conn = db.conectar(app.config["DATABASE"])
        return g.conn

    @app.teardown_appcontext
    def fechar_conexao(erro):
        conn = g.pop("conn", None)
        if conn is not None:
            conn.close()

    # ---------- início ----------

    @app.route("/")
    def inicio():
        return redirect(url_for("listar_pacientes"))

    # ---------- pacientes ----------

    @app.route("/pacientes")
    def listar_pacientes():
        lista = pacientes.listar(get_conn())
        return render_template("listar.html", lista=lista)

    @app.route("/pacientes/novo", methods=["GET", "POST"])
    def novo_paciente():
        if request.method == "GET":
            return render_template("form.html", erro=None, dados={})

        dados = request.form.to_dict()
        nome = dados.get("nome", "").strip()

        try:
            if not nome:
                raise ValueError("O nome não pode estar vazio.")
            idade = validar_idade(dados.get("idade", ""))
            telefone = validar_telefone(dados.get("telefone", ""))
        except ValueError as e:
            return render_template("form.html", erro=str(e), dados=dados), 400

        pacientes.cadastrar(get_conn(), Paciente(nome, idade, telefone))
        return redirect(url_for("listar_pacientes"))

    @app.route("/pacientes/buscar")
    def buscar_paciente():
        nome = request.args.get("nome", "").strip()
        achados = pacientes.buscar_por_nome(get_conn(), nome) if nome else None
        return render_template("buscar.html", nome=nome, achados=achados)

    # ---------- estatísticas ----------

    @app.route("/estatisticas")
    def ver_estatisticas():
        lista = pacientes.listar(get_conn())
        stats = estatisticas.calcular_estatisticas(lista)
        return render_template("estatisticas.html", stats=stats)

    # ---------- fila de atendimento ----------

    @app.route("/fila")
    def ver_fila():
        return render_template(
            "fila.html", fila=fila_atendimento.listar(), erro=None, mensagem=None
        )

    @app.route("/fila/entrar", methods=["POST"])
    def entrar_na_fila():
        nome = request.form.get("nome", "").strip()
        cpf = request.form.get("cpf", "").strip()

        if not nome or not cpf:
            return render_template(
                "fila.html",
                fila=fila_atendimento.listar(),
                erro="Informe o nome e o CPF.",
                mensagem=None,
            ), 400

        fila_atendimento.entrar(nome, cpf)
        return redirect(url_for("ver_fila"))

    @app.route("/fila/proximo", methods=["POST"])
    def atender_proximo():
        atendido = fila_atendimento.atender_proximo()

        if atendido is None:
            mensagem = "Fila vazia: ninguém para atender."
        else:
            mensagem = f"Em atendimento: {atendido['nome']} (CPF {atendido['cpf']})"

        return render_template(
            "fila.html", fila=fila_atendimento.listar(), erro=None, mensagem=mensagem
        )

    # ---------- regras (tabela verdade) ----------

    @app.route("/regras", methods=["GET", "POST"])
    def verificar_regras():
        marcados = {"a": False, "b": False, "c": False, "d": False}
        resultado = None

        if request.method == "POST":
            # Checkbox marcado aparece no formulário; desmarcado não aparece.
            marcados = {letra: letra in request.form for letra in "abcd"}
            a, b, c, d = (marcados[letra] for letra in "abcd")
            resultado = {
                "consulta_normal": regras.consulta_normal(a, b, c, d),
                "emergencia": regras.emergencia(a, b, c, d),
            }

        return render_template("regras.html", marcados=marcados, resultado=resultado)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=app.config["DEBUG"])
