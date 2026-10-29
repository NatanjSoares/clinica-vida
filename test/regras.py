"""Regras de atendimento da Clínica Vida+ (tabela verdade da Tarefa 3).

Variáveis lógicas:
    a: paciente tem agendamento marcado
    b: paciente está com documentos em dia
    c: há médico disponível no horário
    d: paciente está em dia com os pagamentos

Operadores: "and" é o E (∧) e "or" é o OU (∨).
"""


def consulta_normal(a, b, c, d):
    """CN = (A ∧ B ∧ C) ∨ (B ∧ C ∧ D)"""
    return (a and b and c) or (b and c and d)


def emergencia(a, b, c, d):
    """EM = C ∧ (B ∨ D)

    O parâmetro 'a' existe só para as duas funções serem chamadas do mesmo
    jeito. A regra de emergência NÃO usa o agendamento.
    """
    return c and (b or d)
