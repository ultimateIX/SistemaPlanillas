from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.shortcuts import render

from .forms import (
    CompraForm,
    ProductoForm,
    VentaForm,
)

from .models import (
    MovimientoInventario,
    Producto,
)


def es_htmx(request):

    return request.headers.get("HX-Request")


@login_required
def productos(request):

    productos = Producto.objects.all()

    template = "inventario/productos.html"

    if es_htmx(request):

        template = "inventario/productos_content.html"

    return render(
        request,
        template,
        {
            "productos": productos
        }
    )


@login_required
def producto_crear(request):

    if request.method == "POST":

        form = ProductoForm(
            request.POST
        )

        if form.is_valid():

            existencia_inicial = form.cleaned_data[
                "existencia_inicial"
            ]

            producto = form.save(
                commit=False
            )
            producto.activo = True

            producto.existencia_actual = existencia_inicial

            producto.save()

            if existencia_inicial > 0:

                MovimientoInventario.objects.create(
                    producto=producto,
                    tipo="ENTRADA",
                    cantidad=existencia_inicial,
                    precio_unitario=producto.precio_compra,
                    total=(
                        Decimal(existencia_inicial)
                        * producto.precio_compra
                    ),
                    existencia_anterior=0,
                    existencia_nueva=existencia_inicial,
                    descripcion="Existencia inicial"
                )

            productos = Producto.objects.all()

            response = render(
                request,
                "inventario/productos_content.html",
                {
                    "productos": productos
                }
            )

            response["HX-Trigger"] = "cerrarModalInventario"

            return response

    else:

        form = ProductoForm()

    return render(
        request,
        "inventario/producto_form.html",
        {
            "form": form
        }
    )


@login_required
def producto_editar(request, id):

    producto = get_object_or_404(
        Producto,
        id=id
    )

    if request.method == "POST":

        form = ProductoForm(
            request.POST,
            instance=producto
        )

        if form.is_valid():

            producto_editado = form.save(
                commit=False
            )

            producto_editado.existencia_actual = (
                producto.existencia_actual
            )

            producto_editado.save()

            productos = Producto.objects.all()

            response = render(
                request,
                "inventario/productos_content.html",
                {
                    "productos": productos
                }
            )

            response["HX-Trigger"] = "cerrarModalInventario"

            return response

    else:

        form = ProductoForm(
            instance=producto,
            initial={
                "existencia_inicial": producto.existencia_actual
            }
        )

    return render(
        request,
        "inventario/producto_form.html",
        {
            "form": form
        }
    )


@login_required
def compras(request):

    form = CompraForm()

    movimientos = MovimientoInventario.objects.filter(
        tipo="ENTRADA"
    )

    template = "inventario/compras.html"

    if es_htmx(request):

        template = "inventario/compras_content.html"

    return render(
        request,
        template,
        {
            "form": form,
            "movimientos": movimientos
        }
    )


@login_required
def registrar_compra(request):

    if request.method == "POST":

        form = CompraForm(
            request.POST
        )

        if form.is_valid():

            producto = form.cleaned_data["producto"]

            cantidad = form.cleaned_data["cantidad"]

            precio = form.cleaned_data[
                "precio_compra_unitario"
            ]

            existencia_anterior = producto.existencia_actual

            existencia_nueva = (
                existencia_anterior
                + cantidad
            )

            total = Decimal(cantidad) * precio

            MovimientoInventario.objects.create(
                producto=producto,
                tipo="ENTRADA",
                cantidad=cantidad,
                precio_unitario=precio,
                total=total,
                existencia_anterior=existencia_anterior,
                existencia_nueva=existencia_nueva,
                descripcion="Compra de producto"
            )

            producto.existencia_actual = existencia_nueva

            producto.precio_compra = precio

            producto.save()

    form = CompraForm()

    movimientos = MovimientoInventario.objects.filter(
        tipo="ENTRADA"
    )

    return render(
        request,
        "inventario/compras_content.html",
        {
            "form": form,
            "movimientos": movimientos
        }
    )


@login_required
def ventas(request):

    form = VentaForm()

    movimientos = MovimientoInventario.objects.filter(
        tipo="SALIDA"
    )

    template = "inventario/ventas.html"

    if es_htmx(request):

        template = "inventario/ventas_content.html"

    return render(
        request,
        template,
        {
            "form": form,
            "movimientos": movimientos
        }
    )


@login_required
def registrar_venta(request):

    if request.method == "POST":

        form = VentaForm(
            request.POST
        )

        if form.is_valid():

            producto = form.cleaned_data["producto"]

            cantidad = form.cleaned_data["cantidad"]

            precio = form.cleaned_data[
                "precio_venta_unitario"
            ]

            if cantidad <= producto.existencia_actual:

                existencia_anterior = (
                    producto.existencia_actual
                )

                existencia_nueva = (
                    existencia_anterior
                    - cantidad
                )

                total = Decimal(cantidad) * precio

                MovimientoInventario.objects.create(
                    producto=producto,
                    tipo="SALIDA",
                    cantidad=cantidad,
                    precio_unitario=precio,
                    total=total,
                    existencia_anterior=existencia_anterior,
                    existencia_nueva=existencia_nueva,
                    descripcion="Venta de producto"
                )

                producto.existencia_actual = existencia_nueva

                producto.precio_venta = precio

                producto.save()

    form = VentaForm()

    movimientos = MovimientoInventario.objects.filter(
        tipo="SALIDA"
    )

    return render(
        request,
        "inventario/ventas_content.html",
        {
            "form": form,
            "movimientos": movimientos
        }
    )


@login_required
def historial_movimientos(request):

    movimientos = MovimientoInventario.objects.all()

    template = "inventario/historial.html"

    if es_htmx(request):

        template = "inventario/historial_content.html"

    return render(
        request,
        template,
        {
            "movimientos": movimientos
        }
    )