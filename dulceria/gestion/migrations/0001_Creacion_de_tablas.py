# Generated by Django 4.2.4 on 2023-08-26 22:10

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CategoriaModel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('nombre', models.TextField()),
                ('nivel_azucar', models.TextField(choices=[['MA', 'MUY_ALTO'], ['ALTO', 'ALTO'], ['MEDIO', 'MEDIO'], ['BAJO', 'BAJO'], ['MUY_BAJO', 'MUY_BAJO'], ['CERO', 'CERO']])),
            ],
            options={
                'db_table': 'categoria',
            },
        ),
        migrations.CreateModel(
            name='GolosinaModel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('nombre', models.TextField()),
                ('fecha_vencimiento', models.DateField(editable=False)),
                ('precio', models.FloatField()),
                ('procedencia', models.TextField(choices=[['NACIONAL', 'NACIONAL'], ['IMPORTADO', 'IMPORTADO']], default='NACIONAL')),
                ('categoria', models.ForeignKey(db_column='categoria_id', on_delete=django.db.models.deletion.PROTECT, related_name='golosinas', to='gestion.categoriamodel')),
            ],
            options={
                'db_table': 'golosinas',
                'unique_together': {('nombre', 'fecha_vencimiento')},
            },
        ),
    ]
