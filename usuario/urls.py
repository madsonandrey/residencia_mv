from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('dashboard/', views.dash, name='dash'),
    path('cadastro/', views.cadastrar, name='cadastrar'),
    path('editar/<int:usuario_id>', views.editar, name='editar'),
    path('deletar/<int:usuario_id>', views.deletar_usuario, name='deletar_usuario'),
    path('lista/', views.listar, name='listar'),
    path('logout', views.logout, name='logout'),

    # Exames
    path('cadastrar_exame/', views.novo_exame, name='novo_exame')
]
