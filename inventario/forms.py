from django import forms

from .models import Producto


class ProductoForm(forms.ModelForm):

    existencia_inicial = forms.IntegerField(
        min_value=0,
        initial=0,
        required=True,
        label="Existencia inicial",
        widget=forms.NumberInput(
            attrs={
                "class": "form-control"
            }
        )
    )

    class Meta:

        model = Producto

        fields = [
            "codigo",
            "nombre",
            "descripcion",
            "precio_compra",
            "precio_venta",
            "existencia_inicial",
            "activo",
        ]

        widgets = {
            "codigo": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),
            "nombre": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),
            "descripcion": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3
                }
            ),
            "precio_compra": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01"
                }
            ),
            "precio_venta": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01"
                }
            ),
                      "activo": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                    "checked": "checked"
    }
 ),
}

class CompraForm(forms.Form):

    producto = forms.ModelChoiceField(
        queryset=Producto.objects.filter(
            activo=True
        ),
        widget=forms.Select(
            attrs={
                "class": "form-control"
            }
        )
    )

    cantidad = forms.IntegerField(
        min_value=1,
        widget=forms.NumberInput(
            attrs={
                "class": "form-control"
            }
        )
    )

    precio_compra_unitario = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=0,
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "step": "0.01"
            }
        )
    )


class VentaForm(forms.Form):

    producto = forms.ModelChoiceField(
        queryset=Producto.objects.filter(
            activo=True
        ),
        widget=forms.Select(
            attrs={
                "class": "form-control"
            }
        )
    )

    cantidad = forms.IntegerField(
        min_value=1,
        widget=forms.NumberInput(
            attrs={
                "class": "form-control"
            }
        )
    )

    precio_venta_unitario = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=0,
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "step": "0.01"
            }
        )
    )