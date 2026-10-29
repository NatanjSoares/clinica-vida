"""Fila de atendimento da Clínica Vida+ (Tarefa 4).

Regra FIFO: o primeiro que chega é o primeiro a ser atendido.
A fila fica na memória do programa (se o programa reiniciar, ela esvazia).
"""

from collections import deque


class FilaAtendimento:
    """Fila de pacientes esperando atendimento (nome e CPF)."""

    def __init__(self):
        self._fila = deque()

    def entrar(self, nome, cpf):
        """Coloca uma pessoa no fim da fila. O CPF é só guardado, sem validação."""
        self._fila.append({"nome": nome, "cpf": cpf})

    def atender_proximo(self):
        """Tira e devolve a primeira pessoa da fila. Fila vazia devolve None."""
        if not self._fila:
            return None
        return self._fila.popleft()

    def listar(self):
        """Devolve quem está na fila, em ordem. É uma cópia: mexer nela não altera a fila."""
        return [dict(pessoa) for pessoa in self._fila]

    def tamanho(self):
        """Quantas pessoas estão esperando."""
        return len(self._fila)
