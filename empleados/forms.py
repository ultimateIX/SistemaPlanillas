from django import forms

from .models import Empleado


class EmpleadoForm(forms.ModelForm):

    class Meta:

        model = Empleado

        fields = [

             "dui",
             "numero_isss",
             "telefono",
             "nombre_completo",
             "correo",
             "cargo",
             "fecha_ingreso",
             "salario_mensual",

        ]

        widgets = {

            "dui": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "numero_isss": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "telefono": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "nombre_completo": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),
            "correo": forms.EmailInput(
                attrs={
                    "class": "form-control"
                     }
            ),

            "cargo": forms.TextInput(
                attrs={
                    "class": "form-control"
                     }
            ),

            "fecha_ingreso": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control"
                }
            ),

            "salario_mensual": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01"
                }
            ),

        }

    # ==========================================
    # VALIDAR DUI
    # ==========================================

    def clean_dui(self):

        dui = self.cleaned_data["dui"]

        if Empleado.objects.filter(
            dui=dui
        ).exclude(
            pk=self.instance.pk
        ).exists():

            raise forms.ValidationError(
                "Ya existe un empleado con este DUI."
            )

        return dui

    # ==========================================
    # VALIDAR ISSS
    # ==========================================

    def clean_numero_isss(self):

        numero = self.cleaned_data["numero_isss"]

        if Empleado.objects.filter(
            numero_isss=numero
        ).exclude(
            pk=self.instance.pk
        ).exists():

            raise forms.ValidationError(
                "Ya existe un empleado con este número ISSS."
            )

        return numero