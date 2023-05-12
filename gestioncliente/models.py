from django.contrib.auth.models import Group, User #importa los modelos Group y user
from django.db import models #importa los metodos necesarios para trabajar con modellos

class Cliente(models.Model):
    nombre1 = models.CharField(max_length=30, null=True, blank=True, verbose_name='Nombre 1 del cliente')
    nombre2 = models.CharField(max_length=30, null=True, blank=True, verbose_name='Nombre 2 del cliente')
    nombre3 = models.CharField(max_length=30, null=True, blank=True, verbose_name='Nombre 3 del cliente')
    apellido1 = models.CharField(max_length=100, null=True, blank=True, verbose_name='Apellido 1 del cliente')
    apellido2 = models.CharField(max_length=100, null=True, blank=True, verbose_name='Apellido 2 del cliente')
    correo_electronico = models.EmailField() 
    celular = models.IntegerField()
    edad = models.IntegerField()
    direccion_postal = models.IntegerField() 
    created = models.DateTimeField(auto_now_add=True,verbose_name='Fecha Creación')
    updated = models.DateTimeField(auto_now=True,verbose_name='Fecha Actualización')

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['nombre1']   
    def __str__(self):
        return self.nombre1
