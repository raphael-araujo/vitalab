from django.contrib import admin

from .models import AcessoMedico, PedidoExame, SolicitacaoExame, TipoExame

# Register your models here.


admin.site.register(AcessoMedico)
admin.site.register(PedidoExame)
admin.site.register(SolicitacaoExame)
admin.site.register(TipoExame)
