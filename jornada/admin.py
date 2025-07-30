from django.contrib import admin
from .models import Academico, Estudiante
from .models import Sala, Reserva
from .models import Aviso
from .models import Publicacion
from .models import Escuela, ProgramaPostgrado, Departamento, Cargo
from django.utils.safestring import mark_safe

# @admin.register(Departamento)
# class DepartamentoAdmin(admin.ModelAdmin):
#     list_display = ('nombre',)
#     prepopulated_fields = {'slug': ('nombre',)}


@admin.register(Departamento)
class DepartamentoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'cantidad_academicos', 'academicos_asociados')
    prepopulated_fields = {'slug': ('nombre',)}

    def cantidad_academicos(self, obj):
        return obj.academicos.count()
    cantidad_academicos.short_description = "Nº Académicos"

    def academicos_asociados(self, obj):
        if obj.academicos.exists():
            return mark_safe("<br>".join([a.nombre for a in obj.academicos.all()]))
        return "—"
    academicos_asociados.short_description = "Académicos del Departamento"


@admin.register(Academico)
class AcademicoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'departamento', 'especialidad','cargos_display')
    search_fields = ('nombre', 'departamento', 'especialidad', 'cargo','cargos__nombre')
    list_filter = ('departamento','cargos') 
    filter_horizontal = ('escuelas', 'programas_postgrado','cargos')
    def cargos_display(self, obj):
        return ", ".join(c.nombre for c in obj.cargos.all())
    cargos_display.short_description = 'Cargos'

@admin.register(Cargo)
class CargoAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)


@admin.register(Estudiante)
class EstudianteAdmin(admin.ModelAdmin):
    list_display = ('user', 'carrera', 'año_ingreso', 'rut')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'rut')

admin.site.register(Sala)
admin.site.register(Reserva)
# admin.site.register(Aviso)
# from django.contrib import admin
# from .models import Aviso

@admin.register(Aviso)
class AvisoAdmin(admin.ModelAdmin):
    list_display = (
        'academico_nombre',
        'departamento',
        'destino',
        'tipo_actividad',
        'fecha_salida',
        'fecha_regreso',
        'creado',
    )
    list_filter = ('tipo_actividad', 'fecha_salida', 'fecha_regreso')
    search_fields = ('academico__nombre', 'destino')

    def academico_nombre(self, obj):
        return obj.academico.nombre
    academico_nombre.short_description = 'Académico'

    def departamento(self, obj):
        return obj.academico.departamento
    departamento.short_description = 'Departamento'




@admin.register(Publicacion)
class PublicacionAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'academico', 'anio', 'tipo', 'visible')
    search_fields = ('titulo', 'autores', 'revista', 'doi')
    list_filter = ('anio', 'tipo', 'visible')

admin.site.register(Escuela)
class EscuelaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'departamento')

admin.site.register(ProgramaPostgrado)