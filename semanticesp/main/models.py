from django.db import models

class ProvenanceStatement(models.Model):
    title = models.CharField(max_length=150, blank=True, null=True)
    url = models.CharField(max_length=255, blank=True, null=True)
    creator = models.CharField(unique=True, max_length=255, blank=True, null=True, )
    codigo = models.CharField(unique=True, max_length=255, blank=True, null=True, )
    last_extraction = models.DateTimeField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    source = models.CharField(max_length=20, blank=True, null=True)
    populated = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'provenance_statement'

class CollegeOrUniversity(models.Model):
    provenance_statement = models.ForeignKey(ProvenanceStatement, models.CASCADE, blank=True, null=True)
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
    link_open_data = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'college_or_university'
        unique_together = ('codigodoestabelecimento')
        unique_together = ('provenance_statement', 'PartitionKey', 'RowKey')



class CursoCnaef(models.Model):
    provenance_statement = models.ForeignKey(ProvenanceStatement, models.CASCADE, blank=True, null=True)
    PartitionKey = models.CharField(max_length=255, blank=True, null=True)
    RowKey = models.CharField(max_length=255, blank=False, null=False, primary_key=True)
    Timestamp = models.DateTimeField(blank=True, null=True)
    entityid = models.CharField(max_length=255, blank=True, null=True)
    subsistema = models.CharField(max_length=255, blank=True, null=True)
    tipodeensino = models.CharField(max_length=255, blank=True, null=True)
    distrito = models.CharField(max_length=255, blank=True, null=True)
    estabelecimento = models.CharField(max_length=255, blank=True, null=True)
    nome = models.CharField(max_length=255, blank=True, null=True)
    niveldeformacao = models.CharField(max_length=255, blank=True, null=True)
    areacnaef = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'curso_cnaef'


class Trabalho(models.Model):
    provenance_statement = models.ForeignKey(ProvenanceStatement, models.CASCADE, blank=True, null=True)
    titulo = models.CharField(max_length=250, blank=True, null=True)
    descricao = models.CharField(max_length=4096, blank=True, null=True)
    requisitos = models.CharField(max_length=255, blank=False, null=False)
    remuneracao = models.CharField(max_length=255, blank=False, null=False)
    localizacao = models.CharField(max_length=255, blank=False, null=False)
    modo = models.CharField(max_length=255, blank=False, null=False)
    area_curso = models.CharField(max_length=255, blank=False, null=False)

    class Meta:
        managed = False
        db_table = 'trabalho'


class Curso(models.Model):
    provenance_statement = models.ForeignKey(ProvenanceStatement, models.CASCADE, blank=True, null=True)
    curso_cnaef = models.ForeignKey(CursoCnaef, models.CASCADE, blank=True, null=True)
    url = models.CharField(max_length=255, blank=False, null=False)
    descricao = models.CharField(max_length=2048, blank=True, null=True)
    valor_propina_nacional = models.CharField(max_length=255, blank=False, null=False)
    valor_propina_internacional = models.CharField(max_length=255, blank=False, null=False)
    duracao = models.CharField(max_length=255, blank=False, null=False)
    modo = models.CharField(max_length=255, blank=False, null=False)

    class Meta:
        managed = False
        db_table = 'curso'
