from django.db import models
from django.utils import timezone
from decimal import Decimal


class Vaca(models.Model):
    nome = models.CharField(max_length=100, help_text="Nome da Vaca (obrigatório)")
    data_nascimento = models.DateField(null=True, blank=True, help_text="Data de nascimento (opcional)")
    pai = models.CharField(max_length=100, null=True, blank=True, help_text="Nome do pai (opcional)")
    mae = models.CharField(max_length=100, null=True, blank=True, help_text="Nome da mãe (opcional)")

    def __str__(self):
        return self.nome


class Ordenha(models.Model):
    vaca = models.ForeignKey(Vaca, on_delete=models.CASCADE, help_text="Vaca que foi ordenhada")
    data_hora = models.DateTimeField(default=timezone.now, help_text="Data e hora da ordenha")
    quantidade_leite = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text="Quantidade de leite em litros"
    )

    def __str__(self):
        return f"Ordenha de {self.vaca.nome} em {self.data_hora.strftime('%d/%m/%Y %H:%M')}"