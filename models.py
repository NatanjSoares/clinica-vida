"""Modelos do sistema Clínica Vida+ (reaproveitados da Tarefa 2)."""


class Paciente:
    """Guarda os dados de um paciente: nome, idade e telefone."""

    def __init__(self, nome, idade, telefone):
        self.nome = nome
        self.idade = idade
        self.telefone = telefone

    def __str__(self):
        return f"Nome: {self.nome} | Idade: {self.idade} | Telefone: {self.telefone}"
