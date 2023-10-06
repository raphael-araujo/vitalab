from django.urls import path

from . import views

urlpatterns = [
    path('solicitar_exames/', views.solicitar_exames, name='solicitar_exames'),
    path('fechar_pedido/', views.fechar_pedido, name='fechar_pedido'),
    path('gerenciar_pedidos/', views.gerenciar_pedidos, name='gerenciar_pedidos'),
    path('cancelar_pedido/<int:pedido_id>', views.cancelar_pedido, name='cancelar_pedido'),
    path('gerenciar_exames/', views.gerenciar_exames, name='gerenciar_exames'),
    path('abrir_exame/<int:exame_id>', views.abrir_exame, name='abrir_exame'),
    path('solicitar_senha_exame/<int:exame_id>', views.solicitar_senha_exame, name='solicitar_senha_exame'),
    path('gerar_acesso_medico/', views.gerar_acesso_medico, name='gerar_acesso_medico'),
]
