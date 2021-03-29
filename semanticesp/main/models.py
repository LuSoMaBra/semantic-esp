from django.db import models

class SourceData(models.Model):
    nome = models.CharField(max_length=150, blank=True, null=True)
    uri = models.CharField(max_length=255, blank=True, null=True)
    codigo = models.CharField(unique=True, max_length=255, blank=True, null=True, )
    data_ultimo_acesso = models.DateTimeField(blank=True, null=True)
    tipo = models.CharField(max_length=20, blank=True, null=True)
    populated = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'source_data'

class InstituicoesdoEnsinoSuperior(models.Model):
    source_data = models.CharField(max_length=255, blank=True, null=True)
    PartitionKey = models.CharField(max_length=255, blank=True, null=True)
    RowKey = models.CharField(max_length=255, blank=False, null=False, primary_key=True)
    Timestamp = models.DateTimeField(blank=True, null=True)
    entityid = models.CharField(max_length=255, blank=True, null=True)
    codigodoestabelecimento = models.CharField(max_length=255, blank=True, null=True)
    nomedoestabelecimento = models.CharField(max_length=255, blank=True, null=True)
    morada = models.CharField(max_length=255, blank=True, null=True)
    codigopostal = models.CharField(max_length=255, blank=True, null=True)
    distrito = models.CharField(max_length=255, blank=True, null=True)
    concelho = models.CharField(max_length=255, blank=True, null=True)
    tipodeensino = models.CharField(max_length=255, blank=True, null=True)
    paginaweb = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    telefone = models.CharField(max_length=255, blank=True, null=True)
    fax = models.CharField(max_length=255, blank=True, null=True)
    codigodependede = models.CharField(max_length=255, blank=True, null=True)
    dependede = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'instituicoes_do_ensino_superior'
        unique_together = ('source_data', 'PartitionKey', 'RowKey')


class ClassNacionaldeareasdeeducacaoeformacao(models.Model):
    source_data = models.CharField(max_length=255, blank=True, null=True)
    PartitionKey = models.CharField(max_length=255, blank=True, null=True)
    RowKey = models.CharField(max_length=255, blank=False, null=False, primary_key=True)
    Timestamp = models.DateTimeField(blank=True, null=True)
    entityid = models.CharField(max_length=255, blank=True, null=True)
    subsistema = models.CharField(max_length=255, blank=True, null=True)
    tipodeensino = models.CharField(max_length=255, blank=True, null=True)
    distrito = models.CharField(max_length=255, blank=True, null=True)
    estabelecimento = models.CharField(max_length=255, blank=True, null=True)
    curso = models.CharField(max_length=255, blank=True, null=True)
    niveldeformacao = models.CharField(max_length=255, blank=True, null=True)
    areacnaef = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'class_nacional_de_areas_de_educacao_e_formacao'
        unique_together = ('source_data', 'PartitionKey', 'RowKey')


class VolNegEmpresaDados(models.Model):
    geocod = models.OneToOneField('VolNegEmpresaRegiao', models.CASCADE, db_column='geocod', primary_key=True)
    dim_3 = models.ForeignKey('VolNegEmpresaCae', models.CASCADE, db_column='dim_3')
    valor = models.BigIntegerField(blank=True, null=True)
    ultimo_pref = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'vol_neg_empresa_dados'
        unique_together = (('geocod', 'dim_3', 'ultimo_pref'),)


class VolNegEmpresaRegiao(models.Model):
    geocod = models.CharField(primary_key=True, max_length=10)
    geodsg = models.CharField(max_length=150, blank=True, null=True)
    total_ultimo_pref = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'vol_neg_empresa_regiao'


class VolNegEmpresaCae(models.Model):
    dim_3 = models.CharField(primary_key=True, max_length=10)
    dim_3_t = models.CharField(max_length=255, blank=True, null=True)
    total_ultimo_pref = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'vol_neg_empresa_cae'

