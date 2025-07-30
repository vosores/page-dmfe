from django.core.management.base import BaseCommand
from jornada.models import Escuela, ProgramaPostgrado

class Command(BaseCommand):
    help = 'Agrega escuelas y programas de postgrado predeterminados'

    def handle(self, *args, **kwargs):
        escuelas = [
            "Ingeniería Matemática", "Geología", "Ingeniería en Estadística",
            "Pedagogía en Matemática y Computación", "Pedagogía en Ciencias"
        ]
        programas = [
            "Doctorado en Didáctica de las Ciencias Experimentales",
            "Doctorado en Modelamiento Matemático Aplicado",
            "Doctorado en Didáctica de la Matemática",
            "Magíster en Didáctica de la Matemática",
            "Magíster en Didáctica de las Ciencias Experimentales",
            "Magíster en Data Science"
        ]

        for nombre in escuelas:
            obj, creado = Escuela.objects.get_or_create(nombre=nombre)
            if creado:
                self.stdout.write(self.style.SUCCESS(f'Escuela creada: {nombre}'))
            else:
                self.stdout.write(self.style.WARNING(f'Escuela ya existe: {nombre}'))

        for nombre in programas:
            obj, creado = ProgramaPostgrado.objects.get_or_create(nombre=nombre)
            if creado:
                self.stdout.write(self.style.SUCCESS(f'Programa creado: {nombre}'))
            else:
                self.stdout.write(self.style.WARNING(f'Programa ya existe: {nombre}'))

        self.stdout.write(self.style.SUCCESS("Carga completa de escuelas y programas."))
