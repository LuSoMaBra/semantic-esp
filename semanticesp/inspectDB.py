# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class ClassNacionalDeAreasDeEducacaoEFormacao(models.Model):
    rowkey = models.CharField(db_column='RowKey', max_length=255, blank=True, null=True)  # Field name made lowercase.
    timestamp = models.DateTimeField(db_column='Timestamp', blank=True, null=True)  # Field name made lowercase.
    entityid = models.CharField(max_length=255, blank=True, null=True)
    subsistema = models.CharField(max_length=255, blank=True, null=True)
    tipodeensino = models.CharField(max_length=255, blank=True, null=True)
    distrito = models.CharField(max_length=255, blank=True, null=True)
    estabelecimento = models.CharField(max_length=255, blank=True, null=True)
    curso = models.CharField(max_length=255, blank=True, null=True)
    niveldeformacao = models.CharField(max_length=255, blank=True, null=True)
    areacnaef = models.CharField(max_length=255, blank=True, null=True)
    partitionkey = models.CharField(db_column='PartitionKey', max_length=255, blank=True, null=True)  # Field name made lowercase.
    source_data = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'class_nacional_de_areas_de_educacao_e_formacao'
        unique_together = (('rowkey', 'partitionkey', 'source_data'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class InstituicoesDoEnsinoSuperior(models.Model):
    rowkey = models.CharField(db_column='RowKey', max_length=255, blank=True, null=True)  # Field name made lowercase.
    timestamp = models.DateTimeField(db_column='Timestamp', blank=True, null=True)  # Field name made lowercase.
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
    partitionkey = models.CharField(db_column='PartitionKey', max_length=255, blank=True, null=True)  # Field name made lowercase.
    source_data = models.CharField(max_length=255, blank=True, null=True)
    codigodependede = models.CharField(max_length=255, blank=True, null=True)
    dependede = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'instituicoes_do_ensino_superior'
        unique_together = (('rowkey', 'partitionkey', 'source_data'),)


class SourceData(models.Model):
    nome = models.CharField(max_length=150, blank=True, null=True)
    uri = models.CharField(max_length=255, blank=True, null=True)
    data_ultimo_acesso = models.DateTimeField(blank=True, null=True)
    tipo = models.CharField(max_length=20, blank=True, null=True)
    codigo = models.CharField(unique=True, max_length=255, blank=True, null=True)
    populated = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'source_data'


class VolNegEmpresaDados(models.Model):
    geocod = models.OneToOneField('VolNegEmpresaRegiao', models.DO_NOTHING, db_column='geocod', primary_key=True)
    dim_3 = models.ForeignKey('VolNegRegiaoCae', models.DO_NOTHING, db_column='dim_3')
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


class VolNegRegiaoCae(models.Model):
    dim_3 = models.CharField(primary_key=True, max_length=10)
    dim3_t = models.CharField(max_length=255, blank=True, null=True)
    total_ultimo_pref = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'vol_neg_regiao_cae'
