# Generated by Django 4.2.5 on 2023-10-04 00:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TipoExame',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=50)),
                ('tipo', models.CharField(choices=[('I', 'Exame de imagem'), ('S', 'Exame de sangue')], max_length=2)),
                ('preco', models.DecimalField(decimal_places=2, max_digits=7)),
                ('disponivel', models.BooleanField(default=False)),
                ('horario_inicial', models.TimeField()),
                ('horario_final', models.TimeField()),
            ],
        ),
        migrations.CreateModel(
            name='SolicitacaoExame',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('E', 'Em análise'), ('F', 'Finalizado')], max_length=2)),
                ('resultado', models.FileField(blank=True, null=True, upload_to='resultados')),
                ('requer_senha', models.BooleanField(default=False)),
                ('senha', models.CharField(blank=True, max_length=6, null=True)),
                ('exame', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='exames.tipoexame')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PedidoExame',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('agendado', models.BooleanField(default=True)),
                ('data', models.DateTimeField()),
                ('exames', models.ManyToManyField(to='exames.solicitacaoexame')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
