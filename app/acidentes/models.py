from django.conf import settings
from django.db import models

from app.core.models import Servidor, Setor, Unidade, TimeStampedModel

# Choices reaproveitados em filtros/forms
ACIDENTE_STATUS_CHOICES = [
    ("ABERTO", "Aberto"),
    ("EM_ANALISE", "Em analise"),
    ("ENCERRADO", "Encerrado"),
]


class Acidente(TimeStampedModel):
    """Registro de acidente/doenca ocupacional (S-2210)."""

    TIPO_CHOICES = [
        ("TIPO_ACIDENTE", "Acidente tipico"),
        ("TRAJETO", "Acidente de trajeto"),
        ("DOENCA", "Doenca ocupacional"),
    ]
    GRAVIDADE_CHOICES = [
        ("LEVE", "Leve"),
        ("MODERADO", "Moderado"),
        ("GRAVE", "Grave"),
        ("IMINENTE", "Grave com risco iminente"),
    ]
    STATUS_CHOICES = ACIDENTE_STATUS_CHOICES

    servidor = models.ForeignKey(Servidor, on_delete=models.PROTECT, related_name="acidentes")
    unidade = models.ForeignKey(Unidade, on_delete=models.PROTECT, related_name="acidentes")
    setor = models.ForeignKey(Setor, on_delete=models.PROTECT, related_name="acidentes")
    data_ocorrencia = models.DateTimeField()
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    gravidade = models.CharField(max_length=20, choices=GRAVIDADE_CHOICES, default="LEVE")
    descricao = models.TextField()
    houve_afastamento = models.BooleanField(default=False)
    dias_afastamento = models.PositiveIntegerField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="ABERTO")
    local = models.CharField(max_length=200, blank=True)
    testemunhas = models.TextField(blank=True, help_text="Nomes das testemunhas, se houver.")

    class Meta:
        ordering = ["-data_ocorrencia"]
        verbose_name = "Acidente"
        verbose_name_plural = "Acidentes"

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.servidor} ({self.data_ocorrencia.date()})"


class CAT(TimeStampedModel):
    """Comunicacao de Acidente de Trabalho vinculada ao acidente."""

    STATUS_CAT = [
        ("NAO_ENVIADA", "Nao enviada"),
        ("ENVIADA", "Enviada"),
        ("CANCELADA", "Cancelada"),
    ]

    acidente = models.OneToOneField(Acidente, on_delete=models.CASCADE, related_name="cat")
    numero = models.CharField(max_length=30, blank=True)
    data_emissao = models.DateField(null=True, blank=True)
    responsavel_emissao = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="cats_emitidas",
    )
    status = models.CharField(max_length=20, choices=STATUS_CAT, default="NAO_ENVIADA")
    observacoes = models.TextField(blank=True)

    class Meta:
        verbose_name = "CAT"
        verbose_name_plural = "CATs"

    def __str__(self):
        return self.numero or f"CAT - {self.acidente}"
