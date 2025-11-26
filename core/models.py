from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models


class TimeStampedModel(models.Model):
    """Campos de auditoria básicos."""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_%(class)s_set",
        help_text="Usuário que criou o registro.",
    )

    class Meta:
        abstract = True


class Unidade(TimeStampedModel):
    nome = models.CharField(max_length=150)
    sigla = models.CharField(max_length=20, blank=True)
    cnpj = models.CharField(max_length=18, blank=True)
    email_contato = models.EmailField(blank=True)
    telefone = models.CharField(max_length=20, blank=True)
    descricao = models.TextField(blank=True)
    logradouro = models.CharField("Endereço", max_length=150, blank=True)
    numero = models.CharField(max_length=10, blank=True)
    complemento = models.CharField(max_length=80, blank=True)
    bairro = models.CharField(max_length=80, blank=True)
    cidade = models.CharField(max_length=80, blank=True)
    uf = models.CharField(max_length=2, blank=True)
    cep = models.CharField(
        max_length=9,
        blank=True,
        validators=[RegexValidator(r"^[0-9]{5}-?[0-9]{3}$", "CEP no formato 99999-999")],
    )
    ativa = models.BooleanField(default=True)

    class Meta:
        ordering = ["nome"]
        verbose_name = "Unidade"
        verbose_name_plural = "Unidades"

    def __str__(self):
        return self.sigla or self.nome


class Setor(TimeStampedModel):
    unidade = models.ForeignKey(Unidade, on_delete=models.CASCADE, related_name="setores")
    nome = models.CharField(max_length=120)
    codigo = models.CharField(max_length=30, blank=True)
    descricao = models.TextField(blank=True)
    ativa = models.BooleanField(default=True)

    class Meta:
        ordering = ["nome"]
        verbose_name = "Setor"
        verbose_name_plural = "Setores"
        unique_together = ("unidade", "nome")

    def __str__(self):
        return f"{self.nome} - {self.unidade}"


class Cargo(TimeStampedModel):
    titulo = models.CharField(max_length=120)
    cbo = models.CharField("CBO", max_length=10, blank=True)
    descricao = models.TextField(blank=True)
    ativo = models.BooleanField(default=True)

    class Meta:
        ordering = ["titulo"]
        verbose_name = "Cargo"
        verbose_name_plural = "Cargos"

    def __str__(self):
        return self.titulo


class Servidor(TimeStampedModel):
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="servidor",
        help_text="Opcional: associa o servidor a um usuário do sistema.",
    )
    nome = models.CharField(max_length=150)
    cpf = models.CharField(
        max_length=14,
        unique=True,
        validators=[RegexValidator(r"^[0-9]{3}\.?[0-9]{3}\.?[0-9]{3}-?[0-9]{2}$", "CPF no formato 999.999.999-99")],
    )
    matricula = models.CharField(max_length=30, unique=True)
    pis = models.CharField("PIS/PASEP", max_length=15, blank=True)
    email = models.EmailField(blank=True)
    telefone = models.CharField(max_length=20, blank=True)
    celular = models.CharField(max_length=20, blank=True)
    data_nascimento = models.DateField(null=True, blank=True)
    unidade = models.ForeignKey(Unidade, on_delete=models.PROTECT, related_name="servidores")
    setor = models.ForeignKey(Setor, on_delete=models.PROTECT, related_name="servidores")
    cargo = models.ForeignKey(Cargo, on_delete=models.PROTECT, related_name="servidores")
    ativo = models.BooleanField(default=True)
    admissao = models.DateField(null=True, blank=True)
    demissao = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ["nome"]
        verbose_name = "Servidor"
        verbose_name_plural = "Servidores"

    def __str__(self):
        return self.nome
