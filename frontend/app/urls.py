from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('configuracion/', views.upload_configuration, name='upload_configuration'),
    path('consumo/', views.upload_consumption, name='upload_consumption'),
    path('inicializar/', views.initialize_system, name='initialize_system'),
    path('consultar/', views.query_data, name='query_data'),
    path('estudiante/', views.student_info, name='student_info'),
    
    # Nuevas rutas Semana 3
    path('facturar/', views.billing, name='billing'),
    path('crear/recurso/', views.create_resource, name='create_resource'),
    path('crear/categoria/', views.create_category, name='create_category'),
    path('crear/cliente/', views.create_client, name='create_client'),
    path('crear/instancia/', views.create_instance, name='create_instance'),
    path('cancelar/instancia/', views.cancel_instance_view, name='cancel_instance'),
    path('facturas/', views.view_invoices, name='view_invoices'),
]
