from django import forms

from .models import AusenciaIncapacidad


class AusenciaIncapacidadForm(forms.ModelForm):

    class Meta:

        model = AusenciaIncapacidad

        fields = [
            "empleado",
            "tipo",
            "fecha_inicio",
            "fecha_fin",
            "motivo",
            "observaciones",
            "documento",
            "estado",
        ]

        widgets = {
            "empleado": forms.Select(
                attrs={
                    "class": "form-control"
                }
            ),
            "tipo": forms.Select(
                attrs={
                    "class": "form-control"
                }
            ),
            "fecha_inicio": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date"
                }
            ),
            "fecha_fin": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date"
                }
            ),
            "motivo": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),
            "observaciones": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3
                }
            ),
            "documento": forms.ClearableFileInput(
                attrs={
                    "class": "form-control"
                }
            ),
            "estado": forms.Select(
                attrs={
                    "class": "form-control"
                }
            ),
        }