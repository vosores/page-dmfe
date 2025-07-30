from django.shortcuts import render
import csv
from django.http import JsonResponse
from .models import ArchivoAcademico, Asignatura
from .forms import ArchivoAcademicoForm, PublicarMaterialForm
from .decorators import solo_academicos


def portada(request):
    return render(request, 'jornada/portada.html')

# def portada_ima(request):
#     return render(request, 'jornada/escuelas/ingenieria-matematica.html')

def resumenes(request):
    return render(request, 'jornada/resumenes.html')

def cursillos(request):
    return render(request, 'jornada/cursillos.html')

def sesiones(request):
    return render(request, 'jornada/sesiones.html')

def plenarias(request):
    return render(request, 'jornada/plenarias.html')

# def representantes_estudiantiles(request):
#     return render(request, 'jornada/representantes_estudiantiles.html')

def ima(request):
    return render(request, 'jornada/ima.html')

from django.contrib.auth.decorators import login_required
@login_required
def material(request):
    asignaturas = Asignatura.objects.prefetch_related('archivos_publicados').all()
    return render(request, 'jornada/material.html', {'asignaturas': asignaturas})


import pandas as pd
import os
from django.conf import settings

from django.utils.safestring import mark_safe

def malla_im(request):
    # Obtener la ruta absoluta del CSV usando settings.py
    archivo_csv = os.path.join(settings.BASE_DIR, 'jornada/static/docs/ac.csv')

    try:
        data = pd.read_csv(archivo_csv)
        # Reemplazar NaN con cadena vacía en todas las columnas
        data = data.fillna("")

        # Verificar si las columnas necesarias existen
        if 'Año' in data.columns and 'Semestre' in data.columns:
            # Obtener todos los años únicos en orden
            años = sorted(data['Año'].unique())

            # Agrupar asignaturas por año y semestre
            malla = {
                año: {
                    semestre: data[(data['Año'] == año) & (data['Semestre'] == semestre)].to_dict(orient='records')
                    for semestre in sorted(data[data['Año'] == año]['Semestre'].unique())
                }
                for año in años
            }

            # Formatear la bibliografía como lista HTML
            for año in malla:
                for semestre in malla[año]:
                    for asignatura in malla[año][semestre]:
                        if 'Bibliografía' in asignatura and isinstance(asignatura['Bibliografía'], str):
                            referencias = asignatura['Bibliografía'].split(";")
                            asignatura['Bibliografía'] = mark_safe("<ul class='text-justify'>" + "".join(f"<li>{ref.strip()}</li>" for ref in referencias) + "</ul>")
                        else:
                            asignatura['Bibliografía'] = mark_safe("<p>No disponible</p>")

        else:
            malla = {}

    except Exception as e:
        print("Error al leer el archivo CSV:", e)
        malla = {}

    return render(request, 'jornada/malla_im.html', {'malla': malla})

from django.template.loader import render_to_string

def generar_malla_ima():
    """Genera la página estática 'malla_ima.html' desde el CSV."""
    
    # 📌 Obtener la ruta absoluta del CSV
    archivo_csv = os.path.join(settings.BASE_DIR, 'jornada/static/docs/ac.csv')

    try:
        data = pd.read_csv(archivo_csv)
        data = data.fillna("")  # Reemplazar NaN con ""

        if 'Año' in data.columns and 'Semestre' in data.columns:
            años = sorted(data['Año'].unique())

            malla = {
                año: {
                    semestre: data[(data['Año'] == año) & (data['Semestre'] == semestre)].to_dict(orient='records')
                    for semestre in sorted(data[data['Año'] == año]['Semestre'].unique())
                }
                for año in años
            }

            # 📌 Formatear bibliografía como lista HTML
            for año in malla:
                for semestre in malla[año]:
                    for asignatura in malla[año][semestre]:
                        asignatura['Requisito'] = asignatura.get('Requisito', "") or "Sin requisito"
                        asignatura['Rec_cod'] = asignatura.get('Rec_cod', "")

                        if 'Bibliografía' in asignatura and isinstance(asignatura['Bibliografía'], str):
                            referencias = asignatura['Bibliografía'].split(";")
                            asignatura['Bibliografía'] = mark_safe(
                                "<ul class='text-justify'>" + "".join(f"<li>{ref.strip()}</li>" for ref in referencias) + "</ul>"
                            )
                        else:
                            asignatura['Bibliografía'] = mark_safe("<p>No disponible</p>")

        else:
            malla = {}

        # 📌 Renderizar la plantilla con los datos procesados
        html_content = render_to_string("jornada/malla_im.html", {'malla': malla})

        # 📌 Guardar el HTML generado en una nueva ruta
        output_path = os.path.join(settings.BASE_DIR, 'jornada/templates/jornada/malla_ima.html')
        with open(output_path, "w", encoding="utf-8") as file:
            file.write(html_content)

        print(f"✅ Archivo generado: {output_path}")

    except Exception as e:
        print(f"❌ Error al generar el HTML estático: {e}")

from django.shortcuts import render, get_object_or_404
from .models import Academico

def lista_academicos(request):
    escuela = Escuela.objects.get(slug="ingenieria-matematica")
    academicos = Academico.objects.filter(escuelas=escuela)
    return render(request, 'jornada/academicos/lista.html', {
        'academicos': academicos,
        'escuela': escuela  # si quieres mostrar el nombre en el template
    })


# def detalle_academico(request, slug):
#     academico = get_object_or_404(Academico, slug=slug)
#     return render(request, 'jornada/academicos/detalle.html', {'academico': academico})

# @login_required  # o sin decorador, según visibilidad
from django.contrib.auth.models import AnonymousUser

def detalle_academico(request, slug):
    academico = get_object_or_404(Academico, slug=slug)
    publicaciones_publicadas = academico.publicaciones.filter(estado='publicada')
    publicaciones_sometidas = academico.publicaciones.filter(estado='sometida')
    publicaciones_en_preparacion = academico.publicaciones.filter(estado='en_preparacion')
    publicaciones_rechazadas = academico.publicaciones.filter(estado='rechazada')
    publicaciones_aceptadas = academico.publicaciones.filter(estado='aceptada')


    avisos = None
    es_director = False

    if request.user.is_authenticated:
        try:
            if request.user.academico.tiene_cargo('Director(a) de Departamento'):
                # avisos = Aviso.objects.all().order_by('-creado') Si quiero que al Director le aparezcan todos los avisos de todos los académicos
                avisos = Aviso.objects.filter(academico=academico).order_by('-creado')
                es_director = True
            else:
                avisos = Aviso.objects.filter(academico=request.user.academico).order_by('-creado')
        except Academico.DoesNotExist:
            avisos = None
    else:
        avisos = None

    embed_path = reverse('perfil_academico_embed', args=[slug])
    absolute_embed_url = request.build_absolute_uri(embed_path)

    return render(request, 'jornada/academicos/detalle.html', {
        'academico': academico,
        'avisos': avisos,
        'es_director': es_director,
        'publicaciones_publicadas': publicaciones_publicadas,
        'publicaciones_sometidas': publicaciones_sometidas,
        'publicaciones_en_preparacion': publicaciones_en_preparacion,
        'publicaciones_rechazadas': publicaciones_rechazadas,
        'publicaciones_aceptadas': publicaciones_aceptadas,
        'absolute_embed_url': absolute_embed_url,
    })


from django.shortcuts import render, get_object_or_404, redirect
from .forms import AcademicoForm
from django.http import HttpResponseForbidden

@login_required
@solo_academicos
def editar_academico(request):
    # Obtiene el objeto Academico relacionado al usuario autenticado
    academico = get_object_or_404(Academico, user=request.user)
    
    if request.method == 'POST':
        form = AcademicoForm(request.POST, request.FILES, instance=academico)
        if form.is_valid():
            form.save()
            return redirect('detalle_academico', slug=academico.slug)
    else:
        form = AcademicoForm(instance=academico)
    
    return render(request, 'jornada/academicos/editar.html', {'form': form, 'academico': academico})

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
# Si creaste tu formulario personalizado, úsalo:
from .forms import CustomAuthForm

def login_view(request):
    # Usar el formulario personalizado
    form = CustomAuthForm(request, data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Redireccionar a la página que el usuario intentaba visitar o a 'portada'
            next_url = request.GET.get('next')
            return redirect(next_url if next_url else 'portada')
        else:
            messages.error(request, "Credenciales inválidas. Intenta nuevamente.")
    return render(request, 'registration/login.html', {'form': form})


# En views.py
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy

class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'registration/password_change.html'
    success_url = reverse_lazy('password_change_hecho')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Suponiendo que tienes una relación OneToOne desde User hacia Academico
        try:
            context['academico'] = self.request.user.academico
        except AttributeError:
            context['academico'] = None
        return context
    
from django.contrib.auth.views import PasswordChangeDoneView

class CustomPasswordChangeDoneView(PasswordChangeDoneView):
    template_name = 'registration/password_change_hecho.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Si el usuario está autenticado y tiene objeto academico, lo agrega al contexto
        if self.request.user.is_authenticated:
            try:
                context['academico'] = self.request.user.academico
            except AttributeError:
                context['academico'] = None
        return context

@login_required
@solo_academicos
def subir_archivo(request):
    """ Permite a un académico subir un archivo o proporcionar un enlace """
    if request.method == 'POST':
        form = ArchivoAcademicoForm(request.POST, request.FILES)
        if form.is_valid():
            archivo = form.save(commit=False)
            archivo.academico = request.user.academico  # Asigna el académico logueado
            
            # Si no se sube un archivo ni se proporciona un enlace, no se permite guardar
            if not archivo.archivo and not archivo.link:
                form.add_error(None, "Debes subir un archivo o proporcionar un enlace.")
            else:
                archivo.save()
                form.save_m2m()  # Guarda etiquetas si existen
                return redirect('material_apuntes')  # Redirige a la página de archivos

    else:
        form = ArchivoAcademicoForm()

    return render(request, 'jornada/subir_archivo.html', {'form': form})


@login_required
@solo_academicos
def material_apuntes(request):
    """ Muestra todos los archivos subidos por los académicos """
    archivos = ArchivoAcademico.objects.all()
    return render(request, 'jornada/material_apuntes.html', {'archivos': archivos})


from django.shortcuts import get_object_or_404, redirect

@login_required
@solo_academicos
def eliminar_archivo(request, archivo_id):
    archivo = get_object_or_404(ArchivoAcademico, id=archivo_id)

    if request.user == archivo.academico.user:
        archivo.archivo.delete()  # Borra el archivo del sistema de almacenamiento
        archivo.delete()  # Borra la entrada en la base de datos
        messages.success(request, "Archivo eliminado exitosamente.")
    else:
        messages.error(request, "No tienes permiso para eliminar este archivo.")

    return redirect('material_apuntes')  # Cambia por el nombre real de la URL de la vista de archivos

from .forms import PublicarMaterialForm

@login_required
@solo_academicos
def publicar_material(request, archivo_id):
    archivo = get_object_or_404(ArchivoAcademico, id=archivo_id)

    if request.method == "POST":
        form = PublicarMaterialForm(request.POST)
        if form.is_valid():
            asignatura_id = int(form.cleaned_data['asignatura'])  # Convierte a entero
            asignatura = get_object_or_404(Asignatura, id=asignatura_id)  # Obtiene la instancia

            archivo.asignatura = asignatura  # Asigna la instancia correcta
            archivo.save()  # Guarda los cambios en la base de datos
            return redirect('material')  # Redirige a la página pública

    else:
        # Si el archivo ya tiene una asignatura, seleccionarla en el formulario
        form = PublicarMaterialForm(initial={'asignatura': str(archivo.asignatura.id) if archivo.asignatura else ''})

    return render(request, "jornada/publicar_material.html", {"form": form, "archivo": archivo})


# Hoy es 2025 29 marzo
# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Sala, Reserva

@login_required
def reservar_sala(request):
    if request.method == 'POST':
        sala_id = request.POST.get('sala')
        titulo = request.POST.get('titulo')
        fecha = request.POST.get('fecha')
        hora_inicio = request.POST.get('hora_inicio')
        hora_fin = request.POST.get('hora_fin')

        # Manejo de excepción al buscar la sala
        try:
            sala = Sala.objects.get(id=sala_id)
        except Sala.DoesNotExist:
            return render(request, 'jornada/reserva.html', {'error': 'La sala seleccionada no existe.'})

        # Crear la reserva si la sala existe
        Reserva.objects.create(
            sala=sala,
            usuario=request.user,
            titulo=titulo,
            fecha=fecha,
            hora_inicio=hora_inicio,
            hora_fin=hora_fin
        )
        return redirect('calendario')

    salas = Sala.objects.all()
    return render(request, 'jornada/reserva.html', {'salas': salas})

# def render_calendar(request):
#     return render(request, 'jornada/calendario.html')

# from django.shortcuts import render
# from .models import Sala

def render_calendar(request):
    salas = Sala.objects.all()
    return render(request, 'jornada/calendario.html', {'salas': salas})

from django.views.decorators.csrf import csrf_exempt
from datetime import timedelta, date
from dateutil.relativedelta import relativedelta
from django.utils.timezone import now

def crear_eventos_recurrentes(reserva, frecuencia):
    eventos = [reserva]
    current_date = reserva.fecha
    end_date = now().date() + relativedelta(years=1)  # Limitar a un año de repetición

    while current_date <= end_date:
        if frecuencia == 'diaria':
            current_date += timedelta(days=1)
        elif frecuencia == 'semanal':
            current_date += timedelta(weeks=1)
        elif frecuencia == 'mensual_cuarto':
            current_date += relativedelta(months=1)
            # Ajustar al cuarto jueves del mes
            first_day = current_date.replace(day=1)
            thursdays = [first_day + timedelta(days=(3 - first_day.weekday()) % 7 + 7 * i) for i in range(4)]
            current_date = thursdays[3] if len(thursdays) >= 4 else thursdays[-1]
        elif frecuencia == 'mensual_ultimo':
            current_date += relativedelta(months=1)
            last_day = current_date.replace(day=1) + relativedelta(day=31)
            while last_day.weekday() != 3:  # Último jueves
                last_day -= timedelta(days=1)
            current_date = last_day
        elif frecuencia == 'anual':
            current_date += relativedelta(years=1)
        elif frecuencia == 'laboral':
            current_date += timedelta(days=1)
            while current_date.weekday() >= 5:  # Evitar sábado y domingo
                current_date += timedelta(days=1)
        else:
            break  # No repetir si la frecuencia es 'ninguna'

        if current_date <= end_date:
            eventos.append(Reserva(
                sala=reserva.sala,
                usuario=reserva.usuario,
                titulo=reserva.titulo,
                fecha=current_date,
                hora_inicio=reserva.hora_inicio,
                hora_fin=reserva.hora_fin
            ))

    Reserva.objects.bulk_create(eventos)


from datetime import datetime, timedelta
@csrf_exempt
def api_reservas(request, reserva_id=None):
    # Ver reservas - acceso público
    if request.method == 'GET':
        if reserva_id:
            try:
                reserva = Reserva.objects.get(id=reserva_id)
                data = {
                    'id': reserva.id,
                    'titulo': reserva.titulo,
                    'sala': reserva.sala.nombre,
                    'fecha': str(reserva.fecha),
                    'hora_inicio': str(reserva.hora_inicio),
                    'hora_fin': str(reserva.hora_fin),
                    'usuario': reserva.usuario.username,
                    'frecuencia': reserva.frecuencia if hasattr(reserva, 'frecuencia') else 'ninguna'
                }
                return JsonResponse(data, safe=False)
            except Reserva.DoesNotExist:
                return JsonResponse({'error': 'Reserva no encontrada'}, status=404)

        reservas = Reserva.objects.all()
        eventos = [
            {
                'id': reserva.id,
                'title': f"{reserva.titulo} - {reserva.sala.nombre}",
                'start': f"{reserva.fecha}T{reserva.hora_inicio}",
                'end': f"{reserva.fecha}T{reserva.hora_fin}",
            }
            for reserva in reservas
        ]
        return JsonResponse(eventos, safe=False)

    # Crear o actualizar reserva - solo usuarios autenticados
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'No autorizado'}, status=403)

    if request.method in ['POST', 'PUT']:
        try:
            titulo = request.POST.get('titulo')
            sala_id = request.POST.get('sala')
            hora_inicio = request.POST.get('hora_inicio')
            hora_fin = request.POST.get('hora_fin')
            start = request.POST.get('start')
            fecha = start.split('T')[0]
            frecuencia = request.POST.get('frecuencia', 'ninguna')

            # Convertir fechas y horas a objetos datetime
            hora_inicio = datetime.strptime(hora_inicio, "%H:%M").time()
            hora_fin = datetime.strptime(hora_fin, "%H:%M").time()
            fecha = datetime.strptime(fecha, "%Y-%m-%d").date()

            # Obtener las fechas de inicio y fin (si existen)
            fecha_inicio = request.POST.get('fecha_inicio')
            fecha_fin = request.POST.get('fecha_fin')

            # Convertir fechas de inicio y fin a objetos date (si no están vacías)
            if fecha_inicio and fecha_fin:
                fecha_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d").date()
                fecha_fin = datetime.strptime(fecha_fin, "%Y-%m-%d").date()
            else:
                # Si las fechas no están definidas, usar la fecha única
                fecha_inicio = fecha
                fecha_fin = fecha

            sala = Sala.objects.get(id=sala_id)

            # Verificar conflictos de horario
            def verificar_conflicto(fecha_reserva):
                conflictos = Reserva.objects.filter(
                    sala_id=sala_id,
                    fecha=fecha_reserva,
                    hora_inicio__lt=hora_fin,
                    hora_fin__gt=hora_inicio
                ).exclude(id=reserva_id)

                if conflictos.exists():
                    return True
                return False

            def crear_reserva(fecha_reserva):
                if verificar_conflicto(fecha_reserva):
                    raise Exception(f'Conflicto de horario el {fecha_reserva}.')
                Reserva.objects.create(
                    sala=sala,
                    usuario=request.user,
                    titulo=titulo,
                    fecha=fecha_reserva,
                    hora_inicio=hora_inicio,
                    hora_fin=hora_fin,
                    frecuencia=frecuencia,
                    fecha_inicio=fecha_inicio,
                    fecha_fin=fecha_fin
                )

            # Crear reservas según la frecuencia y el rango de fechas
            current_date = fecha_inicio
            while current_date <= fecha_fin:
                if frecuencia == 'diaria':
                    crear_reserva(current_date)
                    current_date += timedelta(days=1)
                elif frecuencia == 'semanal':
                    crear_reserva(current_date)
                    current_date += timedelta(weeks=1)
                elif frecuencia == 'mensual_cuarto':
                    crear_reserva(current_date)
                    current_date += relativedelta(months=1)
                elif frecuencia == 'mensual_ultimo':
                    crear_reserva(current_date)
                    current_date += relativedelta(months=1)
                elif frecuencia == 'anual':
                    crear_reserva(current_date)
                    current_date += relativedelta(years=1)
                elif frecuencia == 'laboral':
                    if current_date.weekday() < 5:
                        crear_reserva(current_date)
                    current_date += timedelta(days=1)
                else:
                    # Si no es recurrente, solo crear una vez
                    crear_reserva(fecha)
                    break

            return JsonResponse({'status': 'Reserva creada o actualizada'}, status=201)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


    # Eliminar reserva - solo el creador puede hacerlo
    elif request.method == 'DELETE':
        try:
            if reserva_id is None:
                return JsonResponse({'error': 'ID de reserva no proporcionado'}, status=400)

            reserva = Reserva.objects.get(id=reserva_id)

            # Verificar si el usuario que solicita es el creador
            if reserva.usuario != request.user:
                return JsonResponse({'error': 'No tienes permiso para eliminar esta reserva'}, status=403)

            # Eliminar todas las reservas del mismo grupo
            if reserva.frecuencia != 'ninguna':
                Reserva.objects.filter(titulo=reserva.titulo, sala=reserva.sala).delete()
                return JsonResponse({'status': 'Reservas repetidas eliminadas'}, status=204)
            else:
                reserva.delete()
                return JsonResponse({'status': 'Reserva única eliminada'}, status=204)

        except Reserva.DoesNotExist:
            return JsonResponse({'error': 'Reserva no encontrada'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)



from .models import Reserva

def verificar_disponibilidad(request):
    try:
        sala_id = request.GET.get('sala')
        fecha = request.GET.get('fecha')
        hora_inicio = request.GET.get('hora_inicio')
        hora_fin = request.GET.get('hora_fin')

        if not (sala_id and fecha and hora_inicio and hora_fin):
            return JsonResponse({'disponible': False, 'mensaje': 'Datos incompletos'}, status=400)

        # Convertir horas a formato datetime
        hora_inicio = datetime.strptime(hora_inicio, "%H:%M").time()
        hora_fin = datetime.strptime(hora_fin, "%H:%M").time()

        # Verificar si existe un conflicto
        conflictos = Reserva.objects.filter(
            sala_id=sala_id,
            fecha=fecha,
            hora_inicio__lt=hora_fin,
            hora_fin__gt=hora_inicio
        )

        if conflictos.exists():
            return JsonResponse({'disponible': False, 'mensaje': 'Sala ocupada en el horario seleccionado'})

        return JsonResponse({'disponible': True, 'mensaje': 'Sala disponible'})

    except Exception as e:
        return JsonResponse({'disponible': False, 'mensaje': f'Error: {str(e)}'}, status=500)


# 5 de julio de 2025

from .models import Academico, Aviso
from .forms import AvisoForm

@login_required
def crear_aviso(request, slug):
    academico = get_object_or_404(Academico, slug=slug)
    # ✅ Evita que otros creen avisos en perfiles ajenos
    if request.user != academico.user:
        messages.warning(request, "No puedes crear un aviso en nombre de otro académico.")
        return redirect('detalle_academico', slug=slug)
    if request.method == 'POST':
        form = AvisoForm(request.POST)
        if form.is_valid():
            aviso = form.save(commit=False)
            aviso.academico = academico
            aviso.save()
            messages.success(request, "✅ Aviso creado exitosamente.")
            return redirect('detalle_academico', slug=slug)
    else:
        form = AvisoForm()
    return render(request, 'jornada/academicos/crear_aviso.html', {
        'form': form,
        'academico': academico
    })


from .models import Aviso
@login_required
def lista_avisos(request):
    if not request.user.is_authenticated:
        return redirect('login')  # por si no está logueado

    try:
        academico = request.user.academico
    except Academico.DoesNotExist:
        return redirect('portada')  # o mostrar error si no es académico

    if not academico.tiene_cargo('Director(a) de Departamento'):
        return redirect('portada')

    # Obtener solo los avisos de académicos del mismo departamento
    departamento = academico.departamento
    avisos = Aviso.objects.select_related('academico').filter(
        academico__departamento=departamento
    ).order_by('-creado')

    # Resto del código de filtros
    meses = [
        (1, 'Enero'), (2, 'Febrero'), (3, 'Marzo'), (4, 'Abril'),
        (5, 'Mayo'), (6, 'Junio'), (7, 'Julio'), (8, 'Agosto'),
        (9, 'Septiembre'), (10, 'Octubre'), (11, 'Noviembre'), (12, 'Diciembre'),
    ]
    hoy = now()
    mes_actual = hoy.month
    anio_actual = hoy.year

    semana = request.GET.get('semana')
    mes = request.GET.get('mes') or str(mes_actual)
    anio = request.GET.get('anio') or str(anio_actual)

    try:
        anio = int(anio)
    except ValueError:
        anio = anio_actual

    if semana:
        try:
            semana = int(semana)
            fecha_inicio = datetime.fromisocalendar(anio, semana, 1)
            fecha_fin = fecha_inicio + timedelta(days=6)
            avisos = avisos.filter(fecha_salida__date__range=[fecha_inicio.date(), fecha_fin.date()])
        except (ValueError, TypeError):
            semana = ''
    elif mes:
        try:
            mes = int(mes)
            avisos = avisos.filter(fecha_salida__year=anio, fecha_salida__month=mes)
        except ValueError:
            mes = mes_actual
    elif anio:
        avisos = avisos.filter(fecha_salida__year=anio)

    return render(request, 'jornada/avisos/lista_avisos.html', {
        'avisos': avisos,
        'anio': anio,
        'mes': str(mes),
        'semana': semana or '',
        'meses': meses,
    })


from django.shortcuts import render, get_object_or_404, redirect
from .models import Academico, Publicacion
from .forms import PublicacionForm
from .utils.crossref import obtener_datos_crossref
from django.contrib import messages

def agregar_publicacion_doi(request, slug):
    academico = get_object_or_404(Academico, slug=slug)

    if request.method == "POST":
        # Paso 1: envío del DOI
        if "doi_submit" in request.POST:
            doi = request.POST.get("doi", "").strip()
            datos = obtener_datos_crossref(doi)

            if datos:
                form = PublicacionForm(initial=datos)
                return render(request, "jornada/academicos/agregar_publicacion_doi.html", {
                    "form": form,
                    "academico": academico,
                    "doi": doi
                })
            else:
                messages.error(request, "No se pudo obtener información desde Crossref.")
                return redirect("agregar_publicacion_doi", slug=slug)

        # Paso 2: envío del formulario editable
        else:
            form = PublicacionForm(request.POST, request.FILES)
            if form.is_valid():
                publicacion = form.save(commit=False)
                publicacion.academico = academico
                publicacion.save()
                messages.success(request, "Publicación agregada exitosamente.")
                return redirect("detalle_academico", slug=slug)

    return render(request, "jornada/academicos/agregar_publicacion_doi.html", {"academico": academico})


from django.shortcuts import render, get_object_or_404, redirect
from .models import Academico, Publicacion
from .forms import PublicacionForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def agregar_publicacion_manual(request, slug):
    academico = get_object_or_404(Academico, slug=slug)
    if request.user != academico.user and request.user.academico.tiene_cargo('Director(a) de Departamento'):
        messages.error(request, "No tienes permisos para agregar publicaciones a este perfil.")
        return redirect('detalle_academico', slug=slug)

    if request.method == 'POST':
        form = PublicacionForm(request.POST, request.FILES)
        if form.is_valid():
            publicacion = form.save(commit=False)
            publicacion.academico = academico
            publicacion.save()
            messages.success(request, "Publicación agregada exitosamente.")
            return redirect('detalle_academico', slug=slug)
    else:
        form = PublicacionForm()

    return render(request, 'jornada/academicos/agregar_publicacion_manual.html', {
        'form': form,
        'academico': academico
    })


# En views.py
from django.shortcuts import get_object_or_404, render, redirect
from .models import Publicacion
from .forms import PublicacionForm

def editar_publicacion(request, pk):
    publicacion = get_object_or_404(Publicacion, pk=pk)
    if request.method == "POST":
        form = PublicacionForm(request.POST, request.FILES, instance=publicacion)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Publicación actualizada correctamente.')
            return redirect("detalle_academico", slug=publicacion.academico.slug)
    else:
        form = PublicacionForm(instance=publicacion)
    return render(request, "jornada/academicos/editar_publicacion.html", {"form": form, "publicacion": publicacion})


@login_required
def confirmar_eliminar_publicacion(request, pk):
    publicacion = get_object_or_404(Publicacion, pk=pk)
    if request.user != publicacion.academico.user and (
        not hasattr(request.user, 'academico') or request.user.academico.tiene_cargo('Director(a) de Departamento')):
        return redirect('detalle_academico', slug=publicacion.academico.slug)

    return render(request, 'jornada/publicaciones/confirmar_eliminar.html', {
        'publicacion': publicacion
    })

@login_required
def eliminar_publicacion(request, pk):
    publicacion = get_object_or_404(Publicacion, pk=pk)
    slug = publicacion.academico.slug

    if request.user != publicacion.academico.user and (
        not hasattr(request.user, 'academico') or request.user.academico.tiene_cargo('Director(a) de Departamento')):
        return redirect('detalle_academico', slug=slug)

    publicacion.delete()
    messages.success(request, "✅ Publicación eliminada correctamente.")
    return redirect('detalle_academico', slug=slug)



from django.template.loader import get_template
from weasyprint import HTML
from django.http import HttpResponse

@login_required
def exportar_cv_pdf(request, slug):
    academico = get_object_or_404(Academico, slug=slug)

    publicaciones_agrupadas = [
        ("Trabajos publicados en revistas indexadas", academico.publicaciones.filter(estado='publicada')),
        ("Trabajos aceptados", academico.publicaciones.filter(estado='aceptada')),
        ("Trabajos sometidos", academico.publicaciones.filter(estado='sometida')),
        ("Trabajos en preparación", academico.publicaciones.filter(estado='en_preparacion')),
        ("Publicaciones rechazadas", academico.publicaciones.filter(estado='rechazada')),
    ]

    template = get_template('jornada/academicos/cv_pdf_template.html')
    html_string = template.render({
        'academico': academico,
        'publicaciones_agrupadas': publicaciones_agrupadas,
    })

    base_url = request.build_absolute_uri('/')

    html = HTML(string=html_string, base_url=base_url)
    pdf = html.write_pdf()

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="{academico.nombre}_CV.pdf"'
    return response

from jornada.models import Escuela
def academicos_ima(request):
    escuela = Escuela.objects.get(slug="ingenieria-matematica")
    academicos = escuela.academicos.all()
    return render(request, "jornada/lista_academicos.html", {"academicos": academicos})


def lista_academicos_por_escuela(request, slug):
    escuela = get_object_or_404(Escuela, slug=slug)
    academicos = escuela.academicos.all()

    template = f'jornada/escuelas/{slug}/lista_academicos.html'

    return render(request, template, {
        "academicos": academicos,
        "escuela": escuela,
    })



from jornada.models import ProgramaPostgrado

def academicos_por_postgrado(request, slug):
    programa = ProgramaPostgrado.objects.get(slug=slug)
    academicos = programa.academicos.all()
    return render(request, 'jornada/academicos_por_programa.html', {
        'academicos': academicos,
        'programa': programa
    })


# 13 de julio de 2025
from .models import Escuela
def pagina_escuela(request, slug):
    escuela = get_object_or_404(Escuela, slug=slug)

    # Selecciona la plantilla específica o una genérica si no existe
    template = select_template([
        f'jornada/escuelas/{slug}/portada.html',   # Ej: jornada/escuelas/ingenieria-matematica/portada.html
        'jornada/escuelas/portada_generica.html'   # Fallback si no existe la específica
    ])

    return render(request, template.template.name, {
        'escuela': escuela
    })

from .models import Departamento

def filtro_math(request):
    dpto_mate = Departamento.objects.get(nombre="Matemática, Física y Estadística")

    escuelas_mate = Escuela.objects.filter(departamento=dpto_mate)

    return render(request, 'jornada/escuelas/ingenieria-matematica.html', {
        'escuelas_mate': escuelas_mate,
    })


from django.template.loader import select_template
from .models import ProgramaPostgrado

def filtroposgrado_por_departamento(request, slug):
    departamento = get_object_or_404(Departamento, slug=slug)
    programas = ProgramaPostgrado.objects.filter(departamento=departamento)

    # Busca un template específico (por slug) y si no existe, usa uno genérico
    template = select_template([
        f'jornada/postgrados/{slug}.html',
        'jornada/postgrados/base_postgrado.html'
    ])

    return render(request, template.template.name, {
        'programas': programas,
        'departamento': departamento,
    })


def comite_por_escuela(request, slug):
    escuela = get_object_or_404(Escuela, slug=slug)
    template = f'jornada/escuelas/{slug}/comites.html'
    return render(request, template, {'escuela': escuela})

def malla_por_escuela(request, slug):
    template = f'jornada/escuelas/{slug}/malla.html'
    return render(request, template, {"escuela": Escuela.objects.get(slug=slug)})

def representantes_estudiantiles_por_escuela(request, slug):
    template = f'jornada/escuelas/{slug}/representantes_estudiantiles.html'
    return render(request, template, {"escuela": Escuela.objects.get(slug=slug)})

def informacion_por_carrera(request, slug):
    template = f'jornada/escuelas/{slug}/informacion.html'
    return render(request, template, {"escuela": Escuela.objects.get(slug=slug)})


from collections import OrderedDict

CARGOS_CLAVE = [
    "Decano(a)",
    "Director(a) de Departamento",
    "Director(a) de Doctorado",
    "Director(a) de Magíster",
    "Director(a) de Escuela",
]

def academicos_por_departamento(request, slug):
    departamento = get_object_or_404(Departamento, slug=slug)
    todos = Academico.objects.filter(departamento=departamento).prefetch_related("cargos").distinct()

    usados = set()
    academicos_ordenados = []

    # Agregar primero los cargos clave
    for cargo in CARGOS_CLAVE:
        aca = todos.filter(cargos__nombre=cargo).distinct()
        academicos_ordenados.extend(aca)
        usados.update(a.id for a in aca)

    # Agregar el resto (que solo tienen cargo 'Académico(a)')
    resto = todos.filter(cargos__nombre="Académico(a)").exclude(id__in=usados)
    academicos_ordenados.extend(resto)

    return render(request, f'jornada/academicos/{slug}/por_departamento.html', {
        'departamento': departamento,
        'academicos': academicos_ordenados,
    })

from .models import Academico, Aviso
from django.views.decorators.clickjacking import xframe_options_exempt
from django.urls import reverse

@xframe_options_exempt
def perfil_academico_embed(request, slug):
    academico = get_object_or_404(Academico, slug=slug)

    # Publicaciones
    publicaciones_publicadas   = academico.publicaciones.filter(estado='publicada')
    publicaciones_aceptadas    = academico.publicaciones.filter(estado='aceptada')
    publicaciones_sometidas    = academico.publicaciones.filter(estado='sometida')
    publicaciones_en_preparacion = academico.publicaciones.filter(estado='en_preparacion')
    # (omites rechazadas si no quieres mostrar)

    # Proyectos
    proyectos_actuales = academico.proyectos_investigacion_actuales
    proyectos_pasados  = academico.proyectos_investigacion_pasados

    # Actividades y otros
    actividades = academico.actividades_curriculares
    otros       = academico.otros_interes

    embed_path = reverse('perfil_academico_embed', args=[slug])
    absolute_embed_url = request.build_absolute_uri(embed_path)

    return render(request, 'jornada/academico_embed.html', {
        'academico': academico,
        'publicaciones_publicadas': publicaciones_publicadas,
        'publicaciones_aceptadas': publicaciones_aceptadas,
        'publicaciones_sometidas': publicaciones_sometidas,
        'publicaciones_en_preparacion': publicaciones_en_preparacion,
        'proyectos_actuales': proyectos_actuales,
        'proyectos_pasados': proyectos_pasados,
        'actividades': actividades,
        'otros': otros,
        'absolute_embed_url': absolute_embed_url,
    })
