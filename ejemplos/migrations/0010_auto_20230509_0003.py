# Generated by Django 3.2.19 on 2023-05-09 04:03

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('ejemplos', '0009_egreso_productosegreso'),
    ]

    operations = [
        migrations.CreateModel(
            name='DetalleOrdenCompra',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.PositiveIntegerField()),
                ('precio_unitario', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='OrdenCompra',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_compra', models.DateField(default=django.utils.timezone.now)),
                ('productos', models.ManyToManyField(through='ejemplos.DetalleOrdenCompra', to='ejemplos.Producto')),
                ('proveedor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ejemplos.proveedor')),
            ],
        ),
        migrations.RemoveField(
            model_name='productosegreso',
            name='egreso',
        ),
        migrations.RemoveField(
            model_name='productosegreso',
            name='producto',
        ),
        migrations.DeleteModel(
            name='Egreso',
        ),
        migrations.DeleteModel(
            name='ProductosEgreso',
        ),
        migrations.AddField(
            model_name='detalleordencompra',
            name='orden_compra',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ejemplos.ordencompra'),
        ),
        migrations.AddField(
            model_name='detalleordencompra',
            name='producto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ejemplos.producto'),
        ),
    ]
