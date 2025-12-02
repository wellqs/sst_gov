from django import forms

from .models import Cargo, Servidor, Setor, Unidade


class UnidadeForm(forms.ModelForm):
    class Meta:
        model = Unidade
        fields = [
            "nome",
            "sigla",
            "cnpj",
            "email_contato",
            "telefone",
            "descricao",
            "logradouro",
            "numero",
            "complemento",
            "bairro",
            "cidade",
            "uf",
            "cep",
            "ativa",
        ]


class SetorForm(forms.ModelForm):
    class Meta:
        model = Setor
        fields = ["unidade", "nome", "codigo", "descricao", "ativa"]


class CargoForm(forms.ModelForm):
    class Meta:
        model = Cargo
        fields = ["titulo", "cbo", "descricao", "ativo"]


class ServidorForm(forms.ModelForm):
    admissao = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}), required=False)
    demissao = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}), required=False)

    class Meta:
        model = Servidor
        fields = [
            "usuario",
            "nome",
            "cpf",
            "matricula",
            "pis",
            "email",
            "telefone",
            "celular",
            "data_nascimento",
            "unidade",
            "setor",
            "cargo",
            "ativo",
            "admissao",
            "demissao",
        ]
        widgets = {
            "data_nascimento": forms.DateInput(attrs={"type": "date"}),
        }
