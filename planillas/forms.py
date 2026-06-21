from django import forms

from .models import (
    ConfiguracionPlanilla,
    TramoISR,
    TramoAguinaldo
)


# ==========================================
# CONFIGURACION GENERAL
# ==========================================

class ConfiguracionPlanillaForm(forms.ModelForm):

    class Meta:

        model = ConfiguracionPlanilla

        fields = [

            "porcentaje_isss_empleado",
            "porcentaje_isss_patronal",

            "porcentaje_afp_empleado",
            "porcentaje_afp_patronal",

            "tope_isss",

            "aplicar_exencion_aguinaldo",

            "limite_exento_aguinaldo",

            "porcentaje_quincena_25",

            "antiguedad_minima_quincena_25",

        ]

        widgets = {

            "porcentaje_isss_empleado": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01"
                }
            ),

            "porcentaje_isss_patronal": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01"
                }
            ),

            "porcentaje_afp_empleado": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01"
                }
            ),

            "porcentaje_afp_patronal": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01"
                }
            ),

            "tope_isss": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01"
                }
            ),

            "limite_exento_aguinaldo": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01"
                }
            ),

            "porcentaje_quincena_25": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01"
                }
            ),

            "antiguedad_minima_quincena_25": forms.NumberInput(
                attrs={
                    "class": "form-control"
                }
            ),

        }


# ==========================================
# ISR
# ==========================================

class TramoISRForm(forms.ModelForm):

    class Meta:

        model = TramoISR

        fields = [

            "periodo",

            "desde",

            "hasta",

            "porcentaje",

            "exceso_sobre",

            "cuota_fija",

            "orden",

        ]

        widgets = {

            "periodo": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "desde": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01"
                }
            ),

            "hasta": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01"
                }
            ),

            "porcentaje": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01"
                }
            ),

            "exceso_sobre": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01"
                }
            ),

            "cuota_fija": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01"
                }
            ),

            "orden": forms.NumberInput(
                attrs={
                    "class": "form-control"
                }
            ),

        }


# ==========================================
# AGUINALDO
# ==========================================

class TramoAguinaldoForm(forms.ModelForm):

    class Meta:

        model = TramoAguinaldo

        fields = [

            "antiguedad_desde",

            "antiguedad_hasta",

            "dias_aguinaldo",

            "orden",

        ]

        widgets = {

            "antiguedad_desde": forms.NumberInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "antiguedad_hasta": forms.NumberInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "dias_aguinaldo": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01"
                }
            ),

            "orden": forms.NumberInput(
                attrs={
                    "class": "form-control"
                }
            ),

        }