# Generated by Django 3.1.7 on 2021-03-26 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ClassNacionaldeareasdeeducacaoeformacao',
            fields=[
                ('PartitionKey', models.CharField(blank=True, max_length=255, null=True)),
                ('RowKey', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('Timestamp', models.DateTimeField(blank=True, null=True)),
                ('entityid', models.CharField(blank=True, max_length=255, null=True)),
                ('subsistema', models.CharField(blank=True, max_length=255, null=True)),
                ('tipodeensino', models.CharField(blank=True, max_length=255, null=True)),
                ('distrito', models.CharField(blank=True, max_length=255, null=True)),
                ('estabelecimento', models.CharField(blank=True, max_length=255, null=True)),
                ('curso', models.CharField(blank=True, max_length=255, null=True)),
                ('niveldeformacao', models.CharField(blank=True, max_length=255, null=True)),
                ('areacnaef', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'class_nacional_de_areas_de_educacao_e_formacao',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='InstituicoesdoEnsinoSuperior',
            fields=[
                ('PartitionKey', models.CharField(blank=True, max_length=255, null=True)),
                ('RowKey', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('Timestamp', models.DateTimeField(blank=True, null=True)),
                ('entityid', models.CharField(blank=True, max_length=255, null=True)),
                ('codigodoestabelecimento', models.CharField(blank=True, max_length=255, null=True)),
                ('nomedoestabelecimento', models.CharField(blank=True, max_length=255, null=True)),
                ('morada', models.CharField(blank=True, max_length=255, null=True)),
                ('codigopostal', models.CharField(blank=True, max_length=255, null=True)),
                ('distrito', models.CharField(blank=True, max_length=255, null=True)),
                ('concelho', models.CharField(blank=True, max_length=255, null=True)),
                ('tipodeensino', models.CharField(blank=True, max_length=255, null=True)),
                ('paginaweb', models.CharField(blank=True, max_length=255, null=True)),
                ('email', models.CharField(blank=True, max_length=255, null=True)),
                ('telefone', models.CharField(blank=True, max_length=255, null=True)),
                ('fax', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'instituicoes_do_ensino_superior',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SourceData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(blank=True, max_length=150, null=True)),
                ('uri', models.CharField(blank=True, max_length=255, null=True)),
                ('codigo', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('data_ultimo_acesso', models.DateTimeField(blank=True, null=True)),
                ('tipo', models.CharField(blank=True, max_length=20, null=True)),
                ('populated', models.BooleanField(blank=True, null=True)),
            ],
            options={
                'db_table': 'source_data',
                'managed': False,
            },
        ),
    ]
