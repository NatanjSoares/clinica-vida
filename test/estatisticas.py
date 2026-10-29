"""Estatísticas dos pacientes (reaproveitadas de ver_estatisticas da Tarefa 2).

Esta função só CALCULA e devolve os valores. Mostrar na tela (print ou HTML)
é trabalho de quem chamar.
"""


def calcular_estatisticas(pacientes):
    """Recebe uma lista de Paciente e devolve um dicionário com:

    - total: quantidade de pacientes
    - media_idade: idade média
    - mais_novos: lista com TODOS os pacientes da menor idade (pode haver empate)
    - mais_velhos: lista com TODOS os pacientes da maior idade (pode haver empate)

    Se a lista estiver vazia, devolve None.
    """
    if not pacientes:
        return None

    idades = [p.idade for p in pacientes]
    menor = min(idades)
    maior = max(idades)

    return {
        "total": len(pacientes),
        "media_idade": sum(idades) / len(pacientes),
        "mais_novos": [p for p in pacientes if p.idade == menor],
        "mais_velhos": [p for p in pacientes if p.idade == maior],
    }
