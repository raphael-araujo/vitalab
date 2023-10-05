from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .models import PedidoExame, SolicitacaoExame, TipoExame


@login_required(login_url='login')
def solicitar_exames(request: HttpRequest) -> HttpResponse:
    exames_id = []

    if request.method == 'POST':
        exames_id += request.POST.getlist('exames')

    tipos_exames = TipoExame.objects.all()
    exames_solicitados = tipos_exames.filter(id__in=exames_id)
    preco_total = exames_solicitados.aggregate(total=Sum('preco'))['total']
    # preco_total = sum(exame.preco for exame in solicitacao_exames)

    context = {
        'tipos_exames': tipos_exames,
        'exames_solicitados': exames_solicitados,
        'preco_total': preco_total,
    }
    return render(request, 'solicitar_exames.html', context)


@login_required(login_url='login')
def fechar_pedido(request: HttpRequest) -> HttpResponse:
        exames_id = request.POST.getlist('exames')
        exames_solicitados = TipoExame.objects.filter(id__in=exames_id)
        
        pedido_exame = PedidoExame(
            usuario=request.user,
            data=datetime.now()
        )
        pedido_exame.save()
        
        for exame in exames_solicitados:
            solicitacao_exame_temp = SolicitacaoExame(
                usuario=request.user,
                exame=exame,
                status='E'
            )
            solicitacao_exame_temp.save()
            pedido_exame.exames.add(solicitacao_exame_temp)
        
        pedido_exame.save()

        messages.success(request, 'Pedido de exame concluído com sucesso.')
        return redirect(to='gerenciar_pedidos')


@login_required(login_url='login')
def gerenciar_pedidos(request: HttpRequest) -> HttpResponse:
    pedidos_exames = PedidoExame.objects.filter(usuario=request.user)
    context = {
        'pedidos_exames': pedidos_exames
    }
    return render(request, 'gerenciar_pedidos.html', context)


@login_required(login_url='login')
def cancelar_pedido(request: HttpRequest, pedido_id: int) ->HttpResponse:
    pedido = get_object_or_404(PedidoExame, id=pedido_id)

    if pedido.usuario != request.user:
        messages.error(request, 'Esse pedido não é seu!')

    pedido.agendado = False
    pedido.save()
    messages.warning(request, 'Pedido cancelado com sucesso.')

    return redirect(to='gerenciar_pedidos')


@login_required(login_url='login')
def gerenciar_exames(request: HttpRequest) -> HttpResponse:
    exames = SolicitacaoExame.objects.filter(usuario=request.user)

    return render(request, 'gerenciar_exames.html', {'exames': exames})


@login_required(login_url='login')
def abrir_exame(request:HttpRequest, exame_id: int) -> HttpResponse:
    exame = get_object_or_404(SolicitacaoExame, id=exame_id, usuario=request.user)

    if exame.resultado:
        if not exame.requer_senha:
            return redirect(to=exame.resultado.url)

        return redirect(to='solicitar_senha_exame', exame_id=exame.id)

    raise Http404('O exame não existe.')
