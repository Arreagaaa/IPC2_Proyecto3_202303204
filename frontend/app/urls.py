from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('configuracion/', views.upload_configuration, name='upload_configuration'),
    path('consumo/', views.upload_consumption, name='upload_consumption'),
    path('inicializar/', views.initialize_system, name='initialize_system'),
    path('consultar/', views.query_data, name='query_data'),
    path('estudiante/', views.student_info, name='student_info'),
]
