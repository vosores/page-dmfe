from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

class Departamento(models.Model):
    nombre = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre

class Escuela(models.Model):
    nombre = models.CharField(max_length=200, unique=True)
    # slug = models.SlugField(unique=True, blank=True, null=True)
    # slug = models.SlugField(unique=True, blank=True, null=False) # Cambiado a null=False para evitar problemas con la creación de objetos sin slug
    slug = models.SlugField(unique=True, blank=True)
    # departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE, related_name='escuelas')
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE, related_name='escuelas', null=True, blank=True)


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre

class ProgramaPostgrado(models.Model):
    nombre = models.CharField(max_length=200, unique=True)
    # slug = models.SlugField(unique=True, blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True)
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE, related_name='programas', null=True, blank=True)


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre

class Cargo(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre

class Academico(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)

    CARGO_CHOICES = [
        ('Director de departamento', 'Director de departamento'),
        ('Director de escuela', 'Director de escuela'),
        ('Académico', 'Académico'),
    ]

    HONORIFIC_CHOICES = [
        ('',       '— Selecciona —'),
        ('Dr.',    'Dr.'),
        ('Dra.',   'Dra.'),
        ('Prof.',  'Prof.'),
        ('Profa.', 'Profa.'),
        ('Mg.',    'Mg.'),
        ('M.Sc.',  'M.Sc.'),
        ('M.A.',   'M.A.'),
        ('MBA',    'MBA'),
        ('PhD',    'PhD'),
    ]
    honorifico = models.CharField(
        "Prefijo / Título",
        max_length=10,
        choices=HONORIFIC_CHOICES,
        blank=True,
        help_text="Cómo quiere que se refieran a usted (Dr., Dra., Ing., Mg., etc.)"
    )

    nombre = models.CharField(max_length=200)
    foto = models.ImageField(upload_to='academicos/')
    titulo_grado = models.TextField(
        "Títulos y Grados", 
        blank=True,
        help_text="Ingrese títulos y grados, colocando cada uno en una línea separada (deje un salto de línea entre cada uno)."
    )
    especialidad = models.CharField(max_length=200)
    biografia = models.TextField()
    cargos = models.ManyToManyField('Cargo', blank=True, related_name='academicos')
    def tiene_cargo(self, nombre):
        return self.cargos.filter(nombre__iexact=nombre).exists()
    
    # cargo = models.CharField(max_length=30, choices=CARGO_CHOICES, default='Académico')
    slug = models.SlugField(unique=True, blank=True)
    
    departamento = models.ForeignKey(Departamento, on_delete=models.SET_NULL, blank=True, null=True, related_name='academicos')
    lineas_investigacion = models.TextField(
        "Líneas de Investigación", 
        blank=True,
        help_text="Ingrese las líneas de investigación, colocando cada una en una línea separada (deje un salto de línea entre cada una)."
    )
    actividades_curriculares = models.TextField("Actividades Curriculares", blank=True, help_text="Lista de cursos o actividades curriculares.")
    otros_interes = models.TextField("Otros de Interés", blank=True, help_text="Cualquier otra información relevante.")
    email = models.EmailField("Correo Electrónico", blank=True, null=True, help_text="Ingrese el correo electrónico del académico.")
    sitio_web = models.URLField("Página Web", blank=True, null=True, help_text="Ingrese la URL de la página web del académico.")
    researchgate = models.URLField("ResearchGate", blank=True, null=True, help_text="Ingrese la URL a ResearchGate.")
    orcid = models.URLField("ORCID", blank=True, null=True, help_text="Ingrese la URL a ORCID.")
    wos = models.URLField("WOS", blank=True, null=True, help_text="Ingrese la URL a WOS.")
    proyectos_investigacion_actuales = models.TextField(
        "Proyectos de Investigación Actuales", 
        blank=True,
        help_text="Listado de proyectos actuales de investigación. Puede incluir HTML para formatear listas."
    )
    proyectos_investigacion_pasados = models.TextField(
        "Proyectos de Investigación Pasados", 
        blank=True,
        help_text="Listado de proyectos pasados de investigación. Puede incluir HTML para formatear listas."
    )

    escuelas = models.ManyToManyField(Escuela, blank=True, related_name='academicos')
    programas_postgrado = models.ManyToManyField(ProgramaPostgrado, related_name='academicos', blank=True)
    # programas_postgrado = models.ManyToManyField(ProgramaPostgrado, blank=True, related_name='academicos_postgrado')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)

    def __str__(self):
        if self.honorifico:
            return f"{self.honorifico} {self.nombre}"
        return self.nombre


class Asignatura(models.Model):
    nombre = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.nombre

import os
from django.utils.timezone import now

def ruta_archivo(instance, filename):
    """Guarda los archivos en una carpeta específica por académico, agregando un timestamp para evitar sobrescrituras."""
    extension = filename.split('.')[-1]  # Extrae la extensión del archivo
    nombre_base = os.path.splitext(filename)[0]  # Obtiene el nombre sin la extensión
    timestamp = now().strftime('%Y%m%d%H%M%S')  # Genera un timestamp con el formato AAAAMMDDHHMMSS
    nuevo_nombre = f"{nombre_base}_{timestamp}.{extension}"  # Agrega el timestamp al nombre
    return f'archivos_academicos/{instance.academico.user.username}/{nuevo_nombre}'


from django.core.exceptions import ValidationError
class ArchivoAcademico(models.Model):
    """ Modelo para los archivos subidos por los académicos """
    academico = models.ForeignKey(Academico, on_delete=models.CASCADE, related_name="archivos")
    titulo = models.CharField(max_length=255, help_text="Nombre del archivo o descripción corta.")
    # archivo = models.FileField(upload_to=ruta_archivo)  # Se guardará en 'archivos_academicos/{username}/'
    archivo = models.FileField(upload_to=ruta_archivo, blank=True, null=True,help_text="Opcional: Sube un archivo si lo deseas. Puedes proporcionar un archivo o un enlace (en el siguiente apartado).")  # Ahora es opcional
    link = models.URLField(blank=True, null=True, help_text="Opcional. Enlace a un documento externo. Puedes proporcionar un enlace o un archivo (en el apartado previo).")
    fecha_subida = models.DateTimeField(auto_now_add=True)
    asignatura = models.ForeignKey(Asignatura, on_delete=models.SET_NULL, null=True, blank=True, related_name="archivos_publicados")
    descripcion = models.TextField(blank=True, null=True, help_text="Descripción opcional del archivo.")
    seccion = models.CharField(max_length=255, blank=True, null=True, help_text="Nombre de sección opcional del archivo.")

    def clean(self):
        """Asegura que al menos uno de los dos campos (archivo o link) esté presente."""
        if not self.archivo and not self.link:
            raise ValidationError("Debes subir un archivo o proporcionar un enlace.")

    def __str__(self):
        return f"{self.titulo} - {self.academico.nombre}"


# hoy
class Estudiante(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    carrera = models.CharField(max_length=200, blank=True, null=True)
    año_ingreso = models.IntegerField(blank=True, null=True)
    rut = models.CharField(max_length=12, blank=True, null=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username



# hoy 29 marzo 2025
# models.py
class Sala(models.Model):
    nombre = models.CharField(max_length=100)
    ubicacion = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.nombre

# class Reserva(models.Model):
#     sala = models.ForeignKey(Sala, on_delete=models.CASCADE)
#     usuario = models.ForeignKey(User, on_delete=models.CASCADE)
#     titulo = models.CharField(max_length=100)
#     fecha = models.DateField()
#     hora_inicio = models.TimeField()
#     hora_fin = models.TimeField()

#     class Meta:
#         unique_together = (('sala', 'fecha', 'hora_inicio'),)

#     def __str__(self):
#         return f'{self.titulo} - {self.sala.nombre} ({self.fecha})'
from uuid import uuid4

class Reserva(models.Model):
    FRECUENCIA_CHOICES = [
        ('ninguna', 'Ninguna'),
        ('diaria', 'Cada día'),
        ('semanal', 'Cada semana el mismo día'),
        ('mensual_cuarto', 'Cada mes el cuarto día de la semana'),
        ('mensual_ultimo', 'Cada mes el último día de la semana'),
        ('anual', 'Anualmente en la misma fecha'),
        ('laboral', 'Todos los días laborables'),
    ]

    sala = models.ForeignKey(Sala, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100)
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    fecha_inicio = models.DateField(null=True, blank=True)  # Nuevo campo
    fecha_fin = models.DateField(null=True, blank=True)      # Nuevo campo
    frecuencia = models.CharField(max_length=20, choices=FRECUENCIA_CHOICES, default='ninguna')
    grupo_id = models.UUIDField(default=uuid4, editable=False)  # Identificador de grupo

    class Meta:
        unique_together = (('sala', 'fecha', 'hora_inicio'),)

    def __str__(self):
        return f'{self.titulo} - {self.sala.nombre} ({self.fecha})'


# 5 julio 2025
from django.conf import settings
class Aviso(models.Model):
    academico = models.ForeignKey(
        Academico,
        on_delete=models.CASCADE,
        related_name='avisos'
    )
    detalle_actividad = models.TextField(verbose_name="Detalle de la actividad", blank=True)
    destino = models.CharField("Destino", max_length=200)
    tipo_actividad = models.CharField(
        "Tipo de actividad",
        max_length=20,
        choices=[
            ("Charla", "Charla"),
            ("Congreso", "Congreso"),
            ("Viaje", "Viaje"),
            ("Otro", "Otro"),
        ]
    )
    fecha_salida = models.DateTimeField("Fecha y hora de salida")
    fecha_regreso = models.DateTimeField("Fecha y hora de regreso")
    telefono_emergencia = models.CharField(
        "Teléfono de emergencia", max_length=20
    )
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Aviso de {self.academico.nombre} a {self.destino}"
    

# from django.utils import timezone
# class Publicacion(models.Model):
#     TIPO_CHOICES = [
#         ('Articulo', 'Artículo'),
#         ('Libro', 'Libro'),
#         ('Capitulo', 'Capítulo de libro'),
#         ('Conferencia', 'Artículo en conferencia'),
#         ('Otro', 'Otro'),
#     ]

#     academico = models.ForeignKey('Academico', on_delete=models.CASCADE, related_name='publicaciones')
#     titulo = models.CharField(max_length=300)
#     autores = models.TextField(help_text="Lista completa de autores en formato: Apellido, Iniciales")
#     revista = models.CharField("Revista / Editorial", max_length=200, blank=True)
#     anio = models.PositiveIntegerField(default=timezone.now().year)
#     doi = models.CharField(max_length=100, blank=True)
#     tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='Articulo')
#     pdf = models.FileField(upload_to='publicaciones/', blank=True, null=True)
#     visible = models.BooleanField(default=True)

#     class Meta:
#         ordering = ['-anio']  # Ordena automáticamente por año descendente

#     def __str__(self):
#         return f"{self.titulo} ({self.anio})"


from django.utils import timezone
class Publicacion(models.Model):
    ESTADO_CHOICES = [
        ('en_preparacion', 'En preparación'),
        ('sometida', 'Sometida'),
        ('aceptada', 'Aceptada'),
        ('publicada', 'Publicada'),
        ('rechazada', 'Rechazada'),
    ]
    TIPO_CHOICES = [
        ('Articulo', 'Artículo'),
        ('Libro', 'Libro'),
        ('Capitulo', 'Capítulo de libro'),
        ('Conferencia', 'Artículo en conferencia'),
        ('Otro', 'Otro'),
    ]

    MESES_CHOICES = [
        (1, "Enero"), (2, "Febrero"), (3, "Marzo"), (4, "Abril"),
        (5, "Mayo"), (6, "Junio"), (7, "Julio"), (8, "Agosto"),
        (9, "Septiembre"), (10, "Octubre"), (11, "Noviembre"), (12, "Diciembre"),
    ]

    academico = models.ForeignKey('Academico', on_delete=models.CASCADE, related_name='publicaciones')
    titulo = models.CharField(max_length=300)
    autores = models.TextField(help_text="Lista completa de autores en formato: Apellido, Iniciales")
    revista = models.CharField("Revista / Editorial", max_length=200, blank=True)
    anio = models.PositiveIntegerField(default=timezone.now().year)
    mes = models.PositiveSmallIntegerField(choices=MESES_CHOICES, blank=True, null=True)  # <-- Nuevo campo
    doi = models.CharField(max_length=100, blank=True)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='Articulo')
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='en_preparacion')
    pdf = models.FileField(upload_to='publicaciones/', blank=True, null=True)
    visible = models.BooleanField(default=True)

    class Meta:
        ordering = ['-anio', '-mes', 'titulo']  # Ordena por año, luego mes descendente

    def __str__(self):
        return f"{self.titulo} ({self.anio})"
