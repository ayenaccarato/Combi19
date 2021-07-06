# Generated by Django 3.2 on 2021-07-06 02:12

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('dni', models.BigIntegerField(unique=True)),
                ('nombre', models.CharField(max_length=20)),
                ('apellido', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('direccion', models.CharField(max_length=20)),
                ('telefono', models.IntegerField()),
                ('long_contra', models.IntegerField()),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='date joined')),
                ('is_active', models.BooleanField(default=True, verbose_name='account is activated')),
                ('is_admin', models.BooleanField(default=False, verbose_name='staff account')),
                ('is_premium', models.BooleanField(default=False)),
                ('fecha_premium', models.DateTimeField(default=datetime.datetime.now, verbose_name='%m/%d/%Y')),
                ('tipo_usuario', models.IntegerField(default=3)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Anuncio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=20)),
                ('texto', models.CharField(max_length=10000)),
                ('fecha_y_hora', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Ciudad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=30)),
                ('provincia', models.CharField(max_length=25)),
                ('codigo_postal', models.IntegerField()),
                ('pais', models.CharField(default='Argentina', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='InformacionDeContacto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('direccion', models.CharField(max_length=50)),
                ('telefono1', models.IntegerField(blank=True, null=True)),
                ('telefono2', models.IntegerField(blank=True, null=True)),
                ('celular', models.IntegerField(blank=True, null=True)),
                ('descripcion', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Insumo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=60)),
                ('precio', models.FloatField()),
                ('stock', models.IntegerField()),
                ('sabor', models.BooleanField()),
                ('categoria', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Premium',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descuento', models.IntegerField()),
                ('cuota', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Premium_pago',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_user', models.IntegerField()),
                ('fecha', models.DateTimeField(verbose_name='%m/%d/%Y')),
                ('nro_tarjeta', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Ruta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('origen', models.CharField(max_length=30)),
                ('destino', models.CharField(max_length=30)),
                ('nombre', models.CharField(max_length=30)),
                ('km', models.IntegerField()),
                ('duracion', models.IntegerField()),
                ('duracion_en', models.CharField(max_length=10)),
                ('codigo_origen', models.IntegerField()),
                ('codigo_destino', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pasaje', models.IntegerField()),
                ('temperatura', models.CharField(max_length=20)),
                ('olfato', models.BooleanField()),
                ('gusto', models.BooleanField()),
                ('contacto', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Vehiculo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patente', models.CharField(max_length=10)),
                ('marca', models.CharField(max_length=50)),
                ('modelo', models.CharField(max_length=4)),
                ('capacidad', models.IntegerField(verbose_name='Cantidad de asientos')),
                ('premium', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Viaje',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_salida', models.DateTimeField()),
                ('fecha_llegada', models.DateTimeField(verbose_name='%m/%d/%Y')),
                ('hora_salida', models.CharField(max_length=20)),
                ('asientos_total', models.IntegerField(default=0)),
                ('asientos_disponibles', models.IntegerField(default=0)),
                ('vendidos', models.IntegerField()),
                ('precio', models.FloatField()),
                ('estado', models.CharField(max_length=20)),
                ('chofer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('ruta', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to='combi19app.ruta')),
                ('vehiculo', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to='combi19app.vehiculo')),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField(null=True)),
                ('precio_ticket', models.FloatField(null=True)),
                ('id_user', models.IntegerField()),
                ('insumo', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='combi19app.insumo')),
                ('viaje', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to='combi19app.viaje')),
            ],
        ),
        migrations.CreateModel(
            name='Tarjeta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.CharField(max_length=50)),
                ('vencimiento', models.CharField(max_length=6)),
                ('titular', models.CharField(max_length=30)),
                ('emisor', models.CharField(max_length=20)),
                ('codigo', models.IntegerField()),
                ('id_user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Pasaje',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_user', models.BigIntegerField()),
                ('dni', models.BigIntegerField()),
                ('nombre', models.CharField(max_length=20)),
                ('apellido', models.CharField(max_length=20)),
                ('estado', models.CharField(max_length=20)),
                ('nro_asiento', models.IntegerField()),
                ('nro_viaje', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to='combi19app.viaje')),
                ('tarjeta', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='combi19app.tarjeta')),
            ],
        ),
        migrations.CreateModel(
            name='Comentario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usuario_dni', models.BigIntegerField()),
                ('usuario_nombre', models.CharField(max_length=50)),
                ('texto', models.CharField(max_length=10000)),
                ('fecha_y_hora', models.CharField(max_length=50)),
                ('viaje', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to='combi19app.viaje')),
            ],
        ),
    ]
