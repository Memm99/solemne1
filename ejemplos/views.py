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
from ejemplos.models import Proveedor, Producto, Categoria, OrdenCompra,DetalleOrdenCompra
from .forms import ProductoForm, CategoriaForm, ProveedorForm,OrdenCompraForm, DetalleOrdenCompraForm

#PRODUCTOS
@login_required
def agregar_producto(request):

    data = {
        'form': ProductoForm()
    }
    if request.method == 'POST':
        formulario = ProductoForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            messages.add_message(request, messages.INFO, 'Producto creado!')
    return render(request, 'ejemplos/agregar.html',data)

    # profile = Profile.objects.get(user_id=request.user.id)
    # if profile.group_id != 1:
    #     messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
    #     return redirect('check_group_main')
    # template_name = 'ejemplos/agregar.html'
    # return render(request,template_name,{'profile':profile})
@login_required
def listar_producto(request):
     productos = Producto.objects.all()
     data={
         'productos': productos
     }
     return render(request, 'ejemplos/listar.html',data)
@login_required
def actualizar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    data ={
        'form': ProductoForm(instance=producto)
    }
    if request.method == 'POST':
        formulario = ProductoForm(data=request.POST,instance=producto)
        if formulario.is_valid():
            formulario.save()
            return redirect(to="listar_producto")
    messages.add_message(request, messages.INFO, 'Producto actualizado!')
    return render(request, 'ejemplos/modificar.html',data)
@login_required
def eliminar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    producto.delete()
    messages.add_message(request, messages.INFO, 'Producto eliminado!')
    return redirect(to="listar_producto")

#CATEGORIAS
@login_required
def agregar_categoria(request):
    data = {
        'form': CategoriaForm()
    }
    if request.method == 'POST':
        formulario = CategoriaForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            messages.add_message(request, messages.INFO, 'Categoria creada!')
    return render(request, 'ejemplos/agregar_categoria.html',data)
    # profile = Profile.objects.get(user_id=request.user.id)
    # if profile.group_id != 1:
    #     messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
    #     return redirect('check_group_main')
    # template_name = 'ejemplos/agregar.html'
    # return render(request,template_name,{'profile':profile})
@login_required
def listar_categoria(request):
     categorias = Categoria.objects.all()
     data={
         'categoria': categorias
     }
     return render(request, 'ejemplos/listar_categoria.html',data)
@login_required
def modificar_categoria(request, id):
    categoria = get_object_or_404(Categoria, id=id)
    data ={
        'form': CategoriaForm(instance=categoria)
    }
    if request.method == 'POST':
        formulario = CategoriaForm(data=request.POST,instance=categoria)
        if formulario.is_valid():
            formulario.save()
            return redirect(to="listar_categoria")
    messages.add_message(request, messages.INFO, 'Categoria modificada!')
    return render(request, 'ejemplos/modificar_categoria.html',data)
@login_required
def eliminar_categoria(request, id):
    categoria = get_object_or_404(Categoria, id=id)
    categoria.delete()
    messages.add_message(request, messages.INFO, 'Categoria eliminada!')
    return redirect(to="listar_categoria")

@login_required
def ejemplos_main(request):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    template_name = 'ejemplos/ejemplos_main.html'
    return render(request,template_name,{'profile':profile})

#########################
#CARGA MASIVA PRODUCTO
@login_required
def ejemplos_carga_masiva(request):
    profiles = Profile.objects.get(user_id = request.user.id)
    if profiles.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    template_name = 'ejemplos/ejemplos_carga_masiva.html'
    return render(request,template_name,{'profiles':profiles})

@login_required
def import_file(request):
    profiles = Profile.objects.get(user_id = request.user.id)
    if profiles.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="archivo_importacion.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('carga_masiva')
    row_num = 0
    columns = ['Nombre Producto','Precio','Descripcion','Talla','Categoria']
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    font_style = xlwt.XFStyle()
    date_format = xlwt.XFStyle()
    date_format.num_format_str = 'dd/MM/yyyy'
    for row in range(1):
        row_num += 1
        for col_num in range(5):
            if col_num == 0:
                ws.write(row_num, col_num, 'ej: producto' , font_style)
            if col_num == 1:                           
                ws.write(row_num, col_num, '10000' , font_style)
            if col_num == 2:                           
                ws.write(row_num, col_num, 'Polera de diseñador...' , font_style)
            if col_num == 3:                           
                ws.write(row_num, col_num, 'xs,s,m,l,xl' , font_style)
            if col_num == 4:                           
                ws.write(row_num, col_num, '1,2,3...' , font_style)
    wb.save(response)
    return response  

@login_required
def ejemplos_carga_masiva_save(request):
    profiles = Profile.objects.get(user_id = request.user.id)
    if profiles.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')

    if request.method == 'POST':
        #try:
        print(request.FILES['myfile'])
        data = pd.read_excel(request.FILES['myfile'])
        df = pd.DataFrame(data)
        acc = 0
        for item in df.itertuples():
            #capturamos los datos desde excel
            nombre = str(item[1])            
            precio = int(item[2])
            descripcion = str(item[3])            
            talla = str(item[4])
            categoria_id = str(item[5])
            producto_save = Producto(
                nombre = nombre,            
                precio = precio,
                descripcion = descripcion,            
                talla = talla,
                categoria_id = categoria_id,         
                
                )
            producto_save.save()
        messages.add_message(request, messages.INFO, 'Carga masiva finalizada, se importaron '+str(acc)+' registros')
        return redirect('ejemplos_carga_masiva')    
#####################################
#########################
#CARGA MASIVA CATEGORIA
@login_required
def carga_masiva_categoria(request):
    profiles = Profile.objects.get(user_id = request.user.id)
    if profiles.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    template_name = 'ejemplos/carga_masiva_categoria.html'
    return render(request,template_name,{'profiles':profiles})

@login_required
def import_file_categoria(request):
    profiles = Profile.objects.get(user_id = request.user.id)
    if profiles.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="archivo_importacion.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('carga_masiva')
    row_num = 0
    columns = ['Nombre Categoria']
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    font_style = xlwt.XFStyle()
    date_format = xlwt.XFStyle()
    date_format.num_format_str = 'dd/MM/yyyy'
    for row in range(1):
        row_num += 1
        for col_num in range(1):
            if col_num == 0:
                ws.write(row_num, col_num, 'ej: categoria' , font_style)
    wb.save(response)
    return response  

@login_required
def categoria_carga_masiva_save(request):
    profiles = Profile.objects.get(user_id = request.user.id)
    if profiles.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')

    if request.method == 'POST':
        #try:
        print(request.FILES['myfile'])
        data = pd.read_excel(request.FILES['myfile'])
        df = pd.DataFrame(data)
        acc = 0
        for item in df.itertuples():
            #capturamos los datos desde excel
            nombre = str(item[1])            
            categoria_save = Categoria(
                nombre = nombre,                   
                )
            categoria_save.save()
        messages.add_message(request, messages.INFO, 'Carga masiva finalizada, se importaron '+str(acc)+' registros')
        return redirect('carga_masiva_categoria')    
#####################################
@login_required
def proveedor_main(request):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    template_name = 'ejemplos/proveedor_main.html'
    return render(request,template_name,{'profile':profile})
@login_required
def agregar_proveedor(request):
    data = {
        'form': ProveedorForm()
    }
    if request.method == 'POST':
        formulario = ProveedorForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            messages.add_message(request, messages.INFO, 'Proveedor creado!')
    return render(request, 'ejemplos/agregar_proveedor.html',data)
@login_required
def listar_proveedor(request):
     proveedor = Proveedor.objects.all()
     data={
         'proveedor': proveedor
     }
     return render(request, 'ejemplos/listar_proveedor.html',data)
@login_required
def actualizar_proveedor(request, id):
    proveedor = get_object_or_404(Proveedor, id=id)
    data ={
        'form': ProveedorForm(instance=proveedor)
    }
    if request.method == 'POST':
        formulario = ProveedorForm(data=request.POST,instance=proveedor)
        if formulario.is_valid():
            formulario.save()
            return redirect(to="listar_proveedor")
    messages.add_message(request, messages.INFO, 'proveedor actualizado!')
    return render(request, 'ejemplos/actualizar_proveedor.html',data)

@login_required
def eliminar_proveedor(request, id):
    proveedor = get_object_or_404(Proveedor, id=id)

    proveedor.delete()
    messages.add_message(request, messages.INFO, 'proveedor eliminado!')
    return redirect(to="listar_proveedor")

######################

@login_required
def ejemplos_proyect_list(request):
        productos = Producto.objects.all()
        data={
            'productos': productos
            }
        template_name = 'ejemplos/ejemplos_proyect_list.html'
        return render(request, 'ejemplos/ejemplos_proyect_list.html',data)

@login_required
def ejemplos_proyect_new(request):
    proveedor_list = Proveedor.objects.all()
    template_name = 'ejemplos/ejemplos_proyect_new.html'
    return render(request,template_name,{'proveedor_list':proveedor_list})

@login_required
def ejemplos_proyect_save(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        precio = request.POST.get('precio')
        descripcion = request.POST.get('descripcion')
        talla = request.POST.get('talla')
        categoria_id = request.POST.get('categoria_id')
        proveedores = request.POST.getlist('proveedor')
        producto = Producto(
            nombre = nombre,
            precio=precio,
            descripcion = descripcion,
            talla=talla,
            categoria_id=categoria_id
            )
        producto.save()

        if proveedores: 
            for a in proveedores:
                producto.proveedor.add(a) #guarda muchos a mucho
        messages.add_message(request, messages.INFO, 'producto creado')   
        return redirect('ejemplos_proyect_list')
    else:
        messages.add_message(request, messages.INFO, 'Error al crear el proyecto')   
        return redirect('ejemplos_proyect_list')

@login_required
def ejemplos_proyect_edit(request, producto_id):
    producto_data = Producto.objects.get(pk=producto_id)
    proveedor_data = Proveedor.objects.filter(producto__id = producto_data.id)
    proveedor_data_list = []
    for a in proveedor_data:
        proveedor_data_list.append(a.id)
    proveedor_list = Proveedor.objects.all()
    template_name = 'ejemplos/ejemplos_proyect_edit.html'
    return render(request,template_name,{'producto_data':producto_data,'proveedor_data_list':proveedor_data_list,'proveedor_list':proveedor_list})

@login_required
def ejemplos_proyect_edit_save(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        nombre = request.POST.get('nombre')
        precio = request.POST.get('precio')
        descripcion = request.POST.get('descripcion')
        talla = request.POST.get('talla')
        categoria_id = request.POST.get('categoria_id')
        proveedores = request.POST.getlist('proveedor')
        Producto.objects.filter(pk=id).update(nombre = nombre)
        Producto.objects.filter(pk=id).update(precio = precio)
        Producto.objects.filter(pk=id).update(descripcion = descripcion)
        Producto.objects.filter(pk=id).update(talla = talla)
        Producto.objects.filter(pk=id).update(categoria_id = categoria_id)
        
        producto = Producto.objects.get(pk=id)#carga el producto que usaremos para muchos a muchos
        #actualizmos proveedores
        proveedor_data = Proveedor.objects.filter(producto__id = id)
        for a in proveedor_data:
            producto.proveedor.remove(a) #elimina muchos a mucho
        if proveedores: 
            for a in proveedores:
                producto.proveedor.add(a) #guarda muchos a mucho        
        messages.add_message(request, messages.INFO, 'proyecto creado')   
        return redirect('ejemplos_proyect_list')
    else:
        messages.add_message(request, messages.INFO, 'Error al crear el proyecto')   
        return redirect('ejemplos_proyect_list')

##############


def lista_ordenes_compra(request):
    ordenes = OrdenCompra.objects.all()
    return render(request, 'ejemplos/lista_ordenes_compra.html', {'ordenes': ordenes})

def crear_orden_compra(request):
    if request.method == 'POST':
        orden_form = OrdenCompraForm(request.POST)
        detalle_form = DetalleOrdenCompraForm(request.POST)
        if orden_form.is_valid() and detalle_form.is_valid():
            orden = orden_form.save()
            detalle = detalle_form.save(commit=False)
            detalle.orden_compra = orden
            detalle.save()
            return redirect('lista_ordenes_compra')
    else:
        orden_form = OrdenCompraForm()
        detalle_form = DetalleOrdenCompraForm()
    return render(request, 'ejemplos/crear_orden_compra.html', {'orden_form': orden_form, 'detalle_form': detalle_form})

def editar_orden_compra(request, orden_id):
    orden = get_object_or_404(OrdenCompra, pk=orden_id)
    if request.method == 'POST':
        orden_form = OrdenCompraForm(request.POST, instance=orden)
        detalle_form = DetalleOrdenCompraForm(request.POST, instance=orden.detalles.first())
        if orden_form.is_valid() and detalle_form.is_valid():
            orden = orden_form.save()
            detalle = detalle_form.save(commit=False)
            detalle.orden_compra = orden
            detalle.save()
            return redirect('lista_ordenes_compra')
    else:
        orden_form = OrdenCompraForm(instance=orden)
        detalle_form = DetalleOrdenCompraForm(instance=orden.detalles.first())
    return render(request, 'ejemplos/editar_orden_compra.html', {'orden_form': orden_form, 'detalle_form': detalle_form})
def eliminar_orden_compra(request, orden_id):
    orden = get_object_or_404(OrdenCompra, pk=orden_id)
    if request.method == 'POST':
        orden.delete()
        return redirect('lista_ordenes_compra')
    return render(request, 'ejemplos/eliminar_orden_compra.html', {'orden': orden})
def order_main(request):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    template_name = 'ejemplos/order_main.html'
    return render(request,template_name,{'profile':profile})




