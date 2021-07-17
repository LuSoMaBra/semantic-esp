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
    return render(request, 'index.html')

def importa_dados(request):
    sites = ProvenanceStatement.objects.all().order_by('id')
    context = {
        'sites': sites,
    }

    return render(request, 'importa_dados.html', context)

def raspagem_curso(request):

    os.system('scrapy runspider scrapies_esp/scrapy_curso.py')

    return redirect('/index')

def raspagem_job(request):

    os.system('scrapy runspider scrapies_esp/scrapy_job_net_empregos.py')

    return redirect('/index')

def visualiza_ontologia(request):
    return render(request, 'visualiza_ontologia.html')

def sparql_ontologia(request):

    context = {
        'sparql_query': '',
        'sparql_resultado': 'Sem resultados para mostrar.',
    }

    return render(request, 'sparql_ontologia.html', context)

def serializa_ontologia(request):
    try:
        g, gc = processa_ontologia()

        curso_serializado = {}
        curso_serializado['n3'] = g.serialize(format='n3').decode('utf-8')
        curso_serializado['nt'] = g.serialize(format='nt').decode('utf-8')
        curso_serializado['prettyxml'] = g.serialize(format='pretty-xml').decode('utf-8')
        curso_serializado['trig'] = g.serialize(format='trig').decode('utf-8')
        curso_serializado['turtle'] = g.serialize(format='turtle').decode('utf-8')
        curso_serializado['xml'] = g.serialize(format='xml').decode('utf-8')

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

        messages.success(request, 'Serialização da ontologia executada com sucesso.'.format(codigo))

    except Exception as error:
        messages.error(request, 'Ocorreu um erro ao serializar a ontologia. Operação não efetuada.')

    return render(request, 'serializa_ontologia.html', context)

def run_sparql_ontologia(request):
    try:
        g, gc = processa_ontologia()
        sparql_query = str(request.POST.get('sparql_text', '').strip())
        run_on = request.POST.get('run_on', '')

        try:
            if run_on == 'curso':
                resultado = g.query(sparql_query)
            elif run_on == 'job':
                resultado = gc.query(sparql_query)
            else:
                resultado = None
        except:
            resultado = None

        sparql_resultado = []
        if resultado:
            for x in resultado:
                sparql_resultado.append(str(x) + '\n')

        if not sparql_resultado:
            sparql_resultado = ['Ocorreu um erro ao executar a query. \n\nSem resultados para mostrar.']
            messages.error(request, 'Ocorreu um erro ao executar a query. Operação não efetuada.')

        context = {
            'sparql_query': sparql_query,
            'sparql_resultado': sparql_resultado,
        }

        messages.success(request, 'Query executada com sucesso.'.format(codigo))

    except Exception as error:
        messages.error(request, 'Ocorreu um erro ao executar a query. Operação não efetuada.')

    return render(request, 'sparql_ontologia.html', context)


def processa_ontologia():

    myOntology = Namespace('https://github.com/LuSoMaBra/semantic-esp/tree/master/semanticesp/ontology#')

    equivalencia_curso = {'NomeCurso': 'nome',
                          'RequisitosEntradaInstituicao': 'instituicao__requisitos_entrada',
                          'QualificacaoCurso': 'qualificacao',
                          'ValorInternacionalCurso': 'valor_anual_internacional',
                          'NomeInstituicao': 'instituicao__nome',
                          'DescricaoCurso':'descricao',
                          'AreaCurso': 'area_curso',
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
        g.add((myOntology['AreaCurso'], OWL.NamedIndividual, Literal(x.area_curso)))
        g.add((myOntology['ModoCurso'], OWL.NamedIndividual, Literal(x.modo)))
        g.add((myOntology['UrlCurso'], OWL.NamedIndividual, Literal(x.url)))
        g.add((myOntology['CampoEstudoCurso'], OWL.NamedIndividual, Literal(x.campo_estudo)))
        g.add((myOntology['LocalizacaoInstituicao'], OWL.NamedIndividual, Literal(x.instituicao.localizacao)))
        g.add((myOntology['DuracaoCurso'], OWL.NamedIndividual, Literal(x.duracao)))
        g.add((myOntology['ValorNacionalCurso'], OWL.NamedIndividual, Literal(x.valor_anual_nacional)))

    # perfil_curso = list(g.triples((myOntology['NomeCurso'], OWL.NamedIndividual, None)))
    # for (sub, pred, obj) in perfil_curso:
    #     print((sub, pred, obj))

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

    return g, gc


def populate_child(request, id):
    try:
        provenance_statement = ProvenanceStatement.objects.get(id=id)
    except:
        provenance_statement = None
    if provenance_statement:
        populated = False
        try:
            # if provenance_statement.source == 'pdf':
            #     res = urlopen(provenance_statement.url)
            # else:
            res = requests.get(provenance_statement.url)
        except Exception as error:
            res = None
            messages.error(request, 'Ocorreu um erro ao efetuar a requisiçao do arquivo {}. Operação não efetuada.'.format(codigo))
            messages.info(request, 'Erro: {}'.format(error))
        try:
            if (res) and (provenance_statement.source == 'json'):
                if provenance_statement.codigo == 'InstituicoesdoEnsinoSuperior':
                    for defaults in (res.json()['d']):
                        partition_key = defaults['PartitionKey']
                        row_key = defaults['RowKey']
                        defaults.pop('PartitionKey')
                        defaults.pop('RowKey')
                        defaults['Timestamp'] = (defaults['Timestamp'].split('T')[0] + ' ' + defaults['Timestamp'].split('T')[1].split('.')[0])
                        modified = datetime.strptime(defaults['Timestamp'], '%Y-%m-%d %H:%M:%S')
                        codigodoestabelecimento = '{:0>4}'.format(defaults['codigodoestabelecimento'])
                        defaults.pop('codigodoestabelecimento')
                        populated, c = CollegeOrUniversity.objects.update_or_create(
                            PartitionKey = partition_key,
                            RowKey = row_key,
                            provenance_statement = provenance_statement,
                            codigodoestabelecimento = codigodoestabelecimento,
                            defaults = defaults
                        )

                        # FALTA CRIAR A TABELA CURSO
                        # DEPENDE DA RASPAGEM
                        # IMPLEMENTAR CAMPO LINKED_DATA_UNIVERSIDADE


                elif provenance_statement.codigo == 'ClassNacionaldeareasdeeducacaoeformacao':
                    for defaults in (res.json()['d']):
                        partition_key = defaults['PartitionKey']
                        row_key = defaults['RowKey']
                        defaults.pop('PartitionKey')
                        defaults.pop('RowKey')
                        defaults['Timestamp'] = (defaults['Timestamp'].split('T')[0] + ' ' + defaults['Timestamp'].split('T')[1].split('.')[0])
                        modified = datetime.strptime(defaults['Timestamp'], '%Y-%m-%d %H:%M:%S')
                        defaults['estabelecimento'] = defaults['estabelecimento'].split(' - ')[0]
                        populated, c = CursoCnaef.objects.update_or_create(
                            PartitionKey = partition_key,
                            RowKey = row_key,
                            provenance_statement = provenance_statement,
                            defaults = defaults
                        )
                else:
                    pass
            elif (res) and (provenance_statement.source == 'xls'):

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

            elif (res) and (provenance_statement.source == 'xls?'):
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

            elif (res) and (provenance_statement.source == 'pdf'):

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
            if populated:   # deve atualizar essa variável para atualização do provenance_statement
                provenance_statement.creator = 'Portal de dados abertos da Administração Pública (https://dados.gov.pt)'
                provenance_statement.created = modified
                provenance_statement.modified = modified
                provenance_statement.last_extraction = datetime.now(tz=utc)
                provenance_statement.populated = True
                provenance_statement.save()
            messages.success(request, 'Processamento do Arquivo: "{}" efetuado com sucesso.'.format(provenance_statement.codigo))
        except Exception as error:
            messages.error(request, 'Ocorreu um erro ao processar o arquivo {}. Operação não efetuada.'.format(provenance_statement.codigo))
            messages.info(request, 'Erro: {}'.format(error))

    return redirect('/importa_dados')



