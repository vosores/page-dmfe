from django.contrib import admin
from jornada import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from jornada.views import login_view
from jornada.views import exportar_cv_pdf
from django.contrib.auth.views import LogoutView
from django.contrib.auth.views import PasswordChangeDoneView
from jornada.views import CustomPasswordChangeView, CustomPasswordChangeDoneView
from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from jornada.views import filtroposgrado_por_departamento


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', login_view, name='login'),
    path('logout/', views.logout_and_redirect, name='logout'),
    path('academicos/', include('jornada.urls')),
    path('', views.portada, name='portada'),
    path('malla_im/', views.malla_im, name='malla_im'),
    path('ima/', views.ima, name='ima'),
    path('reserva/', views.reservar_sala, name='reservar_sala'),
    path('calendario/', views.render_calendar, name='calendario'),
    path('api/reservas/', views.api_reservas, name='api_reservas'),
    path('api/reservas/<int:reserva_id>/', views.api_reservas, name='api_reservas_detail'),
    path('api/verificar_disponibilidad/', views.verificar_disponibilidad, name='verificar_disponibilidad'),

    path('material/', views.material, name='material'),
    path('academicos/', views.lista_academicos, name='lista_academicos'),
    


    path(
        'academico/<slug:slug>/embed/',
        views.perfil_academico_embed,
        name='perfil_academico_embed'
    ),
    path('academico/<slug:slug>/', views.detalle_academico, name='detalle_academico'),
    path('password_change/', 
         CustomPasswordChangeView.as_view(), 
         name='password_change'),
    path('password_change_hecho/', 
         CustomPasswordChangeDoneView.as_view(), 
         name='password_change_hecho'),
    path('password_reset/', 
         auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'),
         name='password_reset'),
    path('password_reset/done/', 
         auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('reset/done/', 
         auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
         name='password_reset_complete'),
    path('material_apuntes/', views.material_apuntes, name='material_apuntes'),
    path('subir_archivo/', views.subir_archivo, name='subir_archivo'),
    path('eliminar_archivo/<int:archivo_id>/', views.eliminar_archivo, name='eliminar_archivo'),
    path('publicar_material/<int:archivo_id>/', views.publicar_material, name='publicar_material'),
    path('academico/<slug:slug>/aviso/', views.crear_aviso, name='crear_aviso'),
    path('avisos/', views.lista_avisos, name='lista_avisos'),
    path('academico/<slug:slug>/agregar_publicacion/', views.agregar_publicacion_doi, name='agregar_publicacion_doi'),
    path('academico/<slug:slug>/agregar-publicacion-manual/', views.agregar_publicacion_manual, name='agregar_publicacion_manual'),
    path('publicacion/<int:pk>/editar/', views.editar_publicacion, name='editar_publicacion'),

    path('publicacion/<int:pk>/editar/', views.editar_publicacion, name='editar_publicacion'),
    path('publicacion/<int:pk>/eliminar/', views.confirmar_eliminar_publicacion, name='confirmar_eliminar_publicacion'),
    path('publicacion/<int:pk>/eliminar/confirmado/', views.eliminar_publicacion, name='eliminar_publicacion'),
    path('academico/<slug:slug>/cv/pdf/', exportar_cv_pdf, name='exportar_cv_pdf'),
    path("academicos/ima/", views.academicos_ima, name="academicos_ima"), # 11 julio 2025
    path("academicos/escuela/<slug:slug>/", views.lista_academicos_por_escuela, name="academicos_por_escuela"),
    
    path('academicos/programa/<slug:slug>/', views.academicos_por_postgrado, name='academicos_por_postgrado'),
    path("escuelas/<slug:slug>/", views.pagina_escuela, name="pagina_escuela"),
    path('postgrados/<slug:slug>/', filtroposgrado_por_departamento, name='postgrados_por_departamento'),
    path('escuelas/<slug:slug>/comite/', views.comite_por_escuela, name='comite_por_escuela'),
    path('escuelas/<slug:slug>/malla/', views.malla_por_escuela, name='malla_por_escuela'),
    path('escuelas/<slug:slug>/representantes/', views.representantes_estudiantiles_por_escuela, name='representantes_por_escuela'),
    path('escuelas/<slug:slug>/informacion/', views.informacion_por_carrera, name='informacion_por_carrera'),
    path('escuelas/<slug:slug>/academicos/', views.lista_academicos_por_escuela, name='lista_academicos_por_escuela'),
    path('academicos/departamento/<slug:slug>/', views.academicos_por_departamento, name='academicos_por_departamento'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
