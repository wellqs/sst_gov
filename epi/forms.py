from django import forms

from .models import EPI, EntregaEPI


class EPIForm(forms.ModelForm):
    validade_ca = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"}), required=False, label="Validade do CA"
    )

    class Meta:
        model = EPI
        fields = ["nome", "ca", "validade_ca", "categoria", "tamanho", "observacoes", "ativo"]
        widgets = {"observacoes": forms.Textarea(attrs={"rows": 3})}


class EntregaEPIForm(forms.ModelForm):
    data_entrega = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    data_validade = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}), required=False)

    class Meta:
        model = EntregaEPI
        fields = [
            "servidor",
            "epi",
            "quantidade",
            "data_entrega",
            "data_validade",
            "status",
            "observacoes",
        ]
        widgets = {
            "observacoes": forms.Textarea(attrs={"rows": 3}),
        }
