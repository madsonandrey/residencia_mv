from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Usuario(models.Model):

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    cpf = models.CharField(max_length=14, null=False, blank=False)

    GENDER_CHOICES = (
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('NB', 'Não Binário')
    )
    genero = models.CharField(max_length=2, choices=GENDER_CHOICES, verbose_name='Gênero')

    data_nascimento = models.DateField(verbose_name='Data de Nascimento')

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
        return f'{self.usuario.first_name} {self.usuario.last_name}'


class Exame(models.Model):
    paciente = models.ForeignKey(User, on_delete=models.CASCADE)

    data_criacao = models.DateTimeField(
        default=timezone.now,
        verbose_name='Data de Criação'
    )

    hemacias = models.FloatField(default=None)

    hematocrito = models.FloatField(default=None)

    hemoglobina = models.FloatField(default=None)

    VCM = models.FloatField(default=None)

    HCM = models.FloatField(default=None)

    CHCM = models.FloatField(default=None)

    RDW = models.FloatField(default=None)

    eritroblastos = models.FloatField(default=None)

    leucocitos = models.FloatField(default=None)

    mielocitos = models.FloatField(default=None)

    metamielocitos = models.FloatField(default=None)

    bastonetes = models.FloatField(default=None)

    segmentados = models.FloatField(default=None)

    neutrofilos_totais = models.FloatField(default=None)

    eosinofilos = models.FloatField(default=None)

    basofilos = models.FloatField(default=None)

    linfocitos = models.FloatField(default=None)

    linfocitos_atipicos = models.FloatField(default=None)

    monocitos = models.FloatField(default=None)

    plasmocitos = models.FloatField(default=None)

    plaquetas = models.FloatField(default=None)

    def __str__(self):
        return f'{self.paciente.first_name} {self.paciente.last_name}'


class Exames(models.Model):
    paciente = models.ForeignKey(User, on_delete=models.CASCADE)

    data_criacao = models.DateTimeField(
        default=timezone.now,
        verbose_name='Data de Criação'
    )

    hemacias = models.FloatField(default=None)

    hematocrito = models.FloatField(default=None)

    hemoglobina = models.FloatField(default=None)

    VCM = models.FloatField(default=None)

    HCM = models.FloatField(default=None)

    CHCM = models.FloatField(default=None)

    RDW = models.FloatField(default=None)

    eritroblastos = models.FloatField(default=None)

    leucocitos = models.FloatField(default=None)

    mielocitos = models.FloatField(default=None)

    metamielocitos = models.FloatField(default=None)

    bastonetes = models.FloatField(default=None)

    segmentados = models.FloatField(default=None)

    neutrofilos_totais = models.FloatField(default=None)

    eosinofilos = models.FloatField(default=None)

    basofilos = models.FloatField(default=None)

    linfocitos = models.FloatField(default=None)

    linfocitos_atipicos = models.FloatField(default=None)

    monocitos = models.FloatField(default=None)

    plasmocitos = models.FloatField(default=None)

    plaquetas = models.FloatField(default=None)

    def __str__(self):
        return f'{self.paciente.first_name} {self.paciente.last_name}'