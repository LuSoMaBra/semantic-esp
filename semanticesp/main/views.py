import requests
import os
from django.shortcuts import render, redirect
from main.defs import *
from main.models import *
from datetime import datetime, timedelta
from pytz import timezone, utc
from openpyxl import load_workbook   # for xls? formats
import xlrd  # for xls formats
from django.contrib import messages
import rdflib
from rdflib import Namespace, URIRef, Literal
from rdflib.namespace import RDF, RDFS, OWL, FOAF

from urllib.request import urlopen

def index(request):
    sites = SourceData.objects.all().order_by('codigo')
    context = {
        'sites': sites,
    }

    return render(request, 'index.html', context)

def raspagem_curso(request):

    os.system('scrapy runspider scrapies_esp/scrapy_curso.py')

    return redirect('/index')

def raspagem_job(request):

    os.system('scrapy runspider scrapies_esp/scrapy_job_net_empregos.py')

    return redirect('/index')

def visualiza_ontologia(request):
    return render(request, 'visualiza_ontologia.html')

def serializa_ontologia(request):

    myOntology = Namespace('https://github.com/LuSoMaBra/semantic-esp/tree/master/semanticesp/ontology#')

    equivalencia_curso = {'NomeCurso': 'nome',
                          'RequisitosEntradaInstituicao': 'instituicao__requisitos_entrada',
                          'QualificacaoCurso': 'qualificacao',
                          'ValorInternacionalCurso': 'valor_anual_internacional',
                          'NomeInstituicao': 'instituicao__nome',
                          'DescricaoCurso':'descricao',
                          'AreaCurso': 'area',
                          'ModoCurso': 'modo',
                          'UrlCurso': 'url',
                          'CampoEstudoCurso': 'campo_estudo',
                          'LocalizacaoInstituicao': 'instituicao__localizacao',
                          'DuracaoCurso': 'duracao',
                          'ValorNacionalCurso': 'valor_anual_nacional',
                          }

    equivalencia_job = {'LocalizacaoTrabalho': 'localizacao',
                        'DescricaoTrabalho': 'descricao',
                        'TituloTrabalho': 'titulo',
                        'RequisitosTrabalho': 'requisitos',
                        'RemuneracaoTrabalho': 'remuneracao',
                        'ModoTrabalho': 'modo'
                        }

    # CURSO
    g = rdflib.Graph()
    ontologia = g.parse('ontology/Ontologia_Curso.rdf')
    g.bind('myOntology', myOntology)
    perfil_curso = PerfilCurso.objects.all()
    last_data_raspagem = perfil_curso.distinct('data_raspagem').order_by('-data_raspagem').first().data_raspagem
    if last_data_raspagem:
        perfil_curso = perfil_curso.filter(data_raspagem=last_data_raspagem)

    for x in perfil_curso:        
        g.add((myOntology['NomeCurso'], OWL.NamedIndividual, Literal(x.nome)))
        g.add((myOntology['RequisitosEntradaInstituicao'], OWL.NamedIndividual, Literal(x.instituicao.requisitos_entrada)))
        g.add((myOntology['QualificacaoCurso'], OWL.NamedIndividual, Literal(x.qualificacao)))
        g.add((myOntology['ValorInternacionalCurso'], OWL.NamedIndividual, Literal(x.valor_anual_internacional)))
        g.add((myOntology['NomeInstituicao'], OWL.NamedIndividual, Literal(x.instituicao.nome)))
        g.add((myOntology['DescricaoCurso'], OWL.NamedIndividual, Literal(x.descricao)))
        g.add((myOntology['AreaCurso'], OWL.NamedIndividual, Literal(x.area)))
        g.add((myOntology['ModoCurso'], OWL.NamedIndividual, Literal(x.modo)))
        g.add((myOntology['UrlCurso'], OWL.NamedIndividual, Literal(x.url)))
        g.add((myOntology['CampoEstudoCurso'], OWL.NamedIndividual, Literal(x.campo_estudo)))
        g.add((myOntology['LocalizacaoInstituicao'], OWL.NamedIndividual, Literal(x.instituicao.localizacao)))
        g.add((myOntology['DuracaoCurso'], OWL.NamedIndividual, Literal(x.duracao)))
        g.add((myOntology['ValorNacionalCurso'], OWL.NamedIndividual, Literal(x.valor_anual_nacional)))

    # perfil_curso = list(g.triples((myOntology['NomeCurso'], OWL.NamedIndividual, None)))
    # for (sub, pred, obj) in perfil_curso:
    #     print((sub, pred, obj))

    # s = g.serialize(format='turtle').decode('utf-8')
    # print('============================== Ontologia Curso ========================================')
    # print(s)

    curso_serializado = {}
    curso_serializado['n3'] = g.serialize(format='n3').decode('utf-8')
    curso_serializado['nt'] = g.serialize(format='nt').decode('utf-8')
    curso_serializado['prettyxml'] = g.serialize(format='pretty-xml').decode('utf-8')
    curso_serializado['trig'] = g.serialize(format='trig').decode('utf-8')
    curso_serializado['turtle'] = g.serialize(format='turtle').decode('utf-8')
    curso_serializado['xml'] = g.serialize(format='xml').decode('utf-8')

    # JOB
    gc = rdflib.Graph()
    ontologia = gc.parse('ontology/Ontologia_Trabalho.rdf')

    gc.bind('myOntology', myOntology)

    perfil_job = PerfilTrabalho.objects.all()
    last_data_raspagem = perfil_job.distinct('data_raspagem').order_by('-data_raspagem').first().data_raspagem
    if last_data_raspagem:
        perfil_job = perfil_job.filter(data_raspagem=last_data_raspagem)

    for x in perfil_job:
        gc.add((myOntology['LocalizacaoTrabalho'], OWL.NamedIndividual, Literal(x.localizacao)))
        gc.add((myOntology['DescricaoTrabalho'], OWL.NamedIndividual, Literal(x.descricao)))
        gc.add((myOntology['TituloTrabalho'], OWL.NamedIndividual, Literal(x.titulo)))
        gc.add((myOntology['RequisitosTrabalho'], OWL.NamedIndividual, Literal(x.requisitos)))
        gc.add((myOntology['RemuneracaoTrabalho'], OWL.NamedIndividual, Literal(x.remuneracao)))
        gc.add((myOntology['ModoTrabalho'], OWL.NamedIndividual, Literal(x.modo)))

    # perfil_job = list(gc.triples((myOntology['NomeCurso'], OWL.NamedIndividual, None)))
    # for (sub, pred, obj) in perfil_job:
    #     print((sub, pred, obj))

    job_serializado = {}
    job_serializado['n3'] = gc.serialize(format='n3').decode('utf-8')
    job_serializado['nt'] = gc.serialize(format='nt').decode('utf-8')
    job_serializado['prettyxml'] = gc.serialize(format='pretty-xml').decode('utf-8')
    job_serializado['trig'] = gc.serialize(format='trig').decode('utf-8')
    job_serializado['turtle'] = gc.serialize(format='turtle').decode('utf-8')
    job_serializado['xml'] = gc.serialize(format='xml').decode('utf-8')

    context = {
        'job_serializado': job_serializado,
        'curso_serializado': curso_serializado,
    }

    return render(request, 'serializa_ontologia.html', context)



def populate_child(request, codigo):
    try:
        source_data = SourceData.objects.get(codigo=codigo)
    except:
        source_data = None
    if source_data:
        populated = False
        try:
            # if source_data.tipo == 'pdf':
            #     res = urlopen(source_data.uri)
            # else:
            res = requests.get(source_data.uri)
        except Exception as error:
            res = None
            messages.error(request, 'Ocorreu um erro ao efetuar a requisiçao do arquivo {}. Operação não efetuada.'.format(codigo))
            messages.info(request, 'Erro: {}'.format(error))
        try:
            if (res) and (source_data.tipo == 'json'):
                if codigo == 'InstituicoesdoEnsinoSuperior':
                    for defaults in (res.json()['d']):
                        partition_key = defaults['PartitionKey']
                        row_key = defaults['RowKey']
                        defaults.pop('PartitionKey')
                        defaults.pop('RowKey')
                        populated, c = InstituicoesdoEnsinoSuperior.objects.update_or_create(
                            PartitionKey = partition_key,
                            RowKey = row_key,
                            source_data = source_data.codigo,
                            defaults = defaults
                        )
                elif codigo == 'ClassNacionaldeareasdeeducacaoeformacao':
                    for defaults in (res.json()['d']):
                        partition_key = defaults['PartitionKey']
                        row_key = defaults['RowKey']
                        defaults.pop('PartitionKey')
                        defaults.pop('RowKey')
                        populated, c = ClassNacionaldeareasdeeducacaoeformacao.objects.update_or_create(
                            PartitionKey = partition_key,
                            RowKey = row_key,
                            source_data = source_data.codigo,
                            defaults = defaults
                        )
                    source_data.data_ultima_atualizacao = datetime.now(tz=utc)
                    source_data.populated = True
                    source_data.save()
                elif codigo == 'VolNegEmpresas':
                    ultimo_pref = res.json()[0]['UltimoPref']
                    lines = res.json()[0]['Dados'][ultimo_pref]
                    for line in lines:
                        if 'valor' in line.keys(): # pega somente se tiver algum valor (exclui informações confienciais)
                            vol_neg_empresa_regiao, c = VolNegEmpresaRegiao.objects.update_or_create(
                                geocod = line['geocod'],
                                defaults = {
                                    'geodsg': line['geodsg']
                                }
                            )
                            if line['dim_3'].isnumeric():
                                vol_neg_empresa_cae, c = VolNegEmpresaCae.objects.update_or_create(
                                    dim_3 = line['dim_3'],
                                    defaults = {
                                        'dim_3_t': line['dim_3_t']
                                    }
                                )
                                vol_neg_empresa_dados, c = VolNegEmpresaDados.objects.update_or_create(
                                    geocod = vol_neg_empresa_regiao,
                                    dim_3 = vol_neg_empresa_cae,
                                    ultimo_pref = ultimo_pref,
                                    defaults = {
                                        'valor': line['valor']
                                    }
                                )
                    vol_neg_empresa_regiao = VolNegEmpresaRegiao.objects.all()
                    for x in vol_neg_empresa_regiao:
                        vol_neg_empresa_dados = VolNegEmpresaDados.objects.filter(geocod=x)
                        total_valor = 0
                        for y in vol_neg_empresa_dados:
                            total_valor += y.valor
                        x.total_ultimo_pref = total_valor
                        x.save()
                    vol_neg_empresa_regiao = VolNegEmpresaCae.objects.all()
                    for x in vol_neg_empresa_regiao:
                        vol_neg_empresa_dados = VolNegEmpresaDados.objects.filter(dim_3=x)
                        total_valor = 0
                        for y in vol_neg_empresa_dados:
                            total_valor += y.valor
                        x.total_ultimo_pref = total_valor
                        x.save()
                    populated = vol_neg_empresa_regiao
                else:
                    pass
            elif (res) and (source_data.tipo == 'xls'):

                file = open('tmp_excel_work.xls', 'wb')
                file.write(res.content)
                file.close()

                book = xlrd.open_workbook(file.name)
                print("The number of worksheets is {0}".format(book.nsheets))
                print("Worksheet name(s): {0}".format(book.sheet_names()))
                sheet = book.sheet_by_index(0)
                print("{0} {1} {2}".format(sheet.name, sheet.nrows, sheet.ncols))
                print("Cell A2 is {0}".format(sheet.cell_value(rowx=1, colx=0)))
                for rx in range(sheet.nrows):
                    print(sheet.cell_value(rx,0), sheet.cell_value(rx,1))
                    # print(sheet.row(rx)[0])
                os.remove(file.name)

            elif (res) and (source_data.tipo == 'xls?'):
                file = open('tmp_excel_work.xlsx', 'wb')
                file.write(res.content)

                wb = load_workbook(file, False, False, False, False)
                sheet = wb.worksheets[0]  # aba da planilha

                max_col = sheet.max_column + 1
                max_row = sheet.max_row + 1

                for lin in range(13, max_col):
                    celula1 = sheet.cell(row=lin, column=1)
                    celula2 = sheet.cell(row=lin, column=2)
                    print(celula1,celula2)
                wb.close()
                os.remove(file.name)

            elif (res) and (source_data.tipo == 'pdf'):

                file = open('tmp_pdf_work.pdf', 'wb')
                file.write(res.content)
                file.close()
                # stringSaida = lerPDF(file)
                stringSaida = getPDFContent(file.name)
                txt = stringSaida.split('\n')
                print(txt[222])
                # for x in stringSaida.split('\n'):
                #     print(x)
                # os.remove(file.name)
            else:
                pass
            if populated:   # deve atualizar essa variável para atualização do source_data
                source_data.data_ultimo_acesso = datetime.now(tz=utc)
                source_data.populated = True
                source_data.save()
            messages.success(request, 'Processamento do Arquivo: "{}" efetuado com sucesso.'.format(codigo))
        except Exception as error:
            raise
            messages.error(request, 'Ocorreu um erro ao processar o arquivo {}. Operação não efetuada.'.format(codigo))
            messages.info(request, 'Erro: {}'.format(error))

    return redirect('/index')



