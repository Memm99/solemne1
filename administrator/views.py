import calendar
import json
import random
import pandas as pd
import xlwt
from turtle import home
import pandas as pd
from datetime import datetime, time, timedelta


from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, GroupManager, User
from django.core.mail import EmailMultiAlternatives
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Avg, Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.http import HttpResponse
from registration.models import Profile


@login_required
def admin_main(request):
    profiles = Profile.objects.get(user_id = request.user.id)
    if profiles.group_id != 1 and profiles.group_id != 2:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    template_name = 'administrator/admin_main.html'
    return render(request,template_name,{'profiles':profiles})

#Flujo usuarios
@login_required
def users_main(request):
    profiles = Profile.objects.get(user_id = request.user.id)
    if profiles.group_id != 1 and profiles.group_id != 2:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    groups = Group.objects.all().exclude(pk=0).order_by('id')
    template_name = 'administrator/users_main.html'
    return render(request,template_name,{'groups':groups,'profiles':profiles})

@login_required
def new_user(request):
    profiles = Profile.objects.get(user_id = request.user.id)
    if profiles.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    if request.method == 'POST':
        grupo = request.POST.get('grupo')
        rut = request.POST.get('rut')
        password = request.POST.get('password')
        first_name = request.POST.get('name')
        last_name = request.POST.get('last_name1')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        #el metodo no contempla validacioens deberá realizarlas
        rut_exist = User.objects.filter(username=rut).count()
        mail_exist = User.objects.filter(email=email).count()
        if rut_exist == 0:
            if mail_exist == 0:
                user = User.objects.create_user(
                    username= rut,
                    email=email,
                    password=rut,
                    first_name=first_name,
                    last_name=last_name,
                    )
                profile_save = Profile(
                    user_id = user.id,
                    group_id = grupo,
                    first_session = 'No',
                    token_app_session = 'No',
                )
                profile_save.save()
                messages.add_message(request, messages.INFO, 'Usuario creado con exito')                             
            else:
                messages.add_message(request, messages.INFO, 'El correo que esta tratando de ingresar, ya existe en nuestros registros')                             
        else:
            messages.add_message(request, messages.INFO, 'El rut que esta tratando de ingresar, ya existe en nuestros registros')                         
    groups = Group.objects.all().exclude(pk=0).order_by('id')
    template_name = 'administrator/new_user.html'
    #messages.success(request, "Usuario nuevo creado")
    return render(request,template_name,{'groups':groups})

@login_required
def list_main(request,group_id):
    profiles = Profile.objects.get(user_id = request.user.id)
    if profiles.group_id != 1 and profiles.group_id != 2:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    group = Group.objects.get(pk=group_id)
    template_name = 'administrator/list_main.html'
    return render(request,template_name,{'group':group,'profiles':profiles})

@login_required
def edit_user(request,user_id):
    profiles = Profile.objects.get(user_id = request.user.id)
    if profiles.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    if request.method == 'POST':
        grupo = request.POST.get('grupo')
        user_id = request.POST.get('user_id')
        first_name = request.POST.get('name')
        last_name = request.POST.get('last_name1')
        email = request.POST.get('email')
        group = request.POST.get('group')
        user_data_count = User.objects.filter(pk=user_id).count()
        user_data = User.objects.get(pk=user_id)
        profile_data = Profile.objects.get(user_id=user_id)    
        if user_data_count == 1:
            if user_data.email != email:
                user_mail_count_all = User.objects.filter(email=email).count()
                if user_mail_count_all > 0:
                    messages.add_message(request, messages.INFO, 'El correo '+str(email)+' ya existe en nuestros registros asociado a otro usuario, por favor utilice otro ')                             
                    return redirect('list_user_active',grupo,page)
            User.objects.filter(pk = user_id).update(first_name = first_name)
            User.objects.filter(pk = user_id).update(last_name = last_name)  
            User.objects.filter(pk = user_id).update(email = email)  
            Profile.objects.filter(user_id = user_id).update(group_id = group)                
            messages.add_message(request, messages.INFO, 'Usuario '+user_data.first_name +' '+user_data.last_name+' editado con éxito')                             
            return redirect('list_user_active',grupo)
        else:
            messages.add_message(request, messages.INFO, 'Hubo un error al editar el Usuario '+user_data.first_name +' '+user_data.last_name)
            return redirect('list_user_active',profile_data.group_id)    
    user_data = User.objects.get(pk=user_id)
    profile_data = Profile.objects.get(user_id=user_id)
    groups = Group.objects.get(pk=profile_data.group_id) 
    profile_list = Group.objects.all().exclude(pk=0).order_by('name')    
    template_name = 'administrator/edit_user.html'
    return render(request,template_name,{'user_data':user_data,'profile_data':profile_data,'groups':groups,'profile_list':profile_list})

@login_required    
def list_user_active(request,group_id,page=None):
    profiles = Profile.objects.get(user_id = request.user.id)
    if profiles.group_id != 1 and profiles.group_id != 2:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    if page == None:
        page = request.GET.get('page')
    else:
        page = page
    if request.GET.get('page') == None:
        page = page
    else:
        page = request.GET.get('page')
    group = Group.objects.get(pk=group_id)
    user_all = []
    user_array = User.objects.filter(is_active='t').filter(profile__group_id=group_id).order_by('first_name')
    for us in user_array:
        profile_data = Profile.objects.get(user_id=us.id)
        name = us.first_name+' '+us.last_name
        user_all.append({'id':us.id,'user_name':us.username,'name':name,'mail':us.email})
    paginator = Paginator(user_all, 30)  
    user_list = paginator.get_page(page)
    template_name = 'administrator/list_user_active.html'
    return render(request,template_name,{'profiles':profiles,'group':group,'user_list':user_list,'paginator':paginator,'page':page})
@login_required    
def list_user_block(request,group_id,page=None):
    profiles = Profile.objects.get(user_id = request.user.id)
    if profiles.group_id != 1 and profiles.group_id != 2:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    if page == None:
        page = request.GET.get('page')
    else:
        page = page
    if request.GET.get('page') == None:
        page = page
    else:
        page = request.GET.get('page')
    group = Group.objects.get(pk=group_id)
    user_all = []
    user_array = User.objects.filter(is_active='f').filter(profile__group_id=group_id).order_by('first_name')
    for us in user_array:
        profile_data = Profile.objects.get(user_id=us.id)
        name = us.first_name+' '+us.last_name
        user_all.append({'id':us.id,'user_name':us.username,'name':name,'mail':us.email})
    paginator = Paginator(user_all, 30)  
    user_list = paginator.get_page(page)
    template_name = 'administrator/list_user_block.html'
    return render(request,template_name,{'profiles':profiles,'group':group,'user_list':user_list,'paginator':paginator,'page':page})
@login_required
def user_block(request,user_id):
    profiles = Profile.objects.get(user_id = request.user.id)
    if profiles.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')

    user_data_count = User.objects.filter(pk=user_id).count()
    user_data = User.objects.get(pk=user_id)
    profile_data = Profile.objects.get(user_id=user_id)       
    if user_data_count == 1:
        User.objects.filter(pk=user_id).update(is_active='f')
        messages.add_message(request, messages.INFO, 'Usuario '+user_data.first_name +' '+user_data.last_name+' bloqueado con éxito')
        return redirect('list_user_active',profile_data.group_id)        
    else:
        messages.add_message(request, messages.INFO, 'Hubo un error al bloquear el Usuario '+user_data.first_name +' '+user_data.last_name)
        return redirect('list_user_active',profile_data.group_id)        
@login_required
def user_activate(request,user_id):
    profiles = Profile.objects.get(user_id = request.user.id)
    if profiles.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    user_data_count = User.objects.filter(pk=user_id).count()
    user_data = User.objects.get(pk=user_id)
    profile_data = Profile.objects.get(user_id=user_id)       
    if user_data_count == 1:
        User.objects.filter(pk=user_id).update(is_active='t')
        messages.add_message(request, messages.INFO, 'Usuario '+user_data.first_name +' '+user_data.last_name+' activado con éxito')
        return redirect('list_user_block',profile_data.group_id)        
    else:
        messages.add_message(request, messages.INFO, 'Hubo un error al activar el Usuario '+user_data.first_name +' '+user_data.last_name)
        return redirect('list_user_block',profile_data.group_id)        

@login_required
def user_delete(request,user_id):
    profiles = Profile.objects.get(user_id = request.user.id)
    if profiles.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')

    user_data_count = User.objects.filter(pk=user_id).count()
    user_data = User.objects.get(pk=user_id)
    profile_data = Profile.objects.get(user_id=user_id)       
    if user_data_count == 1:
        #Profile.objects.filter(user_id=user_id).delete()
        Profile.objects.filter(user_id=user_id).delete()
        User.objects.filter(pk=user_id).delete()
        messages.add_message(request, messages.INFO, 'Usuario '+user_data.first_name +' '+user_data.last_name+' eliminado con éxito')
        return redirect('list_user_block',profile_data.group_id)        
    else:
        messages.add_message(request, messages.INFO, 'Hubo un error al eliminar el Usuario '+user_data.first_name +' '+user_data.last_name)
        return redirect('list_user_block',profile_data.group_id)   
#########################
#CARGA MASIVA PRODUCTO
@login_required
def masiva_usuarios(request):
    profiles = Profile.objects.get(user_id = request.user.id)
    if profiles.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    template_name = 'administrator/masiva_usuarios.html'
    return render(request,template_name,{'profiles':profiles})

@login_required
def import_file_user(request):
    profiles = Profile.objects.get(user_id = request.user.id)
    if profiles.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="archivo_importacion.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('carga_masiva')
    row_num = 0
    columns = ['Grupo','Rut','First_name','Last_name','Email','Mobile']
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    font_style = xlwt.XFStyle()
    date_format = xlwt.XFStyle()
    date_format.num_format_str = 'dd/MM/yyyy'
    for row in range(1):
        row_num += 1
        for col_num in range(6):
            if col_num == 0:
                ws.write(row_num, col_num, 'Grupo' , font_style)
            if col_num == 1:                           
                ws.write(row_num, col_num, 'Rut' , font_style)
            if col_num == 2:                           
                ws.write(row_num, col_num, 'First_name' , font_style)
            if col_num == 3:                           
                ws.write(row_num, col_num, 'Last_name' , font_style)
            if col_num == 4:                           
                ws.write(row_num, col_num, 'Email' , font_style)
            if col_num == 5:                           
                ws.write(row_num, col_num, 'Mobile' , font_style)
    wb.save(response)
    return response  

@login_required
def carga_masiva_save_user(request):
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
        grupo = request.POST.get('grupo')
        rut = request.POST.get('rut')
        first_name = request.POST.get('name')
        last_name = request.POST.get('last_name1')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        #el metodo no contempla validacioens deberá realizarlas
        rut_exist = User.objects.filter(username=rut).count()
        mail_exist = User.objects.filter(email=email).count()

        for item in df.itertuples():
            #capturamos los datos desde excel
            grupo = str(item[1])            
            rut = str(item[2])
            first_name = str(item[3])            
            last_name = str(item[4])
            email = str(item[5])
            mobile=int(item[6])
            user = User.objects.create_user(
                    username= rut,
                    email=email,
                    password=rut,
                    first_name=first_name,
                    last_name=last_name,
                    )
            profile_save = Profile(
                    user_id = user.id,
                    group_id = grupo,
                    first_session = 'No',
                    token_app_session = 'No',
                )
            profile_save.save()
            profile_save.save()
        messages.add_message(request, messages.INFO, 'Carga masiva finalizada')
        return redirect('masiva_usuarios')    



def ejemplo_query_set(request):
    #los query set que estan acontinuación retornan elementos iterables
    #para obtener todos los datos de un modelo
    user_array =  User.objects.all()
    #para obtener todos los datos de un modelo ordenados por algún criterio
    user_array =  User.objects.all().order_by('username') #Ascendente
    user_array =  User.objects.all().order_by('-username') #Descendente
    #para obtener todos los datos de un modelo filtrado por algún criterio
    #para obtener todos los datos de un modelo excluyendo en base a algún criterio
    user_array =  User.objects.all().exclude(username='1234567')
    #si el criterio no existe retornará una lista vacia
    user_array =  User.objects.filter(username='1234567')  
    user_array =  User.objects.filter(username='1234567').order_by('username')#Ascendente
    user_array =  User.objects.filter(username='1234567').order_by('-username')#Descendente
    #para obtener todos los datos de un modelo filtrado por mas de un criterio
    user_array =  User.objects.filter(username='1234567').filter(is_active='t')  
    user_array =  User.objects.filter(username='1234567').filter(is_active='t').order_by('username')#Ascendente
    user_array =  User.objects.filter(username='1234567').filter(is_active='t').order_by('-username')#Descendente
    #para obtener todos los datos de un modelo filtrado por un criterio u otro
    #para usar el o debe importarlo al inicio del archivo from django.db.models Q
    user_array =  User.objects.filter(Q(username='1234567')|Q(is_active='t'))  
    user_array =  User.objects.filter(Q(username='1234567')|Q(is_active='t')).order_by('username')#Ascendente
    user_array =  User.objects.filter(Q(username='1234567')|Q(is_active='t')).order_by('-username')#Descendente

    #para obtener un solo registro
    '''
    si bien se suele usar con el id (pk), se pueden usar con cualquier otro criterio, de usarlo de esta forma debe 
    estar seguro de que le retornará un solo registro, ya que caso contrario le arrojará un error
    '''
    user_data = User.objects.get(pk=1)
    #si desea usar con otro criterio distinto a comparar con pk 
    user_data = User.objects.filter(is_active='t').first()#retorna el primer elemento de la lista
    #para actualizar registros
    User.objects.filter(pk=1).update(is_active='f')#actualiza el registro asociado al id
    User.objects.filter(is_active='f').update(is_active='t')#actualiza todos los registros que cumplen con el criterio
    #para contar registros
    user_data_count = User.objects.filter(pk=1).count()
    #la creación de registros la abordaremos más adelante


    print(user_data_count)
    return redirect('login')
