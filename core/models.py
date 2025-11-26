from django.conf import settings
from django.db import models


class Unidade(models.Model):
    nome = models.CharField(max_length=150)
    sigla = models.CharField(max_length=20, blank=True)
    descricao = models.TextField(blank=True)
    ativa = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["nome"]
        verbose_name = "Unidade"
        verbose_name_plural = "Unidades"

    def __str__(self):
        return self.sigla or self.nome


class Setor(models.Model):
    unidade = models.ForeignKey(Unidade, on_delete=models.CASCADE, related_name="setores")
    nome = models.CharField(max_length=120)
    descricao = models.TextField(blank=True)
    ativa = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["nome"]
        verbose_name = "Setor"
        verbose_name_plural = "Setores"
        unique_together = ("unidade", "nome")

    def __str__(self):
        return f"{self.nome} - {self.unidade}"


class Cargo(models.Model):
    titulo = models.CharField(max_length=120)
    cbo = models.CharField("CBO", max_length=10, blank=True)
    descricao = models.TextField(blank=True)
    ativo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["titulo"]
        verbose_name = "Cargo"
        verbose_name_plural = "Cargos"

    def __str__(self):
        return self.titulo


class Servidor(models.Model):
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="servidor",
        help_text="Opcional: associa o servidor a um usuario do sistema.",
    )
    nome = models.CharField(max_length=150)
    cpf = models.CharField(max_length=14, unique=True)
    matricula = models.CharField(max_length=30, unique=True)
    email = models.EmailField(blank=True)
    unidade = models.ForeignKey(Unidade, on_delete=models.PROTECT, related_name="servidores")
    setor = models.ForeignKey(Setor, on_delete=models.PROTECT, related_name="servidores")
    cargo = models.ForeignKey(Cargo, on_delete=models.PROTECT, related_name="servidores")
    ativo = models.BooleanField(default=True)
    admissao = models.DateField(null=True, blank=True)
    demissao = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["nome"]
        verbose_name = "Servidor"
        verbose_name_plural = "Servidores"

    def __str__(self):
        return self.nome
