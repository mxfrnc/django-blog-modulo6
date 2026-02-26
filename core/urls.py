from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('post/<slug:slug>/', views.detalle_post, name='detalle_post'),
    path('crear/', views.crear_post, name='crear_post'),
    path('nosotros/', views.nosotros, name='nosotros'),
]