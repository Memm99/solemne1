# Generated by Django 2.0.2 on 2023-05-09 05:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ejemplos', '0017_remove_producto_proveedor'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='proveedor',
            field=models.ManyToManyField(to='ejemplos.Proveedor'),
        ),
    ]
