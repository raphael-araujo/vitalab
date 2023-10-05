from django.contrib.auth.models import User
from django.db import models
from django.utils.safestring import mark_safe


class TipoExame(models.Model):
    TIPO_CHOICES = (
        ('I', 'Exame de imagem'),
        ('S', 'Exame de sangue')
    )

    nome = models.CharField(max_length=50)
    tipo = models.CharField(max_length=2, choices=TIPO_CHOICES)
    preco = models.DecimalField(max_digits=7, decimal_places=2)
    disponivel = models.BooleanField(default=False)
    horario_inicial = models.TimeField()
    horario_final = models.TimeField()

    def __str__(self) -> str:
        return self.nome


class SolicitacaoExame(models.Model):
    CHOICE_STATUS = (
        ('E', 'Em análise'),
        ('F', 'Finalizado')
    )

    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    exame = models.ForeignKey(TipoExame, on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=2, choices=CHOICE_STATUS)
    resultado = models.FileField(upload_to='resultados', null=True, blank=True)
    requer_senha = models.BooleanField(default=False)
    senha = models.CharField(max_length=6, null=True, blank=True)

    def badge_template(self):
        if self.status == 'E':
            classes_css = 'bg-warning text-dark'
            texto = "Em análise"
        elif self.status == 'F':
            classes_css = 'bg-success'
            texto = "Finalizado"
        
        return mark_safe(f"<span class='badge bg-primary {classes_css}'>{texto}</span>")

    def __str__(self) -> str:
        return f'{self.usuario} | {self.exame.nome}'


class PedidoExame(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    exames = models.ManyToManyField(SolicitacaoExame)
    agendado = models.BooleanField(default=True)
    data = models.DateTimeField()

    def __str__(self) -> str:
        return f'{self.usuario} | {self.data}'
