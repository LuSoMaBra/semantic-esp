import requests
from django.shortcuts import render, redirect
from main.defs import *
from main.models import *
from datetime import datetime, timedelta
from pytz import timezone, utc

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
        res = requests.get(source_data.uri)
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
            else:
                pass

    return redirect('/index')

