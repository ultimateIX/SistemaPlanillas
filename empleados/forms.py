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
            "tipo_contrato",
            "fecha_inicio_contrato",
            "fecha_fin_contrato",
            "jornada",
            "activo",
        ]

        widgets = {
            "dui": forms.TextInput(attrs={"class": "form-control"}),
            "numero_isss": forms.TextInput(attrs={"class": "form-control"}),
            "telefono": forms.TextInput(attrs={"class": "form-control"}),
            "nombre_completo": forms.TextInput(attrs={"class": "form-control"}),
            "correo": forms.EmailInput(attrs={"class": "form-control"}),
            "cargo": forms.TextInput(attrs={"class": "form-control"}),
            "fecha_ingreso": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "salario_mensual": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "tipo_contrato": forms.Select(attrs={"class": "form-control"}),
            "fecha_inicio_contrato": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "fecha_fin_contrato": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "jornada": forms.Select(attrs={"class": "form-control"}),
            "activo": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }