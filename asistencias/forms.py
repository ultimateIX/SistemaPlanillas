from django import forms

from .models import Asistencia


class AsistenciaForm(forms.ModelForm):

    class Meta:

        model = Asistencia

        fields = [
            "empleado",
            "fecha",
            "estado",
            "observacion",
        ]

        widgets = {
            "empleado": forms.Select(
                attrs={
                    "class": "form-control"
                }
            ),
            "fecha": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date"
                }
            ),
            "estado": forms.Select(
                attrs={
                    "class": "form-control"
                }
            ),
            "observacion": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3
                }
            ),
        }