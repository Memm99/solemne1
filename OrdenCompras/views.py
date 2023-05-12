#orden de compra


def list_ordenes(request):
    ordenes = OrdenDeCompra.objects.all()
    return render(request, 'lista_ordenes.html', {'ordenes': ordenes})

def detalle_orden(request, pk):
    orden = get_object_or_404(OrdenDeCompra, pk=pk)
    return render(request, 'detalle_orden.html', {'orden': orden})

def nueva_orden(request):
    if request.method == "POST":
        proveedor = get_object_or_404(Proveedor, pk=request.POST.get('proveedor'))
        producto = get_object_or_404(Producto, pk=request.POST.get('producto'))
        cantidad = request.POST.get('cantidad')
        precio_unitario = request.POST.get('precio_unitario')
        orden = OrdenDeCompra(proveedor=proveedor, producto=producto, cantidad=cantidad, precio_unitario=precio_unitario)
        orden.save()
        return redirect('detalle_orden', pk=orden.pk)
    else:
        form = NuevaOrdenForm()
    return render(request, 'nueva_orden.html', {'form': form})
