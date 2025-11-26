from django.db import models

from core.models import Servidor, Unidade, TimeStampedModel


class ExameOcupacional(TimeStampedModel):
    """Exames S-2220 com validade e status."""

    TIPO_CHOICES = [
        ("ADMISSIONAL", "Admissional"),
        ("PERIODICO", "Periódico"),
        ("RETORNO", "Retorno ao trabalho"),
        ("MUDANCA", "Mudança de função"),
        ("DEMISSIONAL", "Demissional"),
    ]
    STATUS_CHOICES = [
        ("AGENDADO", "Agendado"),
        ("REALIZADO", "Realizado"),
        ("VENCIDO", "Vencido"),
    ]

    servidor = models.ForeignKey(Servidor, on_delete=models.PROTECT, related_name="exames")
    unidade = models.ForeignKey(Unidade, on_delete=models.PROTECT, related_name="exames")
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    data_realizacao = models.DateField(null=True, blank=True)
    validade = models.DateField(null=True, blank=True, help_text="Data limite para novo exame.")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="AGENDADO")
    observacoes = models.TextField(blank=True)

    class Meta:
        ordering = ["-data_realizacao", "servidor__nome"]
        verbose_name = "Exame Ocupacional"
        verbose_name_plural = "Exames Ocupacionais"

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.servidor}"
