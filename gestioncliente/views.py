import json
import pandas as pd
import xlwt
#nuevas importaciones 30-05-2022
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render,redirect,get_object_or_404
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse
from registration.models import Profile

#fin nuevas importaciones 30-05-2022

from django.db.models import Count, Avg, Q
from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.decorators import (
	api_view, authentication_classes, permission_classes)
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from gestioncliente.models import Cliente
from .forms import ClienteForm
#CLIENTE
@login_required
def clientes_main(request):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    template_name = 'gestioncliente/clientes_main.html'
    return render(request,template_name,{'profile':profile})

@login_required
def agregar_cliente(request):
    data = {
        'form': ClienteForm()
    }
    if request.method == 'POST':
        formulario = ClienteForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            messages.add_message(request, messages.INFO, 'cliente creado!')
    return render(request, 'gestioncliente/agregar_cliente.html',data)

@login_required
def listar_cliente(request):
     clientes = Cliente.objects.all()
     data={
         'clientes': clientes
     }
     return render(request, 'gestioncliente/listar_cliente.html',data)
@login_required
def actualizar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    data ={
        'form': ClienteForm(instance=cliente)
    }
    if request.method == 'POST':
        formulario = ClienteForm(data=request.POST,instance=cliente)
        if formulario.is_valid():
            formulario.save()
            return redirect(to="listar_cliente")
    messages.add_message(request, messages.INFO, 'cliente actualizado!')
    return render(request, 'gestioncliente/modificar_cliente.html',data)
@login_required
def eliminar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    cliente.delete()
    messages.add_message(request, messages.INFO, 'cliente eliminado!')
    return redirect(to="listar_cliente")

