"""Menu de console da Clínica Vida+ (Tarefa 2).

Versão em linha de comando do sistema. Ela NÃO tem regras próprias: reaproveita
os mesmos módulos usados pelo site (validacoes, models, pacientes, estatisticas)
e funciona em laço até o usuário escolher a opção 5 (Sair).

Como usar:
    python cli.py                        usa o banco clinica.db da pasta atual
    python cli.py caminho/do/banco.db    usa outro banco (por exemplo, o do site)
"""

import sys

import db
import estatisticas
import pacientes
from models import Paciente
from validacoes import validar_idade, validar_telefone


def cadastrar_paciente(conn):
    nome = input("Nome do paciente: ").strip()
    if not nome:
        print("\nErro: O nome não pode estar vazio.\n")
        return

    try:
        idade = validar_idade(input("Idade: "))
        telefone = validar_telefone(input("Telefone: "))
    except ValueError as erro:
        print(f"\nErro: {erro}\n")
        return

    pacientes.cadastrar(conn, Paciente(nome, idade, telefone))
    print("\nPaciente cadastrado com sucesso!\n")


def ver_estatisticas(conn):
    dados = estatisticas.calcular_estatisticas(pacientes.listar(conn))
    if dados is None:
        print("\nNenhum paciente cadastrado.\n")
        return

    mais_novos = ", ".join(f"{p.nome} ({p.idade} anos)" for p in dados["mais_novos"])
    mais_velhos = ", ".join(f"{p.nome} ({p.idade} anos)" for p in dados["mais_velhos"])

    print("\n=== Estatísticas ===")
    print(f"Total de pacientes: {dados['total']}")
    print(f"Idade média: {dados['media_idade']:.2f}")
    print(f"Paciente(s) mais novo(s): {mais_novos}")
    print(f"Paciente(s) mais velho(s): {mais_velhos}\n")


def buscar_paciente(conn):
    nome = input("Digite o nome do paciente: ")
    achados = pacientes.buscar_por_nome(conn, nome)

    if achados:
        print("\n=== Paciente encontrado ===")
        for paciente in achados:
            print(paciente)
        print()
    else:
        print("\nPaciente não encontrado.\n")


def listar_pacientes(conn):
    lista = pacientes.listar(conn)
    if not lista:
        print("\nNenhum paciente cadastrado.\n")
        return

    print("\n=== Lista de Pacientes ===")
    for i, paciente in enumerate(lista, start=1):
        print(f"{i}. {paciente}")
    print()


ACOES = {
    "1": cadastrar_paciente,
    "2": ver_estatisticas,
    "3": buscar_paciente,
    "4": listar_pacientes,
}


def menu(conn):
    """Mostra o menu e repete até o usuário escolher 5 (Sair)."""
    while True:
        print("=== SISTEMA CLÍNICA VIDA+ ===")
        print("1. Cadastrar paciente")
        print("2. Ver estatísticas")
        print("3. Buscar paciente")
        print("4. Listar todos os pacientes")
        print("5. Sair")

        try:
            opcao = input("Escolha uma opção: ").strip()

            if opcao == "5":
                print("\nEncerrando o sistema. Até logo!\n")
                break

            acao = ACOES.get(opcao)
            if acao is None:
                print("\nOpção inválida. Tente novamente.\n")
            else:
                acao(conn)
        except (EOFError, KeyboardInterrupt):
            # Ctrl+C ou fim da entrada, em qualquer ponto (inclusive no meio de um cadastro)
            print("\n\nEncerrando o sistema. Até logo!\n")
            break


def main(caminho="clinica.db"):
    conn = db.conectar(caminho)
    db.criar_tabelas(conn)
    try:
        menu(conn)
    finally:
        conn.close()


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "clinica.db")
