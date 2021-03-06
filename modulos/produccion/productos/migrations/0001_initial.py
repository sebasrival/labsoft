# Generated by Django 3.0.7 on 2021-03-04 01:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('codigo_producto', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.TextField(blank=True)),
                ('volumen', models.FloatField(blank=True, default=0, null=True)),
                ('color', models.CharField(blank=True, default='', max_length=10)),
                ('precio', models.FloatField()),
                ('cantidad_neto', models.FloatField(blank=True)),
            ],
            options={
                'verbose_name': 'Producto',
                'verbose_name_plural': 'Productos',
            },
        ),
    ]
