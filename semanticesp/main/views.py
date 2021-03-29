import requests
from django.shortcuts import render, redirect
from main.defs import *
from main.models import *
from datetime import datetime, timedelta
from pytz import timezone, utc
from openpyxl import load_workbook   # for xls? formats
import xlrd  # for xls formats
from django.contrib import messages


def index(request):
    sites = SourceData.objects.all()
    context = {
        'sites': sites,
    }

    return render(request, 'index.html', context)


def populate_child(request, codigo):
    try:
        source_data = SourceData.objects.get(codigo=codigo)
    except:
        source_data = None
    if source_data:
        print('gattering... código: {}'.format(codigo))
        try:
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
                        InstituicoesdoEnsinoSuperior.objects.update_or_create(
                            PartitionKey = partition_key,
                            RowKey = row_key,
                            source_data = source_data.codigo,
                            defaults = defaults
                        )
                    source_data.data_ultima_atualizacao = datetime.now(tz=utc)
                    source_data.populated = True
                    source_data.save()
                elif codigo == 'ClassNacionaldeareasdeeducacaoeformacao':
                    for defaults in (res.json()['d']):
                        partition_key = defaults['PartitionKey']
                        row_key = defaults['RowKey']
                        defaults.pop('PartitionKey')
                        defaults.pop('RowKey')
                        ClassNacionaldeareasdeeducacaoeformacao.objects.update_or_create(
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
                    count = 0
                    valor_acumulado = 0
                    for line in lines:
                        if 'valor' in line.keys(): # pega somente se tiver algum valor (exclui informações confienciais)
                            vol_neg_empresa_regiao = VolNegEmpresaRegiao.objects.update_or_create(
                                geocod = line['geocod'],
                                defaults = {
                                    'geodsg': line['geodsg']
                                }
                            )
                            vol_neg_empresa_cae = VolNegEmpresaCae.objects.update_or_create(
                                dim_3 = line['dim_3'],
                                defaults = {
                                    'dim_3_t': line['dim_3_t']
                                }
                            )
                            vol_neg_empresa_dados = VolNegEmpresaDados.objects.update_or_create(
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
                    source_data.data_ultima_atualizacao = datetime.now(tz=utc)
                    source_data.populated = True
                    source_data.save()
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

            elif (res) and (source_data.tipo == 'xls?'):
                file = open('tmp_excel_work.xlsx', 'wb')
                file.write(res.content)
                # file.close()
                # file = open('tmp_excel_work.xlsx', 'r')

                wb = load_workbook(file, False, False, False, False)
                sheet = wb.worksheets[0]  # aba da planilha

                max_col = sheet.max_column + 1
                max_row = sheet.max_row + 1

                for lin in range(13, max_col):
                    celula1 = sheet.cell(row=lin, column=1)
                    celula2 = sheet.cell(row=lin, column=2)
                    print(celula1,celula2)
                wb.close()
            messages.success(request, 'Processamento do Arquivo: "{}" efetuado com sucesso.'.format(codigo))
        except Exception as error:
            raise
            messages.error(request, 'Ocorreu um erro ao processar o arquivo {}. Operação não efetuada.'.format(codigo))
            messages.info(request, 'Erro: {}'.format(error))

    return redirect('/index')



