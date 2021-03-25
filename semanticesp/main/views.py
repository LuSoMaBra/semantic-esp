from django.shortcuts import render

from main.defs import *

from main.models import *

def index(request):

    # sites = get_sites_to_recover()

    sites = SourceData.objects.all()

    context = {
        'sites': sites,
    }

    return render(request, 'index.html', context)




