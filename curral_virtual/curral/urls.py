from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_vacas, name='lista_vacas'),
    path('vaca/<int:pk>/', views.detalhe_vaca, name='detalhe_vaca'),
    path('relatorio/', views.relatorio_geral, name='relatorio_geral'),
    path('cadastrar/vaca/', views.cadastrar_vaca, name='cadastrar_vaca'),
    path('cadastrar/ordenha/', views.cadastrar_ordenha, name='cadastrar_ordenha'),
    path('editar/ordenha/<int:pk>/', views.editar_ordenha, name='editar_ordenha'),
    path('deletar/ordenha/<int:pk>/', views.deletar_ordenha, name='deletar_ordenha'),
]