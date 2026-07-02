from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('agregar/', views.add_player, name='add_player'),
    path('eliminar/<int:player_id>/', views.delete_player, name='delete_player'),
    path('sorteo/', views.sorteo, name='sorteo'),
    path('tier/', views.tier_list, name='tier_list'),
]
