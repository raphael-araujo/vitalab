from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.db.models import Value
from django.db.models.functions import Concat
from django.http import FileResponse, HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render

from exames.models import SolicitacaoExame


@staff_member_required
def gerenciar_clientes(request: HttpRequest) -> HttpResponse:
    clientes = User.objects.filter(is_staff=False)

    nome = request.GET.get('nome')
    email = request.GET.get('email')

    if nome:
        clientes = clientes.annotate(
            full_name=Concat('first_name', Value(' '), 'last_name')
        ).filter(full_name__icontains=nome)
    if email:
        clientes = clientes.filter(email__icontains=email)

    context = {
        'clientes': clientes,
        'nome': nome,
        'email': email
    }
    return render(request, 'gerenciar_clientes.html', context)


@staff_member_required
def cliente(request: HttpRequest, cliente_id: int) -> HttpResponse:
    cliente = get_object_or_404(User, id=cliente_id)
    exames = SolicitacaoExame.objects.filter(usuario=cliente)
    print(exames)
    context = {
        'cliente': cliente,
        'exames': exames
    }
    return render(request, 'cliente.html', context)


@staff_member_required
def exame_cliente(request: HttpRequest, exame_id: int) -> HttpResponse:
    exame = get_object_or_404(SolicitacaoExame, id=exame_id)
    return render(request, 'exame_cliente.html', {'exame': exame})


@staff_member_required
def proxy_pdf(request:HttpRequest, exame_id: int) -> HttpResponse:
    exame = get_object_or_404(SolicitacaoExame, id=exame_id)
    response = exame.resultado.open()
    return FileResponse(response)
