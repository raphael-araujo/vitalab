import re

from django.contrib import messages
from django.contrib.messages import constants
from django.utils.html import escape


def sanitize_input(input_value):
    return escape(input_value)

def nome_is_valid(request, nome: str) -> bool:
    """verifica se o campo de nome está vazio"""
    if len(nome.strip()) == 0:
        messages.add_message(request, constants.ERROR, 'O campo "Nome" está vazio')
        return False

    return True


def sobrenome_is_valid(request, sobrenome: str) -> bool:
    """verifica se o campo de sobrenome está vazio"""
    if len(sobrenome.strip()) == 0:
        messages.add_message(request, constants.ERROR, 'O campo "Sobrenome" está vazio')
        return False

    return True


def username_is_valid(request, username: str) -> bool:
    """verifica se o campo de nome de usuário está vazio"""
    if len(username.strip()) == 0:
        messages.add_message(request, constants.ERROR, 'O campo "Username" está vazio')
        return False

    return True


def email_is_valid(request, email: str) -> bool:
    """verifica se o campo e-mail está vazio"""
    if len(email.strip()) == 0:
        messages.add_message(request, constants.ERROR, 'O campo "E-mail" está vazio')
        return False

    return True


def password_is_valid(request, senha: str, confirmar_senha: str) -> bool:
    """verifica se a senha é válida."""

    if len(senha.strip()) == 0 or len(confirmar_senha.strip()) == 0:
        messages.add_message(
            request,
            constants.ERROR,
            'Os campos "Senha" e "Confirmar senha" são obrigatórios',
        )

    if len(senha) < 6:
        messages.add_message(
            request, constants.ERROR, "Sua senha deve conter 6 ou mais caracteres"
        )
        return False

    if not senha == confirmar_senha:
        messages.add_message(request, constants.ERROR, "As senhas não coincidem!")
        return False

    if not re.search("[A-Z]", senha):
        messages.add_message(
            request,
            constants.ERROR,
            "Sua senha deve conter ao menos uma letra maiúscula",
        )
        return False

    if not re.search("[a-z]", senha):
        messages.add_message(
            request,
            constants.ERROR,
            "Sua senha deve conter ao menos uma letra minúscula",
        )
        return False

    if not re.search("[0-9]", senha):
        messages.add_message(
            request, constants.ERROR, "Sua senha deve conter pelo menos um número"
        )
        return False

    return True
