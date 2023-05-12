from django.urls import path
from gestioncliente import views #importará los métodos que generemos en nuestra app
from django.views.decorators.csrf import csrf_exempt
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
gestioncliente_urlpatterns = [

    path('clientes_main/',views.clientes_main,name="clientes_main"),
    path('agregar_cliente/',views.agregar_cliente,name="agregar_cliente"),
    path('listar_cliente/',views.listar_cliente,name="listar_cliente"),
    path('actualizar_cliente/<id>/',views.actualizar_cliente,name="actualizar_cliente"),
    path('eliminar_cliente/<id>/',views.eliminar_cliente,name="eliminar_cliente"),




    
    ]