# Generated by Django 4.2.6 on 2023-11-19 16:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RoomGroup',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('is_state', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Grupo Habitacion',
                'verbose_name_plural': 'Grupos Habitaciones',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='RoomState',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('type', models.CharField(choices=[('D', 'DISPONIBLE'), ('R', 'RESERVADO'), ('O', 'OCUPADO'), ('M', 'MANTENIMIENTO'), ('X', 'REINTEGRO')], default='D', max_length=1, verbose_name='TIPO')),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('color', models.CharField(default='08AB05', max_length=200)),
                ('is_state', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Estado Habitacion',
                'verbose_name_plural': 'Estados Habitaciones',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='RoomType',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('is_state', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Tipo Habitacion',
                'verbose_name_plural': 'Tipo Habitaciones',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('number', models.IntegerField(blank=True, null=True, verbose_name='Numero Habitacion')),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('capacity', models.IntegerField(blank=True, default='', null=True, verbose_name='AFORO DE PERSONAS')),
                ('noon', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Precio 12 Hora')),
                ('day', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Precio 24 Hora')),
                ('refund', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Precio Reintegro')),
                ('person', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Precio adicional por persona')),
                ('is_state', models.BooleanField(default=True)),
                ('group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='rooms.roomgroup')),
                ('state', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='rooms.roomstate')),
                ('type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='rooms.roomtype')),
            ],
            options={
                'verbose_name': 'Habitacion',
                'verbose_name_plural': 'Habitaciones',
                'ordering': ['id'],
            },
        ),
    ]
