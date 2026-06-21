from django.db import models


class Producto(models.Model):

    codigo = models.CharField(
        max_length=50,
        unique=True
    )

    nombre = models.CharField(
        max_length=150
    )

    descripcion = models.TextField(
        blank=True
    )

    precio_compra = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    precio_venta = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    existencia_actual = models.IntegerField(
        default=0
    )

    activo = models.BooleanField(
        default=True
    )

    fecha_registro = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = [
            "nombre"
        ]

    def __str__(self):

        return self.nombre


class MovimientoInventario(models.Model):

    TIPO_MOVIMIENTO = [
        ("ENTRADA", "Compra / Entrada"),
        ("SALIDA", "Venta / Salida"),
    ]

    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,
        related_name="movimientos"
    )

    tipo = models.CharField(
        max_length=20,
        choices=TIPO_MOVIMIENTO
    )

    cantidad = models.PositiveIntegerField()

    precio_unitario = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    total = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    existencia_anterior = models.IntegerField()

    existencia_nueva = models.IntegerField()

    descripcion = models.CharField(
        max_length=200,
        blank=True
    )

    fecha = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = [
            "-fecha"
        ]

    def __str__(self):

        return (
            f"{self.tipo} - "
            f"{self.producto.nombre} - "
            f"{self.cantidad}"
        )