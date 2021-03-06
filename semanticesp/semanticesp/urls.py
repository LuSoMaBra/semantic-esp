"""semantic URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from main import views

from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/index/')),
    path('index/', views.index),
    path('populate_child/<int:id>', views.populate_child),
    path('visualiza_ontologia/', views.visualiza_ontologia),
    path('sparql_ontologia/', views.sparql_ontologia),
    path('run_sparql_ontologia/', views.run_sparql_ontologia),
    path('serializa_ontologia/', views.serializa_ontologia),
    path('importa_dados/', views.importa_dados),
    path('raspagem_curso', views.raspagem_curso),
    path('raspagem_job', views.raspagem_job),
]
