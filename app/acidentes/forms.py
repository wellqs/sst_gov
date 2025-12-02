from django import forms

from .models import ACIDENTE_STATUS_CHOICES, Acidente, CAT


class AcidenteForm(forms.ModelForm):
    data_ocorrencia = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"}),
        label="Data/hora da ocorrencia",
    )

    class Meta:
        model = Acidente
        fields = [
            "servidor",
            "unidade",
            "setor",
            "data_ocorrencia",
            "tipo",
            "gravidade",
            "descricao",
            "houve_afastamento",
            "dias_afastamento",
            "status",
            "local",
            "testemunhas",
        ]
        widgets = {
            "descricao": forms.Textarea(attrs={"rows": 3}),
            "testemunhas": forms.Textarea(attrs={"rows": 2}),
        }

    def clean(self):
        cleaned = super().clean()
        houve_afastamento = cleaned.get("houve_afastamento")
        dias = cleaned.get("dias_afastamento")
        if houve_afastamento and dias is None:
            self.add_error("dias_afastamento", "Informe os dias de afastamento.")
        if not houve_afastamento:
            cleaned["dias_afastamento"] = None
        return cleaned


class CATForm(forms.ModelForm):
    data_emissao = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"}),
        required=False,
        label="Data de emissao",
    )

    class Meta:
        model = CAT
        fields = ["numero", "data_emissao", "status", "observacoes"]
        widgets = {
            "observacoes": forms.Textarea(attrs={"rows": 3}),
        }
