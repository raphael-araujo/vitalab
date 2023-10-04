from django.contrib import admin

from .models import PedidoExame, SolicitacaoExame, TipoExame

# Register your models here.


admin.site.register(PedidoExame)
admin.site.register(SolicitacaoExame)
admin.site.register(TipoExame)
