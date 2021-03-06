# Generated by Django 3.0.7 on 2021-03-04 01:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OrdenElaboracion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo_elaboracion', models.CharField(max_length=200)),
                ('codigo_producto', models.CharField(max_length=150)),
                ('desc_producto', models.TextField()),
                ('cant_teorica', models.IntegerField()),
                ('vencimiento', models.DateField()),
                ('estado', models.CharField(max_length=15)),
                ('orden_numero', models.IntegerField()),
                ('fecha_emision', models.DateField()),
                ('fecha_vigencia', models.DateField()),
                ('hora_inicio', models.DateTimeField(blank=True, null=True)),
                ('hora_final', models.DateTimeField(blank=True, null=True)),
                ('realizado_por', models.CharField(max_length=200)),
                ('verificado_por', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name': 'Orden de Elaboración',
                'verbose_name_plural': 'Ordenes de Elaboración',
            },
        ),
    ]
