from django import forms
from django.forms import inlineformset_factory
from .models import Producto, Categoria, Proveedor, OrdenCompra, DetalleOrdenCompra



class ProductoForm(forms.ModelForm):
    class Meta: 
        model = Producto
        fields = '__all__'

class CategoriaForm(forms.ModelForm):
    class Meta: 
        model = Categoria
        fields = '__all__'

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor   
        fields = '__all__'

class OrdenCompraForm(forms.ModelForm):
    class Meta:
        model = OrdenCompra
        fields = ['proveedor']

class DetalleOrdenCompraForm(forms.ModelForm):
    class Meta:
        model = DetalleOrdenCompra
        fields = ['producto', 'cantidad', 'precio_unitario']