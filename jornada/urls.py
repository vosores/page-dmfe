# jornada/urls.py
from django.urls import path
from . import views


urlpatterns = [
    path('editar/', views.editar_academico, name='editar_academico'),
]

