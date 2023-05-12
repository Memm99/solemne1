from django.contrib.auth.models import Group, User #importa los modelos Group y user
from django.db import models #importa los metodos necesarios para trabajar con modellos

class Proveedor(models.Model):
    nombre = models.CharField(max_length=100, null=True, blank=True, verbose_name='Nombre Proveedor')
    apellido = models.CharField(max_length=100, null=True, blank=True, verbose_name='Apellido Proveedor')
    celular = models.IntegerField()
    empresa = models.CharField(max_length=100, null=True, blank=True, verbose_name='Nombre empresa')
    descripcion=models.CharField(max_length=250, null=True, blank=True, verbose_name='Descripcion de los productos')   
    created = models.DateTimeField(auto_now_add=True,verbose_name='Fecha Creación')
    updated = models.DateTimeField(auto_now=True,verbose_name='Fecha Actualización')
    class Meta:
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'
        ordering = ['nombre']   
    def __str__(self):
        return self.nombre

def custom_upload_to(instance, filename):
    return 'product/' + filename
       
class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    proveedor=models.ManyToManyField(Proveedor)
    nombre = models.CharField(max_length=100)
    precio = models.IntegerField()
    descripcion = models.TextField()
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)
    talla = models.CharField(max_length=2)

    def __str__(self):
        return self.nombre


class OrdenCompra(models.Model):
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    fecha = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Orden de compra {self.id} - {self.proveedor}"


class DetalleOrdenCompra(models.Model):
    orden_compra = models.ForeignKey(OrdenCompra, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.IntegerField()
    @property
    def total(self):
        return self.cantidad * self.precio_unitario

    def __str__(self):
        return f"Detalle de orden de compra {self.id} - {self.producto}"


