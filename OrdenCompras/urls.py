from django.urls import path
#from . import views
from OrdenCompras import views

OrdenCompras_urlpatterns = [
    #path ('',views.OrdenCompras_view, name='OrdenCompras'),
    #path('add_venta/',views.add_ventas.as_view(),name='AddVenta'),
    #path('export/',views.export_pdf_view, name="ExportPDF"),
    #path('export/<id>/<iva>',views.export_pdf_view, name="ExportPDF"),
    
]
app_name = 'compras'

urlpatterns = [
    path('orden_compra/', views.orden_compra_list, name='orden_compra_list'),
    path('orden_compra/nueva/', views.orden_compra_create, name='orden_compra_create'),
    path('orden_compra/<int:pk>/', views.orden_compra_detail, name='orden_compra_detail'),
    path('orden_compra/<int:pk>/editar/', views.orden_compra_update, name='orden_compra_update'),
    path('orden_compra/<int:pk>/eliminar/', views.orden_compra_delete, name='orden_compra_delete'),
]
