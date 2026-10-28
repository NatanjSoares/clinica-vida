"""Validações de entrada do sistema Clínica Vida+ (reaproveitadas da Tarefa 2)."""


def validar_idade(valor):
    """Converte o valor para inteiro e confere se não é negativo."""
    try:
        idade = int(valor)
    except (ValueError, TypeError):
        raise ValueError("Idade inválida. Digite um número inteiro positivo.")

    if idade < 0:
        raise ValueError("Idade não pode ser negativa.")
    return idade


def validar_telefone(valor):
    """Remove espaços, hífens e parênteses; exige só dígitos e mínimo de 8."""
    telefone = str(valor).strip()
    for caractere in (" ", "-", "(", ")"):
        telefone = telefone.replace(caractere, "")

    if not telefone.isdigit() or len(telefone) < 8:
        raise ValueError("Telefone inválido. Use apenas números, mínimo 8 dígitos.")
    return telefone
