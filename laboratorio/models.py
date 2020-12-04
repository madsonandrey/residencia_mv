from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Laboratorio(models.Model):

    dados = models.ForeignKey(User, on_delete=models.CASCADE)

    cnpj = models.CharField(
        max_length=14,
        blank=False,
        null=False,
        verbose_name='CNPJ'
        )

    data_criacao = models.DateTimeField(
        default=timezone.now,
        verbose_name='Data de Criação'
    )

    bairro = models.CharField(
        max_length=255,
        null=False,
        blank=False
    )

    cidade = models.CharField(
        max_length=255,
        null=False,
        blank=False
    )

    estado = models.CharField(
        max_length=2,
        choices=(('AC', 'Acre'),
                 ('AL', 'Alagoas'),
                 ('AP', 'Amapá'),
                 ('AM', 'Amazonas'),
                 ('BA', 'Bahia'),
                 ('CE', 'Ceará'),
                 ('DF', 'Distrito Federal'),
                 ('ES', 'Espírito Santo'),
                 ('GO', 'Goiás'),
                 ('MA', 'Maranhão'),
                 ('MT', 'Mato Grosso'),
                 ('MS', 'Mato Grosso do Sul'),
                 ('MG', 'Minas Gerais'),
                 ('PA', 'Pará'),
                 ('PB', 'Paraíba'),
                 ('PR', 'Paraná'),
                 ('PE', 'Pernambuco'),
                 ('PI', 'Piauí'),
                 ('RJ', 'Rio de Janeiro'),
                 ('RN', 'Rio Grande do Norte'),
                 ('RS', 'Rio Grande do Sul'),
                 ('RO', 'Rondônia'),
                 ('RR', 'Roraima'),
                 ('SC', 'Santa Catarina'),
                 ('SP', 'São Paulo'),
                 ('SE', 'Sergipe'),
                 ('TO', 'Tocantins'),
                 ))

    pais = models.CharField(
        max_length=255,
        null=False,
        blank=False,
        verbose_name='País'
    )

    def __str__(self):
        return f'{self.dados.first_name}'