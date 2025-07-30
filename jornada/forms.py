from django import forms
from .models import Academico
from .models import ArchivoAcademico, Asignatura
from .models import Cargo 

class AcademicoForm(forms.ModelForm):
    cargos = forms.ModelMultipleChoiceField(
    queryset=Cargo.objects.all().order_by('nombre'),
    widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
    required=False,
    label="Cargos"
    )
    class Meta:
        model = Academico
        # Lista de campos que permites editar:
        fields = [
            'honorifico',
            'nombre',
            'foto',
            'titulo_grado',
            'especialidad',
            'biografia',
            'departamento',
            'cargos',
            # 'cargo',
            'escuelas',
            'programas_postgrado',
            'lineas_investigacion',
            'actividades_curriculares',
            'otros_interes',
            'email',
            'sitio_web',
            'researchgate',
            'orcid',
            'wos',
            'proyectos_investigacion_actuales',
            'proyectos_investigacion_pasados',
        ]
        widgets = {
            # Campos de texto corto
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'style': 'width: 100%;'
            }),
            'especialidad': forms.TextInput(attrs={
                'class': 'form-control',
                'style': 'width: 100%;'
            }),
            'departamento': forms.Select(attrs={'class': 'form-select'}),
            # 'cargos': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
            # 'cargo': forms.TextInput(attrs={
            #     'class': 'form-control',
            #     'style': 'width: 100%;'
            # }),
            'escuelas': forms.CheckboxSelectMultiple(attrs={
                'class': 'form-check-input'
            }),
            'programas_postgrado': forms.CheckboxSelectMultiple(attrs={
                'class': 'form-check-input'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'style': 'width: 100%;'
            }),
            'sitio_web': forms.URLInput(attrs={
                'class': 'form-control',
                'style': 'width: 100%;'
            }),
            'researchgate': forms.URLInput(attrs={
                'class': 'form-control',
                'style': 'width: 100%;'
            }),
            'orcid': forms.URLInput(attrs={
                'class': 'form-control',
                'style': 'width: 100%;'
            }),
            'wos': forms.URLInput(attrs={
                'class': 'form-control',
                'style': 'width: 100%;'
            }),
            # Campos que necesitan área de texto (multilínea)
            'titulo_grado': forms.Textarea(attrs={
                'class': 'form-control',
                'style': 'width: 100%;',
                'rows': 10
            }),
            'biografia': forms.Textarea(attrs={
                'class': 'form-control',
                'style': 'width: 100%;',
                'rows': 5
            }),
            'lineas_investigacion': forms.Textarea(attrs={
                'class': 'form-control',
                'style': 'width: 100%;',
                'rows': 10
            }),
            'actividades_curriculares': forms.Textarea(attrs={
                'class': 'form-control',
                'style': 'width: 100%;',
                'rows': 10
            }),
            'otros_interes': forms.Textarea(attrs={
                'class': 'form-control',
                'style': 'width: 100%;',
                'rows': 10
            }),
            'proyectos_investigacion_actuales': forms.Textarea(attrs={
                'class': 'form-control',
                'style': 'width: 100%;',
                'rows': 10
            }),
            'proyectos_investigacion_pasados': forms.Textarea(attrs={
                'class': 'form-control',
                'style': 'width: 100%;',
                'rows': 10
            }),
        }

from django.contrib.auth.forms import AuthenticationForm

class CustomAuthForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personalizar labels y placeholders
        self.fields['username'].label = ""
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Usuario o correo electrónico'
        })
        self.fields['password'].label = ""
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Contraseña'
        })



# hoy 26 de feb

from .models import ArchivoAcademico

class ArchivoAcademicoForm(forms.ModelForm):
    class Meta:
        model = ArchivoAcademico
        fields = ['titulo', 'archivo', 'descripcion', 'seccion', 'link']
        widgets = {
            'seccion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Unidad 1 - Introducción'}),
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Teorema Fundamental del Cálculo'}),
            'archivo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Ej: Apuntes sobre cálculo en varias variables.', 'rows': 3}),
        }
    def clean(self):
        cleaned_data = super().clean()
        archivo = cleaned_data.get('archivo')
        link = cleaned_data.get('link')

        if not archivo and not link:
            raise forms.ValidationError("Debes subir un archivo o proporcionar un enlace.")

        return cleaned_data

from .models import ArchivoAcademico

# Lista de asignaturas manualmente definida
ASIGNATURAS_DISPONIBLES = [
    ("1", "IMA-111 » Introducción al Cálculo"),
    ("2", "IMA-112 » Introducción al Álgebra"),
    ("3", "IMA-113 » Geometría"),
    ("4", "IMA-114 » Introducción a la Ingeniería Matemática"),
    ("5", "IMA-115 » Comunicación Oral y Escrita en la Ingeniería Matemática"),
    ("6", "IFG-100 » Inglés I"),
    ("7", "IMA-121 » Cálculo I"),
    ("8", "IMA-122 » Álgebra I"),
    ("9", "IMA-123 » Física I"),
    ("10", "IMA-124 » Fundamentos de Economía I"),
    ("11", "IMA-125 » Computación I"),
    ("12", "IFG-200 » Inglés II"),
    ("13", "IMA-211 » Cálculo II"),
    ("14", "IMA-212 » Álgebra II"),
    ("15", "IMA-213 » Física II"),
    ("16", "IMA-214 » Fundamentos de la Economía II"),
    ("17", "IMA-215 » Computación II"),
    ("18", "IFG-300 » Inglés III"),
    ("19", "IMA-221 » Ecuaciones Diferenciales Ordinarias (Hito I)"),
    ("20", "IMA-222 » Álgebra III"),
    ("21", "IMA-223 » Física III"),
    ("22", "IMA-224 » Química"),
    ("23", "IMA-225 » Computación III"),
    ("24", "IFG-400 » Inglés IV"),
    ("25", "IMA-311 » Análisis Matemático"),
    ("26", "IMA-312 » Matemáticas Discretas y Combinatoria"),
    ("27", "IMA-313 » Termodinámica"),
    ("28", "IMA-314 » Probabilidades y Estadística"),
    ("29", "IMA-315 » Cálculo Numérico"),
    ("30", "MFG-114 » Introducción a la Fe"),
    ("31", "IMA-321 » Topología"),
    ("32", "IMA-322 » Estadística Inferencial"),
    ("33", "IMA-323 » Gestión Estratégica"),
    ("34", "IMA-324 » Modelos Matemáticos Computacionales"),
    ("35", "MFG-216 » Ética Cristiana"),
    ("36", "IMA-411 » Análisis Funcional"),
    ("37", "IMA-412 » Teoría de la Medida"),
    ("38", "IMA-413 » Ciencia de Datos"),
    ("39", "IMA-414 » Marketing e Inteligencia de Negocios"),
    ("40", "IMA-415 » Pre-Práctica"),
    ("41", "CFG » Certificación I"),
    ("42", "IMA-421 » Ecuaciones en Derivadas Parciales"),
    ("43", "IMA-422 » Análisis Numérico"),
    ("44", "IMA-423 » Optimización Lineal (Hito II)"),
    ("45", "IMA-424 » Procesos Estocásticos"),
    ("46", "CFG » Certificación II"),
    ("47", "IMA-511 » Optativo de Profundización I"),
    ("48", "IMA-512 » Laboratorio de Modelación I"),
    ("49", "IMA-513 » Optimización no Lineal"),
    ("50", "IMA-514 » Gestión Financiera"),
    ("51", "IMA-515 » Metodología de la Investigación"),
    ("52", "CFG » Certificación III"),
    ("53", "IMA-521 » Optativo de Profundización II"),
    ("54", "IMA-522 » Laboratorio de Modelación II"),
    ("55", "IMA-523 » Evaluación de Proyectos"),
    ("56", "IMA-524 » Seminario de Título I"),
    ("57", "IMA-525 » Práctica Profesional I"),
    ("58", "IMA-611 » Optativo de Profundización III"),
    ("59", "IMA-612 » Seminario de Título II"),
    ("60", "IMA-613 » Práctica Profesional II (Hito III)"),
]

class PublicarMaterialForm(forms.Form):  # No usar ModelForm ya que no estamos usando todos los campos del modelo
    asignatura = forms.ChoiceField(
        choices=ASIGNATURAS_DISPONIBLES,
        required=True,
        label="Selecciona la asignatura"
    )


# 5 julio 2025
from .models import Aviso
class AvisoForm(forms.ModelForm):
    class Meta:
        model = Aviso
        fields = [
            'destino',
            'tipo_actividad',
            'fecha_salida',
            'fecha_regreso',
            'telefono_emergencia',
            'detalle_actividad',
        ]
        widgets = {
            'fecha_salida': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'fecha_regreso': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'detalle_actividad': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Describa brevemente la actividad a realizar...',
            }),
        }


class DOIForm(forms.Form):
    doi = forms.CharField(label='DOI', max_length=100)


# 6 de julio de 2025
from django import forms
from .models import Publicacion

class PublicacionForm(forms.ModelForm):
    class Meta:
        model = Publicacion
        fields = ['titulo', 'autores', 'revista', 'anio', 'doi', 'tipo', 'estado', 'pdf', 'visible']
        widgets = {
            'anio': forms.NumberInput(attrs={'min': 1900, 'max': 2100}),
            'autores': forms.Textarea(attrs={'rows': 2}),
            'titulo': forms.Textarea(attrs={'rows': 2}),
        }

