from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from .utils import (email_is_valid, nome_is_valid, password_is_valid,
                    sanitize_input, sobrenome_is_valid, username_is_valid)


def cadastro(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        nome = sanitize_input(request.POST['primeiro_nome'])
        sobrenome = sanitize_input(request.POST['sobrenome'])
        username = sanitize_input(request.POST['username'])
        email = sanitize_input(request.POST['email'])
        senha = sanitize_input(request.POST['senha'])
        confirmar_senha = sanitize_input(request.POST['confirmar_senha'])

        if not nome_is_valid(request, nome):
            return redirect(to='cadastro')

        if not sobrenome_is_valid(request, sobrenome):
            return redirect(to='cadastro')

        if not username_is_valid(request, username):
            return redirect(to='cadastro')

        if not email_is_valid(request, email):
            return redirect(to='cadastro')

        if not password_is_valid(request, senha, confirmar_senha):
            return redirect(to='cadastro')

        user = User.objects.filter(username=username)

        if user.exists():
            messages.warning(
                request, message='Este nome de usuário já está cadastrado.'
            )
            return redirect(to='cadastro')

        user_email = User.objects.filter(email=email)

        if user_email.exists():
            messages.warning(request, message='Este email já está cadastrado.')
            return redirect(to='cadastro')

        try:
            novo_usuario = User.objects.create_user(
                first_name=nome,
                last_name=sobrenome,
                username=username,
                email=email,
                password=senha
            )
            messages.success(request, 'Usuário cadastrado com sucesso.')
            return redirect(to='login')

        except:
            messages.error(request, 'Erro interno do sistema.')
    else:
        # if request.user.is_authenticated():
        #     return redirect(to='')
        return render(request, 'cadastro.html')
