from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render, get_object_or_404

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
