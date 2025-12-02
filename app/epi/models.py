from django.db import models

from app.core.models import Servidor, TimeStampedModel


class EPI(TimeStampedModel):
    """Catalogo de EPIs."""

    nome = models.CharField(max_length=120)
    ca = models.CharField("CA", max_length=20, blank=True)
    validade_ca = models.DateField(null=True, blank=True, help_text="Data de validade do CA (se aplicavel)")
    categoria = models.CharField(max_length=80, blank=True, help_text="Ex.: Protecao respiratoria, ocular, auditiva")
    tamanho = models.CharField(max_length=20, blank=True)
    observacoes = models.TextField(blank=True)
    ativo = models.BooleanField(default=True)

    class Meta:
        ordering = ["nome"]
        verbose_name = "EPI"
        verbose_name_plural = "EPIs"

    def __str__(self):
        return f"{self.nome} (CA {self.ca})" if self.ca else self.nome


class EntregaEPI(TimeStampedModel):
    """Registro de entrega de EPI a um servidor."""

    STATUS_CHOICES = [
        ("ENTREGUE", "Entregue"),
        ("PENDENTE", "Pendente"),
        ("DEVOLVIDO", "Devolvido"),
    ]

    servidor = models.ForeignKey(Servidor, on_delete=models.PROTECT, related_name="entregas_epi")
    epi = models.ForeignKey(EPI, on_delete=models.PROTECT, related_name="entregas")
    quantidade = models.PositiveIntegerField(default=1)
    data_entrega = models.DateField()
    data_validade = models.DateField(null=True, blank=True, help_text="Validade do equipamento entregue")
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default="ENTREGUE")
    observacoes = models.TextField(blank=True)

    class Meta:
        ordering = ["-data_entrega"]
        verbose_name = "Entrega de EPI"
        verbose_name_plural = "Entregas de EPI"

    def __str__(self):
        return f"{self.epi} -> {self.servidor} ({self.data_entrega})"
