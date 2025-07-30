from .models import Escuela, Departamento
from .models import ProgramaPostgrado

def escuelas_disponibles(request):
    return {'escuelas': Escuela.objects.all()}

from jornada.models import ProgramaPostgrado, Departamento

def programas_context(request):
    context = {
        'programas': ProgramaPostgrado.objects.all()
    }

    try:
        dpto = Departamento.objects.get(slug="dmfe")
        context['postgrados'] = ProgramaPostgrado.objects.filter(departamento=dpto)
    except Departamento.DoesNotExist:
        context['postgrados'] = []

    return context



def escuelas_dmfe(request):
    try:
        dpto = Departamento.objects.get(nombre="Matemática, Física y Estadística")
        escuelas_mate = Escuela.objects.filter(departamento=dpto)
    except Departamento.DoesNotExist:
        escuelas_mate = []
    return {'escuelas_mate': escuelas_mate}

def departamentos_con_academicos(request):
    departamentos = Departamento.objects.prefetch_related('academicos').all()
    return {'departamentos': departamentos}